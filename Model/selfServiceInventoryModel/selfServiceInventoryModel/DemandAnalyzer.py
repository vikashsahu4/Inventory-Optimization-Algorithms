from scipy import stats
from scipy.stats import poisson
from scipy.stats import chisquare
import numpy
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson
import pandas as pd
import csv,sys,os,re,random
from collections import deque
from numpy.linalg import inv
import datetime
import math
class demandAnalyzer(object):
    def __init__(self,datainsert):
        '''Constructor to initialize the bound object.'''
        #self.path = path
        self.datainsert=datainsert
        self.period=len(self.datainsert)
        self.data=[]
        self.lags=(int(self.period/4))
        #self.data =self.readFromCSVFile(path)
        self.bp=None
        self.r=list(range(0,self.lags))
        self.pacf =np.array([i for i in list(range(self.lags))])
        self.x =numpy.array([i for i in range(1,len(datainsert)+1)])
        self.y = numpy.array(self.datainsert)
        self.lastRow=10
        self.slope, self.intercept, self.r_value, self.p_value, self.std_err = stats.linregress(self.x,self.y)
        self.X,self.Y,self.coeff,self.fit,self.res,self.tsMean,self.SSres,self.Msres=None,None,None,None,None,0,0,0
        self.countError=True
    
    def sac(self,x, k=1):
        """
        Sample autocorrelation (As used in statistics with normalization)
        http://en.wikipedia.org/wiki/Autocorrelation
        Parameters
        ----------
        x : 1d numpy array
            Signal
        k : int or list of ints
            Lags to calculate sample autocorrelation for
        Returns
        -------
        res : scalar or np array
            The sample autocorrelation. A scalar value if k is a scalar, and a
            numpy array if k is a interable.
        """
        try:
            res = []
            for ki in k:
                res.append(self.sac(x, ki))
            return np.array(res)
        except:
            pass
        mx = np.mean(x)
        if k==0:
            n = np.sum((x-mx)*(x-mx))
        else:
            n = np.sum((x[:-k]-mx)*(x[k:]-mx))
        d = len(x) * np.var(x)
        return n/d
        
    def boxpierce(self,x, lags, alpha=0.1):
        """
        The Box-Pierce test for determining if the data is independently distributed.
        Parameters
        ----------
        x : 1d numpy array
            Signal to test
        lags : int
            Number of lags being tested
           
        Returns
        -------
        Q : float
            Test statistic
        """
        n = len(x)
        Q = 0
        for k in range(1, lags+1):
            Q += (self.sac(x, k)**2)
        Q = n*Q
        return Q
        
    def boxpiercetestStatistic(self):
        self.lastRow = (self.lastRow + 1)
        self.bp=self.boxpierce(self.y, self.lags, alpha=0.1)
        return self.bp
        
    def boxpierce_p_value(self):
        self.lastRow = (self.lastRow + 1)
        boxpiercePValue=(1-stats.chi2.cdf(self.bp ,self.lags))
        return boxpiercePValue
        
    def trendlineIntercept(self):
        return self.intercept
        
    def trendlineSlope(self):
        return self.slope
        
    def coeffreturn(self):
        try:
            self.X=np.array([list(range(self.period)),list(range(self.period))])
            self.Y=np.array([list(range(self.period))])
            popList=range(1,31)
            queue = deque(range(0,len(self.datainsert)))
            for i in list(range(np.shape(self.X)[0])):
                for j in list(range(np.shape(self.X)[1])):
                    self.X[i][j]=1
                    if i==1:
                       self.X[i][j]=queue.popleft()
            for i in list(range(self.period)):
                self.Y[0][i]=self.datainsert[i]
            self.X=self.X.transpose()
            self.coeff=(np.dot(self.X.transpose(),self.X))
            self.coeff=inv(self.coeff)
            self.coeff=(np.dot(self.coeff,self.X.transpose()))
            self.coeff=(np.dot(self.coeff,self.Y.transpose())).transpose()
        except Exception as e:
            print(e)
        
    def slope_pValue(self):
        return self.p_value
       
    def zeroDemandfraction(self):
        zero_frac = 0
        for i in list(range(1,len(self.y))):
            if self.y[i]==0:
                zero_frac = zero_frac + 1
        zero_frac = int(zero_frac / len(self.y))
        return zero_frac
        
    def discreteIndicatorFlag(self):
        self.discreteIndicatorFlag=True
        for i in range(0,len(self.y)):
            if((round(self.y[i],0)) != (self.y[i])):
                self.discreteIndicatorFlag=False
        return self.discreteIndicatorFlag
        
    def piosondistributionMLE(self):
        tsMean = (sum(self.y)/len(self.y))
        mle = tsMean
        return mle
              
    def chi_square_statistic_for_poison_distribution(self):
        demand=[]
        demand=self.datainsert
        periods = len(demand)
        #frequency count of unique values
        fcount = {}
        for ind in range(len(demand)):
            if demand[ind] in fcount:
                fcount[demand[ind]]  =  fcount[demand[ind]] + 1
            else:
                fcount[demand[ind]] = 1

        #unique keys of fcount
        uniq = list(fcount.keys())
        mle = sum(demand)/periods

        #getting expected poisson pmf for each unique values
        theoreticalprob = [poisson.pmf(uniq[i], mle) for i in range(len(uniq))]
        exp = [float(theoreticalprob[i]*float(periods)) for i in range(len(uniq))]

        #taking only positive values
        exp = [exp[i] for i in range(len(exp)) if exp[i]>0]

        val = list(fcount.values())
        # only taking those values who expected values are not zero
        val = val[0:len(exp)]

        val.append(0)
        exp.append((1-sum(theoreticalprob))*periods)
        #print(val[0:len(exp)],'\n',exp)
        #print('python chisquare ', chisquare(val[0:len(exp)], exp))
        p_stats,p_value=chisquare(val[0:len(exp)], exp)
        dof=len(uniq)-1
        #print(p_stats,p_value,dof)
        #print('dof ', len(uniq)-1)
        return[p_stats,p_value,dof]
        
    def durbinWWatsonTestStatisticfor_TrendLine_Residuals(self):
        self.X=np.array([list(range(self.period)),list(range(self.period))])
        self.Y=np.array([list(range(self.period))])
        popList=range(1,31)
        queue = deque(range(0,len(self.datainsert)))
        for i in list(range(np.shape(self.X)[0])):
            for j in list(range(np.shape(self.X)[1])):
                self.X[i][j]=1
                if i==1:
                   self.X[i][j]=queue.popleft()
        for i in list(range(self.period)):
            self.Y[0][i]=self.datainsert[i]
        self.X=(self.X.transpose())
        self.coeff=(np.dot((self.X).transpose(),self.X))
        self.coeff=inv(self.coeff)
        self.coeff=(np.dot(self.coeff,self.X.transpose()))
        self.coeff=(np.dot(self.coeff,self.Y.transpose())).transpose()
        self.fit=(np.dot(self.X,self.coeff.transpose())).transpose()
        subarray=numpy.subtract(self.Y,self.fit)
        self.res=subarray
        demo=(np.sum(self.res**2))
        num=0
        for i in list(range(1,self.period)):
           num=(num+((self.res[0][i]- self.res[0][i-1]))**2)
        global dwt
        try:
            if demo != 0:
                dwt=(float(num)/float(demo))
            else:
                self.countError = False
                dwt="No Output due to invalid data passing through durbinWWatsonTest for TrendLine_Residuals so no need to test the all output"
                return [dwt,self.countError]
        except ZeroDivisionError:
            pass

        return dwt   
        
    def durbinWWatsonTestStatisticfor_Lag_1_AutoCorrelation(self):
        self.tsMean =int((sum(self.datainsert)/len(self.datainsert)))
        self.res=np.array([list(range(self.period))])
        for i in list(range(self.period)):
            self.res[0][i] = (self.Y[0][i] - self.tsMean)
        demo=(np.sum(self.res**2))
        num=0
        for i in list(range(1,self.period)):
           num=(num+((self.res[0][i]- self.res[0][i-1]))**2)
        global dwt
        try:
            if demo != 0:
                dwt=(float(num)/float(demo))
            else:
                dwt="No Output due to invalid data passing through durbinWWatsonTest for Lag_1_AutoCorrelation"
        except ZeroDivisionError:
            pass
        return dwt
        
    def slopeTStatistic(self):
        xbar = 0
        ybar = 0
        self.lastRow = (self.lastRow + 4)
        for i in list(range(self.period)):
            xbar = xbar + i
            ybar = (ybar + self.datainsert[i])
        xbar = (xbar / self.period)
        ybar = (ybar / self.period)
        Sxx = 0
        Sxy = 0
        SST = 0
        for i in list(range(self.period)):
            Sxx = (Sxx + ((i - xbar) ** 2))
            Sxy = (Sxy + (self.datainsert[i] * (i - xbar)))
            SST = (SST + ((self.datainsert[i] - ybar) ** 2))
        self.coeffreturn()
        self.SSres = (SST - (self.coeff[0][1] * Sxy))
        self.Msres = (self.SSres / (self.period - 2))
        t0 = (self.coeff[0][1] / ((self.Msres / Sxx) ** (1 / 2)))
        return t0
        
    def autocorrelationFunctionOrder(self):
        acf_signif = 0
        pacf_signif = 0
        acf_order = 0
        pacf_order = 0
        acf_stop = 0
        pacf_stop = 0
        Lags=(self.lags)
        for i in range(0,Lags):
            if (abs(self.r[i]) >= (2/(self.period **(1/2)))):
                pacf_signif = pacf_signif + 1
            if ((abs(self.pacf[i])) >= (2/((self.period)**(1/2)))):
                pacf_signif = pacf_signif + 1
            if (abs(self.r[i]) >= (2/(self.period **(1/2)))) and acf_stop==0:
                acf_order = acf_order + 1
            else:
                acf_stop = 1
            if (abs(self.pacf[i]) >= (2/((self.period)**(1/2))) and (pacf_stop==0)):
                pacf_order = pacf_order + 1
            else:
                pacf_stop = 1
        return acf_order
        
    def autocorrelation_Detected_In_Trend_Line_Residuals(self):
        self.lastRow = (self.lastRow + 1)
        if self.period <20:
            dL = 1.08
            dU = 1.36
        elif self.period <25:
            dL = 1.2
            dU = 1.41
        elif self.period <30:
            dL = 1.2
            dU = 1.45
        elif self.period <40:
            dL = 1.35
            dU = 1.49
        elif self.period <50:
            dL = 1.44
            dU = 1.54
        elif self.period <60:
            dL = 1.5
            dU = 1.59
        elif self.period <80:
            dL = 1.55
            dU = 1.62
        elif self.period <100:
            dL = 1.61
            dU = 1.66
        elif self.period >=100:
            dL = 1.65
            dU = 1.69
        if dwt < dL:
             slope_fit_dwt_result = "Yes"
        else:
            slope_fit_dwt_result = "No"
        self.lastRow = (self.lastRow + 1)
        return slope_fit_dwt_result
        
    def lag_1_auto_correlation_detected(self):
        if self.period <20:
            dL = 1.08
            dU = 1.36
        elif self.period <25:
            dL = 1.2
            dU = 1.41
        elif self.period <30:
            dL = 1.2
            dU = 1.45
        elif self.period <40:
            dL = 1.35
            dU = 1.49
        elif self.period <50:
            dL = 1.44
            dU = 1.54
        elif self.period <60:
            dL = 1.5
            dU = 1.59
        elif self.period < 80:
            dL = 1.55
            dU = 1.62
        elif self.period <100:
            dL = 1.61
            dU = 1.66
        elif self.period >=100:
            dL = 1.65
            dU = 1.69
        if self.durbinWWatsonTestStatisticfor_Lag_1_AutoCorrelation() <dL:
            dwt_lag1_result = "Yes"
        else:
            dwt_lag1_result = "No"
        return dwt_lag1_result

    def diffusion_model(self):
        demand=[]
        demand=self.datainsert
        demand = [float(demand[i]) for i in range(len(demand))]
        x1 =0
        X = list()
        for ind in range(1,len(demand)):
            x1 += demand[ind-1]                     # summation of previous demand
            x2 = x1 * x1     # summation of square of all previous demands
            X.append([x1, x2, 1])                   # adding 1 for the intercept
                                            # Equation for OLS
                                            # demand(t) = coeff1 * summation(demand[0:t-1]) + coeff2 * summation(demand[0:t-1] ^ 2) + coeff3
        X = np.array(X)
        y = np.array(demand[1:len(demand)])         # ignoring the first value of demand 

        res = sm.OLS(y, X).fit()
        #print(res.summary())
        #USe dir(res) for list of all attributes of res
        #print('adjusted ', res.rsquared_adj)
        #print('pvalues ', res.pvalues)
        adj_rsq=res.rsquared_adj
        p_val,yp_val,zp_val=res.pvalues
        return [adj_rsq,p_val,yp_val,zp_val]


    def seasonality_model(self):
        demand=[]
        demand=self.datainsert
        period = [i for i in range(1, len(demand)+1)]
        r2 = list()
        pval = list()
        res = None
        for d in range(1, int(len(demand)/2)):
            X = list()
            for ind in range(len(demand)):
                x1 = period[ind]                        # t
                x2 = math.sin((2*math.pi*x1)/d)         #Sin(2*pi*t/d)
                x3 = math.cos((2*math.pi*x1)/d)         #Cos(2*pi*t/d)
                X.append([x1, x2, x3, 1])    # adding 1 for the intercept
            # equation for OLS
            # demand =  coeff1 * t + coeff2 * Sin(2*pi*t/d) + coeff3 * Cos(2*pi*t/d) + coeff4
            X = np.array(X)
            res = sm.OLS(demand, X).fit()
            r2.append(res.rsquared_adj)
            pval.append(res.pvalues)
        #picking up maximum r sqaure adjusted values
        seasonality = r2.index(max(r2))
        period=seasonality+1
        r_sq=max(r2)
        #print('seasonality period',seasonality+1)
        #print('adjusted r square ', max(r2))
        # getting pvalues of coefficients
        #print('t_Pval \t sin_Pval \t cos_Pval \t const_Pval')
        t_Pval,sin_Pval,cos_Pval,const_Pval=pval[seasonality]
        #print(pval[seasonality])
        return [period,r_sq,t_Pval,sin_Pval,cos_Pval]

    def displayResult(inputData):
        if(not inputData.any()):
            raise Exception("Please Check the input excel values and try again")
        try:
            arr=np.array([])
            arr=np.append(arr,np.array(inputData))
            json_format ={}
            obj = demandAnalyzer(arr)  #User can give the file path name here
            if obj.countError:
                result=obj.boxpiercetestStatistic()
                #print('Box-Pierce test statistic===={}'.format(result)) #Calculating Box-Pierce test statistic
                json_format['Box-Pierce test statistic']=result
            if obj.countError:
                result =obj.boxpierce_p_value()
                #print('Box-Pierce test p-value===={}'.format(result)) #Calculating Box-Pierce test p-value
                boxpval=result
                json_format['Box-Pierce test p-value']=result
            if obj.countError:
                result=obj.trendlineIntercept()
                #print('The Trend line intercept:===={}'.format(result)) #Calculating Trend line intercept
                json_format['Trend line intercept']=result
            if obj.countError:
                result=obj.trendlineSlope()
                #print('The Trend line slope:===={}'.format(result)) #Calculating Trend line slope
                json_format['Trend line slope']=result
            if obj.countError:
                result=obj.slopeTStatistic()
                #print('The Slope t-value===={}'.format(result)) #Calculating Slope t-statistic
                json_format['Slope t-value']=result
            if obj.countError:
                result=obj.slope_pValue()
                slope_pval=result
                #print('The Slope p-value===={}'.format(result)) #Calculating Slope p-value
                json_format['Slope p-value']=result
            if obj.countError:
                result=obj.durbinWWatsonTestStatisticfor_TrendLine_Residuals()          
                #print('Durbin-Watson test statistic for trend line residuals:===={}'.format(result)) #Calculating Durbin-Watson test statistic for trend line residuals
                json_format['Durbin-Watson test statistic for trend line residuals']=result
            if obj.countError:
                result=obj.autocorrelation_Detected_In_Trend_Line_Residuals() 
                slope_fit_dwt_result=result       
                #print('Autocorrelation detected in trend line residuals:===={}'.format(result)) #Calculating Autocorrelation detected in trend line residuals
                json_format['Autocorrelation detected in trend line residuals']=result
            if obj.countError:
                result=obj.autocorrelationFunctionOrder()
                pacf_order=result
                #print('Autocorrelation function order:===={}'.format(result)) #Calculating Autocorrelation function order
                json_format['Autocorrelation function order']=result
            if obj.countError:
                result=obj.durbinWWatsonTestStatisticfor_Lag_1_AutoCorrelation()
                #print('Durbin-Watson test statistic for lag-1 autocorrelation:===={}'.format(result)) #calculating Durbin-Watson test statistic for lag-1 autocorrelation
                json_format['Durbin-Watson test statistic for lag-1 autocorrelation']=result
            if obj.countError:
                result=obj.lag_1_auto_correlation_detected()  
                dwt_lag1_result=result         
                #print('Lag-1 autocorrelation detected:===={}'.format(result))
                json_format['Lag-1 autocorrelation detected']=result
            if obj.countError:
                result=obj.zeroDemandfraction()
                #print('The Zero demand fraction===={}'.format(result)) #Calculating Zero demand fraction
                json_format['Zero demand fraction']=result
                zero_frac=result
            if obj.countError:
                result=obj.discreteIndicatorFlag()
                #print('The Discrete Indicator Flag is===={}'.format(result)) #Calculating Discreate Indicator Flag
                #json_format['Discrete Indicator Flag']=obj.discreteIndicatorFlag()
                flag=result
                if result:
                    json_format['Discrete Indicator Flag']=1
                else:
                    json_format['Discrete Indicator Flag']=0
            if obj.countError:
                result=obj.piosondistributionMLE()
                #print('The Poisson distribution MLE is===={}'.format(result)) #Calculating pioson distribution MLE Value
                json_format['Poisson distribution MLE']=result
            if obj.countError:  
                result=obj.chi_square_statistic_for_poison_distribution()        
                #print('The Chi-square test statistic for Poisson distribution===={}'.format(result)) # Calculating Chi-square test statistic for Poisson distribution
                json_format['Chi-square test statistic for Poisson distribution']=result[0]
            if obj.countError:
                result =obj.chi_square_statistic_for_poison_distribution()            
                #print('The Chi-square test degrees of freedom is===={}'.format(result)) #calculating Chi-square test degrees of freedom
                chipval=result
                json_format['Chi-square test degrees of freedom']=result[2]
            if obj.countError:
                result= obj.chi_square_statistic_for_poison_distribution()
                json_format['Chi-square p-value for Poisson distribution']=result[1]
            if obj.countError:
                result= obj.seasonality_model()
                json_format['Seasonality Period']=result[0]
            if obj.countError:
                result= obj.seasonality_model()
                json_format['Seasonality Adjusted R Square']=result[1]
            if obj.countError:
                result= obj.seasonality_model()
                json_format['Seasonality P-Value']=result[2]
            if obj.countError:
                result= obj.seasonality_model()
                json_format['Seasonality Sin p-val']=result[3]
            if obj.countError:
                result= obj.seasonality_model()
                json_format['Seasonality Cosine p-val']=result[4]
            if obj.countError:
                result= obj.diffusion_model()
                json_format['Diffusion model adjusted r-square']=result[0]
            if obj.countError:
                result= obj.diffusion_model()
                json_format['Diffusion model p-val']=result[1]
            if obj.countError:
                result= obj.diffusion_model()
                json_format['Diffusion model Y p-val']=result[2]
            if obj.countError:
                result= obj.diffusion_model()
                json_format['Diffusion model Z p-val']=result[3]
            if obj.countError:
                result= obj.diffusion_model()
                Ycum_pval=result[2]
                Z_pval=result[3]
                diff_r_sq=result[0]
            if obj.countError:
                result=obj.seasonality_model()
                seasonal_pval=result[2]
                seasonal_rsquare=result[1]

            result={}
            result['name']='Demand Analyzer'
            result['value']=[json_format]

            demand={}
            json_format1={}
            if(zero_frac > 0.1):
                var="Lumpy"
                json_format1['Demand Type']=var
            elif(flag=='True' and chipval>0.05):
                var="Poisson"
                json_format1['Demand Type']=var
            elif(flag=='False' and boxpval>0.05):
                var="Normal"
                json_format1['Demand Type']=var
            elif(seasonal_rsquare>0.6 and seasonal_pval<0.05):
                var="Seasonal"
                json_format1['Demand Type']=var
            elif(slope_pval<0.05 and slope_fit_dwt_result=='No'):
                var="Trending"
                json_format1['Demand Type']=var
            elif(Ycum_pval< 0.05 and Z_pval<0.05 and diff_r_sq>0.6):
                var="Diffusion"
                json_format1['Demand Type']=var
            elif(pacf_order>0 and dwt_lag1_result=='Yes'):
                var="Ar"
                json_format1['Demand Type']=var
            else:
                var="Unknown"
                json_format1['Demand Type']=var

            demand['name']='Demand Characterization'
            demand['value']=[json_format1]
            return [result,demand]
        except Exception:
            raise Exception("Error in processing the model")

  
