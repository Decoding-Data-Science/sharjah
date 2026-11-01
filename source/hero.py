import math
from PIL import Image, ImageDraw
W, H, S = 1333, 750, 2          # slide size in 100px units, supersample 2
img = Image.new("RGB", (W*S, H*S), "#05070B")
d = ImageDraw.Draw(img, "RGBA")
ICE = (159, 214, 255); AMB = (255, 180, 84)
# perspective floor
hz = int(H*0.64*S)
for i in range(-22, 23):
    x = W*S/2 + i*70*S
    a = int(30 + 60*(1-abs(i)/22))
    d.line([(W*S/2 + i*6*S, hz), (W*S/2 + (x-W*S/2)*2.6, H*S)], fill=ICE+(a,), width=2)
for j in range(1, 16):
    k = j/16; y = hz + (H*S-hz)*k**2.2
    d.line([(0, y), (W*S, y)], fill=ICE+(int(18+90*k),), width=2)
for k in range(8):
    k1, k2 = k/8, (k+.45)/8
    d.line([(W*S/2, hz+(H*S-hz)*k1**2.2), (W*S/2, hz+(H*S-hz)*k2**2.2)], fill=AMB+(150,), width=4)
# glow at the horizon
for r in range(40):
    d.line([(0, hz-r*2), (W*S, hz-r*2)], fill=ICE+(int(2.2*(40-r)/2),), width=2)
# icosahedron + rings
p = (1+5**.5)/2
V = [(-1,p,0),(1,p,0),(-1,-p,0),(1,-p,0),(0,-1,p),(0,1,p),(0,-1,-p),(0,1,-p),(p,0,-1),(p,0,1),(-p,0,-1),(-p,0,1)]
F = [(0,11,5),(0,5,1),(0,1,7),(0,7,10),(0,10,11),(1,5,9),(5,11,4),(11,10,2),(10,7,6),(7,1,8),(3,9,4),(3,4,2),(3,2,6),(3,6,8),(3,8,9),(4,9,5),(2,4,11),(6,2,10),(8,6,7),(9,8,1)]
E = set()
for f in F:
    for i in range(3):
        a, b = f[i], f[(i+1)%3]; E.add((min(a,b), max(a,b)))
def rot(v, ax, ay, az):
    x,y,z = v; c1,s1,c2,s2,c3,s3 = math.cos(ax),math.sin(ax),math.cos(ay),math.sin(ay),math.cos(az),math.sin(az)
    y1,z1 = y*c1-z*s1, y*s1+z*c1; x2,z2 = x*c2+z1*s2, -x*s2+z1*c2; x3,y3 = x2*c3-y1*s3, x2*s3+y1*c3
    return (x3,y3,z2)
def proj(v, cx, cy, s):
    k = 1/(1+v[2]*.1); return (cx+v[0]*s*k, cy+v[1]*s*k, v[2])
cx, cy, sc = 960*S, 320*S, 150*S
ax, ay = 0.55, 0.8
P = [proj(rot(v, ax, ay, 0), cx, cy, sc) for v in V]
for a, b in sorted(E):
    dep = (P[a][2]+P[b][2])/2
    d.line([(P[a][0],P[a][1]),(P[b][0],P[b][1])], fill=ICE+(int(110+110*(dep+2)/4),), width=3)
for i,q in enumerate(P):
    if i%3==0: d.ellipse([q[0]-6,q[1]-6,q[0]+6,q[1]+6], fill=ICE+(230,))
for r,(ra,rb,rc) in enumerate([(0.8,0.5,0.0),(-0.5,1.2,0.6)]):
    pts=[proj(rot((math.cos(t/64*6.283)*1.9, math.sin(t/64*6.283)*1.9, 0), ax*ra+r*1.2, ay*rb+r*.9, rc), cx, cy, sc) for t in range(65)]
    d.line([(q[0],q[1]) for q in pts], fill=(ICE if r==0 else AMB)+(110,), width=2)
    q = pts[14+r*20]; d.ellipse([q[0]-9,q[1]-9,q[0]+9,q[1]+9], fill=AMB+(255,))
img.resize((W*2, H*2), Image.LANCZOS).save("hero.png")
print("hero ok", img.size)
