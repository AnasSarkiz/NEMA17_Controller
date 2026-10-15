"""Keep each physical TOP path from a driver land to its nearest plated via."""
import json,sys,math,heapq
from shapely.geometry import LineString,Point
from shapely.strtree import STRtree
import verify_supplier_connectivity as g
phases={'A_PLUS','A_MINUS','B_PLUS','B_MINUS'};keep=[];receipt=[]
for p in g.ports.values():
 sp=g.sp[p['source_port_id']];name=g.nets.get(sp.get('subcircuit_connectivity_map_key'))
 if g.src[sp['source_component_id']]!='U_DRV' or name not in phases:continue
 key=sp['subcircuit_connectivity_map_key'];pad=next(e for e in g.j if e['type']=='pcb_smtpad' and e.get('pcb_port_id')==p['pcb_port_id']);records=[pad];shapes=[g.geometry(pad)];costs=[0]
 for e in g.j:
  if g.key(e)!=key:continue
  if e['type']=='pcb_via':records.append(e);shapes.append(Point(e['x'],e['y']).buffer(e['outer_diameter']/2));costs.append(0)
  elif e['type']=='pcb_trace':
   for a,b in zip(e['route'],e['route'][1:]):
    if a['route_type']==b['route_type']=='wire' and a['layer']==b['layer']=='top':
     line=LineString([(a['x'],a['y']),(b['x'],b['y'])]);records.append({**e,'route':[a,b]});shapes.append(line.buffer(max(a['width'],b['width'])/2));costs.append(line.length)
 tree=STRtree(shapes);best={0:0};prev={};heap=[(0,0)];end=None
 while heap:
  cost,i=heapq.heappop(heap)
  if cost!=best[i]:continue
  if records[i]['type']=='pcb_via':end=i;break
  for q in tree.query(shapes[i],predicate='intersects'):
   q=int(q);nc=cost+costs[q]
   if nc<best.get(q,float('inf')):best[q]=nc;prev[q]=i;heapq.heappush(heap,(nc,q))
 assert end is not None,('No physical TOP escape to a via',name)
 assert best[end]<=3,(name,'Native driver escape needs separate review',best[end])
 path=[end]
 while path[-1]!=0:path.append(prev[path[-1]])
 path.reverse();base='reviewed_local_U_DRV_'+sp['name'];old=[];count=0
 for index in path[1:]:
  e=dict(records[index]);old.append(e[e['type']+'_id'])
  if e['type']=='pcb_via':e['pcb_via_id']=base+'_via'
  else:
   e['pcb_trace_id']=base+('' if count==0 else '_segment_'+str(count));count+=1
   e['route']=[{k:v for k,v in q.items() if k not in ['start_pcb_port_id','end_pcb_port_id']} for q in e['route']];e['pcb_port_ids']=[]
   for q,tag in [(e['route'][0],'start_pcb_port_id'),(e['route'][-1],'end_pcb_port_id')]:
    for land in g.j:
     if land['type']=='pcb_smtpad' and land.get('layer')=='top' and g.key(land)==key and land.get('pcb_port_id') and g.geometry(land).covers(Point(q['x'],q['y'])):
      q[tag]=land['pcb_port_id'];e['pcb_port_ids'].append(land['pcb_port_id']);break
  keep.append(e)
 receipt.append({'net':name,'source_port':p['pcb_port_id'],'original_records':old,'retained_top_length_mm':best[end],'retained_barrel_xy_mm':[records[end]['x'],records[end]['y']]})
assert len(receipt)==4
removed=[e for e in g.j if e['type'] in ['pcb_trace','pcb_via'] and g.nets.get(g.key(e)) in phases]
print(json.dumps(receipt,indent=2));print('Replacing',len(removed),'phase records with',len(keep),'native driver escape records')
if '--apply' in sys.argv:
 g.j[:]=[e for e in g.j if e not in removed and e['type']!='pcb_copper_pour']+keep
 g.path.write_text(json.dumps(g.j,indent=2)+'\n');(g.ROOT/'artifacts/opposite-edge/phase-trunk-reset.json').write_text(json.dumps({'retained_driver_escapes':receipt,'removed_copper_records':removed,'qualification_required':True},indent=2)+'\n')
