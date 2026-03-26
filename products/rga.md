---
model: SRS RGA
name: Residual Gas Analyzer
slug: rga

category: Analytical Instruments

price: "from $3,900"

price_prefix: "Starting From"

tile_desc: "Ultra-compact quadrupole mass spectrometer. All electronics in the sensor head — no separate chassis required."

image: "images/instr/rga/RGA_Wide.jpg"

datasheet: "https://thinksrs.com/downloads/pdfs/catalog/RGAc.pdf"
manual: "https://thinksrs.com/downloads/pdfs/manuals/RGAm.pdf"

quick_specs:
  - label: Mass Range
    value: "1 – 100/200/300 amu"
  - label: Min. Detectable PP
    value: "5 × 10⁻¹³ Torr (FC)"
  - label: Max. Operating Pressure
    value: "1 × 10⁻⁴ Torr"
  - label: Mass Resolution
    value: "Unit resolution (1 amu)"
  - label: Scan Rate
    value: "Up to 25 amu/sec"
  - label: Interfaces
    value: "USB, RS-232"
  - label: Flange
    value: "2.75\" ConFlat (CF)"
  - label: Multiplier Option
    value: "CHANNELTRON available"

description_title: "Compact Design, No Separate Electronics"

description_bullets:
  - "All electronics in the sensor head; no external chassis"
  - "USB and RS-232 interfaces standard"
  - "Included SRS RGA Windows software"
  - "LabVIEW and MATLAB drivers included"
  - "ConFlat flange mount, 2.75\" CF standard"
  - "Faraday cup standard; electron multiplier option"
  - "Up to 1 × 10⁻⁴ Torr total pressure operation"
  - "Scan rates up to 25 amu/sec analog"

spec_groups:
  - name: Mass Range
    rows:
      - ["RGA100", "1 to 100 amu"]
      - ["RGA200", "1 to 200 amu"]
      - ["RGA300", "1 to 300 amu"]
  - name: Detector
    rows:
      - ["Faraday cup sensitivity", "10 A/Torr (typ.)"]
      - ["Min. detectable partial pressure (FC)", "5 × 10⁻¹³ Torr"]
      - ["Electron multiplier option", "Min. detectable: 1 × 10⁻¹⁴ Torr"]
  - name: Operating Conditions
    rows:
      - ["Max. operating pressure", "1 × 10⁻⁴ Torr total"]
      - ["Min. operating pressure", "No lower limit (UHV compatible)"]
      - ["Bakeout temperature", "250 °C (300 °C without electronics)"]
  - name: Scan Parameters
    rows:
      - ["Analog scan rate", "Up to 25 amu/sec"]
      - ["Histogram dwell time", "25 ms to 1 sec per amu"]
      - ["Mass resolution", "Unit resolution (1 amu) across full range"]
  - name: Mechanical
    rows:
      - ["Flange", "2.75\" ConFlat (CF) standard; other flanges available"]
  - name: Interfaces
    rows:
      - ["Host interface", "USB (primary), RS-232"]
      - ["Software", "SRS RGA Windows app; LabVIEW VIs; MATLAB scripts"]
      - ["Power", "Supplied by USB or external 24 VDC"]

related:
  - label: "BGA244 Binary Gas Analyzer"
    url: "https://thinksrs.com/products/bga244.html"
  - label: "IGC100 Ion Gauge Controller"
    url: "https://thinksrs.com/products/igc100.html"

troubleshooting:
  - q: "Analog scan only displays noise around 10 -9 Torr"
    a: "Most likely the repeller cage is shorting to your vacuum chamber. The solution is to remove the repeller cage and operate without it. You can easily remove it by unscrewing it from the ionizer. Another possibility is that the filament is damaged. Measure the resistance between the filament supply and return pins of the feedthru flange (click here for picture ). A healthy filament will have a little less than an ohm of resistance. If you measure a very high resistance, the filament most likely needs replacing. You can order a replacement filament by clicking here . If the ionizer appears dirty or coated, you may wish to replace the whole ionizer (which includes the filament). You can order a replacement ionizer kit by clicking here ."
  - q: "Analog scan looks noisy after replacing the filament and removing the repeller cage"
    a: "Most likely your ionizer is contaminated and needs replacing. There are instructions in the manual on how to replace an ionizer. You can order a replacement ionizer kit by clicking here ."
  - q: "No communication with PC"
    a: "The most common problem is that a USB port is being used for communication along with an RS-232 to USB adapter that doesn't support 28.8 kBaud. Many RS-232 to USB adapters support 28.8 kBaud. One that many customers use is the UC232R-10 from FTDI (https://ftdichip.com/products/uc232r-10/)."
  - q: "When powering on an RGA300, a red warning indicator on the ECU lights, and a software message says mass range is limited"
    a: "Click here to download a detailed explanation and solution."
  - q: "Operating the RGA with the filament turned off"
    a: "Using the RGA Windows software, go to the HEAD menu and turn the filament off. Then proceed with taking data. The filament will be off until you turn it back on again. There is a hardware modification that can also be made to the RGA ECU that allows you to run without the filament. Click here to download instructions on the hardware modification."
  - q: "Option 2 Built-in Power Module needs installing"
    a: "Click here to download instructions on installing option 2."
  - q: "Problem communicating over ethernet with a direct connection from my RGA (with ethernet option) to the TCP/IP port on my computer"
    a: "Click here to download instructions on TCP/IP communication using a direct connection from your RGA to your computer."
---

The SRS RGA is a complete quadrupole mass spectrometer in a compact, flange-mounted package. Unlike older RGA designs that require a separate electronics chassis, the entire signal-processing electronics are housed inside the sensor head — you only need a USB or RS-232 cable to a PC.

The result is an instrument that installs cleanly into any vacuum system without external boxes, and connects directly to a laptop or desktop for analysis with the included RGA software.
