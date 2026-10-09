# Saved-board validation

Run `npm run typecheck`, `npm run source:check`, `npm run build`, `npm exec -- tsci check artifacts/board.circuit.json`, `npm exec -- tsci check schematic-placement artifacts/board.circuit.json`, `npm run export`, and `npm run shorts`. Source compilation writes its separate unrouted artifact; build/check/render use the saved delivery copper. `scripts/sync-presentation.py` merges source/schematic metadata with assertions that saved PCB records and physical pin/net identities are retained.

`artifacts/validation/` contains actual command outputs. `artifacts/drc-report.json` contains full checks including power/ground pin attributes. Passive connector/crystal footprints are classified by physical role for ERC. `artifacts/physical-connectivity.json` independently checks the copper islands with Shapely geometry. Gerber shorts are checked on every copper layer at 100 pixels/mm. These are software checks and do not establish physical flashing, assembly, rear fit or thermal behavior.

## Browser schematic review

Run `python3 scripts/schematic-review-ui.py` for a read-only browser UI that displays native tscircuit A4 SVG pages beside actual `tsci check schematic-placement` and DRC findings. The browser review visits every numbered A4 page; screenshots and its result JSON are in `artifacts/validation/`.

The standalone tscircuit IDE was also launched. In this environment its PCB pane cannot obtain a WebGPU adapter, and the Schematic tab is disabled for the saved circuit-JSON selection. The review UI provides the native SVGs and CLI analysis without requiring GPU access; it is a project review tool, not the IDE's disabled schematic analyzer pane. External telemetry/CDN requests blocked by the cloud allowlist are recorded as environmental limitations.

See [USB programming](usb-programming.md). All fitted components now have exact supplier imports and OBJ/STEP assets; consult the reference-level import report.

## Final official CLI results

[Actual native CLI results](../artifacts/validation/native-cli-final/results.json) report netlist, pin specification and source checks on `index.circuit.tsx` exiting 0. Netlist checking directly against a JSON array was unsupported and produced a React element-type error; the TSX entrypoint is the supported final input.

PCB `placement` checking exits **1**, both on the immutable unrouted source and the accepted saved board. It reports **three orientation suggestions**: rotate R_PD, C_VM_ISO and C_REF 180°. Its placement DRC section reports 0 errors / 0 warnings. These airwire/rotation heuristics are recorded as advisories, not erased or counted as an overall CLI pass. Exact native pad connectivity and actual all-layer CAM prove the existing routes have no shorts/opens; future placement optimization and physical performance remain separate review decisions. The standalone `schematic-placement` check reports zero findings and has a different scope.

The current source/board/ZIP, mechanical/A4/replay hashes and exact software outcomes are bound in [engineering review manifest](../artifacts/validation/engineering-review-manifest.json). Fabrication and physical qualification remain blocked as recorded in [program state](../.pcba-workflow/program-state.json).
