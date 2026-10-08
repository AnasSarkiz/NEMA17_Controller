"""Replay recorded supplier routing corrections against the exact SES import."""
import json,pathlib
root=pathlib.Path(__file__).resolve().parents[1];path=root/'artifacts/board.circuit.json'
j=json.loads((root/'artifacts/supplier.circuit.json').read_text());proof=json.loads((root/'artifacts/supplier-routing-adjustments.json').read_text());ids={e.get(e['type']+'_id'):e for e in j}
for c in proof['changes']:
 assert ids.get(c['id'])==c['before'],c['id']+' input mismatch'
 if c['before'] is not None:j.remove(ids[c['id']])
 if c['after'] is not None:j.append(c['after'])
# Apply exact fresh-source insertion metadata for the three bare interfaces.
# This is the only semantic PCB difference left after the copper replay.
metadata=json.loads((root/'artifacts/ch-source-metadata-physical-delta.json').read_text())
fresh=json.loads((root/'artifacts/final-source.circuit.json').read_text());key=lambda e:e.get(e['type']+'_id')
current={key(e):e for e in j};expected={key(e):e for e in fresh};assert len(metadata['changes'])==3
for c in metadata['changes']:
 assert c['reference'] in ['J_BOOT','J_DEBUG','J_MOTOR'] and c['field']=='insertion_direction'
 assert current.get(c['id'])==c['before'],c['id']+' metadata baseline mismatch'
 assert expected.get(c['id'])==c['after'] and c['after']['insertion_direction']=='from_above'
 assert {k:v for k,v in c['after'].items() if k!='insertion_direction'}==c['before'],'Metadata changed native geometry'
replacements={c['id']:c['after'] for c in metadata['changes']};j=[replacements.get(key(e),e) for e in j]
path.write_text(json.dumps(j,indent=2)+'\n');print('Replayed',len(proof['changes']),'PCB adjustments; refresh presentation and run checks.')
