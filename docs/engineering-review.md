# CH32X035 engineering review — 2026-10-08

This is the **NEMA14_CH32X035G8U6** project in the historically named
`NEMA17_Controller` GitHub repository. The target is only STEPperONLINE
**14HM11-0404S**. It remains a two-layer, 35 × 35 mm, top-assembly engineering
prototype. Physical tests, firmware and rear mounting qualification have not
been performed. This report does not authorize ordering or production.

## Findings and corrections

| Severity | Evidence and consequence | Disposition |
| --- | --- | --- |
| Critical | CH224K physical pin 8 was directly connected to 15 V although WCH v1F specifies a 13.5 V absolute limit and a series resistor when used. | Changed to manufacturer section 5.5 PD-only circuit: pin 8 explicitly NC, chip DP/DM tied together on isolated `PD_LEGACY_DATA`, connector D+/D− remain NC. |
| Major | A4988 ±20 µA logic-input leakage through original 100 kΩ pulls permits a 2 V error. Disabled enable/sleep states were not guaranteed at 3.3 V. | Both pulls changed to 10 kΩ genuine C25804. Worst leakage drop is 0.2 V: enable ≥3.1 V, sleep ≤0.2 V at nominal rail. |
| Major | A4988 REF input ±3 µA acting through 39 kΩ/10 kΩ yields up to 23.88 mV offset. | Changed to exact native 3.9 kΩ C23018 / 1 kΩ C441922, preserving approximately 0.6735 V and 0.3508 A nominal. Thévenin resistance falls from 7.96 kΩ to 796 Ω; leakage shift falls to 2.39 mV. |
| Major | Previous sense-net copper lengths were 19.70 and 21.77 mm, with distant resistor ground returns. | Resistors moved immediately north of driver; saved top SENSE paths are approximately 2.642 mm each before safe widening. Native land patterns are unchanged. Ground returns join grounded local pours and driver star/exposed-pad network; this is not a four-terminal resistor measurement. |
| Major | MCU bypass was distant from its actual physical VDD pin; driver charge-pump/local power paths depended on arbitrary global routing. | Moved MCU/driver/regulator bypass parts. Frozen local top paths: MCU bypass 1.299 mm, driver logic 1.400 mm, CP1/CP2 1.512/1.761 mm, VCP 2.597 mm, VREG 2.296 mm, local VBB capacitors 2.461/3.372 mm, LDO output bypass 2.149 mm. Added a second genuine 100 nF, 50 V C14663 capacitor for the second VBB input. |
| Major | The selected original small aluminum bulk capacitor had an unqualified chopping-current ripple budget. | Replaced with exact native Panasonic EEEFPV101XAP, C178585, 100 µF/35 V, 0.60 Arms at 100 kHz/105 °C, 6.3 × 7.7 mm. Pads and polarity match the original. Manufacturer ripple evidence is recorded in `component-evidence.md`; effective sharing and temperature remain bench measurements. |
| Major | DATA/VM inputs previously received externally powered dividers before the MCU rail; WCH limits GPIO voltage to VDD+0.3 V without a retrieved injection allowance. | Replaced host divider with exact native MMBT3904 transistor sensing and added qualified powered-off-protected SN74CBTLV1G125DCKR, OE pull-up/firmware enable, output bleed and local bypass for VM. Fast rail collapse and intermediate supply behavior remain a qualification gate below. |
| Major | Independent actual CAM found a floating GND fragment despite logical connectivity passing, and the initial LDO heat-pour records omitted the required `shape: 'brep'` discriminant. | Added 0.15 mm minimum-neck splitting and mapped-GND-pad/anchored-barrel filtering; corrected heat-pour shape/mask fields and verified LOGIC_IN net IDs. Actual Gerber copper is independently rechecked; source geometry checks alone are insufficient. |
| Major | Original Gerbers put bare interfaces into automatic assembly files and placed paste over plated holes/bottom shield slots. | Bare interfaces are now `doNotPlace`; they retain copper/drills/mask. The corrected assembly/paste process, thermal-via process and independent CAM result are documented in `manufacturing-review.md`. |
| Major / qualification | Cached supplier metadata identifies the exact HT7533-1 variant as 30 V/100 mA; primary Holtek input, tolerance, stability and thermal limits could not be established. | Retained HT7533-1 after correcting the load assumptions and improving local copper. It is a prototype qualification blocker; no claim of verified voltage/thermal margin is made. Obtain the exact Holtek datasheet and measure worst-case mounted temperature/transients before release. |
| Major / qualification | Allegro's ±5% current error is specified at VREF = 2 V, not the approximately 0.6735 V used here. | Removed the misleading qualified-maximum interpretation. Nominal current stays below the motor's 0.40 A rating; actual phase-current waveform must be measured across DAC points, temperature and supply. See `motor-compatibility.md`. |
| Major / qualification | Front 26 mm motor threads do not prove a rear mounting interface. | Exact STEP-based carrier/insulation proposal and measurements are in `mechanical-fit.md`; no motor drilling/end-cap screw reuse is authorized. |

## Electrical operation and physical pins

The two USB-C ports have independent purposes. `J_PD` supplies the motor bus;
`J_DATA` connects the computer USB PHY and also supports logic-only power.
Two Schottky diodes OR these sources into `LOGIC_IN`; there is no intentional
conductive 15 V path into host VBUS. The actual imported connector mating
planes both face outward at the same +Y board edge (Y=17.5 mm). PD is at X=−5.3 mm and DATA at X=+5.3 mm. The 10.6 mm port-center spacing requires compact cable overmolds no more than 10 mm wide as a clearance-screening gate; verify simultaneous straight insertion, retention, carrier/screw clearance and bend access with actual selected cables.

CH224K CFG1/2/3 = 0/1/1 requests 15 V. PG is open-drain **active low**, pulled
to 3.3 V. PG alone does not establish that the measured bus equals 15 V.
The VDD feed remains 1 kΩ with local 1 µF bypass. At 15 V and 3.24 V shunt,
the resistor dissipates approximately 0.138 W; at a 15.75 V screening input,
approximately 0.157 W. The exact 0.25 W resistor needs its temperature/pulse
derating checked; sustained 20 V operation is not approved.

MCU physical pins 2/29 are VDD/GND, 5/6 STEP/DIR, 7 PG, 8 DATA_PRESENT,
9 VM_SENSE, 14/15 ENABLE_N/SLEEP, 24/25 debug clock/data, 26/27 USB D−/D+.
Pin 8 PA3 must be a **digital host-presence input** because ADC channel 3 is
unavailable on some WCH lots. Host VBUS now drives a MMBT3904 base through
10 kΩ; its emitter is grounded and its collector is pulled only to V3V3 through
10 kΩ. **DATA_PRESENT is active low**: low means a host supply is present.
Verify low/high thresholds across the selected transistor and MCU limits.
Physical pin 18 PB7 is now VM_ENABLE_N; high disables the analog switch.

A4988 physical pin 18 is GND, not NC, and the exposed pad is grounded.
MS1/MS2/MS3 high selects 1/16 microsteps. RESET high permits operation;
ENABLE_N high and SLEEP low prevent output drive before firmware. ROSC grounded
uses the manufacturer's fixed off-time/mixed-decay option. Required STEP high
and low times are each ≥1 µs, control setup/hold ≥200 ns, and sleep-release delay
≥1 ms. Start with ≥2 µs STEP pulses and ≥2 ms sleep delay.

Firmware must initialize STEP low, DIR to a known value, enable high and sleep
low before enabling outputs. Check measured VM against a conservative 15 V
acceptance window; reject a 5 V fallback and remain disabled. On USB loss,
command timeout, undervoltage, overvoltage or reset, disable outputs. A4988's
8 V minimum operating supply means PD 5 V fallback does not satisfy motor
operation, although the logic can remain powered.

| Connection state | Expected behavior to validate |
| --- | --- |
| Data only | 3.3 V logic and ROM USB programming; motor bus absent, outputs disabled. |
| PD only | 15 V requested, 3.3 V logic powered; outputs remain disabled without a valid command/firmware. |
| Both | PD normally supplies logic through OR diode; computer VBUS remains its own 5 V domain. |
| PD source lacks 15 V | Measure fallback; firmware refuses motor enable outside accepted VM range. |
| Reset/power transition | 10 kΩ hardware defaults persist; check transient GPIO/rail waveforms and absence of unintended steps. |

## LDO decision and thermal screening

WCH typical MCU current is 4.2 mA at 3.3 V/48 MHz with all peripheral clocks
enabled; Allegro specifies 8 mA maximum driver logic current. These establish
approximately 12.2 mA before GPIO loads, REF divider and USB operating effects.
The reduced-impedance divider adds about 0.674 mA; active 10 kΩ enable/sleep
pulls and PG can add about 0.99 mA. The active-low host collector and enabled
VM switch OE pull add approximately 0.33 mA each; include the selected switch
supply current in the measured load. **15 mA is a planning scenario, not a measured load or a
guaranteed system maximum.** A 25 mA screening scenario covers additional
uncertainty but must be validated under the actual firmware and USB modes.

Ignoring the input-diode drop conservatively, `(15−3.3)×I` is 0.1755 W at
15 mA or 0.2925 W at 25 mA. At assumed 60 °C local ambient and assumed
100/150/250 °C/W, estimated junction temperatures are respectively
77.6/86.3/103.9 °C at 15 mA and 89.3/103.9/133.1 °C at 25 mA.
These theta values and 125 °C screening limit are **not Holtek specifications**.
The reproducible PCB Designer calculator commands/results are in
`artifacts/engineering/ldo-thermal-screening.json`.

The old 40–70 mA cases were conservative allocation scenarios, not realistic
typical CH32 measurements; they alone do not prove an electrical defect.
Retention preserves the low component count and avoids unnecessary switching
noise on this low-current board. Additional masked VIN/tab
copper improves the physical heat path without claiming a verified thermal
resistance. The saved same-edge layout retains approximately 16.38 mm² of masked top
LOGIC_IN tab copper. No bottom region survives the final foreign-copper
clearance screen; no thermal resistance is claimed from this area.
The attempted external via candidates did not clear native copper, so no
additional thermal via was forced into a solder pad or narrow clearance. Motor-case heating, cable-only startup, diode
drop, output-capacitor stability and regeneration must be checked physically.
If the measured load/temperature exceeds the exact Holtek derated allowance,
replace this supply with a qualified buck architecture before further use.

## Analog, protection and routing limits

VM first enters a 100 kΩ/10 kΩ divider on VM_DIV. A native SC70-5
SN74CBTLV1G125DCKR bus switch feeds VM_SENSE only when its OE_N is low.
OE_N has a 10 kΩ pull-up to V3V3 and is controlled by PB7 VM_ENABLE_N.
The output has an additional 10 kΩ ground bleed and the existing 10 nF filter.
Enabled, the nominal transfer is **VM/21**, approximately 0.714 V at 15 V,
with approximately 4.76 kΩ Thévenin resistance before switch on-resistance.
Firmware must initialize VM_ENABLE_N high, enable measurement only after
V3V3 is established, wait at least 0.5 ms, multiply ADC volts by approximately
21 and calibrate resistor/switch/ADC errors. Keep slow acquisition and disable
the switch for reset, sleep and a detected rail fault. The datasheet Ioff
maximum of 10 µA at VCC=0 gives at most approximately 0.101 V through the
1%-tolerance 10 kΩ output bleed in the steady off state; it does not establish
safety through every brownout trajectory.

The SMF18A designation is not a guaranteed 18 V clamp. Cached exact-CID supplier metadata gives 29.2 V at 6.8 A, 10/1000 µs, leaving little margin to the supplier-listed 30 V LDO rating before diode drop; cable/PCB inductive overshoot is not included. Exact selected TVS
surge and repetitive-energy limits remain unresolved. A 35 V divider arithmetic
envelope is not permission to operate the motor bus/LDO at 35 V. The intended
supply remains 15 V; mechanical load inertia and regenerated stopping energy
are unspecified. Use a scope to check VM and LOGIC_IN peaks, and add qualified
bus-clamp/braking hardware if measurements require it.

All fitted land patterns remain exact supplier imports. Global autorouter
results are retained separately from accepted routing. Critical motor escapes
and local support routes are explicitly saved before global routing; selected
repairs and copper widening are recorded. USB is full-speed, with moved ESD
protection and verified connectivity, but the two-layer reference/impedance and
assembled eye/enumeration performance are not physically qualified. Do not
interpret whole-net copper totals with duplicated Type-C contacts as pair skew.

See `manufacturing-review.md`, machine-readable validation artifacts and
`bringup-checklist.md` for the executed software checks and remaining physical
gates. Manufacturer-authored evidence and unresolved exact-part specifications
are in `component-evidence.md`; rear mounting is separately qualified by the
mechanical report.

## Input protection and remaining power-sequence qualification

The original divider-fed MCU inputs could be present before V3V3 rose. WCH
CH32X035 V2.3 Table 3-1 limits GPIO voltage to **VDD+0.3 V**, and no applicable
positive injection-current allowance was retrieved. The recorded original
conditional clamp-current calculation is diagnostic evidence, not permission
for current injection.

The saved source now uses the exact native C94514 MMBT3904-7-F with a 10 kΩ
host-VBUS base resistor, grounded emitter and 10 kΩ collector pull-up to V3V3.
This isolates the MCU host input from a direct VBUS divider and reverses host
presence to active low. VM uses genuine C131992 SN74CBTLV1G125DCKR, specified
powered-off Ioff, 10 kΩ output bleed, 10 nF output filter, 10 kΩ OE_N pull-up,
MCU pin 18 control and a local 100 nF C14663 supply bypass. All five added
parts have native imported footprints and CAD models. Exact manufacturer
conditions and pin maps are recorded in `component-evidence.md`.

**A transition qualification gate remains.** TI's Ioff condition at VCC=0
is not a guarantee of behavior throughout an intermediate supply below the
specified 2.3 V operating range. The output capacitor can retain a previous
measurement after the switch opens: 10 nF × 10 kΩ gives 100 µs nominal decay
and approximately 111.1 µs using 10% C / 1% R screening tolerances. A
hypothetically instantaneous V3V3 collapse can therefore briefly leave
VM_SENSE above VDD+0.3 V. The OE pull-up and correct firmware sequence improve
startup; they do not prove an arbitrary brownout waveform safe.

Before release, capture V3V3, OE_N and both inputs simultaneously, including
**Vpin−V3V3**, during DATA-only, PD-only, both cable orders, 5 V fallback,
attach/removal, reset, brownout and intended temperatures. Verify host
transistor saturation/leakage and ghost-rail voltage against exact guaranteed
conditions. Verify ADC acquisition/settling and disable timing. If measured
trajectories violate the pin limit or cannot be bounded by guaranteed device
behavior, add qualified supervision/clamping or change the protection
architecture before further release. Absence of visible damage and successful
USB enumeration do not clear this gate. See
[power-sequencing-audit.json](../artifacts/validation/power-sequencing-audit.json).

## Same-edge USB placement and rerouting

Both untouched C165948 connectors now share +Y, with CAD anchors X±5.3 mm,
Y12.1499711 mm, PCB rotation180° and CAD rotation0°. The native mouth planes
are Y17.5 mm. Four Ø5.4 mm circular mounting keepouts preserve the full
head allowance. The supplier courtyard rectangles remain intact; only their
empty-area port conflicts are explicitly excluded. An independent native
16-pad-per-connector and hashed OBJ triangle projection guard measures about
0.446 mm copper and 0.530 mm body clearance to those circles. Exact native
STEP collisions are reviewed separately. Physical cables must have maximum
10 mm overmold width; 12 mm overmolds cannot fit at 10.6 mm port pitch.

The fresh tscircuit local autorouter attempt did not settle within its 90-second
deadline; no output from that attempt was accepted. Official Freerouting
2.0.1 completed the native-footprint DSN in ten passes, preserving 12 short
critical local connections, 13 MCU/driver fanouts and four motor escapes.
The saved SES, fixed-route source and 189 exact copper adjustments reproduce
the accepted routes. Final saved-board native checks report zero errors and
one genuine generic-NPN ERC warning; independent copper connectivity joins
all 37 active nets. The remaining manufacturing and hardware qualification
gates still apply. Earlier opposite-edge review artifacts are preserved under
`artifacts/superseded-opposite-edge-review/` and are superseded.

A specific ghost-host boundary also requires testing: PD-only ROM or a USB pull-up may drive a rail-steering ESD path into unpowered DATA_VBUS, potentially asserting the low-threshold NPN detector without an external host. The exact selected ESD primary topology and actual voltages/currents are not yet established; this is a conditional circuit risk, not a measured outcome. Test PD-only reset/ROM/pull-up, host at 0 V connection, DATA_VBUS ghost power and DATA_PRESENT thresholds. Firmware gating does not qualify ROM behavior or a self-triggering detector; stronger guaranteed host-voltage detection or isolation is needed if the boundary fails.
