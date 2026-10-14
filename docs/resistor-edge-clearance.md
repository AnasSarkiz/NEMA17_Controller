# CH32X035 resistor edge clearance — v1.7.0

Every resistor is reviewed on all four board edges, including top and bottom assembly sides. The nominal pad-to-profile target is **at least 0.75 mm**. A 1 mm placement attempt was assessed; the delivered layout uses the 0.75 mm target within the fixed 35 × 35 mm outline, fixed connectors, native courtyards and screw envelopes.

11 resistors move or rotate. Native land patterns, original JLCPCB OBJ/STEP files, resistor values, physical pin identities and all net assignments are retained. Other component placements, both USB mouths, the JST, the four exact (±13, ±13) Ø3.2 mm holes and PCB outline remain unchanged. Affected copper is rerouted and the ground regions refilled; obsolete trace ends are removed only when the live-pad connectivity partitions remain identical.

The [independent clearance receipt](../artifacts/edge-resistors/clearance-verification.json) matches every resistor pad to its actual regenerated Gerber flash and measures all four edges. The [CSV](../artifacts/edge-resistors/clearance-verification.csv) lists every resistor; the [placement plan](../artifacts/edge-resistors/placement-plan.json) and [translation/rip-up receipt](../artifacts/edge-resistors/translation-and-ripup.json) record construction. The editable `src/supplier-placement.json` contains the final locations and rotations. Freshly compiled native footprints were compared with the translated geometry and canonicalized only for sub-micrometre floating-point differences.

Native DRC, independent physical connectivity, every-trace/net review, copper width/current screening, actual Gerber copper/drill analysis and STEP mechanical screening qualify the final board revision. The [full qualification receipt](../artifacts/resume-validation.json) retains actual exit codes. The six functional schematic sheets and existing electrical interfaces are preserved, with the authorized upright USB-C replacement and optional bottom DNP encoder addition.

The approved 10 mm USB plug housings and M3 DIN 920 maximum Ø4 mm head requirement remain in force. Mechanical screening is nominal CAD evidence. The default export applies the reviewed BOM/CPL, paste/stencil and silkscreen policies. Read the current hash-bound manufacturing audit for its result. Supplier approval, firmware/bench tests and rear motor fit remain pending.

| Resistor | Previous centre (mm) | New centre (mm) | Rotation | New nominal minimum pad-to-edge (mm) |
|---|---|---|---|---|
| R_PG | (16.642, -15.973) | (16.315, -14.560) | 90° | 0.753 |
| R_CC1 | (-16.414, -15.720) | (-16.030, -15.720) | 0° | 0.754 |
| R_CC2 | (16.226, -10.720) | (16.030, -10.720) | 0° | 0.754 |
| R_USB_SENSE_H | (-12.803, 16.702) | (-12.805, 16.315) | 0° | 0.753 |
| R_VM_H | (-15.973, 16.702) | (-15.975, 15.590) | 90° | 0.753 |
| R_VM_L | (-6.623, -16.698) | (-6.625, -16.315) | 0° | 0.753 |
| R_SLEEP | (16.702, 13.877) | (16.315, 13.875) | 90° | 0.753 |
| R_TEMP_SCL | (16.860, 16.396) | (16.030, 16.440) | 180° | 0.754 |
| R_PWR_LED | (15.346, 15.830) | (16.025, 8.510) | 90° | 1.205 |
| R_STATUS_G | (0.480, 16.226) | (0.480, 16.030) | 90° | 0.754 |
| R_BUZZER_GATE | (16.226, -11.930) | (16.030, -11.930) | 0° | 0.754 |

CH32 inner1 retains ground fill with reviewed tracks for ground stitching, the low-current 3.3 V resistor branch and static SLEEP control. Signal routes on this layer are limited to those two named nets and 25 mm. Clock, USB differential pairs and motor phase outputs are excluded. The [layer review](../artifacts/edge-resistors/inner1-routing-review.json) inventories the actual tracks; independent Gerber/ground connectivity and width/current checks remain mandatory. Hardware EMI/thermal validation is pending.
