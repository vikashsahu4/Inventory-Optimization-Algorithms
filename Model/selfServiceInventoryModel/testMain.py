from imp import reload
import sys
import selfServiceInventoryModel
import selfServiceInventoryModel.getting_Data_from_Source as t
from selfServiceInventoryModel import DemandAnalyzer
from selfServiceInventoryModel.DemandAnalyzer import demandAnalyzer as da
import selfServiceInventoryModel.EOQ as eoq
import selfServiceInventoryModel.ForecastAnalyzer as fa
import selfServiceInventoryModel.safety_stock_multiplier as ss
import selfServiceInventoryModel.newsVendor as nv
import selfServiceInventoryModel.ForecastErrorBased_Standard as fc
import selfServiceInventoryModel.forecast_LumpyDemand as fl
import selfServiceInventoryModel.mcb_demand as md
import selfServiceInventoryModel.mcb_demand_batch as mdb
import selfServiceInventoryModel.ContainerLoop as cl
import selfServiceInventoryModel.DependentDemand as dd
import selfServiceInventoryModel.PartRepairLoop as prl
import selfServiceInventoryModel.PoissonModel as p
import selfServiceInventoryModel.ForecastRealignment as fr
import pandas,datetime
import numpy as np
import pandas as pd
import json
from collections import OrderedDict
import datetime
   

def DemandAnalyzer(path,pathOfErrorFile):
    flag = True
    try:
        print("\n\n====================================================================================================")
        get = t.read_from_csv(path)
        data=get.dataFetchedFromCSVFile()
        obj=da.displayResult(data)
        s=json.dumps(obj)
        jsonObj=json.loads(s)
        print(jsonObj)
        return obj
        '''
        if type(data) ==str:
            print(data)
        else:
            if data.any():
                if get.noOfColumns() ==1:
                    result=displayResult(data)
                    if result['Discrete Indicator Flag'] == 1:
                        result['Discrete Indicator Flag'] =True
                    else:
                        result['Discrete Indicator Flag'] =False
                    s=json.dumps(result)
                    jsonObj=json.loads(s)
                    print(jsonObj)
                    print("\n\n\n")
                else:
                   for inputData in data:
                       result=displayResult(inputData)
                       if result['Discrete Indicator Flag'] == 1:
                           result['Discrete Indicator Flag'] =True
                       else:
                           result['Discrete Indicator Flag'] =False
                       s=json.dumps(result)
                       jsonObj=json.loads(s)
                       print(jsonObj)
                       print("\n\n\n")
        '''
    except Exception as e:
        flag = False
        orig_stdout = sys.stdout
        f = open(pathOfErrorFile,"w")
        sys.stdout = f
        print("The error occured in the execution of the DemandAnalyzer modules is ---------------------------\n\n\n")
        print(e)
        sys.stdout = orig_stdout
        f.close()
    return flag
    
def EOQ(path,pathOfErrorFile):
    flag = True
    try:
        print("\n\n====================================================================================================")
        get=t.read_from_csv(path)
        data=get.dataFetchedFromCSVFile()
        avgDemand,purchaseCost,orderingCost,holdingCost=data
        obj=eoq.Eoq(avgDemand=float(avgDemand[0]),purchaseCost=float(purchaseCost[0]),orderingCost=float(orderingCost[0]),holdingCost=float(holdingCost[0]))
        obj.demandAnalysis()
        obj.orderAnalysis()
        Result=obj.returnTheData()
        print(Result)
        json_format=json.dumps(Result)
        print(json_format)
        #remove
        return Result
    except Exception as e:
        flag = False
        orig_stdout = sys.stdout
        f = open(pathOfErrorFile,"w")
        sys.stdout = f
        print("The error occured in the execution of the EOQ modules is ---------------------------\n\n\n")
        print(e)
        sys.stdout = orig_stdout
        f.close()
    return flag

def ForecastAnalyzer(path,pathOfErrorFile):
    flag = True
    try:
        print("====================================================================================================\n")
        get=t.read_from_csv(path)
        data=get.dataFetchedFromCSVFile()
        forecastData,demadData=data
        obj=fa.Forecast_Analyzer(forecastData=forecastData,demadData=demadData)
        result= obj.outputToGetUII()
        s=json.dumps(result)
        jsonObj=json.loads(s)
        print(jsonObj)
        return result
    except Exception as e:
        flag = False
        orig_stdout = sys.stdout
        f = open(pathOfErrorFile,"w")
        sys.stdout = f
        print("The error occured in the execution of the Forecast Analyzer module is ---------------------------\n\n\n")
        print(e)
        sys.stdout = orig_stdout
        f.close()
    return flag

def RSPeriodicReview(path=None,pathOfErrorFile=None,model=None):
    flag = True
    print(model)
    try:
        print("\n\n====================================================================================================")
        get=t.read_from_csv(path)
        data=get.dataFetchedFromCSVFile()
        json_format_Output =ss.main(data,model='RSPeriodicReview')
        s=json.dumps(json_format_Output)
        jsonObj=json.loads(s)
        print(jsonObj)
        return json_format_Output
    except Exception as e:
        flag = False
        orig_stdout = sys.stdout
        f = open(pathOfErrorFile,"w")
        sys.stdout = f
        print("The error occured in the execution of the (R,S) Periodic Review is ---------------------------\n\n\n")
        print(e)
        sys.stdout = orig_stdout
        f.close()
    return flag  

def SQContinousReview(path=None,pathOfErrorFile=None,model=None):
    flag = True
    try:
        print("\nMoved to (s,Q) Continuous Review================================\n")
        starttime=datetime.datetime.now()
        get=t.read_from_csv(path)
        data=get.dataFetchedFromCSVFile()
        json_format_Output =ss.main(data,model='SQContinousReview')
        s=json.dumps(json_format_Output)
        jsonObj=json.loads(s)
        print(jsonObj)
        endtime=datetime.datetime.now()
        print("sf",endtime-starttime)
        return json_format_Output
    except Exception as e:
        flag = False
        orig_stdout = sys.stdout
        f = open(pathOfErrorFile,"w")
        sys.stdout = f
        print("The error occured in the execution of the (s,Q) Continuous Review is ---------------------------\n\n\n")
        print(e)
        sys.stdout = orig_stdout
        f.close()
    return flag  

def NewsVendor(path=None,pathOfErrorFile=None):
    flag = True
    try:
        print("\n\n=====================================================================================================")
        get=t.read_from_csv(path)
        data=get.dataFetchedFromCSVFile()
        print(data)
        mean, sd, cost, price=data
        json_format_Output =nv.mainnewsVendorFunction(mean, sd, cost, price)
        s=json.dumps(json_format_Output)
        jsonObj=json.loads(s)
        print(jsonObj)
        return json_format_Output
    except Exception as e:
        flag = False
        orig_stdout = sys.stdout
        f = open(pathOfErrorFile,"w")
        sys.stdout = f
        print("The error occured in the execution of the NewsVendor modules is ---------------------------\n\n\n")
        print(e)
        sys.stdout = orig_stdout
        f.close()
    return flag  

def ForecastErrorBasedStandard(path,pathOfErrorFile):
    flag = True
    try:
        print("\n\n======================================================================================================")
        print("\nMoved to ForeCastErrorBased Standard Module================================\n")
        get=t.read_from_csv(path)
        falseLeadtime,serviceLevel,ww,forecast,demand,ww_for_forecast_lumpy,demand_for_forecast_lumpy=get.dataFetchedFromCSVFile(param="forecast")
        futureForecast =list(map(lambda x:x.item(),demand_for_forecast_lumpy))
        json_format_Output=fc.foreCastErrorBased_Standard_Function(falseLeadtime,serviceLevel,ww,forecast,demand,futureForecast)
        #json_format_Output_for_forecast_lumpy =fl.ForeCastLumpyDemand(falseLeadtime,serviceLevel,forecast,demand,futureForecast)
        #output=json_format_Output_for_forecast_lumpy.actionOnForcastLumpy()
        s=json.dumps(json_format_Output)
        jsonObj=json.loads(s)
        print(jsonObj)
        return json_format_Output
    except Exception as e:
        flag = False
        orig_stdout = sys.stdout
        f = open(pathOfErrorFile,"w")
        sys.stdout = f
        print("The error occured in the execution of the ForeCastErrorBased Standard modules is ---------------------------\n\n\n")
        print(e)
        sys.stdout = orig_stdout
        f.close()
    return flag 
    
def MCBDemand(path,pathOfErrorFile):
    flag = True
    try:
        print("\n\n======================================================================================================")
        starttime=datetime.datetime.now()
        get=t.read_from_csv(path)
        falseLeadtime,serviceLevel,demand=get.dataFetchedFromCSVFile()
        falseLeadtime,serviceLevel,demand=int(falseLeadtime[0]),serviceLevel[0],demand
        obj=md.mcbDemand(falseLeadtime,serviceLevel,demand)
        json_format_Output=obj.actionOnMcbDemand()
        s=json.dumps(json_format_Output)
        jsonObj=json.loads(s)
        print(jsonObj)
        endtime=datetime.datetime.now()
        print("Time Taken",endtime-starttime)
        return json_format_Output
    except Exception as e:
        flag = False
        orig_stdout = sys.stdout
        f = open(pathOfErrorFile,"w")
        sys.stdout = f
        print("The error occured in the execution of the Mcb Demand modules is ---------------------------\n\n\n")
        print(e)
        sys.stdout = orig_stdout
        f.close()
    return flag
    
def ContainerLoop(path,pathOfErrorFile):
    flag = True
    try:
        print("\n\n======================================================================================================")
        print("\nMoved to Container Loop Module================================\n")
        get=t.read_from_csv(path)
        YYYYMM,containerSize,bufferPercentage,site1LRPVolumes,site2LRPVolumes,site3LRPVolumes,site1ForLoopCycle,site2ForLoopCycle,site3ForLoopCycle,manualBuffer1,manualBuffer2,manualBuffer3=get.dataFetchedFromCSVFile()
        obj=cl.ContainerLoop(YYYYMM,containerSize,bufferPercentage,site1LRPVolumes,site2LRPVolumes,site3LRPVolumes,site1ForLoopCycle,site2ForLoopCycle,site3ForLoopCycle,manualBuffer1,manualBuffer2,manualBuffer3)
        obj.outputContainersMonth()
        obj.outputContainerFleetPerMonthPerLittlesLaw()
        obj.outputManualBuffer()  
        json_format_Output=obj.returnJsonOutput()
        s=json.dumps(json_format_Output)
        jsonObj=json.loads(s)
        print(jsonObj)
        return json_format_Output
    except Exception as e:
        flag = False
        orig_stdout = sys.stdout
        f = open(pathOfErrorFile,"w")
        sys.stdout = f
        print("The error occured in the execution of the Container Loop modules is ---------------------------\n\n\n")
        print(e)
        sys.stdout = orig_stdout
        f.close()
    return flag
    
def DependentDemand(path,pathOfErrorFile):
    flag = True
    try:
        print("\n\n======================================================================================================")
        print("\nMoved to Dependent Demand Module================================\n")
        get=t.read_from_csv(path)
        YYYYMM,attachRate,dependentPartBusinessProcessLoss,substrateLotSize,capacitorLotSize,site1ForLrpVolumesInMonths,site2ForLrpVolumesInMonths,site3ForLrpVolumesInMonths,yields=get.dataFetchedFromCSVFile()
        obj=dd.dependantDemand(YYYYMM,attachRate,dependentPartBusinessProcessLoss,substrateLotSize,capacitorLotSize,site1ForLrpVolumesInMonths,site2ForLrpVolumesInMonths,site3ForLrpVolumesInMonths,yields)        
        json_format_Output=obj.outputDepedentPartsNeeded()
        s=json.dumps(json_format_Output)
        jsonObj=json.loads(s)
        print(jsonObj)
        return json_format_Output
    except Exception as e:
        flag = False
        orig_stdout = sys.stdout
        f = open(pathOfErrorFile,"w")
        sys.stdout = f
        print("The error occured in the execution of the Dependent Demand modules is ---------------------------\n\n\n")
        print(e)
        sys.stdout = orig_stdout
        f.close()
    return flag
    
def PartRepairLoop(path,pathOfErrorFile):
    flag = True
    try:
        #print("\n\n======================================================================================================")
        print("\nMoved to Part Repair Loop Module================================\n")
        get=t.read_from_csv(path)
        #data=get.dataFetchedFromCSVFile()
        #print(data)
        YYYYMM,partRepairRate,bufferPercentage,site1ForLRPVolumes,site2ForLRPVolumes,site3ForLRPVolumes,site1ForTotalLoopCycle,site2ForTotalLoopCycle,site3ForTotalLoopCycle,manualBuffer1,manualBuffer2,manualBuffer3=get.dataFetchedFromCSVFile()
        obj=prl.partRepairLoop(YYYYMM,partRepairRate,bufferPercentage,site1ForLRPVolumes,site2ForLRPVolumes,site3ForLRPVolumes,site1ForTotalLoopCycle,site2ForTotalLoopCycle,site3ForTotalLoopCycle,manualBuffer1,manualBuffer2,manualBuffer3)
        #obj=prl.partRepairLoop(data)                
        json_format_Output=obj.calculatingOnPartRepairLoopFeatures()
        s=json.dumps(json_format_Output)
        jsonObj=json.loads(s)
        print(jsonObj)
        return json_format_Output
    except Exception as e:
        flag = False
        orig_stdout = sys.stdout
        f = open(pathOfErrorFile,"w")
        sys.stdout = f
        print("The error occured in the execution of the Part Repair Loop modules is ---------------------------\n\n\n")
        print(e)
        sys.stdout = orig_stdout
        f.close()
    return flag
    
def ForecastLumpyDemand(path,pathOfErrorFile):
    flag = True
    try:
        print("\n\n======================================================================================================")
        startTime = datetime.datetime.now().replace(microsecond=0)
        get=t.read_from_csv(path)
        data=get.dataFetchedFromCSVFile(param='forecast')
        leadTime,serviceLevel,Forecast,Demand,Futureforecast=data[0],data[1],data[3],data[4],data[6]
        futureForecast =list(map(lambda x:x.item(),Futureforecast))
        json_format_Output_for_forecast_lumpy =fl.ForeCastLumpyDemand(leadTime,serviceLevel,Forecast,Demand,futureForecast)
        output=json_format_Output_for_forecast_lumpy.actionOnForcastLumpy()
        s=json.dumps(output)
        jsonObj=json.loads(s)
        print(jsonObj)
        return output
    except Exception as e:
        flag = False
        orig_stdout = sys.stdout
        f = open(pathOfErrorFile,"w")
        sys.stdout = f
        print("The error occured in the execution of the Forecast Lumpy Demand modules is ---------------------------\n\n\n")
        print(e)
        sys.stdout = orig_stdout
        f.close()
    return flag

def PoissonModel(path,pathOfErrorFile):
    flag = True
    try:
        print("\n\n=============================================")
        starttime=datetime.datetime.now()
        get=t.read_from_csv(path)
        DemandMean,FixedOrderingCost,Cost,HoldingCharge,LeadTime,ReorderPoint,CycleServiceLevel,CostperStockoutEvent,ItemFillRate,CostPerItemShort=get.dataFetchedFromCSVFile()
        obj=p.PoissonModel(DemandMean,FixedOrderingCost,Cost,HoldingCharge,LeadTime,ReorderPoint,CycleServiceLevel,CostperStockoutEvent,ItemFillRate,CostPerItemShort)
        json_format_Output =obj.run()
        s=json.dumps(json_format_Output)
        jsonObj=json.loads(s)
        print(jsonObj) 
        endtime=datetime.datetime.now()
        print("Time Taken",endtime-starttime)
        return json_format_Output
    except Exception as e:
        flag = False
        orig_stdout = sys.stdout
        f = open(pathOfErrorFile,"w")
        sys.stdout = f
        print("The error occured in the Poisson Model is ---------------------------\n\n\n")
        print(e)
        sys.stdout = orig_stdout
        f.close()
    return flag

def ForecastRealignment(path,pathOfErrorFile):
    flag = True
    try:
        print("\n\n====================================================================================================")
        get=t.read_from_csv(path)
        Forecast,Demand=get.dataFetchedFromCSVFile()
        obj=fr.ForecastRealignment(Forecast,Demand)
        json_format_Output =obj.run()
        s=json.dumps(json_format_Output)
        jsonObj=json.loads(s)
        print(jsonObj) 
        return json_format_Output
    except Exception as e:
        flag = False
        orig_stdout = sys.stdout
        f = open(pathOfErrorFile,"w")
        sys.stdout = f
        print("The error occured in the Forecast Realignment Model is ---------------------------\n\n\n")
        print(e)
        sys.stdout = orig_stdout
        f.close()
    return flag
    

def BatchModelSQ(path,pathOfErrorFile):
    flag = True
    try:
        print("\nMoved to Batch Mode=======\n")
        get=t.read_from_csv(path)
        data=get.dataFetchedFromCSVFile()
        json_format_Output =ss.main(data,model='SQContinousReview')
        s=json.dumps(json_format_Output)
        jsonObj=json.loads(s)
        print(jsonObj)
        return json_format_Output
    except Exception as e:
        flag = False
        orig_stdout = sys.stdout
        f = open(pathOfErrorFile,"w")
        sys.stdout = f
        print("The error occured in the execution of the batch is ---------------------------\n\n\n")
        print(e)
        sys.stdout = orig_stdout
        f.close()
    return flag

def BatchPoissonModel(path,pathOfErrorFile):
    flag = True
    try:
        print("\n\nBatch Model for Poisson=======")
        get=t.read_from_csv(path)
        DemandMean,FixedOrderingCost,Cost,HoldingCharge,LeadTime,ReorderPoint,CycleServiceLevel,CostperStockoutEvent,ItemFillRate,CostPerItemShort=get.dataFetchedFromCSVFile()
        obj=p.PoissonModel(DemandMean,FixedOrderingCost,Cost,HoldingCharge,LeadTime,ReorderPoint,CycleServiceLevel,CostperStockoutEvent,ItemFillRate,CostPerItemShort)
        json_format_Output =obj.run()
        s=json.dumps(json_format_Output)
        jsonObj=json.loads(s)
        print(jsonObj) 
        return json_format_Output
    except Exception as e:
        flag = False
        orig_stdout = sys.stdout
        f = open(pathOfErrorFile,"w")
        sys.stdout = f
        print("The error occured in the Poisson Model is ---------------------------\n\n\n")
        print(e)
        sys.stdout = orig_stdout
        f.close()
    return fla

def BatchModelSQ(path,pathOfErrorFile):
    flag = True
    try:
        print("\nMoved to Batch Mode=======\n")
        get=t.read_from_csv(path)
        data=get.dataFetchedFromCSVFile()
        #print(data)
        json_format_Output =ss.main(data,model='SQContinousReview')
        s=json.dumps(json_format_Output)
        jsonObj=json.loads(s)
        print(jsonObj)
        return json_format_Output
    except Exception as e:
        flag = False
        orig_stdout = sys.stdout
        f = open(pathOfErrorFile,"w")
        sys.stdout = f
        print("The error occured in the execution of the batch is ---------------------------\n\n\n")
        print(e)
        sys.stdout = orig_stdout
        f.close()
    return flag

def BatchPoissonModel(path,pathOfErrorFile):
    flag = True
    try:
        print("\n\nBatch Model for Poisson=======")
        get=t.read_from_csv(path)
        DemandMean,FixedOrderingCost,Cost,HoldingCharge,LeadTime,ReorderPoint,CycleServiceLevel,CostperStockoutEvent,ItemFillRate,CostPerItemShort=get.dataFetchedFromCSVFile()
        obj=p.PoissonModel(DemandMean,FixedOrderingCost,Cost,HoldingCharge,LeadTime,ReorderPoint,CycleServiceLevel,CostperStockoutEvent,ItemFillRate,CostPerItemShort)
        json_format_Output =obj.run()
        s=json.dumps(json_format_Output)
        jsonObj=json.loads(s)
        print(jsonObj) 
        return json_format_Output
    except Exception as e:
        flag = False
        orig_stdout = sys.stdout
        f = open(pathOfErrorFile,"w")
        sys.stdout = f
        print("The error occured in the Poisson Model is ---------------------------\n\n\n")
        print(e)
        sys.stdout = orig_stdout
        f.close()
    return flag

def BatchMCBDemand(path,pathOfErrorFile):
    flag = True
    try:
        print("\n\n============Entered into Mcb Batch Mode")
        starttime=datetime.datetime.now()
        get=t.read_from_csv(path)
        falseLeadtime, serviceLevel, demand = get.dataFetchedFromCSVFile(param='batch_mcb')
        result = {}
        json_format_Output = []
        # expectation is falseLeadtime, serviceLevel , Demand all are list containing another list
        # hence flt,sl,dm are list objects, change code of dataFetchedFromCSVFile
        for index in range(0, len(falseLeadtime)):
            obj = mdb.mcbDemand(falseLeadtime[index][0], serviceLevel[index][0], demand[index])
            json_format = obj.actionOnMcbDemand()
            json_format_Output.append(json_format)
        result['name'] = 'MCB Demand'
        result['value'] = json_format_Output
        print(result)
        return [result]
    except Exception as e:
        flag = False
        orig_stdout = sys.stdout
        f = open(pathOfErrorFile,"w")
        sys.stdout = f
        print("The error occured in the execution of the Mcb Demand modules is ---------------------------\n\n\n")
        print(e)
        sys.stdout = orig_stdout
        f.close()
    return flag