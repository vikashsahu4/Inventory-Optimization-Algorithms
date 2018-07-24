import numpy as np
from collections import OrderedDict

class ContainerLoop(object):
    def __init__(self,YYYYMM,containerSize,bufferPercentage,site1LRPVolumes,site2LRPVolumes,site3LRPVolumes,site1ForLoopCycle,site2ForLoopCycle,site3ForLoopCycle,manualBuffer1,manualBuffer2,manualBuffer3):
        try:
            self.materialName='chemA'
            self.materialType='Container'
            self.containerSize=containerSize[0]
            self.bufferPercentage=bufferPercentage
            self.csite1=[];self.csite2=[];self.csite3=[];self.buff=[];
            self.osite1=[];self.osite2=[];self.osite3=[];self.obuf1=[];self.obuf2=[];self.obuf3=[];self.tbuf=[];
            self.mbuf1=[];self.mbuf2=[];self.mbuf3=[];self.mtbuf=[];self.vftotal_nobuffer=[];self.vftotal_withbuffer=[];self.roll_avg=[];
            self.Site_1 =site1LRPVolumes
            self.Site_2= site2LRPVolumes
            self.Site_3= site3LRPVolumes
            self.tsite1=site1ForLoopCycle
            self.tsite2=site2ForLoopCycle
            self.tsite3=site3ForLoopCycle
            self.manualBuffer1=manualBuffer1
            self.manualBuffer2=manualBuffer2
            self.manualBuffer3=manualBuffer3
            self.YYYYMM=YYYYMM
            self.json_output={}
        except Exception:
            raise Exception("Please check the entered values in excel files and try again")
        
    def outputContainersMonth(self):
        try:
            for i in range(len(self.Site_1)):
                k=(self.Site_1[i]+self.Site_2[i]+self.Site_3[i])*(self.bufferPercentage[0]/100)
                self.buff.append(k)
                self.csite1.append(self.Site_1[i]/self.containerSize)
                self.csite2.append(self.Site_2[i]/self.containerSize)
                self.csite3.append(self.Site_3[i]/self.containerSize)

            self.json_output['Site1 Containers']=self.csite1
            self.json_output['Site2 Containers']=self.csite2
            self.json_output['Site3 Containers']=self.csite3
            self.json_output['Buffer']=self.buff
            return [self.csite1,self.csite2,self.csite3,self.buff]
        except Exception:
            raise Exception("Error in Processing the model")
    def outputContainerFleetPerMonthPerLittlesLaw(self):
        try:
            for i in range(len(self.Site_1)):
                self.osite1.append(self.csite1[i]*self.tsite1[i]/30)
                self.osite2.append(self.csite2[i]*self.tsite2[i]/30)
                self.osite3.append(self.csite3[i]*self.tsite3[i]/30)
                self.obuf1.append(self.osite1[i]*self.bufferPercentage[0]/100)
                self.obuf2.append(self.osite2[i]*self.bufferPercentage[0]/100)
                self.obuf3.append(self.osite3[i]*self.bufferPercentage[0]/100)
                self.tbuf.append(self.obuf1[i]+self.obuf2[i]+self.obuf3[i])

            self.osite1=list(map(lambda x:round(x,2),self.osite1))
            self.osite2=list(map(lambda x:round(x,2),self.osite2))
      
            self.json_output['Site1 for fleet']=self.osite1
            self.json_output['Site2 for fleet']=self.osite2
            self.json_output['Site3 for fleet']=self.osite3
            self.json_output['Buffer1 for fleet']=self.obuf1
            self.json_output['Buffer2 for fleet']=self.obuf2
            self.json_output['Buffer3 for fleet']=self.obuf3
            self.json_output['Total buffer fleet']=self.tbuf
            return [self.osite1,self.osite2,self.osite3,self.obuf1,self.obuf2,self.obuf3,self.tbuf]
        except:
            raise Exception("Error in Processing the model")
        
    def outputManualBuffer(self):
        try:
            self.mbuf1=self.manualBuffer1
            self.mbuf2=self.manualBuffer2
            self.mbuf3=self.manualBuffer3
            for i in range(len(self.Site_1)):
                self.mtbuf.append(self.mbuf1[i]+self.mbuf2[i]+self.mbuf3[i])

            for i in range(len(self.Site_1)):
                self.vftotal_nobuffer.append(self.osite1[i]+self.osite2[i])
           
            for i in range(len(self.Site_1)):
                self.vftotal_withbuffer.append(self.tbuf[i]+self.vftotal_nobuffer[i]+self.mtbuf[i])


            for i in range(len(self.Site_1)):
                if(i+3 <=len(self.Site_1)):
                    k=(self.vftotal_withbuffer[i]+self.vftotal_withbuffer[i+1]+self.vftotal_withbuffer[i+2])/3
                    self.roll_avg.append(k)
                else:
                    self.roll_avg.append(self.roll_avg[i-1])

            self.json_output['Total manual buffer']=self.mtbuf
            self.json_output['VF Total (no buffer)']=self.vftotal_nobuffer
            self.json_output['VF Total (with buffer)']=self.vftotal_withbuffer
            self.json_output['3 months rolling average']=self.roll_avg
            return [self.mtbuf,self.vftotal_nobuffer,self.vftotal_withbuffer,self.roll_avg]
        except Exception:
            raise Exception("Error in Processing the model")
        
    def returnJsonOutput(self):
        try:
            lrp_vol_json = {}
            lrp_vol_json['name']  = 'LRP_Volume'
            if(not self.YYYYMM):
                [self.YYYYMM.append('NA') for i in range(len(self.Site_1))]
            lrp_vol_json['value'] = [{'Site1':self.Site_1[ind],'Site2':self.Site_2[ind],'Site3':self.Site_3[ind],'30%_buff':self.buff[ind],'YYYYMM':self.YYYYMM[ind]}  for ind in range(len(self.Site_1))]
            fleet={}
            fleet['name']= 'Container Fleet per month'
            fleet['value']=[{'YYYYMM':self.YYYYMM[ind],'Site1':self.osite1[ind],'Site2':self.osite2[ind],'Site3':self.osite3[ind],'Output Buffer1':self.obuf1[ind],'Output Buffer2':self.obuf2[ind],'Output Buffer3':self.obuf3[ind],'Total Buffer':self.tbuf[ind]} for ind in range(len(self.Site_1))]
            manual={}
            manual['name']= 'Manual Buffer'
            manual['value']= [{'YYYYMM':self.YYYYMM[ind],'Total Manual Buffer':self.mtbuf[ind],'VF Total (no buffer)':self.vftotal_nobuffer[ind],'VF Total (with buffer)':self.vftotal_withbuffer[ind]} for ind in range(len(self.Site_1))]
            roll={}
            roll['name']= 'Rolling Average'
            roll['value']= [{'3 months rolling average':self.roll_avg[ind]} for ind in range(len(self.roll_avg))]
            return [lrp_vol_json,fleet,manual,roll]
        except Exception:
            raise Exception("Error in Processing the model")

        
    