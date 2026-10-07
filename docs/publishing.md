# Publishing

Requested name: `NEMA14_CH32X035G8U6` (case retained).

Public registry project: https://tscircuit.com/AnasSarkiz/NEMA14_CH32X035G8U6 . Publish updates with `npm run publish:tscircuit`; CLI login uses `XDG_CONFIG_HOME=/workspace/.config tsci login`. The configuration includes checked copper in `artifacts/board.circuit.json`. The source-rendered registry preview may autoroute differently; use the saved artifact and Gerbers to review manufactured copper.

GitHub: https://github.com/AnasSarkiz/NEMA17_Controller . Renaming to `AnasSarkiz/NEMA14_CH32X035G8U6` remains blocked: GitHub returned HTTP 403, "Resource not accessible by integration", although account access reports administrator permission. The integration credential needs repository Administration write permission, or the owner can rename in repository Settings. After renaming:

```sh
git remote set-url origin https://github.com/AnasSarkiz/NEMA14_CH32X035G8U6.git
git push origin HEAD:main
```

The registry upload is independent; automatic GitHub linking was rejected because the repository is not accessible to the tscircuit GitHub app installation. Both projects are public. Publication does not imply firmware completion, tested electrical behavior, rear mounting compatibility, or manufacturing approval.
