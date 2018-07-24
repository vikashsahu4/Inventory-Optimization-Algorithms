import math,random
import pandas as pd
import numpy as np
import scipy.stats as stats
from scipy.stats import norm
from collections import OrderedDict
class ForeCastLumpyDemand(object):
    def __init__(self,falseLeadtime,serviceLevel,forecast,demand,futureForecast):
        self.leadtime=int(falseLeadtime.item());
        self.serviceLevel=float(serviceLevel.item()/100);
        self.forecast=forecast;
        self.demand=demand;
        self.futureForecast=futureForecast;
        self.json_format={}
    def actionOnForcastLumpy(self):
        try:
            self.forecast =list(map(lambda x:x.item(),self.forecast))
            self.demand =list(map(lambda x:x.item(),self.demand))
            forecast =self.forecast
            demand = self.demand
            futureforecast =self.futureForecast
            leadtime=self.leadtime
            serviceLevel=self.serviceLevel
            Period=[];WW = [];Forecast = [];Actualdemand = [];Forecasterror = [];Demandzerofraction= [];
            tpm = [[0.0 for i in range(4)] for j in range(4)];
            Zerodemand = 0;state = [];zerostate = 0;posstate =0;posvals = [];negstate = 0;negvals = []
            Nww = len(forecast)
            # print(len(forecast))
            
            for i in list(range(1,Nww+1)):
                Period.append(i)
            posvals.append(0) # wasting the 0th positon of these arrays
            negvals.append(0) # wasting the 0th positon of these arrays
            for i in list(range(Nww)):
                WW.append(2016101);
                Forecast.append(round(forecast[i]))
                Actualdemand.append(round(demand[i]));
                Forecasterror.append(round(Actualdemand[i]-Forecast[i]))
                if Actualdemand[i] ==0:
                    Zerodemand = (Zerodemand + 1) #counter for zerodemand
                if Forecasterror[i] < 0 :
                    state.append("neg")
                    negstate = negstate + 1
                    negvals.append(Forecasterror[i])
                elif Forecasterror[i] == 0 :
                    state.append("zero")
                    zerostate = zerostate + 1
                else:
                    state.append("pos")
                    posstate = posstate + 1
                    posvals.append(Forecasterror[i])
                Demandzerofraction = (Zerodemand / Nww)
            for k in list(range(2,Nww)):
                if state[k-1] == "neg":
                    i = 1
                elif state[k-1] == "pos":
                    i = 2
                elif state[k-1] == "zero":
                    i = 3
                if state[k] == "neg":
                    # print("he",k)
                    j = 1
                elif state[k] == "pos":
                    j = 2
                elif state[k] == "zero":
                    j = 3
            
                tpm[i][j] = tpm[i][j] + 1
            for i in range(1,4):
                rowsum = tpm[i][1] + tpm[i][2] + tpm[i][3]
                if rowsum > 0 :
                    for j in range(1,4):
                        # print(tpm[i][j]," ",rowsum)
                        tpm[i][j] = float(tpm[i][j])/rowsum
                        # print(tpm[i][j]," ",rowsum)
            trials = 10000
            max_length = max(negstate,posstate,zerostate)
            start_index = 0
            if max_length == negstate:
                start_index = 1
            elif max_length == posstate:
                start_index = 2
            else:
                start_index = 3
            simstate =    [["na" for i in range(leadtime+1)] for j in range(trials+1)]
            simerror =    [[0.0 for i in range(leadtime+1)] for j in range(trials+1)]
            simcumerror = [[0.0 for i in range(leadtime+1)] for j in range(trials+1)]
            simmaxerror = [ 0 for i in range(trials+1)]
            for i in range(trials):
                uni = random.random()
                if uni >= tpm[start_index][1] + tpm[start_index][2] :
                    simstate[i][1] = "zero"
                    simerror[i][1] = 0
                elif uni >= tpm[start_index][1]:
                    simstate[i][1] = "pos"
                    rnd = random.random()
                    index = round(random.random() * posstate)
                    # print("index ",index)
                    simerror[i][1] = round(posvals[index] + norm.ppf(rnd) * abs(posvals[index] ** 0.5))
                else:
                    simstate[i][1] = "neg"
                    index = round(random.random() * negstate)
                    rnd = random.random()
                    simerror[i][1] = round(negvals[index] + norm.ppf(rnd) * abs(negvals[index] ** 0.5))
            
                simcumerror[i][1] = simerror[i][1]
                simmaxerror[i] = simcumerror[i][1]
                for j in range(2,leadtime):
                    uni = random.random()
                    k = 0 # this k will be set below
                    if simstate[i][j-1] == "neg":
                        k = 1
                    elif simstate[i][j-1] == "pos":
                        k = 2
                    elif simstate[i][j-1] == "zero":
                        k = 3
            
                    if uni >= tpm[k][1] + tpm[k][2] :
                        simstate[i][j] = "zero"
                        simerror[i][j] = 0
                    elif uni >= tpm[k][1]:
                        simstate[i][j] = "pos"
                        index = round(random.random() * posstate)-1
                        simerror[i][j] = round(posvals[index] + norm.ppf(random.random()) * abs(posvals[index] ** 0.5))
                    elif uni < tpm[k][1]:
                        simstate[i][j] = "neg"
                        index = round(random.random() * negstate)
                        simerror[i][j] = round(negvals[index] + norm.ppf(random.random()) * abs(negvals[index] ** 0.5))
            
                    simcumerror[i][j] = simcumerror[i][j-1] + simerror[i][j]
                    if simcumerror[i][j] > simmaxerror[i] :
                        simmaxerror[i] = simcumerror[i][j]
            csl=serviceLevel;
            safetystock = np.percentile(simmaxerror, round(csl*100))
            print("Safetystock=================== ", safetystock)
            self.json_format['safetystock']=safetystock
            avghistforecast = np.mean(forecast)
            avgfutureforecast = np.mean(futureforecast)
            forecastscale = avgfutureforecast / avghistforecast
            fww = len(futureforecast)
            if(fww < 8) :
                avgfutureforecasttwomonths = avgfutureforecast
            else :
                avgfutureforecasttwomonths = (futureforecast[1] + futureforecast[2] + futureforecast[3] + futureforecast[4] + futureforecast[5] + futureforecast[6] + futureforecast[7] + futureforecast[8]) / 8
            
            if avgfutureforecasttwomonths == 0 :
                avgfutureforecasttwomonths = avgfutureforecast
            leadtimeforecast = np.mean(futureforecast)
            out = safetystock + leadtimeforecast;
            outdoi = round(out / avgfutureforecasttwomonths * forecastscale * 7 , 0 )
            if outdoi < 14:
                outdoi = 14
            ordqtystckunits = safetystock + round(avgfutureforecast)
            self.json_format['Order Upto Qty, Markov Chain Bootstrap (units)']=ordqtystckunits
            self.json_format['Order Upto Qty, Markov Chain Bootstrap (DOI)']=outdoi
            result={}
            result['name']= 'ForecastLumpyDemand'
            result['value']= [self.json_format]
            return [result]
        except Exception:
            raise Exception("Error in processing the model")
'''              
if __name__ == '__main__':
    leadtime = 5 # take this value from user
    serviceLevel = 0.95  # take this value from user
    forecast = [0,0,31.5,0,0,0,0,45.5,0,0,0,0,28,0,31.5,0,0,0,17.5,0,0,0,21,0,0]
    demand   = [0,0,35.736,0,0,0,0,29.092,0,0,0,0,0,0,45.129,0,0,0,13.124,0,0,0,19.16,0,0]
    futureforecast = [17.5,0,0,0,21,0,0]
    o=ForeCastLumpyDemand()
    x=o.actionOnForcastLumpy(falseLeadtime=leadtime,serviceLevel=serviceLevel,forecast=forecast,demand=demand,futureForecast=futureforecast)
    print(x)
'''