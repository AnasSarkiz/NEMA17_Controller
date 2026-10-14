"""Attach each paired trunk end to its intended physical terminals.

Symmetric non-VIP escapes keep independent routing from bypassing the paired
trunk or consuming the adjacent WCH debug-pin escape lanes.
"""
import json
import verify_supplier_connectivity as g
j=g.j;ROOT=g.ROOT;nets={e['name']:e for e in j if e['type']=='source_net'};usb={nets[n]['subcircuit_connectivity_map_key'] for n in ['USB_DP','USB_DM']}
j[:]=[e for e in j if not(e['type'] in ['pcb_trace','pcb_via'] and g.key(e) in usb and not e.get('pcb_trace_id','').startswith('usb_coupled_'))]
plan=json.loads((ROOT/'artifacts/engineering-fixes/usb-routing-plan.json').read_text());core=next(c for c in plan['cores'] if c['name']=='ESD_to_MCU');input_core=next(c for c in plan['cores'] if c['name']=='connector_to_ESD')
def port(ref,role):return next(p for p in g.ports.values() if g.src[g.sp[p['source_port_id']]['source_component_id']]==ref and g.sp[p['source_port_id']]['name']==role)
def attrs(net,p):
 key=nets[net]['subcircuit_connectivity_map_key'];source=next(e['source_trace_id'] for e in j if e['type']=='source_trace' and e.get('subcircuit_connectivity_map_key')==key and p['source_port_id'] in e.get('connected_source_port_ids',[]));return {'source_net_id':nets[net]['source_net_id'],'source_trace_id':source,'subcircuit_connectivity_map_key':key,'subcircuit_id':'subcircuit_source_group_0'}
def trace(uid,net,p,points,layer,tag=False):
 route=[{'route_type':'wire','x':x,'y':y,'width':.16,'layer':layer} for x,y in points]
 if tag:route[0]['start_pcb_port_id']=p['pcb_port_id']
 j.append({'type':'pcb_trace','pcb_trace_id':uid,'route':route,'pcb_port_ids':[p['pcb_port_id']] if tag else [],**attrs(net,p)})
def via(uid,net,p,x,y):j.append({'type':'pcb_via','pcb_via_id':uid,'x':x,'y':y,'outer_diameter':.45,'hole_diameter':.3,'layers':['top','inner1','inner2','bottom'],'from_layer':'top','to_layer':'bottom','tented_on_top':True,'tented_on_bottom':True,**attrs(net,p)})
for net,x in [('USB_DP',2.5),('USB_DM',3.15)]:
 p=port('U_MCU',net);track=next(t for t in core['tracks'] if t['net']==net);end=track['points'][-1]
 trace('usb_fan_MCU_'+net,net,p,[(p['x'],p['y']),(p['x'],4.65),(x,5.1)],'top',True);via('usb_fan_MCU_'+net+'_via',net,p,x,5.1);trace('usb_fan_MCU_'+net+'_bottom',net,p,[(x,5.1),end],'bottom')
for net,role in [('USB_DP','DP1'),('USB_DM','DM1')]:
 p=port('U_ESD',role);track=next(t for t in core['tracks'] if t['net']==net);start=track['points'][0];x,y=p['x'],7.0
 trace('usb_fan_ESD_'+net,net,p,[(p['x'],p['y']),(x,y)],'top',True);via('usb_fan_ESD_'+net+'_via',net,p,x,y);trace('usb_fan_ESD_'+net+'_bottom',net,p,[(x,y),(start[0],6.45),start],'bottom')
for net,inrole,outrole in [('USB_DP','DP2','DP1'),('USB_DM','DM2','DM1')]:
 p=port('U_ESD',inrole);q=port('U_ESD',outrole);track=next(t for t in input_core['tracks'] if t['net']==net)
 trace('usb_fan_ESD_IO_link_'+net,net,q,[(q['x'],q['y']),(p['x'],p['y'])],'top',True);trace('usb_fan_ESD_input_'+net+'_bottom',net,p,[(q['x'],7.0),track['points'][-1]],'bottom')
g.path.write_text(json.dumps(j,indent=2)+'\n');print('Seeded symmetric MCU and ESD fanouts to the intended paired-trunk ends')
