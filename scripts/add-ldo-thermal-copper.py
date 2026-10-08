"""Add masked VIN/tab heat-spreading copper without changing native pads.

No thermal resistance is claimed; final temperature remains a bench gate.
External standard through vias are kept out of every component solder pad.
"""
import json,math
import verify_supplier_connectivity as g
from shapely.geometry import Point,LineString,Polygon,box
from shapely.ops import unary_union
from shapely.geometry.polygon import orient
j=g.j;key=next(k for k,n in g.nets.items() if n=='LOGIC_IN')
net=next(e for e in j if e['type']=='source_net' and e['name']=='LOGIC_IN')
j[:]=[e for e in j if e.get('pcb_copper_pour_id','').startswith('ldo_heat_')==False and not e.get('pcb_via_id','').startswith('ldo_heat_')]
def shapes(e,l):
 if e['type'] in ['pcb_smtpad','pcb_plated_hole'] and l in e.get('layers',[e.get('layer','top')]):return [g.geometry(e)]
 if e['type']=='pcb_via':return [Point(e['x'],e['y']).buffer(e['outer_diameter']/2)]
 if e['type']=='pcb_trace':return [LineString([(a['x'],a['y']),(b['x'],b['y'])]).buffer(max(a['width'],b['width'])/2) for a,b in zip(e['route'],e['route'][1:]) if a['route_type']==b['route_type']=='wire' and a['layer']==b['layer']==l]
 return []
accepted=[]
for x,y in [(-7.7,-4.7),(-6.7,-4.7)]:
 v=Point(x,y).buffer(.25);safe=True
 for e in j:
  for l in ['top','bottom']:
   for geom in shapes(e,l):
    if (e['type'] in ['pcb_smtpad','pcb_plated_hole'] or g.key(e)!=key) and v.distance(geom)<.155:safe=False
 if not safe:continue
 e={'type':'pcb_via','pcb_via_id':'ldo_heat_'+str(len(accepted)+1),'x':x,'y':y,'hole_diameter':.25,'outer_diameter':.5,'layers':['top','bottom'],'from_layer':'top','to_layer':'bottom','tented_on_top':True,'tented_on_bottom':True,'source_net_id':net['source_net_id'],'subcircuit_connectivity_map_key':key,'subcircuit_id':'subcircuit_source_group_0'}
 j.append(e);accepted.append({'x':x,'y':y})
areas=[]
for l in ['top','bottom']:
 cuts=[];touch=[]
 for e in j:
  for geom in shapes(e,l):
   if g.key(e)==key:touch.append(geom)
   else:cuts.append(geom.buffer(.20,quad_segs=16))
  if e['type']=='pcb_keepout':
   c=e['center'];cuts.append(Point(c['x'],c['y']).buffer(e['radius']+.20) if e.get('shape')=='circle' else box(c['x']-e['width']/2-.20,c['y']-e['height']/2-.20,c['x']+e['width']/2+.20,c['y']+e['height']/2+.20))
  elif e['type']=='pcb_hole':cuts.append(Point(e['x'],e['y']).buffer(e['hole_diameter']/2+.25))
 region=box(-10.05,-5.65,-4.2,-.75).difference(unary_union(cuts))
 polys=[region] if region.geom_type=='Polygon' else list(region.geoms)
 for p in polys:
  if p.geom_type!='Polygon' or p.area<.25 or not any(p.intersects(s) for s in touch):continue
  p=orient(p,sign=1);pts=lambda r:[{'x':x,'y':y} for x,y in list(r.coords)[:-1]]
  e={'type':'pcb_copper_pour','pcb_copper_pour_id':'ldo_heat_'+l+'_'+str(len(areas)), 'layer':l,'source_net_id':net['source_net_id'],'subcircuit_connectivity_map_key':key,'subcircuit_id':'subcircuit_source_group_0','shape':'brep','covered_with_solder_mask':True,'brep_shape':{'outer_ring':{'vertices':pts(p.exterior),'edges':[]},'inner_rings':[{'vertices':pts(r),'edges':[]} for r in p.interiors]}}
  j.append(e);areas.append({'layer':l,'areaMm2':p.area})
g.path.write_text(json.dumps(j,indent=2)+'\n')
(g.ROOT/'artifacts/engineering/ldo-thermal-copper.json').write_text(json.dumps({'net':'LOGIC_IN','minimumForeignClearanceMm':.20,'externalStandardVias':accepted,'regions':areas,'thermalResistanceVerified':False},indent=2)+'\n')
print('Masked LDO tab heat spreader:',areas,'external vias:',accepted)
