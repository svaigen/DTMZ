class mobileEntity:
    id = ""
    trace = []
    current_location = (0,0)
    in_mix_zone = False
    mix_zone_label = ""
    number_of_anonymizations = 0

    def __init__(self,id,trace):
        self.id = id
        self.trace = trace
        self.current_location = self.trace[0]

    