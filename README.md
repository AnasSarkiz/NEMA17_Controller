# NEMA14 USB-C PD controller

A two-layer tscircuit **hardware prototype** for the STEPperONLINE 14HM11-0404S, using **CH32X035G8U6**, two separate USB-C receptacles, and four mounting holes. Manufacturing release is blocked pending electrical and physical prototype qualification of the proposed front-thread carrier. See `artifacts/drc-report.json` for the current routed-board checks; a generated Gerber ZIP is not a release approval.

| Item | Design |
| --- | --- |
| Motor | 35 × 35 × 28 mm, bipolar, 0.9°, 0.4 A/phase, 10 V, 11 N·cm — specifications from the supplied product listing |
| Board | 35 × 35 mm, two copper layers, 1.6 mm FR-4; all components assembled on top |
| USB-C placement | Both openings face outward at the same +Y edge; PD at X−5.3 mm, data at X+5.3 mm; compact cable overmolds ≤10 mm wide require physical fit check |
| Mounting | Four Ø3.2 mm non-plated holes at (±13, ±13) mm; 26 mm square pitch; 5.4 mm square copper/component exclusions |
| MCU | CH32X035G8U6, QFN-28 plus grounded exposed pad; internal oscillator |
| Power USB-C | CH224K fixed request for **15 V**: CFG1 low, CFG2/CFG3 high |
| Computer USB-C | USB 2.0 full-speed D+/D− and two 5.1 kΩ CC pull-downs; USBLC6-2SC6 ESD protection |
| Driver | A4988SETTR-T, fixed 1/16 microsteps, regulated phase current |
| Current | 0.351 A nominal peak; 0.24 Ω sense resistors; 3.9 kΩ/1 kΩ VREF divider |
| Motor connection | Four plated wire-solder holes: A+, A−, B+, B− |
| Programming | Data USB-C via ROM ISP with 4.7 kΩ BOOT jumper; WCH-LinkE debug pads retained |
| Tools | tscircuit 0.0.2764, CLI 0.1.2261; pinned in lockfile |

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

The A4988 regulates coil current, so 15 V supply does not apply a constant 15 V to the 10 V-rated windings. VREF = 3.3 × 1/(3.9+1) = 0.6735 V; I_peak = VREF/(8 × 0.24 Ω) = 0.3508 A. Allegro does not specify trip accuracy at this low VREF; no qualified maximum current is claimed. Measure actual phase peaks ≤0.40 A and temperature on a prototype. The motor has 400 full steps/revolution, giving 6,400 commanded microsteps/revolution.

The motor bridge draws only from `PD_VBUS`. Two B5819W Schottky diodes OR `PD_VBUS` and `DATA_VBUS` into an HT7533-1 3.3 V regulator (supplier-listed 30 V input; primary thermal/stability limits remain to be verified). This provides computer-only logic power and diode reverse isolation from the motor source; actual USB enumeration and host-backfeed behavior require assembled-board tests. Both ports share signal ground. The linear regulator supplies only logic; motor current bypasses it. Driver SLEEP has a 10 kΩ pull-down and ENABLE_N a 10 kΩ pull-up, so the bridge remains disabled until firmware deliberately enables it.

Use a USB PD supply advertising a 15 V PDO. The CH224K requests 15 V; it cannot force an unsupported supply to deliver it. CH224K PG is an **active-low** good-power indication. Firmware must also check measured motor voltage before enabling the bridge. DATA_PRESENT is now active low through native NPN sensing. PB7 controls a powered-off-protected VM switch; its enabled output uses calibrated nominal ×21 conversion. The switch OE/filter and NPN power-transition behavior remain qualification gates. See `docs/firmware-interface.md`; no USB motor-control firmware or physical enumeration result is claimed by this hardware-only prototype.

## Rear mounting decision

The official [full motor drawing](references/motor/14hm11-0404s/14HM11-0404S_Full_Datasheet.pdf) and [native STEP](references/motor/14hm11-0404s/14HM11-0404S.STEP) establish front-face mounting: four M3 threads on a 26 ± 0.2 mm square, minimum thread depth 4 mm. Rear end-cap recesses do not establish separate usable rear mounting threads. The four PCB holes instead fit the proposed separate front-mounted carrier, which returns behind the motor and provides a 7.2 mm insulating gap. Exact native model collision checks and carrier STEP assemblies are in [mechanical-fit.md](docs/mechanical-fit.md); supplied motor revision, carrier strength, fasteners, tolerance and cable samples still require physical qualification. Do not replace motor end-cap screws or drill the motor from these files.

## Cost and release

There are 44 fitted native supplier parts and three bare motor/debug/BOOT interfaces, with no purchased PD module, motor-driver module, external crystal, buck inductor, potentiometer, or motor connector. The exact 44-part BOM requires a fresh supplier and assembly quote, including the qualified 100 µF capacitor and sensor isolation parts. PCB, filled/capped exposed-pad vias, carrier, assembly, shipping, motor and supply also require quotes; no absolute cost is claimed. Ratings and procurement notes are in `docs/bom.md`.

Before ordering: qualify the proposed carrier on the supplied motor, review the footprint pin numbering and assembly rotations, check the current DRC/short report, then bench-test USB, PD negotiation, disabled start-up, phase current, regeneration, and temperature. The configured install/start instructions are saved as a draft in environment settings; saving that draft does not publish the environment.

## Published project

[tscircuit: NEMA14_CH32X035G8U6](https://tscircuit.com/AnasSarkiz/NEMA14_CH32X035G8U6). GitHub rename to the same exact name is pending repository-administration authorization; see [publishing notes](docs/publishing.md).

## Supplier models and A4 schematics

[Printable A4 schematic](artifacts/schematic-a4.pdf): 10 numbered landscape sheets with chip-purpose notes and every numbered physical pin. All **44/44 fitted components** use exact JLCPCB imports with native land patterns and OBJ/STEP models. Motor/debug/boot connections are bare PCB pads. See [supplier CAD details](docs/supplier-cad.md) and [the import report](artifacts/jlcpcb-import-report.json).

The GitHub repository is currently [AnasSarkiz/NEMA17_Controller](https://github.com/AnasSarkiz/NEMA17_Controller). Its requested rename to `NEMA14_CH32X035G8U6` is blocked by the GitHub integration (HTTP 403); repository settings must apply it. The project/package name is already correct. Supplier CAD URLs use the existing public repository so they load now.

## USB and final validation

[USB programming procedure](docs/usb-programming.md) · [Validation details](docs/validation.md) · [Browser schematic analysis](artifacts/validation/schematic-analysis-ui.png). Both board variants support boot-mode entry through their Data USB-C port; flashing still requires assembled-hardware validation. The corrected saved board passes DRC, native copper connectivity and Gerber shorts checks. One generic-chip ERC warning describes the native NPN import as missing a supply pin; an NPN has no VDD pin. Final schematic/presentation and manufacturing evidence are recorded in the review artifacts; passing software checks does not establish hardware qualification. Application firmware remains a separate task.

The public main entry point is `index.circuit.tsx`, which exports the board from `src/board.tsx`. `index.circuit.json` is the checked saved layout; publication refreshes it from `artifacts/board.circuit.json` and includes both JSON files. `tscircuit.config.json` selects the root source entry and saved-layout preview.

Publication uses the CLI build-output option: `tsci push index.circuit.tsx --include-dist`. Before uploading, the script runs `tsci build index.circuit.json` and verifies that `dist/index/circuit.json` equals the checked saved routing.

## Copper and electrical review

The [electrical review](docs/electrical.md) records power-trace widening, filled grounds, the protected VM divider with enabled ×21 transfer, copper-thickness requirements, and remaining prototype tests. Run `npm run check:copper` for the actual saved-segment audit. The [machine-readable report](artifacts/trace-width-review.json) distinguishes isolated tracks from parallel ground-plane paths; software checks do not certify hardware operation.

## Engineering prototype review

[Engineering findings](docs/engineering-review.md) · [Bring-up procedure](docs/bringup-checklist.md) · [Manufacturer evidence](docs/component-evidence.md) · [Mechanical fit](docs/mechanical-fit.md) · [Manufacturing review](docs/manufacturing-review.md). The corrected bulk part is native Panasonic C178585, 100 µF/35 V; original supplier land patterns remain intact. This review candidate has not been ordered, merged or republished. Regulator/transient margins, low-VREF phase accuracy, powered-off transitions, actual USB flashing and sample carrier fit remain physical release gates.
