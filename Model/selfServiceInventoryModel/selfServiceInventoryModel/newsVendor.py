import math
from scipy.stats import norm
import numpy 
from collections import OrderedDict
class newsVendorModel(object):
    """
        Constructor to create a newsVendorModel
        Parameter
        ---------
        mean: average demand
        sd: standard deviation of a normally distributed demand
        cost: Cost of a product
        price: The selling price of a product 
    """
    def __init__(self, mean, sd, cost, price, minOrderSize):

        #input checking
        try:
            if mean < 0: 
                raise Exception("Please check the values and try and again")
            if sd <= 0:
                raise Exception("Please check the values and try and again")
            if cost <= 0 or cost>price:
                raise Exception("Please check the values and try and again")
            if minOrderSize < 1:
                raise Exception("Please check the values and try and again")
            self.mean = mean
            self.sd = sd
            self.cost = cost
            self.price = price
            self.minOrderSize = minOrderSize
            """ 
            mean = 3200
            sd = 1100
            cost = 15
            price = 25
            minOrderSize = 250
            """        
            #calculations
            self.shortageLoss= self.price - self.cost
            self.excessLoss = self.cost
            self.lossRatio = (self.shortageLoss / (self.excessLoss + self.shortageLoss))
            z = norm.ppf(self.lossRatio) #calculates inverse of the noraml cumulative distribution
            self.optimalOrder = z*sd + mean
        except Exception:
            raise Exception("Please check the values and try and again")

    def shortageLoss(self):    
        return self.shortageLoss

    def excessLoss(self):
        return self.excessLoss

    def lossRatio(self):
        return self.lossRatio

    

    #given the input variables calculates zScore of a sample mean
    def calcZscore(self,sampleMean):
        #in our example standard error will simply be standard deviation
        try:
            return ((sampleMean - self.mean) / self.sd)
        except Exception:
            #print("Zero Divison Error")
            raise Exception("Zero Divison Error")
    
    
    """
    Function returns the optimal order regardless if it is possible with our minimum order size or not.
    """
    
    def getOptimalOrder(self):
        return self.optimalOrder
       
    """
    Function to calculate the optimal order size. Since we have a minimum order size the actual 
    optimal order size may not be possible. We will have to choose between a shortage or an 
    excess. This function will return which of the two has a lower total cost.
    Outputs
    -------
    possibleOptimalOrder = size of the best possible order
    """
    def calcPossibleOptimalOrder(self):
        if (self.optimalOrder % self.minOrderSize != 0):
            
            #one minOrderSize less than optimal
            lower = (self.minOrderSize * math.floor(self.optimalOrder / self.minOrderSize))
            #one minOrderSize more than optimal
            upper = lower + self.minOrderSize 
            #check if surplus * surplus cost < shortage * shortage cost
            if (((upper - self.optimalOrder)* self.cost) < ((self.optimalOrder - lower) * (self.price - self.cost))):
                possibleOptimalOrder = upper 
            else:
                possibleOptimalOrder = lower
            
        else:
            possibleOptimalOrder = self.optimalOrder
        return possibleOptimalOrder
        
    
    """
    Function estimates the expected profits of an ordersize for a model created
    
    Parameters:
        numIntervals: number of intervals to simulate a CDF. Larger numbers 
        will be more accurate, but slower. 
        
        orderSize: the amount of products you will order. Usually you will want 
        to calculate the result given by the optimal order size, but you can 
        specify any other quantity. 
        
        factor: How many standard deviations to select a range of demand values
        For reference 1 = 68%, 2 = 95%, 3 = 99.7% of the population. Again more
        accuracy sacrifices performance
        
        numIntervals = 10000 and factor = 3 is a good starting point 
        
        
    Outputs:
        Returns the expected profit from a given order size
    """
    def calcExpectedProfits(self, numIntervals, orderSize, factor):
        if self.sd*factor > self.mean:
            #fail we must find the z score of z because 1 side is skewed
            lowerZ = self.calcZscore(0)
            lowerBound = 0
            upperBound = abs(lowerZ * self.sd) + self.mean
        
        else:
            lowerBound = self.mean - self.sd*factor 
            upperBound = self.mean + self.sd*factor
        #set up demands            
      
        demandList = numpy.linspace(lowerBound,upperBound, numIntervals)
        #gather cdfs of demand
        cdfList = norm(self.mean,self.sd).cdf(demandList)
        #initialize pdfList with first result of cdfList     
        pdfList = [cdfList[0]]
        #creates the pdflist to multiply with profit and add
        for index,value in enumerate(cdfList[1:], start=1):
            addItem = value - cdfList[index-1]
            pdfList.append(addItem)
        #creates list of profits 
        profitsList = []
        for index, value in enumerate(demandList):
            profitsList.append(self.price * min(value,orderSize) - self.cost*orderSize)
        return sum(map(lambda x1,y1: x1 * y1, profitsList,pdfList))
    def graphpoints(self,mean,price,cost,sd):
        
        evalpoints=10
        
        def expProfit(Q,mean,sd,price,cost):
            k = (Q-mean[0])/sd[0]
            Gk = norm.pdf(k,loc=0,scale=1) - k*(1-norm.cdf(k,loc=0,scale=1))
            return(mean[0]*price[0] - cost[0]*Q - price[0]*sd[0]*Gk)
        #print(mean[0])
        
        llim = int(mean[0]-2*sd[0])
        #print(llim)
        
        step = int(round(4*sd[0]/(evalpoints-1)))
        #print(step)
        
        ulim = int(round(llim+(evalpoints-1)*step))
        #print(ulim)

        EProfit=numpy.zeros(evalpoints)
        Order = numpy.zeros(evalpoints)
        #print(Order)
        i=0;

        for Q in range(llim,ulim+1,step):
            Order[i]=Q
            EProfit[i]=expProfit(Q,mean,sd,price,cost)
            i+=1
        #print(EProfit,Order)
        return[Order,EProfit]
        
def mainnewsVendorFunction(mean, sd, cost, price):
    #try:
        #print(shortageLoss)
        json_format ={}
        obj=newsVendorModel(mean=mean, sd=sd, cost=cost, price=price, minOrderSize=250)
        calz = obj.calcZscore(sampleMean=3200)
        # print('zScore===={}'.format(calz[0]))
        #json_format['zScore']=calz[0]
        optimalOrder = obj.getOptimalOrder()
        # print('optimal order regardless if it is possible with our minimum order size or not ===={}'.format(optimalOrder[0]))
        json_format['Optimal order']=round(optimalOrder[0])
        posoptimalOrder = obj.calcPossibleOptimalOrder()
        # print('Function to calculate the optimal order size (possibleOptimalOrder = size of the best possible order) ===={}'.format(posoptimalOrder))
        json_format['Optimal order size']=posoptimalOrder
        
        cal = obj.calcExpectedProfits(numIntervals =10000,orderSize=250, factor =3)
        # print('Function estimates the expected profits of an ordersize for a model created (Returns the expected profit from a given order size) ===={}'.format(cal[0]))
        json_format['Expected profit']=round(cal[0])
        
        graph={}
        #json_format1={}
        order,profit= obj.graphpoints(mean=mean,sd=sd,cost=cost,price=price)
        #json_format1['Order']=order.tolist()
        #json_format1['Profit']=profit.tolist()
        graph['name']='Graph'
        graph['value']=[{'Order':order.tolist()[ind],'Profit':profit.tolist()[ind]} for ind in range(10)]
        result= {}
        result['name'] = 'NewsVendor'
        result['value']= [json_format]
        return [result,graph]
    #except Exception:
    #    raise Exception("Please check the input values and try again")
    
            
    

    
        
        
        
        


    