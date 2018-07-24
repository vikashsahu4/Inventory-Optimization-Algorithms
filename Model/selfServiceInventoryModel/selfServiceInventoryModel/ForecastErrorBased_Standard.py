import math
import pandas as pd
import numpy as np
import scipy.stats as stats
from collections import OrderedDict
class ForeCastErrorBased(object):
    def __init__(self,falseLeadtime,serviceLevel,ww,forecast,demand,futureForecast):
        self.False_lead_time=int(falseLeadtime.item())
        self.service_level=float(serviceLevel.item()/100)
        self.ww=ww
        self.cs1=self.service_level
        self.leadtime = self.False_lead_time
        self.Zerodemand = 0
        self.forecast=forecast
        self.demand=demand
        #print(self.demand)
        self.futureForecast=futureForecast
        self.Nww=len(self.forecast)
        self.Period=[];self.WW=[];self.Forecast=[];self.Actualdemand=[];self.Forecasterror=[];
        self.Currleadtimedemand=[];self.Sumactuals=[];self.Sumforecasts=[];self.Cummerror=[];self.Countunder=[];self.Peakdemand=[];self.Maxcountunder=[];self.Maxcummerror=[]
        self.ForecastErrorStationary=[];self.Forecasterrorslope=[]; self.Forecasterrorintercept=[]; self.r_value=[]; self.p_value=[]; self.std_err=[]
        self.Forecastslope=[];self.Forecastintercept=[];self.ForecastEquation=[];self.ForecastStationary=[];
        self.Q1=0;self.Q3=0;self.Iqr=0;self.Lowerbound=0.0;self.Upperbound=0.0;self.Forecasterroradj=[];
        self.Ss=0;self.out=0;self.Outdoi=0;self.Outarray=[];self.Peak=[];self.Outunderforecast=[];self.Ssleadtime=0;self.Leadtimeforecast=0;self.Forecastperiod=0;
        self.avghistforecast=0;self.avgfutureforecast=0;self.forecastscale=0;
        self.Outweeks=0; self.Currentout=0; self.Overshot=0; self.Lastfraction=0; self.avgfutureforecasttwomonths=0;
    def calculatingDemandzerofraction(self):
        self.forecast =list(map(lambda x:x.item(),self.forecast))
        self.demand =list(map(lambda x:x.item(),self.demand))
        for i in list(range(1,self.Nww+1)):
            self.Period.append(i)
        for i in list(range(self.Nww)):
            # this should not be hardcoded in final program, user will provide work week dates
            self.Forecast.append(round(self.forecast[i]))
            self.Actualdemand.append(round(self.demand[i]));
            self.Forecasterror.append(round(self.Actualdemand[i]-self.Forecast[i]))
            if self.Actualdemand[i] ==0:
                self.Zerodemand = (self.Zerodemand + 1) #counter for zerodemand
        Demandzerofraction = (self.Zerodemand / self.Nww)
        return Demandzerofraction
    def maxCounConsecutiveUnderForecast_with_LT(self):
        self.Peakdemand = max(self.Actualdemand)
        self.Maxcummerror=0
        self.Maxcountunder = 0
        for i in list(range(self.Nww)):
            self.Currleadtimedemand = 0
            self.Sumactuals = 0
            self.Sumforecasts = 0
            self.Cummerror = 0
            self.Countunder = 0
            for j in list(range(int(self.leadtime))):
                if(i+j)<self.Nww:
                    if (i + j) <= self.Nww:
                        self.Currleadtimedemand = self.Actualdemand[i + j]
                    if (i + j) <= self.Nww:
                        self.Sumactuals = self.Sumactuals + self.Actualdemand[i + j]
                    if (i + j) <= self.Nww:
                        self.Sumforecasts = self.Sumforecasts + self.Forecast[i + j]
                    self.Cummerror = self.Sumactuals - self.Sumforecasts
                    if self.Cummerror > self.Maxcummerror:
                        self.Maxcummerror = self.Cummerror
                    if self.Cummerror > 0:
                        self.Countunder = self.Countunder + 1
                    if self.Cummerror < 0:
                        self.Countunder = 0
                    if self.Countunder > self.Maxcountunder:
                        self.Maxcountunder = self.Countunder
        self.Maxcummerror=int(self.Maxcummerror)
        return [self.Peakdemand,self.Maxcountunder]
    def calculatingForecastErrorEquationAndForecastErrorStationary(self):
        self.ForecastErrorStationary = True
        self.Forecasterrorslope, self.Forecasterrorintercept, self.r_value, self.p_value, self.std_err = stats.linregress(self.Period,self.Forecasterror)
        self.ForecastErrorEquation = str(self.Forecasterrorslope) + "*Period + " +str(self.Forecasterrorintercept)
        if abs(self.p_value) < 0.05:
            self.ForecastErrorStationary = False
        #print(self.ForecastErrorEquation)
        return [self.ForecastErrorEquation,self.ForecastErrorStationary]
    def calculatingForecastEquationAndForecastStationary(self):
        self.Forecastslope, self.Forecastintercept, self.r_value, self.p_value, self.std_err = stats.linregress(self.Period,self.Forecast)
        self.ForecastEquation = str(self.Forecastslope) + "*Period + " +str(self.Forecastintercept)
        self.ForecastStationary = True
        if abs(self.p_value) < 0.05:
            self.ForecastStationary = False 
        if self.ForecastStationary ==True:
            self.ForecastEquation = 'NA'
        return [self.ForecastEquation,self.ForecastStationary]
    def calculatingValueOfForecastAndAllOrderAndMaximumUnderforecast(self):
        self.Q1=int(np.percentile(self.Forecasterror, 25))
        self.Q3=int(np.percentile(self.Forecasterror, 75))
        self.Iqr=(self.Q3-self.Q1)
        if self.Iqr !=0:
            self.Lowerbound = max(self.Q1 - 1.5 * self.Iqr, min(self.Forecasterror))
        if self.Iqr !=0:
            self.Upperbound = min(self.Q3 + 1.5 * self.Iqr, max(self.Forecasterror))
            
        for i in list(range(self.Nww)):
            self.Forecasterroradj.append(self.Forecasterror[i])
            if self.Iqr !=0:
                if self.Forecasterror[i] > self.Upperbound:
                    self.Forecasterroradj.append(self.Upperbound)
                elif self.Forecasterror[i] < self.Lowerbound:
                    self.Forecasterroradj.append(self.Lowerbound)
                else:
                    self.Forecasterroradj.append(self.Forecasterror[i])
        self.Forecastperiod = self.Period[self.Nww-1] + self.leadtime
        self.Leadtimeforecast = round(np.mean(self.futureForecast))
        if self.Nww > 9:
            self.Ssleadtime = self.Maxcountunder
        
        if self.Ssleadtime == 0:
            self.Ssleadtime = 1
        self.Ss = round(np.percentile(self.Forecasterroradj, self.cs1*100) * (self.Ssleadtime ** 0.5))
        self.Out = self.Ss + self.Leadtimeforecast
        for i in list(range(self.Nww)):
            self.Outarray.append(self.Out)
            self.Peak.append(self.Peakdemand)
            self.Outunderforecast.append(self.Maxcummerror + int(self.Leadtimeforecast))
        return [self.Leadtimeforecast,self.Ss,self.Out,self.Outunderforecast[1],self.Maxcummerror]
    def calculatingDoi(self):
        #' Scaling factor (for DOI calc)
        self.avghistforecast = round(np.mean(self.Forecast))
        self.avgfutureforecast = int(np.mean(self.futureForecast))
        self.forecastscale = int(self.avgfutureforecast / self.avghistforecast)
        #' Perform DOI calculation
        Fww=1;
        if Fww <8:
            self.avgfutureforecasttwomonths = self.avgfutureforecast
        else:
            self.avgfutureforecasttwomonths=self.futureForecast
        if self.avgfutureforecasttwomonths <0:
            self.avgfutureforecasttwomonths = self.avgfutureforecast
        doiErrFlag = 0
        try:
            Outdoi = round(self.Out / self.avgfutureforecasttwomonths * self.forecastscale * 7, 0)
        except ZeroDivisionError:
            print("Warning: DOI calculation failed due to an error. Only recommended safety stock units will be reported")
            doiErrFlag = 1
        if Outdoi < 14:
            Outdoi = 14
        return Outdoi
        
def foreCastErrorBased_Standard_Function(falseLeadtime,serviceLevel,ww,forecast,demand,futureForecast):
    try:
        json_format ={}
        obj=ForeCastErrorBased(falseLeadtime,serviceLevel,ww,forecast,demand,futureForecast)
        #print('The value of Zero demand fraction===={}'.format(obj.calculatingDemandzerofraction()))
        json_format['Zero demand fraction']=obj.calculatingDemandzerofraction()
        Peakdemand,Maxcountunder= obj.maxCounConsecutiveUnderForecast_with_LT()
        #print('The value of Peakdemand is===={}'.format(Peakdemand))
        #print('Max count consecutive under forecast (with LT) =======  {}'.format(Maxcountunder))
        json_format['Peakdemand']=Peakdemand
        json_format['Max count consecutive under forecast (with LT)']=Maxcountunder
        ForecastErrorEquation,ForecastErrorStationary=obj.calculatingForecastErrorEquationAndForecastErrorStationary()
        #print('The value of Forecast Error Equation=======  {}'.format(ForecastErrorEquation))
        #print('The Forecast Error Stationary? ========  {}'.format(ForecastErrorStationary))
        json_format['Forecast Error Equation']=ForecastErrorEquation
        json_format['Forecast Error Stationary']=ForecastErrorStationary
        ForecastEquation,ForecastStationary=obj.calculatingForecastEquationAndForecastStationary()
        #print('The value of Forecast Equation=======  {}'.format(ForecastEquation))
        #print('The Forecast Stationary? ========  {}'.format(ForecastStationary))
        json_format['Forecast Equation']=ForecastEquation
        json_format['Forecast Stationary']=ForecastStationary
        Leadtimeforecast,Ss,Out,Outunderforecast,Maxcummerror=obj.calculatingValueOfForecastAndAllOrderAndMaximumUnderforecast()
        #print('The value of Forecast ======{}'.format(Leadtimeforecast))
        #print('The Recommended Safety Stock (units) ======={}'.format(Ss))
        #print('The Order Up To Qty (units) ========{}'.format(Out))
        #print('The value of Order Up To Qty, max underforecast (units) ====={}'.format(int(Outunderforecast)))
        #print('The value of Maximum underforecast over lead time is===={}'.format(Maxcummerror))
        json_format['Forecast']=Leadtimeforecast
        json_format['Recommended Safety Stock (units)']=Ss
        json_format['The Order Up To Qty (units)']=Out
        json_format['Order Up To Qty, max underforecast (units)']=int(Outunderforecast)
        json_format['Maximum underforecast over lead time is']=Maxcummerror
        Outdoi=obj.calculatingDoi()
        #print('Order Up To Qty (DOI) ====={}'.format(Outdoi))
        json_format['Order Up To Qty (DOI)']=Outdoi
        #print(Outdoi)
        result={}
        result['name'] = 'ForeCastErrorBased_Standard'
        result['value'] = [json_format]
        return [result]
    except Exception:
        result={}
        result['error']="Error in processing the model"
        raise Exception(result)
    
        
    
        
        