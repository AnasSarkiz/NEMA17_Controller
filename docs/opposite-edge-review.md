# NEMA14 CH32 — current engineering review

**CAD qualified for hardware-prototype publication and JLCPCB engineering/order review.** All 50 physical nets are connected. Native DRC reports zero errors and warnings. All 23 qualification checks ran: 22 returned zero; the remaining command returned component-orientation advice with zero placement DRC errors/warnings. Default and order-review CAM audits pass.

35 × 35 × 1.6 mm, four layers. Four NPTH mounting holes are exactly (±13, ±13), Ø3.2 mm in actual Circuit JSON and Excellon drills. Minimum via drill/pad is Ø0.30/Ø0.45 mm. Upright GCT USB4145 sockets occupy opposite edges; the defined 10 mm cable housings have 23.3 mm nominal clearance. The model screens maximum Ø6 × 3 mm screw heads within a Ø6.4 mm envelope and an Ø6 mm tool path.

All 61 fitted parts are TOP SMT. The bottom AS5600 and two capacitors are doNotPlace; six separate top test pads remain bare. Exact source components, ports, nets and traces match GitHub baseline a342a888. USB/PD, JST-SH A+/A−/B+/B− wiring, TMP102, status/power LEDs and buzzer are retained.

[Current review and checks](opposite-edge-review.md) · [Qualification](../artifacts/resume-validation.json) · [Connectivity](../artifacts/physical-connectivity.json) · [JLCPCB review package](../artifacts/jlcpcb-review/JLCPCB-OrderReview.zip) · [Six-sheet schematic PDF](../artifacts/schematic-a4.pdf) · [Nominal mechanical screen](../artifacts/mechanical/opposite-edge-fit.png).

Supplier stock, CPL pickup/polarity confirmation, thermal-via filling/capping, USB shell secondary soldering, and real cable/fastener tolerances need confirmation. Firmware, electrical/thermal bench testing, rear motor fit, and encoder shaft/magnet/air gap remain unverified. No order or payment was submitted.

Frozen board SHA-256: `0d772c1f839f50f30caa512a0dcc58f8ecfa88e35c2e9b44c2422365bc0a8e64`. The native placement log contains eight recognized orientation advisories; informational empty-space data are retained. Publication accepts only this complete recognized class and continues to reject real DRC/CAM or unknown findings. Six guard regression cases pass.

B+ uses 10.847 mm total inner1 copper at 0.30 mm. Its maximum screened rise is 18.91 °C at 0.40 A on 17.5 µm inner copper, below the 30 °C screen. The revised 12 mm phase bound retains the ≥700 mm² connected inner1 ground requirement and all USB/clearance/CAM checks. This is a calculation, not a bench temperature measurement.

| Check | Actual exit code | Evidence |
|---|---:|---|
| all_resistor_edge_clearances | 0 | [log](../artifacts/validation-resume/all_resistor_edge_clearances.txt) |
| typescript | 0 | [log](../artifacts/validation-resume/typescript.txt) |
| drc | 0 | [log](../artifacts/validation-resume/drc.txt) |
| connectivity | 0 | [log](../artifacts/validation-resume/connectivity.txt) |
| fitted_JST_and_actual_drills | 0 | [log](../artifacts/validation-resume/fitted_JST_and_actual_drills.txt) |
| exact_mounts_and_actual_drills | 0 | [log](../artifacts/validation-resume/exact_mounts_and_actual_drills.txt) |
| native_json_checks | 0 | [log](../artifacts/validation-resume/native_json_checks.txt) |
| native_netlist | 0 | [log](../artifacts/validation-resume/native_netlist.txt) |
| native_pin_specification | 0 | [log](../artifacts/validation-resume/native_pin_specification.txt) |
| native_source | 0 | [log](../artifacts/validation-resume/native_source.txt) |
| native_schematic-placement | 0 | [log](../artifacts/validation-resume/native_schematic-placement.txt) |
| native_placement | 1 | [log](../artifacts/validation-resume/native_placement.txt) |
| strict_Circuit_JSON_schema | 0 | [log](../artifacts/validation-resume/strict_Circuit_JSON_schema.txt) |
| USB_coupled_copper_and_ground_reference | 0 | [log](../artifacts/validation-resume/USB_coupled_copper_and_ground_reference.txt) |
| schematic_geometry_ERC | 0 | [log](../artifacts/validation-resume/schematic_geometry_ERC.txt) |
| every_trace_review | 0 | [log](../artifacts/validation-resume/every_trace_review.txt) |
| reference_feedback | 0 | [log](../artifacts/validation-resume/reference_feedback.txt) |
| gerber_shorts | 0 | [log](../artifacts/validation-resume/gerber_shorts.txt) |
| copper_widths | 0 | [log](../artifacts/validation-resume/copper_widths.txt) |
| full_independent_CAM | 0 | [log](../artifacts/validation-resume/full_independent_CAM.txt) |
| native_circular_keepout_regression | 0 | [log](../artifacts/validation-resume/native_circular_keepout_regression.txt) |
| actual_via_drills_and_JLCPCB_clearances | 0 | [log](../artifacts/validation-resume/actual_via_drills_and_JLCPCB_clearances.txt) |
| oscillator_layout | 0 | [log](../artifacts/validation-resume/oscillator_layout.txt) |
