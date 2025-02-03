from .shapes import geometrical_object as geoj
from .shapes import extrusion as ext
from . import transform_shape as ts
from copy import deepcopy

import numpy as np

def Graph2txt(G,name_obj,fn_mtl,name_mtl):
    txt = f"o {name_obj}\n"
    flag_v = False
    flag_n = False
    flag_t = False
    K = list(G.keys())
    if 'N' not in K:
        G['N'] = []
    if 'T' not in K:
        G['T'] = []
    if fn_mtl is not None:
        txt = txt + f"mtllib {fn_mtl}\n"
    for pt in G['pts']:
        flag_v = True
        x,y,z = pt
        s = f'v {x:.6f} {y:.6f} {z:.6f}\n'
        txt = txt + s
    for pt in G['N']:
        flag_n = True
        x,y,z = pt
        s = f'vn {x:.6f} {y:.6f} {z:.6f}\n'
        txt = txt + s
    for pt in G['T']:
        flag_t = True
        uu,vv = pt
        s = f'vt {uu:.6f} {vv:.6f}\n'
        txt = txt + s
    txt = txt + '\n'
    if name_mtl is not None and fn_mtl is not None:
        txt = txt + f'usemtl {name_mtl}\n'
    for fi in G['F']:
        s = 'f '
        for vi in fi:
            try:
                s += '/'.join(vi)+' '
            except:
                s += str(vi+1) + ' '
        s += '\n'
        txt = txt + s
    return txt

class Scene:
    def __init__(self):
        self.objects = {}
        self.selected = None
        self.idx_v2 = 0
        self.idx_vt2 = 0
        self.idx_vn2 = 0
        self.txts = {}
        self.txts2 = {}
        self.range = {}
        self.seq = []
    def add(self, H, name,
            fn_mtl=None, name_mtl=None):
        name2 = name.replace(' ','_')
        name = name2
        if name not in self.objects.keys():
            self.seq.append(name)
            obj = geoj.GeometricalObject(H,name)
            self.objects[name] = obj
            self.select(name)
            self.txts[name] = Graph2txt(\
                obj.G,name,fn_mtl,name_mtl)
            
            self.txts2[name],\
                idx_v2,\
                idx_vt2,\
                idx_vn2 = \
                ts.process(self.txts[name],\
                    [0,0,0],[1,1,1],[0,0,0],\
                    self.idx_v2,\
                    self.idx_vt2,\
                    self.idx_vn2)
            self.range[name] = \
                [(self.idx_v2,self.idx_vt2,self.idx_vn2),
                 (idx_v2,idx_vt2,idx_vn2)]
            self.idx_v2 = idx_v2
            self.idx_vt2 = idx_vt2
            self.idx_vn2 = idx_vn2
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
            self.selected = idx
        return
    def transform(self,T,R,S,Pivot=[0,0,0]):
        if self.selected is not None:
            self.objects[self.selected].transform(\
                T,R,S,Pivot)    
            self.txts2[self.selected] =\
                ts.static_process(\
                    self.txts2[self.selected],
                    R,S,T,\
                    self.range[self.selected])
        return
    def bbox(self):
        if self.selected is not None:
            obj = self.objects[self.selected]
            G = obj.G
            pts = deepcopy(G['pts'])
            P = np.array(pts)
            Pmin = np.min(P,axis=0)
            Pmax = np.max(P,axis=0)
            dims = Pmax - Pmin
            Pmin = list(map(float,list(Pmin.flatten())))
            Pmax = list(map(float,list(Pmax.flatten())))
            dims = list(map(float,list(dims.flatten())))
            return (Pmin,Pmax,dims)
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
        print(f"so.save:")
        Gs,keys = self.get_Gs_names()
        ext.Graphs2OBJ(fn_save,Gs,"scene",keys)
    def get_txt(self):
        txt = ""
        for i in range(len(self.seq)):
            name_i = self.seq[i]
            txt_i = self.txts2[name_i]
            txt = txt + txt_i
        return txt

