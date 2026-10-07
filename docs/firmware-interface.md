# Firmware interface (hardware contract; implementation pending)

| Signal | CH32X035G8U6 pad | GPIO | Requirement |
| --- | --- | --- | --- |
| STEP | 5 | PA0 | Timer-driven pulses, ≥2 µs high and ≥2 µs low |
| DIR | 6 | PA1 | Hold stable ≥2 µs before STEP edge |
| PD_GOOD | 7 | PA2 | Active-low CH224K PG; pull-up to 3.3 V |
| DATA_PRESENT | 8 | PA3 | 100 kΩ/100 kΩ divider from computer VBUS |
| VM_SENSE | 9 | PA4 | 100 kΩ/10 kΩ divider; 15 V → 1.364 V; ADC full scale is not a safe overvoltage limit |
| ENABLE_N | 14 | PB3 | High disables driver; hardware default high |
| SLEEP | 15 | PB4 | Low disables bridge/charge pump; hardware default low |
| DCK | 24 | PC19 | WCH two-wire programming clock |
| DIO | 25 | PC18 | WCH two-wire programming data |
| USB D− | 26 | PC16 | USBFS native PHY |
| USB D+ | 27 | PC17 | USBFS native PHY |

CH32X035G8U6 uses 3.3 V supply and its internal 48 MHz oscillator. USB firmware must select the MCU's **3.3 V PHY mode**, detect data-port VBUS, and use the native USB pull-up configuration; do not copy a 5 V-only example unchanged. The fixed PD trigger requires no MCU PD stack.

Startup sequence: initialize STEP low, ENABLE_N high, SLEEP low; read voltage and PG; expose USB only with data VBUS present; require an explicit host command; enable only with PG low and motor supply 13.5–16.5 V; raise SLEEP, wait at least 1 ms for the charge pump, then drive ENABLE_N low. A source without a 15 V PDO must leave the motor disabled. Stop on a lost PD contract, USB disconnect, or command watchdog timeout. Never automatically resume motion after reset.

A proposed USB CDC command interface is `STATUS`, `MOVE <signed microsteps> <microsteps/second>`, `STOP`, and `DISABLE`. Use a timer/state machine rather than blocking delays. Limit acceleration and speed through bench testing; winding current and available torque limit the useful rate. This file is a contract for the next firmware task, not tested firmware. WCH provides `EVT/EXAM/USB/USBFS/DEVICE/SimulateCDC` in its CH32X035 SDK; remove the example's USART2 bridge because PA2 is used here for PD power sensing. PA3 is used for computer-VBUS presence.

For factory ROM USB boot entry, see [USB programming](usb-programming.md). This hardware contract does not supply a motor-control application.

Motor voltage conversion: `VM_V = VM_SENSE_V × 11` for the reviewed 100 kΩ/10 kΩ divider. Update/calibrate firmware accordingly; the former ×(122/22) conversion is obsolete.
