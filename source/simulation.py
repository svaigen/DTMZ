import mobileEntity as me
import mixZone as mz
import datetime as dt
import dtmzUtils as utils
import pandas as pd
import graphOperations as graphOp
import os

def simulation(G, n_mixzones, k_anonymity, mobile_entities_path,sim_file,mixzones_path, days, intervals, radius_mixzone):
    print("Simulation begins at {}".format(dt.datetime.now()))
    df_mixzones_selected = pd.read_csv(mixzones_path,delimiter=',', header=None)
    counter_day = 0
    counter_interval = 0
    counter_changes = 0
    mobile_entities, entities_per_day = utils.generateMobileEntities("{}".format(mobile_entities_path))
    time_references, time_ordered = generateTimeReferences(mobile_entities)
    # last_date = dt.datetime.strptime("{} {}".format(days[len(days)-1],intervals[len(intervals)-1]), '%Y-%m-%d %H:%M:%S')
    last_date = dt.datetime.strptime("{} 23:59:59".format(days[len(days)-1]), '%Y-%m-%d %H:%M:%S')
    
    #beginning simulation for day 0, interval 0
    print("Simulating initial interval")
    mixzones = graphOp.selectMixZonesByEngenvectorAndRegion(n_mixzones,G,k_anonymity, radius_mixzone)    
    while time_ordered:
        timestamp = time_ordered.pop(0)        
        # considered_date = dt.datetime.strptime("{} {}".format(days[counter_day],intervals[counter_interval]), '%Y-%m-%d %H:%M:%S')
        considered_date = dt.datetime.strptime("{} 23:59:59".format(days[counter_day]), '%Y-%m-%d %H:%M:%S')
        timestamp_date = dt.datetime.fromtimestamp(timestamp)
        if (timestamp_date > considered_date):
            genSimFile(days[counter_day],mixzones, entities_per_day[counter_day])
            for m in mixzones:
                for entity in m.entities:
                    m.entities[entity].in_mix_zone = False
                    m.entities[entity].mix_zone = None            
            if (timestamp_date > last_date):
                print("Simulation ends at {}".format(dt.datetime.now()))
                return None
            counter_changes += 1
            counter_day, counter_interval = adjustCounters(counter_changes, counter_day, counter_interval)
            selected_mixzones = df_mixzones_selected.iloc[counter_changes -1].values.tolist()
            mixzones = utils.generateMixZonesObjects(selected_mixzones,G,k_anonymity,radius_mixzone)
            # print("Simulating {} {}".format(days[counter_day],intervals[counter_interval]))
            print("Simulating {}".format(days[counter_day]))
        else:
            entities = time_references[timestamp]
            for entity in entities:
                if entity.in_mix_zone:
                    already_in_mix_zone = entity.mix_zone.isInCoverage((entity.getCurrentLocation()[0],entity.getCurrentLocation()[1]))
                    if not already_in_mix_zone:
                        entity.exitMixZone()     
                else:
                    entity.enteringMixzone(mixzones)                    
                next_location = entity.nextLocation()
                if not entity.nextLocation() == -1:                    
                    time = entity.getCurrentLocation()[2]
                    if time in time_references:
                        time_references[time].append(entity)
                    else:
                        time_references[time] = [entity]
                        time_ordered.append(time)
                        time_ordered.sort()
    print("Simulation ends at {}".format(dt.datetime.now()))
    return None

def generateTimeReferences(mobile_entities):
    time_references = {}
    time_ordered = []
    for entity in mobile_entities:
        if entity.getCurrentLocation()[2] in time_references:
            time_references[entity.getCurrentLocation()[2]].append(entity)
        else:
            time_ordered.append(entity.getCurrentLocation()[2])
            time_references[entity.getCurrentLocation()[2]] = [entity]
    time_ordered.sort()
    return time_references, time_ordered

def adjustCounters(counter_changes, counter_day, counter_interval):
    # counter_interval += 1
    # if counter_interval % 4 == 0:
    #     counter_interval = 0
    #     counter_day += 1
    counter_day += 1
    return counter_day, counter_interval

def genSimFile(day, mixzones, coverage_day):
    path_csv = "./simresults/{}.csv".format(day)
    path_txt = "./simresults/{}.txt".format(day)
    f = open(path_csv,"a") if (os.path.exists(path_csv)) else open(path_csv,"w")
    f_txt = open(path_txt,"a") if (os.path.exists(path_txt)) else open(path_txt,"w")
    for m in mixzones:
        entities_covered = 0 if m.entities_covered is None else len(m.entities_covered)
        entities_anonymized = 0 if m.entities_anonymized is None else len(m.entities_anonymized)
        f.write("{},{},{},{}\n".format(m.id,entities_covered,entities_anonymized,coverage_day))
        if entities_covered == 0:
            f_txt.write(" <-> ")
        else:
            for e in m.entities_covered:
                f_txt.write("{},".format(int(e.id)))
            f_txt.write(" <-> ")
        if not entities_anonymized == 0:
            for e in m.entities_anonymized:
                f_txt.write("{},".format(int(e.id)))
        f_txt.write("\n")
    f.close()
    f_txt.close()