# Publishing

Target GitHub name: `AnasSarkiz/nema14_CH32X035G8U6`.
Target tscircuit package name: `nema14_CH32X035G8U6`, under the authenticated tscircuit account. The registry CLI accepts letters, numbers, underscores and hyphens; case is retained. The package configuration selects `src/board.tsx`, and the checked Circuit JSON is included as a board file. No firmware or fabrication readiness is implied by publication.

The design has been pushed to the existing GitHub repository on `main`; its rename remains pending. The GitHub API rename was attempted and denied by the environment proxy. The registry package-create endpoint was also denied; registry push reported no login. GitHub and registry operations need `api.github.com` and `registry-api.tscircuit.com` allowed in the active environment and credentials with repository-administration / registry-publication permissions. Configure credentials in environment settings or use the normal account login; do not put tokens in source or chat.

After access is available, rename the existing repository (preserving its visibility):

```sh
gh repo rename nema14_CH32X035G8U6 --repo AnasSarkiz/NEMA17_Controller --yes
git remote set-url origin https://github.com/AnasSarkiz/nema14_CH32X035G8U6.git
git push origin HEAD:main
```

For tscircuit, authenticate using `XDG_CONFIG_HOME=/workspace/.config tsci login`. Then run `npm run publish:tscircuit`; `tsci push` creates the package when absent and uploads its files. The initial registry publication is private. The saved copper lives in `artifacts/board.circuit.json`; the registry's source-rendered preview may autoroute differently, so review/download the saved artifact for copper verification.
