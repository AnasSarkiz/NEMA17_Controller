# CH32 first-prototype bring-up

Use the final source/BOM/CPL/CAM revision together. Record board serial number,
assembly revision, component lot codes, firmware hash, instruments, local/motor
temperatures and measured waveforms. No tests below have been performed on
physical hardware yet. Firmware is not supplied by the hardware project.

1. **Assembly inspection, unpowered.** Check native MPNs and polarity, A4988/
   CH32/CH224 pin 1, bulk capacitor positive pad, Schottky/TVS orientation,
   3.9 kΩ/1 kΩ REF divider, 0.24 Ω sense parts and 10 kΩ default pulls. Confirm
   USB shell slots are manually soldered as specified. Inspect exposed-pad joints
   and the approved filled/capped via process; X-ray hidden pads if possible.
   Verify no bare wire/debug/BOOT interface was machine placed. Inspect switch
   pins 1 OE_N / 2 VM_DIV / 3 GND / 4 VM_SENSE / 5 VCC, NPN pins
   1 base / 2 emitter / 3 collector, and the 10 kΩ OE/output-bleed resistors.
2. **Unpowered shorts and isolation.** Measure PD_VBUS, DATA_VBUS, LOGIC_IN and
   V3V3 resistance to GND in both meter polarities, allowing capacitors to charge.
   Investigate persistent near-zero resistance. Confirm motor wire phase pairs
   are Black/Green and Red/Blue with approximately 25 Ω each; do not infer color
   order from a different motor. Check no PCB copper touches the metal case or
   mounting hardware.
3. **Data-only logic power, motor disconnected.** Use a USB breakout with
   current-limited 5 V supply initially; do not connect a computer until rails
   and no shorts are verified. Begin with a 30–50 mA limit, accounting for input
   capacitor charging. Measure 3.3 V, LOGIC_IN drop and steady current. Scope
   VDD startup and DATA_PRESENT/VM_SENSE input voltages during the ramp. Verify
   ENABLE_N high, SLEEP low and motor outputs inactive before firmware.
4. **Independent CH32 USB ROM programming.** With PD disconnected, hold the
   documented BOOT jumper tying PC17/D+ through 4.7 kΩ to 3.3 V during a cold
   Data-port power connection, then release as required by WCH ISP. Confirm WCH
   ISP enumeration, flash and verify a minimal program; test both USB-C plug
   orientations and repeated reconnects. If ROM entry fails, use the DCK/DIO/
   VDD/GND debug pads and verify the exact WCH boot sequence. RP2040 UF2 steps do
   not apply to this MCU.
5. **Minimal diagnostic firmware.** Initialize driver disabled, STEP low and
   DIR known; configure PA3 digital **active-low** host-presence and PG active-low.
   Initialize PB7 VM_ENABLE_N high before other control changes. Enable the
   VM switch only after V3V3 is valid, wait ≥0.5 ms, use slow ADC acquisition,
   and apply the calibrated nominal ×21 VM conversion. Disable measurement
   before sleep and detected supply faults. Log supply voltage and command timeouts over
   USB. Wait ≥2 ms after sleep release and use ≥2 µs STEP high/low pulses. First
   tests must not automatically enable after reset or USB reconnection.
6. **PD-only power, motor still disconnected.** Use a PD source known to offer
   15 V and a PD analyzer/breakout. Verify requested/actual voltage, PG polarity,
   3.3 V ripple and current. Repeat both Type-C orientations. Test a source
   lacking 15 V: logic may run at fallback voltage but firmware must refuse
   motor enable. Confirm the CH224K unused VBUS pin is physically unconnected.
7. **Both ports and cable transitions.** With a breakout, confirm the host VBUS
   never rises toward PD voltage. Test Data-only, PD-only, both, insertion,
   removal, reset, BOOT, suspend and enumeration. Scope input/3.3 V dips and
   GPIO defaults; watch for backfeed, unintended motor pulses, repeated USB
   reconnects and startup/shutdown input absolute-limit violations. Capture OE_N and
   VM_SENSE against V3V3 during forced brownouts; the 100 µs output-filter
   decay and unspecified intermediate-VCC switch behavior require testing.
8. **Low-speed motor/current test.** Power down before connecting or swapping
   motor wires. Connect Black A+, Green A−, Red B+, Blue B−. Start with slow
   single-step motion, then a gentle acceleration ramp. Measure both chopped
   phase waveforms with a current probe or safe differential sense-resistor
   measurement. A multimeter average is insufficient. Expected formula peak is
   approximately 0.351 A; **measured peak must stay ≤0.40 A** throughout relevant
   DAC points, supply and temperature. Inspect sense-ground noise and current
   offsets. Stop and change current-setting values if limits are exceeded.
9. **Thermal and regeneration qualification.** Record total logic current,
   LDO/driver/bulk temperatures and 3.3 V ripple with USB traffic, enabled hold,
   acceleration, reversal and brief current-limited stall. Repeat against the
   actual hot motor using the insulating carrier/standoffs. Compare measured
   temperatures/current/VIN against the exact Holtek derated specifications;
   obtain these before accepting LDO margin. Capture VM/LOGIC_IN overshoot at
   cable insertion, emergency stop and commanded deceleration with the intended
   mechanical load. Compare with exact TVS/diode/capacitor/driver limits and
   assess bulk ripple/ESR heating. No acceptable temperature/energy limit may
   be invented from a generic package or TVS name.
10. **Mechanical and endurance.** Validate the carrier dimensions, rear-face
    protrusions, screw engagement, insulating air gap, capacitor height, cable
    access and wire strain relief against the exact motor. Do not attach to
    undocumented rear threads/end-cap screws. After initial electrical gates,
    run an extended warm operating cycle with logged USB errors, current,
    missed-step behavior and temperatures. Mark the prototype qualified only
    for the tested operating envelope; production remains a separate decision.

For every stage record pass/fail, actual measured values, oscilloscope captures
and the corrective action. Stop if a rail, current, temperature or component
absolute maximum is exceeded, or if an unexpected output drives the motor.

## Sequencing acceptance gate after hardware correction

- [ ] Qualify the implemented native NPN/CBTLV protection in `engineering-review.md`, including fast collapse and intermediate switch supply behavior. Capture simultaneous rail and DATA_PRESENT/VM_SENSE voltages during cable attach/removal and all power orders, evaluate Vpin−VDD, ghost power and source currents against guaranteed limits. Resistor-limited injection without a manufacturer allowance or qualified hardware protection is not an accepted pass. See `artifacts/validation/power-sequencing-audit.json`.

- [ ] **ROM/pull-up ghost-VBUS test:** with PD power and no powered DATA host, exercise reset/ROM USB and deliberately enable the USB pull-up in test firmware. Measure DATA_VBUS and DATA_PRESENT before attaching any host. Rail-steering ESD diodes may raise the otherwise unpowered DATA rail from D+/D−; determine whether this falsely asserts the active-low NPN detector. Then connect a protected host breakout at 0 V and measure injection/backfeed. Qualify exact ESD topology and thresholds; if false detection or disallowed current occurs, revise hardware VBUS detection/isolation rather than accepting a firmware-only claim.
