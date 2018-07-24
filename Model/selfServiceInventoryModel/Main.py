import json
import selfServiceInventoryModel
import sys
import testMain
from testMain import *
try:
	program_name = sys.argv[0]
	arguments = sys.argv[1:]
	count = len(arguments)
	filepath=arguments[0]
	function_name = arguments[1]
	datafile = arguments[2]
	logfile = arguments[3]
	outfile = arguments[4]
	errfile = arguments[5]

	def actionOnModule(path,pathOfOutputFile,pathOfErrorFile,moduleName):
		#calling the required module
		result = globals()[moduleName](path,pathOfErrorFile)
		with open(pathOfOutputFile,'w') as f:
			json.dump(result,f)

	def ListModels():
		modelName = ["DemandAnalyzer","ForecastRealignment","ForecastLumpyDemand","EOQ","ForecastAnalyzer","RSPeriodicReview","SQContinousReview","NewsVendor","ForecastErrorBasedStandard","MCBDemand","PoissonModel","ContainerLoop","DependentDemand","PartRepairLoop"]
		mappingCSV = {"DemandAnalyzer":"Demand_Analyzer.csv","ForecastRealignment":"ForecastRealignment.csv","ForecastLumpyDemand":"ForeCastLumpyDemand.csv","EOQ":"Eoq.csv","ForecastAnalyzer":"Forecast_Analyzer.csv","RSPeriodicReview":"rs_periodic_review.csv","SQContinousReview":"sq_continuous_review.csv","NewsVendor":"newsVendor.csv","ForecastErrorBasedStandard":"ForeCastErrorBased.csv","MCBDemand":"Mcb_Demand.csv","PoissonModel":"Poisson.csv","ContainerLoop":"Container_Loop.csv","DependentDemand":"Dependent_Demand.csv","PartRepairLoop":"partRepairLoop.csv"}
		mappingFunc = {"DemandAnalyzer":"DemandAnalyzer","ForecastRealignment":"ForecastRealignment","ForecastLumpyDemand":"ForecastLumpyDemand","EOQ":"EOQ","ForecastAnalyzer":"ForecastAnalyzer","RSPeriodicReview":"RSPeriodicReview","SQContinousReview":"SQContinousReview","NewsVendor":"NewsVendor","ForecastErrorBasedStandard":"ForecastErrorBasedStandard","MCBDemand":"MCBDemand","PoissonModel":"PoissonModel","ContainerLoop":"ContainerLoop","DependentDemand":"DependentDemand","PartRepairLoop":"PartRepairLoop"}
		mappingHeader = {"DemandAnalyzer":["(ActualHistoricalDemand)"],"ForecastRealignment":["(Forecast)","(Demand)"],"ForecastLumpyDemand":["LeadTime (Weeks)","ServiceLevel (%)","(YYYYWW)","(ActualHistoricalForecast)","(ActualHistoricalDemand)","(WWForFutureForecast)","(Future Forecast)"],"EOQ":["Average Demand(units/yr)","Variable Purchase Cost($/unit)","Fixed Ordering Cost($/order)","Unit Holding Cost($/yr)"],"ForecastAnalyzer":["(ActualHistoricalForecast)","(ActualHistoricalDemand)"],"RSPeriodicReview":["Demand Mean","Demand Sigma","Fixed Ordering Cost","Cost","Holding Charge(%)","Lead Time(Years)","Review Period","Cycle Service Level(%)","Cost per Stockout Event","Item Fill Rate(%)","Cost Per Item Short"],"SQContinousReview":["Demand Mean(units/yr)","Demand Sigma(units/yr)","Fixed Ordering Cost($/order)","Cost($/item)","Holding Charge(%/yr)","Lead Time(years)","Cycle Service Level(%)","Cost per Stockout Event($/event)","Item Fill Rate(%)","Cost Per Item Short($/item/yr)"],"NewsVendor":["Mean","Std.Dev","Cost","Price"],"ForecastErrorBasedStandard":["LeadTime (Weeks)","ServiceLevel (%)","(YYYYWW)","(ActualHistoricalForecast)","(ActualHistoricalDemand)","(WWForFutureForecast)","(Future Forecast)"],"MCBDemand":["LeadTime (Weeks)","ServiceLevel (%)","(ActualHistoricalDemand)"],"PoissonModel":["Demand Mean","Fixed Ordering Cost","Cost","Holding Charge(%)","Lead Time(years)","Reorder Point","Cycle Service Level(%)","Cost per Stockout Event","Item Fill Rate(%)","Cost Per Item Short"],"ContainerLoop":["(YYYYMM)","Container Size","Buffer Percentage(%)","(Site1 LRP Volumes)","(Site2 LRP Volumes)","(Site3 LRP Volumes)","(Site1 Loop Cycle Time(Days))","(Site2 Loop Cycle Time(Days))","(Site3 Loop Cycle Time(Days))","(Manual Buffer1(Containers))","(Manual Buffer2(Containers))","(Manual Buffer3(Containers))"],"DependentDemand":["(YYYYMM)","Attach Rate(%)","Dependent part business process loss(%)","Independant material lot size(Units)","Dependent material lot size(Units)","(Site1 For LRP Volumes(Months))","(Site2 For LRP Volumes(Months))","(Site3 For LRP Volumes(Months))","(Yield(%))"],"PartRepairLoop":["(YYYYMM)","Part repair Rate(%)","Buffer Percentage(%)","(Site1 LRP Volumes)","(Site2 LRP Volumes)","(Site3 LRP Volumes)","(Site1 loop cycle time(days))","(Site2 loop cycle time(days))","(Site3 loop cycle time(days))","(Manual Buffer1(Containers))","(Manual Buffer2(Containers))","(Manual Buffer3(Containers))"]}
		a = [{'modelName':modelName,'mappingCSV':mappingCSV,'mappingFunc':mappingFunc,'mappingHeader':mappingHeader}]
		with open(outfile,'w') as fileObj:
			json.dump(a, fileObj)

  #Main methods starts here------------------------------------------------
	if __name__ == '__main__':

		if function_name== "ListModels":
			ListModels()
		else:
			actionOnModule(datafile,outfile,errfile,function_name)
except Exception as e:
       print("exception in code ",e)
       with open(errfile,'w+') as f:
       	    # Beyond DEV, comment above line
       		f.write("Exception in code: " + str(e) + ". ")
       		f.write("Internal error, please contact support team.")
       #raise Exception("Exception in code execution")
