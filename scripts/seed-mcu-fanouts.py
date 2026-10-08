"""Reserve inspectable standard-via escapes for every crowded active MCU GPIO.
No supplier pad geometry is modified. Exact native copper is independently checked.
"""
import json,pathlib,math
import verify_supplier_connectivity as g
ROOT=g.ROOT;j=json.loads((ROOT/'artifacts/final-source.circuit.json').read_text());g.j=j
g.sp={e['source_port_id']:e for e in j if e['type']=='source_port'};g.ports={e['pcb_port_id']:e for e in j if e['type']=='pcb_port'};g.comp={e['pcb_component_id']:e for e in j if e['type']=='pcb_component'};g.src={e['source_component_id']:e['name'] for e in j if e['type']=='source_component'}
nets={e['subcircuit_connectivity_map_key']:e for e in j if e['type']=='source_net'};traces={e['subcircuit_connectivity_map_key']:e['source_trace_id'] for e in j if e['type']=='source_trace'}
def port(pin,ref='U_MCU'):return next(p for p in g.ports.values() if g.src[g.comp[p['pcb_component_id']]['source_component_id']]==ref and g.sp[p['source_port_id']]['name']==pin)
plans={
 'STEP':[(2.4,1.09995),(2.2,1.3),(1.5,1.3)],
 'DIR':[(2.05,.6999)],
 'PD_PG':[(2.4,.300104),(2.2,.1),(1.5,.1)],
 'DATA_PRESENT':[(3.799404,-1.05),(3.3,-1.4)],
 'VM_SENSE':[(4.1992,-1.0),(4.3,-1.4)],
 'DRV_ENABLE_N':[(6.199196,-1.45)],
 'DRV_SLEEP':[(7.95,.300104)],
 'VM_ENABLE_N':[(8.1,1.5)],
 'USB_DP':[(4.1992,4.1),(3.5,4.55)],
 'USB_DM':[(4.599504,4.55)],
 'SWDIO':[(4.9993,4.1),(5.5,4.75)],
 'SWCLK':[(5.399096,4.1),(6.8,4.4)],
 'DRV_DIR':[(3.95,-7.499593)]}
# Pin names are native supplier logical mappings, not assumed package positions.
aliases={'DRV_DIR':['DIR'],'PD_PG':['PD_GOOD','PD_PG','PG'],'DRV_ENABLE_N':['DRV_ENABLE_N','ENABLE_N'],'DRV_SLEEP':['DRV_SLEEP','SLEEP'],'SWDIO':['SWDIO','DIO'],'SWCLK':['SWCLK','DCK']}
seeds=[];report=[]
for proposed,turns in plans.items():
 p=None
 for name in aliases.get(proposed,[proposed]):
  try:p=port(name,'U_DRV' if proposed=='DRV_DIR' else 'U_MCU');break
  except StopIteration:pass
 assert p is not None,proposed
 key=g.sp[p['source_port_id']]['subcircuit_connectivity_map_key'];points=[(p['x'],p['y']),*turns];via=points[-1];width=.16;line=g.LineString(points).buffer(width/2);ann=g.Point(*via).buffer(.25)
 minimum=99
 for e in j:
  typ=e['type']
  if typ in ['pcb_smtpad','pcb_plated_hole']:
   shape=g.geometry(e)
   assert ann.distance(shape)>=.15-1e-6,(proposed,'via-to-pad',g.key(e),ann.distance(shape))
   if g.key(e)!=key:
    dist=line.distance(shape);minimum=min(minimum,dist);assert dist>=.15-1e-6,(proposed,'trace-to-pad',g.key(e),dist,g.src[g.comp[g.ports[e['pcb_port_id']]['pcb_component_id']]['source_component_id']],g.sp[g.ports[e['pcb_port_id']]['source_port_id']]['name'])
  elif typ=='pcb_via' and g.key(e)!=key:
   shape=g.Point(e['x'],e['y']).buffer(e['outer_diameter']/2)
   assert ann.distance(shape)>=.15-1e-6,(proposed,'via-to-via',ann.distance(shape))
   assert line.distance(shape)>=.15-1e-6,(proposed,'trace-to-via',line.distance(shape))
  elif typ=='pcb_trace' and g.key(e)!=key:
   for a,b in zip(e['route'],e['route'][1:]):
    if a['route_type']==b['route_type']=='wire' and a['layer']==b['layer']=='top':
     shape=g.LineString([(a['x'],a['y']),(b['x'],b['y'])]).buffer(max(a['width'],b['width'])/2)
     assert ann.distance(shape)>=.15-1e-6,(proposed,'via-to-trace',ann.distance(shape))
     assert line.distance(shape)>=.15-1e-6,(proposed,'trace-to-trace',line.distance(shape))
 common={'source_trace_id':traces[key],'subcircuit_connectivity_map_key':key,'subcircuit_id':'subcircuit_source_group_0'}
 if key in nets:common['source_net_id']=nets[key]['source_net_id']
 tid='supplier_repair_U_MCU_fanout_'+proposed
 route=[{'route_type':'wire','x':x,'y':y,'width':width,'layer':'top'} for x,y in points];route[0]['start_pcb_port_id']=p['pcb_port_id']
 t={'type':'pcb_trace','pcb_trace_id':tid,'route':route,'pcb_port_ids':[p['pcb_port_id']],**common}
 v={'type':'pcb_via','pcb_via_id':tid+'_via0','x':via[0],'y':via[1],'outer_diameter':.5,'hole_diameter':.25,'layers':['top','bottom'],'tented_on_top':True,'tented_on_bottom':True,**common}
 j.extend([t,v]);seeds.extend([t,v]);report.append({'pin':proposed,'via':via,'minimumPadClearanceMm':minimum,'lengthMm':sum(math.dist(a,b) for a,b in zip(points,points[1:]))})
(ROOT/'artifacts/supplier-seeds.circuit.json').write_text(json.dumps(seeds,indent=2)+'\n');(ROOT/'artifacts/engineering-mcu-fanouts.json').write_text(json.dumps(report,indent=2)+'\n');print('Reserved',len(report)-1,'MCU and one driver native-pad standard-via fanouts')
