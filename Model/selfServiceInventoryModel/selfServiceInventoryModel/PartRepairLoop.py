import math
import numpy as np
class partRepairLoop(object):
    def __init__(self,YYYYMM,partRepairRate,bufferPercentage,site1ForLRPVolumes,site2ForLRPVolumes,site3ForLRPVolumes,site1ForTotalLoopCycle,site2ForTotalLoopCycle,site3ForTotalLoopCycle,manualBuffer1,manualBuffer2,manualBuffer3):
        try:
            self.part_name='chemA'
            self.loopType='Repair'
            self.partRepairRate=partRepairRate
            self.bufferPercentage=bufferPercentage
            self.site1 = site1ForLRPVolumes
            self.site2 = site2ForLRPVolumes
            self.site3 = site3ForLRPVolumes
            self.totalLoopSite1 = site1ForTotalLoopCycle
            self.totalLoopSite2 = site2ForTotalLoopCycle
            self.totalLoopSite3 = site3ForTotalLoopCycle
            self.manualBuffer1 = manualBuffer1
            self.manualBuffer2 = manualBuffer2
            self.manualBuffer3 = manualBuffer3
            self.YYYYMM=YYYYMM
            self.json_format={}
        except Exception:
            raise Exception("Please check the values and try again")
    def calculatingOnPartRepairLoopFeatures(self):
        try:
            LRP =[];extraPartNSite1 =[];extraPartNSite2 =[];extraPartNSite3 = [];ep1 =[];ep2 =[];ep3 =[];buffer1 =[];buffer2 =[];totalbuffer =[];
            vfNB =[];vfB =[];k=[];avg=0;rollAvg =[];buffer3=[];totalManualBuffer=[];d=100;
            buffper= [x/d for x in self.bufferPercentage]
            arr = np.array(self.site1).tolist()
            arr1 = np.array(self.site2).tolist()
            arr2 = np.array(self.site3).tolist()
            tls1 = np.array(self.totalLoopSite1).tolist()
            tls2 = np.array(self.totalLoopSite2).tolist()
            tls3 = np.array(self.totalLoopSite3).tolist()
            for i in range(len(arr)):
                k = (arr[i]+arr1[i]+arr2[i])*buffper[0]
                LRP.append(k)
            self.json_format['30% Buffer']=LRP
            for i in range(len(arr)):
                extraPartNSite1.append(arr[i]/self.partRepairRate[0])
                extraPartNSite2.append(arr1[i]/self.partRepairRate[0])
                extraPartNSite3.append(arr2[i]/self.partRepairRate[0])
                ep1.append(round((extraPartNSite1[i]*tls1[i])/(buffper[0]*d)))
                k = (extraPartNSite2[i]*tls2[i])/(buffper[0]*d)
                ep2.append(math.ceil(k))
                ep3.append(round((extraPartNSite3[i]*tls3[i])/(buffper[0]*d)))
                buffer1.append(ep1[i]*buffper[0])
                buffer2.append(ep2[i]*buffper[0])
                buffer3.append(ep3[i]*buffper[0])
                totalbuffer.append(buffer1[i]+round(buffer2[i],2)+buffer3[i])
                totalManualBuffer.append(self.manualBuffer1[i]+self.manualBuffer2[i]+self.manualBuffer3[i])
                #VF with non-buffer
                vfNB.append(ep1[i]+ep2[i]+ep3[i])
                #VF value with buffer
                vfB.append(vfNB[i]+totalbuffer[i]+totalManualBuffer[i])  
            self.json_format['Extra Parts for Site1']=extraPartNSite1
            self.json_format['Extra Parts for Site2']=extraPartNSite2
            self.json_format['Extra Parts for Site3']=extraPartNSite3
            self.json_format['Site1(total loop cycle time)']=ep1
            self.json_format['Site2(total loop cycle time)']=ep2
            self.json_format['Site3(total loop cycle time)']=ep3
            self.json_format['Buffer1(total loop cycle time)']=buffer1
            self.json_format['Buffer2(total loop cycle time)']=buffer2
            self.json_format['Buffer3(total loop cycle time)']=buffer3
            self.json_format['Total Buffer']=totalbuffer
            self.json_format['Total Maunal Buffer']=totalManualBuffer
            self.json_format['VF Total (no buffer)']=vfNB
            self.json_format['VF Total (with buffer)']=vfB
            
            for i in range(len(vfB)):
                if(i+3 <=len(vfB)):
                    avg = (vfB[i]+vfB[i+1]+vfB[i+2])/3
                    rollAvg.append(avg)
                else:
                    rollAvg.append(rollAvg[i-1])

            self.json_format['3 Month Rolling Average']=rollAvg
            lrp_vol_json = {}
            if(not self.YYYYMM):
                [self.YYYYMM.append('NA') for i in range(len(arr))]
            lrp_vol_json['name']  = 'LRP_Volume'
            lrp_vol_json['value'] = [{'YYYYMM':self.YYYYMM[ind],'site1':arr[ind],'site2':arr1[ind],'site3':arr2[ind],'%_buff':LRP[ind]}  for ind in range(len(arr))]
            extraParts ={}
            extraParts['name'] = 'Extra Parts Needed'
            extraParts['value'] = [{'YYYYMM':self.YYYYMM[ind],'site1':extraPartNSite1[ind],'site2':extraPartNSite2[ind],'site3':extraPartNSite3[ind]} for ind in range(len(arr))]
            extra={}
            extra['name']='Extra Parts'
            extra['value']= [{'YYYYMM':self.YYYYMM[ind],'site1':ep1[ind],'site2':ep2[ind],'site3':ep3[ind],'Buffer1':buffer1[ind],'Buffer2':buffer2[ind],'Buffer3':buffer3[ind],'Total Buffer':totalbuffer[ind]} for ind in range(len(arr))]
            total={}
            total['name']= 'Total Buffer'
            total['value'] = [{'YYYYMM':self.YYYYMM[ind],'VF Total (no buffer)':vfNB[ind],'VF Total (with buffer)':vfB[ind],'3 Month Rolling Average':rollAvg[ind]} for ind in range(len(arr))]
            return [lrp_vol_json,extraParts,extra,total]
        except Exception:
            raise Exception("Error in processing the model")
            
      
if __name__ == '__main__':
    obj=partRepairLoop()
    obj.calculatingOnPartRepairLoopFeatures()
  