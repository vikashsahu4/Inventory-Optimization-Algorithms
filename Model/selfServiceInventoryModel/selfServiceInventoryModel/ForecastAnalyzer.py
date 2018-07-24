import math
import numpy as np
from collections import OrderedDict
class Forecast_Analyzer(object):
    try:
        def __init__(self,forecastData=None,demadData=None):
            self.forecastData=forecastData
            self.demadData=demadData
        def outputToGetUII(self):
            json_format ={}
            json_format['name']="Forecast Analyzer"
            if ((not self.forecastData.any()) or (not self.demadData.any())):
                raise Exception("...............User have to give the input data for ForecastData or DemandData or both................")
            forecastchange,actualchange,actualchangesq,diff,nom,denom =np.array([]),np.array([]),np.array([]),np.array([]),0,0
            for i in range(len(self.forecastData)-1):
                forecastchange = np.append(forecastchange,np.array([self.forecastData[i+1]-self.forecastData[i]]))
                actualchange = np.append(actualchange,np.array([self.demadData[i+1]-self.demadData[i]]))
                actualchangesq = np.append(actualchangesq,np.array([math.pow(actualchange[i],2)]))
                diff = np.append(diff,np.array([math.pow((forecastchange[i]-actualchange[i]),2)]))
                nom=nom+diff[i]
                denom=denom+actualchangesq[i]
            try:
                #denom='abc'
                uii=(math.sqrt(nom)/math.sqrt(denom))
            except Exception:
                raise Exception("Divide by Zero Exception error or String mismatch compatibility")

            json_format ={}
            json_format['name']="Forecast Analyzer"
            value = {}
            #value['UII']= round(uii,3)
            if(uii >1):
                ans = 'Not Forecastable'
            else:
                ans = 'Forecastable'
            #value['Result'] = ans
            data = {'UII':round(uii,3),'Result':ans}
            json_format['value'] = [data]
            return [json_format]
    except Exception:
       print("Contact Dev Team. There is something wrong in the processing of model")

            
    
    
    