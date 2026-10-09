# Firmware interface (hardware contract; implementation pending)

| Signal | CH32X035G8U6 pad | GPIO | Requirement |
| --- | --- | --- | --- |
| STEP | 5 | PA0 | Timer-driven pulses, ≥2 µs high and ≥2 µs low |
| DIR | 6 | PA1 | Hold stable ≥2 µs before STEP edge |
| PD_GOOD | 7 | PA2 | Active-low CH224K PG; pull-up to 3.3 V |
| DATA_PRESENT | 8 | PA3 | Digital active-low NPN host sensing; low means computer VBUS present |
| VM_SENSE | 9 | PA4 | Switched, loaded divider; nominal VM/21, 15 V → 0.714 V; calibrate ADC |
| VM_ENABLE_N | 18 | PB7 | High isolates VM measurement; 10 kΩ pull-up; low only after V3V3 is valid |
| ENABLE_N | 14 | PB3 | High disables driver; hardware default high |
| SLEEP | 15 | PB4 | Low disables bridge/charge pump; hardware default low |
| DCK | 24 | PC19 | WCH two-wire programming clock |
| DIO | 25 | PC18 | WCH two-wire programming data |
| USB D− | 26 | PC16 | USBFS native PHY |
| USB D+ | 27 | PC17 | USBFS native PHY |

CH32X035G8U6 uses 3.3 V supply and its internal 48 MHz oscillator. USB firmware must select the MCU's **3.3 V PHY mode**, detect data-port VBUS, and use the native USB pull-up configuration; do not copy a 5 V-only example unchanged. The fixed PD trigger requires no MCU PD stack.

Startup sequence: initialize STEP low, ENABLE_N high, SLEEP low and VM_ENABLE_N high; establish V3V3, drive VM_ENABLE_N low, wait ≥0.5 ms, acquire/calibrate voltage and read PG; expose USB only with data VBUS present; require an explicit host command; enable only with PG low and motor supply 13.5–16.5 V; raise SLEEP, wait at least 2 ms for the charge pump, then drive ENABLE_N low. A source without a 15 V PDO must leave the motor disabled. Stop on a lost PD contract, USB disconnect, or command watchdog timeout. Never automatically resume motion after reset.

A proposed USB CDC command interface is `STATUS`, `MOVE <signed microsteps> <microsteps/second>`, `STOP`, and `DISABLE`. Use a timer/state machine rather than blocking delays. Limit acceleration and speed through bench testing; winding current and available torque limit the useful rate. This file is a contract for the next firmware task, not tested firmware. WCH provides `EVT/EXAM/USB/USBFS/DEVICE/SimulateCDC` in its CH32X035 SDK; remove the example's USART2 bridge because PA2 is used here for PD power sensing. PA3 is a digital active-low computer-VBUS input; its ADC channel is unavailable on some lots. Disable VM measurement before sleep and a detected rail fault. The switch and output-filter behavior during brownout still requires physical qualification; firmware cannot guarantee an arbitrary unpowered-pin condition.

For factory ROM USB boot entry, see [USB programming](usb-programming.md). This hardware contract does not supply a motor-control application.

Motor voltage conversion with the switch enabled: `VM_V ≈ VM_SENSE_V × 21`. The 100 kΩ/10 kΩ input divider is additionally loaded by a 10 kΩ output bleed; switch resistance and ADC/resistor errors require calibration. Use slow acquisition and ≥0.5 ms settling. A disabled switch reading is not a bus-voltage measurement. Neither the earlier ×11 nor the original ×(122/22) conversion applies to the final protected output.

## USB connector identification and cable access

Both USB-C openings face outward from the same **+Y edge**. **J_PD** is at X=−7 mm and supplies motor PD power; **J_DATA** is at X=+7 mm and connects the computer/programming interface. The 14 mm port-center pitch is screened against Tensility 10-06137 (PD) and 10-06139 (DATA) USB-C plug bodies. Their specified maximum 12.5 mm width leaves 1.5 mm nominal separation, or 1.3 mm after ±0.1 mm placement per port. Verify simultaneous insertion, shoulder registration, screw/carrier clearance and cable bending on the assembled prototype; see `mechanical-fit.md`.
