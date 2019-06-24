import mobileEntity as me
import mixZone as mz
import datetime as dt
import dtmzUtils as utils

def simulation(mixzones,mobile_entities,log_file):
    time_references, time_ordered = generateTimeReferences(mobile_entities)
    lf = open(log_file,'w')
    lf.write("Initializing simulation at {}\n".format(dt.datetime.now()))
    while time_ordered:
        timestamp = time_ordered.pop(0)
        entities = time_references[timestamp]
        for entity in entities:
            if entity.index_current_location == 0:
                lf.write("m.e. {} started at {}\n".format(entity.pseudonym, utils.formatTimestamp(timestamp,"%H:%M:%S")))
            if entity.in_mix_zone:
                already_in_mix_zone = entity.mix_zone.isInCoverage((entity.getCurrentLocation()[0],entity.getCurrentLocation()[1]))
                if not already_in_mix_zone:
                    lf.write("m.e. {} exited from mz {} at time {}\n".format(entity.pseudonym,entity.mix_zone.id,utils.formatTimestamp(timestamp,"%H:%M:%S")))
                    entity.exitMixZone()     
            else:
                mz_id = entity.enteringMixzone(mixzones)
                if mz_id is not None:
                    lf.write("m.e. {} entering in mz {} at time {}\n".format(entity.pseudonym,mz_id,utils.formatTimestamp(timestamp,"%H:%M:%S")))            
            next_location = entity.nextLocation()
            if entity.nextLocation() == -1:
                lf.write("m.e. {} finished at {}\n".format(entity.pseudonym, utils.formatTimestamp(timestamp,"%H:%M:%S")))
            else:
                time = entity.getCurrentLocation()[2]
                if time in time_references:
                    time_references[time].append(entity)
                else:
                    time_references[time] = [entity]
                    time_ordered.append(time)
                    time_ordered.sort()
    anonymized_counter = 0
    covered_counter = 0
    for entity in mobile_entities:
        if(entity.number_of_anonymizations > 0):
            anonymized_counter += 1
            print("Entity anonymized: {}".format(entity.pseudonym))
            for anon in entity.anon_history:
                print("- Pseudonym: {} / timestamp: {}".format(anon,entity.anon_history[anon]))
            print()
    for mixzone in mixzones:
        if(mixzone.entities_covered is not None):
            covered_counter += len(mixzone.entities_covered)
            print("Mixzone {}, entities covered: {}".format(mixzone.id, len(mixzone.entities_covered)))
            for entity in mixzone.entities_covered:
                print("- {}".format(entity.pseudonym))
            print()
        if(mixzone.entities_anonymized is not None):
            print("Mixzone {}, entities anonymized: {}".format(mixzone.id, len(mixzone.entities_anonymized)))
            for entity in mixzone.entities_anonymized:
                print("- {}".format(entity.pseudonym))
            print()
    lf.write("Ending simulation at {}\n".format(dt.datetime.now()))
    lf.close()
    print("Total number of entities covered by mixzones: {} / {}".format(covered_counter,len(mobile_entities)))
    print("Total number of entitiver anonymized by mixzones: {} / {}".format(anonymized_counter, len(mobile_entities)))
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