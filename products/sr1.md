---
datasheet: "datasheets/SR1c.pdf"

image: images/instr/sr1/SR1 MainPic.jpg

model: SR1
name: Audio Analyzer
slug: sr1

tile_desc: Two-channel audio analyzer with <−110 dBc THD+N for high-end audio equipment
  characterization.

troubleshooting:
  - q: "Instrument is unresponsive to front-panel button presses"
    a: "Try a power-up reset. Turn the power off, then while holding the Left Arrow (backspace) key down, turn the power back on. After two seconds release the Left Arrow (backspace) key. If this doesn't correct the problem the instrument will need to come back to SRS for service. Contact SRS for service."
  - q: "Problem communicating over ethernet with a direct connection from my SR1 to the TCP/IP port on my computer"
    a: "See the user manual for instructions on TCP/IP communication using a direct connection from your SR1 to your computer."

description_bullets:
- Analog & digital domain measurements
- ≤-112 dB THD+N
- 200 kHz frequency range
- ≤-118 dBu analog analyzer noise
- ±0.008 dB flatness
- Low Crosstalk
- ≤600 ps jitter (50 Hz to 100 kHz)
- Dual-Channel FFTs

price: $16950
buy_url: "https://thinksrs.com/mult/sr1ec.html"

quick_specs:
- label: Amplitude Range (rms)
  value: 1 μV to 28.3 V (balanced) 1 μV to 14.1 V (unbalanced)
- label: Amplitude Accuracy
  value: ±0.5 % (±0.043 dB) at 1 kHz
- label: Hi BW DAC
  value: 10 Hz to 200 kHz
- label: Hi Res DAC
  value: '10 Hz to 0.45Fs (Fs: 128 kHz or 64 kHz fixed, 24 kHz to 216 kHz adj.)'
- label: Frequency Accuracy
  value: ±0.0005 % (5 ppm)
- label: Frequency Resolution
  value: <Fs/2 24

spec_groups:
- name: Analog Signal Generator
  rows:
  - - Amplitude Range (rms)
    - 1 μV to 28.3 V (balanced) 1 μV to 14.1 V (unbalanced)
  - - Amplitude Accuracy
    - ±0.5 % (±0.043 dB) at 1 kHz
  - - Hi BW DAC
    - 10 Hz to 200 kHz
  - - Hi Res DAC
    - '10 Hz to 0.45Fs (Fs: 128 kHz or 64 kHz fixed, 24 kHz to 216 kHz adj.)'
  - - Frequency Accuracy
    - ±0.0005 % (5 ppm)
  - - Frequency Resolution
    - <Fs/2 24
  - - Output Configuration
    - Balanced Ground, Balanced Float, Unbalanced Ground, Unbalanced Float, Common
      Mode Test
  - - Source Impedance
    - 50 , 150 , 600 (balanced) 25 , 75 , 600 (unbalanced)
  - - Balanced
    - 30.5 dBm
  - - Unbalanced
    - 24.9 dBm
  - - Float Voltage
    - ±40 V
  - - 10 Hz to 20 kHz
    - -125 dB
  - - '>20 kHz'
    - -100 dB
  - - Flatness
    - (relative to 1 kHz)
  - - 20 Hz to 20 kHz
    - ±0.020 dB (typ. ±0.012 dB)
  - - 10 Hz to 64 kHz
    - ±0.025 dB
  - - 10 Hz to 200 kHz
    - ±0.05 dB
  - - 1 kHz, 4 Vrms
    - -112 dB, typ. (22 kHz BW)
  - - 20 Hz to 20 kHz
    - -106 dB + 1 μV (22 kHz BW) -100.5 dB + 1.7 μV (80 kHz BW) -97 dB + 2.5 μV (200
      kHz BW)
  - - 10 Hz to 100 kHz
    - -89 dB + 2.5 μV (200 kHz BW)
  - - Flatness
    - (rel. to 1 kHz, amplitude ≤4 Vrms)
  - - 20 Hz to 20 kHz
    - ±0.008 dB (typ. ±0.003 dB)
  - - 10 kHz to 64 kHz
    - ±0.02 dB
  - - 10 Hz to 200 kHz
    - ±0.03 dB
  - - Residual THD + N
    - (Hi BW DAC)
  - - 1 kHz
    - -86 dB (22 kHz BW)
  - - 22 Hz to 20 kHz
    - -85 dB + 1 μV (22 kHz BW) -84.5 dB + 1.7 μV (80 kHz BW) -82 dB + 2.5 μV (200
      kHz BW)
  - - 10 Hz to 100 kHz
    - -75 dB + 2.5 μV (200 kHz BW)
  - - Residual THD+N
    - (Hi Res DAC, Fs = 128 kHz)
  - - 1 kHz
    - -99 dB (22 kHz BW)
  - - 22 Hz to 20 kHz
    - -98 dB + 1 μV (22 kHz BW)
  - - 20 Hz to 57.6 kHz
    - -96.5 dB + 1.4 μV (57.6 kHz BW)
  - - Residual THD+N
    - (Hi Res DAC, Fs = 64 kHz)
  - - 1 kHz
    - -106 dB (22 kHz BW)
  - - 22 Hz to 20 kHz
    - -101 dB + 1 μV (22 kHz BW)
  - - Phased Sines
    - 0 to 360°, 0.001° resolution
  - - IMD
    - SMPTE/DIN, CCIF/DFD, DIM/TIM
  - - Noise
    - White, Pink, Filtered White/Pink, USASI
  - - Multitone
    - 1 to 50 tones
  - - MLS
    - Repetition rates from 2 8 to 2 20
  - - FFT Chirp
    - Equal power in each FFT bin
  - - Log-sine chirp
    - Swept-sine with log increasing frequencies
  - - Square
    - 10 Hz to 50 kHz frequency range
  - - Ramp
    - Fs/N frequency range (N≥20)
  - - Arbitrary
    - 256 Samples to 136k Samples
  - - Polarity
    - 10 Hz to Fs/4 frequency range
  - - Constant (Offset)
    - DC to 20 Vp (unbal) / 40 Vp (bal)
  - - Burst Types
    - Timed, externally triggered, externally gated, synchronous sine, shaped
- name: Digital Audio Signal Generator
  rows:
  - - Range
    - 16 mV to 10.2 V (110 load)
  - - Accuracy
    - ±10 % + 80 mV
  - - Range
    - 4 mV to 2.55 V (75 load)
  - - Accuracy
    - ±10 % + 20 mV
  - - Output Format
    - Balanced XLR (AES/EBU), dual-connector XLR, unbalanced BNC (SPDIF-EIAJ),dual-connector
      BNC, Optical (Toslink)
  - - Output Sample Rate
    - 24 kHz to 216 kHz
  - - Sample Rate Accuracy
    - ±5 ppm
  - - Output Impedance
    - 110 (balanced), 75 (unbalanced)
  - - Frequency Range
    - 10 Hz to Fs/2
  - - Frequency Resolution
    - <Fs/2 24
  - - Flatness
    - ±0.001 dB
  - - Harmonic/Spurious
    - -148 dB
  - - Phased Sine
    - 0 to 360° range, 0.01° resolution
  - - Square
    - 10 Hz to Fs/2 frequency range
  - - IMD
    - SMPTE/DIN, CCIF/DFD, DIM/TIM
  - - Noise
    - White, Pink, Filtered White/Pink, USASI
  - - MLS
    - Repetition rates from 2 8 to 2 20
  - - Ramp
    - Fs/N frequency range (N≥20)
  - - Arbitrary
    - 256 Samples to 136k Samples
  - - FFT Chirp
    - Equal power in each FFT bin.
  - - Log-swept sine chirp
    - Swept-sine with log increasing frequencies
  - - Polarity
    - 10 Hz to Fs/4 frequency range
  - - Burst waveforms
    - All allowed waveforms
  - - Burst types
    - Timed
  - - Digital Test Waveforms
    - Digital Constant, Count, Rotating Bits, Staircase, J-Test
  - - Dither
    - None, triangle and rectangular probability distribution
  - - Waveforms
    - Sine, square, uniform noise, BP filtered noise, chirp
  - - Frequency Range
    - 2 Hz to 200 kHz
  - - Amplitude Range
    - 0 UI to 13 UI
  - - Unbalanced
    - 0 to 637 mVpp
  - - Balanced
    - 0 to 2.55 Vpp
  - - Amplitude Range
    - 0 to 20 Vpp (balanced only)
  - - Frequency Range
    - 10 Hz to 100 kHz
  - - Cable Simulation
    - Simulates 100 m of digital audio cable
  - - Variable Rise Time
    - 5 ns to 400 ns
- name: Signal Measurements
  rows:
  - - Input Range (rms)
    - 62.5 mV to 160 V
  - - Input Configuration
    - XLR, BNC, Generator Monitor, Digital Audio Common Mode
  - - Balanced
    - 200 k / 95 pF
  - - Unbalanced
    - 100 k / 185 pF
  - - Input Termination (bal)
    - 300 , 600 , 200 k
  - - 10 Hz to 50 kHz
    - ≤-140 dB
  - - '>50 kHz'
    - ≤-135 dB
  - - Type
    - 16-bit sigma-delta
  - - Sampling Frequency
    - 512 kHz
  - - Frequency Range
    - DC to 228 kHz
  - - Type
    - 24-bit sigma-delta
  - - Sampling Frequency
    - 128 kHz or 64 kHz (fixed), 24 kHz to 216 kHz (adj.)
  - - Frequency Range
    - DC to 0.45Fs
  - - Input Format
    - Balanced XLR (AES/EBU), dual-connector XLR, unbalanced BNC (SPDIF-EIAJ), dual-connector
      BNC, Optical (Toslink)
  - - Input Sample Rate
    - 24 kHz to 216 kHz
  - - Input Impedance
    - Hi Z or 110 (balanced) Hi Z or 75 (unbalanced)

manual: "https://thinksrs.com/mult/sr1m.html"

resources:
- label: "What's New with SR1"
  url: "https://thinksrs.com/downloads/pdfs/other%20stuff/What%27s%20new%20with%20SR1.pdf"
- label: "SR1 Volatility Statement"
  url: "app_notes/Volatility Statement SR1.pdf"
---

The SR1 Dual-Domain Audio Analyzer is a stand-alone instrument that delivers cutting edge performance in a wide variety of audio measurements. It combines a versatile generator with analyzers operating in both analog and digital domains, supporting sampling rates up to 192 kHz for digital audio carrier measurements.

### User Interface

The SR1 runs Windows XP embedded, offering familiar operation via external peripherals or front-panel controls. Seven tabbed pages allow flexible screen arrangement with configurations saveable to internal storage or USB drives. The QuickMeas feature streamlines common audio measurements like level, SNR, frequency response, and crosstalk through simple setup questions, delivering clear result reports.

### Analog Signal Generator

![SR1 Generators](../images/instr/sr1/Generatorslg.jpg)

At the heart of SR1 is a uniquely flexible analog signal generator supporting standard waveforms including sine, chirp, burst sine, noise variants, intermodulation test signals, square waves, and arbitrary waveforms. Multiple waveforms combine for unlimited test possibilities. Performance metrics include ±0.008 dB flatness (20 Hz to 20 kHz) and residual THD+N of −106 dB. Multitone waveforms accommodate up to 50 tones with real-time calculation, while FFT Chirp automatically synchronizes with the FFT analyzer.

### Digital Audio Signal Generator

![SR1 Digital I/O](../images/instr/sr1/DigIOlg.jpg)

Nearly all analog waveforms appear in the digital generator with additional digital test waveforms. Output sampling adjusts continuously from 24 kHz to 216 kHz across single and dual connectors. Complete control extends to status bits, user bits, and validity bits. Carrier impairments include variable rise time, common mode sine waves, normal mode noise, and multiple jitter waveforms.

### Timebase

All of SR1's sampling clocks are derived from an internal timebase with 5 ppm accuracy. An optional atomic rubidium timebase offers superior long-term stability with ±5 × 10⁻¹¹ accuracy. External synchronization supports standard clocks, AES11 references, and video signals.

### Analyzers

The heart of SR1's measurement abilities is its versatile set of analyzers which operate symmetrically on both analog and digital audio signals with no need to purchase additional options. Up to two analyzers can operate simultaneously on either input type. The Time Domain Detector performs standard audio measurements with bandwidth limiting and weighting filters. FFT analyzers provide live spectral displays with zoom and heterodyne capabilities. Dual-channel FFT enables single-shot frequency response measurements. Additional analysis options include THD, IMD, histogram, and multitone analyzers.

### Digital Audio Interface

SR1 provides a complete set of measurements for digital interface testing. Direct measurements of carrier level, sampling frequency, and jitter in both time and frequency domains are included. Status bit decoding supports professional and consumer formats.

### Eye Diagram

![SR1 Eye Diagram](../images/instr/sr1/NewEyeDiagramlg.gif)

An optional 80 MHz transient digitizer (opt. 01) processes up to 2M samples, computing time records, spectra, jitter analysis, and probability distributions. Full-color eye diagrams support user-configurable limits for straightforward carrier testing.

### Automation and Programming

SR1 offers unprecedented flexibility for user scripting and remote programming. The instrument supports VBScript, Jscript, and Python scripting with complete instrument access and custom user-interface creation. A hierarchical GPIB command set operates via IEEE-488, RS-232, or Ethernet (TCP/IP VXI-11). Learning mode records keystrokes and operations, automatically converting them to VB or Jscript programs for future execution and editing.
