class PositionTracker(object):
    def __init__(self):
        self.refdict = {"origin": (0, 0)}
    
    def get_abs_pos(self, name, x, y):
        return (x + self.refdict[name][0], y + self.refdict[name][1])
    
    def add_ref(self, name, x, y, ref = "origin"):
        self.refdict[name] = self.get_abs_pos(ref, x, y)
    
    def print(self):
        print(self.refdict)