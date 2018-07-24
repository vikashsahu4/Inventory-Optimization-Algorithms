import argparse
import subprocess
import os
import sys
import testMain
#reload(testMain)
from testMain import *

class returnAllModules(object):
    def allModules(self):
        list =['DemandAnalyzer','EOQ','ForecastAnalyzer','RSPeriodicReview','SQContinousReview','NewsVendor','ForecastErrorBasedStandard','MCBDemand',"ContainerLoop","DependentDemand","PartRepairLoop","ForecastLumpyDemand"]
        return list
        
class OutputStream(object):
    'Class that will return all the models'
    def outputToFile(self,pathOfOutputFile):
        with open(pathOfOutputFile,'w') as f:
            obj =returnAllModules()
            allModelsName =obj.allModules()
            f.write(str(allModelsName))
            f.close()
            
def deleteTheOutputFile(pathOfOutputFile,pathOfErrorFile):
    if os.path.exists(pathOfOutputFile):       
        os.remove(pathOfOutputFile)
    if os.path.exists(pathOfErrorFile):       
        os.remove(pathOfErrorFile)
        
def actionOnModule(path,pathOfOutputFile,pathOfErrorFile,moduleName):
    orig_stdout = sys.stdout
    f = open(pathOfOutputFile,"a")
    sys.stdout = f
    #calling the required module
    result = globals()[moduleName](path,pathOfErrorFile)
    if not result:
        pass
    sys.stdout = orig_stdout
    f.close()
    
def Main():
    try:
        parser= argparse.ArgumentParser()
        #parser.add_argument("listOfAllselfServiceInventoryModels",help="The list of all SelfServiceInventoryModels",type=list)
        parser.add_argument("path",help="The path of the csv file of the module",type=str)
        parser.add_argument("module_name",help="The module name",type=str)
        parser.add_argument("-o","--output",help="Output of result to the outputfile",action="store_true")
        parser.add_argument("pathOfOutputFile",help="Path Of OutputFile",type=str)
        parser.add_argument("-e","--error",help="Error of result to the errorfile",action="store_true")
        parser.add_argument("pathOfErrorFile",help="Path Of Errorfile",type=str)
        args=parser.parse_args()
        module_name=args.module_name
        pathOfOutputFile=args.pathOfOutputFile
        pathOfErrorFile=args.pathOfErrorFile
        deleteTheOutputFile(pathOfOutputFile,pathOfErrorFile)
        #'Class that will return all the models'
        objForOS =returnAllModules()
        listOfAllModules =objForOS.allModules()
        outputFile =OutputStream()
        outputFile.outputToFile(pathOfOutputFile)
        path=args.path
        if args.output and args.pathOfOutputFile and args.pathOfErrorFile and args.error:
            actionOnModule(path,pathOfOutputFile,pathOfErrorFile,args.module_name)
        else:
            print("User didn't provide the complete command line argument.So give the option")
    except IOError as e:
            print("File Didn't found")
    
    
#parser.add_argument("path1",help="The csv path of the module",type= argparse.FileType)
#print(args.path1)
if __name__ == '__main__':
    Main()
    