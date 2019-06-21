class mixZone:
    id = 0
    k_anonymity = 0
    latitude = 0
    longitude = 0
    radius = 0
    cars = 0
    geoLocation = (0,0)
    
    def __init__(self,id,k_anonymity,latitude,longitude,radius):
        self.id = id
        self.k_anonymity = k_anonymity
        self.latitude = latitude
        self.longitude = longitude
        self.geoLocation = (latitude,longitude)
    
    