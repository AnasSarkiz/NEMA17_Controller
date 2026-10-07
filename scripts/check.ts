import { readFileSync, writeFileSync } from "node:fs"
import { runAllChecks, checkViasInPads } from "@tscircuit/checks"
const json=JSON.parse(readFileSync('artifacts/board.circuit.json','utf8'))
const checks=await runAllChecks(json)
// Permit only the three explicit grounded thermal vias inside exposed pads.
const thermalNames=['U_MCU','U_DRV','U_PD']
const thermalCenters:Array<[number,number]>=json.filter((p:any)=>p.type==='pcb_smtpad' && p.width>1 && p.height>1 && json.some((c:any)=>c.type==='pcb_component' && c.pcb_component_id===p.pcb_component_id && json.some((s:any)=>s.type==='source_component' && s.source_component_id===c.source_component_id && thermalNames.includes(s.name)))).map((p:any)=>[p.x,p.y])
const ground=json.find((e:any)=>e.type==='source_net' && e.name==='GND')
const strict=json.filter((e:any)=>!(e.type==='pcb_via' && e.source_net_id===ground.source_net_id && thermalCenters.some(([x,y])=>Math.hypot(e.x-x,e.y-y)<.001))).map((e:any)=>e.type==='pcb_board'?{...e,is_via_in_pad_allowed:false}:e)
checks.push(...checkViasInPads(strict))
const renderErrors=json.filter((e:any)=>e.type.endsWith('_error'))
const errors=[...renderErrors,...checks.filter((e:any)=>e.type.endsWith('_error'))]
const unique=[...new Map(errors.map((e:any)=>[e.message,e])).values()]
const warnings=checks.filter((e:any)=>e.type.endsWith('_warning'))
const traceCount=json.filter((e:any)=>e.type==='pcb_trace').length
if(traceCount===0) unique.push({type:'validation_error',message:'No routed copper was produced.'})
const board=json.find((e:any)=>e.type==='pcb_board')
if(!board || board.width!==35 || board.height!==35) unique.push({type:'validation_error',message:'Expected a 35 by 35 mm PCB.'})
for (const [name,edge] of [['J_PD',-17.5],['J_DATA',17.5]] as const) {
 const source=json.find((e:any)=>e.type==='source_component' && e.name===name)
 const component=json.find((e:any)=>e.type==='pcb_component' && e.source_component_id===source?.source_component_id)
 const cad=json.find((e:any)=>e.type==='cad_component' && e.source_component_id===source?.source_component_id)
 // Exact imported TYPE-C model: mating plane is local Y=2.6 mm, origin Y=-2.7500289 mm.
 const angle=(cad?.rotation?.z??0)*Math.PI/180
 const front=cad ? cad.position.x-Math.sin(angle)*(2.6-cad.model_origin_position.y) : NaN
 if(!Number.isFinite(front) || Math.abs(front-edge)>.001) unique.push({type:'validation_error',message:name+' imported USB-C mating plane is not flush with the board edge.'})
}
const holes=json.filter((e:any)=>e.type==='pcb_hole' && e.hole_diameter===3.2)
if(holes.length!==4) unique.push({type:'validation_error',message:'Expected four 3.2 mm mounting holes.'})
const resistance=(name:string)=>json.find((e:any)=>e.type==='source_component' && e.name===name)?.resistance
const vref=3.3*resistance('R_REF_L')/(resistance('R_REF_H')+resistance('R_REF_L')), current=vref/(8*resistance('R_SA'))
if(!Number.isFinite(current) || resistance('R_SA')!==resistance('R_SB')) unique.push({type:'validation_error',message:'Missing or mismatched phase-current setting resistors.'})
const worstCurrent=3.33*(resistance('R_REF_L')*1.01)/(resistance('R_REF_H')*.99+resistance('R_REF_L')*1.01)/(8*resistance('R_SA')*.99)*1.05
if(worstCurrent>.4) unique.push({type:'validation_error',message:'Estimated tolerance-bound phase current exceeds 0.4 A.'})
if(current>.4) unique.push({type:'validation_error',message:'Nominal phase current exceeds 0.4 A.'})
const report={date:new Date().toISOString(),tool:'@tscircuit/checks',traceCount,currentLimitAmps:current,errors:unique,warnings,manufacturingRelease:false,releaseBlockers:['Manufacturer drawing specifies front mounting only; rear adapter fit is unverified.','Hardware has not been assembled or electrically tested.','Footprint/rating and USB/PD bench validation remain required.']}
writeFileSync('artifacts/drc-report.json',JSON.stringify(report,null,2)+'\n')
console.log(JSON.stringify({traceCount,currentLimitAmps:current,errors:unique.length,warnings:warnings.length},null,2))
for(const error of unique) console.error(error.type+': '+error.message)
if(unique.length) process.exitCode=1
