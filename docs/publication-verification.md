# Public release verification

The release version comes from `package.json`. The unchanged `scripts/verify-publication.py` compares unauthenticated public Circuit JSON/native build, default Gerbers, actual mounting drills, the order-review package and pinned GitHub CAD/source files against the qualified board. The authoritative completed receipt is committed to `artifacts/publication-verification.json` after publication.

The latest verified publication is v1.11.2, with 373 public files and board SHA-256 `0d772c1f839f50f30caa512a0dcc58f8ecfa88e35c2e9b44c2422365bc0a8e64`. Its CAD/source files are pinned to GitHub revision `14f39543d57c6af1f158146d4898bcdf79173081`. This update corrects order instructions and refreshes the assembly concept while retaining qualified copper.

Supplier/process/pickup approval, prototype bench qualification and rear motor/encoder mechanical evidence remain outstanding.
