"""Z-buffered CAD views. Uses numpy already installed with build123d; no GUI."""
from math import sin, cos
from base64 import b64encode
import struct
import zlib
import numpy as np


def png(rgb):
    def chunk(kind,data):
        return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data))
    h,w,_=rgb.shape
    rows=b''.join(b'\0'+row.tobytes() for row in rgb)
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>2I5B',w,h,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(rows))+chunk(b'IEND',b'')


def draw(parts,path):
    meshes=[]
    for name,p,color in parts:
        v,t=p.tessellate(.5,.15)
        meshes.append((np.array([tuple(q) for q in v]),t,np.array([int(color[i:i+2],16) for i in (1,3,5)])))
    out=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="0 0 1600 1000">',
         '<rect width="1600" height="1000" fill="#f4f6f4"/>',
         '<g font-family="Arial,sans-serif" fill="#203343">',
         '<text x="55" y="58" font-size="32" font-weight="bold">Fantom-08 · lift-off plywood music rest</text>',
         '<text x="55" y="93" font-size="19">Actual exported CAD · 460 × 320 mm board · 65° reading angle · lift-off rail mounts</text>']
    for yaw,pitch,left,w,title in [(-.65,-.40,45,810,'Front / assembled'),(2.5,-.45,890,665,'Rear / joints and supports')]:
        projected=[]
        h=715
        for vertices,tris,color in meshes:
            x,y,z=(vertices-np.array([50,141.3,280])).T
            u=cos(yaw)*x-sin(yaw)*y
            d=sin(yaw)*x+cos(yaw)*y
            projected.append((np.column_stack([u,-cos(pitch)*z+sin(pitch)*d,cos(pitch)*d+sin(pitch)*z]),tris,color))
        allv=np.concatenate([v for v,_,_ in projected])
        lo,hi=allv[:,:2].min(axis=0),allv[:,:2].max(axis=0)
        scale=min((w-4)/(hi[0]-lo[0]),(h-4)/(hi[1]-lo[1]))
        offset=(np.array([w,h])-(hi-lo)*scale)/2
        rgb=np.full((h,w,3),[244,246,244],dtype=np.uint8)
        depth=np.full((h,w),np.inf)
        for vs,tris,color in projected:
            vs=vs.copy(); vs[:,:2]=(vs[:,:2]-lo)*scale+offset
            for tri in tris:
                p=vs[list(tri)]
                n=np.cross(p[1]-p[0],p[2]-p[0])
                if abs(n[2])<1e-8: continue
                xmin,ymin=np.maximum(np.floor(p[:,:2].min(axis=0)).astype(int),0)
                xmax,ymax=np.minimum(np.ceil(p[:,:2].max(axis=0)).astype(int),[w-1,h-1])
                yy,xx=np.mgrid[ymin:ymax+1,xmin:xmax+1]; xx=xx+.5; yy=yy+.5
                den=(p[1,1]-p[2,1])*(p[0,0]-p[2,0])+(p[2,0]-p[1,0])*(p[0,1]-p[2,1])
                a=((p[1,1]-p[2,1])*(xx-p[2,0])+(p[2,0]-p[1,0])*(yy-p[2,1]))/den
                b=((p[2,1]-p[0,1])*(xx-p[2,0])+(p[0,0]-p[2,0])*(yy-p[2,1]))/den
                c=1-a-b
                zz=a*p[0,2]+b*p[1,2]+c*p[2,2]
                tile=depth[ymin:ymax+1,xmin:xmax+1]
                mask=(a>=-1e-7)&(b>=-1e-7)&(c>=-1e-7)&(zz<tile)
                tile[mask]=zz[mask]
                # Undo display scale when calculating surface lighting.
                n[:2]*=scale
                shade=.65+.35*abs(np.dot(n,[.25,-.5,.83])/np.linalg.norm(n))
                rgb[ymin:ymax+1,xmin:xmax+1][mask]=(color*shade).astype(np.uint8)
        out.append(f'<text x="{left}" y="140" font-size="20" font-weight="bold">{title}</text>')
        out.append(f'<image x="{left}" y="170" width="{w}" height="{h}" href="data:image/png;base64,{b64encode(png(rgb)).decode()}"/>')
    out.extend(['<text x="55" y="936" font-size="19">Wood: backboard and ledge · teal: two one-piece mounts · gray: existing stand</text>',
                '<text x="55" y="970" font-size="16">Mirrored mounts, flat faces outward. Original channel fit retained. Verify assembled stability and book load. Board fasteners omitted.</text>',
                '</g></svg>'])
    path.write_text(''.join(out))
