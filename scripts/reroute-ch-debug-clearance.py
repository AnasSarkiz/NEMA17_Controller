"""Reconstruct the paired USB trunk with room for .30/.45 WCH debug escapes.
Construction only; native, CAM and exact reference-coverage checks remain required.
"""
import json,math
from shapely.geometry import Point,LineString
import verify_supplier_connectivity as g
j=g.j;planpath=g.ROOT/'artifacts/engineering-fixes/usb-routing-plan.json';plan=json.loads(planpath.read_text());core=next(c for c in plan['cores'] if c['name']=='ESD_to_MCU');pts=[(9,5.1),(9,4.7),(7.7,4.7),(5.725,6.675),(3.675,6.675),(2.825,5.825),(2.825,5.8)];line=LineString(pts);nets={n:k for k,n in g.nets.items()};pair={nets['USB_DP'],nets['USB_DM']};tracks=[]
for name,offset in [('USB_DP',-.205),('USB_DM',.205)]:
 curve=line.offset_curve(offset,join_style='mitre');assert curve.geom_type=='LineString' and curve.is_simple
 t=next(e for e in j if e.get('pcb_trace_id')=='usb_coupled_ESD_to_MCU_'+name);t['route']=[dict(route_type='wire',x=x,y=y,width=.25,layer='bottom') for x,y in curve.coords];tracks.append(dict(net=name,trace_id=t['pcb_trace_id'],length_mm=curve.length,points=list(curve.coords)))
core.update(centerline=pts,tracks=tracks,core_length_difference_mm=abs(tracks[0]['length_mm']-tracks[1]['length_mm']))
# Preserve protected escape barrels when the actual copper and reference projection clear.
ripped=[]
for e in list(j):
 if g.key(e) in pair or e['type'] not in ['pcb_trace','pcb_via','pcb_copper_pour']:continue
 hit=e['type']=='pcb_copper_pour'
 if e['type']=='pcb_via':
  shape=Point(e['x'],e['y']).buffer(e['outer_diameter']/2+.205)
  hit=any(shape.distance(LineString(t['points']))<.025 for t in tracks)
 if e['type']=='pcb_trace':
  for a,b in zip(e['route'],e['route'][1:]):
   if a['route_type']==b['route_type']=='wire' and a['layer']==b['layer']:
    shape=LineString([(a['x'],a['y']),(b['x'],b['y'])]).buffer(max(a['width'],b['width'])/2)
    if a['layer']=='bottom' and any(shape.distance(LineString(t['points']).buffer(.125))<.153 for t in tracks) or a['layer']=='inner2' and any(shape.distance(LineString(t['points']))<.25 for t in tracks):hit=True
 if hit:
  if e['type']=='pcb_trace':assert not e['pcb_trace_id'].startswith(('usb_','reviewed_local_')),'New pair crosses a protected escape'
  if e['type']=='pcb_via':assert not e['pcb_via_id'].startswith(('usb_','reviewed_local_')),'New pair crosses a protected barrel'
  j.remove(e);ripped.append(e[e['type']+'_id'])
j[:]=[e for e in j if not(e['type'] in ['pcb_trace','pcb_via'] and e.get(e['type']+'_id','').startswith(('usb_fan_MCU_','reviewed_local_U_MCU_USB_')))]
for name,x in [('USB_DP',2.5),('USB_DM',3.15)]:
 p=next(p for p in g.ports.values() if g.src[g.sp[p['source_port_id']]['source_component_id']]=='U_MCU' and g.sp[p['source_port_id']]['name']==name);k=nets[name];n=next(e for e in j if e['type']=='source_net' and e['name']==name);s=next(e for e in j if e['type']=='source_trace' and e.get('subcircuit_connectivity_map_key')==k and p['source_port_id'] in e.get('connected_source_port_ids',[]));attrs=dict(source_net_id=n['source_net_id'],source_trace_id=s['source_trace_id'],subcircuit_connectivity_map_key=k,subcircuit_id='subcircuit_source_group_0');uid='usb_fan_MCU_'+name
 for layer,points,suffix in [('top',[(p['x'],p['y']),(p['x'],4.65),(x,5.1)],''),('bottom',[(x,5.1),tracks[0 if name=='USB_DP' else 1]['points'][-1]],'_bottom')]:
  route=[dict(route_type='wire',x=a,y=b,width=.16,layer=layer) for a,b in points]
  if layer=='top':route[0]['start_pcb_port_id']=p['pcb_port_id']
  j.append(dict(type='pcb_trace',pcb_trace_id=uid+suffix,route=route,pcb_port_ids=[p['pcb_port_id']] if layer=='top' else [],**attrs))
 j.append(dict(type='pcb_via',pcb_via_id=uid+'_via',x=x,y=5.1,outer_diameter=.45,hole_diameter=.3,layers=['top','inner1','inner2','bottom'],from_layer='top',to_layer='bottom',tented_on_top=True,tented_on_bottom=True,**attrs))
g.path.write_text(json.dumps(j,indent=2)+'\n');plan['constructed_not_yet_qualified']=True;planpath.write_text(json.dumps(plan,indent=2)+'\n');print('Paired trunk rebuilt, skew',core['core_length_difference_mm'],'ripped',ripped)
