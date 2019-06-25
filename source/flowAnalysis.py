import pandas as pd
import os
import shutil
import datetime as dt
import numpy as np
import dtmzUtils as utils

INTERVAL_HOUR = 1
INTERVAL_HALF_HOUR = 2
INTERVAL_QUARTER_HOUR = 3

def generateIntervalsFlow(granularity, number_of_days):
    if(granularity == INTERVAL_HOUR):
        return {'00:00:00':[0] * number_of_days,'01:00:00':[0] * number_of_days,'02:00:00':[0] * number_of_days,'03:00:00':[0] * number_of_days,'04:00:00':[0] * number_of_days,'05:00:00':[0] * number_of_days,'06:00:00':[0] * number_of_days,'07:00:00':[0] * number_of_days,'08:00:00':[0] * number_of_days,'09:00:00':[0] * number_of_days,'10:00:00':[0] * number_of_days,'11:00:00':[0] * number_of_days,'12:00:00':[0] * number_of_days,'13:00:00':[0] * number_of_days,'14:00:00':[0] * number_of_days,'15:00:00':[0] * number_of_days,'16:00:00':[0] * number_of_days,'17:00:00':[0] * number_of_days,'18:00:00':[0] * number_of_days,'19:00:00':[0] * number_of_days,'20:00:00':[0] * number_of_days,'21:00:00':[0] * number_of_days,'22:00:00':[0] * number_of_days,'23:00:00':[0] * number_of_days}
    elif (granularity == INTERVAL_HALF_HOUR):
        return {'00:00:00':[0] * number_of_days,'00:30:00':[0] * number_of_days,'01:00:00':[0] * number_of_days,'01:30:00':[0] * number_of_days,'02:00:00':[0] * number_of_days,'02:30:00':[0] * number_of_days,'03:00:00':[0] * number_of_days,'03:30:00':[0] * number_of_days,'04:00:00':[0] * number_of_days,'04:30:00':[0] * number_of_days,'05:00:00':[0] * number_of_days,'05:30:00':[0] * number_of_days,'06:00:00':[0] * number_of_days,'06:30:00':[0] * number_of_days,'07:00:00':[0] * number_of_days,'07:30:00':[0] * number_of_days,'08:00:00':[0] * number_of_days,'08:30:00':[0] * number_of_days,'09:00:00':[0] * number_of_days,'09:30:00':[0] * number_of_days,'10:00:00':[0] * number_of_days,'10:30:00':[0] * number_of_days,'11:00:00':[0] * number_of_days,'11:30:00':[0] * number_of_days,'12:00:00':[0] * number_of_days,'12:30:00':[0] * number_of_days,'13:00:00':[0] * number_of_days,'13:30:00':[0] * number_of_days,'14:00:00':[0] * number_of_days,'14:30:00':[0] * number_of_days,'15:00:00':[0] * number_of_days,'15:30:00':[0] * number_of_days,'16:00:00':[0] * number_of_days,'16:30:00':[0] * number_of_days,'17:00:00':[0] * number_of_days,'17:30:00':[0] * number_of_days,'18:00:00':[0] * number_of_days,'18:30:00':[0] * number_of_days,'19:00:00':[0] * number_of_days,'19:30:00':[0] * number_of_days,'20:00:00':[0] * number_of_days,'20:30:00':[0] * number_of_days,'21:00:00':[0] * number_of_days,'21:30:00':[0] * number_of_days,'22:00:00':[0] * number_of_days,'22:30:00':[0] * number_of_days,'23:00:00':[0] * number_of_days,'23:30:00':[0] * number_of_days}

def getDateIntervalIndex(granularity,timestamp):
    formatted_date = dt.datetime.fromtimestamp(timestamp) - dt.timedelta(hours=7) #timedelta: managing timestamp to UTC -7 of San Francico
    if (granularity == INTERVAL_HOUR):        
        return formatted_date.hour       
    elif (granularity == INTERVAL_HALF_HOUR):
        return ( 2 * formatted_date.hour + formatted_date.minute // 30)

def calculateTripsFlow(interval, index_day, timestamps, granularity):
    interval_indexes_to_check = [False] * len(interval)
    for timestamp in timestamps:
        index = getDateIntervalIndex(granularity,timestamp)
        interval_indexes_to_check[index] = True
    for i in range(len(interval_indexes_to_check)):
        if (interval_indexes_to_check[i] == True):
            interval[list(interval)[i]][index_day] += 1
    return None

def getDays(days_path):
    days = []
    for day in os.listdir(days_path):
        days.append(day)
    return days

def calculateTripsByDayAndInterval(days_path,granularity):
    print("Calculating flow...")    
    days = getDays(days_path)
    flow_interval = generateIntervalsFlow(granularity,len(days))
    index_day = 0
    for day in os.listdir(days_path):
        print("Calculating day {} ({}/{})".format(day,index_day + 1,len(days)))
        for trips in os.listdir("{}{}".format(days_path,day)):
            df = pd.read_csv("{}{}/{}".format(days_path,day,trips), delimiter=',', header=0)
            calculateTripsFlow(flow_interval, index_day, df['time'], granularity)                        
        index_day+=1   
    return flow_interval

def flowToCSV(flow,days,output_file):
    print("Generating .csv ...")
    f = open(output_file,'w')
    intervals = ""
    for key in flow:
        intervals += "{},".format(key)
    f.write("day,{}\n".format(intervals))
    for i in range(len(days)):
        flow_day = ""
        for key in flow:
            flow_day += "{},".format(flow[key][i])
        f.write("{},{}\n".format(days[i],flow_day))
    f.close()
    print("Done! File available in: {}".format(output_file))
    return None

def calculateFlow(regions_flow_history,mobile_entities,cluster_model):
    for entity in mobile_entities:
        regions_time_matched = {}
        for point in entity.trace:
            location = np.asarray([point[0],point[1]]).reshape(1,-1)
            prediction = cluster_model.predict(location)
            region_time_key = generateRegionTimeKey(prediction[0], point[2])
            regions_time_matched[region_time_key] = 1
        for key in regions_time_matched:
            reg = key.split()[0]
            day = key.split()[1]
            interval_t = key.split()[2]
            regions_flow_history[int(reg)].ix[utils.getIndexDay(day),interval_t] += 1
    return None

def generateRegionTimeKey(region,timestamp):
    d = dt.datetime.fromtimestamp(timestamp) - dt.timedelta(hours=7)
    intervals = [dt.datetime.strptime("05:59:59","%H:%M:%S"),dt.datetime.strptime("10:59:59","%H:%M:%S"),dt.datetime.strptime("16:59:59","%H:%M:%S"),dt.datetime.strptime("23:59:59","%H:%M:%S")]
    t_interval = ""
    for interval in intervals:
        t_interval = interval.time()
        if d.time() < interval.time():
            break
    key = "{} {} {}".format(region,d.strftime("%Y-%m-%d"),t_interval.strftime("%H:%M:%S"))
    return key

def initializeRegionsFlowHistory(n_regions,rows,cols):
    regions_flow_history = {}
    for r in range(n_regions):
        df = pd.DataFrame(columns=cols)
        df.set_index('day')
        df['day'] = rows
        for col_id in range(1,len(cols)):
            df[cols[col_id]] = 0
        regions_flow_history[r] = df
    return regions_flow_history

def calculateRegionFlowHistory(days,time_intervals,kmeans):
    regions_flow_history = utils.initializeRegionsFlowHistory(n_regions,days,['day'] + time_intervals)
    for day in days:
        print("Calculating day: {}".format(day))
        mobile_entities = utils.generateMobileEntitiesByFolder("./../data/tripsPerDay/{}/".format(day))    
        flow.calculateFlow(regions_flow_history,mobile_entities,kmeans)
    for pd in regions_flow_history:
        regions_flow_history[pd].to_csv("./../flow/region-{}.csv".format(pd))
    return None


# flow = calculateTripsByDayAndInterval("./../data/tripsPerDay/", INTERVAL_HALF_HOUR)
# flowToCSV(flow,getDays("./../data/tripsPerDay/"),"./../data/flow-day-interval-30-minutes.csv")


# input_dir = './../data/trips/'
# interval = generateIntervalsFlow(INTERVAL_HOUR)
# for file in os.listdir(input_dir):
#     df = pd.read_csv("{}{}".format(input_dir,file), delimiter=',', header=0)    
#     calculateTripsByInterval(interval, df['time'], INTERVAL_HOUR)
# print(interval)