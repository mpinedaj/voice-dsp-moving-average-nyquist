# voice-dsp-moving-average-nyquist

> **Digital Signal & Image Processing — Laboratory 1**  
> Voice Signal Acquisition, Moving Average Filtering, and Nyquist Sampling Verification.

---

## 📌 Project Overview
This repository contains the Python implementation for **Lab 1** of the Digital Signal and Image Processing course. The project focuses on processing real-time or pre-recorded audio signals through two main tasks:

1. **Part 1 — Audio Acquisition & Noise Reduction:** Capturing a voice signal contaminated with background noise and passing it through a **Moving Average (Comb) Filter** to minimize white noise.
2. **Part 2 — Sampling Rate & Nyquist Criterion:** Modifying the sampling rate ($f_s$) above and below the Nyquist limit to evaluate audio degradation and demonstrate the *aliasing* effect.

---

## 📐 Mathematical Model

### Moving Average Filter
For an input signal $x(n)$ consisting of $N$ discrete points, the filter computes the unweighted average over $M$ consecutive samples ($M < N$):

$$y(n) = \sum_{k=0}^{M-1} \frac{1}{M} x(n - k)$$

### Nyquist-Shannon Sampling Theorem
To prevent aliasing during discrete sampling, the sampling frequency $f_s$ must satisfy:

$$f_s \ge 2 \cdot f_{\max}$$

where $f_{\max}$ is the maximum frequency component present in the input voice signal.

---

## 🛠️ Requirements & Installation

Clone the repository and install the required dependencies:

```bash
git clone [https://github.com/your-username/voice-dsp-moving-average-nyquist.git](https://github.com/your-username/voice-dsp-moving-average-nyquist.git)
cd voice-dsp-moving-average-nyquist
pip install numpy matplotlib scipy sounddevice
