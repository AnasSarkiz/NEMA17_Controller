# NEMA14_CH32X035G8U6 1.11.0

**CAD qualified for hardware-prototype publication and JLCPCB engineering/order review.** All 50 physical nets are connected. Native DRC reports zero errors and warnings. All 23 qualification checks ran: 22 returned zero; the remaining command returned component-orientation advice with zero placement DRC errors/warnings. Default and order-review CAM audits pass.

35 × 35 × 1.6 mm, four layers. Four NPTH mounting holes are exactly (±13, ±13), Ø3.2 mm in actual Circuit JSON and Excellon drills. Minimum via drill/pad is Ø0.30/Ø0.45 mm. Upright GCT USB4145 sockets occupy opposite edges; the defined 10 mm cable housings have 23.3 mm nominal clearance. The model screens maximum Ø6 × 3 mm screw heads within a Ø6.4 mm envelope and an Ø6 mm tool path.

All 61 fitted parts are TOP SMT. The bottom AS5600 and two capacitors are doNotPlace; six separate top test pads remain bare. Exact source components, ports, nets and traces match GitHub baseline a342a888. USB/PD, JST-SH A+/A−/B+/B− wiring, TMP102, status/power LEDs and buzzer are retained.

[Current review and checks](docs/opposite-edge-review.md) · [Qualification](artifacts/resume-validation.json) · [Connectivity](artifacts/physical-connectivity.json) · [JLCPCB review package](artifacts/jlcpcb-review/JLCPCB-OrderReview.zip) · [Six-sheet schematic PDF](artifacts/schematic-a4.pdf) · [Nominal mechanical screen](artifacts/mechanical/opposite-edge-fit.png).

Supplier stock, CPL pickup/polarity confirmation, thermal-via filling/capping, USB shell secondary soldering, and real cable/fastener tolerances need confirmation. Firmware, electrical/thermal bench testing, rear motor fit, and encoder shaft/magnet/air gap remain unverified. No order or payment was submitted.

Version 1.11.1 corrects generated order instructions and preview captions for the opposite-edge upright USB-C arrangement. CPL guidance now uses the native land-pattern datum and requires supplier pickup confirmation. The qualified copper, footprints, drill files and frozen board hash are unchanged.
