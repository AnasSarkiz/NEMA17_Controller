# JLCPCB imports and printable schematics

Every fitted component uses a supplier component created with `tsci import --jlcpcb --download --use-exact-footprint C<number>`. `src/jlcpcb-catalog.json` maps every reference to its exact JLCPCB part and records original import/model hashes. The active component resolver in `src/supplier-parts.tsx` renders the imported JSX; it rejects custom footprint and CAD overrides. Unused generic component files have been removed.

`imports/supplier/` contains the native TSX, unchanged original `.tsx.original`, OBJ and STEP files. Active TSX only adds React compatibility, public GitHub model URLs and a CAD anchor correction for asymmetric pad bounds. Imported footprint JSX is checked byte for byte against the original. No model vertices or supplier footprints have been resized or translated. Public raw GitHub URLs keep large CAD assets outside the registry upload limit.

Both USB receptacles are **C165948 / TYPE-C-31-M-12**. All 16 numbered supplier contacts, including four shield tabs, use the actual land pattern. Both native model mating planes face +Y at Y=17.5 mm, with centers X=−5.3/+5.3 mm. Native PCB bounding-box centers are Y=12.57501465 mm at 180°; logical/CAD anchors are Y=12.1499711 mm at 0°. These are different datums, not interchangeable placement coordinates. Compact cable overmolds must be ≤10 mm wide and physically checked together. Model bounds are checked against native courtyards. Coordinate checks do not establish physical rear-motor fit.

Motor, debug and BOOT connections are bare PCB solder interfaces. They have no fitted component to import or model. The four mounting holes are PCB features.

The exact sense resistors are **C2930216 / FRL0805FR240TS**, 0.24 Ω, 1%, 125 mW. A 3.9 kΩ/1 kΩ VREF divider sets about 0.351 A nominal peak phase current; estimated sense dissipation is 29.5 mW. The bulk capacitor is **C178585 / Panasonic EEEFPV101XAP**, 100 µF ±20%, 35 V, with verified 0.60 Arms rating at 100 kHz/105 °C. Verify current, thermal behavior and capacitor bias on an assembled prototype.

Native numbered landscape A4 sheets include every physical pin and chip-purpose text. `report-presentation.py` verifies original imported footprint JSX, supplier IDs/MPNs, both CAD assets and hashes, 3D placement bounds, USB opening planes, A4 dimensions and pin/net coverage.

CH224K supply resistor R_PD uses **C441922 / ERJPA3F1001V**, 1 kΩ, 0603, 0.25 W, with its exact imported land pattern. The rating provides nominal dissipation allowance at the requested 15 V; actual resistor temperature and manufacturer derating remain qualification requirements.

The final CH32 board contains **44 fitted native models**. The NPN C94514 and SC70-5 switch C131992 also use direct supplier imports. C178585’s native generic model measures approximately 5.82 mm high while its manufacturer envelope is 7.7 ±0.3 mm. Native CAD is not resized: the mechanical review checks a separate maximum envelope and records this explicit review item. CAD-model collision checks alone cannot replace exact body specifications or a motor sample fit.
