# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 15:27:58 2016

@author: vksahu
"""

'This program is designed to calculate the Safety Stock Multipler for Item Fill Rate function in r,s and s,q modules'
from imp import reload
from selfServiceInventoryModel.s_q_continuos_model import *
from selfServiceInventoryModel.r_s_periodic_model import *
#reload(selfServiceInventoryModel.s_q_continuos_model)
import selfServiceInventoryModel.s_q_continuos_model
#reload(selfServiceInventoryModel.r_s_periodic_model)
import selfServiceInventoryModel.r_s_periodic_model
from collections import OrderedDict

z = [-3.00,-2.96,-2.92,-2.88,-2.84,-2.80,-2.76,-2.72,-2.68,-2.64,-2.60,-2.56,-2.52,-2.48,-2.44,-2.40,-2.36,-2.32,-2.28,-2.24,-2.20,-2.16,-2.12,-2.08,-2.04,-2.00,-1.96,-1.92,-1.88,-1.84,-1.80,-1.76,-1.72,-1.68,-1.64,-1.60,-1.56,-1.52,-1.48,-1.44,-1.40,-1.36,-1.32,-1.28,-1.24,-1.20,-1.16,-1.12,-1.08,-1.04,-1.00,-0.96,-0.92,-0.88,-0.84,-0.80,-0.76,-0.72,-0.68,-0.64,-0.60,-0.56,-0.52,-0.48,-0.44,-0.40,-0.36,-0.32,-0.28,-0.24,-0.20,-0.16,-0.12,-0.08,-0.04,0.00,0.04,0.08,0.12,0.16,0.20,0.24,0.28,0.32,0.36,0.40,0.44,0.48,0.52,0.56,0.60,0.64,0.68,0.72,0.76,0.80,0.84,0.88,0.92,0.96,1.00,1.04,1.08,1.12,1.16,1.20,1.24,1.28,1.32,1.36,1.40,1.44,1.48,1.52,1.56,1.60,1.64,1.68,1.72,1.76,1.80,1.84,1.88,1.92,1.96,2.00,2.04,2.08,2.12,2.16,2.20,2.24,2.28,2.32,2.36,2.40,2.44,2.48,2.52,2.56,2.60,2.64,2.68,2.72,2.76
,2.80,2.84,2.88,2.92,2.96,3.00]
lz = [3.000,2.960,2.921,2.881,2.841,2.801,2.761,2.721,2.681,2.641,2.601,2.562,2.522,2.482,2.442,2.403,2.363,2.323,2.284,2.244,2.205,2.165,2.126,2.087,2.048,2.008,1.969,1.930,1.892,1.853,1.814,1.776,1.737,1.699,1.661,1.623,1.586,1.548,1.511,1.474,1.437,1.400,1.364,1.327,1.292,1.256,1.221,1.186,1.151,1.117,1.083,1.050,1.017,0.984,0.952,0.920,0.889,0.858,0.828,0.798,0.769,0.740,0.712,0.684,0.657,0.630,0.605,0.579,0.554,0.530,0.507,0.484,0.462,0.440,0.419,0.399,0.379,0.360,0.342,0.324,0.307,0.290,0.274,0.259,0.245,0.230,0.217,0.204,0.192,0.180,0.169,0.158,0.148,0.138,0.129,0.120,0.112,0.104,0.097,0.090,0.083,0.077,0.071,0.066,0.061,0.056,0.052,0.047,0.044,0.040,0.037,0.034,0.031,0.028,0.026,0.023,0.021,0.019,0.017,0.016,0.014,0.013,0.012,0.010,0.009,0.008,0.008,0.007,0.006,0.005,0.005,0.004,0.004,0.003,0.003,0.003
,0.002,0.002,0.002,0.002,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.000,0.000]
lnegz = [0.000,0.000,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.001,0.002,0.002,0.002,0.002,0.003,0.003,0.003,0.004,0.004,0.005,0.005,0.006,0.007,0.008,0.008,0.009,0.010,0.012,0.013,0.014,0.016,0.017,0.019,0.021,0.023,0.026,0.028,0.031,0.034,0.037,0.040,0.044,0.047,0.052,0.056,0.061,0.066,0.071,0.077,0.083,0.090,0.097,0.104,0.112,0.120,0.129,0.138,0.148,0.158,0.169,0.180,0.192,0.204,0.217,0.230,0.245,0.259,0.274,0.290,0.307,0.324,0.342,0.360,0.379,0.399,0.419,0.440,0.462,0.484,0.507,0.530,0.554,0.579,0.605,0.630,0.657,0.684,0.712,0.740,0.769,0.798,0.828,0.858,0.889,0.920,0.952,0.984,1.017,1.050,1.083,1.117,1.151,1.186,1.221,1.256,1.292,1.327,1.364,1.400,1.437,1.474,1.511,1.548,1.586,1.623,1.661,1.699,1.737,1.776,1.814,1.853,1.892,1.930,1.969,2.008,2.048,2.087,2.126,2.165,2.205,2.244,2.284,2.323,2.363,2.403,2.442,2.482,2.522,2.562,2.601,2.641,2.681,2.721,2.761,2.801
,2.841,2.881,2.921,2.960,3.000] 

def safetyStockMultiplierValue(lookup_val):
    #'For match-type 1'
    x=len(lookup_val)
    safety_stock_temp=[]
    #print(x)
    for j in range(x):
        temp = []
        a=z;b=lz;c=lnegz
        for i in c:
            if i<lookup_val[j]:
                temp.append(i)
                       
        r1=(a[temp.index(max(temp))])
        #print(r1)
        temp=[]
        'For match-type -1'
        for i in b:
            if i>=lookup_val[j]:
                temp.append(i)
                #print(temp)
        #print(temp)       
        r2=(a[b.index(min(temp))]) 
            
        #print(r2)
        #print(b.index(min(temp)))
            
        temp=[]
        for i in b:
            if i>=lookup_val[j]:
                temp.append(i)
                    
        r3=(b[b.index(min(temp))])
        #print(r3)
            
        temp=[]
        for i in c:
            if i<=lookup_val[j]:
                temp.append(i)
                    
        r4=(c[c.index(max(temp))])
        #print(r4)
            
        'To return the safety stock multiplier value'
        r5=-r1+(r2+r1)/(r3-r4)*(lookup_val[j]-r4)
        safety_stock_temp.append(r5)
    #print(safety_stock_temp)
    return safety_stock_temp
    #except Exception:
       # raise Exception("Error in Computing the Safety Stock")
    
def main(data,model=None):
        result={}
    #try:
        if model == 'SQContinousReview':    
            #try:
                Demand_Mean,Demand_Sigma,Fixed_Ordering_Cost,Cost_of_Acquisition,Holding_Charge,Lead_Time,Cycle_Service_Level,Cost_per_Stockout_Event,Item_Fill_Rate,Cost_Per_Item_Short=data
                objForSQ=SQ_Continuous_Review(Demand_Mean,Demand_Sigma,Fixed_Ordering_Cost,Cost_of_Acquisition,Holding_Charge,Lead_Time,Cycle_Service_Level,Cost_per_Stockout_Event,Item_Fill_Rate,Cost_Per_Item_Short)       
                json_format ={}

                data= objForSQ.commonCalculations()
                #print ('\nThe value of Unit Holding Cost is===={}'.format(data[0][0]))
                #json_format['Unit Holding Cost_for_s_Q']=data[0][0]
                #print ('\nThe value of Order_Quantity is===={}'.format(data[1][0]))
                json_format['Order Quantity']=data
                #print(data)
                #print ('\nThe value of Mean_of_Demand_over_lead_time===={}'.format(data[2][0]))
                #json_format['Mean_of_Demand_over_lead_time_for_s_Q']=data[2][0]
                #print ('\nThe value of Sigma_of_Demand_over_lead_timeis===={}'.format(data[3][0]))
                #json_format['Sigma_of_Demand_over_lead_time_for_s_Q']=data[3][0]
                
                reorderPoint_csl= objForSQ.toMeetcycleServiceLevel()
                #print ('\nTo Meet Cycle Service Level, the Reorder Point is ===={}'.format(reorderPoint[0]))
                #json_format['Cycle Service Level']=reorderPoint_csl
                #print(reorderPoint_csl)
                
                lookup_val =objForSQ.toMeetItemFillRate()
                #print(lookup_val)
                safety_stock_multiplier_val =safetyStockMultiplierValue(lookup_val)
                #print(safety_stock_multiplier_val)
                reorderPoint_ifr= objForSQ.toMeetItemFillRate(safety_stock_multiplier_val=safety_stock_multiplier_val,flag=True)
                #print ('\nTo Meet Item Fill Rate, the Reorder Point is ===={}'.format(reorderPoint[0]))
                #print(reorderPoint_ifr)
                #json_format['Meet Item Fill Rate']=reorderPoint[0]
                
                reorderPoint_msc= objForSQ.toMinimizeStockoutCost()
                #print(reorderPoint_msc)
                temp=reorderPoint_msc[2]
                flag=reorderPoint_msc[1]
                for i in range(temp):
                    if flag[i]==0:
                        res = 'N'
                        json_format['Minimize Stockout Cost']= res
                    else:
                        res=reorderPoint_msc[0]
                        #print ('\nTo Minimize Stockout Cost, the Reorder Point is ===={}'.format(reorderPoint[0]))
                        json_format['Minimize Stockout Cost']=res
                
                reorderPoint_cpis=objForSQ.toMinimizeCostPerItemShort()
                temp_cpim=reorderPoint_msc[2]
                flag_cpim=reorderPoint_msc[1]
                for i in range(temp_cpim):
                    if flag_cpim[i]==0:
                        res1 = 'N'
                        json_format['Minimize Cost Per Item Short']= res1
                    else:
                        res1=reorderPoint_cpis[0]
                        #print(reorderPoint_msc)
                        #print ('\nTo Minimize Stockout Cost, the Reorder Point is ===={}'.format(reorderPoint[0]))
                        json_format['Minimize Cost Per Item Short']=res1
                #print(temp,flag)
                #if reorderPoint_cpis is 0:
                #    res = 'S_Q model is not fit'
                #    json_format['Minimize Cost Per Item Short']= res
                #else:
                #    pass
                    #print ('\nTo To Minimize Cost Per Item Short, the Reorder Point is ===={}'.format(reorderPoint[0]))
                    #json_format['Minimize Cost Per Item Short']=reorderPoint[0]


                result={}
                result['name']='S_Q Continuos Model'
                result['value']=[{'Cycle Service Level':reorderPoint_csl[ind],'Meet Item Fill Rate':reorderPoint_ifr[ind],'Minimize Stockout Cost':res[ind],'Minimize Cost Per Item Short':res1[ind]} for ind in range(len(reorderPoint_csl))]
                print(result)
                return [result]
            #except Exception:
                #raise Exception("Error in processing S,Q Continuos model.Please check the values and try again")

        if model == 'RSPeriodicReview':
            try:    
                Demand_Mean,Demand_Sigma,Fixed_Ordering_Cost,Cost_of_Acquisition,Holding_Charge,Lead_Time,Review_Period,Cycle_Service_Level,Cost_per_Stockout_Event,Item_Fill_Rate,Cost_Per_Item_Short=data
                objForRS =RS_Periodic_Review(Demand_Mean,Demand_Sigma,Fixed_Ordering_Cost,Cost_of_Acquisition,Holding_Charge,Lead_Time,Review_Period,Cycle_Service_Level,Cost_per_Stockout_Event,Item_Fill_Rate,Cost_Per_Item_Short)
                #print ("\nCommon Calculations=========")
                json_format ={}
                data=objForRS.commonCalculations()
                #print('shape',data.shape)
                #print ('\nThe value of Unit Holding Cost is===={}'.format(data[0][0]))
                #json_format['Unit Holding Cost_for_R_S']=data[0][0]
                #print ('\nThe value of Order_Quantity is===={}'.format(data[1][0]))
                json_format['Order_Quantity_for_R_S']=data[1][0]
                #print ('\nThe value of Mean_of_Demand_over_lead_time is===={}'.format(data[2][0]))
                #json_format['Mean_of_Demand_over_lead_time_for_R_S']=data[2][0]
                #print ('\nThe value of Sigma_of_Demand_over_lead_time is===={}'.format(data[3][0]))
                #json_format['Sigma_of_Demand_over_lead_time_for_R_S']=data[3][0]
                #print ('\nThe value of Cost of Cycle Stock is===={}'.format(data[4][0]))
                #json_format[' Cost of Cycle Stock_for_R_S']=data[4][0]
                reorderPoint= objForRS.toMeetcycleServiceLevel()
                #print ('\nTo Meet Cycle Service Level, the Reorder Point is ===={}'.format(reorderPoint[0]))
                json_format['Meet Cycle Service Level']=reorderPoint[0]
                #print(type(reorderPoint), reorderPoint.shape)
                lookup_val =objForRS.toMeetItemFillRate()
                safety_stock_multiplier_val =safetyStockMultiplierValue(lookup_val)
                reorderPoint= objForRS.toMeetItemFillRate(safety_stock_multiplier_val=safety_stock_multiplier_val,flag=True)
                #print ('\nTo Meet Item Fill Rate, the Reorder Point is ===={}'.format(reorderPoint[0]))
                json_format['Meet Item Fill Rate']=reorderPoint[0]
                reorderPoint= objForRS.toMinimizeStockoutCost()
                if reorderPoint is False:
                    res ='Do not use R_S Model'
                    json_format['To Minimize Stockout Cost']= res 
                else:
                    #print ('\nTo Minimize Stockout Cost, the Reorder Point is ===={}'.format(reorderPoint[0]))
                    json_format['Minimize Stockout Cost']=reorderPoint[0]
                
                reorderPoint= objForRS.toMinimizeCostPerItemShort()
                if reorderPoint is False:
                    res ='Do not use R_S Model'
                    json_format['To minimize Stockout Cost']= res
                else:
                    #print ('\nTo To Minimize Cost Per Item Short, the Reorder Point is ===={}'.format(reorderPoint[0]))
                    json_format['Minimize Cost Per Item Short']=reorderPoint[0]

                result={}
                result['name']='R_S Periodic Review'
                result['value']=[json_format]
                return [result]
            except Exception:
                raise Exception("Error in processing R,S Periodic Review Model.Please check the values and try again")
    #except Exception:
        #json_format={}
        #json_format['error']="Error in processing the model. Please check the input values and try again"
        #raise Exception(json_format)
    
