"""Finish explicitly selected connections on saved copper.
A collision-aware grid assists the selected manual repairs; unchanged routes are retained.
All results must pass the independent tscircuit DRC and Gerber short checks.
"""
import json,math,pathlib,heapq,time
import numpy as np
from PIL import Image,ImageDraw
ROOT=pathlib.Path(__file__).resolve().parents[1];path=ROOT/'artifacts/board.circuit.json';j=json.loads(path.read_text())
STEP=.05;LOW=-17.5;N=701
src={e['source_component_id']:e for e in j if e['type']=='source_component'}
sp={e['source_port_id']:e for e in j if e['type']=='source_port'}
ports={e['pcb_port_id']:e for e in j if e['type']=='pcb_port'}
comp={e['pcb_component_id']:e for e in j if e['type']=='pcb_component'}
nets={e['subcircuit_connectivity_map_key']:e for e in j if e['type']=='source_net'}
traces={e['subcircuit_connectivity_map_key']:e['source_trace_id'] for e in j if e['type']=='source_trace'}
pads=[e for e in j if e['type'] in ['pcb_smtpad','pcb_plated_hole']]
def xy(x,y):return (round((x-LOW)/STEP),round((y-LOW)/STEP))
def world(p):return (LOW+p[0]*STEP,LOW+p[1]*STEP)
def key(e):
 if e['type'] in ['pcb_smtpad','pcb_plated_hole']:
  p=ports.get(e.get('pcb_port_id'),{});return sp.get(p.get('source_port_id'),{}).get('subcircuit_connectivity_map_key')
 return e.get('subcircuit_connectivity_map_key')
def findport(cname,pname):
 return next(p for p in ports.values() if src[comp[p['pcb_component_id']]['source_component_id']]['name']==cname and sp[p['source_port_id']]['name']==pname)
def drawrect(draw,x,y,w,h,r=0):draw.rectangle([xy(x-w/2-r,y-h/2-r),xy(x+w/2+r,y+h/2+r)],fill=1)
def circle(draw,x,y,r):draw.ellipse([xy(x-r,y-r),xy(x+r,y+r)],fill=1)
def obstacle(net,width,via=False):
 imgs=[Image.new('L',(N,N)) for _ in range(2)];ds=[ImageDraw.Draw(i) for i in imgs]
 margin=.15+(.25 if via else width/2)+.018
 for e in j:
  typ=e['type']
  if typ in ['pcb_smtpad','pcb_plated_hole']:
   if key(e)==net and not via:continue
   w=e.get('width',e.get('outer_width',e.get('outer_diameter',e.get('radius',0)*2)));h=e.get('height',e.get('outer_height',e.get('outer_diameter',e.get('radius',0)*2)))
   if abs(e.get('ccw_rotation',0)%180-90)<.01:w,h=h,w
   ls=[0 if l=='top' else 1 for l in e.get('layers',[e.get('layer','top')])]
   for l in ls:drawrect(ds[l],e['x'],e['y'],w,h,margin)
  elif typ=='pcb_trace' and key(e)!=net:
   rr=e['route']
   for a,b in zip(rr,rr[1:]):
    if a['route_type']!='wire' or b['route_type']!='wire' or a['layer']!=b['layer']:continue
    r=margin+max(a['width'],b['width'])/2;d=ds[0 if a['layer']=='top' else 1]
    d.line([xy(a['x'],a['y']),xy(b['x'],b['y'])],fill=1,width=math.ceil(2*r/STEP))
    circle(d,a['x'],a['y'],r);circle(d,b['x'],b['y'],r)
  elif typ=='pcb_via':
   if key(e)==net and not via:continue
   r=.72 if via else e['outer_diameter']/2+margin
   for d in ds:circle(d,e['x'],e['y'],r)
  elif typ=='pcb_keepout':
   c=e['center']
   for d in ds:drawrect(d,c['x'],c['y'],e.get('width',e.get('radius',0)*2),e.get('height',e.get('radius',0)*2),.15+(.25 if via else width/2)+.018)
  elif typ=='pcb_hole':
   for d in ds:circle(d,e['x'],e['y'],e['hole_diameter']/2+.2+(.25 if via else width/2)+.018)
 border=.3+(.25 if via else width/2)
 for d in ds:
  b=math.ceil(border/STEP);d.rectangle([0,0,N-1,b],fill=1);d.rectangle([0,N-1-b,N-1,N-1],fill=1);d.rectangle([0,0,b,N-1],fill=1);d.rectangle([N-1-b,0,N-1,N-1],fill=1)
 return [np.asarray(im,dtype=np.bool_) for im in imgs]
assert not any(e.get('pcb_trace_id','').startswith('usb_boot_route_') for e in j), 'BOOT routes already present; this script adds branches once'
repairs=[]
original=[e for e in j if e['type'].startswith('pcb_')]
for cname,pname in [('J_BOOT','USB_DP'),('R_USB_BOOT','pin2'),('R_USB_BOOT','pin1')]:
 p=findport(cname,pname);net=sp[p['source_port_id']]['subcircuit_connectivity_map_key']
 width=.16
 goals={}
 for e in j:
  if e['type']=='pcb_trace' and key(e)==net:
   for a in e['route']:
    if a['route_type']=='wire':gx,gy=xy(a['x'],a['y']);goals[(gx,gy,0 if a['layer']=='top' else 1)]=(a['x'],a['y'])
 if not goals:
  for pp in ports.values():
   if pp['pcb_port_id']!=p['pcb_port_id'] and sp[pp['source_port_id']].get('subcircuit_connectivity_map_key')==net:
    gx,gy=xy(pp['x'],pp['y']);goals[(gx,gy,0)]=(pp['x'],pp['y'])
    if any(e.get('pcb_port_id')==pp['pcb_port_id'] and e['type']=='pcb_plated_hole' for e in pads):goals[(gx,gy,1)]=(pp['x'],pp['y'])
 # Remove the source pad itself from candidate targets.
 goals={g:v for g,v in goals.items() if math.hypot(v[0]-p['x'],v[1]-p['y'])>.25}
 if not goals:raise RuntimeError('No target copper for '+cname+'.'+pname)
 blocked=obstacle(net,width);vb=obstacle(net,width,True);start=(*xy(p['x'],p['y']),0)
 pts=np.asarray([[g[0],g[1],g[2]] for g in goals]);lo=pts[:,:2].min(axis=0);hi=pts[:,:2].max(axis=0)
 def heuristic(s):return max(lo[0]-s[0],0,s[0]-hi[0])+max(lo[1]-s[1],0,s[1]-hi[1])
 heap=[(heuristic(start),0,start)];best={start:0};prev={};end=None;expanded=0
 while heap:
  _,cost,s=heapq.heappop(heap)
  if cost!=best.get(s):continue
  if s in goals:end=s;break
  expanded+=1
  if expanded>600000:break
  x,y,l=s
  options=[(x+dx,y+dy,l,1.41421356 if dx and dy else 1) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]]
  if not vb[0][y,x] and not vb[1][y,x]:options.append((x,y,1-l,35))
  for nx,ny,nl,dc in options:
   if not(0<=nx<N and 0<=ny<N) or blocked[nl][ny,nx]:continue
   if nl==l and nx!=x and ny!=y and (blocked[l][y,nx] or blocked[l][ny,x]):continue
   t=(nx,ny,nl);nc=cost+dc
   if nc+1e-8<best.get(t,float('inf')):best[t]=nc;prev[t]=s;heapq.heappush(heap,(nc+heuristic(t),nc,t))
 if end is None:pathlib.Path('/tmp/repair-debug.json').write_text(json.dumps(j));raise RuntimeError(f'No collision-free repair for {cname}.{pname} after {expanded} nodes')
 nodes=[end]
 while nodes[-1]!=start:nodes.append(prev[nodes[-1]])
 nodes.reverse()
 # Retain turns and layer changes; simplify only exact collinear runs.
 slim=[nodes[0]]
 for i in range(1,len(nodes)-1):
  a,b,c=nodes[i-1:i+2]
  if a[2]!=b[2] or b[2]!=c[2] or (b[0]-a[0],b[1]-a[1])!=(c[0]-b[0],c[1]-b[1]):slim.append(b)
 slim.append(nodes[-1]);route=[];newvias=[]
 for i,s in enumerate(slim):
  x,y=world(s);layer='top' if s[2]==0 else 'bottom'
  if i==0:x,y=p['x'],p['y']
  if i==len(slim)-1:x,y=goals[end]
  if route and route[-1]['layer']!=layer:
   old=route[-1]['layer'];route.append({'route_type':'via','x':x,'y':y,'from_layer':old,'to_layer':layer,'via_diameter':.5,'via_hole_diameter':.25})
   newvias.append((x,y))
  route.append({'route_type':'wire','x':x,'y':y,'width':width,'layer':layer})
 if p['pcb_port_id']:route[0]['start_pcb_port_id']=p['pcb_port_id']
 tid=f'usb_boot_route_{cname}_{pname}'
 j.append({'type':'pcb_trace','pcb_trace_id':tid,'route':route,**({'source_net_id':nets[net]['source_net_id']} if nets.get(net,{}).get('source_net_id') else {}),'source_trace_id':traces[net],'subcircuit_connectivity_map_key':net,'subcircuit_id':'subcircuit_source_group_0','pcb_port_ids':[p['pcb_port_id']] if p['pcb_port_id'] else []})
 for i,(x,y) in enumerate(newvias):j.append({'type':'pcb_via','pcb_via_id':tid+'_via'+str(i),'pcb_trace_id':tid,'source_trace_id':traces[net],**({'source_net_id':nets[net]['source_net_id']} if nets.get(net,{}).get('source_net_id') else {}),'subcircuit_connectivity_map_key':net,'subcircuit_id':'subcircuit_source_group_0','x':x,'y':y,'hole_diameter':.25,'outer_diameter':.5,'layers':['top','bottom']})
 repairs.append({'connection':cname+'.'+pname,'net':nets.get(net,{}).get('name','USB_BOOT'),'points':len(route),'vias':len(newvias),'expandedNodes':expanded,'route':route})
 print(repairs[-1]['connection'],nets.get(net,{}).get('name','USB_BOOT'),len(route),'points',len(newvias),'vias',expanded,'searched nodes',flush=True)
assert all(e in j for e in original),'Saved copper was altered'
for e in j:
 if e['type']=='pcb_via':e['tented_on_bottom']=True;e['tented_on_top']=True
path.write_text(json.dumps(j,indent=2)+'\n')
(ROOT/'artifacts/validation/usb-boot-routing.json').write_text(json.dumps(repairs,indent=2)+'\n')
