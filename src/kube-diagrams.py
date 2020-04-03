#!/usr/bin/env python3

import subprocess
import json
import sys
import argparse
from pprint import pprint

from diagrams import Diagram, Cluster
from diagrams.k8s.rbac import ClusterRole, ClusterRoleBinding, Group, RoleBinding, Role, ServiceAccount, User
from diagrams.k8s.infra import ETCD, Master, Node
from diagrams.k8s.podconfig import ConfigMap, Secret
from diagrams.k8s.group import Namespace
from diagrams.k8s.network import Endpoint, Ingress, NetworkPolicy, Service
from diagrams.k8s.others import CRD, PSP
from diagrams.k8s.storage import PersistnetVolume, PersistentVolumeClaim, StorageClass, Volume
from diagrams.k8s.clusterconfig import HorizontalPodAutoscaler, LimitRange, Quota
from diagrams.k8s.controlplane import APIServer, CCM, ControllerManager, KubeProxy, Kubelet, Scheduler
from diagrams.k8s.compute import Cronjob, Deployment, DaemonSet, Job, Pod, ReplicaSet, StatefulSet

def main():

    parser = argparse.ArgumentParser(description='Create Kubernetes diagrams')
    parser.add_argument('-n',
                        required=True,
                        type=str,
                        action = 'store',
                        dest = 'namespace',
                        help='Kubernetes namespace to get objects from')
    args = parser.parse_args()

    command = "kubectl -n "+args.namespace+" get ingress -o json"
    commandOutput = subprocess.run(command.split(), stdout=subprocess.PIPE)
    commandJson = commandOutput.stdout.decode('utf-8')
    ingressList = json.loads(commandJson)

    if len(ingressList["items"]) == 0:
        print("No ingress found. Aboring.")
        sys.exit()
    
    diagramMap = {}
    diagramMap["ingress"] = []
    for ingress in ingressList["items"]:
        ingressMap = {}
        ingressMap["name"] = ingress["metadata"]["name"]
        ingressMap["items"] = []
        for rule in ingress["spec"]["rules"]:
            hostMap = {}
            hostMap["name"] = rule["host"]
            hostMap["items"] = []
            for path in rule["http"]["paths"]:
                pathMap = {}
                pathMap["name"] = path["path"]
                srvName = path["backend"]["serviceName"]
                pathMap["serviceName"] = srvName
                pathMap["items"] = []
                

                command = "kubectl -n "+args.namespace+" get service "+srvName+" -o json"
                print("Running: "+command)
                commandOutput = subprocess.run(command.split(), stdout=subprocess.PIPE)
                commandJson = commandOutput.stdout.decode('utf-8')
                srvObj = json.loads(commandJson)
                
                #kubectl get pods -l environment=production,tier=frontend

                filter = ""
                for selector in srvObj["spec"]["selector"]:
                    if filter != "":
                        filter = ","+filter
                    filter = selector+"="+srvObj["spec"]["selector"][selector]
                
                
                command = "kubectl -n "+args.namespace+" get pods -l "+filter+" -o json"
                print("Running: "+command)
                commandOutput = subprocess.run(command.split(), stdout=subprocess.PIPE)
                commandJson = commandOutput.stdout.decode('utf-8')
                podsList = json.loads(commandJson)

                for pod in podsList["items"]:
                    podMap = {}
                    podMap["name"] = pod["metadata"]["name"]
                    pathMap["items"].append(podMap)

                hostMap["items"].append(pathMap)
            
            ingressMap["items"].append(hostMap)

        diagramMap["ingress"].append(ingressMap)

    for ingress in diagramMap["ingress"]:
        print(ingress["name"])
        with Diagram("auto_"+ingress["name"], show=False):
            dIngress = Ingress(ingress["name"])
            for host in ingress["items"]:
                print(host["name"])
                with Cluster(host["name"]):
                    for path in host["items"]:
                        print(path["name"])
                        print(path["serviceName"])
                        with Cluster(path["name"]):
                            dSrv = Service(path["serviceName"])
                            for pod in path["items"]:
                                dSrv >> Pod(pod["name"])
                            dIngress >> dSrv

    sys.exit()

if __name__ == '__main__':
    main()