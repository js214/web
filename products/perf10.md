---
datasheet: "datasheets/PERF10c.pdf"

image: images/instr/perf10/PERF10_FP.jpg

manual: "manuals/PERF10m.pdf"

model: PERF10
name: Audio Atomic Clock
slug: perf10

tile_desc: Rubidium-referenced 10 MHz word clock for professional recording studios
  demanding ultimate timing accuracy.

description_bullets:
- Atomic stability and accuracy
- Eight 10 MHz, 75 Ω outputs
- 10 year aging less than 5 ppb
- Ultra-low phase noise

price: $4695

quick_specs:
- label: Accuracy at shipment
  value: ±0.05 ppb ( ±5 × 10 -11)
- label: Aging (after 30 days)
  value: <5 × 10 -11 (monthly) <5 × 10 -10 (yearly) 5 × 10 -9 (20 years, typ.)
- label: Spurious harmonics
  value: <-60 dBc
- label: Phase noise (SSB)
  value: <-130 dBc/Hz (10 Hz) <-140 dBc/Hz (100 Hz) <-150 dBc/Hz (1 kHz) <-155 dBc/Hz
    (10 kHz)
- label: Short term stability (Allan variance)
  value: <2 × 10 -11 (1 s) <1 × 10 -11 (10 s) <2 × 10 -12 (100 s)
- label: Warm-up time
  value: <6 minutes (time to lock)

spec_groups:
- name: Rubidium Oscillator
  rows:
  - - Accuracy at shipment
    - ±0.05 ppb ( ±5 × 10 -11)
  - - Aging (after 30 days)
    - <5 × 10 -11 (monthly) <5 × 10 -10 (yearly) 5 × 10 -9 (20 years, typ.)
  - - Spurious harmonics
    - <-60 dBc
  - - Phase noise (SSB)
    - <-130 dBc/Hz (10 Hz) <-140 dBc/Hz (100 Hz) <-150 dBc/Hz (1 kHz) <-155 dBc/Hz
      (10 kHz)
  - - Short term stability (Allan variance)
    - <2 × 10 -11 (1 s) <1 × 10 -11 (10 s) <2 × 10 -12 (100 s)
  - - Warm-up time
    - <6 minutes (time to lock)
- name: Outputs
  rows:
  - - Number of outputs
    - 8 BNC (rear panel)
  - - Output impedance
    - 75 Ω
  - - Output amplitude
    - 1 Vpp (terminated in 75 Ω)
- name: Environmental
  rows:
  - - Operating temperature
    - +10 °C to +40 °C
  - - Storage temperature
    - -55 °C to +85 °C
  - - Relative humidity
    - 95 % (non-condensing)
- name: General
  rows:
  - - AC power
    - 90 to 132 VAC or 175 to 264 VAC , 47 to 63 Hz, 50 W
  - - DC power
    - 12 VDC, 54 W (When equipped with Option 01)
  - - Dimensions
    - 19 × 3.5 × 10.125 (WHL)
  - - Weight
    - 8 lbs.
  - - Warranty
    - One year parts and labor on defects in materials and workmanship

resources:
  - label: "PRS10 Dimensional Dwg."
    url: "app_notes/RBoutline.pdf"

related:
  - label: "FS725 10 MHz Rubidium Frequency Standard"
    url: "fs725.html"
  - label: "PRS10 Rubidium Oscillator"
    url: "prs10.html"
---

The PERF10 is engineered for audio professionals and audiophiles requiring exceptional frequency reference stability. It incorporates Stanford Research Systems' proprietary PRS10 rubidium oscillator.

### Rubidium Performance

The device combines an oven-stabilized, third-overtone SC-cut crystal oscillator to deliver both atomic-level accuracy and superior jitter performance. Phase noise is approximately 30 dB superior at 10 Hz offset compared to competing rubidium clocks. Aging is less than 5 ppb over 10 years.

### Outputs

Eight rear-panel BNC connectors provide 10 MHz, 75 Ω outputs compatible with professional master clocks.

### Redundant Power

Option 01 enables operation from external 12 VDC power, supporting redundant operation where DC automatically substitutes during AC supply failure.
