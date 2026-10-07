"""Verify each named net is a single physical copper island, across the copper layers, including anonymous debug/USB-BOOT nets."""
import json,hashlib
import routing_grid as g
errors=[];count=0
for p in g.sp.values():
 k=p.get('subcircuit_connectivity_map_key')
 if k and k not in g.nets: g.nets[k]={'name':p['name']+' (direct connection)'}
for net,source in g.nets.items():
 elems,roots=g.groups(net);islands={}
 for e,r in zip(elems,roots):
  pid=e.get('pcb_port_id')
  if pid:
   p=g.ports[pid];c=g.src[g.comp[p['pcb_component_id']]['source_component_id']]['name'];pn=g.sp[p['source_port_id']]['name'];islands.setdefault(r,[]).append(c+'.'+pn)
 if len(islands)>1:errors.append({'net':source['name'],'islands':list(islands.values())})
 count+=1
report={'checkedNets':count,'disconnectedNets':errors,'sha256':hashlib.sha256(g.path.read_bytes()).hexdigest()}
(g.ROOT/'artifacts/physical-connectivity.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
raise SystemExit(bool(errors))
