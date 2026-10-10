# Current outer-layer routing review

Final saved source SHA256`6ee4720f90233844e02e207973f481f5ac5da1e55ca5bc92325e957412b3959d`. Main motor/PD width≥0.45 mm on top/bottom only; sense≥0.30 mm on outer layers. Short native driver/USB escapes and resistor-only leaves are individually proved and checked; no thermal arithmetic waives the main rule. Actual Gerber/drill topology independently passes source/copper agreement, shorts/opens and available series-via transitions.

- A_PLUS: main minimum 0.450 mm; total branched vias 1.
- A_MINUS: main minimum 0.450 mm; total branched vias 1.
- B_PLUS: main minimum 0.450 mm; total branched vias 2.
- B_MINUS: main minimum 0.450 mm; total branched vias 3.
- PD_VBUS: main minimum 0.450 mm; total branched vias 3.
- SENSE1: main minimum 0.300 mm; total branched vias 2.
- SENSE2: main minimum 0.300 mm; total branched vias 0.

Total branched via counts differ from series-path transitions; see`service-outer-power-cam.json`. Motor phases retain nonzero vias and are not claimed via-free. RP SENSE1/2 are 2.099/2.098 mm,0.30 mm top, no sense vias. Its single-inner-plane/full-barrel DC return screen is in`artifacts/engineering/independent-sense-return-review.json`; switching/thermal/current balance still needs measurement. CH sense forward copper retains its separately reported trace/barrel screen; ground return is not inferred from that sum. The native router/FreeRouting attempts and explicit local repairs are recorded; diagnostics do not constitute acceptance.
