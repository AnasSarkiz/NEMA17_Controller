# Current mounting and USB verification

Saved board SHA-256: `0d772c1f839f50f30caa512a0dcc58f8ecfa88e35c2e9b44c2422365bc0a8e64`. Source, actual Gerber outline and Excellon drill files agree on 35 × 35 mm and four Ø3.2 mm NPTH holes at exactly (±13, ±13). Native STEP screening passes for the approved upward USB insertion, two defined 10 mm housings on opposite edges, a Ø6.4 × 3 mm head envelope around maximum Ø6 × 3 mm heads, and a Ø6 mm vertical tool shaft.

The nominal cable-housing gap is 23.300 mm. Actual supplier footprints/courtyards and models are retained. See [engineering fixes](engineering-fixes.md), `artifacts/mechanical/mount-usb-screen.json`, `artifacts/mount-drill-verification.json` and the actual CAM audit for current evidence.

Both primary and order-review manufacturing archives pass their full CAM audits. Passive-orientation advisories remain reviewable in the native placement log. The publication gate rejects other diagnostics and any real geometry/CAM failure.

The manufacturer motor drawing dimensions front holes only. Rear motor fit, adapter geometry, physical cable/fastener tolerances, assembly stack/thread engagement and hardware operation remain unverified.
