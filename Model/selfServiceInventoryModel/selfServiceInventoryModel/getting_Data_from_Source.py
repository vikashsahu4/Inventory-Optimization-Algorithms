
import numpy as np
import pandas as pd
import csv
class read_from_csv(object):
    def __init__(self,path_to_csv,cols=None):
        '''Constructor to initialize the bound object.'''
        self.path=path_to_csv
        self.cols=cols
        self.last=[]
        self.typeOfDataToBeInCSVFile = [int,float]
    
    def noOfColumns(self):
        return len(self.cols)
        
    def generator(self,dataInColumn):
        for i in dataInColumn:
            yield(i.item())

    def using_clump(self, a):
        return [a[s] for s in np.ma.clump_unmasked(np.ma.masked_invalid(a))]
        
    def dataFetchedFromCSVFile(self,param=None):
        try:
            with open(self.path, "r") as f:
                d_reader = csv.DictReader(f)
                headers = d_reader.fieldnames
            if((self.cols is None) or (len(self.cols)==0)):
                self.cols=headers
            data = pd.read_csv(self.path, usecols=self.cols)
            # if param=='news_vendor':
            #     inc=0;cols=[]
            #     for column in self.cols:
            #         if inc != 0:
            #             cols.append(column)
            #         inc=inc+1
            #     self.cols=cols
            if param == 'p_r_l':
                try:
                    partRepairRate=data[headers[0]][0]
                    bufferPercentage=data[headers[1]][0]
                    site1ForLRPVolumes=[];site2ForLRPVolumes=[];site1ForTotalLoopCycle=[];site2ForTotalLoopCycle=[]
                    for i in list(range(len(data[headers[2]]))):
                        site1ForLRPVolumes.append(data[headers[2]][i])
                        site2ForLRPVolumes.append(data[headers[3]][i])
                        site1ForTotalLoopCycle.append(data[headers[5]][i])
                        site2ForTotalLoopCycle.append(data[headers[6]][i])
                    return [partRepairRate,bufferPercentage,site1ForLRPVolumes,site2ForLRPVolumes,site1ForTotalLoopCycle,site2ForTotalLoopCycle]
                except Exception:
                    raise Exception("Please check the input values again and try again")
            if param =="forecast":
                try:
                    falseLeadtime =data[headers[0]][0]
                    serviceLevel =data[headers[1]][0]
                    self.cols=self.cols[2:]
                    data = pd.read_csv(self.path, usecols=self.cols)
                    ww=[];forecast=[];demand=[];
                    ww_for_forecast_lumpy=[];demand_for_forecast_lumpy=[];
                    for i in list(range(len(data[headers[2]]))):
                        ww.append(data[headers[2]][i])
                        forecast.append(data[headers[3]][i])
                        demand.append(data[headers[4]][i])
                    checkingTheIndexForNaN =pd.isnull(data).any(1).nonzero()[0]
                    diff1=(len(data[headers[5]])-len(checkingTheIndexForNaN))
                    for i in list(range(diff1)):
                        ww_for_forecast_lumpy.append(data[headers[5]][i])
                        demand_for_forecast_lumpy.append(data[headers[6]][i])
                    return [falseLeadtime,serviceLevel,ww,forecast,demand,ww_for_forecast_lumpy,demand_for_forecast_lumpy]
                except Exception:
                    raise Exception("Please check the input values again and try again")
            if param =="mcb":
                try:
                    falseLeadtime=data[headers[0]][0]
                    serviceLevel = data[headers[1]][0]
                    self.cols=self.cols[2]
                    data = pd.read_csv(self.path, usecols=self.cols)
                    print(data)
                    demand=[]
                    print(len(data[headers[2]]))
                    for i in list(range(len(data[headers[2]]))):
                        demand.append(data[headers[2]][i])
                    return [falseLeadtime,serviceLevel,demand]
                except Exception:
                    raise Exception("Please check the input values and try again")

            if param == "batch_mcb":
                try:
                    df = pd.read_csv(self.path, header=0)
                    #print(df[0])
                    falseLeadtime = self.using_clump(df[headers[0]].tolist())
                    #print('falseLeadtime ', falseLeadtime)
                    serviceLevel = self.using_clump(df[headers[1]].tolist())
                    demand = self.using_clump(df[headers[2]].tolist())
                    return falseLeadtime, serviceLevel, demand
                except Exception as e:
                    print('error in parsing', e)
                    raise Exception("Error in parsing batch mcb")
            for column in self.cols:
                tempList =[]
                dataInColumn=data.loc[:,column]
                c=self.generator(dataInColumn)
                for count in list(range(len(dataInColumn)-dataInColumn.isnull().values.sum())):
                    backupVar = next(c)
                    if type(backupVar) in self.typeOfDataToBeInCSVFile:
                        tempList.append(backupVar)
                self.last.append(tempList)
                #arr = np.append(arr,np.array(self.last))
            arr=np.array(self.last)
            return arr
            #return self.last
        except Exception:
            raise Exception("Please check the input values again and try again")
            
            
    
   

        
