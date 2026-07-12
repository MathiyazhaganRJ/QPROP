# QPROP to CAD: 3D Modeling & Pitch Calculation Guide

When transitioning from QPROP's aerodynamic analysis to 3D CAD modeling (Fusion 360, SolidWorks, etc.), you must correctly interpret the `.prop` geometry file. This guide outlines how to calculate traditional propeller pitch and how to loft the 3D blade geometry.

---

## 1. Calculating Actual Propeller Pitch (Inches)

In the RC and UAV industry, a propeller is usually defined by two numbers: `Diameter x Pitch` (e.g., `15x8` means 15-inch diameter, 8-inch pitch). 

QPROP calculates the blade twist angle **$\beta$ (Beta)** in degrees, but it does not explicitly spit out the "Pitch in inches". 

### The Pitch Formula
Pitch ($P$) is the theoretical forward distance the propeller would move in one full revolution if traveling through a solid medium (like a screw in wood). 
If you unwrap the circular path of a blade section into a flat triangle, the base is the circumference ($2 \pi r$) and the angle is $\beta$.

$$ P = 2 \pi r \tan(\beta) $$

### Finding the Nominal Pitch
By industry standard, a propeller's "nominal pitch" is measured at the **75% radius station**.
To find your QPROP propeller's nominal pitch:

1. Identify your Tip Radius ($R_{tip}$). For a 15-inch prop, $R_{tip}$ is 7.5 inches (0.1905 meters).
2. Find the 75% station: $r = 0.75 \times R_{tip}$ (e.g., 0.1428 meters).
3. Look at your QPROP `.prop` file and find the $\beta$ angle at that specific radius $r$.
4. Calculate Pitch:
   $$ Pitch = 2 \pi \times r \times \tan(\beta_{75\%}) $$
*(Note: Ensure your calculator is set to DEGREES, and remember to convert your final answer from meters to inches by dividing by 0.0254).*

---

## 2. 3D CAD Lofting Workflow (Fusion 360)

The `.prop` file contains rows of data: `Radius(m) | Chord(m) | Beta(deg)`. 
To turn this into a 3D printable blade, follow these rules:

### A. Unit Conversion
QPROP operates strictly in **Meters**. Most CAD programs operate in **Millimeters**.
- Multiply all `Radius` and `Chord` values in your `.prop` file by **1000**.
- The `Beta` value is already in **Degrees** and requires no conversion.

### B. The Golden Rule: Quarter-Chord (25%) Alignment
Do not align your airfoil sketches by their leading edge or geometric center. Aerodynamic forces and structural twisting moments act around the aerodynamic center, which is located at the **Quarter-Chord (25% back from the leading edge)**.

**Step-by-Step Lofting:**
1. **The Hub Axis:** Draw a vertical construction line originating from the center of your hub. This is your master Pitch Axis.
2. **Offset Planes:** Create a series of offset construction planes moving up the Pitch Axis. The offset distances correspond to the `Radius` column in your `.prop` file (converted to mm).
3. **Airfoil Sketches:** On each offset plane, import your 2D airfoil coordinate sketch (e.g., Clark-Y, SG6043). Scale the sketch so its length matches the `Chord` column (in mm).
4. **Alignment:** On the airfoil sketch, place a point exactly **25%** of the chord length behind the leading edge. Constrain this specific point to intersect the vertical Pitch Axis.
5. **Twist (Beta):** Rotate the entire airfoil sketch by the `Beta` angle (in degrees). Use the 25% Quarter-Chord point as the exact center of rotation.
6. **Loft:** Once all station sketches are aligned and twisted, use the CAD `Loft` command to connect the airfoils, creating a perfectly optimized, continuous 3D blade surface.
