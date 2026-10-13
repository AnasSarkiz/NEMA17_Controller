# Verified public release 1.8.2

Public package: https://tscircuit.com/AnasSarkiz/NEMA14_CH32X035G8U6

The unauthenticated index and native dist match the reviewed saved Circuit JSON apart from CAD URLs pinned to GitHub code revision `ef555afc5a3ed2d5ba50a91a28379e832b20931e`. Actual public Gerber outline and NPTH mounting drills match the 35 × 35 mm board and four Ø3.2 mm holes at (±13, ±13). Every public JLCPCB review file was compared byte-for-byte with the locally audited handoff; its corrected CAM audit passes with zero findings. Standard USB-C drawings have empty native placement diagnostics.

See `artifacts/publication-verification.json` for file hashes and the public review-package receipt. All fitted components populate the top; separate bare top-side test points retain debug/boot access. Both outward-facing USB mouths share +Y at 12.4 mm pitch; the accepted housing width is 10 mm, giving 2.4 mm nominal separation. J_MOTOR is SMT C160390.

Supplier placement/process approval, firmware and bench tests, and rear-motor mounting evidence remain pending. The separate motor/harness view is a concept. Native component placement has seven orientation advisories; strict generic JSON importers retain inherited metadata findings described in the review package.
