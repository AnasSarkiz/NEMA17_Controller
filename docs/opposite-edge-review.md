# NEMA14_CH32X035G8U6 — opposite-edge v1.11.0 draft

**Status: electrically unqualified; not ready for JLCPCB order review, fabrication or publication.**

Frozen Circuit JSON SHA-256: `8a2522a9feb5440f003af73734c87f3c0b27506f1052c12bc4991b42aad42f59`. All 23 required checks ran: 16 returned zero, 7 returned nonzero. Native placement advisories retain their actual exit code; they do not explain the electrical/CAM failures.

The PCB is 35 × 35 × 1.6 mm with four copper layers. Actual JSON and Excellon mount checks pass for four Ø3.2 mm holes at (±13, ±13). Actual via/drill fabrication checks pass the requested Ø0.30 mm drill / Ø0.45 mm pad minima.

USB-C sockets remain upright (+Z) and now occupy opposite edges: J_PD (0.30000000000000027, 15.149999999999999) and J_DATA (0, -15.149999999999999) mm. Defined 10 × 7 × 30 mm housings have 23.300 mm nominal separation. Native part models, with conservative bounds for the invalid GCT STEP solids, pass the nominal head/tool screen for heads ≤Ø6 × 3 mm and a Ø6.4 mm screening envelope. This is model evidence, not measured assemblies or rear-motor fit.

All intended source ports, source nets, source traces and functional component fields match the latest GitHub baseline. This proves electrical intent was retained; physical copper connectivity below is incomplete. TMP102, status/power LEDs, buzzer, driver, flash (RP2040), USB/PD and fitted JST-SH C160390 remain. All 81 RP2040 / 61 CH32 fitted components are TOP SMT; bare TOP pads and the BOTTOM AS5600 plus two doNotPlace capacitors are excluded from the factory placement and paste.

The JST-SH SHR-04V-S harness retains A+, A−, B+, B− pin order. It is not physically interchangeable with the JST-PH connector in Rishabh’s reference. USB schematic and physical-pin checks pass; these do not establish USB/PD bench operation.

## Remaining blockers

- **A_PLUS**: 2 disconnected physical pad groups. See the exact pad lists in [physical connectivity](../artifacts/physical-connectivity.json).
- **A_MINUS**: 2 disconnected physical pad groups. See the exact pad lists in [physical connectivity](../artifacts/physical-connectivity.json).
- **B_PLUS**: 2 disconnected physical pad groups. See the exact pad lists in [physical connectivity](../artifacts/physical-connectivity.json).
- Native DRC records **28 errors**. Open connections and unused/dangling copper must be resolved; no real errors were suppressed.
- USB reference: Insufficient full-width adjacent GND reference usb_coupled_connector_to_ESD_USB_DM 0.999015.
- USB reference: Insufficient full-width adjacent GND reference usb_coupled_ESD_to_MCU_USB_DM 0.992718.
- Failed **every_trace_review**: [actual log](../artifacts/validation-resume/every_trace_review.txt).
- Failed **copper_widths**: [actual log](../artifacts/validation-resume/copper_widths.txt).
- Failed **full_independent_CAM**: [actual log](../artifacts/validation-resume/full_independent_CAM.txt).
- Independent CAM: unassigned-copper-islands (34 islands).
- Independent CAM: physical-netlist-failure.
- JLCPCB stock, pickup/polarity/rotation confirmation, three filled/capped/planarized thermal vias and secondary soldering of eight USB shell joints remain supplier decisions. No order was placed.
- Rear mounting, rear shaft/magnet dimensions, encoder air gap, complete fastener/cable tolerances and bench electrical/thermal/firmware operation remain unverified.

## Current evidence

| Check | Actual exit code | Log |
|---|---:|---|
| all_resistor_edge_clearances | 0 | [log](../artifacts/validation-resume/all_resistor_edge_clearances.txt) |
| typescript | 0 | [log](../artifacts/validation-resume/typescript.txt) |
| drc | 1 | [log](../artifacts/validation-resume/drc.txt) |
| connectivity | 1 | [log](../artifacts/validation-resume/connectivity.txt) |
| fitted_JST_and_actual_drills | 0 | [log](../artifacts/validation-resume/fitted_JST_and_actual_drills.txt) |
| exact_mounts_and_actual_drills | 0 | [log](../artifacts/validation-resume/exact_mounts_and_actual_drills.txt) |
| native_json_checks | 0 | [log](../artifacts/validation-resume/native_json_checks.txt) |
| native_netlist | 0 | [log](../artifacts/validation-resume/native_netlist.txt) |
| native_pin_specification | 0 | [log](../artifacts/validation-resume/native_pin_specification.txt) |
| native_source | 0 | [log](../artifacts/validation-resume/native_source.txt) |
| native_schematic-placement | 0 | [log](../artifacts/validation-resume/native_schematic-placement.txt) |
| native_placement | 1 | [log](../artifacts/validation-resume/native_placement.txt) |
| strict_Circuit_JSON_schema | 0 | [log](../artifacts/validation-resume/strict_Circuit_JSON_schema.txt) |
| USB_coupled_copper_and_ground_reference | 1 | [log](../artifacts/validation-resume/USB_coupled_copper_and_ground_reference.txt) |
| schematic_geometry_ERC | 0 | [log](../artifacts/validation-resume/schematic_geometry_ERC.txt) |
| every_trace_review | 1 | [log](../artifacts/validation-resume/every_trace_review.txt) |
| reference_feedback | 0 | [log](../artifacts/validation-resume/reference_feedback.txt) |
| gerber_shorts | 0 | [log](../artifacts/validation-resume/gerber_shorts.txt) |
| copper_widths | 1 | [log](../artifacts/validation-resume/copper_widths.txt) |
| full_independent_CAM | 1 | [log](../artifacts/validation-resume/full_independent_CAM.txt) |
| native_circular_keepout_regression | 0 | [log](../artifacts/validation-resume/native_circular_keepout_regression.txt) |
| actual_via_drills_and_JLCPCB_clearances | 0 | [log](../artifacts/validation-resume/actual_via_drills_and_JLCPCB_clearances.txt) |
| oscillator_layout | 0 | [log](../artifacts/validation-resume/oscillator_layout.txt) |

[Nominal mechanical screen](../artifacts/mechanical/opposite-edge-fit.png) · [six-sheet schematic PDF](../artifacts/schematic-a4.pdf) · [every-trace inventory](../artifacts/reference-feedback/every-trace-review.csv) · [native manufacturing audit](../artifacts/manufacturing/audit.json)

Gerbers/BOM/CPL/paste/silk were regenerated from this hash and are diagnostic review assets. Their corrected assembly policy does not qualify incomplete copper. Current tscircuit public releases remain v1.10.2. The publication guard must pass before any new release.
