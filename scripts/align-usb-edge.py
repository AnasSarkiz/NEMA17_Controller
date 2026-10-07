"""Move the two connector mouths flush with the 35 mm board edges.
Translate connector geometry 0.95 mm outward and elastically extend existing copper.
All copper checks must be rerun; this script is applied once to the prior layout.
"""
import json,pathlib,math
p=pathlib.Path('artifacts/board.circuit.json');j=json.loads(p.read_text())
source={e['source_component_id']:e for e in j if e['type']=='source_component'}
connectors={e['pcb_component_id']:source[e['source_component_id']]['name'] for e in j if e['type']=='pcb_component' and source[e['source_component_id']]['name'] in ['J_PD','J_DATA']}
assert all(abs(abs(e['center']['x'])-11.44)<.001 for e in j if e['type']=='pcb_component' and e['pcb_component_id'] in connectors),'Apply this move only to the original connector placement.'
def warp(x,y):
 f=max(0,min(1,(abs(x)-7.3)/.8));g=min(max(0,min(1,(y+2)/1.9)),max(0,min(1,(10-y)/.6)))
 return x+math.copysign(.95*f*g,x),y
for e in j:
 if e.get('pcb_component_id') in connectors:
  dx=-.95 if connectors[e['pcb_component_id']]=='J_PD' else .95
  if 'x' in e:e['x']+=dx
  for k in ['center','anchor_position','position']:
   if k in e:e[k]['x']+=dx
  if 'display_offset_x' in e:e['display_offset_x']+=dx
  for q in e.get('route',[]):
   if 'x' in q:q['x']+=dx
 if e['type']=='pcb_trace':
  route=e['route'];dense=[]
  for a,b in zip(route,route[1:]):
   dense.append(a)
   if a['route_type']=='wire' and b['route_type']=='wire' and a['layer']==b['layer']:
    n=math.ceil(math.hypot(b['x']-a['x'],b['y']-a['y'])/.2)
    for i in range(1,n):dense.append({'route_type':'wire','x':a['x']+(b['x']-a['x'])*i/n,'y':a['y']+(b['y']-a['y'])*i/n,'width':a['width'],'layer':a['layer']})
  dense.append(route[-1]);e['route']=dense
  for q in e['route']:q['x'],q['y']=warp(q['x'],q['y'])
 if e['type']=='pcb_via':e['x'],e['y']=warp(e['x'],e['y'])
# Separate the compressed pair of bottom traces near the upper right screw keepout.
for e in j:
 if e['type']=='pcb_trace' and e['pcb_trace_id']=='manual_repair_PATCH_V3V3':
  for q in e['route']:
   if q.get('layer')=='bottom' and q['x']>15:q['x']+=.5*max(0,1-abs(q['y']-9.6))
# Keep the data-presence neck in its original position beside the screw-head exclusion.
for e in j:
 if e['type']=='pcb_trace' and e['pcb_trace_id']=='manual_repair_U_MCU_DATA_PRESENT':
  for q in e['route']:
   if q.get('layer')=='bottom' and q['y']>=9.6 and q['x']<10.5:q['x']-=.95*max(0,min(1,(10-q['y'])/.6))
p.write_text(json.dumps(j,indent=2)+'\n')
print('Both USB-C mouths moved outward 0.95 mm. Run source sync, DRC and Gerber checks.')
