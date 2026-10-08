# Electrical design review — CH32X035, 2026-10-08

The saved CH32 board has 44 fitted supplier components, three bare solder
interfaces, two copper layers and top assembly. See [engineering review](engineering-review.md)
for findings, manufacturer evidence and disposition; software checks do not
qualify physical operation.

## Phase current and support circuits

A4988 VREF = 3.3 × 1/(3.9+1) = 0.6735 V; Itrip = VREF/(8 × 0.24 Ω) =
0.3508 A nominal. The exact 0.24 Ω, 1%, 125 mW sense resistors dissipate about
29.5 mW at nominal peak. Exact 3.9 kΩ/1 kΩ imports reduce REF source resistance
to approximately 796 Ω and the specified ±3 µA REF-leakage shift to 2.39 mV.
A rail/resistor/leakage-only screening corner is approximately 0.3792 A, but
Allegro does not specify trip accuracy at this low VREF. **There is no qualified
maximum phase-current guarantee here.** Measure all relevant DAC points and
temperatures, keeping actual peak ≤0.40 A. The former provisional ±5% driver
allowance is removed.

Both enable/sleep pulls are 10 kΩ: the manufacturer's ±20 µA input leakage
causes at most 0.2 V through each pull instead of 2 V through the old 100 kΩ.
Sense resistors, charge-pump and local bypass parts are placed close to their
actual native driver pins. Saved SENSE paths are approximately 2.642 mm each;
CP1/CP2 are 1.512/1.761 mm. Both VBB inputs have local 100 nF/50 V capacitors.
The bulk capacitor is exact Panasonic C178585 EEEFPV101XAP, 100 µF/35 V,
rated 0.60 Arms at 100 kHz/105 °C; actual ripple sharing and temperature need
measurement.

## Copper review

Power tracks are widened only when native pads, vias and foreign tracks retain
at least 0.15 mm clearance. Centerlines and supplier land patterns are retained.
`artifacts/power-copper-adjustments.json` records widening;
`artifacts/supplier-routing-adjustments.json` replays all accepted copper from
the saved SES import. Ground fills and masked LOGIC_IN regulator-tab regions
retain 0.20 mm foreign clearance. No unconnected copper islands are accepted.

| Copper | Saved CH32 width / screening |
| --- | --- |
| Motor outputs | 0.300–0.348 mm; screened at 0.40 A peak |
| Sense tracks | 0.351 mm; screened at 0.40 A peak |
| PD supply | 0.30–0.60 mm; 0.75 A conservative input budget |
| Logic supply | 0.16–0.30 mm; 0.15 A screening allocation, not measured CH32 demand |
| Ground | 0.16–0.45 mm tracks plus parallel connected ground fills |
| USB and other signals | 0.16 mm; width alone does not establish impedance or signal integrity |

The screening requires at least 35 µm finished external copper, 1.6 mm FR-4
and 20 µm via-barrel plating. These are fabrication requirements, not measured
board properties. IPC-2221 uses external k=0.048 and a 30 °C rise screen.
The saved isolated non-ground maximum estimate is approximately 5.21 °C at
its assigned conservative current budget. Motor/enclosure heat, pulses, neck
heat spreading and plane sharing are not included. Ground traces covered by
same-net pours are parallel paths; their isolated-track estimates do not
predict actual plane temperature. See the actual segment/via report in
`artifacts/trace-width-review.json`.

## PD and input protection

CH224K requests 15 V with CFG1/2/3 = 0/1/1, and PG is active low. Its physical
VBUS pin 8 is explicitly NC in the manufacturer PD-only configuration; chip
DP and DM are tied together separately from connector contacts. R_PD is a
native 1 kΩ/0.25 W resistor. It dissipates approximately 0.138 W at 15 V;
20 V sustained operation is not approved.

Host sensing uses a native MMBT3904 NPN: 10 kΩ base feed from DATA_VBUS,
grounded emitter and 10 kΩ collector pull-up to V3V3. **DATA_PRESENT is active
low.** VM uses a 100 kΩ/10 kΩ input divider on VM_DIV followed by genuine
SN74CBTLV1G125DCKR, an OE pull-up/control, local 100 nF bypass, 10 kΩ output
bleed and 10 nF output filter. Firmware controls PB7 VM_ENABLE_N.

Enabled, the output bleed loads the divider: **VM_SENSE = VM/21 nominal**,
approximately 0.714 V at 15 V with about 4.76 kΩ source resistance. The 1%
resistor-only 35 V arithmetic corner is 1.699 V at the MCU output and 3.240 V
at the disabled switch input. Positive switch on-resistance lowers the
output. The 35 V arithmetic envelope does not approve motor/regulator
operation at 35 V; intended input remains 15 V. Enable measurement only after
V3V3 is valid, wait ≥0.5 ms and calibrate the nominal ×21 conversion.

TI's Ioff guarantee applies at VCC=0. It does not prove every intermediate-VCC
or fast-collapse trajectory safe. The 10 nF/10 kΩ output filter retains a
previous voltage for approximately 100 µs nominal. Scope Vpin−VDD, OE timing,
NPN levels and ghost power; add qualified supervision/clamping if guaranteed
limits or observed waveforms require it. This remains a release gate.

## Power, USB and physical qualification

Two Schottky diodes OR PD and computer sources into the logic regulator;
the bridge draws only from PD_VBUS. Both ports share ground. HT7533-1 is
retained after correcting the load assumptions: WCH lists 4.2 mA typical
MCU current with all peripheral clocks; A4988 lists 8 mA maximum logic current.
15/25 mA are planning scenarios, not measured bounds. At 15 V they imply
approximately 0.176/0.293 W regulator dissipation before diode-drop credit.
Exact Holtek tolerance/stability/thermal limits and mounted tests remain
required. The same-edge layout retains approximately 16.38 mm² of masked top tab copper; no legal bottom thermal region remains after rerouting;
no additional via was forced where native clearances did not permit it.

USB ROM programming is wired through PC17/D+ BOOT detection and the Data port.
Firmware must use 3.3 V PHY mode. Enumeration, both Type-C orientations,
repeated flashing and USB performance have not been tested physically. Copper
continuity/short checks do not establish impedance or pair skew; branched
connector/ESD copper totals are not endpoint length matching.

SMF18A is a name, not an 18 V clamp guarantee. Cached exact-CID metadata gives
29.2 V at 6.8 A/10–1000 µs, close to the supplier-listed 30 V LDO limit before
overshoot. Exact pulse/energy limits, capacitor heating, PD startup/inrush,
host backfeed, regenerated stopping energy and hot-motor temperature require
measurement. The front-thread drawing does not prove rear attachment;
validate the proposed insulating carrier against a motor sample.

Follow [bring-up checklist](bringup-checklist.md). No motor-control firmware
or physical test result is supplied. **Manufacturing release remains blocked.**

## USB connector identification and cable access

Both USB-C openings face outward from the same **+Y edge**. **J_PD** is at X=−5.3 mm and supplies motor PD power; **J_DATA** is at X=+5.3 mm and connects the computer/programming interface. Firmware roles and signal pin assignments are unchanged by this placement. The 10.6 mm port-center pitch requires compact overmolds **≤10 mm wide** as a screening gate; verify both selected cables fit simultaneously and clear the carrier, screw heads and bend path before operating the prototype.
