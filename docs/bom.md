# Procurement and ratings

[The supplier BOM](../artifacts/bom.csv) and [import report](../artifacts/jlcpcb-import-report.json) identify every fitted part. All supplier land patterns and OBJ/STEP assets are included under `imports/supplier/`. Do not substitute parts without reviewing pinout, ratings and land pattern.

R_PD is C441922 / ERJPA3F1001V, 1 kΩ 1%, 0.25 W 0603. R_SA/R_SB are C2930216 / FRL0805FR240TS, 0.24 Ω 1%, 125 mW 0805. R_REF_H/R_REF_L are 39k/10k. C_BULK is C72522 / RVT1V470M0605, 47 µF 35 V, SMD 6.3 × 5.4 mm. USB receptacles are C165948 / TYPE-C-31-M-12. Both Schottkys are C8598 / B5819W SL, 40 V.

Capacitor effective capacitance, regulator stability, thermal behavior and regenerative-energy handling require prototype checks. BOM cost estimates are allowances, not current distributor quotations. Motor/debug/boot use bare solder pads. Assembly is top only, with USB shell plated joints requiring soldering.
