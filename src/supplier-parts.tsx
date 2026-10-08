import { MMBT3904_7_F } from "../imports/supplier/MMBT3904_7_F/MMBT3904_7_F"
import { SN74CBTLV1G125DCKR } from "../imports/supplier/SN74CBTLV1G125DCKR/SN74CBTLV1G125DCKR"
import { EEEFPV101XAP } from "../imports/supplier/EEEFPV101XAP/EEEFPV101XAP"
import { A_0603WAF3901T5E } from "../imports/supplier/A_0603WAF3901T5E/A_0603WAF3901T5E"
import { ERJPA3F1001V } from "../imports/supplier/ERJPA3F1001V/ERJPA3F1001V"
import React from "react"
import catalog from "./jlcpcb-catalog.json"
import { HT7533_1 } from "../imports/supplier/HT7533_1/HT7533_1"
import { CC0603KRX7R9BB104 } from "../imports/supplier/CC0603KRX7R9BB104/CC0603KRX7R9BB104"
import { CL10A105KB8NNNC } from "../imports/supplier/CL10A105KB8NNNC/CL10A105KB8NNNC"
import { CL10B103KB8NNNC } from "../imports/supplier/CL10B103KB8NNNC/CL10B103KB8NNNC"
import { TYPE_C_31_M_12 } from "../imports/supplier/TYPE_C_31_M_12/TYPE_C_31_M_12"
import { SMF18A } from "../imports/supplier/SMF18A/SMF18A"
import { CL10B224KA8NNNC } from "../imports/supplier/CL10B224KA8NNNC/CL10B224KA8NNNC"
import { A_0603WAF1001T5E } from "../imports/supplier/A_0603WAF1001T5E/A_0603WAF1001T5E"
import { A_0603WAF3902T5E } from "../imports/supplier/A_0603WAF3902T5E/A_0603WAF3902T5E"
import { A_0603WAF5101T5E } from "../imports/supplier/A_0603WAF5101T5E/A_0603WAF5101T5E"
import { A_0603WAF1003T5E } from "../imports/supplier/A_0603WAF1003T5E/A_0603WAF1003T5E"
import { A_0603WAF1002T5E } from "../imports/supplier/A_0603WAF1002T5E/A_0603WAF1002T5E"
import { A_0402WGF4701TCE } from "../imports/supplier/A_0402WGF4701TCE/A_0402WGF4701TCE"
import { USBLC6_2SC6 } from "../imports/supplier/USBLC6_2SC6/USBLC6_2SC6"
import { CL21B105KBFNNNE } from "../imports/supplier/CL21B105KBFNNNE/CL21B105KBFNNNE"
import { FRL0805FR240TS } from "../imports/supplier/FRL0805FR240TS/FRL0805FR240TS"
import { A_0603WAF2202T5E } from "../imports/supplier/A_0603WAF2202T5E/A_0603WAF2202T5E"
import { A4988SETTR_T } from "../imports/supplier/A4988SETTR_T/A4988SETTR_T"
import { CC0805KRX7R9BB104 } from "../imports/supplier/CC0805KRX7R9BB104/CC0805KRX7R9BB104"
import { RVT1V470M0605 } from "../imports/supplier/RVT1V470M0605/RVT1V470M0605"
import { CH32X035G8U6 } from "../imports/supplier/CH32X035G8U6/CH32X035G8U6"
import { B5819W_SL } from "../imports/supplier/B5819W_SL/B5819W_SL"
import { CH224K } from "../imports/supplier/CH224K/CH224K"
import { CL21A475KBQNNNE } from "../imports/supplier/CL21A475KBQNNNE/CL21A475KBQNNNE"
const parts: Record<string, React.ComponentType<any>> = {
 "C94514": MMBT3904_7_F,
 "C131992": SN74CBTLV1G125DCKR,
 "C178585": EEEFPV101XAP,
 "C23018": A_0603WAF3901T5E,
 "C441922": ERJPA3F1001V,
 "C14289": HT7533_1,
 "C14663": CC0603KRX7R9BB104,
 "C15849": CL10A105KB8NNNC,
 "C1589": CL10B103KB8NNNC,
 "C165948": TYPE_C_31_M_12,
 "C19077512": SMF18A,
 "C21120": CL10B224KA8NNNC,
 "C21190": A_0603WAF1001T5E,
 "C23153": A_0603WAF3902T5E,
 "C23186": A_0603WAF5101T5E,
 "C25803": A_0603WAF1003T5E,
 "C25804": A_0603WAF1002T5E,
 "C25900": A_0402WGF4701TCE,
 "C2687116": USBLC6_2SC6,
 "C28323": CL21B105KBFNNNE,
 "C2930216": FRL0805FR240TS,
 "C31850": A_0603WAF2202T5E,
 "C38437": A4988SETTR_T,
 "C49678": CC0805KRX7R9BB104,
 "C72522": RVT1V470M0605,
 "C7437027": CH32X035G8U6,
 "C8598": B5819W_SL,
 "C970725": CH224K,
 "C98192": CL21A475KBQNNNE
}
/** Uses supplier-imported components directly; never overrides land patterns or CAD transforms. */
export function SupplierPart({name,...props}:any) {
 const id=(catalog.components as Record<string,string>)[name]
 if(!id || !parts[id]) throw new Error("Missing supplier import for "+name)
 if(props.footprint || props.cadModel) throw new Error("Supplier geometry override is forbidden: "+name)
 return React.createElement(parts[id], {name,...props})
}
