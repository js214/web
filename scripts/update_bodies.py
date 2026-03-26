#!/usr/bin/env python3
"""Update body text for remaining products."""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent

updates = {}

updates['sr715'] = """The SR715 and SR720 are high-performance LCR meters for accurate impedance measurement of passive components.

### Making Measurements

The instruments operate at test frequencies of 100 Hz, 120 Hz, 1 kHz, 10 kHz and 100 kHz (SR720 only). Drive voltage can be set to preset levels or adjusted from 0.1 to 1.0 V in 50 mV increments. Both series and parallel circuit models are supported.

### Binning

The meters support component sorting into as many as ten bins using pass/fail, overlapping, or sequential binning schemes.

### Test Fixtures

A kelvin fixture with four wires prevents current-carrying wire voltage drops from affecting measurements. RS-232 and GPIB connectivity are standard."""

updates['sr630'] = """The SR630 provides multi-channel temperature monitoring with 16 channels supporting B, E, J, K, R, S and T thermocouples with 0.1 \u00b0C resolution.

### Data Storage and Output

The device includes a 2,000-point memory for logging readings with timestamp capability. Four analog outputs proportional to temperature are provided. GPIB, RS-232 and printer interfaces enable remote access.

### Monitoring Functions

Individual channels support independent configuration for temperature limits and alarm settings. An audio alarm and relay closure activate when measurements exceed preset thresholds. The instrument can also function as a voltmeter with ranges from 30 mV to 100 V."""

updates['sr770'] = """The SR770 FFT Network Analyzer offers 102.4 kHz bandwidth with 90 dB dynamic range.

### High Dynamic Range

The SR770 has a dynamic range of 90 dB with no spurious responses larger than \u221290 dBc. Dual 24-bit DSPs manage data from a 16-bit ADC, delivering 100 kHz real-time bandwidth with zero dead time.

### Spectrum and Octave Measurements

Displays spectrum, power spectral density, and time records. Octave analysis computes 1/3 octave spectra with A-weighting for acoustics and noise applications.

### Synthesized Source

Low-distortion (\u221280 dB) synthesis generates sine waves, two-tone signals, pink/white noise, and chirp (100 \u00b5V to 1 V).

### Transfer Function and Analysis

Measures magnitude and phase response with 0.05 dB precision. Data tables, limit tables, harmonic/sideband analysis, and a built-in trace calculator are included."""

updates['sim900'] = """The SIM900 Mainframe supports up to eight SIM modules in a compact enclosure with shared computer interface.

### Communications

Standard RS-232 with optional GPIB. Two auxiliary RS-232 ports enable cascading multiple mainframes through a single connection.

### Timebase and Power

A 10 MHz VCXO synchronizes all modules. An optional timebase input allows phase-locking to external references. The power supply delivers \u00b15 V, \u00b115 V, and +24 V with 70 W total capacity.

### Start-Up Configuration

A 4000-byte start-up script automatically configures modules upon power-on."""

updates['cg792'] = """The CG792 is a multi-output synthesized clock generator for distributing synchronized signals across complex digital systems.

The instrument generates clock signals with exceptional frequency resolution and low jitter. Each output channel can be independently configured for frequency, phase, and amplitude, enabling flexible timing architectures for FPGA testing, ADC/DAC characterization, and digital communications development."""

updates['sr470'] = """The SR470 and SR474 optical shutters provide precise timing control of optical beams.

The instruments accept TTL trigger inputs and provide both manual and remote control. An adjustable delay allows precise timing between the trigger signal and shutter activation. The SR470 provides a single channel while the SR474 provides four independent channels. Both include RS-232 interfaces."""

updates['sr540'] = """The SR540 Optical Chopper provides frequency-stabilized modulation of optical beams for use with lock-in amplifiers.

The chopper operates from 4 Hz to 3.7 kHz with frequency stability better than 0.05 %. An internal crystal-referenced oscillator locks the chopper to a precise reference frequency. Both internal and external references are supported. A synchronous TTL reference output is phase-locked to the optical modulation."""

updates['sr542'] = """The SR542 Precision Optical Chopper provides high-stability frequency-locked modulation with exceptional frequency accuracy.

The chopper operates from 10 Hz to 3.1 kHz with frequency accuracy better than 10 ppm. A digital PID controller locks the chopper to an internal crystal reference or external source. When used with the SR860 or SR865A lock-in amplifier, the lock-in directly controls the chopper, virtually eliminating frequency drift."""

updates['sc10'] = """The SC10 is a compact precision frequency standard based on a rubidium atomic transition, providing a 10 MHz output with accuracy better than \u00b15 \u00d7 10\u207b\u00b9\u00b9.

The instrument features a small form factor suitable for portable applications. The 10 MHz output drives 50 \u03a9 loads and serves as a reference for frequency counters, signal generators, and other instruments. RS-232 interface provides remote monitoring."""

updates['fs725'] = """The FS725 Rubidium Frequency Standard provides a stable, accurate 10 MHz reference.

### Rubidium Oscillator

The instrument achieves frequency accuracy of \u00b15 \u00d7 10\u207b\u00b9\u00b9 and aging less than 5 \u00d7 10\u207b\u00b9\u00b9 per month.

### Outputs

Three rear-panel outputs provide 10 MHz sine wave (13 dBm into 50 \u03a9), 10 MHz CMOS square wave, and 1 PPS.

### Monitoring

RS-232 interface allows remote monitoring of oscillator parameters. A Windows monitoring application is available. Compact half-rack enclosure with optional rack mounting kits."""

updates['prs10'] = """The PRS10 is a compact rubidium oscillator module for OEM integration.

The module provides a 10 MHz output with accuracy of \u00b15 \u00d7 10\u207b\u00b9\u00b9 and aging less than 5 \u00d7 10\u207b\u00b9\u00b9 per month. The compact package (3.4 \u00d7 3.25 \u00d7 6.0 inches) and low power (15 W) make it suitable for embedding in other instruments. RS-232 provides access to all oscillator parameters."""

updates['fs740'] = """The FS740 GPS Time and Frequency System combines a GPS-disciplined oscillator with precision outputs.

### GPS Disciplined Oscillator

GPS satellite signals discipline an internal OCXO, achieving frequency accuracy of 1 \u00d7 10\u207b\u00b9\u00b2 over 24 hours. An optional rubidium oscillator provides holdover stability.

### Outputs

Ten configurable outputs provide 10 MHz, 5 MHz, 1 PPS, and programmable signals. Time accuracy is better than 25 ns relative to UTC when GPS-locked.

### Interfaces

GPIB, RS-232, Ethernet, and a web server provide full remote control and monitoring."""

updates['fs752'] = """The FS752 GPS/GNSS Disciplined Oscillator provides a stable 10 MHz reference disciplined by multiple satellite constellations.

The instrument receives GPS, GLONASS, Galileo, and BeiDou signals to discipline an internal OCXO, achieving frequency accuracy better than 1 \u00d7 10\u207b\u00b9\u00b2. Outputs include 10 MHz, 5 MHz, and 1 PPS signals. RS-232 and Ethernet interfaces provide remote monitoring."""

updates['fs710'] = """The FS710 provides a 10 MHz sine wave reference distribution amplifier with four outputs at +7 dBm (1 Vrms) into 50 \u03a9 loads.

The amplifier maintains low added phase noise and high isolation between outputs. BNC connectors with 50 \u03a9 impedance are used for all inputs and outputs. The compact half-rack enclosure can be rack mounted singly or in pairs."""

updates['fs730'] = """The FS730 and FS735 are frequency distribution amplifiers providing multiple phase-coherent copies of a reference signal.

The FS730 provides seven 10 MHz sine wave outputs at +7 dBm. The FS735 provides seven 10 MHz CMOS square wave outputs. Both include an internal VCXO that phase-locks to the input, providing clean outputs even with noisy input references. All outputs are phase-coherent and isolated."""

updates['nl100'] = """The NL100 Nitrogen Laser provides pulsed ultraviolet output at 337 nm for spectroscopy, dye laser pumping, and laboratory use.

The laser delivers pulses with peak power greater than 150 kW at repetition rates up to 20 Hz. Pulse duration is approximately 3.5 ns. The output beam is linearly polarized.

The instrument includes a built-in trigger generator and accepts external TTL triggers. No external gas supply is needed \u2014 the laser operates with ambient air."""

updates['mpa100'] = """The MPA100 OptiMelt determines melting points of pharmaceutical and chemical compounds with high accuracy and reproducibility.

The instrument uses digital image processing to automatically detect the onset of melting. Up to three samples can be measured simultaneously. A built-in camera captures the melting process, and recorded videos can be reviewed. The touchscreen interface provides simple setup and operation. Results include full traceability."""

updates['mpa160'] = """The MPA160 Visual Melting Point Apparatus provides a simple method for visual determination of melting points.

The instrument heats samples in standard capillary tubes with a programmable temperature ramp. An integrated magnifying optic and LED illumination provide a clear view of the sample during heating. Programmable start temperature, ramp rate, and end temperature allow customization for different materials."""

updates['qms100'] = """The QMS100 Gas Analyzer monitors gas composition at or near atmospheric pressure.

The instrument samples gas through a calibrated capillary inlet, ionizes it in a closed-ion-source chamber, and analyzes the ions with a quadrupole mass spectrometer. The closed-ion-source design provides enhanced sensitivity and reduced interference.

Real-time Windows software provides trending, alarm monitoring, and data logging. Multiple gas species can be tracked simultaneously."""

updates['ugapm'] = """The UGAPM Process Monitor provides continuous gas composition monitoring for process environments.

The instrument delivers real-time partial pressure measurements of multiple gas species simultaneously. A capillary inlet samples gas at or near atmospheric pressure for analysis by the internal quadrupole mass spectrometer.

Windows monitoring software provides trending displays, alarm management, and data logging for unattended operation."""

updates['uga120'] = """The UGA120 Universal Gas Analyzer is a versatile leak detector and gas analyzer for laboratory and production environments.

The instrument combines a quadrupole mass spectrometer with a flexible inlet system to detect and identify gas leaks, analyze gas mixtures, and monitor vacuum system contamination.

Real-time Windows software provides analog scan, histogram, leak detection, and pressure vs. time measurement modes. Multiple gas species can be tracked simultaneously with programmable alarms and data logging."""

updates['sr250'] = """The SR250 Gated Integrator and Boxcar Averager recovers fast, repetitive signals from noisy backgrounds.

The instrument provides a gate window as short as 2 ns positioned anywhere within a repetitive signal. The signal within the gate is integrated and averaged over many trigger events to recover signals buried in noise. The technique is effective for pulsed laser spectroscopy, time-resolved fluorescence, and similar applications.

The SR250 includes an exponential moving average filter with adjustable time constant. GPIB interface provides remote control of gate position, width, and sensitivity."""

updates['sr400'] = """The SR400 is a dual-channel gated photon counter for time-resolved photon counting experiments.

The instrument provides two independent counting channels with gate windows from 5 ns to 1 s. Gates can be independently positioned, allowing simultaneous measurement of signal and background. Count rates up to 200 MHz are supported with 5 ns pulse-pair resolution.

Built-in discriminators with adjustable threshold (\u2212300 mV to +300 mV) convert detector pulses to digital counts. Gate scanning sweeps the gate position across the signal, building a time-resolved histogram. GPIB and RS-232 interfaces provide remote control."""

updates['sim910'] = """The SIM910 JFET Voltage Preamplifier is a high-impedance, low-noise DC-coupled amplifier for the SIM900 mainframe.

The module provides selectable gain (1, 2, 5, 10, 20, 50, 100) with input impedance greater than 10\u00b9\u00b3 \u03a9. Input noise is 4 nV/\u221aHz at 1 kHz. Bandwidth extends from DC to 1 MHz (gain of 1). An input offset adjustment allows nulling DC offsets up to \u00b110 mV."""

updates['sim918'] = """The SIM918 Precision Voltage Source provides a stable, low-noise DC output for the SIM900 mainframe.

Four voltage ranges (\u00b11 V, \u00b110 V, \u00b1100 V, and \u00b1100 V with 10\u00d7 output) with 4\u00bd-digit resolution. Output noise is less than 3 \u00b5Vrms (0.1 Hz to 10 Hz) on the 1 V range. The output can scan linearly between two voltages at adjustable rates."""

updates['sim921'] = """The SIM921 AC Resistance Bridge provides high-resolution resistance measurement for cryogenic thermometry in the SIM900 mainframe.

The bridge measures resistance from 2 \u03a9 to 2 M\u03a9 with resolution better than 1 ppm. AC excitation at 15.9 Hz minimizes thermoelectric errors while keeping self-heating low. Excitation current is adjustable from 10 nA to 3 mA. Designed for precision temperature measurement using RTDs, germanium, and ruthenium oxide sensors."""

updates['sim922'] = """The SIM922 and SIM923 are temperature monitors for the SIM900 mainframe. The SIM922 reads silicon diode sensors; the SIM923 reads platinum RTDs.

Each module provides two input channels with independent 24-bit ADC conversion and 0.001 K resolution. Standard calibration curves are included with support for user-defined tables of up to 200 points. High and low temperature alarms with relay outputs are provided for each channel."""

updates['sim928'] = """The SIM928 Isolated Voltage Source provides a precision, low-noise DC output with complete electrical isolation for the SIM900 mainframe.

The module offers \u00b120 V output range with 1 mV resolution and less than 10 \u00b5Vrms noise (0.1 Hz to 10 Hz). The output is fully isolated from the mainframe ground, making it suitable for biasing sensitive experiments. Battery-backed operation ensures stability during mainframe communication."""

updates['sim940'] = """The SIM940 10 MHz Rubidium Oscillator provides a precision frequency reference for the SIM900 mainframe.

The module uses a rubidium atomic transition to provide a 10 MHz output with accuracy of \u00b15 \u00d7 10\u207b\u00b9\u00b9 and aging less than 5 \u00d7 10\u207b\u00b9\u00b9 per month. The output synchronizes the mainframe timebase when installed, providing a stable reference for all time-dependent modules."""

updates['sim960'] = """The SIM960 Analog PID Controller provides proportional-integral-derivative feedback control for the SIM900 mainframe.

The module computes the PID error signal in fully analog circuitry, ensuring no digital noise couples into sensitive experiments. Proportional gain ranges from 0.1 to 1000, with integral and derivative time constants from 0.1 ms to 10 s. An internal setpoint can be programmed via RS-232 or set from an external voltage."""

updates['sim964'] = """The SIM964 Analog Isolation Pre-Amp provides low-noise, electrically isolated preamplification for the SIM900 mainframe.

The module offers gain of 1, 10, 100, and 1000 with input/output isolation greater than 10\u2079 \u03a9. Input noise is 8 nV/\u221aHz at 1 kHz (gain of 100). The isolation barrier prevents ground loops between the signal source and the mainframe."""

updates['sim970'] = """The SIM970 Quad Digital Voltmeter provides four channels of DC voltage measurement for the SIM900 mainframe.

Each channel provides 7\u00bd-digit resolution with input ranges from 100 mV to 10 V full scale. Input impedance is greater than 10 G\u03a9. The four channels share a single ADC through a multiplexer, with measurement rates up to 14 readings per second per channel."""

updates['sim985'] = """The SIM983, SIM984, and SIM985 are scaling amplifier, isolation amplifier, and analog multiplier modules for the SIM900 mainframe.

The SIM983 Scaling Amplifier provides adjustable gain from \u221213.11 to +13.11 with 0.01 resolution and 1 MHz bandwidth. The SIM984 Isolation Amplifier provides electrically isolated signal amplification with gain of 1, 10, or 100. The SIM985 Analog Multiplier computes the real-time product of two analog signals with 1 MHz bandwidth.

These signal conditioning modules are designed for in-line processing of analog signals within SIM-based measurement systems."""

updates['sr10'] = """The SR10, SR11, and SR12 are audio signal switchers designed for use with the SR1 Audio Analyzer.

These switcher panels allow automated routing of audio test signals between multiple devices under test and the SR1 analyzer. The SR10 provides balanced audio switching, the SR11 provides unbalanced audio switching, and the SR12 provides digital audio switching. All models are controlled via the SR1's software interface."""

updates['sr445a'] = """The SR445A is a four-channel, 350 MHz preamplifier designed for fast pulse amplification in photon counting, nuclear spectroscopy, and time-resolved measurements.

### Output Drivers

The SR445A provides four independent amplifier channels, each with 350 MHz bandwidth, 1 ns rise time, and gain selectable from 5 to 625 (in factors of 5). Input and output impedance is 50 \u03a9, and noise performance is 6.4 nV/\u221aHz.

### Versatile Operation

Each channel recovers from overload in less than 3 ns, critical for high count rate applications. The channels can be cascaded internally for higher gain, or used independently for four separate signals. A 500 \u03a9 front-panel switch on channel 1 provides impedance matching for high-impedance detectors. Per-channel DC offset adjustments allow fine-tuning of signal baselines."""

updates['sr446'] = """The SR446 is a single-channel, DC to 4 GHz preamplifier designed for fast signal amplification and conditioning.

### Wideband Performance

The SR446 provides DC to 4 GHz bandwidth with less than 1 ns rise time. Voltage gain is selectable from 1 to 100 in six steps, with 50 \u03a9 input and output impedance.

### Front Panel Display and USB

A front-panel LCD display shows the current gain setting and input signal level. The instrument can be controlled via USB interface for automated test applications."""

updates['sr550'] = """The SR550, SR551, and SR552 are lock-in voltage preamplifiers designed to provide low-noise gain at the detector, before cable noise can degrade the signal.

The SR550 uses a FET input with 4 nV/\u221aHz noise, the SR551 offers a high-impedance (10\u00b9\u00b2 \u03a9) input for electrometer applications, and the SR552 uses a BJT input with 0.8 nV/\u221aHz noise for the lowest noise with low source impedance.

All three preamplifiers are powered directly from any SRS lock-in amplifier via a 9-pin cable (included). Gain is selectable from 1 to 100. The compact design places the preamplifier right at the experiment, minimizing cable noise and pickup."""

updates['sr554'] = """The SR554 is a transformer-input preamplifier designed for the lowest possible noise with low source impedances.

The SR554 achieves 0.1 nV/\u221aHz input noise by using a precision step-up transformer at the input, providing a voltage gain of 100 and matching low-impedance sources to the amplifier's optimal noise impedance. The transformer bandwidth extends from 0.01 Hz to 1 MHz.

Two modes of operation are available: bypassed mode with a gain of 100, and non-bypassed mode with a gain of 500 and a low-impedance output suitable for driving long cables. The preamplifier is powered from any SRS lock-in amplifier."""

updates['sr555'] = """The SR555 and SR556 are current preamplifiers for use with SRS lock-in amplifiers.

The SR555 provides high-bandwidth current-to-voltage conversion with a gain of 10\u2077 V/A and bandwidth from DC to 1 MHz. The SR556 offers lower noise with a gain of 10\u2076 V/A and bandwidth from DC to 50 kHz.

Both preamplifiers are powered from SRS lock-in amplifiers via the rear-panel preamp power connector. A DC bias input allows applying up to \u00b110 V to the signal source through the current input."""

updates['ec301'] = """The EC301 is a versatile potentiostat/galvanostat for electrochemical research and testing.

### Power Amplifier

The instrument delivers \u00b130 V compliance voltage and \u00b11 A maximum current with optional power boosters offering up to \u00b120 A.

### Stand-Alone Operation

An intuitive front panel enables independent operation. Indicator LEDs provide immediate visibility into instrument status.

### Software

SRSLab, provided at no cost, supports major electrochemical techniques. The open command set permits custom procedures using LabVIEW, MATLAB, or comparable languages.

### Electrochemical Impedance Spectroscopy

Built-in EIS spans 1 mHz to 100 kHz with 120 dB dynamic range.

### Scan Rate Performance

Fast cyclic voltammetry reaches scan rates up to 10 kV/s while acquiring potential, current and auxiliary signal at 250,000 samples per second."""

updates['perf10'] = """The PERF10 is engineered for audio professionals requiring exceptional frequency reference stability. It incorporates Stanford Research Systems' proprietary PRS10 rubidium oscillator.

The device combines an oven-stabilized, third-overtone SC-cut crystal oscillator to deliver both atomic-level accuracy and superior jitter performance. It achieves phase noise approximately 30 dB superior at 10 Hz offset compared to competing rubidium clocks.

Eight rear-panel BNC connectors provide 10 MHz, 75 \u03a9 outputs compatible with professional master clocks. Option 01 enables 12 VDC operation for redundant power setups."""

# Apply updates
count = 0
for slug, new_body in updates.items():
    md = ROOT / 'products' / f'{slug}.md'
    text = md.read_text(encoding='utf-8')
    m = re.match(r'^(---\n.*?\n---\n)(.*)', text, re.DOTALL)
    if not m:
        print(f'{slug}: no match')
        continue
    md.write_text(m.group(1) + '\n' + new_body + '\n', encoding='utf-8')
    words = len(new_body.split())
    count += 1
    print(f'{slug}: updated ({words} words)')

print(f'\nUpdated {count} files')
