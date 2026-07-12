# QPROP vs APC: Data Validation & Correlation Guide

When validating your theoretical QPROP physics model against real-world wind tunnel data (like the APC `.PE0` files), you must apply specific mathematical conversions. Mark Drela (QPROP) and APC use completely different mathematical definitions for the exact same aerodynamic variables.

Yes, the APC data is **incredibly useful**. It allows you to "calibrate" your QPROP digital twin. If your QPROP output doesn't match the APC output for the same propeller, you can tweak the airfoil coefficients (`CLmax`, `CD0`) inside your QPROP `.prop` file until the numbers match reality perfectly.

---

## The Correlation Cheat Sheet

### 1. Velocity (The X-Axis)
*   **QPROP:** Outputs flight speed in **m/s**.
*   **APC:** Outputs flight speed in **mph**. 
*   *Conversion:* Multiply APC's mph by `0.44704` to get m/s.

### 2. Advance Ratio (`adv` vs `J`)
They both measure how far the prop moves forward per revolution, but are defined differently.
*   **QPROP (`adv`):** Defined as $V / (\Omega R)$
*   **APC (`J`):** Defined as $V / (n D)$ *(The industry standard)*
*   *Conversion:* Multiply QPROP's `adv` by **$\pi$ (3.14159)** to get APC's `J`.

### 3. The Coefficients (`CT` and `CP`) - ⚠️ DO NOT COMPARE DIRECTLY
You cannot compare the raw $C_T$ and $C_P$ columns between QPROP and APC. They use completely different non-dimensionalization formulas.
*   **APC (Standard):** $C_T = \frac{Thrust}{\rho \cdot n^2 \cdot D^4}$
*   **QPROP (Drela):** $C_T = \frac{Thrust}{\frac{1}{2} \rho \cdot V_{tip}^2 \cdot \pi R^2}$
*   *Conversion:* Drela's $C_T$ is mathematically $\sim 3.87$ times smaller than APC's $C_T$ for the exact same propeller. It is safer to ignore these columns and compare the physical real-world forces below.

### 4. Real-World Forces (Thrust and Watts) - ✅ SAFE TO COMPARE
These are absolute physical units and can be compared 1-to-1 to calibrate your model.
*   **Thrust:** Compare QPROP's `T(N)` directly to APC's `Thrust (N)`.
*   **Power:** Compare QPROP's `Pshaft(W)` directly to APC's `PWR (W)`.

---

## How to Calibrate Your Digital Twin

If you simulate a 15x8 propeller at 4000 RPM in QPROP, and compare it to APC's real wind tunnel data for a 15x8 at 4000 RPM, you will often find slight discrepancies. 

For example, if QPROP predicts **13.9 N** of thrust but APC measured **11.4 N**:
1. Open your `.prop` file.
2. Your theoretical airfoil coefficients (`CLmax`, `CD0`) at the top of the file are likely too "optimistic" compared to the cheap plastic used in real APC props.
3. Lower the `CLmax` slightly and increase `CD0` (parasitic drag).
4. Re-run `qtool graph` until your QPROP Thrust and Power columns perfectly match the APC wind tunnel numbers!
