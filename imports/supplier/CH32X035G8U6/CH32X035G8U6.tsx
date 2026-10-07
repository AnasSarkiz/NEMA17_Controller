import React from "react"
const objPath = "https://raw.githubusercontent.com/AnasSarkiz/NEMA17_Controller/main/imports/supplier/CH32X035G8U6/CH32X035G8U6.obj"
const stepPath = "https://raw.githubusercontent.com/AnasSarkiz/NEMA17_Controller/main/imports/supplier/CH32X035G8U6/CH32X035G8U6.step"
import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["PC15","CC2","T2C3_1","T1ET_1"],
  pin2: ["VDD"],
  pin3: ["PC0","TX2_","T2C4_1","T1C1_","T2BK_1","A10"],
  pin4: ["PC3","T1C4_1","T2C3N_1","T2C1N_1","C1N0","A13"],
  pin5: ["PA0","T2C1","CTS2","C1P1","A0"],
  pin6: ["PA1","RTS2","T2C2","C1O","O1N2","O2N2","A1"],
  pin7: ["PA2","TX2","T2C3","O2O1","T2ET_","A2"],
  pin8: ["PA3","T2C4","O1O0","T3C1_1","RX2","A3"],
  pin9: ["PA4","CS","O2O0","T3C2_1","A4"],
  pin10: ["PA5","SCK","TX4_1","O2N0","A5"],
  pin11: ["PA6","MISO","T3C1","T1BK_","O1N0","A6"],
  pin12: ["PA7","MOSI","T3C2","T1C1N_","TX1_","O2P0","A7"],
  pin13: ["PB0","TX4","T1C2N_","O1P0","A8"],
  pin14: ["PB3","TX3","T2C3_2","T2C3N_2","O2P1"],
  pin15: ["PB4","T2C4_2","T3C1_2","T2BK_2","RX3","O1P2"],
  pin16: ["PB1","T1C3N_","RX4","O2N1","A9","PB5","O1O1","T3C2_2","T1BK"],
  pin17: ["PB6","T1C1N","CTS3","O1N1"],
  pin18: ["PB7","T1C2N","RTS3_","O2P2"],
  pin19: ["PB8","T1C3N","O1P1"],
  pin20: ["PB9","T1C1","MCO","TX4_2"],
  pin21: ["PB10","TX1","T1C2"],
  pin22: ["PB11","T1C3","T2C1N_2","RX1"],
  pin23: ["PB12","T1C4_2","T2C2N_"],
  pin24: ["PC19","DCK","T2C1_","T3C1_3","I2C_1","RX3_","C1P0"],
  pin25: ["PC18","DIO","TX3_","T2C1N_3","T3C2_3","I2C_2","T1ET_2"],
  pin26: ["PC16","UDM","T1C4","TX4_3","I2C_3","RX4_1","CTS1","PC11"],
  pin27: ["PC17","UDP","RTS1","TX4_4","I2C_4","RX4_2","T1ET","PC10"],
  pin28: ["PC14","CC1","T1C3_","T2C2_"],
  pin29: ["GND"]
} as const

const pinAttributes = {
  pin2: {requiresPower: true},
  pin29: {requiresGround: true}
} as const

export const CH32X035G8U6 = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      pinAttributes={pinAttributes}
      supplierPartNumbers={{
  "jlcpcb": [
    "C7437027"
  ]
}}
      manufacturerPartNumber="CH32X035G8U6"
      footprint={<footprint>
        <smtpad portHints={["pin4"]} pcbX="-0.001016mm" pcbY="-1.999996mm" width="0.1999996mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin5"]} pcbX="0.40005mm" pcbY="-1.999996mm" width="0.1999996mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin6"]} pcbX="0.8001mm" pcbY="-1.999996mm" width="0.1999996mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin7"]} pcbX="1.199896mm" pcbY="-1.999996mm" width="0.1999996mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin3"]} pcbX="-0.399796mm" pcbY="-1.999996mm" width="0.1999996mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin2"]} pcbX="-0.8001mm" pcbY="-1.999996mm" width="0.1999996mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin1"]} pcbX="-1.199896mm" pcbY="-1.999996mm" width="0.1999996mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin8"]} pcbX="1.999996mm" pcbY="-1.199896mm" width="0.6999986mm" height="0.1999996mm" shape="rect" />
<smtpad portHints={["pin9"]} pcbX="1.999996mm" pcbY="-0.8001mm" width="0.6999986mm" height="0.1999996mm" shape="rect" />
<smtpad portHints={["pin10"]} pcbX="1.999996mm" pcbY="-0.40005mm" width="0.6999986mm" height="0.1999996mm" shape="rect" />
<smtpad portHints={["pin11"]} pcbX="1.999234mm" pcbY="0mm" width="0.6999986mm" height="0.1999996mm" shape="rect" />
<smtpad portHints={["pin12"]} pcbX="1.999996mm" pcbY="0.399796mm" width="0.6999986mm" height="0.1999996mm" shape="rect" />
<smtpad portHints={["pin13"]} pcbX="1.999996mm" pcbY="0.8001mm" width="0.6999986mm" height="0.1999996mm" shape="rect" />
<smtpad portHints={["pin14"]} pcbX="1.999996mm" pcbY="1.199896mm" width="0.6999986mm" height="0.1999996mm" shape="rect" />
<smtpad portHints={["pin15"]} pcbX="1.199896mm" pcbY="1.999996mm" width="0.1999996mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin16"]} pcbX="0.8001mm" pcbY="1.999996mm" width="0.1999996mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin17"]} pcbX="0.399796mm" pcbY="1.999996mm" width="0.1999996mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin18"]} pcbX="0mm" pcbY="1.999996mm" width="0.1999996mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin19"]} pcbX="-0.399796mm" pcbY="1.999996mm" width="0.1999996mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin20"]} pcbX="-0.8001mm" pcbY="1.999996mm" width="0.1999996mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin21"]} pcbX="-1.199896mm" pcbY="1.999996mm" width="0.1999996mm" height="0.6999986mm" shape="rect" />
<smtpad portHints={["pin22"]} pcbX="-1.999996mm" pcbY="1.199896mm" width="0.6999986mm" height="0.1999996mm" shape="rect" />
<smtpad portHints={["pin23"]} pcbX="-1.999996mm" pcbY="0.8001mm" width="0.6999986mm" height="0.1999996mm" shape="rect" />
<smtpad portHints={["pin24"]} pcbX="-1.999996mm" pcbY="0.399796mm" width="0.6999986mm" height="0.1999996mm" shape="rect" />
<smtpad portHints={["pin25"]} pcbX="-1.999742mm" pcbY="0mm" width="0.6999986mm" height="0.1999996mm" shape="rect" />
<smtpad portHints={["pin26"]} pcbX="-1.999996mm" pcbY="-0.399796mm" width="0.6999986mm" height="0.1999996mm" shape="rect" />
<smtpad portHints={["pin27"]} pcbX="-1.999996mm" pcbY="-0.8001mm" width="0.6999986mm" height="0.1999996mm" shape="rect" />
<smtpad portHints={["pin28"]} pcbX="-1.999996mm" pcbY="-1.199896mm" width="0.6999986mm" height="0.1999996mm" shape="rect" />
<smtpad portHints={["pin29"]} pcbX="0.000254mm" pcbY="0.019812mm" width="2.7999944mm" height="2.7999944mm" shape="rect" />
<silkscreenpath route={[{"x":1.9999960000001238,"y":-1.4999969999998939},{"x":1.9999960000001238,"y":-1.9999959999998964},{"x":1.4999970000001213,"y":-1.9999959999998964}]} />
<silkscreenpath route={[{"x":1.4999970000001213,"y":1.99999600000001},{"x":1.9999960000001238,"y":1.99999600000001},{"x":1.9999960000001238,"y":1.4999970000001213}]} />
<silkscreenpath route={[{"x":-1.99999600000001,"y":1.4999970000001213},{"x":-1.99999600000001,"y":1.99999600000001},{"x":-1.4999969999998939,"y":1.99999600000001}]} />
<silkscreenpath route={[{"x":-1.4999969999998939,"y":-1.9999959999998964},{"x":-1.99999600000001,"y":-1.9999959999998964},{"x":-1.99999600000001,"y":-1.4999969999998939}]} />
<silkscreencircle pcbX="-1.905mm" pcbY="-2.286mm" radius="0.09906mm" />
<silkscreentext text="{NAME}" pcbX="0.011684mm" pcbY="3.343658mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-2.5999952999999323,"y":2.599995300000046},{"x":2.599995300000046,"y":2.599995300000046},{"x":2.599995300000046,"y":-2.5999952999999323},{"x":-2.5999952999999323,"y":-2.5999952999999323},{"x":-2.5999952999999323,"y":2.599995300000046}]} />
      </footprint>}
      cadModel={{
        objUrl: objPath,
        positionOffset: { x: (-0.0) * Math.cos(Number(props.pcbRotation ?? 0) * Math.PI / 180) - (0.0) * Math.sin(Number(props.pcbRotation ?? 0) * Math.PI / 180), y: (-0.0) * Math.sin(Number(props.pcbRotation ?? 0) * Math.PI / 180) + (0.0) * Math.cos(Number(props.pcbRotation ?? 0) * Math.PI / 180), z: 0 },
        stepUrl: stepPath,
        pcbRotationOffset: 0,
        modelOriginPosition: { x: 0, y: 0, z: -0.72 },
      }}
      {...props}
    />
  )
}