# NEMA14 USB-C PD controller

A two-layer tscircuit **hardware prototype** for the STEPperONLINE 14HM11-0404S, using **CH32X035G8U6**, two separate USB-C receptacles, and four mounting holes. Manufacturing release is blocked until the motor's rear geometry is verified and the prototype is tested. See `artifacts/drc-report.json` for the current routed-board checks; a generated Gerber ZIP is not a release approval.

| Item | Design |
| --- | --- |
| Motor | 35 × 35 × 28 mm, bipolar, 0.9°, 0.4 A/phase, 10 V, 11 N·cm — specifications from the supplied product listing |
| Board | 35 × 35 mm, two copper layers, 1.6 mm FR-4; all components assembled on top |
| USB-C placement | PD opening flush with left edge; data opening flush with right edge; pads and shell anchors inside PCB |
| Mounting | Four Ø3.2 mm non-plated holes at (±13, ±13) mm; 26 mm square pitch; 5.4 mm square copper/component exclusions |
| MCU | CH32X035G8U6, QFN-28 plus grounded exposed pad; internal oscillator |
| Power USB-C | CH224K fixed request for **15 V**: CFG1 low, CFG2/CFG3 high |
| Computer USB-C | USB 2.0 full-speed D+/D− and two 5.1 kΩ CC pull-downs; USBLC6-2SC6 ESD protection |
| Driver | A4988SETTR-T, fixed 1/16 microsteps, regulated phase current |
| Current | 0.351 A nominal peak; 0.24 Ω sense resistors; 39 kΩ/10 kΩ VREF divider |
| Motor connection | Four plated wire-solder holes: A+, A−, B+, B− |
| Programming | Data USB-C via ROM ISP with 4.7 kΩ BOOT jumper; WCH-LinkE debug pads retained |
| Tools | tscircuit 0.0.2764, CLI 0.1.2261; latest npm versions at setup time, pinned in lockfile |

## View and work on the design

```sh
cd /workspace/NEMA17_Controller
npm ci --legacy-peer-deps --cache /workspace/.npm-cache
npm run dev
npm run check
```

`npm run dev` starts the tscircuit editor. The editor source is `src/board.tsx`; the final, saved copper is `artifacts/board.circuit.json`. Editor autorouting can produce different traces; **do not replace the checked copper without rerunning DRC**. The original tscircuit autorouting, including its diagnosed violations, is retained as `artifacts/autorouted.circuit.json` for comparison.

The routing workflow is recorded in `docs/routing.md`. Render the saved final layout with `npm run render`; this preserves routes. `npm run autoroute` runs tscircuit's local autorouter afresh. The final fallback uses freerouting 2.0.1 and the physically accurate DSN exporter in `scripts/export-supplier-router.py`; both the DSN and SES are saved. Checks run against actual copper, not the existence of a server or a generated file.

## Electrical choices

The A4988 regulates coil current, so 15 V supply does not apply a constant 15 V to the 10 V-rated windings. VREF = 3.3 × 10/(39+10) = 0.6735 V; I_peak = VREF/(8 × 0.24 Ω) = 0.3508 A. The tolerance/engineering allowance estimates 0.3815 A; current and temperature must be measured on a prototype. The motor has 400 full steps/revolution, giving 6,400 commanded microsteps/revolution.

The motor bridge draws only from `PD_VBUS`. Two B5819W Schottky diodes OR `PD_VBUS` and `DATA_VBUS` into a 30 V-rated HT7533-1 3.3 V regulator. This lets the MCU enumerate from the computer alone and prevents 15 V backfeeding into the computer's VBUS. Both ports share signal ground. The linear regulator supplies only logic; motor current bypasses it. Driver SLEEP has a pull-down and ENABLE_N a pull-up, so the bridge remains disabled until firmware deliberately enables it.

Use a USB PD supply advertising a 15 V PDO. The CH224K requests 15 V; it cannot force an unsupported supply to deliver it. CH224K PG is an **active-low** good-power indication. Firmware must also check measured motor voltage before enabling the bridge. DATA_PRESENT permits USB attachment only when computer VBUS is present. See `docs/firmware-interface.md`; no USB motor-control firmware or physical enumeration result is claimed by this hardware-only prototype.

## Rear mounting decision

The supplied listing establishes the motor envelope; it does **not** establish rear screw threads or rear-hole pitch. The [manufacturer drawing](https://www.omc-stepperonline.com/download/14HM11-0404S.pdf) confirms 26 ± 0.2 mm pitch and four M3 threads, minimum 4 mm depth, on the front mounting face; it does not dimension rear attachment holes. The four 26 mm-spaced board holes are provisionally suitable for a separate rear adapter/standoff plate. **They are not asserted to match the motor's rear screws. Do not replace motor end-cap screws or drill the motor from these files.** The mounting drawing explicitly marks the unresolved fit. Rear installation also needs an insulating gap and clearance for motor wiring, any rear shaft/boss, and screw heads. Use an adapter plate after the rear drawing or physical motor is available.

## Cost and release

There are 38 fitted parts and three bare motor/debug/BOOT interfaces, with no purchased PD module, motor-driver module, external crystal, buck inductor, potentiometer, or motor connector. A rough small-volume component allowance is **US$4–7**, excluding PCB, assembly, shipping, motor, and supply. This is an estimate, not a vendor quote or an absolute budget guarantee. Ratings and procurement notes are in `docs/bom.md`.

Before ordering: obtain the motor rear drawing, review the footprint pin numbering and assembly rotations, check the current DRC/short report, then bench-test USB, PD negotiation, disabled start-up, phase current, regeneration, and temperature. The configured install/start instructions are saved as a draft in environment settings; saving that draft does not publish the environment.

## Published project

[tscircuit: NEMA14_CH32X035G8U6](https://tscircuit.com/AnasSarkiz/NEMA14_CH32X035G8U6). GitHub rename to the same exact name is pending repository-administration authorization; see [publishing notes](docs/publishing.md).

## Supplier models and A4 schematics

[Printable A4 schematic](artifacts/schematic-a4.pdf): 9 numbered landscape sheets with chip-purpose notes and every numbered physical pin. All **38/38 fitted components** use exact JLCPCB imports with native land patterns and OBJ/STEP models. Motor/debug/boot connections are bare PCB pads. See [supplier CAD details](docs/supplier-cad.md) and [the import report](artifacts/jlcpcb-import-report.json).

The GitHub repository is currently [AnasSarkiz/NEMA17_Controller](https://github.com/AnasSarkiz/NEMA17_Controller). Its requested rename to `NEMA14_CH32X035G8U6` is blocked by the GitHub integration (HTTP 403); repository settings must apply it. The project/package name is already correct. Supplier CAD URLs use the existing public repository so they load now.

## USB and final validation

[USB programming procedure](docs/usb-programming.md) · [Validation details](docs/validation.md) · [Browser schematic analysis](artifacts/validation/schematic-analysis-ui.png). Both board variants support boot-mode entry through their Data USB-C port; flashing still requires assembled-hardware validation. Current software checks report zero DRC errors/warnings, zero schematic-placement findings and no Gerber shorts. Application firmware remains a separate task.

The public main entry point is `index.circuit.tsx`, which exports the board from `src/board.tsx`. `index.circuit.json` is the checked saved layout; publication refreshes it from `artifacts/board.circuit.json` and includes both JSON files. `tscircuit.config.json` selects the root source entry and saved-layout preview.
