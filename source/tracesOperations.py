import pandas as pd
import os
import shutil

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

def separatingByTrip():
    input_dir = "./../data/tracesByEntity/"
    trips_path = "./../data/trips/"
    counter = 1
    for csv in os.listdir(input_dir):
        df = pd.read_csv("{}{}".format(input_dir,csv), delimiter=',', header=0)
        for name, df_name in df.groupby('name'):
            df_name.to_csv("{}{}.csv".format(trips_path,counter),index=False)
            counter = counter + 1
    return None

separatingByTrip()

