# Weak Measurements for Quantum Information

Undergraduate research project, Université de Moncton — experimental investigation of **weak measurement** techniques applied to optical/quantum-information systems, using a two-laser interferometric setup read out with a National Instruments (NI) DAQ board.

Author: Kumar Rahul

---

## Table of Contents

- [Background and Motivation](#background-and-motivation)
- [Theory](#theory)
  - [Quantum State Characterization](#quantum-state-characterization)
  - [Weak Measurement and the Weak Value](#weak-measurement-and-the-weak-value)
  - [Optical Interference as a Measurement Pointer](#optical-interference-as-a-measurement-pointer)
- [Experimental Setup](#experimental-setup)
- [Repository Contents](#repository-contents)
- [How the Scripts Work](#how-the-scripts-work)
  - [`Time delay between 2 lasers.py`](#time-delay-between-2-lasers)
  - [`Interference Pattern with Filter.py`](#interference-pattern-with-filter)
- [Requirements](#requirements)
- [Usage](#usage)
- [Results](#results)
- [Future Work](#future-work)
- [References](#references)

---

## Background and Motivation

Characterizing quantum states accurately is foundational to quantum physics and underlies many real-world applications such as quantum computing, quantum cryptography, and quantum sensing. The conventional approach — **quantum state tomography** — performs a predefined set of strong (projective) measurements on an ensemble of identically prepared states and uses a reconstruction algorithm (e.g. maximum likelihood estimation) to infer the most likely state consistent with the data.

A key limitation of strong, projective measurement is that it necessarily disturbs the system: by the postulates of quantum mechanics, a strong measurement collapses the wavefunction onto an eigenstate of the measured observable, destroying information about the state's other properties (and about superpositions/coherences) in the process. This motivates an alternative paradigm — **weak measurement** — in which the system is only *weakly* coupled to a measuring apparatus, extracting partial information about an observable while leaving the quantum state (approximately) intact. Repeating a weak measurement over an ensemble, or following it with a strong measurement and post-selection, allows reconstruction of quantum states and observables (including the real and imaginary parts of the wavefunction) with minimal disturbance.

This project builds a tabletop optical analogue of a weak-measurement scheme: two coherent laser beams are combined and allowed to interfere, and their relative phase/timing is read out via photodiodes and a DAQ card. The interference signal plays the role of the "pointer" variable whose shift, in a true weak-measurement experiment, encodes the (generally complex) weak value of an observable.

## Theory

### Quantum State Characterization

For a quantum system described by a density matrix ρ, full characterization (tomography) requires measuring the expectation values of a complete set of observables (e.g. the Pauli operators for a qubit) over many identically prepared copies of the state, since a single projective measurement yields only one bit of information and destroys the state. The number of measurement settings required grows with the dimension of the Hilbert space, and each measurement necessarily perturbs the system being probed — this is the standard quantum back-action associated with strong measurement.

### Weak Measurement and the Weak Value

Weak measurement, introduced by Aharonov, Albert, and Vaidman (1988), couples a quantum system (the "system") to a measuring device (the "pointer," e.g. the transverse position of a photon, or in our case the relative phase/timing between two beams) through a weak, non-destructive interaction Hamiltonian:

  H = g(t) · Â ⊗ p̂

where g(t) is a coupling strength that is small compared to the energy scales of the system, Â is the observable being measured, and p̂ is the pointer's momentum operator. Because the coupling is weak, the interaction only slightly perturbs the pointer's wavefunction — too weak to resolve on a single trial — but it also only minimally disturbs the system.

When the weak measurement is followed by a strong, *post-selected* measurement onto a final state |f⟩, the average shift of the pointer, averaged over many trials, is proportional to the real part of the **weak value**:

  A_w = ⟨f| Â |i⟩ / ⟨f|i⟩

Unlike an eigenvalue, the weak value A_w is in general a *complex number* and can lie far outside the normal eigenvalue spectrum of Â — a counterintuitive feature known as **weak value amplification**, which has been exploited to measure extremely small physical effects (e.g. the spin Hall effect of light, sub-femtosecond time delays, and beam deflections far below the shot-noise limit).

- The **real part** of A_w shows up as a shift in the pointer's expectation value of position/time (what we try to resolve by measuring an interference/time-delay signal).
- The **imaginary part** of A_w shows up as a shift in the pointer's momentum, which for an optical pointer corresponds to a change in propagation direction or a modification of the interference fringe pattern.

Because the perturbation to the system is weak, weak measurements followed by post-selection can, over an ensemble of repeated trials, reconstruct the full complex wavefunction of a quantum state — including phase information that strong projective measurement alone cannot access — a technique known as **direct state tomography** (Lundeen et al., 2011).

### Optical Interference as a Measurement Pointer

In this project, two laser beams act as a stand-in for the system/pointer interaction: the interference pattern formed when the beams are recombined is highly sensitive to their relative phase and arrival-time difference, in direct analogy to how an optical pointer's wavefunction is shifted in a real weak-measurement experiment. Two complementary measurements are implemented:

1. **Time delay measurement** — the two beams are detected on separate photodiodes, and the cross-correlation of the two photocurrent traces is computed. The lag that maximizes the cross-correlation gives the relative time delay between the arrival of the two beams at the detectors, analogous to extracting the real part of a weak value (a pointer-position shift).

2. **Interference fringe measurement** — a single photodiode records the intensity of the recombined/interfering beam as a function of time (or of a scanned path-length difference), producing the classic sinusoidal(ish) interference pattern I(t) ∝ I₁ + I₂ + 2√(I₁I₂)·cos(Δφ), whose fringe visibility and phase are sensitive to the coherence and relative phase of the two beams — the optical analogue of a pointer-momentum shift.

Both signals are acquired with a National Instruments DAQ (`Dev1`, analog input channels `ai0`/`ai1`) and processed/plotted in Python.

## Experimental Setup

Two coherent laser sources are aligned so their beams can be combined/interfered on a beamsplitter. Fast photodiodes convert the optical intensity at each arm (or at the combined output) into a voltage signal, which is digitized by an NI data-acquisition card and streamed into Python via the `nidaqmx` driver for analysis.

![Experimental setup](https://github.com/rahulkr3101/Weak-Measurements-for-Quantum-Information/assets/92712071/d500dd69-7ea2-4ce8-ab1b-fdd04263fd41)

## Repository Contents

| File | Purpose |
|---|---|
| [`Time delay between 2 lasers.py`](Time%20delay%20between%202%20lasers.py) | Acquires two photodiode channels simultaneously and computes the relative time delay between the two laser signals via cross-correlation. |
| [`Interference Pattern with Filter.py`](Interference%20Pattern%20with%20Filter.py) | Acquires a single photodiode channel, applies a moving-average smoothing filter, logs the data to CSV, and plots the resulting interference pattern. |

## How the Scripts Work

### Time delay between 2 lasers

1. Configures an `nidaqmx.Task` with two analog input channels (`Dev1/ai0`, `Dev1/ai1`), one per photodiode, sampled continuously at 10 kHz for 1 second (10,000 samples per channel).
2. Reads both channels into a NumPy array and splits it into `laser1_output` and `laser2_output`.
3. Builds a time axis from the sample rate and number of samples.
4. Computes `np.correlate(laser1_output, laser2_output, mode='same')`, the cross-correlation between the two traces, and finds the time index of its maximum — this is the estimated relative time delay between the two beams.
5. Plots both photodiode traces on the same axes and annotates the plot with the computed time delay.

### Interference Pattern with Filter

1. Defines a simple `moving_average(data, window_size)` smoothing filter implemented with a sliding-window running sum (O(1) update per sample).
2. Configures a single analog input channel (`Dev1/ai0`) on the NI DAQ, sampled at 10 kHz for 1 second.
3. Acquires the raw photodiode voltage trace and applies the moving-average filter (window size 3) to reduce high-frequency noise.
4. Locates the peak of the raw signal (`peak_time`) and writes the raw time axis, raw data, filtered data, and peak index to a CSV file (`test.csv`) via `pandas`, then appends the raw sample array as an extra row with the built-in `csv` module.
5. Plots the filtered signal versus time to visualize the interference pattern.

## Requirements

- Python 3.x
- [`nidaqmx`](https://pypi.org/project/nidaqmx/) (NI-DAQmx Python driver — requires NI-DAQmx runtime/drivers and compatible NI hardware, e.g. an NI USB-6361 or similar multifunction DAQ device)
- `numpy`
- `pandas`
- `matplotlib`

Install the Python dependencies with:

```bash
pip install nidaqmx numpy pandas matplotlib
```

> **Note:** Both scripts require physical NI DAQ hardware connected and configured as device `Dev1` in NI MAX (Measurement & Automation Explorer). They will not run without the corresponding hardware attached.

## Usage

```bash
python "Time delay between 2 lasers.py"
python "Interference Pattern with Filter.py"
```

Each script will acquire live data from the connected photodiodes, process it, and display a `matplotlib` plot of the result. The interference-pattern script additionally writes the acquired data to `test.csv` in the working directory.

## Results

**Time-delay measurement** — cross-correlation output showing the measured delay between the two photodiode channels:

![Time delay output](https://github.com/rahulkr3101/Weak-Measurements-for-Quantum-Information/assets/92712071/53fdf4d7-1cd1-4e96-9a43-b490be65b331)

**Interference pattern** — filtered photodiode signal showing the characteristic interference fringe shape:

![Interference pattern output](https://github.com/rahulkr3101/Weak-Measurements-for-Quantum-Information/assets/92712071/7d352dec-8a7e-4b5c-b587-926f32cf0615)

## Future Work

- Introduce a true pre-selection/post-selection scheme (e.g. polarization pre/post-selection on a single photon or weak coherent beam) to directly measure a complex weak value rather than a classical interference proxy.
- Extend the single-pixel photodiode readout to a position-sensitive detector or camera to resolve spatial (transverse) weak-value amplification, as in the original spin Hall effect of light experiments.
- Automate scanning of the relative path length / phase (e.g. with a piezo-actuated mirror) to sweep out a full interference curve per acquisition rather than relying on a short time-domain capture.
- Apply the acquired pointer-shift data to reconstruct a density matrix via weak-value state tomography and compare against a standard strong-measurement tomography result.

## References

1. Y. Aharonov, D. Z. Albert, and L. Vaidman, "How the result of a measurement of a component of the spin of a spin-1/2 particle can turn out to be 100," *Phys. Rev. Lett.* **60**, 1351 (1988).
2. J. S. Lundeen, B. Sutherland, A. Patel, C. Stewart, and C. Bamber, "Direct measurement of the quantum wavefunction," *Nature* **474**, 188–191 (2011).
3. O. Hosten and P. Kwiat, "Observation of the Spin Hall Effect of Light via Weak Measurements," *Science* **319**, 787–790 (2008).
4. A. G. Kofman, S. Ashhab, and F. Nori, "Nonperturbative theory of weak pre- and post-selected measurements," *Phys. Rep.* **520**, 43–133 (2012).
