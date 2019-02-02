#DTW with relaxed constraints and symmetric2 path
import numpy as np
class ForecastRealignment(object):

    def __init__(self,x,y):
        if((not x.any()) or (not y.any())):
            raise Exception("Please check the input values in excel and try again")
        self.x=x
        self.y=y
        self.window_min=0
        self.window_max=3     


    # Define the dynamic time warping function
    def dtw(self,x, y, window_min=-1, window_max=-1):
    
        # x and y are the two time series
        # window_min and window_max >=0 specity the global constraint
        # function returns the time aligned vectors along with index lookups
        # in the original input vectors
    
        # Padding time series with zeros
        self.window_min=window_min
        self.window_max=window_max
        self.x=x 
        self.y=y
        if x[0] != 0 or y[0] != 0:
            x = np.insert(x, 0, 0)
            y = np.insert(y, 0, 0)
        if x[np.size(x)-1] != 0 or y[np.size(y)-1] != 0:
            x = np.append(x, 0)
            y = np.append(y, 0)
        
        N = np.size(x)
        M = np.size(y)
        d = np.empty([N,M])
    
        # Remove global constraint if none is defined
        if (window_min==-1):
            window_min=N-1
        
        if (window_max==-1):
            window_max=M-1
    
        # Initialize the cost function
        for n in range(N):
            for m in range(M):
                d[n,m]=np.square(x[n]-y[m])
            
        D = np.ones(np.shape(d))*np.Inf
        D[0,0] = d[0,0]
    
        # Initialise edges with constraint
        for m in range(1,1+window_max):
            D[0,m] = d[0,m] + D[0,m-1]
        
        for n in range(1,1+window_min):
            D[n,0] = d[n,0] + D[n-1,0]
    
        # Forward Dynamic Programming    
        for n in range(1,N):
            for m in range(min(M,max(1,n-window_min-1)),min(n+window_max+1,M)):
                D[n,m] = np.min([d[n,m]+D[n-1,m],1*(d[n,m]+D[n-1,m-1]),d[n,m]+D[n,m-1]])
    
        Dist=D[N-1,M-1]
    
        # Cost should be infinity if no feasible path is found
        if Dist==np.Inf:
            raise Exception('No Feasible Path Found With Constraint Window')
    
        # Initialise and reverse look up lowest cost path
        n=N-1
        m=M-1

        x_out_idx=[N-1]
        y_out_idx=[M-1]
    
        while (n+m !=0):
            if (n==0):
                m=m-1
            elif (m==0):
                n=n-1
            else:
                idx = np.argmin([D[n-1,m-1],D[n,m-1],D[n-1,m]])
                if (idx==0):
                    n=n-1
                    m=m-1
                elif (idx==1):
                    m=m-1
                elif (idx==2):
                    n=n-1
        

            x_out_idx.insert(0,n)
            y_out_idx.insert(0,m)
    
        return (x[x_out_idx], y[y_out_idx], x_out_idx, y_out_idx)  
    
    def run(self):
        try:
            json_format={};json_format1={};
            m=[];n=[];
            json_format['name']='ForecastRealignment'
            a,b,c,d=self.dtw(self.x,self.y,self.window_min,self.window_max)
            #value['X_OUT']=a.tolist()
            #value['Y_OUT']=b.tolist()
            m=a.tolist()
            n=b.tolist()
            json_format1['name']='Input Forecast and Demand'
            json_format1['value']=[{'Forecast':self.x[i],'Demand':self.y[i]} for i in range(len(self.x))]
            json_format['value']=[{'Realigned Forecast':m[ind],'Realigned Demand':n[ind]} for ind in range(len(m))]
            #print(json_format)
            return [json_format1,json_format] 
        except Exception:
            raise Exception("Error in processing the model")


if __name__ == '__main__':
    '''
    # initialize and test the function using data    
    x = np.array([31.5,0,0,0,0,45.5,0,28,0,31.5,0,0,0,17.5,0,0,0,21,0])
    y = np.array([0,35.736,0,0,0,29.092,0,0,30,0,0,45.129,0,0,13.124,0,0,0,19.16])
    w_min=0
    w_max=3

    #(x_out, y_out, x_out_idx, y_out_idx) = dtw(x,y,w_min,w_max)
    p=ForecastRealignment(x,y,w_min,w_max)
    p.run()
    '''

        
