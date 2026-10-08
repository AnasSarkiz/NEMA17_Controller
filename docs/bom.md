# Procurement and ratings

[The supplier BOM](../artifacts/bom.csv) and [import report](../artifacts/jlcpcb-import-report.json) identify every fitted part. All supplier land patterns and OBJ/STEP assets are included under `imports/supplier/`. Do not substitute parts without reviewing pinout, ratings and land pattern.

R_PD is C441922 / ERJPA3F1001V, 1 kΩ 1%, 0.25 W 0603. R_SA/R_SB are C2930216 / FRL0805FR240TS, 0.24 Ω 1%, 125 mW 0805. R_REF_H is C23018 / 0603WAF3901T5E, 3.9 kΩ 1%; R_REF_L is C441922 / ERJPA3F1001V, 1 kΩ 1%. ENABLE_N/SLEEP pulls are 10 kΩ C25804. C_BULK is C178585 / Panasonic EEEFPV101XAP, 100 µF ±20%, 35 V, rated 0.60 Arms at 100 kHz/105 °C; manufacturer body is 6.3 × 7.7 ±0.3 mm. USB receptacles are C165948 / TYPE-C-31-M-12. Both Schottkys are C8598 / B5819W SL, 40 V.

Capacitor effective capacitance, regulator stability, thermal behavior and regenerative-energy handling require prototype checks. BOM cost estimates are allowances, not current distributor quotations. Motor/debug/boot use bare solder pads. Assembly is top only, with USB shell plated joints requiring soldering.

The final design has **44 fitted native supplier parts**, plus three bare motor/debug/BOOT interfaces. Added protection uses U_VM_ISO C131992 / SN74CBTLV1G125DCKR, Q_DATA C94514 / MMBT3904-7-F, R_VM_EN/R_VM_BLEED 10 kΩ C25804 and C_VM_ISO 100 nF/50 V C14663. Host sense resistors are repurposed 10 kΩ parts. C_VM/C_VM2 are genuine 100 nF/50 V C14663. Native capacitor CAD is retained even though C178585’s generic short model is lower than its maximum manufacturer body; check the separate mechanical envelope before assembly. See component-evidence.md for exact ratings and limits.
