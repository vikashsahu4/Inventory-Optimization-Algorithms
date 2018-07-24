# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 14:27:55 2016

@author: vksahu
"""

'Represents class s,q continuos review. In this module we return Reorder point from each function to the main test file'
'For Safety Stock multiplier I have to import results from safety stock multiplier.py for "To meet Item Fill Rate Function"'
import math
from math import log
import scipy.special
import numpy as np
class SQ_Continuous_Review(object):
    def __init__(self,Demand_Mean,Demand_Sigma,Fixed_Ordering_Cost,Cost_of_Acquisition,Holding_Charge,Lead_Time,Cycle_Service_Level,Cost_per_Stockout_Event,Item_Fill_Rate,Cost_Per_Item_Short):   
        self.demandMean=Demand_Mean
        self.demandSigma=Demand_Sigma
        self.fixedOrderedCost=Fixed_Ordering_Cost
        self.costOfAcquisition=Cost_of_Acquisition
        self.holdingCharge=Holding_Charge
        self.leadTime=Lead_Time
        self.cycleServiceLevel=Cycle_Service_Level
        self.costPerStockoutEvent=Cost_per_Stockout_Event
        self.itemFillRate=Item_Fill_Rate
        self.costPeritemShort=Cost_Per_Item_Short
        self.Safety_Stock_Multiplier=0
            
    def commonCalculations(self):
        ##########################'Common Calculations'###################################
        self.Unit_Holding_Cost= ((self.holdingCharge/100)*self.costOfAcquisition)
        self.Order_Quantity=np.sqrt((2 * self.fixedOrderedCost * self.demandMean)/self.Unit_Holding_Cost)
        #self.Order_Quantity = [math.sqrt((2 * self.fixedOrderedCost * self.demandMean)/self.Unit_Holding_Cost)]
        self.Mean_of_Demand_over_lead_time=(self.demandMean*self.leadTime)
        self.Sigma_of_Demand_over_lead_time=(self.demandSigma * np.sqrt(self.leadTime))
        #print(self.Sigma_of_Demand_over_lead_time)
        return [self.Unit_Holding_Cost,self.Order_Quantity,self.Mean_of_Demand_over_lead_time,self.Sigma_of_Demand_over_lead_time]
        
    def toMeetcycleServiceLevel(self):
        ##############################'To Meet Cycle Service Level:'##############################
        per=self.cycleServiceLevel
        per=(per/100)
        self.Safety_Stock_Multiplier= (scipy.special.ndtri(per))
        Safety_Stock= (self.Safety_Stock_Multiplier*self.Sigma_of_Demand_over_lead_time)
        Reorder_Point= (self.Mean_of_Demand_over_lead_time+Safety_Stock)
        return Reorder_Point
        
    def toMeetItemFillRate(self,safety_stock_multiplier_val=0,flag=False):
        #################################'To Meet Item Fill Rate'#####################################
        Unit_Normal_Loss_Value = self.Order_Quantity/self.Sigma_of_Demand_over_lead_time*(1-(self.itemFillRate/100))
        #print(self.Sigma_of_Demand_over_lead_time)
        #print(Unit_Normal_Loss_Value)
        if not flag:
            return Unit_Normal_Loss_Value
        else:
            self.Safety_Stock_Multiplier=safety_stock_multiplier_val
            #print(safety_stock_multiplier_val)
            Safety_Stock=(self.Sigma_of_Demand_over_lead_time*self.Safety_Stock_Multiplier)
            Reorder_Point=(self.Mean_of_Demand_over_lead_time+Safety_Stock)
            return Reorder_Point
        
    def toMinimizeStockoutCost(self):
        ################################'To Minimize Stockout Cost'##################################
        x = math.sqrt(2*(math.pi))
        #############'<-- If less than or equal 1, then use other method'
        Limit=self.costPerStockoutEvent*self.demandMean/(self.Unit_Holding_Cost*self.Order_Quantity*self.Sigma_of_Demand_over_lead_time*x)    
        temp=len(Limit)
        flag=[1]*temp
        #print(Limit)
        for i in range(temp):
            if Limit[i]<=1:
                flag[i]=0
                Safety_Stock=0
                self.Mean_of_Demand_over_lead_time=0
            else:
                Safety_Stock_Multiplier = np.sqrt([2*log(y,10) for y in Limit])
                #print(Safety_Stock_Multiplier)
                Safety_Stock =  self.Sigma_of_Demand_over_lead_time*Safety_Stock_Multiplier
        Reorder_Point = self.Mean_of_Demand_over_lead_time + Safety_Stock
        return Reorder_Point,flag,temp
        
    def toMinimizeCostPerItemShort(self):
        ############################'To Minimize Cost Per Item Short'################################
        Cost_Ratio = (self.Unit_Holding_Cost*self.Order_Quantity)/(self.costPeritemShort*self.demandMean) 
        #print(Cost_Ratio)
        Safety_Stock_Multiplier1=0
        Safety_Stock1=0
        temp=len(Cost_Ratio)
        flag=[1]*temp
        #print(self.Sigma_of_Demand_over_lead_time)
        for i in range(temp):
            if ((Cost_Ratio[i] > 1) or (Cost_Ratio[i] < 0)):
                flag[i]=0
                return flag,temp
            else:
                Safety_Stock_Multiplier1 = scipy.special.ndtri(1-Cost_Ratio)
                Safety_Stock1 =(Safety_Stock_Multiplier1*self.Sigma_of_Demand_over_lead_time)
        Reorder_Point = self.Mean_of_Demand_over_lead_time + Safety_Stock1
        #print(Reorder_Point)
        #print(flag)
        return Reorder_Point,flag,temp
        #################################'For Cost Ratio, If greater than 1 or less than zero, then use other method'
        














