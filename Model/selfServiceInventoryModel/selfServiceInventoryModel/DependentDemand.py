class dependantDemand(object):
    def __init__(self,YYYYMM,attachRate,dependentPartBusinessProcessLoss,substrateLotSize,capacitorLotSize,site1ForLrpVolumesInMonths,site2ForLrpVolumesInMonths,site3ForLrpVolumesInMonths,yields):
        try:
            self.part_name_independent='substrate'
            self.part_name_dependent='capacitor'
            self.attach_rate=attachRate[0]
            self.dependent_part_business_process_loss=dependentPartBusinessProcessLoss[0]
            self.substrate_lot_size=substrateLotSize[0]
            self.capacitor_lot_size=capacitorLotSize[0]
            self.Site_1 =site1ForLrpVolumesInMonths
            self.Site_2 =site2ForLrpVolumesInMonths
            self.Site_3 =site3ForLrpVolumesInMonths
            self.yeild =yields
            self.YYYYMM=YYYYMM
            self.json_format={}
            print(self.Site_1)
        except Exception:
            raise Exception("Please check the values and try again")
            #return "Please Check the Input Format"
            #exit()
    def outputDepedentPartsNeeded(self):
        try:
            if (self.capacitor_lot_size>self.substrate_lot_size):
                mismatch= self.capacitor_lot_size%self.substrate_lot_size   
            else:
                mismatch= self.substrate_lot_size%self.capacitor_lot_size

            x = round(self.capacitor_lot_size / self.substrate_lot_size)
                
            if (self.capacitor_lot_size>self.substrate_lot_size):
                mismatch_loss=(mismatch/self.capacitor_lot_size)*100
            else:
                mismatch_loss=(mismatch/self.substrate_lot_size)*100
            dsite1=[];dsite2=[];dsite3=[];vftotal=[]

            for i in range(len(self.Site_1)):
                dsite1.append(self.Site_1[i]*self.attach_rate*(2-(self.yeild[i]/100))*(1+(self.dependent_part_business_process_loss/100)))
                dsite2.append(self.Site_2[i]*self.attach_rate*(2-(self.yeild[i]/100))*(1+(self.dependent_part_business_process_loss/100)))
                dsite3.append(self.Site_3[i]*self.attach_rate*(2-(self.yeild[i]/100))*(1+(self.dependent_part_business_process_loss/100)))
                vftotal.append(dsite1[i]+dsite2[i]+dsite3[i])
            y=round(mismatch_loss,2)
            self.json_format[('Mismatch %f units every %f lots')%(mismatch,x)]=mismatch
            self.json_format['Mismatch Loss']= y
            self.json_format['Units'] = x

            for i in range(1,len(self.Site_1)):
                self.json_format['Depedent parts Site1']=dsite1
                self.json_format['Depedent parts Site2']=dsite2
                self.json_format['Depedent parts Site3']=dsite3
                self.json_format['Depedent parts VF Total']=vftotal
            
            if(not self.YYYYMM):
                [self.YYYYMM.append('NA') for i in range(len(self.Site_1))]

            mis={}
            mis['name']= 'Mismatch Loss'
            mis['value']= [{'Mismatch':mismatch,'Units per Lot':x,'Mismatch Loss':y}]
            inp={}
            inp['name']= 'Input for Dependant Demand'
            inp['value'] = [{'YYYYMM':self.YYYYMM[ind],'Site1':self.Site_1[ind],'Site2':self.Site_2[ind],'Site3':self.Site_3[ind],'Yeild':self.yeild[ind]} for ind in range(len(self.Site_1))]
            result={}
            result['name']='Dependant Parts Needed'
            result['value'] = [{'YYYYMM':self.YYYYMM[ind],'Site1':dsite1[ind],'Site2':dsite2[ind],'Site3':dsite3[ind],'VF Total':vftotal[ind]} for ind in range(len(self.Site_1))]
            return [mis,inp,result]
        except Exception:
            raise Exception("Error in processing the model")
        
if __name__ == '__main__':
    obj=dependantDemand()
    obj.outputDepedentPartsNeeded()
  