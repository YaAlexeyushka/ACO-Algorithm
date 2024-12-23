class Vertex:
    def __init__(self, _name):
        self.name = _name 
        self.neighbors = {}
    
    def add_neighbor(self, _v, _weight):
        self.neighbors[_v] = [_weight]
        
    def get_neighbor_weight(self, _v):
        if _v in self.neighbors.keys():
            return self.neighbors[_v][0]
    
    def get_neighbors(self):
        return self.neighbors.keys()        
        
         