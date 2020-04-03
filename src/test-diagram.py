
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


with Diagram("test-diagram", show=False):
    ingress = Ingress("in-as-mob")

    with Cluster("as-mob.ambevdevs.com.br"):
        with Cluster("/nonprod/asmob-empregado(/|$)(.*)"):
            ingress >> Service("autenticacao") >> Pod("teste")
        with Cluster("/nonprod/asmob-a(/|$)(.*)"):
            ingress >> Service("autenticacao") >> Pod("teste")
