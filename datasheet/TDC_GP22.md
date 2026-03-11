This product, formerly sold by ams AG, and before that optionally by eitherApplied Sensors GmbH, acam-messelectronic GmbH or Cambridge CMOS Sensors,is now owned and sold by

# ScioSense

The technical content of this document under ams / Applied Sensors / acam-messelectronic / Cambridge CMOS Sensors is still valid.

Contact information

Headquarters:

ScioSense B.V.

High Tech Campus 10

5656 AE Eindhoven

The Netherlands

info@sciosense.com

www.sciosense.com

# Ultrasonic-Flow-Converter

# Data Sheet

# TDC-GP22

Universal 2-Channel Time-to-Digital ConvertersDedicated to Ultrasonic Heat & Water Meters

March $1 3 ^ { \mathrm { t h } }$ 2014

Document-No: DB_GP22_en V0.9

# Pu bli sh ed by a cam -me s sele ct roni c gmbh©acam-messelectronic gmbh 2014

# Di s cl ai me r / No te s

“Preliminary” product information describes a product which is not in full production sothat full information about the product is not available yet. Therefore, acam-messelectronicgmbh (“acam”) reserves the right to modify this product without notice. The informationprovided by this data sheet is believed to be accurate and reliable. However, noresponsibility is assumed by acam for its use, nor for any infringements of patents orother rights of third parties that may result from its use. The informatio n is subject tochange without notice and is provided “as is” without warranty of any kind (expressed orimplied). All other brand and product names in this document are trademarks or servicemarks of their respective owners.

# Suppo rt / C ont a ct

For a complete listing of Direct Sales, Distributor and Sales Representative contacts, visitthe acam web site at:

http://www.acam.de/sales/distributors/

For technical support you can contact the acam support team in the headquarters inGermany or the Distributor in your country. The contact details of acam in Germany are:

support@acam.de

or by phone

+49-7244-74190.

# Content

1 Overview . . 1-3

1.1 Features.. . 1-3

1.2 Blockdiagram . . 1-4

1.3 Ordering Numbers .. . 1-4

2 Characteristics & Specifications 2-1

2.1 Electrical Characteristics . 2-1

2.2 Converter Specification.. . 2-4

2.3 Timings ... 2-6

2.4 Pin Description . 2-9

2.5 Package Drawings .. 2-11

2.6 Power Supply... 2-14

3 Registers & Communication . 3-1

3.1 Configuration registers .. . 3-1

3.2 Read registers... 3-14

3.3 EEPROM . 3-18

3.4 SPI-interface 3-19

4 Converter Frontend . 4-1

4.1 TDC - Measurement mode 1 . 4-1

4.2 TDC - Measurement mode 2 . 4-9

4.3 Analog Input Section . 4-16

4.4 First Wave Mode 4-17

4.5 Temperature Measurement. 4-23

5 Details and Special Functions .. 5-1

5.1 Oscillator . . 5-1

5.2 Fire Pulse Generator. . 5-3

5.3 Fast Initialization . . 5-7

5.4 Noise Unit . . 5-7

5.5 EMC Measures . . 5-8

6 Applications . 6-1

6.1 Ultrasonic Heat Meter . 6-1

7 Miscellaneous 7-1

7.1 Bug Report . . 7-1

7.2 Last Changes . . 7-2

# 1 Overview

TDC-GP22 is next generation‘s upgrade for TDC-GP21. It is a $100 \%$ pin-to-pin and functionalcompatible upgrade of TDC-GP21, with an extended functionality. Especially the new first-wavedetection capability makes the TDC-GP22 perfectly suited for ultrasonic water meters with theirhigh dynamics. The programmable offset range of the comparator is increased to $\pm 3 5 ~ \mathrm { m V }$ andthe offset is automatically set back to zero after the first wave detection. Measuring the relativepulse width of the first wave gives the user an indication of the strength of the received signal.This can be used for adopting the system to long-term signal attenuation or for bubble detection.The multi-hit data processing and data read-out is simplified compared to TDC-GP21.

All in all, the TDC-GP22 is a further improvement and simplification for the design of ultrasonicheat meters and a necessary step for compact ultrasonic water meters.

# 1.1 Features

# Measurement mode 2

 1 channel with typ. 90 ps resolution

 Double resolution mode with 45 ps, Quad resolution mode with 22 ps resolutio n

 Measurement range 700 ns to 4 ms

 3-fold multihit capability with automatic processing of all 3 data

# Analog Input Circuit

 Chopper-stabilized low-offset comparator, programmable, $\pm 3 5 { \mathrm { ~ m V } }$

First-wave detection: offset set zero automatically after first wave, hit selectionrelative to first wave

 First-wave pulse-width measurement for signal monitoring and bubble detection

 Integrated analog switches for input selection

 External circuit is reduced to 2 resistors and 2 capacitors

# Temperature Measurement Unit

 2 or 4 sensors, PT500/PT1000 or higher

 Schmitt trigger integrated

16-Bit eff. with external Schmitt trigger, 17.5-Bit eff. with integrated low noiseSchmitt trigger

 Ultra low current (0.08 $\mu \mathsf { A }$ when measuring every 30 seconds)

# Special Functions

 Fire pulse generator, up to 127 pulses

 Trigger to rising and/or falling edge

 Precise stop enable by windowing

 Low-power 32 kHz oscillator (500 nA)

 Clock calibration unit

 7x32 Bit EEPROM

# Measurement mode 1

 2 channels with typ. 90 ps resolution

 channel double resolution with typ. 45 ps

 Range 3.5 ns (0 ns) to 2.5 µs

 20 ns pulse-pair resolution, 4-fold multihit

 Up to 500 000 measurements per second in measurement mode 1

# General

 4-wire SPI interface

500 kHz continuous data rate max.

 I/O voltage 2.5 V to 3.6 V

 Core voltage 2.5 V to 3.6 V

 Temperature range – 40 $^ \circ \mathbb { C }$ to $+ 1 2 5 ~ ^ { \circ } \mathrm { C }$

 QFN 32 Package

# 1.2 Blockdiagram

![](images/3218b241e773c101f464a53831e8d25161ead7e3821298480d35c01e9c90a234.jpg)


# 1.3 Ordering Numbers

<table><tr><td>Part#</td><td>Package</td><td>Package Qty; Carrier</td><td>Order number</td><td></td></tr><tr><td>TDC-GP22</td><td>QFN32</td><td colspan="2">5000/3000; T&amp;R</td><td>MNR 1950</td></tr><tr><td>TDC-GP22</td><td>QFN32</td><td colspan="2">490; Tray</td><td>MNR 1949</td></tr><tr><td>GP22-EVA-KIT</td><td>System</td><td colspan="2">1; Box</td><td>MNR 1951</td></tr></table>

This product is RoHS compliant and does not contain any Pb.

# 2 Characteristics & Specifications

# 2.1 Electrical Characteristics

# Absolute Maximum Ratings

Supply voltage

Vcc vs. GND - 0.3 to 4.0 V

Vio vs. GND - 0.3 to 4.0 V

$\mathsf { V } _ { \mathsf { i n } }$ - 0.5 to $\mathsf { V } _ { \mathbb { c } \mathbb { c } } + \mathsf { O } . 5$ V

Storage temperature (Tstg)

ESD rating (HBM), each pin

Junction temperature (Tj)

- 55 to 150 $^ \circ \mathbb { C }$

> 2 kV

max.125 $^ \circ \mathbb { C }$

# Recommended Operating Conditions

<table><tr><td>Symbol</td><td>Parameter</td><td>Conditions</td><td>Min</td><td>Typ</td><td>Max</td><td>Unit</td></tr><tr><td>Vcc</td><td>Core supply voltage1</td><td>Vio = Vcc</td><td>2.5</td><td></td><td>3.6</td><td>V</td></tr><tr><td>Vio</td><td>I/O supply voltage</td><td></td><td>2.5</td><td></td><td>3.6</td><td>V</td></tr><tr><td>tri</td><td>Normal input rising time</td><td></td><td></td><td></td><td>200</td><td>ns</td></tr><tr><td>ta</td><td>Normal input falling time</td><td></td><td></td><td></td><td>200</td><td>ns</td></tr><tr><td>tri</td><td>Schmitt trigger rising time</td><td></td><td></td><td></td><td>5</td><td>ms</td></tr><tr><td>ta</td><td>Schmitt trigger falling time</td><td></td><td></td><td></td><td>5</td><td>ms</td></tr><tr><td>Ta</td><td>Ambient temperature</td><td>Tj must not exceed 125°C</td><td>-40</td><td></td><td>125</td><td>°C</td></tr><tr><td>Rth(j-a)</td><td>Thermal resistance</td><td>junction-ambient</td><td></td><td>28</td><td></td><td>K/W</td></tr></table>


1 including the oscillator pins XIN, XOUT, Clk32In, Clk32Out


DC Characteristics ${ \left\{ \mathsf { U } _ { \mathrm { i } \mathrm { 0 } } = \mathsf { U } _ { \mathrm { c c } } = 3 . \mathsf { \mathbf { 0 } } \right\} }$ V, $\bar { \mathbf { I } } _ { \mathrm { j } } = - 4 \mathbf { \mathbb { I } }$ to $+ 8 5 ^ { \circ } \mathbf { \vec { U } } 1$

<table><tr><td>Symbol</td><td>Parameter</td><td>Conditions</td><td>Min</td><td>Typ</td><td>Max</td><td>Unit</td></tr><tr><td>I32</td><td>Current 32 kHz</td><td>Icc + Iio, only 32 kHz oscillator running</td><td></td><td>1.0</td><td></td><td>μA</td></tr><tr><td>Ihs</td><td>Current 4 MHz oscillator</td><td>Vcc = Vio = 3.6 V = 3.0 V off</td><td></td><td>200
130
&lt; 1</td><td></td><td>μA
μA
nA</td></tr><tr><td>Itmu</td><td>Current time measuring unit</td><td>only during active time measurement</td><td></td><td>4</td><td></td><td>mA</td></tr><tr><td>Iddq</td><td>Quiescent current</td><td>all clocks off, @ 85 °C</td><td></td><td>&lt; 0.1</td><td></td><td>μA</td></tr><tr><td>Io</td><td>Operating current</td><td>TOF_UP/DOWN, 1/s Temperature average, PT1000, 1/30s</td><td></td><td>1.1
0.15</td><td></td><td>μA</td></tr><tr><td>Voh</td><td>High level output voltage</td><td>Ioh= tbd mA Vio=Min.</td><td>0.8Vio</td><td></td><td></td><td>V</td></tr><tr><td>Vol</td><td>Low level output voltage</td><td>Iol = tbd mA, Vio=Min</td><td></td><td></td><td>0.2Vio</td><td>V</td></tr><tr><td>Vih</td><td>High level input voltage</td><td>LVTTL Level, Vio = Max.</td><td>0.7Vio</td><td></td><td></td><td>V</td></tr><tr><td>Vil</td><td>Low level input voltage</td><td>LVTTL Level, Vio = Min.</td><td></td><td></td><td>0.3Vio</td><td>V</td></tr><tr><td>Vth</td><td>High level Schmitt trigger voltage</td><td></td><td>0.7Vio</td><td></td><td></td><td>V</td></tr><tr><td>VtI</td><td>Low level Schmitt trigger voltage</td><td></td><td></td><td></td><td>0.3Vio</td><td>V</td></tr><tr><td>Vh</td><td>Schmitt trigger hysteresis</td><td></td><td></td><td>0.28</td><td></td><td>V</td></tr></table>

# Terminal Capacitance

<table><tr><td rowspan="2">Symbol</td><td rowspan="2">Terminal</td><td rowspan="2">Condition</td><td colspan="3">Rated Value</td><td rowspan="2">Unit</td></tr><tr><td>Min.</td><td>Typ.</td><td>Max.</td></tr><tr><td>Ci</td><td>Digital input</td><td rowspan="3">measured @ Vcc = Vio, f = 1 MHz, Ta = 25°C</td><td></td><td>7</td><td></td><td rowspan="3">pF</td></tr><tr><td>Co</td><td>Digital output</td><td></td><td></td><td></td></tr><tr><td>Cio</td><td>Bidirectional</td><td></td><td>9</td><td></td></tr><tr><td></td><td>PT ports</td><td></td><td></td><td>t.b.d.</td><td></td><td></td></tr><tr><td></td><td>Analog in</td><td></td><td></td><td>t.b.d.</td><td></td><td></td></tr></table>

# Analog Frontend

<table><tr><td rowspan="2">Symbol</td><td rowspan="2">Terminal</td><td rowspan="2">Condition</td><td colspan="3">Rated Value</td><td rowspan="2">Unit</td></tr><tr><td>Min.</td><td>Typ.</td><td>Max.</td></tr><tr><td></td><td>Comparator input offset voltage (chopper stabilized)</td><td></td><td></td><td>&lt; 1</td><td>2</td><td>mV</td></tr><tr><td>Rdson(AS)</td><td>Switch-on resistance of analog switches at STOP1/STOP2 inputs</td><td></td><td></td><td>200</td><td></td><td>Ohm</td></tr><tr><td>Rdson(FIRE)</td><td>Switch-on resistance of FIRE_UP, FIRE_DOWN output buffers</td><td>Symmetrical outputs, 
Rdson(HIGH) = 
Rdson(LOW)</td><td></td><td>4</td><td></td><td>Ohm</td></tr><tr><td>Ifire</td><td>Output current FIRE_UP, 
FIRE_DOWN output buffers</td><td></td><td></td><td>48</td><td></td><td>mA</td></tr></table>

# EEPROM

<table><tr><td>Symbol</td><td>Terminal</td><td>Condition</td><td>Minimum Value</td><td>Unit</td></tr><tr><td rowspan="2"></td><td rowspan="2">Data retention @ 85°C</td><td>normal</td><td>10</td><td>years</td></tr><tr><td>with Error correction</td><td>practically endless</td><td></td></tr></table>

# 2.2 Converter Specification

Time Measuring Unit ${ \left\{ \big \| \mathbf { I } _ { \mathrm { i 0 } } = \mathbf { U } _ { \mathrm { c c } } = 3 . \mathbf { 0 } \ \right.}  $ V, $\bar { \mathbf { I } } _ { \mathrm { j } } = \mathbf { 2 5 } ^ { \circ } \mathbf { [ [ \bar { \mathbf { z } } ] ] }$

<table><tr><td rowspan="2">Symbol</td><td rowspan="2">Terminal</td><td rowspan="2">Condition</td><td colspan="3">Rated Value</td><td rowspan="2">Unit</td></tr><tr><td>Min.</td><td>Typ.</td><td>Max.</td></tr><tr><td rowspan="2">LSB</td><td rowspan="2">Resolution (BIN-Size)</td><td>Measurement mode 1 &amp; 2: DOUBLE_RES = 0 DOUBLE_RES = 1</td><td></td><td>9045</td><td></td><td>ps</td></tr><tr><td>Measurement mode 2: QUAD_RES = 1</td><td></td><td>22</td><td></td><td>ps</td></tr><tr><td rowspan="2"></td><td>Standard deviation Measurement Mode 1</td><td>DOUBLE_RES = 0 Delay = 200ns Delay = 1μs DOUBLE_RES = 1 Delay = 200ns</td><td></td><td>457235</td><td></td><td>ps</td></tr><tr><td>Standard deviation Measurement Mode 2</td><td>DOUBLE_RES = 0 Delay = 2μs Delay = 100μs DOUBLE_RES = 1 Delay = 2μs Delay = 100μs QUAD_RES = 1 Delay = 2μs Delay = 100μs</td><td></td><td>547050623962</td><td></td><td>ps</td></tr><tr><td>tm</td><td>Measurement range</td><td>Measurement mode 1</td><td>3.5 ns</td><td></td><td>2.4 μs=26224*LSB</td><td></td></tr><tr><td></td><td></td><td>Measurement mode 2</td><td>700 ns</td><td></td><td>4 ms</td><td></td></tr><tr><td>INL</td><td>Integral Non-linearity</td><td></td><td></td><td>&lt; 0.1</td><td></td><td>LSB</td></tr><tr><td>DNL</td><td>Differential Non-linearity</td><td></td><td></td><td>&lt; 0.8</td><td></td><td>LSB</td></tr></table>


Figure 2-1 Relative Variation of un-calibrated least significant bit with temperature and supplyvoltage, reference 3.0V/25°C


![](images/ffcbb6dd6f210676843b161b9519696e13f3f746abf71637def5f69050421846.jpg)



1 All values measured at $\mathsf { V i o } = \mathsf { V c c } = 3 . 0 \mathrm { ~ V ~ }$ , Cload $=$ 100 nF for PT1000 and 200 nF forPT500 (C0G-type)



Temperature Measuring Unit1



2 measured with external 74AHC14 Schmitt trigger


<table><tr><td>Symbol</td><td colspan="2">Terminal</td><td colspan="2">Internal Schmitt trigger</td><td colspan="2">external Schmitt trigger2</td><td>Unit</td></tr><tr><td></td><td colspan="2"></td><td>PT500</td><td>PT1000</td><td>PT500</td><td>PT1000</td><td></td></tr><tr><td></td><td colspan="2">Resolution RMS</td><td>17.5</td><td>17.5</td><td>16.0</td><td>16.0</td><td>Bit</td></tr><tr><td></td><td colspan="2">SNR</td><td>105</td><td>105</td><td>96</td><td>96</td><td>dB</td></tr><tr><td></td><td colspan="2">Absolute Gain3</td><td>0.9912</td><td>0.9931</td><td>0.9960</td><td>0.9979</td><td></td></tr><tr><td></td><td></td><td>3.6 V</td><td>0.9923</td><td>0.9940</td><td>0.9962</td><td>0.9980</td><td></td></tr><tr><td></td><td>Absolute Gain vs. Vio3</td><td>3.0 V</td><td>0.9912</td><td>0.9931</td><td>0.9960</td><td>0.9979</td><td></td></tr><tr><td></td><td></td><td>2.5 V</td><td>0.9895</td><td>0.9915</td><td>0.9956</td><td>0.9979</td><td></td></tr><tr><td></td><td colspan="2">Gain-Drift vs. Vio</td><td>0,25</td><td>0.23</td><td>0.06</td><td>0.04</td><td>%/V</td></tr><tr><td></td><td colspan="2">max. Gain Error (@ dΘ = 100 K)</td><td>0,05%</td><td>0,05%</td><td>0,02%</td><td>&lt; 0.01%</td><td></td></tr><tr><td></td><td colspan="2">Gain-Drift vs. Temp</td><td>0.022</td><td>0.017</td><td>0.012</td><td>0.0082</td><td>%/10 K</td></tr><tr><td></td><td colspan="2">Gain-Drift vs. Vio</td><td></td><td></td><td>0,08</td><td></td><td>%/V</td></tr><tr><td></td><td colspan="2">Initial Zero Offset</td><td>&lt; 20</td><td>&lt;10</td><td>&lt; 20</td><td>&lt; 10</td><td>mK</td></tr><tr><td></td><td colspan="2">Offset Drift vs. Temp</td><td>&lt; 0.05</td><td>&lt; 0.03</td><td>&lt; 0,012</td><td>&lt; 0.0082</td><td>mK/ °C</td></tr><tr><td></td><td colspan="2">PSRR</td><td></td><td></td><td>&gt;100</td><td></td><td>dB</td></tr></table>


3 compared to an ideal gain of 1


# 2.3 Timings

At $\mathsf { V c c } = 3 . 0 \mathsf { V } \pm \mathsf { O } . 3 \mathsf { V }$ , ambient temperature -40 °C to $+ 8 5 ~ ^ { \circ } \complement$ unless otherwise specified

# Oscillator

<table><tr><td>Symbol</td><td>Parameter</td><td>Min.</td><td>Typ.</td><td>Max.</td><td>Unit</td></tr><tr><td>Clk32</td><td>32 kHz reference oscillator</td><td></td><td>32,768</td><td></td><td>kHz</td></tr><tr><td>t32st</td><td>32 kHz oscillator start-up time after power-up</td><td></td><td>250</td><td></td><td>ms</td></tr><tr><td>ClkHS</td><td>High-speed reference oscillator</td><td>2</td><td>4</td><td>8</td><td>MHz</td></tr><tr><td>toszst</td><td>Oscillator start-up time with ceramic resonator</td><td></td><td>100</td><td></td><td>μs</td></tr><tr><td>toszst</td><td>Oscillator start-up time with crystal oscillator</td><td></td><td>3</td><td></td><td>ms</td></tr></table>

# Note:

It is strongly recommended to use a ceramic oscillator. Exactly because a quartz needsmuch longer to settle than a ceramic oscillator. This costs a lot current, but using aquartz oscillator has no advantage.

# Serial Interface

<table><tr><td rowspan="2">Symbol</td><td rowspan="2">Parameter</td><td colspan="2">Max. @ Vio =</td><td rowspan="2">Unit</td></tr><tr><td>2.5 V</td><td>3.3 V</td></tr><tr><td>fclk</td><td>Serial clock frequency</td><td>15</td><td>20</td><td>MHz</td></tr></table>

<table><tr><td rowspan="2">Symbol</td><td rowspan="2">Parameter</td><td colspan="2">Min. @ \(V_{io}\)=</td><td rowspan="2">Unit</td></tr><tr><td>2.5 V</td><td>3.3 V</td></tr><tr><td>tpwh</td><td>Serial clock, pulse width high</td><td>30</td><td>25</td><td>ns</td></tr><tr><td>tpwl</td><td>Serial clock, pulse width low</td><td>30</td><td>25</td><td>ns</td></tr><tr><td>tsussen</td><td>SSN enable to valid latch clock</td><td>40</td><td>10</td><td>ns</td></tr><tr><td>tpwssn</td><td>SSN pulse width between write cycles</td><td>50</td><td>40</td><td>ns</td></tr><tr><td>thssn</td><td>SSN hold time after SCLK falling</td><td>40</td><td>25</td><td>ns</td></tr><tr><td>tsud</td><td>Data set-up time prior to SCLK falling</td><td>5</td><td>5</td><td>ns</td></tr><tr><td>thd</td><td>Data hold time before SCLK falling</td><td>5</td><td>5</td><td>ns</td></tr></table>

<table><tr><td rowspan="2">Symbol</td><td rowspan="2">Parameter</td><td colspan="2">Max. @ Vio =</td><td rowspan="2">Unit</td></tr><tr><td>2.5 V</td><td>3.3 V</td></tr><tr><td>tvd</td><td>Data valid after SCLK rising</td><td>20</td><td>16</td><td>ns</td></tr></table>


Serial Interface (SPI compatible, Clock Phase Bit =1, Clock Polarity Bit $= \boldsymbol { \mathrm { 0 1 } }$ ):


![](images/9fdb869020559b50398ef4325ad1dbd98d6c36848145b23071743896a7b3de31.jpg)



Figure 2-2 SPI Write


![](images/d3321acefd0a7e920567cf54487635488cf1011b15aa9e0f373dbc57382d38a7.jpg)



Figure 2-3 SPI Read


# Disable Timings

![](images/5d7d0687f84594bcaefbacabe52988f1ddf7537633d552ebfba87bac7d30af6c.jpg)


![](images/c96a5a8829532490befd11a186ac5163d9163d3defeeac5231e796139abd0b19.jpg)



Figure 2-4 Disable Timings


<table><tr><td>Spec</td><td>Description</td><td>Measurement mode 1</td><td>Measurement mode 2</td></tr><tr><td>tS-EN</td><td>Enable Setup Time</td><td>0 ns</td><td>0 ns</td></tr><tr><td>tSH-EN</td><td>Enable Hold Time</td><td>1.5 ns</td><td>3.0 ns</td></tr></table>

# Reset Timings

![](images/4613556a81b04a5db972a3ed4b946af365bae1d3c5000198e49da8a58ee3e55e.jpg)



Figure 2-5 Reset Timings


<table><tr><td>Spec</td><td>Description</td><td>Typ. Min</td></tr><tr><td>tph</td><td>Reset pulse width</td><td>50 ns</td></tr><tr><td>trfs</td><td>Time after rising edge of reset pulse before further communication</td><td>200 ns</td></tr><tr><td></td><td>Time after rising edge of reset pulse before analog section is ready</td><td>500 μs</td></tr></table>

# 2.4 Pin Description

![](images/ffa5ac90df5bb89787e7b145056ae34585d607c7294730a8488e48515eb9c2fe.jpg)



Figure 2-6 TDC-GP22 Pinout


<table><tr><td>No.</td><td>Name</td><td>Description</td><td>Buffer type</td><td>Value</td><td>If not used</td></tr><tr><td>1</td><td>XIN</td><td>Oscillator driver in</td><td></td><td></td><td>GND</td></tr><tr><td>2</td><td>XOUT</td><td>Oscillator driver out</td><td></td><td></td><td></td></tr><tr><td>3</td><td>VIO</td><td>I/O - supply voltage</td><td></td><td></td><td></td></tr><tr><td>4</td><td>GND</td><td>Ground</td><td></td><td></td><td></td></tr><tr><td>5</td><td>FIRE_UP</td><td>Fire pulse generator output 1</td><td>48 mA</td><td></td><td></td></tr><tr><td>6</td><td>FIRE_DOWN</td><td>Fire pulse generator output 2</td><td>48 mA</td><td></td><td></td></tr><tr><td>7</td><td>FIRE_IN</td><td>Diagnostics output</td><td></td><td></td><td>GND</td></tr><tr><td>8</td><td>INTN</td><td>Interrupt flag</td><td>4 mA</td><td>LOW active</td><td></td></tr><tr><td>9</td><td>SSN</td><td>Slave select</td><td></td><td>LOW active</td><td></td></tr><tr><td>10</td><td>SCK</td><td>Clock serial interface</td><td></td><td></td><td></td></tr><tr><td>11</td><td>SI</td><td>Data input serial interface</td><td></td><td></td><td></td></tr><tr><td>12</td><td>SO</td><td>Data output serial interface</td><td>4 mA tristate</td><td></td><td></td></tr><tr><td>13</td><td>RSTN</td><td>Reset input</td><td></td><td>LOW active</td><td></td></tr><tr><td>14</td><td>VCC</td><td>Core supply voltage</td><td></td><td></td><td></td></tr><tr><td>15</td><td>CLK32OUT</td><td>Output 32 kHz clock generator</td><td></td><td></td><td>n. c.</td></tr><tr><td>16</td><td>CLK32IN</td><td>Input 32 kHz clock generator</td><td></td><td></td><td>GND</td></tr><tr><td>17</td><td>SENSET</td><td>Sense input temperature measurement</td><td>Schmitt trigger</td><td></td><td>GND</td></tr><tr><td>18</td><td>LOADT</td><td>Load output temperature measurement</td><td>24 mA</td><td></td><td>n.c.</td></tr><tr><td>19</td><td>PT4*</td><td>Port 4 temperature measurement</td><td>&gt;96 mA open drain</td><td></td><td></td></tr><tr><td>20</td><td>PT3*</td><td>Port 3 temperature measurement</td><td>&gt;96 mA open drain</td><td></td><td></td></tr><tr><td>21</td><td>GND</td><td>Ground</td><td></td><td></td><td></td></tr><tr><td>22</td><td>VIO</td><td>I/O - supply voltage</td><td></td><td></td><td></td></tr><tr><td>23</td><td>PT2*</td><td>Port 2 temperature measurement</td><td>&gt;96 mA open drain</td><td></td><td></td></tr><tr><td>24</td><td>PT1*</td><td>Port 1 temperature measurement</td><td>&gt;96 mA open drain</td><td></td><td></td></tr><tr><td>25</td><td>EN_STOP2</td><td>Enable pin stop input 2</td><td></td><td>HIGH active</td><td>VIO</td></tr><tr><td>26</td><td>EN_STOP1</td><td>Enable pin stop input 1</td><td></td><td>HIGH active</td><td>VIO</td></tr><tr><td>27</td><td>STOP2</td><td>Stop input 2</td><td></td><td></td><td>GND</td></tr><tr><td>28</td><td>GND</td><td>Ground</td><td></td><td></td><td></td></tr><tr><td>29</td><td>VCC</td><td>Core supply voltage</td><td></td><td></td><td></td></tr><tr><td>30</td><td>STOP1</td><td>Stop input 1</td><td></td><td></td><td>GND</td></tr><tr><td>31</td><td>START</td><td>Start input</td><td></td><td></td><td></td></tr><tr><td>32</td><td>EN_START</td><td>Enable pin start input</td><td></td><td>HIGH active</td><td>VIO</td></tr></table>


* RDSON temperature ports: typ. 1.8 Ω @ 3.0 V


# 2.5 Package Drawings

![](images/9cdf65497fd7e9eac0667f4e317277c7ef79787db4f9eac628c2bd809623b8e9.jpg)


![](images/f38b3b45668abff4f35a4e2f3f714e8d930c1a3a14dc13463354bdf84f1ac482.jpg)



Figure 2-7 QFN-32 package outline, $5 \times 5 \times 0 . 9 \mathsf { m m } ^ { 3 }$ , 0.5 mm lead pitch


Caution: Center pad, $3 . 7 0 \cdot 3 . 7 0 \mathrm { m m } ^ { 2 }$ , is internally connected to GND. No wires otherthan GND are allowed underneath. It is not necessary to connect the center pad to GND.

Suitable socket: Plastronics 32QN50S15050D

# Landing Pattern:

![](images/1edefdc66dc6f12d3d60b2908b3347d156dca0aa6995a669aa6a537112a1924e.jpg)



Figure 2-8


Thermal resistance: Roughly 28 K/W (value just for reference).

Environmental: The package is RoHS compliant and does not contain any Pb.

# Moisture Sensitive Level (MSL)

Based on JEDEC 020 Moisture Sensitivity Level definition the TDC-GP22 is classified asMSL 1.

# Soldering Temperature Profile

The temperature profile for infrared reflow furnace (in which the temperature is the resin’ssurface temperature) should be maintained within the range described below.

![](images/c2f69faa58e75371731daa7bd86d76469d36dedef773adb73d042518cff0ed89.jpg)



Figure 2-9 Soldering profile


# Maximum temperature

The maximum temperature requirement for the resin surface, given $2 6 0 ^ { \circ } \mathrm { C }$ as the peaktemperature of the package body’s surface, is that the resin surface temperature mustnot exceed $2 5 0 ^ { \circ } \mathrm { C }$ for more than 10 seconds. This temperature should be kept as low aspossible to reduce the load caused by thermal stress on the package, which is whysoldering for short periods only is recommended. In addition to using a suitabletemperature profile, we also recommend that you check carefully to confirm goodsoldering results.

Date Code: YYWWA: YY $=$ Year, WW $=$ week, A = Assembly site code

# 2.6 Power Supply

# Supply voltage

TDC-GP22 is a high end mixed analog/digital device. To reach full performance of the chipa good power supply is mandatory. It should be high capacitive and of low inductance.

The TDC-GP22 provides two pairs of power supply terminals:

Vio - I/O supply voltage

Vcc - Core supply voltage

![](images/6c6c35adc22ce4a85c0c143d325ea5ab91a72dba236f4cfe9a9f25ce6779014e.jpg)



Figure 2-10


Both voltages should be applied with low series resistance from the same source. On thechip there are connected, but a separate external connection is recommended for goodmeasurement quality. All ground pins should be connected to a ground plane on the

printed circuit board. Vio and Vcc should be provided by a battery or fixed linear vol tageregulator. Do not use switched regulators to avoid disturbances caused by the I/O supply.

Vio and Vcc are connected internally on the chip. The resistance between both is in therange of several Ohms. However, Vio is connected to the pads with significantly lowerimpedance and therefore can provide this better than Vcc.

The measurement quality of a time-to-digital converter depends on a good power supply.The chip sees mainly pulsed current and therefore a sufficient bypassing is mandatory:

Vcc 47 to 100 µF (minimum 22 µF)

Vio 100 µF (minimum 22 µF)

The supply voltage should be provided through analog regulators. We strongly recommendnot to use switch mode power supplies.

# Current consumption

The current consumption is the sum from different parties (all data for $\mathsf { V i o } = \mathsf { V c c } = 3 . 0 \mathsf { V } ]$ :

Iddq < 5 nA typ. $@ 3 . 0 \lor$ ,  Quiescent current, no 32 kHz oscillator running25°C

I32 typ. 1.0 µA Standby current with active 32 kHz oscillator (GP22 waiting forcommand).

Ihs typ. 130 µA/s Current into the high speed oscillator at 3.0 V Vio.

Example: In ultrasonic flow-meters the high-speed oscillator is on forabout 2ms only.

The average current consumption is $1 3 0 ~ \mu \ A / \sigma ^ { \mathrm { ~ \star ~ } } 2 ~ \mathsf { m s } = 0 . 2 6 ~ \mu \mathsf { A }$

Itmu typ. 4 mA/s Current into the time measuring unit, In measurement mode 1

* (active measuring The time measuring unit is active for the start-stop time interval plustime) the calibration time interval of 2 periods of the reference clock permeasurement.

In measurement mode 2 the time measuring unit is on for average 4periods of the reference clock per measurement, two for the timemeasurement and two for calibration.

Example: With 10 measurements per second in measurement mode2 and a 4 MHz reference clock the time measuring unit is active for

only about ${ \mathsf { 1 0 } } \ \mu \mathbf { s }$ .

The average current is $4 ~ \mathrm { m A / s } ~ { \star } ~ 1 0 ~ \mu \mathrm { s } = 0 . 0 4 0 ~ \mu \mathrm { A } .$ .

IT typ. 2.5 µAs

* measure rate

The current for a full temperature measurement is typ. $2 . 5 \mu \mathsf { A s }$ .

In heat-meters the temperature is measured typically once every 30seconds. The average current is about 0.085 µA

Iana typ. 0.8 mA

Current consumption of the integrated analog part of TDC-GP22

during a Time-of-flight (ToF) measurement. The analog part is activefor a duration of 250 µs + ToF.

Itotal 2.3 µA

In a typical ultrasonic heat meter application, the flow is measuredtwice per second. The temperature is measured every 30 seconds

Typical current consumption of the complete flow and temperaturemeasuring unit, including the analog part, the transducers and PTsensors.

# 3 Registers & Communication

# 3.1 Configuration registers

The TDC-GP22 has 7 configuration registers with 32 bit. The upper 24 bit are used forconfiguration and are write only. They are used to setup the TDC-GP22 operating mode.The lowest 8 bit can be used e.g. as an ID and can be read back.

For communication test please write to register 1 and read back the highest 8 bit fromaddress 5.

# Note:

The write registers of TDC-GP22 are fully upwards compatible with TDC-GP21. In addition,the formerly unused bits 30, 31 in register 3 activate new functionality. Especially with bit30 the First Wave Mode is switched on and the parameter bits DELVAL2 and DELVAL3 inregisters 3 and 4 get a second meaning.

For proper work of TDC-GP22, a power-up reset via pin or SPI command is necessary afterthe power-up of the circuit.

# 3.1.1 Alphanumeric listing of configuration parameters


Table 3-1: Configuration Parameters


<table><tr><td>Parameter</td><td>Register</td><td>Bits</td><td>Default value</td></tr><tr><td>ANZ_FAKE</td><td>0</td><td>15</td><td>0</td></tr><tr><td>ANZ FIRE [3:0] [6:4]</td><td>0 6</td><td>28-31 8-10</td><td>2</td></tr><tr><td>ANZ_PER_CALRES</td><td>0</td><td>22,23</td><td>0</td></tr><tr><td>ANZ_PORT</td><td>0</td><td>17</td><td>1</td></tr><tr><td>CALIBRATE</td><td>0</td><td>13</td><td>1</td></tr><tr><td>CON_FIRE</td><td>5</td><td>28-31</td><td>0</td></tr><tr><td>CURR32K</td><td>1</td><td>15</td><td>0</td></tr><tr><td>CYCLE_TEMP</td><td>6</td><td>18,19</td><td>0</td></tr><tr><td>CYCLE_TOF</td><td>6</td><td>16,17</td><td>0</td></tr><tr><td>DA_KORR</td><td>6</td><td>25-28</td><td>0</td></tr><tr><td>DELREL1</td><td>3</td><td>8-13</td><td>0</td></tr><tr><td>DELREL2</td><td>3</td><td>14-19</td><td>0</td></tr><tr><td>DELREL3</td><td>3</td><td>20-25</td><td>0</td></tr><tr><td>DELVAL1</td><td>2</td><td>8-23</td><td>0</td></tr><tr><td>DELVAL2</td><td>3</td><td>8-23</td><td>0</td></tr><tr><td>DELVAL3</td><td>4</td><td>8-23</td><td>0</td></tr><tr><td>DIS_PHASESHIFT</td><td>5</td><td>27</td><td>0</td></tr><tr><td>DIS_PWM</td><td>4</td><td>16</td><td>0</td></tr><tr><td>DIV_CLKHS</td><td>0</td><td>20,21</td><td>0</td></tr><tr><td>DIV_FIRE</td><td>0</td><td>24-27</td><td>2</td></tr><tr><td>DOUBLE_RES</td><td>6</td><td>12</td><td>0</td></tr><tr><td>EDGE_HW</td><td>4</td><td>15</td><td>0</td></tr><tr><td>EN_ANALOG</td><td>6</td><td>31</td><td>0</td></tr><tr><td>EN_AUTOCALC_MB2</td><td>3</td><td>31</td><td>0</td></tr><tr><td>EN_ERR_VAL</td><td>3</td><td>29</td><td>0</td></tr><tr><td>EN_FAST_INIT</td><td>1</td><td>23</td><td>0</td></tr><tr><td>EN_FIRST_WAVE</td><td>3</td><td>30</td><td>0</td></tr><tr><td>EN_INT [2:0] [3]</td><td>2 6</td><td>29-31 21</td><td>1</td></tr><tr><td>EN_STARTNOISE</td><td>5</td><td>28</td><td>0</td></tr><tr><td>FIREO_def</td><td>6</td><td>14</td><td>0</td></tr><tr><td>HIT1</td><td>1</td><td>24-27</td><td>5</td></tr><tr><td>HIT2</td><td>1</td><td>28-31</td><td>5</td></tr><tr><td>HITIN1</td><td>1</td><td>16-18</td><td>0</td></tr><tr><td>HITIN2</td><td>1</td><td>19-21</td><td>0</td></tr><tr><td>HZ60</td><td>6</td><td>15</td><td>0</td></tr><tr><td>IDO</td><td>0</td><td>0-7</td><td>0</td></tr><tr><td>ID1</td><td>1</td><td>0-7</td><td>0</td></tr><tr><td>ID2</td><td>2</td><td>0-7</td><td>0</td></tr><tr><td>ID3</td><td>3</td><td>0-7</td><td>0</td></tr><tr><td>ID4</td><td>4</td><td>0-7</td><td>0</td></tr><tr><td>ID5</td><td>5</td><td>0-7</td><td>0</td></tr><tr><td>ID6</td><td>6</td><td>0-7</td><td>0</td></tr><tr><td>MESSB2</td><td>0</td><td>11</td><td>1</td></tr><tr><td>NEG_START</td><td>0</td><td>8</td><td>0</td></tr><tr><td>NEG_STOP_TEMP</td><td>6</td><td>30</td><td>0</td></tr><tr><td>NEG_STOP1</td><td>0</td><td>9</td><td>0</td></tr><tr><td>NEG_STOP2</td><td>0</td><td>10</td><td>0</td></tr><tr><td>NO_CAL_AUTO</td><td>0</td><td>12</td><td>0</td></tr><tr><td>OFFS</td><td>4</td><td>8-12</td><td>0</td></tr><tr><td>OFFSRNG1</td><td>4</td><td>13</td><td>0</td></tr><tr><td>OFFSRNG2</td><td>4</td><td>14</td><td>0</td></tr><tr><td>PHFIRE</td><td>5</td><td>8-23</td><td>0</td></tr><tr><td>QUAD_RES</td><td>6</td><td>13</td><td>0</td></tr><tr><td>REPEAT FIRE</td><td>5</td><td>24-26</td><td>0</td></tr><tr><td>RFEDGE1</td><td>2</td><td>27</td><td>0</td></tr><tr><td>RFEDGE2</td><td>2</td><td>28</td><td>0</td></tr><tr><td>SEL_ECLK(tmp)</td><td>0</td><td>14</td><td>1</td></tr><tr><td>SEL_START FIRE</td><td>1</td><td>14</td><td>0</td></tr><tr><td>SEL_TIMO_MB2</td><td>3</td><td>27,28</td><td>3</td></tr><tr><td>SEL_TST01</td><td>1</td><td>8-10</td><td>0</td></tr><tr><td>SEL_TST02</td><td>1</td><td>11-13</td><td>0</td></tr><tr><td>START_CLKHS [1:0] [2]</td><td>0 6</td><td>18,19 20</td><td>1</td></tr><tr><td>TCYCLE</td><td>0</td><td>16</td><td>0</td></tr><tr><td>TEMP_PORTDIR</td><td>6</td><td>11</td><td>0</td></tr><tr><td>TW2</td><td>6</td><td>22,23</td><td>0</td></tr></table>

# 3.1.2 List of configuration registers

Bit number 

Parameter

Default value 

<table><tr><td>15</td><td>14</td><td>13</td><td>12</td><td>11</td><td>10</td><td>9</td><td>8</td><td>7</td><td>6</td><td>5</td><td>4</td><td>3</td><td>2</td><td>1</td><td>0</td></tr><tr><td rowspan="2" colspan="2"></td><td rowspan="2" colspan="4">param1</td><td colspan="6">k.d.</td><td></td><td></td><td></td><td></td></tr><tr><td>1</td><td>1</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td></tr></table>

k.d. $=$ keep default values

# Register 0 (address 0):

<table><tr><td>31</td><td>30</td><td>29</td><td>28</td><td>27</td><td>26</td><td>25</td><td>24</td><td>23</td><td>22</td><td>21</td><td>20</td><td>19</td><td>18</td><td>17</td><td>16</td><td>15</td><td>14</td><td>13</td><td>12</td><td>11</td><td>10</td><td>9</td><td>8</td><td>7-0</td><td></td></tr><tr><td colspan="4">ANZ FIRE[3:0]</td><td colspan="4">DIV_FIRE</td><td colspan="2"></td><td colspan="2"></td><td colspan="2"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td>IDO</td><td></td></tr><tr><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>1</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td></td></tr><tr><td colspan="4">Parameter</td><td colspan="10">Description</td><td colspan="11">Settings</td><td></td></tr><tr><td colspan="4">ANZ FIRE[3:0]</td><td colspan="10">Sets number of pulses generated by fire pulse generator. Additional 3 bits are set in register 6.For values ANZ FIRE &gt; 15 the phase setting (PHFIRE) can not be used.</td><td colspan="12">ON-PORT TACYCLE NO CAL AUTO NEG-STOP2 NEG-START</td></tr><tr><td colspan="4">DIV FIRE</td><td colspan="10">Sets predivider for internal clock signal of fire pulse generator</td><td colspan="11">0 = off1 = 1 pulse2 = 2 pulses...127 = 127 pulses</td><td></td></tr><tr><td colspan="4">ANZ_PER_CALRES</td><td colspan="10">Sets number of periods used for calibrating the ceramic resonator</td><td colspan="11">0 = not permitted1 = divided by 22 = divided by 33.= divided by 4...15 = divided by 16</td><td></td></tr><tr><td colspan="4">DIV_CLKHS</td><td colspan="10">Sets predivider for CLKHS</td><td colspan="11">0 = 2 periods = 61.035 μs1 = 4 periods = 122.07 μs2 = 8 periods = 244.14 μs3 = 16 periods = 488.281 μs</td><td></td></tr><tr><td colspan="4">START_CLKHS[1:0]</td><td colspan="10">Defines the time interval the chip waits after switching on the oscillator before making a measurement.Note:The highest bit to adjust START_CLKS is located in register 6, bit 20. This has to be set to 1 for settling times of 2.44 ms and</td><td colspan="10">0 = Oscillator off1 = Oscillator continuously on2 = settling time 480 μs3 = settling time 1.46 ms4 = settling time 2.44 ms5 to 7 = settling time 5.14 ms</td><td></td><td></td></tr></table>

<table><tr><td></td><td>5.14 ms.</td><td></td></tr><tr><td>ANZ_PORT</td><td>Sets number of ports used for temperature measurement</td><td>0 = 2 temperature ports (PT1 and PT2)1 = 4 temperature ports</td></tr><tr><td>TCYCLE</td><td>Sets cycle time for temperature measurement</td><td>0 = 128 μs cycle time @ 4 MHz1 = 512 μs cycle time @ 4 MHz(recommended)</td></tr><tr><td>ANZ_FAKE</td><td>Number of dummy cycles at the beginning of a temperature measurement</td><td>0 = 2 Fake measurements1 = 7 Fake measurements</td></tr><tr><td>SEL_ECLK_CMP</td><td>Select reference signal for internal cycle clock for temperature measurement</td><td>0 = use 32.768 kHz as cycle clock1 = use 128 * CLKHS as period for cycle clock (32 μs with 4 MHz high speed clock signal)</td></tr><tr><td>CALIBRATE</td><td>Enables/disables calibration calculation in the ALU</td><td>0 = calculation of calibrated results off (allowed only in measurement mode 1)1 = calculation of calibrated results on (recommended)</td></tr><tr><td>NO_CAL_AUTO</td><td>Enables/disables auto-calibration run in the TDC</td><td>0 = auto-calibration after measurement1 = auto-calibration disabled</td></tr><tr><td>MESSB2</td><td>Switch to measurement mode 2</td><td>0 = measurement mode 11 = measurement mode 2</td></tr><tr><td>NEG_STOP2</td><td>Negation stop 2 input</td><td>0 = non-inverted input signal - rising edge1 = inverted input signal - falling edge</td></tr><tr><td>NEG_STOP1</td><td>Negation stop 1 input</td><td>0 = non-inverted input signal - rising edge1 = inverted input signal - falling edge</td></tr><tr><td>NEG_START</td><td>Negation start input</td><td>0 = non-inverted input signal - rising edge1 = inverted input signal - falling edge</td></tr><tr><td>IDO</td><td>Free bits, e.g. to be used as identification or version number</td><td></td></tr></table>


Register 1 (address 1):


<table><tr><td>31</td><td>30</td><td>29</td><td>28</td><td>27</td><td>26</td><td>25</td><td>24</td><td>23</td><td>22</td><td>21</td><td>20</td><td>19</td><td>18</td><td>17</td><td>16</td><td>15</td><td>14</td><td>13</td><td>12</td><td>11</td><td>10</td><td>9</td><td>8</td><td>7-0</td></tr><tr><td colspan="4">HIT2</td><td colspan="4">HIT1</td><td></td><td></td><td colspan="3">HITIN2</td><td colspan="3">HITIN1</td><td></td><td></td><td colspan="3">SEL_TST02</td><td colspan="3">SEL_TST01</td><td>ID1</td></tr><tr><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr><tr><td colspan="4">Parameter</td><td colspan="9">Description</td><td colspan="12">Settings</td></tr><tr><td colspan="4">HIT2</td><td colspan="10">Defines operator for ALU data post-processingMeasurement mode 1: HIT1-HIT2Measurement mode 2: HIT2-HIT1</td><td colspan="7">Measurementmode 1:0 = Start1 = 1. Stop Ch12 = 2. Stop Ch13 = 3. Stop Ch14 = 4. Stop Ch15 = no action6 = Cal1 Ch17 = Cal2 Ch19 = 1. Stop Ch2A = 2. Stop Ch2B = 3. Stop Ch2C = 4. Stop Ch2</td><td>Measurementmode 2:2 = 1. Stop Ch13 = 2. Stop Ch14 = 3. Stop Ch1</td><td></td><td></td><td></td></tr><tr><td colspan="4">HIT1</td><td colspan="10">Defines operator for ALU data post-processingMeasurement mode 1: HIT1-HIT2Measurement mode 2: HIT2-HIT1</td><td colspan="7">Measurementmode 1:0 = Start1 = 1. Stop Ch12 = 2. Stop Ch13 = 3. Stop Ch14 = 4. Stop Ch15 = no action6 = Cal1 Ch17 = Cal2 Ch19= 1. Stop Ch2A = 2. Stop Ch2B = 3. Stop Ch2C = 4. Stop Ch2</td><td>Measurementmode 2:1 = Start</td><td></td><td></td><td></td></tr><tr><td colspan="4">EN_FAST_INIT</td><td colspan="10">Enables fast init operation</td><td colspan="11">O = Fast init mode disabled1 = Fast init mode enabled</td></tr><tr><td colspan="4">HITIN2</td><td colspan="10">Number of expected hits on channel 2</td><td colspan="11">O = stop channel 2 disabled1 = 1 hit2 = 2 hits3 = 3 hits4 = 4 hits5 to 7 = not permitted</td></tr><tr><td colspan="4">HITIN1</td><td colspan="10">Number of expected hits on channel 1</td><td colspan="11">O = stop channel 1 disabled1 = 1 hit</td></tr><tr><td colspan="4"></td><td colspan="10"></td><td colspan="11">2 = 2 hits
3 = 3 hits
4 = 4 hits
5 to 7 = not permitted</td></tr><tr><td colspan="4">CURR32K</td><td colspan="10">Low current option for 32 kHz oscillator.
Basically there is no need to use high current option [1]. Low current (0) also guarantees oscillation.</td><td colspan="11">0 = low current (recommended)
1 = high current (GP2 compatibility)</td></tr><tr><td colspan="4">SEL_START_FIRE</td><td colspan="10">Fire pulse is used as TDC start. The START input is disabled.</td><td colspan="11">0 = TDC-GP2 behavior
1 = Use FIRE as Start</td></tr><tr><td colspan="4">SEL_TST02</td><td colspan="10">Defines functionality of EN_START pin.
Besides the GP2 functionality this pin can act as output for various signals. If SEL_TST02 &gt; 0 then EN_START = HIGH internally.</td><td colspan="11">0 = GP2 functionality, High level enables the START pin.
1 = START_TDC output
2 = STOP1 TDC output
3 = STOP2 TDC output
4 = Stop Temperature measurement output
5 = “0” indicates TOF_DOWN being active, “1” indicates TOF_UP being active
6 = n.c.
7 = 4 kHz (32 kHz/8) clock</td></tr><tr><td colspan="4">SEL_TST01</td><td colspan="10">Defines functionality of FIRE_IN pin. Besides the GP2 functionality this pin can act as output for various signals. If SEL_TST01 &gt;1 the FIRE_IN is connected to GND internally.</td><td colspan="11">0 = GP2 functionality, FIRE_IN input for sing-around
1 = START_TDC output
2 = STOP1 TDC output
3 = STOP2 TDC output
4 = Start Temperature measurement output
5 = EN_STOP by DELVAL output
6 = Comparator out
7 = 32 kHz clock</td></tr><tr><td colspan="4">ID1</td><td colspan="10">Free bits, e.g. to be used as identification or version number</td><td colspan="11"></td></tr></table>


Register 2 (address 2):


<table><tr><td>31</td><td>30</td><td>29</td><td>28</td><td>27</td><td>26</td><td>25</td><td>24</td><td>23</td><td>22</td><td>21</td><td>20</td><td>19</td><td>18</td><td>17</td><td>16</td><td>15</td><td>14</td><td>13</td><td>12</td><td>11</td><td>10</td><td>9</td><td>8</td><td>7-0</td></tr><tr><td colspan="3">EN_INT[2:0]</td><td></td><td></td><td colspan="19">DELVAL1</td><td>ID2</td></tr><tr><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr></table>

<table><tr><td>Parameter</td><td>Description</td><td>Settings</td></tr><tr><td>EN_INT[2:0]</td><td>Activates interrupt sources wired by OR. Additional bit in register 6 (see there, too)</td><td>Bit 31 = Timeout interrupt enable Bit 30 = End Hits interrupt enable Bit 29 = ALU interrupt enable Reg6, BIT21 = End of EEPROM action</td></tr><tr><td>RFEDGE2</td><td>Edge sensitivity channel 2</td><td>0 = rising or falling edge 1 = rising and falling edge</td></tr><tr><td>RFEDGE1</td><td>Edge sensitivity channel 1</td><td>0 = rising or falling edge 1 = rising and falling edge</td></tr><tr><td>DELVAL1</td><td>Delay value for internal stop enable unit, hit 1 channel 1. Fixed point number with 14 integer and 5 fractional digits in multiples of Tref</td><td>DELVAL1 = 0 to 16383.96875 Mandatory: If EN_ANALOG = 0 then set DELVAL1 = 0</td></tr><tr><td>ID2</td><td>Free bits, e.g. to be used as identification or version number</td><td></td></tr></table>

Register 3 (address 3) with EN_FIRST_WAVE $\mathbf { \mu } = \pmb { \mathbb { 0 } }$ :

![](images/885c08f459070de53884c89f8017c1c04ae458e6d8aca8cb562f8e433f414ccb.jpg)


Register 3 (address 3) with EN_FIRST_WAVE $=$ 1:

![](images/997ac6862c947a7add480dc50116a57ae957f0c35853157dc5c15573113c939d.jpg)


<table><tr><td>Parameter</td><td>Description</td><td>Settings</td></tr><tr><td>EN_AUTOCALC_MB2</td><td>Only in measurement mode 2: automatic calculation of all enabled hits. The sum of the results is written to read register 4.</td><td>0 = disabled1 = enabled</td></tr><tr><td>EN_ERR_VAL</td><td>Timeout forces ALU to write &#x27;hFFFFFF into the output register</td><td>0 = disabled1 = enabled</td></tr><tr><td>EN_FIRST_WAVE</td><td>Enables the automatic first hit detection. In case this bit is set registers 3 and 4 get a new meaning</td><td>0 = disabled1 = enabled</td></tr><tr><td>SEL_TIMO_MB2</td><td>Select predivider for timeout in measurement mode 2</td><td>0 = 64 μs1 = 256 μs2 = 1024 μs3 = 4096 μs recommended@ 4 MHz CikHS</td></tr><tr><td>DELREL3</td><td>Sets the number of the periods after the first hit for the 3rd stop</td><td>5 to 63DELREL3 &gt; DELREL2</td></tr><tr><td>DELREL2</td><td>Sets the number of the periods after the first hit for the 2nd stop</td><td>4 to 63DELREL2 &gt; DELREL1</td></tr><tr><td>DELREL1</td><td>Sets the number of the periods after the first hit for the 1st stop</td><td>3 to 63</td></tr><tr><td>DELVAL2</td><td>Delay value for internal stop enable unit, hit 2 channel 1. Fixed point number with 14 integer and 5 fractional digits in multiples of Tref</td><td>DELVAL2 = 0 to 16383.96875Mandatory: If EN_ANALOG = 0 then setDELVAL2 = 0</td></tr><tr><td>ID3</td><td>Free bits, e.g. to be used as identification or version number</td><td></td></tr></table>

Register 4 (address 4) with EN_FIRST_WAVE $\mathbf { \mu } = \mathbf { \mathfrak { v } }$ :

<table><tr><td>31</td><td>30</td><td>29</td><td>28</td><td>27</td><td>26</td><td>25</td><td>24</td><td>23</td><td>22</td><td>21</td><td>20</td><td>19</td><td>18</td><td>17</td><td>16</td><td>15</td><td>14</td><td>13</td><td>12</td><td>11</td><td>10</td><td>9</td><td>8</td><td>7-0</td></tr><tr><td colspan="5">k.d.</td><td colspan="19">DELVAL3</td><td>ID4</td></tr><tr><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr></table>


Register 4 (address 4) with EN_FIRST_WAVE = 1:


<table><tr><td>31</td><td>30</td><td>29</td><td>28</td><td>27</td><td>26</td><td>25</td><td>24</td><td>23</td><td>22</td><td>21</td><td>20</td><td>19</td><td>18</td><td>17</td><td>16</td><td>15</td><td>14</td><td>13</td><td>12</td><td>11</td><td>10</td><td>9</td><td>8</td><td>7-0</td></tr><tr><td colspan="15">k.d.</td><td></td><td></td><td></td><td></td><td colspan="5">OFFS</td><td>ID4</td></tr><tr><td colspan="3">Parameter</td><td colspan="12">Description</td><td colspan="10">Settings</td></tr><tr><td colspan="3">DELVAL3</td><td colspan="12">Delay value for internal stop enable unit, hit 3 channel 1. Fixed point number with 14 integer and 5 fractional digits in multiples of Tref</td><td colspan="9">DELVAL3 = 0 to 16383.96875Mandatory: If EN_ANALOG = 0 then set DELVAL3 = 0</td><td></td></tr><tr><td colspan="3">DIS_PWM</td><td colspan="12">Disable pulse width measurement</td><td colspan="9">O = Enable pulse width measurement1 = Disable pulse width measurement</td><td></td></tr><tr><td colspan="3">EDGE_FW</td><td colspan="12">Sets the edge sensitivity for the first wave. With a negative offset it is reasonable to trigger on the falling edge of the first wave.</td><td colspan="9">O = rising edge1 = falling edge</td><td></td></tr><tr><td colspan="3">OFFSRNG2</td><td colspan="12">Additional offset shift by + 20 mV</td><td colspan="9">O = off1 = active</td><td></td></tr><tr><td colspan="3">OFFSRNG1</td><td colspan="12">Additional offset shift by - 20 mV</td><td colspan="9">O = off1 = active</td><td></td></tr><tr><td colspan="3">OFFS</td><td colspan="12">2&#x27;s complement number setting the offset shift in 1 mV steps</td><td colspan="9">O = 0 mV1 = +1 mV...15 = +15 mV16 = -16 mV17 = -15 mV...30 = -2 mV31 = -1 mV</td><td></td></tr><tr><td colspan="3">ID4</td><td colspan="12">Free bits, e.g. to be used as identification or version number</td><td colspan="9"></td><td></td></tr></table>

Note: When switching to First Wave Mode make sure that the highest 5 bits have thedefault values. Especially bit 29 has to be 1.


Register 5 (address 5):


<table><tr><td>31</td><td>30</td><td>29</td><td>28</td><td>27</td><td>26</td><td>25</td><td>24</td><td>23</td><td>22</td><td>21</td><td>20</td><td>19</td><td>18</td><td>17</td><td>16</td><td>15</td><td>14</td><td>13</td><td>12</td><td>11</td><td>10</td><td>9</td><td>8</td><td>7-0</td></tr><tr><td colspan="3"></td><td></td><td></td><td colspan="4"></td><td colspan="15">PHFIRE</td><td>ID5</td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr></table>

![](images/5ab2bd135aa5bba339a26d1e143b59695224396e2d58398fe9377a827fbbbb70.jpg)


<table><tr><td>Parameter</td><td>Description</td><td>Settings</td></tr><tr><td>CONF FIRE</td><td>Output configuration for pulse generator 3&#x27;b O11 is not allowed</td><td>Bit 31 = 1: FIRE_BOTH (inverts FIRE_DOWN) 
Bit 30 = 1: enable output FIRE_UP 
Bit 29 = 1: enable output FIRE_DOWN</td></tr><tr><td>EN_STARTNOISE</td><td>Enables additional noise for start channel</td><td>1 = switch on noise unit</td></tr><tr><td>DIS_PHASEhift</td><td>Phase noise unit. Improves statistics and should be enabled if start pulse generation is derived from the GP2 reference clock (e.g. with fire pulse generator).</td><td>1 = disables phase noise 
0 = enables phase noise unit</td></tr><tr><td>REPEAT FIRE</td><td>Number of pulse sequence repetition for &quot;quasi-sing-around&quot;</td><td>0 = no signal repetition 
1 = 1 signal repetition 
2 = 2 signal repetition 
... 
7 = 7 signal repetition</td></tr><tr><td>PHIRE</td><td>Enables phase reversing for each pulse of a sequence of up to 15 possible pulses. PHFIRE[0..14] are available.</td><td>0 = no inversion, phase jump HIGH-LOW 
1 = inversion, phase jump LOW-HIGH 
Bit 23 = 0 (mandatory)</td></tr><tr><td>ID5</td><td>Free bits, e.g. to be used as identification or version number</td><td></td></tr></table>

Register 6 (address 6):

<table><tr><td>31</td><td>30</td><td>29</td><td>28</td><td>27</td><td>26</td><td>25</td><td>24</td><td>23</td><td>22</td><td>21</td><td>20</td><td>19</td><td>18</td><td>17</td><td>16</td><td>15</td><td>14</td><td>13</td><td>12</td><td>11</td><td>10</td><td>9</td><td>8</td><td>7-0</td></tr><tr><td></td><td></td><td></td><td colspan="4"></td><td></td><td colspan="2"></td><td></td><td></td><td colspan="3"></td><td></td><td></td><td></td><td></td><td></td><td></td><td colspan="3"></td><td>ID6</td></tr><tr><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td></tr></table>

<table><tr><td>Parameter</td><td>Description</td><td>Settings</td></tr><tr><td>EN_ANALOG</td><td>Activates the analog part for the ultrasonic flow measurement is. If active, this section is powered only for the duration of the measurement to save current. STOP1 and STOP2 are analog inputs now and automatically selected by the internal multiplexer.</td><td>0 = STOP1 and STOP2 are digital inputs (TDC-GP2 compatibility) 
1 = The analog section is used. 
Mandatory: 
If EN_ANALOG = 0 then set DELVAL1 = DELVAL2 = DELVAL3 = 0</td></tr><tr><td>NEG_STOP_TEMP</td><td>Inverts the SenseT input signal. This is mandatory when the internal comparator is used instead of the external one like in TDC-GP2</td><td>0 = external 74HC14 is used (TDC-GP2 compatibility) 
1 = internal Schmitt trigger is used</td></tr><tr><td>DA_KORR</td><td>Sets comparator offset from -8 mV to +7 mV. 2's complement</td><td>7 = 7 mV      15 = -1 mV 
6 = 6 mV      14 = -2 mV 
... 
1 = 1 mV     9 = -7 mV 
0 = 0 mV     8 = -8 mV</td></tr><tr><td>TW2</td><td>Timer to charge up the capacitor of the recommend RC network when the internal analog part is used.</td><td>Charge time: 
0 = 90 μs 
1 = 120 μs 
2 = 150 μs 
3 = 300 μs, recommended setting</td></tr><tr><td>EN_INT[3]</td><td>Additional interrupt source. See also register 2 for the lower 3 bits of EN_INT. The various sources are wired by an OR. An EEPROM action, e.g. EEPROMCOMPARE, is managed by the TDC-GP21 and especially the EEPROM write may last up to 130ms. Indicating the end will be helpful.</td><td>1 = end of EEPROM action</td></tr><tr><td>START_CLKHS[2]</td><td>Highest bit to set the settling time for the high speed oscillator. The lower bits are set in register 0, bit 18 and 19.</td><td>0 = off 
1 = continuously on 
2 = 480 μs delay 
3 = 1.46 ms 
4 = 2.44 ms 
5 to 7 = 5.14 ms</td></tr><tr><td>CYCLE_TEMP</td><td>Selects timer for triggering the second temperature measurement in multiples of 50/60Hz</td><td>0 = 1
1 = 1.5
2 = 2
3 = 2.5</td></tr><tr><td>CYCLE_TOF</td><td>Selects timer for triggering the second ToF measurement in multiples of 50/60Hz</td><td>0 = 1
1 = 1.5
2 = 2
3 = 2.5</td></tr><tr><td>HZ60</td><td>TDC-GP21 can make complete up and down flow measurement and also two temperature measurements in series. The time interval between 2 measurements is based on 50 or 60 Hz.</td><td>0 = 50 Hz base, 20 ms
1 = 60 Hz base, 16.67ms</td></tr><tr><td>FIREODEF</td><td>Specifies the default level of the inactive fire buffer. Example: if FIRE_UP is active then the FIRE_DOWN buffer is connected to the default level. Setting 1 is mandatory when using the integrated analog section.</td><td>0 = High-Z (as in GP2)
1 = LOW</td></tr><tr><td>QUAD_RES</td><td>Option to improve the resolution by factor 4 from 90 ps to 22 ps. Can be used only in measurement mode 2.</td><td>0 = off (TDC-GP2 mode)
1 = on</td></tr><tr><td>DOUBLE_RES</td><td>Doubles the resolution from 90 ps to 45 ps. In measurement mode 1 this option limits the number of stop inputs to one (Stop1)</td><td>0 = off (TDC-GP2 mode)
1 = on</td></tr><tr><td>TEMP_PORTDIR</td><td>Ports for temperature measurement are measured in the opposite order.</td><td>0 = PT1 &gt; PT2 &gt; PT3 &gt; PT4
1 = PT4 &gt; PT3 &gt; PT2 &gt; PT1</td></tr><tr><td>ANZ_FIRE[6:4]</td><td>Highest 3 bits of the number of fire pulses. See also register 0. If ANZ_FIRE &gt; 15 then PHFIRE is no longer active.</td><td>0 = off
1 = 1 pulse
2 = 2 pulses
... 
127 = 127 pulses</td></tr><tr><td>ID6</td><td>Free bits, e.g. to be used as identification or version number</td><td></td></tr></table>

# 3.2 Read registers

The result and status registers can be read by means of opcode ’hBx. The opcode isfollowed by 4, 2 or 1 bytes, depending on the address.

The ID register bits in the configuration registers can be read back by means of opcode’hB7. This opcode is followed by 7 bytes in the order ID0, ID1 ... ID6, each byte with theMSB first.


Table 3-2: Read Registers


<table><tr><td>ADR</td><td>Symbol</td><td>Bits</td><td colspan="9">Description</td><td></td></tr><tr><td>0</td><td>RES_0</td><td>32</td><td colspan="9">Measurement result 1, fixed-point number with 16 integer and 16 fractional digits\(2^{15}\)20, 2-120-16</td><td></td></tr><tr><td>1</td><td>RES_1</td><td>32</td><td colspan="9">Measurement result 2, fixed-point number with 16 integer and 16 fractional digits</td><td></td></tr><tr><td>2</td><td>RES_2</td><td>32</td><td colspan="9">Measurement result 3, fixed-point number with 16 integer and 16 fractional digits</td><td></td></tr><tr><td>3</td><td>RES_3</td><td>32</td><td colspan="9">Measurement result 4, fixed-point number with 16 integer and 16 fractional digits</td><td></td></tr><tr><td rowspan="2">4</td><td rowspan="2">STAT</td><td rowspan="2">16</td><td>15</td><td>14</td><td>13</td><td>12</td><td>11</td><td>10</td><td>9</td><td>8 - 6</td><td>5 - 3</td><td>2 - 0</td></tr><tr><td>EEPROM_eq_CREG</td><td>EEPROM_DED</td><td>EEPROM_Error</td><td>Error short</td><td>Error open</td><td>Timeout Precounter</td><td>Timeout TDC</td><td># of hits Ch 2</td><td># of hits Ch 1</td><td>ALU_OP_PTR</td></tr><tr><td>5</td><td>REG_1</td><td>8</td><td colspan="10">Content of highest 8 bits of write register 1, to be used for testing the communication</td></tr><tr><td>8</td><td>PW1ST</td><td>8</td><td colspan="10">Pulse width 1st wave compared to measured hits, fixed point with 1 bit integer</td></tr></table>

# 3.2.1 Result Registers

The data structure and the occupancy of the result registers depend on the operationmode and whether calibrated or non-calibrated data are stored. Several cases must bedistinguished:

Only in measurement mode 1 negative results are possible.

In measurement mode 2 only positive results are possible, given as unsigned numbers.

A non-calibrated measure is possible only in measurement mode 1.

In measurement mode 1 with calibrated data (ALU) the time intervals that have to bemeasured can not exceed twice the period of the calibration clock. When measuringbigger time intervals an ALU - overflow will occur and ’hFFFFFFFF is written in theappropriate result register.

# a. Measurement mode 1 with calibrated data (CALIBRATE = 1)

The results are given in multiples of the internal reference clock $[ =$ external referenceclock divided by 1, 2 or 4 (DIV_CLKHS)). Calibrated data are 32 bit fixed point numberswith 16 integer bits and 16 fractional bits. Any calibrated result covers therefore 1 resultregister. The serial output begins with the highest bit $[ 2 ^ { 1 5 } ]$ and ends with the lowest one$[ 2 ^ { - 1 6 } ]$ . The numbers are available in complements of 2.

Time $=$ RES_X * Tref * 2 DIV_CLKHS = RES_X * Tref * N , with $\ N = \ 1$ , 2 or 4

Time < 2 * Tref * 2 DIV_CLKHS

# b. Measurement mode 1 without calibration (CALIBRATE = 0)

Non-calibrated data are of the type ‘Signed Integer’ and are stored as a 16 bit value in thehigh word of the result registers. The bits of the low word are set to zero. The result isrepresented as number of LSB and is available in complements of 2.

Time $=$ RES_X * LSB ~ RES_X * 90 ps

# c. Measurement mode 2

In measurement mode 2 the TDC-GP22 only supports calibrated measurement. Theresults are given in multiples of the internal reference clock $[ =$ external reference clockdivided by 1, 2 or 4 (DIV_CLKHS)). Calibrated data are 32 bit fixed point numbers with 16integer bits and 16 fractional bits. Any calibrated result covers therefore 1 result register.The serial output begins with the highest bit $[ 2 ^ { 1 5 } ]$ and ends with the lowest one $[ 2 ^ { - 1 6 } ]$ . Thenumbers are available in complements of 2.

Time $=$ RES_X * Tref * 2 DIV_CLKHS = RES_X * Tref * N , with $\ N = \ 1$ , 2 or 4

# d. Temperature measurement

Discharge time in the same format as in c., measurement mode 2.

The ratio of the discharge times equal the ratio of resistance:

$$
R _ {T} = R _ {\text {r e f}} ^ {*} \tau_ {T} / \tau_ {\text {r e f}}
$$

# 3.2.2 Status Register


Table 3-3: Status registers


<table><tr><td>Bits</td><td>Name</td><td>Description</td><td>Values</td></tr><tr><td>2 - 0</td><td>ALU_OP_PTR</td><td>ALU operation pointer. Pointer to the result register. See description below</td><td></td></tr><tr><td>5 - 3</td><td># of hits Ch 1</td><td>Number of hits registered on channel 1</td><td></td></tr><tr><td>8 - 6</td><td># of hits Ch 2</td><td>Number of hits registered on channel 2</td><td></td></tr><tr><td>9</td><td>Timeout TDC</td><td>Indicates an overflow of the TDC unit</td><td>1 = overflow</td></tr><tr><td>10</td><td>Timeout Precounter</td><td>Indicates an overflow of the 14 bit precounter in MR 2</td><td>1 = overflow</td></tr><tr><td>11</td><td>Error open</td><td>Indicates an open sensor at temperature measurement</td><td>1 = open</td></tr><tr><td>12</td><td>Error short</td><td>Indicates a shorted sensor at temperature measurement</td><td>1 = short</td></tr><tr><td>13</td><td>EEPROM_Error</td><td>Single error in EEPROM which has been corrected</td><td>1 = error</td></tr><tr><td>14</td><td>EEPROM_DED</td><td>Double error detection. A multiple error has been detected which can not be corrected.</td><td>1 = multiple error</td></tr><tr><td>15</td><td>EEPROM_eq_CREG</td><td>Indicates whether the content of the configuration registers equals the EEPROM</td><td>1 = equal</td></tr></table>

# ALU Operation Pointer

Description: The ALU operation pointer is stored in bits 0-2 of the status register (rangeof 0x00 to 0x03) and provides an index to one of the 4 results registers (RES_0 to RES_3)as follows:

When the EN_AUTOCALC_MB2 parameter is set to 0, and thereforeautocalculation is OFF, the ALU operation pointer is set to the next free resultregister that will be used by the ALU for its next TDC cycle. This occurs once a TDCmeasurement is performed. Therefore after a TDC measurement ALU_OP_PTRminus 1 will point to the ALU result.

 When EN_AUTOCALC_MB2 is 1 (autocalculation ON) and once a TDC measurementis performed the ALU operation pointer is set to the result register that containsthe sum of the hit calculations stored in RES_0 to RES_2. This calculation does not

increase the ALU operation pointer. Of course, if the number of hits you expect isless than 4 (3 results + 1 start), then not all of the registers from R ES_0 to RES_2will be used in the sum.


Example 1: EN_AUTOCALC_MB2 $=$ 0FF


After sending an INIT opcode:  
ALU_OP_PTR  $= =$  0x00  
TDC Measurement Performed, ALU performs one calculation.  
ALU_OP_PTR  $= =$  0x01  
Calculation result is in register O (ALU_OP_PTR -1)  
By writing to configuration register 1 the ALU performs a second calculation  
ALU_OP_PTR  $= =$  0x02  
Calculation result is in register 1 (ALU_OP_PTR -1)  
By writing to configuration register 1 the ALU performs a third calculation  
ALU_OP_PTR  $= =$  0x03  
Calculation result is in register 2 (ALU_OP_PTR -1)


Example 2: EN_AUTOCALC_MB2 = ON


Three hits are configured by the user   
TDC measurement performed   
ALU_OP_PTR  $= = 0x03$    
Automatic calculation of the sum of RES_0 + RES_1 + RES_2 Calculation result is in register 3 (ALU_OP_PTR)

# 3.2.3 PW1ST Register

This register holds a 8-bit fixed point number with 1 integer and 7 fractional digits.

PW1ST gives the ratio of the width of the first half wave (at a given offset) compared tothe half period of the received signal. See section 4.4 for further details.

```txt
Data range: 0 to 1.99219  
(with EDGE_FW = rising edge and negative offset the ratio is > 1).
```

# 3.3 EEPROM

The TDC-GP22 has a $7 { \times } 3 2$ bit EEPROM. This EEPROM can be used to store theconfiguration data together with the ID or version number. Only the following three actionsare possible:

 Write configuration register content into the EEPROM

 Transfer the EEPROM content into the configuration registers

 Compare the configuration registers‘ content with the EEPROM content

# Important Note:

If values are to be stored in the EEPROM it is mandatory to ensure that NO measurement isrunning (neither ToF nor temperature nor calibration measurements). During measurement awrite access to the EEPROM is not permitted. The write access to the EEPROM takes about300 ms. With no consideration, the EEPROM may be written with incorrect values. It may evenhappen that adjustment values are overwritten which prevents proper operation of the TDC.

Besides the ID it is not possible to read back the EEPROM. This gives customers thepossibility to program the chips by themselves and prohibit other to read back theconfiguration.

For verification it is possible to compare the configuration register may be compare withthe EEPROM. Bit EEPROM_eq_CREG in the status register indicates whether the content isequal or not.

The EEPROM has an internal error correction (Hamming code). It is possible

 to detect and correct single bit errors,

 to detect multi-bit errors without correction

Errors are indicated in the status register, bits EEPROM_Error (single bit) andEEPROM_DED (double error detection).

*****With each read access/compare to the EEPROM the error bit is checked. In casea single bit error is detected a refresh cycle is started automatically and the data isrestored.

The data retention of the EEPROM is > 10 years $@$ $8 5 ~ ^ { \circ } \complement$ without single or multipleerrors. With regular Compare_EEPROM commands (e.g. once per month) the dataretention can be extended unlimited.

# 3.4 SPI-interface

The serial interface is compatible with the 4-wire SPI standard. It needs theSerialSelectNot (SSN) and can not operated as 3-wire interface.

SSN - Slave Select

SCK - SPI Clock

SI - SPI Data In

SO - SPI Data Out

The TDC-GP22 does only support the following SPI mode (Motorola specification) *:

Clock Phase Bit = 1

Clock Polarity Bit = 0

SCK starts with LOW, data take over is with the falling edge of SCK. The timings areshown in section 2.3. The interrupt pin is set back to INTN = 1 if:

SSN goes LOW

 or, in case SSN is already LOW, with the first rising edge of SCK.

# SSN as Reset

The SerialSelectNot (SSN) line is the HIGH-active reset for the serial interface. After SSNis set to LOW different operations can be addressed, not depending on the status of theinterface before the reset.

# Note:

It is mandatory to set the SSN – line to High-state for at least 50 ns between eachRead-/Write sequence.

* There is no common SPI specification, especially for phase $\&$ polarity. Some microcontroller mayneed a different setting, e.g. MSP430 run with Clock Phase $=$ Clock Polarity = 0

# Opcodes


Table 3-4: Opcodes


<table><tr><td>Hex</td><td colspan="4">MSB</td><td colspan="4">LSB</td><td>Description</td><td>Followed by</td></tr><tr><td>'h8x</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>A2</td><td>A1</td><td>A0</td><td>Write into address A</td><td>24 bit or 32 bit data</td></tr><tr><td>'hBx</td><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td><td>A2</td><td>A1</td><td>A0</td><td>Read from address A</td><td>8, 16 or 32 bit data</td></tr><tr><td>'hB7</td><td>1</td><td>0</td><td>1</td><td>1</td><td>0</td><td>1</td><td>1</td><td>1</td><td>Read ID bit</td><td>56 bit ID'S</td></tr><tr><td>Hex</td><td colspan="8">MSBLSB</td><td>Description</td><td>Followed by</td></tr><tr><td>'hB8</td><td>1</td><td>0</td><td>1</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>Read PW1ST</td><td>8bit</td></tr><tr><td>'hCO</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>Write configuration registers into EEPROM</td><td></td></tr><tr><td>'hFO</td><td>1</td><td>1</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>Transfer EEPROM content into configuration registers</td><td></td></tr><tr><td>'hC6</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td><td>0</td><td>Compare configuration registers with EEPROM</td><td></td></tr><tr><td colspan="11"></td></tr><tr><td>'h70</td><td>0</td><td>1</td><td>1</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>Init</td><td></td></tr><tr><td>'h50</td><td>0</td><td>1</td><td>0</td><td>1</td><td>0</td><td>0</td><td>0</td><td>0</td><td>Power On Reset</td><td></td></tr><tr><td colspan="11"></td></tr><tr><td>'h01</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>Start_TOF</td><td></td></tr><tr><td>'h02</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>Start_Temp</td><td></td></tr><tr><td>'h03</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td><td>Start_Cal_Resonator</td><td></td></tr><tr><td>'h04</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td><td>Start_Cal_TDC</td><td></td></tr><tr><td>'h05</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>0</td><td>1</td><td>Start_TOF_Restart</td><td></td></tr><tr><td>'h06</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td><td>0</td><td>Start_Temp_Restart</td><td></td></tr></table>

The transfer starts with the MSB and is finished sending the LSB. The transfer is donebytewise. Data transfer can be stopped after each byte, sending a LOW-HIGH-LOW on theSSN line.

# Example:

$\mathsf { \Omega } _ { \mathsf { h } \mathsf { B } \mathsf { O } } + 3$ bytes will write configuration register 0 in the TDC-GP2 compatible mode.

$\cdot _ { \mathrm { h 8 0 } \textrm { + } 4 }$ bytes will write configuration register 0 including IDO (TDC -GP22 only).

It is not possible to do incremental writing. Each register must be addressed separately.

# 3.4.1 Opcode Explanations

1. ’hC0, ’hF0, ’hC6 all refer to EEPROM operations. Those may last up 130 ms, especiallythe EEPROM write. Therefore, the EN_INT bit 3 in register 6 indicates the end of theEEPROM operation. This can be used to adjust microprocessor actions .

2. ’h01, Start_TOF: triggers a sequence for a single time-of-flight measurement. First, the4 MHz oscillator is switched on. After the delay set to settle the oscillator(START_CLKHS), the comparator and the reference voltage are switched on. Thereceiver capacitor is charged up th Vref while inactive fire buffer is pulled down toGND. After the delay set to charge up the capacitor (TW2), the fire buffer sends thefire pulses. After the delay set in DELVAL the TDC stop channel is open. At the end ofthe measurement the analog section and the 4 MHz are switched off and the currentconsumption drops down to near zero. The interrupt is set, pin ${ | \mathsf { N T N } = \mathsf { L O W } }$ .

3. ’h05, Start_TOF_Restart: This opcode runs the Start_TOF sequence twice, in up anddown direction as it is typical in ultrasonic flow meters. The interrupt is set, pin INTN $=$LOW, when the time measurement for each direction is finished. So, for oneStart_TOF_Restart command the microprocessor sees two interrupts and has to readtwice. The time interval between the up and down measurement is set by configurationparameter CYCLE_TOF in multiples of 50 Hz or 60 Hz. The right selection of the delaybetween the two measurements suppresses 50/60 Hz noise.

<table><tr><td>CYCLE_TOF</td><td>factor</td><td>HZ60 = 0(50Hz)</td><td>HZ60 = 1(60Hz)</td></tr><tr><td>0</td><td>1</td><td>20 ms</td><td>16.67 ms</td></tr><tr><td>1</td><td>1.5</td><td>30 ms</td><td>25.00 ms</td></tr><tr><td>2</td><td>2</td><td>40 ms</td><td>33.33 ms</td></tr><tr><td>3</td><td>2.5</td><td>50 ms</td><td>41.67 ms</td></tr></table>

’h02, Start_Temp: triggers a single temperature measurement sequence. It beginswith the fake measurements (ANZ_FAKE) on port PT0. Then it measures ports PT0$> \mathsf { P T } 1 > \mathsf { P T } 2 > \mathsf { P T } 4$ . If TEMP_PORTDIR is set one then the sequence of ports isinverted, starting with the fake measurements at port PT4.

’h06, Start_Temp_Restart: This opcode runs the Start_Temp sequence twice. Thetime interval between the up and down measurement is set by configurationparameter CYCLE_TEMP in multiples of 50 Hz or 60 Hz. The right selection of thedelay between the two measurements suppresses 50/60 Hz noise.

<table><tr><td>CYCLE_TEMP</td><td>factor</td><td>HZ60 = 0 (50Hz)</td><td>HZ60 = 1 (60Hz)</td></tr><tr><td>0</td><td>1</td><td>20 ms</td><td>16.67 ms</td></tr><tr><td>1</td><td>1.5</td><td>30 ms</td><td>25.00 ms</td></tr><tr><td>2</td><td>2</td><td>40 ms</td><td>33.33 ms</td></tr><tr><td>3</td><td>2.5</td><td>50 ms</td><td>41.67 ms</td></tr></table>

’h03, Start_Cal_Resonator: Triggers a calibration measurement of the high speedoscilator. The TDC measures a time interval between 61 µs and 488 µs, specifiedin ANZ_PER_CALRES. The end of the measurement is indicated by the interrupt.The result, in multiples or the high speed clock period, is stored in result register0. Dividing this by the theoretical value gives the correction factor.

 ’h04, Start_Cal_TDC: This command starts a measurement of 2 periods of thereference clock. It is used to update the calibration raw data. Typically, the chip isconfigured for auto-calibration and this command is not necessary.

# 3.4.2 SPI Sample

![](images/0e80fab52dd5186569805caebc3fe859c44fd916eaaf099a5237999d118f1032.jpg)



Figure 3-1: Sample scope picture for sequence INIT ’h70 and Start_Cal_TDC $=$ ’h04


# 4 Converter Frontend

# 4.1 TDC - Measurement mode 1

# 4.1.1 General Description

 Measurement range from 3.5 ns to 2.4 µs (0 to 2.4 µs between stop channels)

 2 stop channels referring to one start channel each of typ. 90 ps resolution

 1 stop channel referring to one start channel with typ. 45 ps resolution

20 ns pulse pair resolution

 4-fold multihit capability for each stop channel

 Selectable rising/falling edge sensitivity for each channel

 Enable pins for windowing functionality

 The possibility to arbitrarily measure all events against each other

 Typical application: Laser ToF, RF ToF, ATE

Digital TDCs use internal propagation delays of signals through gates to measure timeintervals with very high precision. Figure 5 clarifies the principal structure of such anabsolute-time TDC. Intelligent circuit structures, redundant circuitry and special methodsof layout on the chip make it possible to reconstruct the exact number of gates passed bythe signal. The maximum possible resolution strongly depends on the maximum possiblegate propagation delay on the chip.

![](images/72b8396976be99868fb95048d6b8da9dba04c1af5e4107e1a34b2a0db49f306f.jpg)



Figure 4.1


The measuring unit is triggered by a START signal and stopped by a STOP signal. Based onthe position of the ring oscillator and the coarse counter the time interval between STARTand STOP is calculated with a 20 bit measurement range.

The BIN size (LSB) is typically 90 ps at 3.3 V and ${ } ^ { 2 5 } \ ^ { \circ } \mathsf { C }$ ambient temperature. The RMSnoise is about 60 ps (0.7 LSB). The gate propagation delay times strongly depend on

temperature and voltage. Usually this is solved doing a calibration. During such acalibration the TDC measures 1 and 2 periods of the reference clock.

The measurement range is limited by size of the counter:

$$
\mathrm {t _ {y y} = B I N \times 2 6 2 2 4 \sim 9 0 p s \times 2 6 2 2 4 = 2 . 4 \mu s}
$$

<table><tr><td></td><td>Time (Condition)</td><td>Description</td></tr><tr><td>tph</td><td>2,5 ns [min.]</td><td>Minimum pulse width</td></tr><tr><td>tpl</td><td>2,5 ns [min.]</td><td>Minimum pulse width</td></tr><tr><td>tss</td><td>3.5 ns ns [min]
2.4 μs [max.]</td><td>Start to Stop</td></tr><tr><td>trr</td><td>20 ns (typ.)</td><td>Rising edge to rising edge</td></tr><tr><td>tff</td><td>20 ns (typ.)</td><td></td></tr><tr><td>tva</td><td>1.24μs uncalibrated
4.25μs calibrated</td><td>Last hit to data valid</td></tr><tr><td>txx</td><td>No timing limits</td><td></td></tr><tr><td>tyy</td><td>2.4 μs (max)</td><td>Max. measurement range
= 26224 * LSB</td></tr></table>

![](images/7fa10c48f96ec0f4bf474d6badc35599d37c238956185c6759ced9e9874c2728.jpg)



Figure 4.2


# Input circuitry

Each input separately can be set to be sensitive to rising or falling edge or both edges.This is done in register 0, bits 8 to 10. (NEG_START, NEG_STOP1, NEG_STOP2) andregister 2, bit 27 & 28, RFEDGEx.

Furthermore all Start/Stop-inputs support a high active enable pin.

# 4.1.2 Measurement Flow

# Configuration

At the beginning the TDC-GP22 has to be configured. The main settings for measurementmode 1 are:

# a. Select measurement mode 1

Set register 0, bit 11, MESSB2 $= 0$ .

Register 6, bit 12, DOUBLE_RES = 1 selects double resolution. With this bit set theresolution is typ. 45 ps instead of 90 ps, but only one STOP channel is available.

# b. Select the reference clock (see also section 5.1)

Register 0, bits 18 & 19 and register 6, bit 20, START_CLKHS defines the switch-onbehavior of the high-speed clock. If only the 32 kHz is used it should be “0“. If only thehigh-speed clock is used it should be “1“ (continuously on).

Register 0, bits 20 & 21, DIV_CLKHSsets an additional internal divider forthe reference clock (1, 2 or 4). This isimportant for calibratedmeasurements in measurement mode1 because the ALU works correctlyonly if 2*Tref(intern) is bigger than themaximum time interval to bemeasured. Otherwise the ALU outputis ’hFFFFFFFF.

Make also sure that 2*Tref(intern) <2.4 µs to avoid a timeout duringcalibration.

![](images/f79b664bb141e49f278791afbaf0a7a76c9ea06a8d0b1c925e93808f9a20922f.jpg)



Figure 4.3


# c. Set the number of expected hits

In register 1, bits 16 to 18 and 19 to 21, HITIN1 and HITIN2 the user has to define thenumber of hits the TDC-GP22 has to wait for. A maximum of 4 on each channel ispossible. The TDC-GP22 measures until the set number of hits is registered or a timeoutoccurs.

# d. Select calibration

As the BIN size varies with temperature and voltage the TDC-GP22 ALU can internallycalibrate the results. This option is switched on by setting register 0, bit13, CALIBRATE $=$“1“. It is recommended to do this.

For the calibration the TDC measures 1 and 2 cycles of the reference clock. The two dataare stored as Cal1 and Cal2.

There are two ways to update the calibration data Cal1 and Cal2:

- Separate calibration by sending opcode Start_Cal_TDC via the SPI interface

- Automatic update by setting register 0, bit 12, NO_CAL_AUTO = “0“. In most applicationsthis will be the preferred setting.

# e. Define ALU data processing

While the TDC unit can measure up to 4 hits on each channel the user is free in hisdefinition what the ALU shall calculate. The settings are done in register 1, bits 16 to 19and 20 to 23, HIT1 and HIT2. Both parameters can be set to:

0 = Start

$\uparrow = \uparrow$ . Stop Ch1 $9 = 1$ . Stop Ch2

$\mathbf { \Phi } ^ { 2 } = \mathbf { \Phi } ^ { 2 }$ . Stop Ch1 $\mathsf { A } = \mathsf { c }$ . Stop Ch2

$^ { 3 } = 3$ . Stop Ch1 $\mathsf { B } = \mathsf { 3 }$ . Stop Ch2

$4 = 4$ . Stop Ch1 $\complement = 4$ . Stop Ch2

6 = Cal1 Ch1

7 = Cal2 Ch1

# Examples:

Reg1 = ‘h01xxxx - 1st Stop Ch1-Start

Reg1 = ‘h2Bxxxx - 3rd Stop Ch2-2nd Stop Ch1

Reg1 = ‘h06xxxx - Cal1

The ALU calculates HIT1 - HIT2.

In case calibration is active the ALU does the full calibration calculation (except whenreading the calibration values. In this case the ALU writes the Cal1/Cal2 raw data to theoutput register).

$$
\begin{array}{l} R E S \_ X = \frac {(H I T 1 - H I T 2)}{C a l 2 - C a l 1} \\ C a l 2 - C a l 1 = g r a d i e n t \\ T i m e = R E S \_ X * T _ {r e f} * 2 ^ {C l k H S D i v} = R E S \_ X * T _ {r e f} * N, \qquad w i t h N = 1, 2 o r 4 \\ \end{array}
$$

![](images/f4a3a6df3e2d2deaa9192d615c2dbd1115faa72d11511b764011303b480c39a2.jpg)



Figure 4.4


# f. Select input sensitivity

In register 2, bits 27 & 28, RFEDGE1 and RFEDGE2, the user can select whether the stopinputs are sensitive to either rising or falling edges (RFEDGE $=$ “0“) or to both rising andfalling edges (RFEDGE = “1“).

In register 0, bits 8 to 10 the user can add an internal inverter to ea ch input, Start,Stop1 and Stop2. With RFEDGE $=$ “0“ this is the same as rising edge $\lbrack { \mathsf { N E G } } _ { - } { \mathsf { X } } = { \mathsf { \Omega } } ^ { \ast } ,$ ) orfalling edge $( N E G \_ X = " 1 " ]$ .

# g. Interrupt behavior

The interrupt pin 8, INT can have different sources. They are selected in register 2, bits29 to 31, EN_INT and register 6, bit 21.

Reg. 2 bit ${ 2 9 = " 1 " }$ ALU ready

Reg. 2 bit $3 0 = " 1 "$ The set number of hits is there

Reg. 2 bit $3 1 \ : = \ : " \ : 1 \ : "$ Timeout of the TDC unit

Reg. 6 bit $2 1 = " 1 "$ End of EEPROM action

The different options are wired by OR to enable more than one source. The first risingedge of SCK resets the INTN pin (interrupt).

After the configuration the user has to initialize the TDC-GP22 by sending opcode “Init” sothat the TDC accepts Start and Stop hits.

# Measurement

After an initialization the TDC unit will start with the first pulse on the Start input. It willrun until:

 the set number of hits has been seen (maximum 4 on both stop channels in mode1)

 or until a timeout occurs at the end of the measurement range (at about 2.4 µs inmode 1).

The time measurement raw data are internally stored. The number of hits can be seenfrom the status register, bits 3 to 8. In case calibration is active the TDC now m easuresone and two periods of the internal reference clock (Tref * 1, 2 or 4). The calibration rawdata Cal1 and Cal2 are also internally stored.

![](images/e44cd962a4e5a32a4b9c0b81d0d3d2164b3a10c3ff6690f86ac10bbad70b0f73.jpg)



Figure 4.5


# Data Processing

At the end of the measurement the ALU starts to process the data according to the HIT1,HIT2 settings and transfers the result to the output register. In case calibration is off theALU transfers the 16 bit raw data to the output register. With calibration the ALUcalculates according to 3.1.1.d and transfers the 32 bit fixed point number to the outputregister.

The ALU can be switched off configuring HIT1 = HIT2 = 5.

The time it takes the ALU depends on whether calibration is on or not and the supplyvoltage.


Table 4.1: ALU timings


<table><tr><td></td><td>un-calibrated (disable Auto-Cal.)</td><td>calibrated</td><td>Predivider</td></tr><tr><td rowspan="3">2.5 V</td><td rowspan="3">1.56 μs</td><td>3.0 μs</td><td>0</td></tr><tr><td>4.58 μs</td><td>1</td></tr><tr><td>7.58 μs</td><td>2</td></tr><tr><td rowspan="3">3.0 V</td><td rowspan="3">1.24 μs</td><td>2.75 μs</td><td>0</td></tr><tr><td>4.25 μs</td><td>1</td></tr><tr><td>7.26 μs</td><td>2</td></tr><tr><td rowspan="3">3.6 V</td><td rowspan="3">1.0 μs</td><td>2.54 μs</td><td>0</td></tr><tr><td>4.0 μs</td><td>1</td></tr><tr><td>7.0 μs</td><td>2</td></tr></table>

As soon as the data is availablefrom the output register theinterrupt flag is set (assumed thatthe ALU interrupt is enabled, seereg. 2, EN_INT). Further the loadpointer of the output register isincreased by 1 and points to thenext free memory. The actualposition of the load pointer can beseen in the status register, bits 0to 2.

# Reading Data

Now the user can read the data sending theopcode 10110ADR. With the next 16 clockcycles (un-calibrated data) or 32 clock cycles(calibrated data) the TDC-GP22 will send theresult, beginning with the most significant bit(MSB). The first rising edge of SCK resets theINTN pin (interrupt).

# a. Un-calibrated data format:

16 bit Signed integer in complements of 2.1BIN $=$ uncalibrated gate delay is about 90 psat 3.3 V and ${ } ^ { 2 5 } \ ^ { \circ } \mathsf { C }$ .

Time $=$ RES_X x 90 ps

# b. Calibrated data format:

32 bit fixed-point number in complements of 2.Given in multiples of the reference clock.

Time $= \mathsf { R E S \_ X } \star \mathsf { T } _ { \mathsf { r e f } } \star \mathsf { N }$ $=$ , with $\ N = \ 1$ , 2 or 4

# Example:

configuration

write reg1=’h014400 4 hits on channel 1,calculate 1st Stop -Start

Initialize

while(Check interrupt flag)

write reg1 $=$ ’h024400 calculate 2nd -Start

wait(4.6 µs)

write reg1 $=$ ’h034400 calculate 3rd-Start

wait(4.6 µs)

write reg1 $=$ ’h044400 calculate 4th-Start

wait(4.6 µs)

Now all Hit data are available from registers 0 to 3.The load pointer value is 4.

The measured time interval may not exceed otherwise the ALU will go into overflow and willwrite the data ’hFFFFFFFF to the output register.

The configuration of the ALU allows only one hit calculation at the time. In case more thanone hit has been measured it is necessary to write new commands to HIT1/HIT2 toinstruct the ALU for calculating the other hits. After writing to HIT1/HIT2 it is ne cessaryto wait for minimum t.b.d. µs (calibrated data) or t.b.d. ns (un -calibrated data) beforereading or writing again to HIT1/HIT2.

# Reading Calibration Raw Data

The calibration data are not addressed directly after the calibration measurement butafter the next regular measurement, before the next INIT.

# Source Code Example:

```c
// 1st Measurement plus calibration data readout  
gp22_send_1byte(Bus_Type, Init);  
// Wait for INT Slot_x  
Wait_For_Interrupt(Bus_Type);  
// First regular measurement (to readout calibration raw data)  
Result = gp22_read_n_bytes(Bus_Type, 4,0xB0,0x00,16);  
// readout the new calibration data from result register adr 0x01  
gp22_WR_config_reg(Bus_Type, 0x81,0x67490000);  
Diff_Cal2_Cal1 = gp22_read_n_bytes(Bus_Type, 4,0xB0,0x01,16);
```

At the end the TDC-GP22 has to be initialized again to be ready for the next measurement.This is done by sending the opcode “Init“ so that the TDC accepts new Start and Stop hits.

# 4.2 TDC - Measurement mode 2

# 4.2.1 General Description

 1 stop channels referring to one start channel

 Typical 22 ps / 45 ps / 90 ps resolution

 Measurement range from 700 ns to 4 ms $@$ 4 MHz

 2 x Tref pulse pair resolution

 3-fold multihit capability, full-automated calculation

Selectable rising/falling edge sensitivity

 Integrated programmable windowing for each single stop with 10 ns precision

 Typical application: Ultrasonic flow & heat meter

Digital TDCs use internal propagation delays of signals through gates to measure timeintervals with very high precision (see also measurement mode 1, section 4). Inmeasurement mode 2 the maximum time interval is extended using a pre-divider. Theresolution in LSB remains unchanged by that. In this mode the high-speed unit of the TDCdoes not measure the whole time interval but only time intervals from START and STOP tothe next rising edge of the reference clock (fine-counts). In between the fine-counts theTDC counts the number of periods of the reference clock (coarse-count).

![](images/acea0bac53e13d5cd3e5282887a312239e4b559ae7723ff06dd2201a9d285a30.jpg)



Figure 4.6


The GP22 converter front end section achieves a quantization BIN of 90 ps (LSB) where$\mathsf { V c c } = 3 . 3 \mathrm { ~ V ~ }$ and the ambient temperature is at ${ } ^ { 2 5 } \ ^ { \circ } \mathsf { C }$ . RMS noise accounts for 60 ps (0.7LSB) of this same result. As gate propagation delay is used for precision intervalmeasurement it is important to consider that this delay time is directly affected by bothVcc and temperature. Therefore, using Measurement Mode 2, a calibration is requiredand is done automatically with the right configuration. During calibration the TDCmeasures one and two periods of the 4 MHz reference clock.

# The calibrated result does not depend on temperature or supply voltage.

The measurement range is limited by size of the coarse counter:

$$
t _ {y y} = T _ {\text {r e f}} \times 2 ^ {1 4} = 4. 1 \mathrm {m s} @ 4 \mathrm {M H z}
$$

The time interval between START and STOP is calculated with a 26 bit measurementrange.

<table><tr><td></td><td>Time (Condition)</td><td>Description</td></tr><tr><td>tph</td><td>2,5 ns (min.)</td><td>Minimum pulse width</td></tr><tr><td>tpl</td><td>2,5 ns (min.)</td><td>Minimum pulse width</td></tr><tr><td>tss</td><td>2*Tref</td><td>Start to Stop @ DIS_PHASESSHIFT = 1</td></tr><tr><td>trr</td><td>2*Tref</td><td>Rising edge to rising edge</td></tr><tr><td>tff</td><td>2*Tref</td><td>Falling edge to falling edge</td></tr><tr><td>tva</td><td>4.6 μs (max.)</td><td>ALU start to data valid</td></tr><tr><td>tyy</td><td>4 ms (max)</td><td>Max. measurement range</td></tr></table>

![](images/11bd93240192c1b8efdb74040a20e6b1502cdaf9e5adb92a0af250a19545eacd.jpg)



Figure 4.7


# Input circuitry

Each input separately can be set to be sensitive to rising or falling edg e. This is done inregister 0, bits 0 to 2. (NEG_START, NEG_STOP1).

Further all Start/Stop-inputs support a high active enable pin.

# Note:

In case the Start-Stop interval is less than the lower limit tzz the TDC will ignore more andmore events the smaller it is. In no case there will be wrong results.

# 4.2.2 Measurement Flow

![](images/ba7de96c564278d02fa86e5c5194ea3613acc22489963915242c2b18f576543e.jpg)



Figure 4.8


# Configuration

At the beginning the TDC-GP22 has tobe configured. The main settings formeasurement mode 2 are:

# a. Select measurement mode 2

setting register 0, bit 11, MESSB2 = 1

# b. Select the reference clock

(see also section 5.1)

In measurement mode 2 the TDC-GP22needs the high-speed clock for the timemeasurement. In case of low-powerapplications this clock can be switchedof in between measurements. The a32.768 kHz clock is necessary for thetiming control during the oscillatorpower-on.

Register 0, bits 18 & 19, START_CLKHS defines the switch-on behavior of the high-speedclock. If only the high-speed clock is used this is be set to “1“(continuously on). In caseboth oscillators are used for current saving reasons this should be set to “2“ for ceramicoscillators and to “3“ for quartz oscillators.

Register 0, bits 20 & 21, DIV_CLKHS sets an additional internal divider for the referenceclock (1, 2 or 4). The choice has an influence on the minimum time interval

$$
t _ {\min } = 2 * T _ {\text {r e f}} * 2 ^ {\text {D I V} \_ \text {C L K H S}}
$$

and the maximum time interval

$$
t _ {\max } = 2 ^ {1 4} * T _ {\text {r e f}} * 2 ^ {\text {D I V C L K H S}}
$$

Further, it is necessary that

$$
2 ^ {*} T _ {\text {r e f}} ^ {*} 2 ^ {\text {D I V C L K H S}} <   2. 4 \mu \mathrm {s}.
$$

Otherwise the ALU will go into an overflow during calibration and write ’hFFFFFFFF asoutput data.

# Please note:

The resulting clock after the predivider has to be in the allowed range of 2 MHz to 8 MHzin single and double resolution and from 2 MHz ... 6 MHz in quad resolution.

# c. Set the number of expected hits

In register 1, bits 16 to 18, HITIN1 the user has to define the number of hits the TDC-GP22 has to wait for. A maximum of 3 on channel 1 is possible. The number HITIN1always has to be higher by 1 than the number of expected hits. The reason is that theStart is also counted as a hit. The TDC-GP22 measures until the set number of hits isregistered or a timeout occurs. register 1, bits 19 to 21, HITIN2 have to be set to “0“.

# Example:

2 stop pulses are expected:HITIN1 = “3”, HITIN2 = “0”

# d. Select calibration

The calibration is switched on by setting register 0, bit13, CALIBRATE $=$ “1“. It ismandatory to do this.

For the calibration the TDC measures 1 and 2 cycles of the reference clock. The two dataare stored as Cal1 and Cal2.

There are two ways to update the calibration data Cal1 and Cal2:

 Separate calibration by sending opcode Start_Cal_TDC via the SPI interface

 Automatic update by setting register 0, bit 12, NO_AUTO_CAL = “0“. In mostapplications this will be the preferred setting.

# e. Define ALU data processing

With EN_AUTOCALC_MB2 = 1 the TDC-GP22 calculates all set hits automatically. Inaddition, the sum of the results is calculated, too, and written into read register RES_3.This simplifies the communication compared to TDC-GP21 as it is no longer necessary tore-write register 1.

With EN_AUTOCALC_MB2 disabled the ALU calculates only one hit at once. The settingsare done in register 1, bits 24 to 27 and 28 to 31, HIT1 and HIT2. The Start pulse isinternally handled like a Stop pulse because of the special measuring method inmeasurement mode 2.

Reg1 = ’h21xxxx $=$ Calculate 1st Stop Ch1-Start

Reg1 = ’h31xxxx $=$ Calculate 2nd Stop Ch1-Start

Reg1 = ’h41xxxx $=$ Calculate 3rd Stop Ch1-Start

The ALU calculates the time interval as:

$$
R E S \_ X = C o a r s e C o u n t + \frac {(H I T 1 - H I T 2)}{C a l 2 - C a l 1}
$$

$$
T i m e = R E S _ {X} * T r e f * 2 ^ {D I V _ {\text {C L K H S}}}
$$

# f. Select input sensitivity

In register 2, bits 27 & 28, RFEDGE1 and RFEDGE2, the user can select whether the stopinputs are sensitive to either rising or falling edges (RFEDGE $\textstyle { \mathrm { ~ \sum ~ } } ^ { \mathrm { ~ w ~ } } \bigcup ^ { \mathrm { ~ w ~ } }$ “) or to both rising andfalling edges (RFEDGE = “1“). In register 0, bits 8 to 10 the user can add an internalinverter to each input, Start, Stop1 and Stop2. With RFEDGE $=$ “0“ this is the same asrising edge $\begin{array} { r } { \mathopen { } \mathclose \bgroup \left( \mathsf { N E G } _ { - } \aftergroup \egroup \right) \times = \mathrm { ~ \ " { O } ~ } ^ { \cdots } . } \end{array}$ or falling edge $[ N E G \_ X = ^ { \cdots } 1 ^ { \cdots } ]$ .

# g. Interrupt behavior

The INT pin can have various sources, to be selected in regi ster 2, bits 21 to 23, EN_INT,and register 6 bit 21 EN_INT.

EN_INT $=$ no bits set no Interrupt source

reg2 bit 29 ALU ready

reg2 bit 30 The set number of hits is there

reg2 bit 31 Timeout of the TDC unit

reg6 bit 21 EEPROM action has finished

The different options are wired by OR. The first rising edge of SCK resets the INTN pin(interrupt).

After the configuration the user has to initialize the TDC-GP22 by sending opcode “Init“ sothat the TDC accepts Start and Stop hits.

# Measurement

After an initialization the TDC unit will start with the first pulse on the Start input. It willrun until:

the set number of hits has been seen (maximum 3 on channel 1 in measurementmode 2)

or until a timeout occurs. The timeout can be programmed in multiples of thereference clock setting reg. 3, bits 27 & 28, SEL_TIMO_MB2. At 4 MHz the valuesare:

SEL_TIMO_MB2 (@ 4 MHz, DIV_CLKHS = 0)

= 0 = 64 µs

= 1 = 256 µs

= 2 = 1024 µs

= 3 = 4096 µs recommended

At the end of the time measurement the TDC measures 2 periods of the reference clockfor calibration.

# Data processing

At the end of the measurement the ALU starts to process the data according to the HIT1,HIT2 settings and transfers the result to the output register. The ALU calculatesaccording to 4.2.2.e and transfers the 32 bit fixed point number to the output register.

The time it takes the ALU depends on the supply voltage to be calculated:


Table 4-2: ALU timings


<table><tr><td></td><td>2.5 V</td><td>3.0 V</td><td>3.6 V</td></tr><tr><td>First Event (1 Hit)</td><td>3.7 μs</td><td>3.3 μs</td><td>3.1 μs</td></tr></table>

As soon as the data is available from the output register the interrupt flag is set (assumedthat the ALU interrupt is enabled, see reg. 2, EN_INT). Further the load pointer of theoutput register is increased by 1 and points to the next free memory. The actual positionof the load pointer can be seen in the status register, bits 0 to 2.

# Reading Data

Now the user can read the data sending the opcode 10110ADR. With the next 32 cycles(calibrated data) the TDC-GP22 will send the result, beginning with the main significant bit(MSB).

The 32 bit fixed-point numbers in complements of 2 represent the time interval inmultiples of the reference clock.

$$
\text {T i m e} = \operatorname {R E S} _ {\mathrm {X}} * \operatorname {T} _ {\text {r e f}} * 2 ^ {\text {D I V} _ {\text {C L K H S}}}
$$

Now all hit data are available from registers 0 to 2. The load pointer value is 3.

At the end the TDC-GP22 has to be initialized again to be ready for the next measurement.

This is done by sending the opcode “Init“ so that the TDC accepts new Start and Stop hits.

The first rising edge of SCK resets the INTN pin (interrupt).

# 4.2.3 Stop Masking

The TDC-GP22 can set time-based masking windows for each of the 3 hits on Stop1 inputwhen no hits are accepted. The masking refers to the start event and has an accuracy ofless than 10 ns.

The internal enable unit is connected to the external enable pin by a logical AND. Theexternal enable pin must be set to “1” to use the internal masking unit. The configurationsettings are made in registers 2 to 4, DELVAL1, DELVAL2 and DELVAL3:

 DELVAL1 … DELVAL3 are fixed point numbers with 14 bit integer and 5 bitfractional digits, in multiples of the internal reference clock

$$
D e l a y _ {\min } = D E L V A L X / 2 ^ {5} * T _ {\text {r e f}} * 2 ^ {\text {D I V C L K H S}}
$$

 The minimum mask size is 3 clock cycles

 The mask values must have an ascending order. Each mask value must be 3 clockcycles bigger than the previous value

It is mandatory that if not all registers are used the mask values that are not required areset to $" 0 "$ . When all DELVAL registers are set to 0, the complete unit is disabled.

# Example:

4 MHz reference, DIV_CLKHS = 1

DELVAL1 $=$ ’h3200 1st Stop not accepted before 200 µs after Start

$$
(1 2 8 0 0 / 3 2 * 2 5 0 \mathrm {n s} ^ {*} 2 ^ {1} = 2 0 0 \mu \mathrm {s})
$$

DELVAL2 $=$ ’h3300 2nd Stop not accepted before 204 µs after Start

$$
(1 3 0 5 6 / 3 2 * 2 5 0 \mathrm {n s} * 2 ^ {1} = 2 0 4 \mu \mathrm {s})
$$

DELVAL3 $=$ ’h3400 3rd Stop not accepted before 208 µs after Start

$$
(1 3 3 1 2 / 3 2 * 2 5 0 \mathrm {n s} * 2 ^ {1} = 2 0 8 \mu \mathrm {s})
$$

# 4.3 Analog Input Section

TDC-GP22 has an additional analog input section which can be used alternatively to thepure digital inputs. Especially the design of ultrasonic flow and heat meters is greatlysimplified by this option. The external circuit of the ultrasonic part is reduced to just tworesistors and capacitors additional to the piezo transducers.

The ultrasonic signals will be packages of sinusoidal oscillations with several 100 mVamplitude. The signals are coupled to the inputs by means of a high pass filter as thecomparator can not handle GND as threshold. The threshold of the comparator is set to1/3 Vcc. An analog multiplexer selects the input according to the active measurementdirection. The comparator is chopper stabilized to guarantee a low offset voltage in therange of $< 2 ~ \mathsf { m V }$ . This is mandatory for a good measurement quality. The input offsetvoltage of the comparator is frequently corrected by an internal chopper circuit. Iftemperature or supply voltage changes over time, the offset voltage is automaticallyadapted and holds at $< 2 ~ \mathsf { m V }$ .

All elements are controlled by the TDC-GP22 control unit. They are powered only duringthe measurement to keep down the power consumption.

A measurement sequence, triggered by command Start_TOF_Restart looks like thefollowing procedure, starting with the up flow measurement:

 The 4 MHz oscillator is switched on. The chip waits for the programmed delay togive enough time for the oscillator to reach the full amplitude.

 The comparator, the reference voltage and the analog switches get powered.

 The capacitor of the transmitting path (STOP1) is connected to GND.

 The fire down buffer (FIRE_DOWN) is connected to GND.

 The capacitor of the receiving path (STOP2) is charged up to Vref. The TDC waitsthe delay set in TW2.

 The analog switch selects STOP2 input as input to the comparator.

 FIRE_UP is selected as TDC START signal.

 The set number of pulses is sent through the fire up buffer, pin FIRE_UP.

 The analog signal at STOP2 passes the comparator converted to a digital signalthat is connected to the STOP input of the TDC unit.

 When the delay of the stop masking unit (DELVAL) expired the TDC is ready tomeasure. It can measure up to 3 stops.

![](images/35c3a262872a58067c6bb0db2a9c427c038f4e4f7f018bdfae98b1381aa17d89.jpg)



Figure 4.9


 At the end of the measurement the control unit switches off the comparator, thereference the analog switches and the 4 MHz. The current is reduced to closezero. The interrupt flag is set.

 The control unit waits a period, given in multiples of 50Hz/60Hz. During this theprocessor has to read the results.

 After the delay the same procedure is started but in the opposite direction.

# 4.3.1 Offset Setting

The offset of the comparator can be set in steps of $\uparrow \ \mathsf { m V }$ from -8mV to $+ 7 ~ \mathsf { m V }$ by meansof parameter DA_KORR, bits 25 to 28 in register 6. DA_KORR is set as 2‘s complement.

Additionally, with First Wave Mode an additional offset of $\pm 3 5 { \mathrm { ~ m V } }$ can be set for the firstwave detection. See section 4.4 for details.

# 4.4 First Wave Mode

The major improvement of TDC-GP22 is the implementation of the First Wave Mode. It isbased on measurement mode 2 with the analog section being used. The offset is

controlled automatically to detect the first wave safely and to refer the final ToFmeasurement relative to the first wave. Additionally, the width of the first half wave iscompared to the half wave of the first ToF measurement. The ratio can be used asindicator for the signal strength. Thanks to the o ffset noise are suppressed and a time outindicates no water in the tube. The following list summarizes the options :

 Save first wave detection, allows high dynamic applications like water meters

 Higher dynamics allow use of 2 MHz or 4 MHz transducers

Upon the application of transducers with 2-4 MHz, it is necessary to choose alarger interval in the choice of the three waves (e.g. 4-6-8 or 4-7-10), to takeaccount of pulse pair resolution. $[ > 2 ^ { \star } \mathsf { T } _ { \mathsf { r e f } } + 2 0 \mathsf { O } \mathsf { n s }$ )

 Even reverse flow can be handled (very helpful e.g. with water meters)

 Pulse width measurement, allows to analyze the strength of the receive signal andto track the trigger level or to send an alarm.

 Offset for noise suppression, allows to indicate an empty tube.


Figure 4-10 illustrates the importanceof save first hit detection in flowmeters with high dynamic range likewater meters. With a fixed stopmasking (fixed DELVAL values) it is notpossible to recognize if the time-of-flight changes more than the period ofthe sound signal. There are severalreasons that the change in ToF ismore than a period. An important oneis the influence of temperature whichchanges the speed of ultrasound. Forslow systems like heat meters thismight be corrected by intelligentsoftware. But for high dynamicsystems like water meters with flowalso in the opposite direction thismethod will no longer be appropriate.


![](images/a827119a784652170b422ab9044940e533db2e99a33f192d565c56a9ba9850fe.jpg)



Figure 4-10: Typical error by high fluid dynamics


The trend towards higher transducer frequencies like 2 MHz and 4 MHz is another reasonfor having a system that can handle intrinsically changes bigger than a signal period.

There is still another source ofgetting wrong measurements.Dirt deposition on thetransducers, spool piece mirrorsand housing will lead to signaldamping e.g. from ±400 mV to <$\pm 8 0 ~ \mathsf { m V }$ . Figure 4-11 shows howthis will affect the first wavedetection at a given, fixed offsetfor the first wave detection. Oncethe first wave amplitude is belowthe offset level the measurementresult will jump by one period.

![](images/32002cdde75a4e10356e75c808955d1f8e36ac62c102c65dbe794c723a255184.jpg)



Figure 4-11: Wrong measurement due to signal damping


With the TDC-GP22‘s first wave detection the time-of-flight measurement is related to thefirst wave and gets independent from temperature and flow. Miscalculations due to wrongzero crossing assignment are no longer possible.

Additionally, the measurement of the width of the first half wave gives the user a chanceto monitor the signal quality and to adjust the first wave offset trigger level if necessary.

The following figure shows the measurement flow in TDC-GP22 first wave mode.

![](images/b215bb2915c8ab0ca89a535c3684a3bfd7dd28d20bbae069c7b268ec0f0a6f40.jpg)



Figure 4-12: First Wave Mode


1. With the fire pulse generator the offset for the first wave detection is set to aprogrammable level. The DELVAL1 stop masking is used for surprising any noise and it isset just roughly close to the minimum expected time-of-flight. Further noise will besuppressed by the comparator offset until the receive signal reaches the amplitude abovethis offset level.

2. The TDC-GP22 measure the time interval between rising and falling edge of the firstwave. Then, it automatically sets back the offset to $\textsf { O m V }$ . With $< 1 \mathrm { \ m V }$ offset the offsetdrift of the flow measurement over temperature is minimized.

3. The stop masking for the three time measurements is set by parameters DELREL1 toDELREL3, relative to the first wave. E.g. DELREL $\uparrow = 3$ says the 3rd wave after the firstwave is measured.

4. The half wave period (hwp) of the first true time measurement is measured as areference for the first wave. In the example from figure 4-12 this would be the width ofthe 5st wave.

The ratio hwpfirst wave/hwpfirstToF is in the range of “0” to “1”, typically less than “1”. Thesmaller the value the weaker is the receive signal. The information can be used to monitorthe flow meter. If there are too many deposits over the years of operation and the signalration drops e.g. below “0.5” then the second wave can be used as reference in thefuture.

The signal drop might also be caused by bubbles in the water. Therefore, an alarmmessage can be sending in parallel to the operator.

5. TDC-GP22 automatically calculates all three stop event and further calculates theaverage of the three which will be available from register 4. This way, the communicationwith the microprocessor is simplified a lot. As soon as the interrupt is set the processorcan immediately read all three results or just the average value. There is no need to re-write register 1 like it was with TDC-GP21.

6. In case the spool piece is empty then there will be no stop signal. The offset w ill stay atthe level for the first wave detection. This way, noise can not trigger the TDC and the TDCwill run into a time-out.

In other words: the timeout is an indicator for an empty tube.

# 4.4.1 Configuration

The relevant configuration parameters are:


Table 4-3: First Wave Mode Configuration


<table><tr><td>Reg</td><td>Bits</td><td>Parameter</td><td>Description</td></tr><tr><td>3</td><td>30</td><td>EN_FIRST_WAVE</td><td>1 = Switches on the First Wave Mode, Reg3, DELVAL2 and Reg4, DELVAL3 get a new meaning.</td></tr><tr><td>4</td><td>8 - 12</td><td>OFFS</td><td>2&#x27;s complement number setting the offset shift in 1 mV steps
0 = 0 mV
1 = +1 mV
...
15 = +15 mV
16 = -16 mV
17 = -15 mV
...
31 = -1 mV</td></tr><tr><td>4</td><td>13</td><td>OFFSRNG1</td><td>1 = Additional offset shift by - 20 mV</td></tr><tr><td>4</td><td>14</td><td>OFFSRNG2</td><td>1 = Additional offset shift by + 20 mV</td></tr><tr><td>3</td><td>8 - 25</td><td>DELREL1 to DELREL3</td><td>Stop masking, select the xth wave for time-of-flight measurement. Maximum is the 63rd wave. DELREL1 ≥ 3. DELREL1 to DELREL3 have to be set in ascending order. Example:
DELREL1 = 3, DELREL2 = 4, DELREL3 = 5 means to measure 3rd, 4th and 5th wave after the first wave</td></tr><tr><td>4</td><td>16</td><td>DIS_PWM</td><td>0 = switch on / 1 = switch off pulse width measurement. The ratio can be read from address 8, register PW1ST as an 8 bit fixed point number with one integer bit (range 0 to 1.99).</td></tr><tr><td>4</td><td>15</td><td>EDGE_FW</td><td>Sets the edge sensitivity for the first wave. With a negative offset it is reasonable to trigger on the falling edge of the first wave.
0 = rising edge, 1 = falling edge</td></tr><tr><td>3</td><td>31</td><td>EN_AUTOCALC_MB2</td><td>1 = switch on the automatic calculation of all enabled hits. The sum of the results is written to read measurement result 4 at read register address 3 (=RES_3).</td></tr></table>

# 4.5 Temperature Measurement

Especially for heat meter applications the TDC-GP22 has a PICOSTRAIN basedtemperature measuring unit that offers high resolution and very low current consumption.

The measurement is based on measuring discharge times. Therefore, a capacitor isdischarged alternately through the sense resistors and the reference resistors. As animprovement compared to TDC-GP2, the TDC-GP22 has the comparator alreadyintegrated.

![](images/d58621b16b83772d492662048f40ab08108d9f2e2a5c275f1e24d8ee9f78005a.jpg)



Figure 4.13


The unit has 4 resistor ports, two of them to be used for the temperature sensors for hotwater (up) and cold water (down). The other two ports are used for reference resistors.Basically, on reference resistor connected to both ports is suffici ent.

The temperature sensors should have a minimum resistance of 500 Ohm. The cablelength should not exceed $^ { 3 \textrm { m } }$ . TDC-GP22 can measure 2-wire sensors only. It is notpossible to use 4-wire sensors. The precision of the temperature measurement is farwithin the limits of the standard for heat meters when PT500 or PT1000 are used. Incombination with PT500 or PT1000 temperature sensors there is no need for tworeference resistors. A typical setup with one fixed reference is shown in figure 4-14.

The EMC protection is a recommendation from experience of acam-messelection gmbh.Further information will be shown in section 5.5 EMC Measures.

![](images/dab3f548be043cd1de6b95605a7104d845d0104f698e6d1811f9032fe270127e.jpg)



Figure 4.14: PT500 / PT1000 temperature measurement with one reference resistor


The temperature measurement is fully automated. It is triggered by the $\mu \Sigma$ sending theopcodes Start_Temp or Start_Temp_Restart. With Start_Temp_Restart the TDC-GP22measures the temperature twice, with a delay given in multiples of the 50 Hz/60 Hzperiod. This will be of help to reduce 50Hz/60Hz noise.

For a measurement, the TDC-GP22 starts with 2 or 8 dummy measurements at port PT1before it makes the real four measurements in the order $\mathsf { P T 1 } > \mathsf { P T 2 } > \mathsf { P T 3 } > \mathsf { P T 4 }$ . Afterthe 4 measurements have finished the interrupt flag is set. TDC-GP22 has the possibilityto inverse the order, making the dummy measurements at port PT4.

The four data are found in registers 0 to 3. From Res_3/RES_1 and RES_4/RES_2 themicrocontroller can calculate the ratio Rtemp/Rref. By means of a look-up table it cancalculate the temperature for the special type of sensor in use.

# Configuration

Register 0, bit 15, ANZ_FAKE sets the number of dummy measurements at the beginningof a temperature measurement. This is necessary to overcome mechan ical effects of theload capacitor.

ANZ_FAKE = 0

2 dummy measurements

ANZ_FAKE = 1

7 dummy measurements

Register 0, bit 16, T

CYCLE sets the cycle time for the temperature measurement.

TCYCLE = 0

128 µs cycle time $@$ 4MHz

TCYCLE = 1

512 µs cycle time $@$ 4MHz

Register 0, bit 17, ANZ_PORT sets the number of ports that will be used.

ANZ_PORT = 0

2 ports $= 1$ sensor

ANZ_PORT = 1

4 ports $= 2$ sensors

Register 6, bit 11, TEMP_PORTDIR sets the order of the port measurements

TEMP_PORTDIR $= \mathsf { O }$

$\mathsf { P T } \mathsf { 1 } > \mathsf { P T } \mathsf { 2 } > \mathsf { P T } \mathsf { 3 } > \mathsf { P T } \mathsf { 4 }$

TEMP_PORTDIR $= 1$

$\mathsf { P T } 4 > \mathsf { P T } 3 > \mathsf { P T } 2 > \mathsf { P T } 1$

Register 6, bit 15, HZ60 sets the base frequency for the delay between the up and downmeasurements for commands Start_TOF_Restart and Start_Temp_Restart.

HZ60 $= 0$

50 Hz base

HZ60 $= 1$

60 Hz base

Register 6, bits 18, 19, CYCLE_TEMP, selects the factor timer for triggering the secondtemperature measurement in multiples of 50/60Hz.

.5

.5

Register 6, bit 30, NEG_STOP_TEMP inverts this signal at the SenseT path. This ismandatory when the internal comparator is used. Without inversion the unit is compatibleto TDC-GP2 operation with an external Schmitt trigger

NEG_STOP_TEMP $= 0$ No inversion, TDC-GP2 compatible

$= 1$ Inversion, mandatory when the internal compara tor is used

# Recommended Capacitor Values

The discharge time should be about 150 µs. Therefore the capacitor should have thefollowing value:

PT500: 220 nF

PT1000: 100 nF

Please set TCYCLE $= 1$ to avoid timeout error.

# Recommended Capacitor Type

To get accurate results we recommend capacitor types with very low dC/dU. Werecommend:

C0G types or CfCap Series from Tayo Yuden

Please do not use X7R or similar capacitors.

# Current consumption

By means of the TDC technology the temperature measurement needs an extremely lowcurrent, much less than an A/D converter does.

A full temperature measurement with 2 sensors, 2 references am PT1000 sensor type,including all calculations takes less than $2 . 5 ~ \mu \mathsf { A s }$ . With one temperature measurement in30 seconds (typical for heat meters) the average current consumption is 0.08 $\mu \mathsf { A }$ only.This is about 50 times less than other solutions. A PT500 sensor doubles the current.

Note: During temperature measurement the start input has to be enabled.

# Error detection

Additionally the temperature unit checks the plausibility of the results. It is able to detect ashort circuit of the sensor or an open sensor. The TDC-GP22 provides in the relevantoutput register an error code instead of a measurement value.

1. Short circuit between lines: equivalent to a very short time interval $K \otimes \times { \mathsf { T } } _ { \mathsf { r e f } } = { \mathsf { 2 } } \mu \mathsf { s } \ @ $ $@$4 MHz). The TDC-GP22 writes a ’h0 to the output register of the shorted sensor.

2. Broken sensor/Short circuit against GND: equivalent to no stop signal or timeout. TheTDC-GP22 writes a ’hFFFFFFFF into the output register of the open sensor.

Note: Due to a bug it is necessary to have SEL_TIMO_MB2 at 2ms to get a correctinterrupt indication when 512 µs cycle time is selected.

1: Short circuit between lines: Error short

2: Short circuit LoadT against GND: Error open

3: Circuit circuit PT2 against GND: Measurementat PT1 with half the nominal discharge time assensor is in parallel to Rref, result out ofreasonable range

![](images/fef34cbbe78ffd8ff440ad53d6f50e4fd5c0fc38fc099bb383416ce6ce3a521a.jpg)



Figure 4-15: Short circuit indication



Table 4.4: Analog specification


<table><tr><td>Symbol</td><td colspan="2">Terminal</td><td colspan="2">Internal Schmitt trigger</td><td colspan="2">External Schmitt trigger2</td><td>Unit</td></tr><tr><td></td><td colspan="2"></td><td>PT500</td><td>PT1000</td><td>PT500</td><td>PT1000</td><td></td></tr><tr><td></td><td colspan="2">Resolution RMS</td><td>17.5</td><td>17.5</td><td>16.0</td><td>16.0</td><td>Bit</td></tr><tr><td></td><td colspan="2">SNR</td><td></td><td></td><td>96</td><td>96</td><td>dB</td></tr><tr><td></td><td colspan="2">Absolute Gain3</td><td>0.9912</td><td>0.9931</td><td>0.9960</td><td>0.9979</td><td></td></tr><tr><td></td><td rowspan="3">Absolute Gain vs. Vio3(gain factor)</td><td>3.6 V</td><td>0.9923</td><td>0.9940</td><td>0.9962</td><td>0.9980</td><td></td></tr><tr><td></td><td>3.0 V</td><td>0.9912</td><td>0.9931</td><td>0.9960</td><td>0.9979</td><td></td></tr><tr><td></td><td>2.5 V</td><td>0.9895</td><td>0.9915</td><td>0.9956</td><td>0.9979</td><td></td></tr><tr><td></td><td colspan="2">Gain-Drift vs. Vio</td><td>0.25</td><td>0.23</td><td>0.06</td><td>0.04</td><td>%/V</td></tr><tr><td></td><td colspan="2">max. Gain Error(@ dθ = 100 K)</td><td>0,05%</td><td>0,05%</td><td>0,02%</td><td>&lt; 0.01%</td><td></td></tr><tr><td></td><td colspan="2">Gain-Drift vs. Temp</td><td>0.022</td><td>0.017</td><td>0.012</td><td>0.0082</td><td>%/10 K</td></tr><tr><td></td><td colspan="2">Gain-Drift vs. Vio</td><td></td><td></td><td>0,08</td><td></td><td>%/V</td></tr><tr><td></td><td colspan="2">Initial Zero Offset</td><td>&lt; 20</td><td>&lt;10</td><td>&lt; 20</td><td>&lt; 10</td><td>mK</td></tr><tr><td></td><td colspan="2">Offset Drift vs. Temp</td><td>&lt; 0.05</td><td>&lt; 0.03</td><td>&lt; 0,012</td><td>&lt; 0.0082</td><td>mK/ °C</td></tr><tr><td></td><td colspan="2">PSRR</td><td></td><td></td><td>&gt;100</td><td></td><td>dB</td></tr></table>

1 All values measured at $\mathsf { V i o } = \mathsf { V c c } = 3 . 0 \mathrm { ~ V ~ }$ , Cload $=$ 100 nF for PT1000 and 200 nF forPT500 (C0G-type)

2 measured with external 74AHC14 Schmitt trigger

3 compared to an ideal gain of 1

# Gain error and its mathematical correction

The TDC-GP22 temperature measurement is based on acam’s PICOSTRAIN technology.Here the resistance variation of an RTD is digitized by means of a high accurate timeinterval measurement. According to that, the Schmitt trigger’s delay time introduces aconsiderable gain error that results in a gain reduction compared to an ideal output value.This gain reduction can be mathematically described as a deviation from an ideal straightline. Hence, a simple mathematical correction by adding a correction factor compensatesfor this deviation from the ideal gain. It is calculated as follows:

$$
T _ {\text {c o r r}} = T _ {\text {u n c o r r}} / \text {g a i n f a c t o r}
$$

with

Tcorr: gain corrected temperature result

Tuncorr: uncorrected temperature result

gainfactor: gain correction factor, compensates the deviation from an ideal gain of 1

By means of this compensation, the effect of the Schmitt trigger’s delay time can bereduced to a residual gain error of $0 . 0 5 ~ \%$ of F. S. with the internal Schmitt trigger, oreven less in combination with an external 74AHC14 Schmitt trigger.

Three main parameters have to be considered, to select the correct gain factor:

 base resistance of the temperature sensor (e.g. PT500, PT1000)

 used Schmitt trigger (GP22-internal, external 74AHC14)

 GP22 supply voltage

The appropriate gain correction factors are provided in table 4-3 (“Absolute gain vs. Vio”).

# Import note:

The gain correction factors for the external Schmitt trigger exclusively refer to the74AHC14 Schmitt trigger. Other types (e.g. 74HC14) require different gain factors, inorder to ensure a correct compensation. According to that, we strongly recommend touse a 74AHC14 as external Schmitt trigger.

# Example 1:

Application with PT1000 Sensor, GP22 internal Schmitt trigger and 3.0 V supplyvoltage. According to table 4.3 a gain factor of 0.9931 has to be selected. The gaincorrected result is calculated then by the following equation:

$$
T _ {\text {c o r r}} = T _ {\text {u n c o r r}} / 0. 9 9 3 1
$$

# Example 2:

Application with PT500 Sensor, external 74AHC14 Schmitt trigger and 3.6 V supplyvoltage. Table 4-3 now specifies a gain factor of 0.9980. The gain corrected result iscalculated as follows:

$$
T _ {\text {c o r r}} = T _ {\text {u n c o r r}} / 0. 9 9 8 0
$$

# 5 Details and Special Functions

# 5.1 Oscillator

The TDC-GP22 uses up to 2 clock signals depending on the operating mode:

High-speed clock, typically 4 MHz, for calibration and as a predivider for the TDCmeasuring unit in measurement mode 2 and for the EEPROM

 32 kHz clock signal used for internal timer functions.

# 5.1.1 High-Speed Oscillator

Generally, the TDC-GP22 needs a high-speed clock for calibration. The recommend value is4 MHz, the possible range is 2 to 8 MHz (2 to 6 MHz in QUAD_RES mode). When runningin measurement mode 2 the TDC-GP22 needs the high-speed clock signal also as a part ofthe time measuring unit. Finally the operations need the high speed clock, too.

The oscillator takes an average current of 200 $\mu \mathsf { A }$ when running all the time. But as it isneeded only during the time measurement, the TDC-GP22 has the capability to control theon-time by itself. The settings are done with parameter START_CLKHS. WithSTART_CLKHS > 1 the oscillator is switched on after sending opcodes Start_TOF,Start_TOF_Restart, Start_Temp and Start_Temp_Restart for the duration of themeasurement. A delay between starting the oscillator and starting the measurementguarantees sufficient time for the oscillation to settle at full amplitude.

# Note:

It is strongly recommended to use a ceramic oscillator. Exactly because a quartz needsmuch longer to settle than a ceramic oscillator. This costs a lot current, but using aquartz oscillator has no advantage.

# START_CLKHS

= 0 Oscillator off

= 1 Oscillator continuously on

= 2 The measurement is started with 480 µs delay.

$\ c = 3$ same as ‘2’, but with 1.46 ms delay

$= 4$ same as ‘2’, but with 2.44 ms delay

$= 5$ to 7 same as ‘2’, but with 5.14 ms delay

![](images/c67fde831a900d36f181f69d0914fd8c09d0ad633ad41798f47dabfd8b6b4717.jpg)



Figure 5.1


The programmable delay guarantees that the oscillator has

settled before the measurement starts. For ceramic resonators 480 µs will be sufficient.

For quartz the necessary delay might reach the maximum of $5 . 1 4 ~ \mathrm { m s }$

By this measure the average current consumption can be drastically reduced.

# Example:

At one ToF measurement in an ultrasonic flow meter (forth/back) per second the high-speed oscillator is active only for about 2 ms.

The average current consumption is $1 3 0 \mu \mathsf { A } \mathsf { s } \ ^ { \star } \ 2 \mathsf { m } \mathsf { s } = 0 . 2 6 \mu \mathsf { A } .$

# 5.1.2 32.768 kHz Oscillator

The TDC-GP22 needs a 32.768 kHz reference for thestart-up control of the high-speed clock and the clockcalibration. It therefore offers an integrated low-powerdriver.

The 32.768 kHz oscillator is permanently running and hasa current consumption of only about $0 . 5 ~ \mu \mathsf { A }$ at 3.0 V. Thesettling time of this oscillator is about 3 s after power-up.The 32.768 kHz oscillator cannot be switched off. With anexternal 32 kHz clock from the microprocessor pinCLK32in has to be connected to GND.

![](images/f1dfb8cbfb2b1e80c43a950e49b7c7e809d47f92899c089c0a8cbb6552310d7a.jpg)



Figure 5.2


The low-power clock can be internally forwarded to anoutput pin to be available for an external microprocessor. The possible settings are:

SEL_TSTO1 = 7: 32 kHz output at pin FIRE_IN

SEL_TSTO2 = 7: 4 kHz (32 kHz/8) output at pin EN_START

It is also possible to provide an externallow-frequency rectangular clock at theCLK32Out pin (3.6 V max.).

![](images/833146cf0eccd30a11b90a9688ee2e5222a3a5afabc9acae24bffe8de6c8a97b.jpg)



Figure 5.3


# 5.1.3 Calibrating a Ceramic High-speed Oscillator

Using a ceramic oscillator for the 2 to 8 MHz clock will be attractive because it is of lowcost and has a fast settling time. Unfortunately it has a poor tolerance of 0.3 to $0 . 5 ~ \%$and shows a temperature drift. For this reason the TDC-GP22 allows to execute acalibration measurement that allows to compensate this behavior. This measurement isbased on the very precise 32.768 kHz clock. The TDC-GP22 generates start/stop pulsesfrom the 32.768 kHz and measures this time interval with its TDC unit. The result isstored in the result register and the interrupt flag is set. The frequency error of theceramic resonator can be calculated by the microprocessor. The calibration is configuredby setting register 0, ANZ_PER_CALRES and is started with “START_Cal_Resonator“ -instruction by the microprocessor.

The time interval to be measured is set by ANZ_PER_CALRES which defines the numbe r ofperiods of the 32.768 kHz clock:

ANZ_PER_CALRES $=$

$= 1$ $=$

$=$

$=$

The results is given in multiples of the high-speed clock and (divided by 1, 2 or 4(DIV_CLKHS)) as 32 bit fixed point numbers with 16 integer bits and 16 fractional bits.

The microcontroller can compare this measured value to the theoretical value andcalculate the correction factor for the frequency.

$$
R E S _ {t h e o r} = \frac {2 * \left(\frac {1}{3 2 , 7 6 8 k H z C l o c k} * 2 ^ {A N Z _ {-} P E R _ {-} C A L R E S}\right)}{t _ {4 M z R e s o n a t o r}} = t h e o r e t i c a l v a l u e
$$

$$
R E S _ {X} = m e a s u r e d v a l u e
$$

$$
\text {C o r r e c t i o n f a c t o r} = \frac {R E S _ {\text {t h e o r}}}{R E S _ {X}}
$$

Calibrated HSCLK freq. $=$  HSCLK freq. * Correction factor

# Example:

```txt
The system shall work with a 4 MHz resonator. With DIV_CLKHS = 0 and ANZ_PER_CALRES = 1 the theoretical result is 122.0703125μs/250ns = 488.28125 (RES_O = 'h01E84800). If the ceramic resonator in use is not exactly at 4 MHz but only 3.98 MHz the calibration measurement will show 485,83984375 (RES_O = 1E5D700). The correction factor for the microcontroller is 1.005.
```

Note: During clock calibration the start input has to be enabled.

# Source Code Example:

```c
//   
// Start Calibrate High Speed Clock Cycle   
// NOTE: It does not work in combination with EN_AUTOCALC = 1   
gp22_WR_config_reg(Bus_Type, 0x83, 0x00000000); // EN_AUTOCALC=0   
gp22_send_1byte(Bus_Type, Init);   
gp22_send_1byte(Bus_Type, Start_Cal_Resonator);   
// Wait for INT Slot_x   
Wait_For_Interrupt(Bus_Type);   
//Calculate Correction factor (ANZ_PER_CALRES=1)   
CLKHS_freq_corrFact = 122.070/ gp22_read_n_bytes(Bus_Type, 4, 0xBO, 0x00, 16) * CLKHS_freq;   
printf("\n Correction factor for clock = %1.3f\n", CLKHS_freq_corrFact);   
CLKHS_freq_cal *= CLKHS_freq_corrFact; // Calibrated Clock frequency   
gp22_WR_config_reg(Bus_Type, 0x83, 0x80000000); // EN_AUTOCALC=1
```

# 5.1.4 How to use Clock Calibration

# a. Application

This option is dedicated especially to ultrasonic flow and heat meters. In those applicationsthe use of ceramic oscillators shows two main advantages: lower cost and less currentconsumption. Mainly because of the short oscillation start-up time of the ceramic oscillatorthe operating current can be reduced by several $\mu \mathsf { A }$ . Referring to 10 years of operationthis saves several 100 mAh in battery capacitance. There is no negative effect on theresolution when using this option the correct way.

# b. Jitter of the 32 kHz clock and consequences

The 32 kHz clock is very precise in frequency with only a few ppm error. However, thephase jitter is about 3 to 5 ns peak-peak. For this reason also a calibration measurement(Start_Cal_Resonator) has this error. When multiplying a measurement result with thecalibration result, the jitter of the calibration is transferred to the result by the ratiocalibration measurement time (see ANZ_PER_CALRES) to measurement time. Using apermanently updated calibration value will add a considerable jitter to the measurementresult.

# c. Application of this option in ultrasonic flow meters

A measurement result is always made of two single time-of-flight measurements inultrasonic flow meters, with and against the flow direction. The difference between thosemeasurements is a measure for the flow. To avoid an influence of the calibration jitter onthis measurement result it is necessary only to use the same calibration for both ToFmeasurements. Following this, the difference between the two ToF measurements will befree of the jitter of the clock calibration measurement. The clock can be calibrated onlybetween measurements that are not directly subtracted from each other.

# 5.2 Fire Pulse Generator

# 5.2.1 General Description

The fire pulse generator generates a sequence of pulses which is highly programmable infrequency, phase and number of pulses. The high-speed oscillator frequency divided by thefactor selected for DIV_CLKHS is used as the basic frequency. This frequency is internallydoubled and can freely be divided by a factor of 2 to 15. It is possible to g enerate 1 to127 pulses. If maximum 15 pulses are sent the phase for each pulse can be adjusted per

register configuration. The fire pulse generator is activated by sending opcode Start_TOF.The fire pulse maybe used directly for the START of the TDC.

The fire pulse generator provides 2 outputs, FIRE_UP and FIRE_DOWN. The driverstrength of each output is 96 mA $@$ 3.3 V. Furthermore, FIRE_DOWN output signal canbe inverted to double the signal amplitude. The outputs can be set individually High-Z.Alternately, the default level of the inactive buffer can be set to GND.

# 5.2.2 Configuration

# Number of pulses:

ANZ FIRE  $= 0$  Switch off fire pulse generator  $= 1$  1 pulse  $= 2$  2 pulses ... 127 pulses SEL_START_FIRE  $= 1$  Fire pulse is used as TDC START FIRE_DEFAULT  $= 0$  Default level High-Z (GP2 compatible)  $= 1$  Default level GND. Mandatory if the internal analog circuit and the recommended circuit with external R and C is used.

# Phase:

The phase of each pulse can be defined in register 5, PHFIRE[0..14], (Mandatory:PHFIRE[15] = 0), if not more than 15 pulses are sent. “0“ stands for HIGH-LOW and “1“for LOW-HIGH. The pulse sequence begins with the LSB and ends with the MSB .

# Example:

$$
A N Z _ {F I R E} = 1 5, P H F I R E = ^ {\prime} h 0 0 5 5
$$

![](images/f6349308d0b4a2eb20e4bb80550f784f7f2d431a14ab141ba8e95e793b6a2a8d.jpg)


It is an easy way to halvethe pulse frequency.For that use PHFIRE $=$‘h5555 and definingstraight number ofANZ_FIRE = 14.

# Fire pulse frequency:

The input signal fireclk1 for the fire pulse generator is derived from the high speed clockCLKHS and the selected value for the high speed clock divider DIV_CLKHS.

![](images/08ae422df5a388a583abfd0ebb86f284ed5724198ed4b9805fde7a52f66adc67.jpg)



Figure 5.3


This Signal is internally doubled and divided by DIV_FIRE.

DIV_FIRE $=$ 0 not permitted

1 divided by 2

2 divided by 3

15 divided by 16

Register 5, bit 19, DIS_PHASESHIFT actives the phase shift, which introduces additionalnoise to improve statistical behavior when averaging.

DIS_PHASESHIFT = 0 Phase shift on

DIS_PHASESHIFT = 1 Phase shift off

$$
f _ {f i r e c l k 2} = f _ {f i r e c l k 1} * \frac {2}{D I V \_ F I R E + 1}
$$

fireclk2 is used as reference signal for the FIRE_UP / FIRE_DOWN - signal which isemitted by the output buffers FIRE_UP / FIRE_DOWN of the fire pulse generator.

![](images/97ef1932e824c05d2469db2ac7c0a2bb9264728e16abab3c94e8a970e5dacce5.jpg)


Figure 5.4

As shown in Figure 16 at least 2 clock periods Tfireclk2 are required to send one fire pulse.One for the high phase and one for the low phase of the FIRE_UP/FIRE_DOWN outputsignal.

# Example:

$$
\mathrm {C L K H S} = 4 \mathrm {M H z}, \mathrm {D I V} _ {\mathrm {C L K H S}} = 1, \mathrm {D I V} _ {\mathrm {F I R E}} = 1
$$

$$
f _ {f i r e c l k 2} = f _ {f i r e c l k 1} * \frac {2}{D I V \_ F I R E + 1} = 2 M H z
$$

Max. frequency of the FIRE_UP / FIRE_DOWN output signal:

$$
f _ {F i r e 1 / F i r e 2} = \frac {1}{2} * f _ {f i r e c l k 2} = 1 M H z
$$

# Driver outputs:

The output drivers are configured by setting CONF_FIRE in register 5, bits 29 to 31:

CONF_FIRE configures the FIRE_UP and FIRE_DOWN outputs of the GP22. CONF_FIRE isused to control which of the outputs (FIRE_UP or FIRE_DOWN) are first fired when theStart_TOF_Restart command is issued. It is also used to individually enable or disablethese outputs.

Only one of the three bits may be set to 1:

Bit $3 1 \ : = \ : 1$

Fire both outputs (FIRE_UP and FIRE_DOWN) simultaneously. In thiscase, the FIRE_DOWN output is an inverted representation ofFIRE_UP.

Bit $3 0 = 1$

Enable FIRE_UP output only, or when Start_TOF_Restart is issued, firethis output first.

Bit $2 9 = 1$

Enable FIRE_DOWN output only, or when Start_TOF_Restart is issued,fire this output first.

# Note:

In register 5, bits 16 to 18, REPEAT_FIRE originally had been implemented for sing aroundmeasuring. Please set

REPEAT_FIRE = 0 no repetition

# 5.3 Fast Initialization

In measurement mode 1 the TDC-GP22 offers the possibility of a fast initialization.

Activated by setting register 1, bit 15, EN_FAST_INIT = “1“ the interrupt flag automaticallyinitializes the TDC. So the TDC is already prepared for the next measurement while thedata can be read out. This mode is for highest speed applications only. It is mostreasonable for un-calibrated measurements with only one stop.

# 5.4 Noise Unit

In case the user wants to improve the measuring results by averaging it is necessary thatthe values do not always display exactly the same time difference. Instead the user shouldprovide some “noise” so that different quantization steps of the characteristic curve of theTDC are involved. This can not happen with very constant time differences. One wouldconstantly hit the same LSB.

The noise unit enables the use of weighted averaging even for constant time differences.The noise unit adds a random offset to the start. It is dedicated to applications where theTDC gets a dummy start and measures the time difference between STOP1 and STOP2(e.g. laser range finders).

The noise unit is switched on by setting register 5, bit 28, EN_STARTNOISE $=$ “1“

# 5.5 EMC Measures

Regarding the EMC susceptibility, there are measures we can recommend:

 Most importantly: the housing of the spool-piece must be connected to theelectrical GND signal of the PCB

Using ferrite cores with ~100 Ohm $@$ 100 MHZ with a low DC resistance, e.g.MURATA - BLM18EG101TN1D - FERRITE BEAD (Impedance: 100 Ohm, DCResistance Max: 0.045 Ohm, DC Current Rating: 2000 mA, Ferrite Case Style:0603)

 Using capacitors (value = 1 nF) between fire outputs and GND

 Using a shielded cable

 Common mode chokes are not needed

With these measures, we usually see significant improvement.

Please make sure that the capacitors are of C0G type. Use no other types. Values up to

2.2 nF should work without too big disturbance on the measurement result.


EMC protection of transducer (acam-messelectronic gmbh)


![](images/ad9b5b96bb3052af0a803839ed871c3ff615ea822092db35e80ac3d475f64655.jpg)


![](images/232e27646b831bffeafa622144bff4d17644a90d7e7a2a70c1b69acd9bb4b735.jpg)



Figure 5.4


# 6 Applications

# 6.1 Ultrasonic Heat Meter

The TDC-GP22 is perfectly suited for low-cost ultrasonic heat meter designs. Thanks to theimplemented functionality, including precision temperature measurement, fire pulsegenerator, analog switches, comparator, windowing and clock calibration, it is sufficient toadd a simple microprocessor (without A/D converter).

The final circuit reaches a unknown level in compactness and small size. The followingdiagram shows the front end section of a typical ultrasonic heat meter as it might look likewhen TDC-GP22 is used.

![](images/7b67090aa33f8877e36a6c797afef61905499a4caec52c2798fe9306cbbaaba2.jpg)



Figure 6.1


The red parts illustrate the external components needed. The number is reduced to aminimum:

 In the ultrasonic path, the piezo transducers are connected through pairs of R andC.

 In the temperature path only a temperature stable reference resistor and acapacitor

 As oscillators take a 32.768 kHz and a ceramic 4 MHz oscillator. The FIRE_IN pincan be used as output driver for the 32.768 kHz clock, so the $\mu \mathsf { P }$ does not need alow power oscillator.

 For the power supply use separate bypass capacitors of sufficient size to block V ccand Vio. Separate both by a small resistor.

In total 11 low-cost elements only are needed for the measurement.

<table><tr><td>Register</td><td>Value</td><td>Typical example configuration</td></tr><tr><td>Register 0</td><td>'hA30B6800</td><td>ANZ FIRE = 10 (see register 6, too)
DIV FIRE = 3, fire pulse frequency = 4 MHz/4 = 1.0 MHz
ANZ_PER_CALRES = 0, the 4 MHz is calibrated by a 61.035 μs measurement
DIV_CLKHS = 0, the 4 MHz ceramic oscillator is internally used as it is START_CLKHS = 2, the ceramic oscillator has 480 μs to settle
ANZ_PORT = 1, use all 4 ports for the temperature measurement
TCYCLE = 1, 512 μs cycle time for the temperature measurement
ANZ_FAKE = 0, 2 fake measurements
SEL_ECLK_CMP = 1, use 4 MHz for the temperature measurement cycle definition
CALIBRATE = 1, mandatory in measurement mode 2 to be on
NO_CAL_AUTO = 0, mandatory in measurement mode 2 to have auto-calibration
MESSB2 = 1, switch on measurement mode 2 for measuring &gt; 2 μs.
NEG_STOP/NEG_START = 0, all set to rising edges
IDO = 'h00</td></tr><tr><td>Register 1</td><td>'h21444000</td><td>HIT2 = 2, HIT1 = 1: calculate 1. Stop - Start in measurement mode 2
EN_FAST_INIT = 0, off
HITIN2 = 0
HITIN1 = 4, measure 3 stops (in measurement mode 2 this includes the start, too, giving 4 hits)
CURR32K = 0, use default
SEL_START Fires = 1, use the internal direct wiring from the fire pulse buffer to the TDC start
SEL_TST02 = 0, EN_START active
SEL_TST01 = 0, FIRE_IN pin is used as fire in ID1 = 'h00</td></tr><tr><td>Register 2</td><td>'hA0230000</td><td>EN_INT = b0101, interrupt given by Timeout TDC or ALU ready
RFEDGE1 = RFEDGE2 = 0, use only rising edges
DELVAL1 = 8960, the first stop is accepted after 70 μs
ID2 = 'h00</td></tr><tr><td>Register 3</td><td>'hD0A24800</td><td>EN_AUTOCALC_MB2 = 1, automatic calculation of the sum of RES_O,
RES_1 and RES_2. This calculation does not increase the address pointer.
EN_FIRST_WAVE = 1, first hit detection mechanism is enabled
EN_ERR_VAL = 0, there is enough time to read the status register
SEL_TIMO_MB2 = 2, time out is generated after 1024 μs
DELREL1 = 8, DELREL2 = 9, DELREL3 = 10, measure the 8th, 9th and 10th stop after the first hit</td></tr><tr><td></td><td></td><td>ID3 = 'h00</td></tr><tr><td>Register 4</td><td>'h20004A00</td><td>DIS_PWM = 0, pulse width measurement is not disabledEDGE_PWM = 0, pulse width measured on rising edgeOFFSRNG1 = 0, no negative offsetOFFSRNG2 = 1, OFFS = 10: total offset = 20 mV + 10 mV = 30 mVID4 = 'h00</td></tr><tr><td>Register 5</td><td>'h40000000</td><td>CON_FIRE = 2, enable FIRE_UP. If opcode Start_TOF_Restart is used FIRE_UP and FIRE_DOWN are used alternately for up and down flow measurements. With the configuration described here the measurement cycle starts sending fire pulses at pin FIRE_UP. EN_STARTNOISE = 0, switch offDIS_PHASEHIFT = 0, phase noise unit is active to improve the statistical behaviorREPEAT_FIRE = 0, no sing-aroundPHFIRE = 0, no phase change in the fire pulse sequenceID5 = 'h00</td></tr><tr><td>Register 6</td><td>'hCOC06000</td><td>EN_ANALOG = 1, use the internal analog circuitNEG_STOP_TEMP = 1, use the internal Schmitt trigger for the temperature measurementDA_KORR = 0, offset is set in register 4TW2 = 3, 300 μs delay to charge up the capacitors of the highpass EN_INT = b0101, interrupt given by Timeout TDC or ALU ready (see also register 2)START_CLKHS = 2, the ceramic oscillator has 480 μs to settle (see also register 0)CYCLE_TEMP = 0, use factor 1.0 for the Start_Temp_RestartCYCLE_TOF = 0, use factor 1.0 for the delay between two ToF measurementsHZ60 = 0, 50 Hz baseFIRE0_REF = 1, mandatory when using the internal analog circuitQUAD_RES = 1, use 23 ps BINDOUBLE_RES = 0TEMP_PORTDIR = 0, standard order for T measurementANZ_FIRE = 10 (see register 0, too)ID6 = 'h00</td></tr></table>

# Measurement flow:

Power-on reset:

Send SO = ’h50

Calibrate Clock:

Send SO $=$ ’h03 Start_Cal_Resonator

Check-loop INTN = 0?

Send SO $=$ ’hB0, Read SI = RES_0

Correction factor $=$ 61.035/RES_0

# Measurement loop:

Temperature measurement, every 30seconds:

Send SO = ’h02 Start_Temp

Check-loop INTN = 0?

Send SO $=$ ’hB4, Read SI = STAT

STAT&’h1E00 $>$ 0: $- >$ Error routine

Send SO $=$ ’hB0, Read SI = RES_0

Send SO $=$ ’hB1, Read SI = RES_1

Send SO $=$ ’hB2, Read SI $=$ RES_2

Send SO $=$ ’hB3, Read SI = RES_3

Rhot/Rref $=$ RES_0/RES_1

Rcold/Rref $=$ RES_3/RES_2

Go to look-up table to get the temperature.

Time-of-flight measurement every halfsecond:

Send $\mathsf { S } \mathsf { D } = \mathsf { \Omega } ^ { } \mathsf { h } 7 \mathsf { D }$ Initialize TDC

Send SO $=$ ’h05 Start_TOF_Restart

Check-loop INTN = 0? (TOF_UP)

Send SO = ’hB4, Read SI $=$ STAT

STAT&’h0600 > 0: $- >$ Error routine,timeout $=$ empty tube.

Send SO = ’hB3, Read SI = RES_3

Send $\mathsf { S } \mathsf { D } = \mathsf { \Omega } ^ { } \mathsf { h } 7 \mathsf { D }$ Initialize TDC

Check-loop INTN = 0? (TOF_DOWN)

Send SO $=$ ’hB4, Read SI $=$ STAT

STAT&’h0600 > 0: $- >$ Error routine

Send SO = ’hB3, Read SI $=$ RES_3

$\mu \mathsf { P }$ can now start the data post-processingand calculate the flow and the heat.

Check signal strength via pulse width:

Send SO $=$ ’hB8, Read SI = PW1ST

If PW1ST < 0.3 signal is too weak, alarm

# 7 Miscellaneous

# 7.1 Bug Report

# 7.1.1 TDC-CAL read error without Quad resolution

In case quad resolution is not set then reading separately the TDC cal value will give awrong read value. The internal calibration value is correct, but the transfer to the readregister is not correct. Therefore, measurement data are not affected.

Effect in Measurement mode 2:

- In this mode the cal value is for information only. Further, quad resolution isrecommended anyway.

Effect in Measurement mode 1:

- Customers using auto calibration are not affected.

- Only customers that want to read uncalibrated data and do external calibration areaffected.

Workaround:

- The calibration data are not addressed directly after the calibration measurement butafter the next regular measurement, before the next INIT.

Example:

```txt
Reg1 = 'h21...  
Reg1 = 'h67...  
result0 = read(adr=0)  
cal = read(adr=1)  
INIT
```

# 7.1.2 Timeout Temperature Measurement

Note: Due to a bug it is necessary to have SEL_TIMO_MB2 at 2ms to get a correctinterrupt indication when 512 µs cycle time is selected.

# 7.1.3 Timeout and Pulse-width Measurement

Problem:

In case there is a timeout (e.g. because of air in the spool piece) the pulse -widthmeasurement starts but does not end before there is an INIT. The current is increased by500 $\mu \mathsf { A }$ . The problem appears only with active pulse-width measurement.

Solutions:

1. It is mandatory to answer to any interrupt from TDC-GP22 by minimum an INITcommand. Even in case you know the next data are bad you need to send an INIT to stopthe pulse-width measurement. Also in case you don’t read the data. Of course, timeouthas to be selected as an interrupt source.

2. If pulse-width information is not used then switch off this unit.

# 7.2 Last Changes

<table><tr><td>02.11.2011</td><td>Version 0.0 for release</td></tr><tr><td>27.01.2012</td><td>Version 0.1 for release, sections 6 and 7 modified</td></tr><tr><td>29.03.2012</td><td>Version 0.3 for release, 7.1.2 new, registers 1 and 4 corrected</td></tr><tr><td>24.05.2012</td><td>Version 0.4. for release, page 2-6, page 3-7</td></tr><tr><td>26.06.2012</td><td>Version 0.5. for release, page 7-1 and 7-2, section 7.1.3, page 2-9 package outline</td></tr><tr><td>15.02.2013</td><td>Version 0.6 for release</td></tr><tr><td>23.05.2013</td><td>Version 0.7 Correction Status register (EEflags). Smaller additions.</td></tr><tr><td>12.11.2013</td><td>Version 0.8 In Measurement Mode 2 Tmin=700ns adapted; Expands section 2.6 Power Supply, page 2-15; Description EN_ANALOG (Register 6) adds, page 3-12 Description of the ALU Operation Pointer adds; page 3-16; Important supplement to writing the EEPROM, page 3-18; Expands section 4.4 First Wave Mode, page 4-19 Description of the configuration of the Fire Pulse Generator adds, page 5-6 Add new section 5.5 EMC Measures, page 5-10 Revised the used registers, page 6-2;</td></tr><tr><td>13.03.2014</td><td>Version 0.9: EMC section corrected</td></tr></table>

![](images/585dfcac16367bf81cf59b316a111f96522cf32e805ade4fab5a45fe916d6239.jpg)


acam-messelectronic gmbh

Friedrich-List-Straße 4

76297 Stutensee-Blankenloch

Germany

Phone $+ 4 9$ 7244 7419 – 0

Fax $+ 4 9$ 7244 7419 – 29

E-Mail support@acam.de

www.acam.de

# acam-messelectronic gmbH

# is now

# Member of theams Group

The technical content of this acam-messelectronic document is still valid.

Contact information:

Headquarters:

ams AG

Tobelbaderstrasse 30

8141 Unterpremstaetten, Austria

Tel: $+ 4 3$ (0) 3136 500 0

e-Mail: ams_sales@ams.com