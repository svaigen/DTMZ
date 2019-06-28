from haversine import haversine
import dtmzUtils as utils
class mixZone:
    id = 0
    k_anonymity = 0
    latitude = 0
    longitude = 0
    radius = 0 #considering meters
    entities = {}
    geoLocation = (0,0)
    entities_covered = None
    entities_anonymized = None
    
    def __init__(self,id,k_anonymity,latitude,longitude,radius):
        self.id = id
        self.k_anonymity = k_anonymity
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        self.geoLocation = (latitude,longitude)
        self.entities_covered = None
        self.entities_anonymized = None
        self.entities = {}
    
    def isInCoverage(self, entity_location):
        distance = haversine((self.latitude,self.longitude),entity_location) * 1000
        return distance <= self.radius

    def entityExit(self,entity):
        if entity.id in self.entities:
            del self.entities[entity.id]        
        return None    

    def entityEntered(self,entity):
        self.entities[entity.id] = entity
        if len(self.entities) == self.k_anonymity:
            self.anonymize()
        if self.entities_covered is None:
            self.entities_covered = [entity]
        else:
            self.entities_covered.append(entity)
        return None

    def anonymize(self):
        for entity in self.entities:
            self.entities[entity].setAnon(utils.generatingRandomPseudonym(8))
            if self.entities_anonymized is None:
                self.entities_anonymized = [self.entities[entity]]
            else:
                self.entities_anonymized.append(self.entities[entity])
        self.entities = {}
        return None

    def info(self):
        return ("ID: {} - K-anom:{} - location:{} - radius-anom:{} m".format(self.id, self.k_anonymity, self.geoLocation, self.radius))
        
    
