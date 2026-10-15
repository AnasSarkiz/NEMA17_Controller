"""Construct symmetric local USB/debug escapes before paired routing.

The four adjacent controller contacts fan out in pin order to non-overlapping,
ordinary through vias. No component pad contains a signal drill.
"""
import json,pathlib,sys
import verify_supplier_connectivity as g
j=g.j;ROOT=g.ROOT;names={e['name']:e for e in j if e['type']=='source_net'}
def port(ref,role):return next(p for p in g.ports.values() if g.src[g.sp[p['source_port_id']]['source_component_id']]==ref and g.sp[p['source_port_id']]['name']==role)
def source(net,p):return next(e['source_trace_id'] for e in j if e['type']=='source_trace' and e.get('subcircuit_connectivity_map_key')==names[net]['subcircuit_connectivity_map_key'] and p['source_port_id'] in e.get('connected_source_port_ids',[]))
def add(net,ref,role,points,via):
 p=port(ref,role);src=source(net,p);key=names[net]['subcircuit_connectivity_map_key'];uid='usb_escape_'+ref+'_'+role;route=[{'route_type':'wire','x':x,'y':y,'width':.16,'layer':'top'} for x,y in points];route[0]['start_pcb_port_id']=p['pcb_port_id'];j.append({'type':'pcb_trace','pcb_trace_id':uid,'route':route,'pcb_port_ids':[p['pcb_port_id']],'source_trace_id':src,'source_net_id':names[net]['source_net_id'],'subcircuit_connectivity_map_key':key,'subcircuit_id':'subcircuit_source_group_0'});j.append({'type':'pcb_via','pcb_via_id':uid+'_via','x':via[0],'y':via[1],'outer_diameter':.45,'hole_diameter':.3,'layers':['top','inner1','inner2','bottom'],'from_layer':'top','to_layer':'bottom','source_trace_id':src,'source_net_id':names[net]['source_net_id'],'subcircuit_connectivity_map_key':key,'subcircuit_id':'subcircuit_source_group_0','tented_on_top':True,'tented_on_bottom':True})
# Preserve the GPIO order while widening its 0.4 mm pitch into a legal via bank.
for net,x,y in [('DIO',3.7,5.3),('DCK',4.3,4.975)]:
 key=names[net]['subcircuit_connectivity_map_key'];j[:]=[e for e in j if not(e['type'] in ['pcb_trace','pcb_via'] and g.key(e)==key)]
 p=next(p for p in g.ports.values() if g.src[g.sp[p['source_port_id']]['source_component_id']]=='U_MCU' and g.sp[p['source_port_id']].get('subcircuit_connectivity_map_key')==key);role=g.sp[p['source_port_id']]['name'];add(net,'U_MCU',role,[(p['x'],p['y']),(p['x'],4.65),(x,y)],(x,y))

g.path.write_text(json.dumps(j,indent=2)+'\n');print('Constructed ordered DIO/DCK escapes')
