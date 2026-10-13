import React from "react"
import { pinProps } from "./pin-attributes"
import { SupplierPart } from "./supplier-parts"
import placements from "./supplier-placement.json"
const place=(name:string)=>(placements as Record<string,{pcbX:number,pcbY:number,pcbRotation:number}>)[name]
import { SchematicNotes } from "./schematic-notes"

// Fixed NEMA14 hole pattern. Same-edge ports require DIN 920 M3 heads ≤4 mm.
// Circular Ø4.4 mm head envelope includes a defined 0.2 mm radial allowance; rear mounting is unverified.
export const mechanical = { width: 35, height: 35, holePitch: 26, holeDiameter: 3.2, headEnvelopeRadius: 2.2, usbPortPitch: 12.4 }
const n = (name: string) => `net.${name}`
const mcuPins = {pin1:"CC2_UNUSED",pin2:"VDD",pin3:"PC0",pin4:"PC3",pin5:"STEP",pin6:"DIR",pin7:"PD_GOOD",pin8:"DATA_PRESENT",pin9:"VM_SENSE",pin10:"PA5",pin11:"PA6",pin12:"PA7",pin13:"PB0",pin14:"ENABLE_N",pin15:"SLEEP",pin16:"PB1",pin17:"PB6",pin18:"PB7",pin19:"PB8",pin20:"PB9",pin21:"PB10",pin22:"PB11",pin23:"PB12",pin24:"DCK",pin25:"DIO",pin26:"USB_DM",pin27:"USB_DP",pin28:"CC1_UNUSED",pin29:"GND"} as const
const driverPins = {pin1:"OUT2B",pin2:"ENABLE_N",pin3:"GND",pin4:"CP1",pin5:"CP2",pin6:"VCP",pin7:"NC7",pin8:"VREG",pin9:"MS1",pin10:"MS2",pin11:"MS3",pin12:"RESET_N",pin13:"ROSC",pin14:"SLEEP",pin15:"VDD",pin16:"STEP",pin17:"REF",pin18:"GND18",pin19:"DIR",pin20:"NC20",pin21:"OUT1B",pin22:"VBB1",pin23:"SENSE1",pin24:"OUT1A",pin25:"NC25",pin26:"OUT2A",pin27:"SENSE2",pin28:"VBB2",pin29:"EP"} as const
const pdPins = {pin1:"VDD",pin2:"CFG2",pin3:"CFG3",pin4:"DP",pin5:"DM",pin6:"CC2",pin7:"CC1",pin8:"VBUS",pin9:"CFG1",pin10:"PG",pin11:"GND"} as const
const baseUsb = {GND1:n("GND"),GND2:n("GND"),EH1:n("GND"),EH2:n("GND"),EH3:n("GND"),EH4:n("GND")}
const resistor = (name:string,value:string,a:string,b:string) => <SupplierPart key={name} name={name}  resistance={value} {...place(name)} connections={{pin1:n(a),pin2:b.startsWith('.')?b:n(b)}} />
const cap = (name:string,value:string,a:string,b="GND") => <SupplierPart key={name} name={name}  capacitance={value} {...place(name)} connections={{pin1:n(a),pin2:n(b)}} />

export default function Nema14Controller({ routingDisabled = false, assemblyPreview = false }: { routingDisabled?: boolean, assemblyPreview?: boolean } = {}) {
 return <board {...(assemblyPreview?{name:"CONTROLLER_PCB",mountedTo:"MOTOR_REFERENCE_CONCEPT.backface",mountGap:"6mm"}:{})} width={35} height={35} layers={4} thickness={1.6}
  routingDisabled={routingDisabled} minTraceWidth={0.16} minTraceToPadEdgeClearance={0.15} minPadEdgeToPadEdgeClearance={0.15}
  minViaHoleDiameter={0.25} minViaPadDiameter={0.5} minBoardEdgeClearance={0.25}
  autorouter={{local:true, traceClearance:0.15}} autorouterEffortLevel="2x" schAutoLayoutEnabled={false}>
  <schematicsheet name="NEMA14_CH32X035G8U6" sheetSize="A4">
  {['GND','PD_VBUS','V3V3','LOGIC_IN','DATA_VBUS','PD_VDD','PD_CC1','PD_CC2','DATA_CC1','DATA_CC2','USB_DP','USB_DM','STEP','DIR','ENABLE_N','SLEEP','PD_GOOD','DCK','DIO','BOOT_PAD','DATA_PRESENT','VM_SENSE','VREF','CP1','CP2','VCP','VREG','SENSE1','SENSE2','A_PLUS','A_MINUS','B_PLUS','B_MINUS','PWR_LED_A','TEMP_SDA','TEMP_SCL','BUZZER_PWM','BUZZER_GATE','BUZZER_SINK','LED_R','LED_G','LED_B','STATUS_R_K','STATUS_G_K','STATUS_B_K','STATUS_R_C','STATUS_G_C','STATUS_B_C','BUCK_SW','BUCK_BST'].map(name=><React.Fragment key={name}><net name={name} isGroundNet={name==='GND'} isPowerNet={['PD_VBUS','V3V3','LOGIC_IN','DATA_VBUS','PD_VDD'].includes(name)} nominalTraceWidth={['PD_VBUS','A_PLUS','A_MINUS','B_PLUS','B_MINUS','SENSE1','SENSE2'].includes(name)?0.45:0.16} /></React.Fragment>)}
  {/* These keepouts constrain copper. Supplier courtyards remain intact; native STEP solids independently validate component/head clearance. */}
  {[-mechanical.holePitch/2,mechanical.holePitch/2].flatMap(x=>[-mechanical.holePitch/2,mechanical.holePitch/2].map(y=><React.Fragment key={`${x},${y}`}><hole name={`M${x}_${y}`} pcbX={x} pcbY={y} diameter={mechanical.holeDiameter} /><keepout pcbX={x} pcbY={y} shape="circle" radius={mechanical.headEnvelopeRadius} allowPlacements={true} layers={['top','inner1','inner2','bottom']} /><silkscreencircle pcbX={x} pcbY={y} radius={mechanical.headEnvelopeRadius} strokeWidth={0.1} /></React.Fragment>))}
  <SupplierPart name="J_PD" {...pinProps("J_PD")}    noConnect={['DP1','DP2','DM1','DM2','SBU1','SBU2']} {...place("J_PD")} connections={{...baseUsb,VBUS1:n('PD_VBUS'),VBUS2:n('PD_VBUS'),CC1:n('PD_CC1'),CC2:n('PD_CC2')}} />
  <SupplierPart name="J_DATA" {...pinProps("J_DATA")}    noConnect={['SBU1','SBU2']} {...place("J_DATA")} connections={{...baseUsb,VBUS1:n('DATA_VBUS'),VBUS2:n('DATA_VBUS'),CC1:n('DATA_CC1'),CC2:n('DATA_CC2'),DP1:n('USB_DP'),DP2:n('USB_DP'),DM1:n('USB_DM'),DM2:n('USB_DM')}} />
  <SupplierPart name="U_PD" {...pinProps("U_PD")}  pinLabels={pdPins} noConnect={['DP','DM']} {...place("U_PD")} connections={{VDD:n('PD_VDD'),CFG2:n('PD_VDD'),CFG3:n('PD_VDD'),CFG1:n('GND'),VBUS:n('PD_VBUS'),CC1:n('PD_CC1'),CC2:n('PD_CC2'),PG:n('PD_GOOD'),GND:n('GND')}} />
  {resistor('R_PD','1k','PD_VBUS','PD_VDD')}
  {cap('C_PD','1uF','PD_VDD')}
  {resistor('R_PG','10k','V3V3','PD_GOOD')}
  <SupplierPart name="U_MCU" {...pinProps("U_MCU")}  pinLabels={mcuPins} noConnect={["CC2_UNUSED", "PC0", "PC3", "PB1", "PB9", "PB8", "PB10", "PB11", "PB12", "CC1_UNUSED"]} {...place("U_MCU")} connections={{VDD:n('V3V3'),GND:n('GND'),STEP:n('STEP'),DIR:n('DIR'),ENABLE_N:n('ENABLE_N'),SLEEP:n('SLEEP'),PD_GOOD:n('PD_GOOD'),DATA_PRESENT:n('DATA_PRESENT'),VM_SENSE:n('VM_SENSE'),USB_DM:n('USB_DM'),USB_DP:n('USB_DP'),DCK:n('DCK'),DIO:n('DIO'),PB7:n('TEMP_SDA'),PB6:n('TEMP_SCL'),PA6:n('BUZZER_PWM'),PA5:n('LED_R'),PA7:n('LED_G'),PB0:n('LED_B')}} />
  {cap('C_MCU','100nF','V3V3')}
  {cap('C_LOGIC','4.7uF','V3V3','GND')}
  {resistor('R_CC1','5.1k','DATA_CC1','GND')}
  {resistor('R_CC2','5.1k','DATA_CC2','GND')}
  {resistor('R_USB_SENSE_H','100k','DATA_VBUS','DATA_PRESENT')}
  {resistor('R_USB_SENSE_L','100k','DATA_PRESENT','GND')}
  {resistor('R_VM_H','100k','PD_VBUS','VM_SENSE')}
  {resistor('R_VM_L','10k','VM_SENSE','GND')}
  {cap('C_VM_SENSE','10nF','VM_SENSE')}
  <SupplierPart name="U_BUCK" {...pinProps("U_BUCK")} pinLabels={{pin1:"FB",pin2:"EN",pin3:"VIN",pin4:"GND",pin5:"SW",pin6:"BST"}} {...place("U_BUCK")} connections={{FB:n("V3V3"),EN:n("LOGIC_IN"),VIN:n("LOGIC_IN"),GND:n("GND"),SW:n("BUCK_SW"),BST:n("BUCK_BST")}} />
  <SupplierPart name="D_PD" {...place("D_PD")} connections={{anode:n('PD_VBUS'),cathode:n('LOGIC_IN')}} />
  <SupplierPart name="D_DATA" {...place("D_DATA")} connections={{anode:n('DATA_VBUS'),cathode:n('LOGIC_IN')}} />
  <SupplierPart name="U_DRV" {...pinProps("U_DRV")}  pinLabels={driverPins} noConnect={['NC7','NC20','NC25']} {...place("U_DRV")} connections={{OUT1A:n('A_PLUS'),OUT1B:n('A_MINUS'),OUT2A:n('B_PLUS'),OUT2B:n('B_MINUS'),VBB1:n('PD_VBUS'),VBB2:n('PD_VBUS'),GND:n('GND'),GND18:n('GND'),EP:n('GND'),CP1:n('CP1'),CP2:n('CP2'),VCP:n('VCP'),VREG:n('VREG'),MS1:n('V3V3'),MS2:n('V3V3'),MS3:n('V3V3'),RESET_N:n('V3V3'),VDD:n('V3V3'),ROSC:n('GND'),STEP:n('STEP'),DIR:n('DIR'),ENABLE_N:n('ENABLE_N'),SLEEP:n('SLEEP'),REF:n('VREF'),SENSE1:n('SENSE1'),SENSE2:n('SENSE2')}} />
  {cap('C_CP','100nF','CP1','CP2')}
  {cap('C_VCP','100nF','VCP','PD_VBUS')}
  {cap('C_VREG','220nF','VREG')}
  {cap('C_DRV_LOGIC','100nF','V3V3')}
  {cap('C_VM','100nF','PD_VBUS','GND')}
  <SupplierPart name="C_BULK" capacitance="47uF" {...place("C_BULK")} connections={{pin1:n("PD_VBUS"),pin2:n("GND")}} />
  {resistor('R_SA','0.24','SENSE1','GND')}
  {resistor('R_SB','0.24','SENSE2','GND')}
  {resistor('R_REF_H','39k','V3V3','VREF')}
  {resistor('R_REF_L','10k','VREF','GND')}
  {cap('C_REF','10nF','VREF')}
  {resistor('R_ENABLE','100k','V3V3','ENABLE_N')}
  {resistor('R_SLEEP','100k','SLEEP','GND')}
  <SupplierPart noConnect={["MOUNT1","MOUNT2"]} name="J_MOTOR" {...pinProps("J_MOTOR")} {...place("J_MOTOR")} connections={{A_PLUS:n("A_PLUS"),A_MINUS:n("A_MINUS"),B_PLUS:n("B_PLUS"),B_MINUS:n("B_MINUS")}} />
  <SupplierPart name="U_ESD" {...pinProps("U_ESD")}  pinLabels={{pin1:"DP1",pin2:"GND",pin3:"DM1",pin4:"DM2",pin5:"VBUS",pin6:"DP2"}} {...place("U_ESD")} connections={{DP1:n("USB_DP"),DP2:n("USB_DP"),DM1:n("USB_DM"),DM2:n("USB_DM"),VBUS:n("DATA_VBUS"),GND:n("GND")}} />
  <SupplierPart name="D_TVS" {...place("D_TVS")} connections={{pin1:n("GND"),pin2:n("PD_VBUS")}} />
  {resistor('R_USB_BOOT','4.7k','V3V3','BOOT_PAD')}
  <silkscreentext text="NEMA14 USB+PD" pcbX={0} pcbY={-16.9} fontSize={1} />
  <silkscreentext text="PD 15V" pcbX={-6.2} pcbY={8.2} fontSize={.7} />
  <silkscreentext text="USB DATA" pcbX={6.2} pcbY={8.2} fontSize={.7} />
  <silkscreentext text="A+ A- B+ B-" pcbX={0} pcbY={-13.7} fontSize={.65} />
  <SupplierPart name="L_BUCK" inductance="4.7uH" {...place("L_BUCK")} connections={{pin1:n("BUCK_SW"),pin2:n("V3V3")}} />
  {cap("C_BOOTSTRAP","100nF","BUCK_BST","BUCK_SW")}
  {cap("C_BUCK_IN","10uF","LOGIC_IN")}
  {cap("C_BUCK_OUT1","22uF","V3V3")}
  {cap("C_BUCK_OUT2","22uF","V3V3")}

  {/* Reference feedback: TMP102 I2C address 0x48; alerts handled by application firmware. */}
  <SupplierPart name="U_TEMP" {...pinProps("U_TEMP")} {...place("U_TEMP")} noConnect={['ALERT']} connections={{SCL:n('TEMP_SCL'),GND:n('GND'),ADD0:n('GND'),V_POS:n('V3V3'),SDA:n('TEMP_SDA')}} />
  {cap('C_TEMP','100nF','V3V3')}
  {resistor('R_TEMP_SDA','4.7k','TEMP_SDA','V3V3')}
  {resistor('R_TEMP_SCL','4.7k','TEMP_SCL','V3V3')}
  <SupplierPart name="D_PWR" {...place("D_PWR")} connections={{anode:n('PWR_LED_A'),cathode:n('GND')}} />
  {resistor('R_PWR_LED','330','V3V3','PWR_LED_A')}
  {/* Common anode uses fixed programming USB 5 V, never the negotiated PD rail. */}
  <SupplierPart name="D_STATUS" {...pinProps("D_STATUS")} {...place("D_STATUS")} connections={{_POS:n('DATA_VBUS'),R_NEG:n('STATUS_R_K'),G_NEG:n('STATUS_G_K'),B_NEG:n('STATUS_B_K')}} />
  {(['R','G','B'] as const).map(color=><React.Fragment key={'status_'+color}>
    {resistor('R_STATUS_'+color,'1k','STATUS_'+color+'_K','STATUS_'+color+'_C')}
    <SupplierPart name={'Q_STATUS_'+color} {...pinProps('Q_STATUS_'+color)} {...place('Q_STATUS_'+color)} connections={{E:n('GND'),B:n('LED_'+color),C:n('STATUS_'+color+'_C')}} />
  </React.Fragment>)}
  <SupplierPart name="BZ1" {...pinProps("BZ1")} {...place("BZ1")} noConnect={['NC1','NC2']} connections={{_POS:n('V3V3'),_NEG:n('BUZZER_SINK')}} />
  <SupplierPart name="Q_BUZZER" {...pinProps("Q_BUZZER")} {...place("Q_BUZZER")} connections={{G:n('BUZZER_GATE'),S:n('GND'),D:n('BUZZER_SINK')}} />
  <SupplierPart name="D_BUZZER" {...place("D_BUZZER")} connections={{cathode:n('V3V3'),anode:n('BUZZER_SINK')}} />
  {resistor('R_BUZZER_GATE','100','BUZZER_PWM','BUZZER_GATE')}
  {resistor('R_BUZZER_PD','100k','BUZZER_GATE','GND')}
  {cap('C_BUZZER','10uF','V3V3')}
  <testpoint name="TP_3V3" layer="top" footprintVariant="pad" padDiameter="1.1mm" footprint={<footprint><smtpad portHints={["pin1"]} shape="circle" radius={.55} /><courtyardoutline outline={[{x:-.7,y:-.7},{x:.7,y:-.7},{x:.7,y:.7},{x:-.7,y:.7},{x:-.7,y:-.7}]} /></footprint>} {...place("TP_3V3")} connections={{pin1:n("V3V3")}} />
  <testpoint name="TP_GND" layer="top" footprintVariant="pad" padDiameter="1.1mm" footprint={<footprint><smtpad portHints={["pin1"]} shape="circle" radius={.55} /><courtyardoutline outline={[{x:-.7,y:-.7},{x:.7,y:-.7},{x:.7,y:.7},{x:-.7,y:.7},{x:-.7,y:-.7}]} /></footprint>} {...place("TP_GND")} connections={{pin1:n("GND")}} />
  <testpoint name="TP_DCK" layer="top" footprintVariant="pad" padDiameter="1.1mm" footprint={<footprint><smtpad portHints={["pin1"]} shape="circle" radius={.55} /><courtyardoutline outline={[{x:-.7,y:-.7},{x:.7,y:-.7},{x:.7,y:.7},{x:-.7,y:.7},{x:-.7,y:-.7}]} /></footprint>} {...place("TP_DCK")} connections={{pin1:n("DCK")}} />
  <testpoint name="TP_DIO" layer="top" footprintVariant="pad" padDiameter="1.1mm" footprint={<footprint><smtpad portHints={["pin1"]} shape="circle" radius={.55} /><courtyardoutline outline={[{x:-.7,y:-.7},{x:.7,y:-.7},{x:.7,y:.7},{x:-.7,y:.7},{x:-.7,y:-.7}]} /></footprint>} {...place("TP_DIO")} connections={{pin1:n("DIO")}} />
  <testpoint name="TP_BOOT" layer="top" footprintVariant="pad" padDiameter="1.1mm" footprint={<footprint><smtpad portHints={["pin1"]} shape="circle" radius={.55} /><courtyardoutline outline={[{x:-.7,y:-.7},{x:.7,y:-.7},{x:.7,y:.7},{x:-.7,y:.7},{x:-.7,y:-.7}]} /></footprint>} {...place("TP_BOOT")} connections={{pin1:n("BOOT_PAD")}} />
  <testpoint name="TP_BOOT_USB_DP" layer="top" footprintVariant="pad" padDiameter="1.1mm" footprint={<footprint><smtpad portHints={["pin1"]} shape="circle" radius={.55} /><courtyardoutline outline={[{x:-.7,y:-.7},{x:.7,y:-.7},{x:.7,y:.7},{x:-.7,y:.7},{x:-.7,y:-.7}]} /></footprint>} {...place("TP_BOOT_USB_DP")} connections={{pin1:n("USB_DP")}} />
  <SchematicNotes />
  </schematicsheet>
 </board>
}
