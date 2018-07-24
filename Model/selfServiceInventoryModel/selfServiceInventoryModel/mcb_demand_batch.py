import random
import numpy as np
from scipy.stats import norm
from scipy import stats

class mcbDemand(object):
    def __init__(self,falseLeadtime,serviceLevel,demand):
        #self.leadtime=int(falseLeadtime.item());
        #self.serviceLevel=float(serviceLevel.item());
        self.leadtime=int(falseLeadtime)
        self.serviceLevel=float(serviceLevel/100)
        self.demand=demand;
        self.json_format={}
    def actionOnMcbDemand(self):
        #leadtime = 5 # take this value from user
        #csl = 0.95  # take this value from user
        #demand   = [5,6,2,10,2,1,7,8,7,3,1,6,4,2,10,7,5,5,4,8,1,10,3,6,4,1,4,7,6,8]
        leadtime=self.leadtime
        csl=self.serviceLevel
        demand=self.demand
        part = 5
        Nww = len(demand)
        # print(len(forecast))
        WW = [];Forecast = [];Actualdemand = [];Forecasterror = [];Demandzerofraction= [];Period = []
        tpm = [[0.0 for i in range(3)] for j in range(3)];Zerodemand = 0;state = [];zerostate = 0;posstate =0
        posvals = [];negstate = 0;negvals = []
        for i in list(range(1,Nww+1)):
            Period.append(i)
        posvals.append(0) # wasting the 0th positon of these arrays
        negvals.append(0) # wasting the 0th positon of these arrays
        #only two states since demand can be positive or negetive
        for i in range(Nww+1):
            WW.append(2016101);
            Actualdemand.append(round(demand[i-1]));
            if Actualdemand[i] ==0:
                Zerodemand = (Zerodemand + 1) #counter for zerodemand
                state.append("zero")
                zerostate = zerostate + 1
            elif Actualdemand[i] > 0 :
                state.append("pos")
                posstate = posstate + 1
                posvals.append(Actualdemand[i])
        # calculation of tpm matrix from the below code
        for k in range(2,Nww+1):
            if state[k-1] == "pos":
                i = 1
            elif state[k-1] == "zero":
                i = 2
            if state[k] == "pos":
                j = 1
            elif state[k] == "zero":
                j = 2
            tpm[i][j] = tpm[i][j] + 1
        #converting frequency to probability in tpm matrix
        nzero = tpm[2][1] + tpm[2][2]
        npos = tpm[1][1] + tpm[1][2]
        for i in range(1,3):
            rowsum = tpm[i][1] + tpm[i][2]
            if rowsum > 0 :
                for j in range(1,3):
                    tpm[i][j] = float(tpm[i][j])/rowsum
                    #print(tpm[i][j]," ",rowsum)
        trials = 10000
        start_index = 0
        # starting with the state that occured mostfrequently 
        if demand[Nww-1]>0:
            start_index = 1
        else:
            start_index = 2
        
        simstate =[["na" for i in range(leadtime+1)] for j in range(trials+1)]
        simerror =[[0.0 for i in range(leadtime+1)] for j in range(trials+1)]
        simcumerror = [[0.0 for i in range(leadtime+1)] for j in range(trials+1)]
        simmaxerror =[ 0 for i in range(trials+1)]
        simlterror =[ 0 for i in range(trials+1)]
        
        # doing simulation of markov chain and calculating simulation error at each step
        for i in range(trials+1):
            uni = random.random()
            if uni >= tpm[start_index][1]:
                simstate[i][1] = "zero"
                simerror[i][1] = 0
            elif uni < tpm[start_index][1]:
                simstate[i][1] = "pos"
                rnd = random.random()
                index = round(random.random() * posstate)
                # print("index ",index)
                simerror[i][1] = round(posvals[index] + norm.ppf(rnd) * abs(posvals[index] ** 0.5))
        
            simcumerror[i][1] = simerror[i][1]
            simmaxerror[i] = simcumerror[i][1]
            for j in range(2,leadtime+1):
                uni = random.random()
                k = 0 # this k will be set below
                if simstate[i][j-1] == "pos":
                    k = 1
                elif simstate[i][j-1] == "zero":
                    k = 2
        
                if uni >= tpm[k][1]:
                    simstate[i][j] = "zero"
                    simerror[i][j] = 0
                elif uni < tpm[k][1]:
                    simstate[i][j] = "pos"
                    index = round(random.random() * posstate)-1
                    simerror[i][j] = round(posvals[index] + norm.ppf(random.random()) * abs(posvals[index] ** 0.5))
                
                simcumerror[i][j] = simcumerror[i][j-1] + simerror[i][j]
                if simcumerror[i][j] > simmaxerror[i] :
                    simmaxerror[i] = simcumerror[i][j]
            simlterror[i] = simerror[i][leadtime]
        
        #finally when we have simulated error values we calculate csl percintile till that level to get safety stock
        forecast =    np.percentile(simlterror, 50)
        forecastub =  np.percentile(simlterror, round(csl*100))
        safetystock = np.percentile(simmaxerror, round(csl*100))
        #p-value code
        #print(tpm_count)
        
        #print(nzero)
        ts = npos*(2* pow(tpm[1][1]-1,2) + 2 * pow(tpm[1][2],2)) + nzero*(2* pow(tpm[2][1],2) + 2 * pow(tpm[2][2],2))
        #p-val =  
        p_val= 1- stats.chi2.cdf(ts,2)
        #print(p_val)
        #p_value=round(p_val)
        # print(simmaxerror)
        # print(simmaxerror)
        #print("point forecast ", forecast)
        self.json_format['point forecastlb']=forecast
        #print("point forecastub ", forecastub)
        self.json_format['point forecastub']=forecastub
        #print("order upto qty (safetystock) ", safetystock)
        self.json_format['order upto qty (safetystock)']=safetystock
        self.json_format['P-Value']=p_val
        result= {}
        #result['name']='Mcb Demand'
        #result['value'] = [self.json_format]
        #return [result]
        return self.json_format
        
