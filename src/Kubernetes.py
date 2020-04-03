import json
import subprocess
import sys

class Api:
    def getAllKinds(self):
        apiKindList = []

        command = "kubectl api-resources"
        commandOutput = subprocess.run(command.split(), stdout=subprocess.PIPE)

        isNamespaced = None
        for result in commandOutput.stdout.decode('utf-8').split():
            
            if isinstance(isNamespaced, (bool)):
                apiKind = ApiKind(result.lower(), isNamespaced)
                apiKindList.append(apiKind)
                isNamespaced = None

            if result == "true":
                isNamespaced = True

            if result == "false":
                isNamespaced = False
        
        #for kind in apiKindList:
        #    print(kind.toJson())

        return apiKindList

class ApiKind:
    def __init__(self, name, isNamespaced):
        self.name = name
        self.isNamespaced = isNamespaced

    def toJson(self):
        jsonStr = json.dumps(self.__dict__)
        return jsonStr