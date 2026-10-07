# USB programming

1. Disconnect both USB-C cables so the MCU is fully unpowered.
2. Short the two bare `J_BOOT` pads with tweezers. `R_USB_BOOT` (4.7 kΩ) pulls PC17/D+ high, following WCH's reference download circuit.
3. Connect the computer to **J_DATA** while holding the short; release it after power-up.
4. Use WCHISPTool's CH32X035 USB download mode to load a compatible application.
5. Remove the short and power-cycle to run the application.

Source: WCH [CH32X035 official EVT](https://github.com/openwch/ch32x035), `EVT/PUB/CH32x035 Evaluation Board Reference-EN.pdf`, section 5, and `EVT/PUB/CH32X035SCH.pdf`. PC17 is physical pad 27; PC16/D− is pad 26. WCH-LinkE pads remain available. The example USB-IAP application is not preloaded; this procedure targets factory ROM ISP. Both power inputs must be disconnected for cold boot.

The **PD port is motor power only**, requesting 15 V. Programming uses the separate **Data USB-C port**. USB ROM entry connections and physical copper continuity have been checked in CAD. Enumeration, boot-ROM PHY operation at the chosen supply, and actual flashing must still be tested on an assembled prototype. No motor-control firmware has been implemented or preloaded. Keep the motor disconnected during the first flashing/rail checks.
