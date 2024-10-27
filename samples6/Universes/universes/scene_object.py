from .shapes import geometrical_object as geoj
from .shapes import extrusion as ext

class Scene:
    def __init__(self):
        self.objects = {}
        self.selected = set([])
    def add(self, H, name):
        name2 = name.replace(' ','_')
        name = name2
        if name not in self.objects.keys():
            obj = geoj.GeometricalObject(H,name)
            self.objects[name] = obj
            self.select(name)
        return
    def select(self, name):
        name2 = name.replace(' ','_')
        name = name2
        keys = self.objects.keys()
        if name in keys:
            idx = name
        else:
            idx = None
        if idx is not None:
            self.selected = self.selected | set([idx])
        return
    def deselect(self, name):
        name2 = name.replace(' ','_')
        name = name2
        keys = self.objects.keys()
        if name in keys:
            idx = name
        else:
            idx = None
        if idx is not None:
            self.selected = self.selected - set([idx])
        return
    def deselectall(self):
        self.selected = set([])
        return
    def transform(self,T,R,S,Pivot=[0,0,0]):
        if self.selected is not set([]):
            L = list(self.selected)
            G = {}
            G['V'] = []
            G['E'] = []
            G['F'] = []
            G['N'] = []
            G['pts'] = []
            for key in L:
                H = self.objects[key].G
                G = ext.GraphUnionS(G,H)
            for key in L:
                self.objects[key].transform_G(\
                    G,T,R,S,Pivot)
        return  
    def get_G(self):
        G = {}
        G['V'] = []
        G['E'] = []
        G['F'] = []
        G['N'] = []
        G['pts'] = []
        keys = list(self.objects.keys())
        for key in list(keys):
            H = self.objects[key].G
            G = ext.GraphUnionS(G,H)
        return G
    def get_Gs(self):
        print(f"Deprecated: use get_Gs_names now.")
        Gs = []
        keys = list(self.objects.keys())
        for key in keys:
            H = self.objects[key].G
            Gs = ext.Append(Gs,H)
        return Gs
    def get_Gs_names(self):
        Gs = []
        keys = list(self.objects.keys())
        for key in keys:
            H = self.objects[key].G
            Gs = ext.Append(Gs,H)
        return Gs,keys
    def save(self, fn_save):
        # Save Scene 1
        Gs,keys = self.get_Gs_names()
        ext.Graphs2OBJ(fn_save,Gs,"scene",keys)


