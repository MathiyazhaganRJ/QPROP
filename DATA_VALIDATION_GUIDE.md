# QPROP to APC Wind Tunnel Data Correlation Guide

This document outlines the standard procedures for validating theoretical QPROP physics models against empirical wind tunnel data provided by APC Propellers (.PE0 files). 

Due to differing mathematical conventions between Mark Drela's formulations and industry-standard propeller data, specific conversion factors must be applied prior to direct performance comparison.

## 1. Velocity (V)
*   **QPROP:** Outputs flight speed in meters per second (**m/s**).
*   **APC:** Outputs flight speed in miles per hour (**mph**). 
*   **Conversion:** $V_{m/s} = V_{mph} \times 0.44704$

## 2. Advance Ratio (J)
Both parameters measure the forward distance traveled per revolution, but are non-dimensionalized differently.
*   **QPROP (`adv`):** Defined as $\frac{V}{\Omega R}$
*   **APC (`J`):** Defined as $\frac{V}{n D}$ (Industry Standard)
*   **Conversion:** $J = adv \times \pi$

## 3. Aerodynamic Coefficients (CT and CP)
Raw thrust ($C_T$) and power ($C_P$) coefficients cannot be compared directly between QPROP and APC due to differing reference areas.
*   **APC Formulation:** $C_T = \frac{T}{\rho n^2 D^4}$
*   **QPROP Formulation:** $C_T = \frac{T}{\frac{1}{2} \rho V_{tip}^2 \pi R^2}$
*   **Note:** QPROP's calculated $C_T$ is mathematically smaller than APC's $C_T$ for identical forces by a factor of roughly $3.87$. Direct comparison of these dimensional columns should be avoided.

## 4. Absolute Forces (Thrust and Power)
Absolute physical output parameters should be used as the primary metrics for model validation.
*   **Thrust:** Compare QPROP `T(N)` directly to APC `Thrust (N)`.
*   **Power:** Compare QPROP `Pshaft(W)` directly to APC `PWR (W)`.

## 5. Digital Twin Calibration Procedure
To accurately correlate a QPROP theoretical model with APC empirical data:
1. Generate the propeller geometry and run the QPROP simulation at identical RPM intervals as the corresponding APC dataset.
2. Compare the resulting absolute Thrust (N) and Power (W) outputs.
3. If QPROP over-predicts theoretical performance, open the `.prop` file and mathematically adjust the empirical airfoil coefficients located at the file header (e.g., reduce $C_{Lmax}$, increase $C_{D0}$).
4. Iterate the simulation until the theoretical QPROP force vectors precisely align with the physical APC wind tunnel bounds.
