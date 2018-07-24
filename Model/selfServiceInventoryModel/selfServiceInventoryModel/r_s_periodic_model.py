# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 11:25:57 2016

@author: vksahu
"""

'Represents class r,s periodic review. In this module we return Reorder point from each function to the main test file'
'For Safety Stock multiplier I have to import results from safety stock multiplier.py for "To meet Item Fill Rate Function"'

import math
import scipy.special

class RS_Periodic_Review(object):
    def __init__(self,Demand_Mean,Demand_Sigma,Fixed_Ordering_Cost,Cost_of_Acquisition,Holding_Charge,Lead_Time,Review_Period,Cycle_Service_Level,Cost_per_Stockout_Event,Item_Fill_Rate,Cost_Per_Item_Short):
        if(Demand_Mean>0 and Demand_Sigma>0 and Fixed_Ordering_Cost>0 and Cost_of_Acquisition>0 and Holding_Charge>0 and Lead_Time>0 and Review_Period>0 and Cycle_Service_Level>0 and Cost_per_Stockout_Event>0 and Item_Fill_Rate>0 and Cost_Per_Item_Short>0):

            self.demandMean=Demand_Mean
            self.demandSigma=Demand_Sigma
            self.fixedOrderedCost=Fixed_Ordering_Cost
            self.costOfAcquisition=Cost_of_Acquisition
            self.holdingCharge=Holding_Charge
            self.leadTime=Lead_Time
            self.reviewPeriod=Review_Period
            self.cycleServiceLevel=Cycle_Service_Level
            self.costPerStockoutEvent=Cost_per_Stockout_Event
            self.itemFillRate=Item_Fill_Rate
            self.costPeritemShort=Cost_Per_Item_Short
            #print(self.demandMean,self.demandSigma,self.fixedOrderedCost,self.holdingCharge,self.leadTime)
            #print("111111111111111111111111")
            '''
            self.demandMean=300
            self.demandSigma=100
            self.fixedOrderedCost=3270
            self.costOfAcquisition=25
            self.holdingCharge=50
            self.leadTime=(1/52)
            self.reviewPeriod=(4/52)
            self.cycleServiceLevel=99
            self.costPerStockoutEvent=25
            self.itemFillRate=99
            self.costPeritemShort=45
            '''
        else:
            raise Exception("Please check the input values and re-enter")
            exit()

    def commonCalculations(self):
        ##########################'Common Calculations'###################################
        self.Unit_Holding_Cost= ((self.holdingCharge/100)*self.costOfAcquisition)
        self.Order_Quantity = (self.demandMean*self.reviewPeriod)
        self.Mean_of_Demand_over_lead_time =((self.demandMean)*(self.leadTime+self.reviewPeriod))
        self.Sigma_of_Demand_over_lead_time=(self.demandSigma * math.sqrt(self.leadTime+self.reviewPeriod))
        self.Cost_of_Cycle_Stock= (self.Unit_Holding_Cost *((self.demandMean*self.reviewPeriod)/2))
        return [self.Unit_Holding_Cost,self.Order_Quantity,self.Mean_of_Demand_over_lead_time,self.Sigma_of_Demand_over_lead_time,self.Cost_of_Cycle_Stock]
        
    def toMeetcycleServiceLevel(self):
        ####################'To Meet Cycle Service Level:'############################
        per=self.cycleServiceLevel
        per=per/100
        Safety_Stock_Multiplier= scipy.special.ndtri(per)
        Safety_Stock= Safety_Stock_Multiplier*self.Sigma_of_Demand_over_lead_time
        Cost_of_Safety_Stock= Safety_Stock*self.Unit_Holding_Cost
        Reorder_Point= self.Mean_of_Demand_over_lead_time+Safety_Stock
        return Reorder_Point
        
    def toMeetItemFillRate(self,safety_stock_multiplier_val=0,flag=False):
        ##########################'To Meet Item Fill Rate'##############################
        Unit_Normal_Loss_Value = self.Order_Quantity/self.Sigma_of_Demand_over_lead_time*(1-(self.itemFillRate/100))
        if not flag:
            return Unit_Normal_Loss_Value
        else:
            self.Safety_Stock_Multiplier=safety_stock_multiplier_val
            Safety_Stock=(self.Sigma_of_Demand_over_lead_time*self.Safety_Stock_Multiplier)
            Reorder_Point=(self.Mean_of_Demand_over_lead_time+Safety_Stock)
            return Reorder_Point
            
    def toMinimizeStockoutCost(self):
        ################################'To Minimize Stockout Cost'##################################
        flag=True
        x = math.sqrt(2*(math.pi))
        #############'<-- If less than or equal 1, then use other method'
        Limit=self.costPerStockoutEvent*self.demandMean/(self.Unit_Holding_Cost*self.Order_Quantity*self.Sigma_of_Demand_over_lead_time*x)
        if Limit <=1:
            flag=False
        if not flag:
            return flag
        else:
            Safety_Stock_Multiplier = math.sqrt(2*math.log(Limit))
            Safety_Stock =  self.Sigma_of_Demand_over_lead_time*Safety_Stock_Multiplier
            Reorder_Point = self.Mean_of_Demand_over_lead_time + Safety_Stock
            return Reorder_Point
        
    def toMinimizeCostPerItemShort(self):
        ############################'To Minimize Cost Per Item Short'################################
        flag=True
        Cost_Ratio = (self.Unit_Holding_Cost*self.Order_Quantity)/(self.costPeritemShort*self.demandMean)
        if ((Cost_Ratio > 1) or (Cost_Ratio < 0)):
            flag=False
        if not flag:
            return flag
        else:
            self.Safety_Stock_Multiplier = scipy.special.ndtri(1-Cost_Ratio)
            Safety_Stock =(self.Safety_Stock_Multiplier*self.Sigma_of_Demand_over_lead_time)
            Reorder_Point = self.Mean_of_Demand_over_lead_time + Safety_Stock
            return Reorder_Point
        #################################'For Cost Ratio, If greater than 1 or less than zero, then use other method'
        


