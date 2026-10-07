# Saved copper and verification

`artifacts/board.circuit.json` is the delivery layout. `npm run build` renders and checks it, without rerouting. `npm run autoroute` writes a separate `autorouted.circuit.json`; it cannot overwrite the delivery layout.

The tscircuit local autorouter was run first. Its saved copper had shorts and clearance violations, so the permitted fallback was used: freerouting 2.0.1, two layers, 0.15 mm copper clearance, 0.6/0.3 mm fallback vias and 0.5/0.25 mm repair vias, 0.3 mm motor traces and 0.2 mm signals. Tight escape repairs use 0.16 mm copper. Four screw-head keepouts are retained. Three exposed-pad ground vias are deliberate; all other via-in-pad placements are checked separately.

The native DSN export initially duplicated pad geometry. `scripts/freeroute.py` instead exports every actual pad and source connectivity identity. `freerouting-input.dsn`, its identity map, and `board.ses` preserve the fallback routing inputs and result. `scripts/import-session.py` reads the SES's declared units, preserves the physical footprints, and reconstructs source-net identity.

To reproduce the saved fallback and selected repairs **from the saved input files**:

```sh
python3 scripts/import-session.py
python3 scripts/repair-routing.py
python3 scripts/align-usb-edge.py
python3 scripts/sync-source.py
npm run build
npm run export
```

The repair script retains unaffected copper and assists explicitly selected connections with collision-aware searches. `manual-repairs.json` records added route points and vias. It also moves fanout vias to open the B+ escape and flips C_VCP to place its supply pad outside the charge-pump routing pocket. It reserves three separate MCU fanouts, reroutes the ENABLE_N and 3V3 diagonals, and relocates the MCU bypass capacitor. The final source reflects the capacitor placements. The saved unrouted JSON is the pre-repair placement required to reproduce the saved SES; do not replace it with the final placement before importing this SES.

To rerun freerouting from its saved DSN (Java21; optional JAR outside the repository):

```sh
XDG_CONFIG_HOME=/workspace/.config XDG_CACHE_HOME=/workspace/.cache \
java -Duser.home=/workspace/.freerouting -jar /workspace/freerouting-2.0.1.jar \
  --gui.enabled=false --api_server.enabled=false --router.stop_pass_no=25 \
  -de artifacts/freerouting-input.dsn -do artifacts/board.ses -mp 20 -mt 2
```

JAR SHA256: `d7fd0f63f52e6d74b0fad6715f87ca9f0ffd7109d66b2a584638000270592ecf`.
A rerun may choose different routes; the repair script targets the saved SES, not arbitrary new routes. Run all checks after changes. Gerber copper shorts are checked independently of circuit JSON. DRC success does not validate electrical behavior, rear mounting fit, USB firmware, or fabrication readiness.

The USB-C front fabrication outlines are flush at x = ±17.5 mm. Both connector origins moved outward 0.95 mm to ±13.85 mm. `align-usb-edge.py` elastically extends saved copper and preserves pad identities, then separates the two bottom routes beside the upper right screw keepout. It must run once after importing/repairing the archived SES, before source synchronization. The normal check asserts both connector front faces meet the board outline.

The current delivery also contains R_USB_BOOT and J_BOOT. The archived SES predates them. After the archived reconstruction above, compile current source, merge the two new components with `python3 scripts/sync-presentation.py --extend-usb-boot`, then run `/workspace/.routing-venv/bin/python scripts/route-usb-boot.py` **once**. This adds three branches while asserting all original PCB records remain. Its route points are saved in `artifacts/validation/usb-boot-routing.json`. Recheck the complete copper afterward.
