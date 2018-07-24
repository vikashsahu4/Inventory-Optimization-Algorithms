import math
from collections import OrderedDict
import json
import numpy
#import demjson
class Eoq(object):
    """
            Constructor to create an EOQModel object
            Parameters
            ---------
            avgDemand: Yearly average demand this value must be > 0
            purchaseCost: Variable purchase cost per unit
            orderingCost: Fixed ordering cost per order
            holdingCost: Fixed holding cost of holding (a unit for a year)
    """ 
    res={}   
    def __init__(self, avgDemand, purchaseCost, orderingCost, holdingCost):
        if (avgDemand > 0 and purchaseCost > 0 and orderingCost > 0 and holdingCost > 0): 
            self.avgDemand = avgDemand
            self.purchaseCost = purchaseCost
            self.orderingCost = orderingCost
            self.holdingCost = holdingCost
            self.mEOQ = math.sqrt((2*orderingCost*avgDemand)/holdingCost)
            self.mCycleTime = self.mEOQ/avgDemand
            self.mNumOrders = 1/self.mCycleTime
            self.mTotalRelCost = math.sqrt(2*orderingCost*avgDemand*holdingCost)
            self.mTotalCost = self.mTotalRelCost+purchaseCost*avgDemand
            self.dictForDemandAnalysis=[]
            self.dictForOrderAnalysis=[]
        else:
            raise Exception("Please check the values and re-enter")
            exit()
        
    def privateEOQ(self,orderingCost,avgDemand,holdingCost):
        return math.sqrt((2*orderingCost*avgDemand)/holdingCost)

    def EOQ(self):
        return self.mEOQ
            
    def cycleTime(self):
        return self.mCycleTime
        
    def numOrders(self):
        return self.mNumOrders
        
    def totalRelCost(self):
        return self.mTotalRelCost
        
    def totalCost(self):
        return self.mTotalCost
    
    """
    This prints the results of the demand sensitivity analysis in form of a table
    """
    def demandAnalysis(self):
        localdemandList=[]
        json_format1=OrderedDict()
        normal_list =[]
        #Scale |     Actual |   Forecast | Actual EOQ | Forecast EOQ |  EOQ Ratio |  TRC Ratio
        json_format1['name']="Demand Analysis"
        json_format =OrderedDict()
        demandScaleValue = [0.1,0.5,0.75,0.9,1.0,1.5,2.0]
        for scale in demandScaleValue:
            actEOQ = self.privateEOQ(self.orderingCost,(self.avgDemand*scale),self.holdingCost)
            data=OrderedDict([
                ('Scale',round(scale,3)),
                ('Actual',((self.avgDemand*scale))),
                ('Forecast',(self.avgDemand)),
                ('Actual EOQ',round(actEOQ,3)),
                ('Forecast EOQ',round(self.mEOQ,3)),
                ('EOQ Ratio',round((actEOQ/self.mEOQ*100),3)),
                ('TRC Ratio',round((.5*100*((self.mEOQ/actEOQ)+(actEOQ/self.mEOQ))),3))
                ])
            normal_list.append(data)
        json_format1['value']=normal_list
        self.dictForDemandAnalysis= json_format1
        
    """
    This prints the result of the order size sensitivity analysis in form of a table
    """
    def orderAnalysis(self):
        localOrderAnalysisList=[]
        json_format ={}
        json_format1={}
        normal_list =[]
        orderScaleValue = [2,1.5,1,.5,.05]
        json_format1['name']="Order Analysis"
        for scale in orderScaleValue:
            variableOrderingCost = (self.orderingCost*self.avgDemand)/(self.mEOQ*scale)
            variableHoldingCost = self.holdingCost*(self.mEOQ*scale)/2
            p=((variableOrderingCost + variableHoldingCost)/self.mTotalRelCost)
            data=OrderedDict([
                ('Scale', scale),
                ('Optimal Order',round(self.mEOQ,3)),
                ('Actual Order',round(((self.mEOQ)*scale),3)),
                ('Ordering Cost',round(variableOrderingCost,3)),
                ('Holding Cost',round(variableHoldingCost,3)),
                ('TRC Ratio(%)',round(p*100,3))
                ])
            normal_list.append(data)
        json_format1['value']=normal_list
        self.dictForOrderAnalysis=OrderedDict(json_format1)
        
    def returnTheData(self):
        try:
            lis=[]
            res={}
            json_format={}
            res['name']='Output for EOQ'
            json_format['Order Cycle Time']= self.mCycleTime*365
            json_format['EOQ']=self.privateEOQ(self.orderingCost,self.avgDemand,self.holdingCost)
            json_format['Number of Orders']=self.mNumOrders
            json_format['Total Relevant Cost']=self.mTotalRelCost
            json_format['Total Cost']=self.mTotalCost
            res['value']=[OrderedDict(json_format)]
            lis.append(self.dictForDemandAnalysis)
            lis.append(self.dictForOrderAnalysis)
            lis.append(res)
            print(lis)
            return lis
        except Exception:
            res['error']="Error in processing EOQ model. Please check the values and try again"
            raise Exception(res)
            

# if __name__ == '__main__':
#     b = numpy.array([50])
#     a = numpy.array([20])
#     obj = Eoq(200,50,100,13)
#     obj.demandAnalysis()
#     obj.orderAnalysis()
#     Result=obj.returnTheData()

   
#     print(' result ',Result)
