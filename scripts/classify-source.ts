/** Supplier imports use chip JSX; classify passive connectors/crystal accurately for ERC. */
export function classifySource(json:any[]) {
 for(const c of json.filter(e=>e.type==='source_component')) {
  if(c.name.startsWith('J_')) c.ftype='simple_connector'
  if(c.name==='D_TVS') c.ftype='simple_diode'
  if(c.name==='Y_MCU') Object.assign(c,{ftype:'simple_crystal',frequency:12_000_000,load_capacitance:10})
 }
 const bootIds=new Set(json.filter(e=>e.type==='pcb_component' && json.some(c=>c.type==='source_component' && c.source_component_id===e.source_component_id && ['R_USB_BOOT','J_BOOT'].includes(c.name))).map(e=>e.pcb_component_id))
 for(const e of json) if(e.type==='pcb_silkscreen_text' && bootIds.has(e.pcb_component_id)) e.pcb_silkscreen_text_id='usb_boot_'+e.pcb_silkscreen_text_id
 // Full references stay on assembly drawings; PCB silk keeps deliberate
 // functional labels and native graphical polarity/pin-1 marks.
 return json.filter(e=>e.type!=='pcb_silkscreen_text' || !e.pcb_component_id)
}
