import sys
from scipy.stats import poisson
import numpy as np
from collections import OrderedDict
class PoissonModel(object):

    def __init__(self,dm,foc,cost,hc,lt,rp,csl,cpse,ifr,cpis):
        try:
            self.dm = dm
            self.dmcis=dm
            #self.ds = pow(self.dm,0.5)
            self.foc = foc
            self.cost = cost
            self.hc = hc
            self.hccis=hc
            self.lt = lt
            self.rp = rp
            self.csl = csl
            self.cpse = cpse
            self.ifr = ifr
            self.cpis = cpis
        except Exception:
           raise Exception("Input format is not correct.Check documentation for sample input/output.")

    def common_calculations(self):
        #self.uhc = self.cost*self.hc
        #self.oq = self.dm* self.rp
        #self.mdolt = self.dm*(self.lt+self.rp)
        tdm=self.dm;tlt=self.lt;trp=self.rp;
        self.uhc   = [self.cost*self.hc for self.cost, self.hc in zip(list(self.cost), list(self.hc))]
        self.oq    = [self.dm*self.rp for self.dm, self.rp in zip(self.dm, self.rp)]
        self.mdolt = [tdm * (tlt + trp) for tdm,tlt,trp in zip(tdm,tlt,trp)]
        #print(self.mdolt)
        #print(self.uhc,self.oq,self.mdolt)
        #print(type(self.lt), type(self.rp),type(rp))

    # meet cycle service level    
    def meet_csl(self):
        reorder_point = poisson.ppf(self.csl, self.mdolt)
        #print(reorder_point.tolist())
        return reorder_point.tolist()


    # meet item fill rate
    def meet_ifr(self):
        #print(self.ifr,self.oq)
        array_es = [(1 - tifr) * toq for tifr, toq in zip(self.ifr, self.oq)]
        reorder_points = []
        for es, index in zip(array_es, range(len(self.mdolt))):
            s = 0  # s will be reorder point
            # stop if es-val is positive
            lb = 0  # lower bound
            for ub in range(int(pow(sys.maxsize, 0.5))):  # theoritical infinity
                s = pow(2, ub)
                pp1 = poisson.cdf(s - 1, self.mdolt[index])
                pp2 = poisson.cdf(s, self.mdolt[index])
                val = (self.mdolt[index] * (1 - pp1)) - (s * (1 - pp2))
                if (es - val) >= 0:
                    break
            if (ub > 10):  # if within 2^10 = 1000 simply follow linear search
                lb = ub - 1
            for s in range(pow(2, lb) - 1, pow(2, ub) + 1, 1):  # linear search in the found interval
                pp1 = poisson.cdf(s - 1, self.mdolt[index])
                pp2 = poisson.cdf(s, self.mdolt[index])
                val = (self.mdolt[index] * (1 - pp1)) - (s * (1 - pp2))
                if (es - val) >= 0:
                    break
            reorder_points.append(s)
        #print(reorder_points)
        return reorder_points

    def meet_cis(self):
        result = []
        #print(self.hccis)
        for index in range(len(self.cpis)):
            if self.cpis[index] == 0 or self.dmcis[index] == 0:
                result.append(0)
                #print("11111")
                pass
            prev = sys.maxsize # theoritical infinity
            lb = 0  # lower bound
            for ub in range(int(pow(sys.maxsize, 0.5))):  # theoritical infinity
                s = pow(2,ub)
                pp1 = poisson.cdf(s - 1, self.mdolt[index])
                pp2 = poisson.cdf(s, self.mdolt[index])
                val = (((self.hccis[index] * self.oq[index]) / (self.cpis[index] * self.dmcis[index])) * s) + (self.mdolt[index] * (1 - pp1)) - (s * (1 - pp2))
                if (val - prev) >= 0:
                    break
                prev = val
            if ub > 10:  # if within 2^10 = 1000 simply follow linear search
                lb = ub - 1
            prev = sys.maxsize
            for s in range(pow(2, lb)-1, pow(2, ub)+1, 1):
                pp1 = poisson.cdf(s-1,self.mdolt[index])
                pp2 = poisson.cdf(s,self.mdolt[index])
                val = (((self.hccis[index]*self.oq[index])/(self.cpis[index]*self.dmcis[index]))*s) + (self.mdolt[index]*(1-pp1))- (s*(1-pp2))
                if(val-prev) >= 0:
                    break
                prev = val
            result.append(s-1)
        #print(result)
        return result


    def meet_csoe(self):
        # s is the reorder point
        # val is positive
        result = []
        #print(self.oq,self.mdolt,self.cpse,self.dmcis,self.hccis)
        for index in range(len(self.oq)):
            if self.oq[index] == 0: # divide by zero
                result.append(0)
                pass
            lb =0
            for ub in range(int(pow(sys.maxsize, 0.5))):  # theoritical infinity
                s = pow(2, ub)
                pp = poisson.pmf(s + 1, self.mdolt[index])
                val = self.hccis[index] - (self.cpse[index] * (self.dmcis[index] / self.oq[index]) * pp)
                if val >= 0:
                    break
            if ub > 10:  # if within 2^10 = 1000 simply follow linear search
                lb = ub - 1

            for s in range(sys.maxsize):
                pp = poisson.pmf(s+1, self.mdolt[index])
                val = self.hccis[index] - (self.cpse[index] *(self.dmcis[index]/self.oq[index]) * pp)
                if(val >= 0):
                    break
            result.append(s)
        #print(result)
        return result


    def run(self):
        # do common calculaiton
        #try:
            self.common_calculations()
            json_format ={}
            json_format['name']="Poisson Model"
            value = {}
            Reorder_point_to_meet_csl  = self.meet_csl()
            Reorder_point_to_meet_ifr  = self.meet_ifr()
            Reorder_point_to_meet_cis  = self.meet_cis()

            Reorder_point_to_meet_csoe = self.meet_csoe()

            json_format['value'] = [{'Rp_to_meet_csl':Reorder_point_to_meet_csl[index],
                      'Rp_to_meet_ifr':Reorder_point_to_meet_ifr[index],
                      'Rp_to_meet_cis':Reorder_point_to_meet_cis[index],
                      'Rp_to_meet_csoe':Reorder_point_to_meet_csoe[index]
                      }for index in range(len(Reorder_point_to_meet_cis))]

            #print([json_format])
            return [json_format]
        #except Exception:
            #raise Exception("Error in processing the model")

    

if __name__ == '__main__':
	'''
	
    dm = [1,2,3]
    foc = [3270,2345,4]
    cost = [25,25,5]
    hc = [0.15,0.15,6]
    lt = [0.02,0.02,0.03]
    rp = [0.08, 0.08, 0.14]
    csl = [0.95,0.95,0.86]
    cpse = [50000,50000,30000]
    ifr = [0.99,0.99,0.92]
    cpis = [45,45,30]

    p = PoissonModel(dm,foc,cost,hc,lt,rp,csl,cpse,ifr,cpis)
    #print(type(self.dm),type(self.cpis))
    print(p.run())
    '''