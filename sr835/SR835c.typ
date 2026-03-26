#import "srsds.typ": *
#show: datasheet-template

= Dual Lock-In Amplifier

#subtitle[SR835 --- DSP lock-in amplifier]


#v(2.5em)
#image("main.jpg", width: 100%, height: 3.4in, fit: "contain")
#v(1.5em)
#line(length: 100%, stroke: 0.5pt + brand-blue)
#v(1.5em)

#grid(
  columns: (7fr, 7fr),
  gutter: 2.5em,
  align: top,

  features-box[
    #set text(font: heading-font, fill: brand-blue, size: 11pt, weight: "regular")
    #set list(indent: 0.3em, body-indent: 0.5em, spacing: 1.4em)
    - Synchronous sampling architecture
    - Spur-free sine output
    - Phase-linear FIR filters
    - Dual-channel demodulation
    - 1 mHz to 1 MHz frequency range
    - >100 dB dynamic reserve
    - Time constant from 1 μs to 1 day
    - 0.01 degree phase resolution
    - USB and Ethernet interfaces
#v(1.0em)
    - SR835 ... \$3999 (U.S. list)
  ],

  [
    The SR835 is built on a fundamentally new architecture: synchronous sampling.
    A fractional-N clock synthesizer with sub-picosecond jitter locks the ADC and
    DDS clocks to an exact integer multiple of the reference frequency. This
    single innovation eliminates DDS spurs, enables synchronous filtering at any
    frequency, and allows time constants as short as one signal period---all
    without the compromises of traditional lock-in designs.

    The result is a dual-channel, dual-phase lock-in amplifier covering 1~mHz to
    1~MHz in a single 2U rack instrument. A dedicated 1~GHz DSP with a hardware
    FIR accelerator provides phase-linear digital filters that preserve signal
    waveshape with no overshoot and finite settling time. Two independent
    measurement channels share a common oscillator, enabling simultaneous
    two-signal measurement, harmonic detection, or vector network analysis---all
    without external hardware. Live Ethernet streaming, a built-in scan engine,
    FFT display, and a unified SCPI command set complete the instrument.
  ],
)

== A New Architecture

#columns(2, gutter: 1.4em)[

=== Synchronous Sampling

Traditional lock-in amplifiers run their ADC and DDS clocks independently of the
signal frequency. The SR835 takes a different approach: a fractional-N clock
synthesizer with sub-picosecond jitter locks both clocks to an exact integer
multiple of the reference. Because every sample window aligns precisely with the
signal period, a simple boxcar sum over one cycle completely nulls the
$omega$ and $2 omega$ mixer products---no high-order filter required. This is
the foundation from which the SR835's other advantages follow.

=== Spur-Free Sine Output

In a conventional DDS, the output frequency is not an exact sub-multiple of the
clock, producing phase-truncation spurs that can reach --70~dBc. With
synchronous sampling, the DDS clock is an integer multiple of the output
frequency, so every cycle of the waveform is identical. The spurs collapse
underneath the fundamental and the output is spectrally clean. The DDS also
supports arbitrary waveform generation for stimulus applications that require
non-sinusoidal drive.

=== Phase-Linear Digital Filters

The SR835 replaces the cascaded RC (IIR) filters of earlier lock-in amplifiers
with phase-linear FIR low-pass filters, executed on a 1~GHz DSP with a
dedicated hardware FIR accelerator. These filters have equal group delay at all
frequencies: the output preserves the true time-domain shape of the input signal
with no waveform distortion, no overshoot, and an impulse response that settles
to exactly zero---eliminating the long exponential tails of RC filters. For
control-loop applications, the reduced latency of a short FIR is a direct
improvement over an equivalent-bandwidth IIR cascade.

=== Synchronous Filter

Because sampling is synchronous, a boxcar FIR that sums over exactly one signal
period acts as a perfect comb filter, placing nulls at $omega$ and every
harmonic. Unlike older sync filters that worked only at low frequencies, this
provides $>=$ 80~dB rejection of mixer products across the full 1~mHz to 1~MHz
range. The filter tracks the reference automatically, and also enables true DC
measurement of the signal by notching out the $omega$ component. The fastest
time constant equals one period of the signal.

=== Auto Reference Tracking

A slow digital phase-locked loop continuously tracks the user's signal
frequency, keeping the internal oscillator locked even when the reference drifts.
This removes the need for a clean external reference in applications where the
signal source is not frequency-stable.

== SR835 Features

=== Dual-Phase Demodulation

Each channel computes X and Y simultaneously by multiplying the input against
precise cosine and sine waves derived from a numerical oscillator. No
square-wave switching or hidden latency---just true quadrature outputs with
stable phase.

=== Redesigned Inputs

A fully differential input topology features a precision JFET front-end stage
with 2~nV/√Hz input noise and an input impedance of 10~MΩ. Inputs are fully
floating, with an optional chassis ground connection. A rear-panel single-ended
input provides 1~nV/√Hz noise for applications demanding the lowest possible
noise floor.

Inputs are fully protected against overvoltage events by means of bootstrapped
transient voltage suppressors. In case of sustained overload, damage is avoided
by automatically disconnecting the inputs. The "trip" condition can be cleared
from the front panel or via the remote interface.

=== Time Constant and Filter Slope

The time constant is continuously adjustable from one signal period (or 1~μs) up
to a full day, or stepped in 1--2--5 decades. Filter slope is selectable from
6 to 24~dB/octave. Coefficients are precomputed and swapped seamlessly, so
bandwidth changes don't introduce glitches or transients. An up-sampler
interpolates between output samples, eliminating staircase artifacts at long
time constants.

=== Harmonic Detection

Higher harmonic detection is built into the reference generation. By scaling the
internal phase accumulator, the instrument locks to any integer multiple from 1×
to 99×, within range. Each channel can set its harmonic independently, allowing
simultaneous measurement of different spectral components.

=== Dual-Reference Detection

With two references, the instrument locks to their difference frequency. The
internal oscillator and external reference are both tracked, and the
demodulator measures the intermodulation product at their offset. This enables
two-tone measurements without external mixers or added hardware.

=== Vector Network Analysis

The two independent measurement channels can be configured as a ratio
measurement: one channel monitors the stimulus, the other the response. This
turns the SR835 into a vector network analyzer for characterizing transfer
functions with full amplitude and phase information, without additional
instruments.

=== Auxiliary Output Measurement Mode

The auxiliary outputs can be driven by any measured quantity. The selected
signal is normalized, offset, scaled, and mapped into the output range with
configurable full-scale, offset, and expansion. This allows zooming in on small
variations or centering signals, with clipping detection indicating when limits
are exceeded.

=== Parameter Scan Engine

Sweeps are handled internally, varying one parameter at a time in a controlled
way. Frequency, amplitude, offsets, or auxiliary outputs can be ramped between
limits over a set duration, using linear or logarithmic spacing. Scans can run
once, repeat, or reverse direction, all while measurement and capture continue
uninterrupted.

=== Data Capture Buffer

Data is written into onboard memory, supporting sustained acquisition from very
slow trends to high-speed sampling. The buffer holds up to one million points
and supports multiple formats, from X traces to full vector data. It can run as
single-shot, circular, or logarithmic capture, and can be externally triggered.

#colbreak()

=== Real-Time Ethernet or USB Streaming

Demodulated data can be streamed continuously over Ethernet or USB interfaces
for real-time use. Packets are sent using standard protocols, with selectable
formats and sizes to balance throughput and latency. Streaming runs
independently of capture, and sequence numbers allow detection of dropped
packets.

=== Front-Panel Touchscreen GUI

All functionality is exposed through a modern touchscreen interface that
replaces layered menus and knobs. Parameters are organized hierarchically with
touch targets sized for reliable use. Physical increment buttons remain for
fine control, giving both quick navigation and precise adjustment.

#features-box[
  #set text(font: heading-font, fill: brand-blue, size: 10pt, weight: "bold")
  Ordering Information
  #v(0.6em)
  #set text(font: body-font, fill: brand-blue, size: 9pt, weight: "regular")
  #table(
    columns: (auto, 1fr, auto),
    align: (left, left, center),
    [SR835],   [Dual-Channel Lock-In Amplifier],   [\$3999],
    [SR801],   [Remote Voltage Preamplifier (100~MΩ, 1.2~nV/√Hz)], [\$799],
    [SR802],   [Remote Current Preamplifier],                 [\$799],
    [O835RMD], [Double rack mount kit],                [\$100],
    [O835RMS], [Single rack mount kit],                [\$100],
  )
]

] // end columns (Feature Highlights)

#v(1fr)
#align(center, image("rear.jpg", width: 90%))

#pagebreak()

#columns(2, gutter: 2.4em)[
  #include("specs.typ")
]
