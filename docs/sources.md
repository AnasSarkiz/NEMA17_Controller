# Sources and evidence

- Motor requested by user: https://www.omc-stepperonline.com/nema-14-bipolar-0-9deg-11ncm-15-58oz-in-0-4a-10v-35x35x28mm-4-wires-14hm11-0404s . Manufacturer drawing verified: https://www.omc-stepperonline.com/download/14HM11-0404S.pdf . It confirms 0.40 A/phase, 25 Ω ±10%, 24 mH ±20%, 0.9° steps, and front-face 26 ±0.2 mm M3 mounting pitch. Rear attachment dimensions are absent.
- Official WCH SDK: https://github.com/openwch/ch32x035 . Its Snake board embeds a CH32X035G8U6 symbol and QFN28/4×4/0.4/2.6×2.6 footprint.
- Current KiCad symbols: https://gitlab.com/kicad/libraries/kicad-symbols , inspected revision `e1bb0a65cb243525367c5dc7294665b9fd57fc4d`; `MCU_WCH_RiscV/CH32X035G8U6` and `Interface_USB/CH224K` establish pin mapping and package selection.
- Current KiCad footprints: https://gitlab.com/kicad/libraries/kicad-footprints ; `SSOP-10-1EP_3.9x4.9mm_P1mm_EP2.1x3.3mm` and `SOT-89-3` establish the corrected PD and regulator land dimensions.
- Published PD reference: https://github.com/tomorrow56/CH224K_PDDecoy , `toragi/img/04_Schematics.png` independently confirms CC1 pin7 / CC2 pin6. https://github.com/UNIT-Electronics-MX/unit_proto_power_delivery_decoy_ch224k at `36e92b99cba94163813b383ca9a16cd6f7f6ef62` documents CFG1/2/3 = 0/1/1 for 15 V.
- Driver package/pin reference: https://github.com/adafruit/Adafruit-A4988-Breakout-PCB at `f10f6b1d10aeeabc7a4a3445b81925c0a51d0e45`, Eagle A4983_LOGICAL / QFN28_5MM used on that A4988 carrier. Manufacturer A4988 datasheet review remains required before release.
- USB footprint: https://github.com/KiCad/kicad-footprints/blob/master/Connector_USB.pretty/USB_C_Receptacle_HRO_TYPE-C-31-M-12.kicad_mod . Converted to TSX using the current tscircuit CLI; physically shared USB pads are represented once.
- Freerouting fallback: https://github.com/freerouting/freerouting/releases/tag/v2.0.1 ; Java21-compatible release JAR downloaded over verified HTTPS. The unsupported GUI-only 1.9.0 attempt was abandoned.

Tscircuit npm version checked and pinned: 0.0.2757; CLI: 0.1.2257. TLS verification was retained. Registry-import endpoints and direct manufacturer documents were unavailable; local explicit footprints and Git-hosted reference evidence were used. Tracked original repository files were absent (unborn branch); all design files were created under the user's subsequent explicit design request.
