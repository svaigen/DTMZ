import pandas as pd
import os
import shutil
import datetime as dt

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

# flow = calculateTripsByDayAndInterval("./../data/tripsPerDay/", INTERVAL_HALF_HOUR)
# flowToCSV(flow,getDays("./../data/tripsPerDay/"),"./../data/flow-day-interval-30-minutes.csv")


# input_dir = './../data/trips/'
# interval = generateIntervalsFlow(INTERVAL_HOUR)
# for file in os.listdir(input_dir):
#     df = pd.read_csv("{}{}".format(input_dir,file), delimiter=',', header=0)    
#     calculateTripsByInterval(interval, df['time'], INTERVAL_HOUR)
# print(interval)