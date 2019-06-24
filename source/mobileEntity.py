class mobileEntity:
    id=""
    pseudonym = ""
    trace = None
    index_current_location = 0
    in_mix_zone = False
    mix_zone = None
    number_of_anonymizations = 0
    anon_history = None

    def __init__(self,pseudonym,trace,id):
        self.pseudonym = pseudonym
        self.trace = [trace]
        self.id = id

    def setAnon(self,id_anon):
        if self.anon_history == None:
            print("{}-{}".format(len(self.trace),self.index_current_location))
            self.anon_history = {id_anon : self.trace[self.index_current_location][2]}
        else:
            self.anon_history[id_anon] = self.trace[self.index_current_location][2]
        self.number_of_anonymizations += 1

    def addTrace(self,trace):
        self.trace.append(trace)
        return None
    
    def getCurrentLocation(self):
        return self.trace[self.index_current_location]
    
    def nextLocation(self):
        self.index_current_location += 1
        if self.index_current_location < len(self.trace):
            return self.index_current_location
        else:
            self.index_current_location -= 1
            return -1

    def exitMixZone(self):
        self.in_mix_zone = False
        self.mix_zone.entityExit(self)
        self.mix_zone = None
        return None
    
    def enteringMixzone(self,mixzones):
        for mixzone in mixzones:
            if (mixzone.isInCoverage((self.trace[self.index_current_location][0], self.trace[self.index_current_location][1]))):
                self.mix_zone = mixzone
                self.in_mix_zone = True
                mixzone.entityEntered(self)
                return mixzone.id
        return None
    
    def info(self):
        return ("pseudonym: {} - number of trip records: {} - current location: {}".format(self.pseudonym,len(self.trace),self.trace[self.index_current_location]))
