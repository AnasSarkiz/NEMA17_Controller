# Procurement and ratings

The BOM CSV is generated from the final Circuit JSON. Prices below are approximate allowances, not live distributor quotations. Footprint-compatible substitutions need pinout review.

| Parts | Specification / rating |
| --- | --- |
| U_MCU | CH32X035G8U6, QFN-28 4 × 4 mm, 0.4 mm pitch, 2.6 × 2.6 mm ground EP |
| U_DRV | A4988SETTR-T, QFN-28 5 × 5 mm; use the exposed pad and ground thermal via |
| U_PD | CH224K, ESSOP-10 / SSOP-10-EP 3.9 × 4.9 mm, 1 mm pitch, 2.1 × 3.3 mm EP; **not MSOP-10** |
| U_LDO | HT7533-1, 3.3 V, 30 V maximum input, SOT-89-3; pin1 GND, pin2 VIN/tab, pin3 VOUT |
| U_ESD | USBLC6-2SC6, SOT-23-6; D+ pins1/6, D− pins3/4, GND2, data VBUS5 |
| J_PD / J_DATA | HRO TYPE-C-31-M-12, 16-contact USB 2.0 / PD receptacle, four slotted shell anchors; do not substitute a different mechanical footprint |
| D_PD / D_DATA | B5819W, SOD-123, 40 V Schottky; anode=input, cathode=LOGIC_IN |
| D_TVS | SMF18A unidirectional, SOD-123FL-compatible land pattern; cathode PD_VBUS, anode GND; recheck manufacturer land pattern before purchase |
| R_PD | 1 kΩ, **0603 0.25 W high-power**, e.g. Panasonic ERJ-PA3 series; at 15 V its dissipation is approximately 0.10–0.12 W. Do not use ordinary 0.1 W 0603. |
| R_SA / R_SB | 0.25 Ω, 1%, 0805, ≥0.125 W; phase-current dissipation ≈0.04 W each |
| R_REF_H / R_REF_L | 33 kΩ / 10 kΩ, 1%, 0603 |
| R_CC1 / R_CC2 | 5.1 kΩ, 1%, 0603, one independent Rd on each data-port CC pin |
| Other resistors | 0603, 1%, ≥0.1 W; voltage dividers as shown in source |
| C_BULK | 47 µF, **35 V**, radial electrolytic, 5 mm body, 2 mm lead pitch; intended EKMG350ELL470ME11D; verify dimensions/polarity before assembly |
| C_CP / C_VCP / C_VM / C_LDO_IN | 100 nF / 100 nF / 100 nF / 1 µF, X7R, **50 V** (0805 for the latter two); supply capacitor effective capacitance must be reviewed |
| C_VREG | 220 nF X7R, ≥16 V, 0603 |
| C_PD | 1 µF X7R, ≥10 V, 0603; local CH224K VDD decoupling |
| C_MCU / C_DRV_LOGIC | 100 nF X7R, ≥10 V, 0603 |
| C_LOGIC / C_LDO_OUT | 4.7 µF X7R, ≥10 V, 0805; confirm regulator stability with the selected capacitor |
| C_REF / C_VM_SENSE | 10 nF X7R, ≥10 V, 0603 |
| J_MOTOR / J_DEBUG | Wire-solder pads and programmer test pads; no purchased connectors |

Estimated allowance: MCU $0.3–0.7; PD trigger $0.3–0.7; A4988 $1–2; LDO/diodes/ESD/TVS $0.6–1; two USB-C receptacles $0.5–1; passives/bulk $0.5–1. Thermal vias in exposed pads must be bottom-tented; stencil/paste reductions and solder-wicking review are required. No expensive filled via process is assumed. All ordinary signal vias must remain outside component pads.
