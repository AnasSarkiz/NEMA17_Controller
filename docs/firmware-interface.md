
# Firmware interface (hardware contract; implementation pending)

| Signal | CH32X035G8U6 pad | GPIO | Requirement |
| --- | --- | --- | --- |
| STEP | 5 | PA0 | Timer-driven pulses, ≥2 µs high and ≥2 µs low |
| DIR | 6 | PA1 | Hold stable ≥2 µs before STEP edge |
| PD_GOOD | 7 | PA2 | Active-low CH224K PG; pull-up to 3.3 V |
| DATA_PRESENT | 8 | PA3 | Digital active-low NPN host sensing; low means computer VBUS present |
| VM_SENSE | 9 | PA4 | Passive 100k/(10k∥470 Ω); scale 223.76596,15 V→0.067 V; calibrate ADC |
| ENABLE_N | 14 | PB3 | High disables driver; hardware default high |
| SLEEP | 15 | PB4 | Low disables bridge/charge pump; hardware default low |
| DCK | 24 | PC19 | WCH two-wire programming clock |
| DIO | 25 | PC18 | WCH two-wire programming data |
| USB D− | 26 | PC16 | USBFS native PHY |
| USB D+ | 27 | PC17 | USBFS native PHY |

CH32X035G8U6 uses 3.3 V supply and its internal 48 MHz oscillator. USB firmware must select the MCU's **3.3 V PHY mode**, detect data-port VBUS, and use the native USB pull-up configuration; do not copy a 5 V-only example unchanged. The fixed PD trigger requires no MCU PD stack.


A proposed USB CDC command interface is `STATUS`, `MOVE <signed microsteps> <microsteps/second>`, `STOP`, and `DISABLE`. Use a timer/state machine rather than blocking delays. Limit acceleration and speed through bench testing; winding current and available torque limit the useful rate. This file is a contract for the next firmware task, not tested firmware. WCH provides `EVT/EXAM/USB/USBFS/DEVICE/SimulateCDC` in its CH32X035 SDK; remove the example's USART2 bridge because PA2 is used here for PD power sensing. PA3 is a digital active-low computer-VBUS input; its ADC channel is unavailable on some lots. VM monitor is always passive; do not enable pulls/output drive. Brownout/reset transitions still require physical qualification.

For factory ROM USB boot entry, see [USB programming](usb-programming.md). This hardware contract does not supply a motor-control application.


## USB connector identification and cable access

Both USB-C openings face outward from the same **+Y edge**. **J_PD** is at X=−7 mm and supplies motor PD power; **J_DATA** is at X=+7 mm and connects the computer/programming interface. The 14 mm port-center pitch is screened against Tensility 10-06137 (PD) and 10-06139 (DATA) USB-C plug bodies. Their specified maximum 12.5 mm width leaves 1.5 mm nominal separation, or 1.3 mm after ±0.1 mm placement per port. Verify simultaneous insertion, shoulder registration, screw/carrier clearance and cable bending on the assembled prototype; see `mechanical-fit.md`.

## Revised startup and ADC contract

Removed VM switch/OE; CH32 PB7/pad 18 and RP2040 GPIO27/pad 39 are unconnected. Configure VM_SENSE as analog/high impedance, no pull-up/output. Convert `VM_V = ADC_pin_V ×223.7659574468`, use adequate acquisition/settling, calibration and averaging/hysteresis; 12-bit/3.3 V bus resolution≈0.180 V/count. Never use the historical×21 conversion. The divider remains bounded below 0.160034 V at the 35 V screening corner even through instantaneous logic collapse;35 V is not an operating bus allowance.

Initialize STEP low, ENABLE_N high and SLEEP low. Require stable 3.0–3.6 V logic, valid PG-low PD contract, calibrated bus 14.25–15.75 V and an explicit host command. Release SLEEP, wait≥2 ms, then enable. Disable immediately on PG/rail/command loss and never resume after reset without a new command. Qualify acquisition thresholds against ADC resolution/error. Firmware is not regenerative overvoltage protection; preserve the operating-envelope energy/current/temperature limits. USB ROM programming and application firmware remain untested/unimplemented hardware contracts.
