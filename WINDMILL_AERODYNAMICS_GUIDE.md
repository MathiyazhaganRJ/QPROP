# Propeller & Windmill Aerodynamics Guide

This document standardizes the aerodynamic physics, vector mechanics, and QPROP simulation interpretations for windmilling propellers, wind turbines, and regenerative braking.

---

## 1. The Mirror Image: Propellers vs. Windmills

While both use aerodynamic airfoils to interact with the air, their orientations relative to the free-stream wind are exact mirror images.

### The Airplane Propeller
*   **Orientation:** The **curved top** (suction side) faces forward into the wind. The flat bottom (pressure side) faces backward toward the pilot.
*   **Aerodynamics:** The motor spins the blade, generating aerodynamic Lift that points forward. **Lift = Forward Thrust.**

### The Wind Turbine
*   **Orientation:** The **flat bottom** (pressure side) faces forward into the wind. The curved top faces downwind.
*   **Aerodynamics:** The wind crashes into the flat bottom. The vacuum on the curved back pulls the blade sideways. **Lift = Rotational Torque.**

> [!WARNING]
> **The Reverse Flip Fallacy:** You cannot simply unbolt an airplane propeller and mount it backward to create an efficient wind turbine. If you flip a propeller, the Trailing Edge becomes the "high side," forcing the blade to spin backward (blunt Trailing Edge first). Real wind turbines are manufactured with a **Reverse Twist** (a left-handed screw) so the wind hits the flat bottom but still pushes the Leading Edge forward.

---

## 2. The "High Side" Rule (Static Starting Torque)

When a propeller or windmill is completely static (0 RPM) and hit by incoming wind, it is completely aerodynamically stalled. Lift drops to near zero, and Drag takes over. 

To determine which way any angled blade will rotate from a dead stop, use the **High Side Rule**:
*   Because the blade acts like a ramp, the wind hits it and deflects toward the "low" side.
*   Newton's Third Law forces the blade in the opposite direction.
*   **Conclusion:** The physical force will always push the blade toward the **"high" side** (the edge that is physically sticking out closer to the incoming wind). 

---

## 3. Pshaft vs. Thrust (Understanding QPROP Output)

When analyzing flight telemetry or QPROP output, it is critical to separate rotational twisting force from axial pushing force. 

### Pshaft (Shaft Power) = "Who is spinning whom?"
*   **Positive (+):** The **Motor** is burning electricity to twist the shaft and force the propeller to spin. 
*   **Negative (-):** The **Air** is acting as a windmill, twisting the shaft and forcing the dead motor to spin. (Mechanical power is being extracted from the wind).

### T (Thrust) = "Who is pushing whom?"
*   **Positive (+):** The propeller is pushing the airplane **FORWARD**. 
*   **Negative (-):** The propeller is acting as an air-brake, pushing the airplane **BACKWARD** (Aerodynamic Drag).

---

## 4. The 3 Zones of Windmilling Drag

Classical aerospace theory states that a windmilling propeller causes vastly more drag than a locked propeller. This is true for real airplanes, but the full physical picture is divided into three zones:

### Zone 1: The Locked Rotor (0 RPM)
If the ESC applies a hard brake and locks the propeller horizontally, it acts as a completely stalled flat plate. 
*   **Pshaft:** 0 Watts
*   **Drag:** High (Just the frontal area of the two blades).

### Zone 2: Loaded Windmilling (Dead Engine / Generator)
The wind forces the prop to spin, but it is physically attached to the heavy friction of dead engine pistons or a heavy electrical generator. The propeller extracts maximum mechanical power from the air to fight this friction. 
*   **Pshaft:** Highly Negative (Extracting max power).
*   **Drag:** **MAXIMUM.** Because it is extracting massive energy while spinning, it acts like a solid parachute disk. It produces vastly more drag than a locked rotor.

### Zone 3: The 0 Pshaft Region (Perfect Free-Wheeling)
If the propeller is disconnected from the motor and placed on a perfect frictionless bearing, it requires zero power to spin. It spins incredibly fast, the blades slice perfectly into the relative wind, and it perfectly "gets out of the way" of the air. 
*   **Pshaft:** Exactly 0.0 Watts.
*   **Drag:** **MINIMUM.** The drag drops significantly below both Zone 1 and Zone 2. 

---

## 5. Simulating Regenerative Braking in QPROP

To find the absolute maximum regenerative electrical power your drone can harvest in a glide (or dive), you must find the "sweet spot" RPM that extracts the most energy. 

**The Sweep Method:**
Run a manual sweep of fixed RPMs in your terminal (dropping the Volts argument entirely). 
Example for a 10 m/s dive:
```bash
1500, 2000, 2500, 3000, 3500 | ForEach-Object { .\qprop Generic.prop "Tmotor 3520.motor" 10 10 1 $_ | Select-String "10.000" }
```

**How to Read the Results:**
1.  **Find the Sweet Spot:** Look down the `Pelec` (Electrical Power) column. The largest **NEGATIVE** number is your maximum charging rate in Watts. The RPM for that row is the speed your ESC must hold to harvest that power.
2.  **Find the Drag Penalty:** Look at the `T(N)` column for that exact row. This negative number is the massive aerodynamic drag penalty your airframe is paying to harvest that electricity. 
3.  **Find Free-Wheeling:** Keep increasing the RPM in your sweep until `Pshaft(W)` crosses exactly to `0.0`. That is your propeller's true, frictionless free-wheeling speed for that wind condition.
