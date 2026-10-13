# NEMA14 CH32X035 motor controller

35 × 35 mm, four-layer, 15 V USB-PD stepper-controller prototype. Fitted parts populate the top face; LEDs, TMP102 and buzzer remain present. USB-C mouths share the +Y edge. Use two 10 mm cable housings at 12.4 mm pitch and M3 DIN 920 heads ≤Ø4 mm. Mount holes are exactly (±13, ±13), Ø3.2 mm.

The regenerated [JLCPCB order-review package](artifacts/jlcpcb-review/JLCPCB-OrderReview.zip) passes the independent CAM audit. It includes a top-side SMT JST-SH, native supplier BOM/CPL, stencil and assembly maps, plus the eight USB shell joints requiring secondary soldering. Supplier approval of pickup orientation, availability, stencil and thermal-via processing remains required.

See [assembly and harness constraints](docs/top-assembly.md), [functional five-sheet schematic](artifacts/schematic-a4.pdf), [order-review receipt](artifacts/jlcpcb-review/order-review-verification.json) and [current validation](artifacts/resume-validation.json). `assembly-preview.circuit.tsx` is a separate unrouted visual concept. Rear-motor attachment, firmware and bench behavior are unverified.
