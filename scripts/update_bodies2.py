#!/usr/bin/env python3
"""Update body text for the 20 products with short feature descriptions."""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
updates = {}

updates['cg792'] = """The CG792 is a multi-output synthesized clock generator employing a sophisticated dual analog PLL architecture with intelligent spur avoidance algorithms for optimal reference frequency selection and minimal spurious content.

### Clock Outputs

The CG792 generates clocks from 1 mHz to 2.2 GHz with up to four synchronizable outputs. Random jitter is less than 1 ps rms with 11 digits of frequency resolution and 100 ps rise and fall times.

### Phase Control and Synchronization

A built-in phase measurement system enables automatic channel synchronization with hardware-based channel coupling. Both phase and frequency modulation are supported using standard waveforms or user-applied analog signals via rear-panel input.

### Timebase Options

Standard crystal, optional OCXO, and optional rubidium timebases are available for applications demanding higher precision.

### User Interface

An intuitive 5-inch color TFT touchscreen with capacitive touch interface organizes functions through tabs. USB, Ethernet, and RS-232 interfaces provide flexible system integration."""

updates['sr542'] = """The SR542 Precision Optical Chopper provides high-stability frequency-locked modulation with exceptional frequency accuracy and low phase jitter.

### Frequency Range and Accuracy

The chopper operates from 0.4 Hz to 20 kHz (blade-dependent) with 20 ppm frequency accuracy and 0.01\u00b0 phase resolution. Precision photo-etched blackened stainless steel blades are available in various configurations.

### Motor Design

A long-life brushless motor (BLDC) uses analog current amplification with 3-phase unchopped sinusoidal drive currents rather than PWM signals, minimizing EMI and vibrations.

### Synchronization

Flexible synchronization to internal clock, external reference, VCO input, or AC line. Six rear-panel reference outputs support synchronization of multiple instruments. When used with the SR860 or SR865A lock-in amplifier, the lock-in directly controls the chopper.

### Shutter Mode

The SR542 also functions as an optical shutter by setting the internal frequency to 0 Hz and controlling blade position via phase adjustment. USB interface provides remote PC control."""

updates['sim985'] = """The SIM983, SIM984, and SIM985 are scaling amplifier, isolation amplifier, and analog multiplier modules for the SIM900 mainframe.

### SIM983 Scaling Amplifier

The SIM983 provides adjustable gain from \u221213.11 to +13.11 with 0.01 resolution and 1 MHz bandwidth. Both inverting and non-inverting configurations are supported.

### SIM984 Isolation Amplifier

The SIM984 provides electrically isolated signal amplification with selectable gain of 1, 10, or 100. Input-to-output isolation exceeds 10\u2079 \u03a9, preventing ground loops between signal source and mainframe.

### SIM985 Analog Multiplier

The SIM985 computes the real-time product of two analog input signals with 1 MHz bandwidth and 1 % accuracy. Applications include power measurement, AM modulation/demodulation, and phase detection."""

updates['sr445a'] = """The SR445A is a four-channel, 350 MHz preamplifier designed for fast pulse amplification in photon counting, nuclear spectroscopy, and time-resolved measurements.

### Output Drivers

Each of the four independent amplifier channels provides 350 MHz bandwidth with 1 ns rise time. Gain is selectable from 5 to 625 (in factors of 5) with 50 \u03a9 input and output impedance and noise performance of 6.4 nV/\u221aHz.

### Versatile Operation

Each channel recovers from overload in less than 3 ns, critical for high count rate applications. Channels can be cascaded internally for higher gain, or used independently for four separate signals.

### Input Flexibility

A 500 \u03a9 front-panel switch on channel 1 provides impedance matching for high-impedance detectors. Per-channel DC offset adjustments allow fine-tuning of signal baselines."""

updates['sr400'] = """The SR400 Dual-Channel Gated Photon Counter offers a convenient, integrated approach to photon counting that avoids the complexity and expense of older counting systems.

### Counters

Two independent channels count at rates up to 200 MHz with gate generators providing counting gates from 5 ns to 1 s. Gate scanning allows the gate position to be swept across the signal, building a time-resolved histogram of photon arrivals.

### Signal Inputs and Discriminators

Analog signal inputs are internally terminated at 50 \u03a9, accepting signals between \u00b1300 mV with DC to 300 MHz bandwidth. Discriminator thresholds range from \u2212300 mV to +300 mV in 0.2 mV steps with 5 ns pulse-pair resolution.

### Count Periods

Programming supports 1 to 2000 count periods per scan with dwell times from 2 ms to 60 s.

### Outputs and Interfaces

Front panel displays up to 10\u2079 counts. D/A output options include A, B, A\u2212B, or A+B in logarithmic or linear scaling. RS-232 and GPIB interfaces with 2000-point internal data buffering are included."""

updates['sr250'] = """The SR250 Gated Integrator and Boxcar Averager module recovers fast, repetitive signals from noisy backgrounds using gated integration and signal averaging.

### Triggering

The SR250 may be triggered internally or externally. The internal rate generator is continuously variable from 0.5 Hz to 20 kHz in nine ranges.

### Signal Inputs

Input sensitivity ranges from 1 V/1 V to 1 V/5 mV, with protection to 100 V and 1 M\u03a9 impedance. An input filter removes unwanted signals, and unwanted DC offsets are easily nulled with a 10-turn potentiometer.

### Gate Timing

The delay is continuously adjustable from nanoseconds to 100 ms. Gate-delay jitter is only 20 ps + 0.01 % of the full-scale delay. Gate width ranges from 2 ns to 15 \u00b5s across eight ranges, expandable to 150 \u00b5s.

### Signal Averaging

A moving exponential average of 1 to 10,000 samples provides signal-to-noise improvements up to 100\u00d7 for random white noise backgrounds. Active Baseline Subtraction mode allows you to actively cancel baseline drift."""

updates['sr625'] = """The SR625 is a 200 MHz frequency counter with a built-in rubidium timebase that delivers extraordinary accuracy without an external reference.

### Rubidium Timebase

The integrated rubidium oscillator provides 5 \u00d7 10\u207b\u00b9\u00b9 frequency accuracy and \u00b12 \u00d7 10\u207b\u00b9\u00b9 stability after warm-up, eliminating the need for a separate frequency standard. Aging is less than 5 \u00d7 10\u207b\u00b9\u00b9 per month.

### Counter Performance

The counter measures frequency from 0.001 Hz to 200 MHz with up to 11-digit resolution (1 s gate time) and 100 ps period resolution.

### Timebase Output

A 10 MHz timebase output allows other instruments to be referenced to the rubidium standard. GPIB and RS-232 interfaces provide full remote control."""

updates['sr10'] = """The SR10, SR11, and SR12 are audio signal switchers designed for use with the SR1 Audio Analyzer.

### Automated Routing

These switcher panels allow automated routing of audio test signals between multiple devices under test and the SR1 analyzer, eliminating manual cable swapping during production testing and multi-channel measurements.

### Three Models

The SR10 provides balanced audio switching with transformer-isolated relay matrices. The SR11 provides unbalanced audio switching for single-ended test configurations. The SR12 provides digital audio switching for AES/EBU and S/PDIF signals.

### Integration

All models are controlled via the SR1's software interface, enabling fully automated test sequences across multiple DUTs."""

updates['perf10'] = """The PERF10 is engineered for audio professionals and audiophiles requiring exceptional frequency reference stability. It incorporates Stanford Research Systems' proprietary PRS10 rubidium oscillator.

### Rubidium Performance

The device combines an oven-stabilized, third-overtone SC-cut crystal oscillator to deliver both atomic-level accuracy and superior jitter performance. Phase noise is approximately 30 dB superior at 10 Hz offset compared to competing rubidium clocks. Aging is less than 5 ppb over 10 years.

### Outputs

Eight rear-panel BNC connectors provide 10 MHz, 75 \u03a9 outputs compatible with professional master clocks.

### Redundant Power

Option 01 enables operation from external 12 VDC power, supporting redundant operation where DC automatically substitutes during AC supply failure."""

updates['sr770'] = """The SR770 FFT Network Analyzer offers 102.4 kHz bandwidth with 90 dB dynamic range in a single-channel instrument.

### High Dynamic Range

The SR770 has a dynamic range of 90 dB with no spurious responses larger than \u221290 dBc. Through averaging, signals as small as \u2212114 dBc can be observed.

### Powerful Processing

Dual 24-bit DSPs manage data from a 16-bit ADC, delivering 100 kHz real-time bandwidth with zero dead time \u2014 approximately 10\u00d7 faster than typical 10 kHz analyzers.

### Spectrum and Octave Measurements

Displays spectrum, power spectral density, and time records. Real-time octave analysis computes 1/3 octave spectra with A-weighting for acoustics and noise applications (630 mHz to 80 kHz).

### Synthesized Source

Low-distortion (\u221280 dBc) synthesis generates sine waves, two-tone signals, pink/white noise, and chirp (100 \u00b5V to 1 V, 50 mA output).

### Transfer Function Analysis

Measures magnitude and phase response with 0.05 dB precision via synchronized source for characterizing amplifiers, filters, and electromechanical devices.

### Analysis Tools

Data tables display up to 200 selected frequencies. Limit tables track 100 upper/lower segments for pass-fail testing. Harmonic, sideband, and band analysis modes with a built-in trace calculator are all included."""

updates['sr555'] = """The SR555 and SR556 are current preamplifiers designed for use with SRS lock-in amplifiers.

### SR555 High-Bandwidth Current Preamplifier

The SR555 provides current-to-voltage conversion with a gain of 10\u2077 V/A and bandwidth from DC to 1 MHz, ideal for fast photodetector and beam-position monitor applications.

### SR556 Low-Noise Current Preamplifier

The SR556 offers lower noise current amplification with a gain of 10\u2076 V/A and bandwidth from DC to 50 kHz, optimized for sensitive current measurements.

### Common Features

Both preamplifiers are powered from any SRS lock-in amplifier via the rear-panel preamp power connector. A DC bias input allows applying up to \u00b110 V to the signal source through the current input, useful for biasing photodiodes and similar detectors."""

updates['sr550'] = """The SR550, SR551, and SR552 are lock-in voltage preamplifiers designed to provide low-noise gain at the detector, before cable noise can degrade the signal.

### Three Input Configurations

The SR550 uses a FET input with 4 nV/\u221aHz noise for general-purpose low-noise amplification. The SR551 offers a high-impedance (10\u00b9\u00b2 \u03a9) input for electrometer-class applications. The SR552 uses a BJT input with 0.8 nV/\u221aHz noise for the lowest noise with low source impedance.

### Remote Operation

All three preamplifiers are powered directly from any SRS lock-in amplifier via a 9-pin cable (included). Gain is selectable from 1 to 100.

### Compact Design

The small form factor places the preamplifier right at the experiment, minimizing cable length and reducing noise pickup. This is especially important when measuring extremely low-level signals where even short cable runs can introduce significant noise."""

updates['sr554'] = """The SR554 is a transformer-input preamplifier designed for the lowest possible noise with low source impedances.

### Transformer Input

The SR554 achieves 0.1 nV/\u221aHz input noise by using a precision step-up transformer at the input, providing a voltage gain of 100 and matching low-impedance sources to the amplifier's optimal noise impedance. The transformer bandwidth extends from 0.01 Hz to 1 MHz.

### Two Modes of Operation

In bypassed mode, the preamplifier provides a gain of 100 with the full transformer bandwidth. In non-bypassed mode, gain increases to 500 with a low-impedance output suitable for driving long cables to the lock-in amplifier.

### Power

The SR554 is powered from any SRS lock-in amplifier via the rear-panel preamp power port."""

updates['sr446'] = """The SR446 is a single-channel, DC to 4 GHz preamplifier designed for fast signal amplification and conditioning.

### Wideband Performance

The SR446 provides DC to 4 GHz bandwidth with less than 1 ns rise time. Voltage gain is selectable from 1 to 100 in six steps with 50 \u03a9 input and output impedance.

### Front Panel Display

A front-panel LCD display shows the current gain setting and input signal level, providing convenient real-time monitoring.

### USB Interface

The instrument can be controlled via USB interface for automated test applications, enabling integration into computer-controlled measurement systems."""

updates['uga120'] = """The UGA120 Universal Gas Analyzer is a versatile leak detector and gas analyzer for laboratory and production environments.

### Flexible Inlet System

The instrument combines a quadrupole mass spectrometer with a flexible inlet system that operates from atmospheric pressure down to UHV conditions. A calibrated capillary inlet samples gas at or near atmospheric pressure, while a direct connection supports high-vacuum analysis.

### Measurement Modes

Real-time Windows software provides analog scan, histogram, leak detection, and pressure vs. time measurement modes. Multiple gas species can be tracked simultaneously with programmable alarm thresholds and data logging.

### Fast Response

The system provides fast response time for leak detection and process monitoring applications. Stand-alone leak detection mode enables operation without a PC."""

updates['qms100'] = """The QMS100 Gas Analyzer monitors gas composition at or near atmospheric pressure for process and environmental applications.

### Closed-Ion-Source Design

The instrument samples gas through a calibrated capillary inlet, ionizes it in a closed-ion-source chamber, and analyzes the resulting ions with a quadrupole mass spectrometer. The closed-ion-source design provides enhanced sensitivity and reduced interference compared to open-source designs.

### Software and Monitoring

Real-time Windows software provides trending displays, alarm management, and data logging. Multiple gas species can be tracked simultaneously with programmable alarm thresholds for unattended operation."""

updates['ugapm'] = """The UGAPM Process Monitor provides continuous gas composition monitoring for demanding process environments.

### Real-Time Monitoring

The instrument delivers real-time partial pressure measurements of multiple gas species simultaneously. A capillary inlet samples gas at or near atmospheric pressure for analysis by the internal quadrupole mass spectrometer.

### Software and Automation

Windows monitoring software provides trending displays, alarm management, and data logging. The system can be configured for unattended operation with automatic alarm notification via relay outputs and software alerts."""

updates['nl100'] = """The NL100 Nitrogen Laser provides pulsed ultraviolet output at 337 nm for spectroscopy, dye laser pumping, and general laboratory use.

### Laser Performance

The laser delivers pulses with peak power greater than 150 kW at repetition rates up to 20 Hz. Pulse duration is approximately 3.5 ns. The output beam is linearly polarized with a divergence of approximately 4 \u00d7 8 mrad.

### Simple Operation

The instrument includes a built-in trigger generator and accepts external TTL triggers. No external gas supply is needed \u2014 the laser operates with ambient air. Only a standard AC power connection is required.

### Compact Design

The self-contained design makes the NL100 suitable for benchtop applications without the infrastructure requirements of larger laser systems."""

updates['mpa160'] = """The MPA160 Visual Melting Point Apparatus provides a simple, reliable method for visual determination of melting points.

### Temperature Control

The instrument heats samples in standard capillary tubes with a programmable temperature ramp. Programmable start temperature, ramp rate, and end temperature allow customization for different materials.

### Observation

An integrated magnifying optic and LED illumination provide a clear view of the sample during heating, allowing precise visual identification of the melting transition. The temperature display shows the current temperature with 0.1 \u00b0C resolution.

### Compact Design

The benchtop design requires minimal laboratory space while providing reliable results for quality control and research applications."""

updates['mpa100'] = """The MPA100 OptiMelt automated melting point system determines melting points of pharmaceutical and chemical compounds with high accuracy and reproducibility.

### Automated Detection

The instrument uses digital image processing to automatically detect the onset of melting, providing objective results independent of operator technique. Up to three samples can be measured simultaneously with independent detection for each capillary tube.

### Video Recording

A built-in high-resolution camera with LED illumination captures the melting process. Recorded videos can be reviewed for verification of results.

### Traceability

The touchscreen interface provides simple setup and operation. Results are stored with full traceability including sample ID, operator, date, and method parameters."""

# Apply all updates
count = 0
for slug, new_body in updates.items():
    md = ROOT / 'products' / f'{slug}.md'
    if not md.exists():
        print(f'{slug}: file not found')
        continue
    text = md.read_text(encoding='utf-8')
    m = re.match(r'^(---\n.*?\n---\n)(.*)', text, re.DOTALL)
    if not m:
        print(f'{slug}: no frontmatter match')
        continue
    md.write_text(m.group(1) + '\n' + new_body + '\n', encoding='utf-8')
    words = len(new_body.split())
    count += 1
    print(f'{slug}: updated ({words} words)')

print(f'\nUpdated {count} files')
