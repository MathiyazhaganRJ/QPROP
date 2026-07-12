# QPROP to APC Wind Tunnel Data Correlation Guide

This document outlines the standard procedures for validating theoretical QPROP physics models against empirical wind tunnel data provided by APC Propellers (.PE0 files). 

Due to differing mathematical conventions between Mark Drela's formulations and industry-standard propeller data, specific conversion factors must be applied prior to direct performance comparison.

## 1. Velocity (V)
*   **QPROP:** Outputs flight speed in meters per second (**m/s**).
*   **APC:** Outputs flight speed in miles per hour (**mph**). 
*   **Conversion:** $V_{m/s} = V_{mph} \times 0.44704$

## 2. Advance Ratio (`adv` vs `J`)
They both measure how far the prop moves forward per revolution, but are defined differently.
*   **QPROP (`adv`):** Defined as $V / (\Omega R)$
*   **APC (`J`):** Defined as $V / (n D)$ *(The industry standard)*
*   **Conversion:** Multiply QPROP's `adv` by **$\pi$ (3.14159)** to get APC's `J`.

## 3. Aerodynamic Coefficients (CT and CP)
Raw thrust ($C_T$) and power ($C_P$) coefficients cannot be compared directly between QPROP and APC due to differing reference areas.
*   **APC Formulation:** $C_T = \frac{T}{\rho n^2 D^4}$
*   **QPROP Formulation:** $C_T = \frac{T}{\frac{1}{2} \rho V_{tip}^2 \pi R^2}$
*   **Note:** QPROP's calculated $C_T$ is mathematically smaller than APC's $C_T$ for identical forces by a factor of roughly $3.87$. Direct comparison of these dimensional columns should be avoided.

## 4. Absolute Forces (Thrust and Power)
Absolute physical output parameters should be used as the primary metrics for model validation.
*   **Thrust:** Compare QPROP `T(N)` directly to APC `Thrust (N)`.
*   **Power:** Compare QPROP `Pshaft(W)` directly to APC `PWR (W)`.

## 5. Digital Twin Calibration Methodology

When simulating a known propeller (e.g., a 15x8 propeller at 4000 RPM) in QPROP, theoretical outputs frequently exhibit slight discrepancies when compared against empirical APC wind tunnel data for the identical operating condition.

For instance, if QPROP predicts an overly optimistic **13.9 N** of thrust whereas the physical APC propeller yields only **11.4 N**:
*   **Aerodynamic Adjustment:** The theoretical airfoil coefficients ($C_{Lmax}$, $C_{D0}$) defined at the header of the `.prop` file must be mathematically adjusted to account for the physical inefficiencies of manufactured plastic propellers.
*   **Iterative Tuning:** To calibrate the digital twin, the $C_{Lmax}$ parameter is incrementally reduced and the $C_{D0}$ (parasitic drag) is incrementally increased within the `.prop` file.
*   **Validation:** The simulation (`qtool graph`) is re-executed iteratively until the QPROP theoretical Thrust and Power output columns align perfectly with the empirical APC wind tunnel measurements.
