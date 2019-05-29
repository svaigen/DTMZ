import pandas as pd
import os
import shutil
import datetime as dt

def compilingDataTrace():
    root_path = "./../data/viagens agrupadas por periodo/"
    dirs = ["trips_mixzone_0_(5, 17)_(5, 21)","trips_mixzone_0_(5, 22)_(5, 26)","trips_mixzone_0_(5, 27)_(5, 31)","trips_mixzone_0_(6, 1)_(6, 5)","trips_mixzone_0_(6, 6)_(6, 10)"]
    ending_path = "/arqs/trips_mixzone_0/"
    output_path = "./../data/tracesByEntity/"
    counter = 1
    for dir in dirs:
        input_path = "{}{}{}".format(root_path,dir,ending_path)
        for file in os.listdir(input_path):
            shutil.copyfile("{}{}".format(input_path,file),"{}{}.csv".format(output_path,counter))
            counter = counter + 1
    print ("Number of traces compiled: {}".format(counter - 1))
    return None

def orderingTraceID():
    path = "./../data/tracesByEntity/"
    for csv in os.listdir(path):
        id = csv.split('.')[0]
        df = pd.read_csv("{}{}".format(path,csv), delimiter=',', header=0)
        df['id_trace'] = id
        df.to_csv("{}{}".format(path,csv),index=False)
    return None

def separatingTracesByTrip():
    input_dir = "./../data/tracesByEntity/"
    trips_path = "./../data/trips/"
    counter = 1
    for csv in os.listdir(input_dir):
        df = pd.read_csv("{}{}".format(input_dir,csv), delimiter=',', header=0)
        for name, df_name in df.groupby('name'):
            df_name.to_csv("{}{}.csv".format(trips_path,counter),index=False)
            counter = counter + 1
    return None


def organizingTripsPerDay():
    dir_input = "./../data/trips/"
    dir_output = "./../data/tripsPerDay/"
    for csv in os.listdir(dir_input):
        df = pd.read_csv("{}{}".format(dir_input,csv), delimiter=',', header=0, nrows=2)
        date = (dt.datetime.fromtimestamp(df['time'].iloc[0]) - dt.timedelta(hours=7)).strftime("%Y-%m-%d")        
        shutil.copyfile("{}{}".format(dir_input,csv),"{}{}/{}".format(dir_output,date,csv))
    return None

def makeDirTripsPerDay():
    days = ['2008-05-19','2008-05-18','2008-05-21','2008-05-17','2008-06-08','2008-06-06','2008-06-07','2008-06-09','2008-05-20','2008-06-01','2008-06-04','2008-06-03','2008-06-05','2008-06-02','2008-05-24','2008-05-25','2008-05-23','2008-05-22','2008-05-26','2008-05-29','2008-05-28','2008-05-27','2008-05-30','2008-05-31']
    for day in days:
        os.mkdir("./../data/tripsPerDay/{}".format(day))
    return None

organizingTripsPerDay()
