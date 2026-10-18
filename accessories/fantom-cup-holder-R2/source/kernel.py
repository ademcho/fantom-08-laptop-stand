"""Small direct OpenCascade adapter; uses existing OCP, avoids scipy import hydration.
API subset used by generate.py. No extra packages installed.
"""
from math import pi
from OCP.gp import gp_Pnt,gp_Vec,gp_Trsf,gp_Ax1,gp_Dir
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox,BRepPrimAPI_MakeCylinder
from OCP.BRepAlgoAPI import BRepAlgoAPI_Fuse,BRepAlgoAPI_Cut,BRepAlgoAPI_Common
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform,BRepBuilderAPI_MakePolygon,BRepBuilderAPI_MakeFace
from OCP.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCP.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.STEPControl import STEPControl_Reader,STEPControl_Writer,STEPControl_AsIs
from OCP.StlAPI import StlAPI_Writer
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID,TopAbs_EDGE,TopAbs_FACE,TopAbs_REVERSED
from OCP.TopoDS import TopoDS,TopoDS_Compound
from OCP.BRep import BRep_Builder,BRep_Tool
from OCP.BRepAdaptor import BRepAdaptor_Curve
from OCP.TopLoc import TopLoc_Location

class V:
    def __init__(self,x,y,z):self.X,self.Y,self.Z=x,y,z
    def __iter__(self):return iter((self.X,self.Y,self.Z))
class Bounds:
    def __init__(self,s):
        b=Bnd_Box();BRepBndLib.AddOptimal_s(s,b,False,False)
        x,y,z,X,Y,Z=b.Get();self.min=V(x,y,z);self.max=V(X,Y,Z);self.size=V(X-x,Y-y,Z-z)
class Axis:
    X=(1,0,0);Y=(0,1,0);Z=(0,0,1)
class Shape:
    def __init__(self,s):self.s=s
    def _op(self,b,cls):
        op=cls(self.s,b.s);op.Build();assert op.IsDone();return Shape(op.Shape())
    def __add__(self,b):return self._op(b,BRepAlgoAPI_Fuse)
    def __sub__(self,b):return self._op(b,BRepAlgoAPI_Cut)
    def __and__(self,b):return self._op(b,BRepAlgoAPI_Common)
    def bounding_box(self):return Bounds(self.s)
    @property
    def volume(self):
        p=GProp_GProps();BRepGProp.VolumeProperties_s(self.s,p);return p.Mass()
    @property
    def is_valid(self):return BRepCheck_Analyzer(self.s).IsValid()
    def solids(self):
        exp=TopExp_Explorer(self.s,TopAbs_SOLID);items=[]
        while exp.More():items.append(exp.Current());exp.Next()
        return items
    def moved(self,loc):return loc*self
    def rotate(self,axis,angle):
        t=gp_Trsf();t.SetRotation(gp_Ax1(gp_Pnt(0,0,0),gp_Dir(*axis)),angle*pi/180)
        return Shape(BRepBuilderAPI_Transform(self.s,t,True).Shape())
    def tessellate(self,tol,angle):
        BRepMesh_IncrementalMesh(self.s,tol,False,angle,True).Perform()
        exp=TopExp_Explorer(self.s,TopAbs_FACE);vertices=[];tris=[]
        while exp.More():
            face=TopoDS.Face_s(exp.Current());loc=TopLoc_Location();tri=BRep_Tool.Triangulation_s(face,loc)
            if tri:
                start=len(vertices)
                for i in range(1,tri.NbNodes()+1):
                    p=tri.Node(i).Transformed(loc.Transformation());vertices.append((p.X(),p.Y(),p.Z()))
                for i in range(1,tri.NbTriangles()+1):
                    abc=tri.Triangle(i).Get()
                    if face.Orientation()==TopAbs_REVERSED:abc=(abc[0],abc[2],abc[1])
                    tris.append(tuple(start+j-1 for j in abc))
            exp.Next()
        return vertices,tris
class Pos:
    def __init__(self,*v):self.v=v[0] if len(v)==1 else v
    def __mul__(self,s):
        t=gp_Trsf();t.SetTranslation(gp_Vec(*self.v));return Shape(BRepBuilderAPI_Transform(s.s,t,True).Shape())
Location=Pos
def Box(x,y,z):return Shape(BRepPrimAPI_MakeBox(gp_Pnt(-x/2,-y/2,-z/2),x,y,z).Shape())
def Cylinder(r,h,rotation=None):
    p=Shape(BRepPrimAPI_MakeCylinder(r,h).Shape()).moved(Pos(0,0,-h/2))
    if rotation:
        for ax,a in zip((Axis.X,Axis.Y,Axis.Z),rotation):
            if a:p=p.rotate(ax,a)
    return p
class Polygon:
    def __init__(self,*p,align=None):self.p=p
class PlaneXZ:
    def __init__(self,y=0):self.y=y
    def offset(self,v):return PlaneXZ(-v)
    def __mul__(self,p):return (p.p,self.y)
class Plane:XZ=PlaneXZ()
def extrude(poly,amount):
    points,y=poly;p=BRepBuilderAPI_MakePolygon()
    for x,z in points:p.Add(gp_Pnt(x,y,z))
    p.Close();f=BRepBuilderAPI_MakeFace(p.Wire()).Face()
    return Shape(BRepPrimAPI_MakePrism(f,gp_Vec(0,-amount,0)).Shape())
def import_step(path):
    r=STEPControl_Reader();r.ReadFile(str(path));r.TransferRoots();return Shape(r.OneShape())
def export_step(p,path):
    w=STEPControl_Writer();w.Transfer(p.s,STEPControl_AsIs);w.Write(str(path))
def export_stl(p,path,tolerance=.025,angular_tolerance=.12):
    BRepMesh_IncrementalMesh(p.s,tolerance,False,angular_tolerance,True).Perform()
    w=StlAPI_Writer();w.ASCIIMode=False;assert w.Write(p.s,str(path))
def Compound(children,label=''):
    c=TopoDS_Compound();b=BRep_Builder();b.MakeCompound(c)
    for p in children:b.Add(c,p.s)
    return Shape(c)
def round_y_edges(p,r,only=None):
    f=BRepFilletAPI_MakeFillet(p.s);exp=TopExp_Explorer(p.s,TopAbs_EDGE)
    while exp.More():
        e=TopoDS.Edge_s(exp.Current());c=BRepAdaptor_Curve(e)
        a=c.Value(c.FirstParameter());b=c.Value(c.LastParameter())
        if abs(a.X()-b.X())<1e-6 and abs(a.Z()-b.Z())<1e-6 and abs(a.Y()-b.Y())>1:
            if only is None or (abs(a.X()-only[0])<1e-6 and abs(a.Z()-only[1])<1e-6):f.Add(r,e)
        exp.Next()
    f.Build();assert f.IsDone();return Shape(f.Shape())
