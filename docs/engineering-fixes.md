# NEMA14_CH32X035G8U6 1.11.0: engineering fixes

Saved board SHA-256: `0d772c1f839f50f30caa512a0dcc58f8ecfa88e35c2e9b44c2422365bc0a8e64`. Starting GitHub revision: `a342a888b82d46c8a56bb510bb04c3a29b179543`. Original functional nets, NC roles, values and ratings are preserved, with the authorized USB4145 upright connector substitution and three added bottom DNP encoder components; see `artifacts/engineering-fixes/final-engineering-verification.json`.

The board is 35 × 35 × 1.6 mm, four layers, with four NPTH holes exactly (±13, ±13), Ø3.2 mm. USB4145-03-0070-C (C5815189) sockets face +Z on opposite PCB edges at nominal J_PD (0.3, 15.15), J_DATA (0.0, -15.15) mm. Two defined 10 mm cable housings have 23.300 mm separation. Maximum Ø6 mm × 3 mm screw heads are screened with a Ø6.4 mm × 3 mm envelope; a Ø6 mm vertical driver shaft is screened with both cable housings present. This verifies nominal CAD geometry, not physical assembly or rear motor attachment.

All 61 fitted parts and 6 separate bare test pads remain on top. Standard USB-C schematic symbols, both contact orientations, independent 5.1 kΩ data CC resistors, CH224K 15 V configuration, Schottky supply isolation, SMT JST-SH C160390 coil order, TMP102, LEDs and buzzer are retained. See [reference pin review](reference-feedback.md) and [motor connector/harness](jst-restoration.md).

The AS5600-ASOM (C79815) and its 100 nF/1 µF bypass capacitors are on the bottom with doNotPlace. It shares the existing 3.3 V I²C bus (address 0x36, distinct from TMP102 0x48). Its OUT and PGO remain NC. Rear shaft, magnet selection/air gap, encoder firmware and physical fit require later verification.

Minimum via drill/pad are Ø0.30/Ø0.45 mm. Exactly three grounded thermal barrels are required at the reviewed MCU, driver and PD exposed-pad sites; the RP2040 MCU site is shifted within its native EP to clear the bottom encoder lands. The actual process coordinates are in `Thermal-Via-Process.csv` and `src/thermal-via-offsets.json`. The source geometry and actual Excellon drills are checked, including drill-to-copper and drill-to-drill clearance. GCT’s native USB STEP is invalid in OCCT; the mechanical screen uses its complete bounding solid as a conservative envelope, retaining original supplier assets.

## Routing and source fixes

ESD protection and local parts were moved to support coupled outer-layer USB trunks with explicit MCU/ESD/resistor fanouts. Affected copper and ground returns were rerouted; redundant stubs and duplicate records were removed. Every rail bridge retains its actual downstream-load and copper-width screening; see `artifacts/trace-width-review.json`. The reviewed layer policy bounds low-current/control escapes and the short 0.3 mm phase bridge; clocks/flash retain a 15 mm section limit. Every trace, segment, via ownership and attached physical port is inventoried, with actual copper connectivity and thermal/clearance checks required separately.

| Reference | Previous XY mm | Current XY mm |
|---|---|---|
| J_PD | (-6.05, 15.149999999999999) | (0.30000000000000027, 15.149999999999999) |
| J_DATA | (6.05, 15.149999999999999) | (0, -15.149999999999999) |
| R_PD | (12.796602, 15.942003) | (12.8, 8.9) |
| R_PG | (16.31, -14.54) | (16.3, -8.28) |
| R_CC1 | (-16.03, -15.72) | (-6.4, -15.72) |
| R_CC2 | (16.03, -10.72) | (6.8, -10.72) |
| R_USB_SENSE_L | (-8.804901, -11.83999) | (-8.8, -16.3) |
| R_VM_L | (-6.625, -16.315) | (-6.62, 5.5) |
| C_VM_SENSE | (14.580023, -16.670001) | (14.58, 6.76) |
| D_PD | (-14.829979, 0.410011) | (12.88, -8.58) |
| D_DATA | (9.389986, -11.869979) | (-8.59, -11.87) |
| C_VCP | (-7.559885, -8.199998) | (-7.56, -8.2) |
| C_VREG | (-4.689977, -11.490001) | (-4.69, -11.49) |
| C_BULK | (-12.05, -5.4) | (-13.84, -5.01) |
| R_REF_L | (6.006602, -7.787997) | (4.62, -7.79) |
| R_ENABLE | (-7.073398, -9.427997) | (-7.07, -6.96) |
| R_SLEEP | (16.31, 14.13) | (6.04, 14.13) |
| J_MOTOR | (-1.5499999999999996, -14.57) | (-7.2, 12.850000000000001) |
| C_BUCK_OUT1 | (-13.355, 9.805005) | (-15.430000000000001, 7.85) |
| C_BUCK_OUT2 | (-15.165000000000001, 7.745005) | (-7.54, 2.79) |
| U_TEMP | (6.959985, -9.649923) | (4.51, -11.81) |
| C_TEMP | (7.340115, -11.219998) | (7.34, -11.8) |
| R_TEMP_SCL | (16.03, 16.44) | (9.17, 16.44) |
| D_PWR | (-9.341006, -14.216572) | (-13.32, 0.8700000000000001) |
| D_STATUS | (-16.320002, 12.301996) | (7.800000000000001, 12.3) |
| R_STATUS_G | (0.48, 16.03) | (0.48, 9.17) |
| Q_BUZZER | (15.629997, -8.46999) | (8.55, -8.45) |
| D_BUZZER | (11.437407, -7.820002000000001) | (11.82, 5.77) |
| R_BUZZER_GATE | (16.03, -11.93) | (6.98, -12.88) |
| R_BUZZER_PD | (11.755645, -10.219998) | (9.1, -10.71) |
| C_BUZZER | (6.6, -12.5) | (5.64, -1.44) |
| TP_DIO | (10.5, -15.5) | (10.5, -16.69) |

| Coupled core | Signal / reference layer | Length difference mm | Exact grounded reference coverage outside actual USB via antipads |
|---|---|---|---|
| connector_to_ESD | bottom / inner2 | 0.023 | 100.000%, 100.000% |
| ESD_to_MCU | bottom / inner2 | 0.000 | 100.000%, 100.000% |

Core width/gap are 0.25/0.16 mm; local terminal fanouts are 0.16 mm. Every projected centerline is intersected geometrically with adjacent grounded copper. This is layout evidence; fabricator stackup/controlled impedance, USB signal integrity, EMC and hardware operation are unverified.

Display offsets are canonical strings and optional null IDs are omitted. Board-level silkscreen records have a valid metadata owner while retaining absolute coordinates. BZ1 uses the installed generic pinout classification with its real MPN, pins, nets, models and qualified schematic retained. Strict schema checks accept no inherited errors.

## Manufacturing output

The default `artifacts/nema14-gerbers.zip` now applies qualified source-derived BOM/CPL, top-only paste, 100 µm stencil apertures, four 60% exposed-pad windows and readable silkscreen with mask/drill/edge guards. Bare test pads, mounting holes and the three bottom DNP encoder components are excluded from assembly purchasing and paste. Copper, masks, outline and drill bytes remain identical to the upstream native exporter. `artifacts/engineering-fixes/upstream-native-gerbers.zip` is retained for diagnosis; the default archive and the separate order-review CAM both pass their independent audits.

The actual drill/outline files verify the specified 35 mm square and (±13, ±13) Ø3.2 mm mounting holes. Source, placement and Gerber copper agree. Current counts: 427 trace records, 253 vias, 35 grounded regions; 50 physical net groups connected. Native DRC: zero errors/warnings. Placement orientation advice remains visible and is accepted only when every full flagged-component diagnostic is a recognized passive-orientation suggestion and placement DRC is clean.

| Required check | Result | Evidence |
|---|---|---|
| all_resistor_edge_clearances | PASS | `artifacts/validation-resume/all_resistor_edge_clearances.txt` |
| typescript | PASS | `artifacts/validation-resume/typescript.txt` |
| drc | PASS | `artifacts/validation-resume/drc.txt` |
| connectivity | PASS | `artifacts/validation-resume/connectivity.txt` |
| fitted_JST_and_actual_drills | PASS | `artifacts/validation-resume/fitted_JST_and_actual_drills.txt` |
| exact_mounts_and_actual_drills | PASS | `artifacts/validation-resume/exact_mounts_and_actual_drills.txt` |
| native_json_checks | PASS | `artifacts/validation-resume/native_json_checks.txt` |
| native_netlist | PASS | `artifacts/validation-resume/native_netlist.txt` |
| native_pin_specification | PASS | `artifacts/validation-resume/native_pin_specification.txt` |
| native_source | PASS | `artifacts/validation-resume/native_source.txt` |
| native_schematic-placement | PASS | `artifacts/validation-resume/native_schematic-placement.txt` |
| native_placement | Reviewed orientation advisories; placement DRC clean | `artifacts/validation-resume/native_placement.txt` |
| strict_Circuit_JSON_schema | PASS | `artifacts/validation-resume/strict_Circuit_JSON_schema.txt` |
| USB_coupled_copper_and_ground_reference | PASS | `artifacts/validation-resume/USB_coupled_copper_and_ground_reference.txt` |
| schematic_geometry_ERC | PASS | `artifacts/validation-resume/schematic_geometry_ERC.txt` |
| every_trace_review | PASS | `artifacts/validation-resume/every_trace_review.txt` |
| reference_feedback | PASS | `artifacts/validation-resume/reference_feedback.txt` |
| gerber_shorts | PASS | `artifacts/validation-resume/gerber_shorts.txt` |
| copper_widths | PASS | `artifacts/validation-resume/copper_widths.txt` |
| full_independent_CAM | PASS | `artifacts/validation-resume/full_independent_CAM.txt` |
| native_circular_keepout_regression | PASS | `artifacts/validation-resume/native_circular_keepout_regression.txt` |
| actual_via_drills_and_JLCPCB_clearances | PASS | `artifacts/validation-resume/actual_via_drills_and_JLCPCB_clearances.txt` |
| oscillator_layout | PASS | `artifacts/validation-resume/oscillator_layout.txt` |

## Remaining supplier and hardware blockers

JLCPCB must confirm exact stock/quote, pickup datums, pin 1/polarities and rotations, specified copper/plating/stackup, 100 µm stencil/reflow and the three filled/capped/planarized exposed-pad vias. The eight USB shell through-hole joints use the reference part’s 0.7 mm stakes in a 1.6 mm PCB; JLCPCB must quote and confirm a suitable top-side secondary solder process. No bottom-side fitted parts or bottom paste are specified. The mating JST-SH pigtail and motor lead termination need supplier/assembler confirmation; the factory motor has bare leads.

Firmware, USB boot/data, 15 V PD negotiation, host-only regulator headroom, isolation/backfeed, current accuracy, regulator stability, switching/sense/ground behavior, temperature/thermal operation, buzzer/LEDs, motor regeneration and EMC need prototype bench validation. Real plugs, fastener SKU/tolerances, thread engagement, spacing/underside clearance and the rear motor/adapter must be checked physically. The manufacturer drawing supplies front mounting dimensions only. No rear compatibility, supplier order approval or production release is claimed; no order/payment has been submitted.
