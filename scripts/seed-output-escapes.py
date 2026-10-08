"""Reserve standard-via motor output escapes before routing local support nets."""
import json,math,heapq,pathlib,numpy as np
from PIL import Image,ImageDraw
import verify_supplier_connectivity as g
ROOT=g.ROOT;j=json.loads((ROOT/'artifacts/final-source.circuit.json').read_text());g.j=j
g.sp={e['source_port_id']:e for e in j if e['type']=='source_port'}
g.ports={e['pcb_port_id']:e for e in j if e['type']=='pcb_port'}
g.comp={e['pcb_component_id']:e for e in j if e['type']=='pcb_component'}
g.src={e['source_component_id']:e['name'] for e in j if e['type']=='source_component'}
nets={e['subcircuit_connectivity_map_key']:e for e in j if e['type']=='source_net'}
traces={e['subcircuit_connectivity_map_key']:e['source_trace_id'] for e in j if e['type']=='source_trace'}
def port(ref,pin):return next(p for p in g.ports.values() if g.src[g.comp[p['pcb_component_id']]['source_component_id']]==ref and g.sp[p['source_port_id']]['name']==pin)
STEP=.025;LOW=-17.5;N=1401
xy=lambda x,y:(round((x-LOW)/STEP),round((y-LOW)/STEP))
world=lambda p:(LOW+p[0]*STEP,LOW+p[1]*STEP)
seeds=json.loads((ROOT/'artifacts/supplier-seeds.circuit.json').read_text());j.extend(seeds);report=[]
# Reserve the three grounded exposed-pad vias used by the native DSN exporter.
for v in json.loads((ROOT/'artifacts/supplier-map.json').read_text())['thermalVias']:
 j.append({'type':'pcb_via','x':v['x'],'y':v['y'],'outer_diameter':.5,'layers':['top','bottom'],'subcircuit_connectivity_map_key':next(k for k,v in nets.items() if v['name']=='GND')})
for pin,motor,via,turn in [('OUT1A','A_PLUS',(.4,-4.55),(.500353,-4.8)),('OUT2A','B_PLUS',(-.4,-4.55),(-.500407,-4.8)),('OUT1B','A_MINUS',(3.65,-6.5),None),('OUT2B','B_MINUS',(-3.5,-6.5),None)]:
 p,q=(port('U_MCU','DIR'),port('U_DRV','DIR')) if pin=='MCU_DIR' else (port('U_DRV',pin),port('J_MOTOR',motor));key=g.sp[p['source_port_id']]['subcircuit_connectivity_map_key'];width=.16 if pin=='MCU_DIR' else .30
 target_via=(3.9,-7.5) if pin=='MCU_DIR' else None
 top=[(p['x'],p['y'])]
 if pin=='MCU_DIR':top.extend([(2.4,.6999),(2.1,1.0)])
 elif turn:top.append(turn)
 top.append(via)
 line=g.LineString(top).buffer(width/2)
 for e in j:
  if e['type'] in ['pcb_smtpad','pcb_plated_hole'] and g.key(e)!=key:
   assert line.distance(g.geometry(e))>=.15-1e-6,(pin,g.key(e),line.distance(g.geometry(e)))
   assert g.Point(*via).buffer(.25).distance(g.geometry(e))>=.15-1e-6,(pin,'via',g.key(e))
 im=Image.new('L',(N,N));d=ImageDraw.Draw(im)
 def add(shape):
  shape=shape.buffer(.15+width/2+.008)
  for poly in ([shape] if shape.geom_type=='Polygon' else shape.geoms):d.polygon([xy(x,y) for x,y in poly.exterior.coords],fill=1)
 for e in j:
  if e['type']=='pcb_plated_hole' and g.key(e)!=key:add(g.geometry(e))
  elif e['type']=='pcb_via' and g.key(e)!=key:add(g.Point(e['x'],e['y']).buffer(e['outer_diameter']/2))
  elif e['type']=='pcb_trace' and g.key(e)!=key:
   for a,b in zip(e['route'],e['route'][1:]):
    if a['route_type']==b['route_type']=='wire' and a['layer']==b['layer']=='bottom':add(g.LineString([(a['x'],a['y']),(b['x'],b['y'])]).buffer(max(a['width'],b['width'])/2))
  elif e['type']=='pcb_hole':add(g.Point(e['x'],e['y']).buffer(e['hole_diameter']/2+.1))
  elif e['type']=='pcb_keepout':
   c=e['center'];add((g.Point(c['x'],c['y']).buffer(e['radius']) if e.get('shape')=='circle' else g.box(c['x']-e['width']/2,c['y']-e['height']/2,c['x']+e['width']/2,c['y']+e['height']/2)))
 border=math.ceil(.45/STEP)
 d.rectangle([0,0,N-1,border],fill=1);d.rectangle([0,N-1-border,N-1,N-1],fill=1);d.rectangle([0,0,border,N-1],fill=1);d.rectangle([N-1-border,0,N-1,N-1],fill=1)
 mask=np.asarray(im,dtype=np.bool_)
 if target_via:
  found=None
  for vx in np.arange(3.4,4.9,.025):
   candidate=(float(vx),q['y']);vgeom=g.Point(*candidate).buffer(.25);tgeom=g.LineString([candidate,(q['x'],q['y'])]).buffer(width/2);legal=True
   for item in j:
    if item['type'] in ['pcb_smtpad','pcb_plated_hole']:
     shape=g.geometry(item)
     if vgeom.distance(shape)<.158 or (g.key(item)!=key and tgeom.distance(shape)<.158):legal=False
    elif item['type']=='pcb_via' and g.key(item)!=key:
     if vgeom.distance(g.Point(item['x'],item['y']).buffer(item['outer_diameter']/2))<.158:legal=False
    elif item['type']=='pcb_trace' and g.key(item)!=key:
     for aa,bb in zip(item['route'],item['route'][1:]):
      if aa['route_type']==bb['route_type']=='wire' and aa['layer']==bb['layer'] and vgeom.distance(g.LineString([(aa['x'],aa['y']),(bb['x'],bb['y'])]).buffer(max(aa['width'],bb['width'])/2))<.158:legal=False
   if legal and not mask[xy(*candidate)[1],xy(*candidate)[0]]:found=candidate;break
  assert found,'No legal external DIR driver via';target_via=found
 start=xy(*via);goal=xy(*target_via) if target_via else xy(q['x'],q['y']);heap=[(math.dist(start,goal),0,start)];best={start:0};prev={};end=None
 while heap:
  _,cost,s=heapq.heappop(heap)
  if cost!=best.get(s):continue
  if s==goal:end=s;break
  x,y=s
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
   nx,ny=x+dx,y+dy
   if not(0<=nx<N and 0<=ny<N) or mask[ny,nx]:continue
   if dx and dy and (mask[y,nx] or mask[ny,x]):continue
   t=(nx,ny);nc=cost+(math.sqrt(2) if dx and dy else 1)
   if nc<best.get(t,float('inf'))-1e-8:best[t]=nc;prev[t]=s;heapq.heappush(heap,(nc+math.dist(t,goal),nc,t))
 assert end is not None,pin
 ns=[end]
 while ns[-1]!=start:ns.append(prev[ns[-1]])
 ns.reverse();slim=[ns[0]]
 for i in range(1,len(ns)-1):
  a,b,c=ns[i-1:i+2]
  if (b[0]-a[0],b[1]-a[1])!=(c[0]-b[0],c[1]-b[1]):slim.append(b)
 slim.append(ns[-1]);bottom=[world(n) for n in slim];bottom[0]=via;bottom[-1]=target_via if target_via else (q['x'],q['y'])
 route=[{'route_type':'wire','x':x,'y':y,'width':width,'layer':'top'} for x,y in top]+[{'route_type':'via','x':via[0],'y':via[1],'from_layer':'top','to_layer':'bottom','via_diameter':.5,'via_hole_diameter':.25}]+[{'route_type':'wire','x':x,'y':y,'width':width,'layer':'bottom'} for x,y in bottom]
 if target_via:route += [{'route_type':'via','x':target_via[0],'y':target_via[1],'from_layer':'bottom','to_layer':'top','via_diameter':.5,'via_hole_diameter':.25},{'route_type':'wire','x':target_via[0],'y':target_via[1],'width':width,'layer':'top'},{'route_type':'wire','x':q['x'],'y':q['y'],'width':width,'layer':'top'}]
 route[0]['start_pcb_port_id']=p['pcb_port_id'];route[-1]['end_pcb_port_id']=q['pcb_port_id']
 common={'source_net_id':nets[key]['source_net_id'],'source_trace_id':traces[key],'subcircuit_connectivity_map_key':key,'subcircuit_id':'subcircuit_source_group_0'}
 e={'type':'pcb_trace','pcb_trace_id':'supplier_repair_U_DRV_'+pin,'route':route,'pcb_port_ids':[p['pcb_port_id'],q['pcb_port_id']],**common}
 v={'type':'pcb_via','pcb_via_id':e['pcb_trace_id']+'_via0','x':via[0],'y':via[1],'hole_diameter':.25,'outer_diameter':.5,'layers':['top','bottom'],'tented_on_top':True,'tented_on_bottom':True,**common}
 j.extend([e,v]);seeds.extend([e,v])
 if target_via:
  vv={**v,'pcb_via_id':e['pcb_trace_id']+'_via1','x':target_via[0],'y':target_via[1]};j.append(vv);seeds.append(vv)
 report.append({'net':motor,'escapeVia':via,'traceWidthMm':width,'viaOuterMm':.5,'viaDrillMm':.25,'lengthMm':sum(math.dist(a,b) for a,b in zip(top,top[1:]))+sum(math.dist(a,b) for a,b in zip(bottom,bottom[1:]))})
(ROOT/'artifacts/supplier-seeds.circuit.json').write_text(json.dumps(seeds,indent=2)+'\n')
(ROOT/'artifacts/engineering-motor-escapes.json').write_text(json.dumps(report,indent=2)+'\n')
print('Reserved four native-pad motor outputs with standard 0.5/0.25mm vias')
