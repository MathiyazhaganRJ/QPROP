# BLDC Motor Simulation and Real-World Correction

The QPROP engine calculates motor efficiency using a highly accurate DC electric model based on three primary parameters defined in your `.motor` template:
1. **`Kv` (RPM/Volt):** Defines the back-EMF and torque constant.
2. **`Io` (Amps):** The no-load current, accounting for internal magnetic iron losses and bearing friction.
3. **`Rmotor` (Ohms):** The internal winding resistance, accounting for copper heating losses ($I^2R$).

## Reading Motor Efficiency in QPROP

When you execute a full-system QPROP simulation (e.g., `qprop myprop.prop mymotor.motor 15 0 22`), the output table provides three distinct efficiency columns:
*   **`effmot`:** The electrical motor efficiency (Mechanical Power Output / Electrical Power Input).
*   **`effprop`:** The aerodynamic propeller efficiency (Thrust Power / Mechanical Power Input).
*   **`eff`:** Total System Efficiency (`effmot` × `effprop`).

To visualize the motor's peak efficiency curve, you can plot it directly:
```bash
qtool graph output.txt "Amps" "effmot"
```

## Real-World Corrections (Closing the Gap)

While QPROP's internal model is mathematically rigorous, it calculates the physics of the *copper coils in a vacuum*. To make the simulation perfectly match real-world drone flight telemetry, you must account for two physical realities:

### 1. ESC Switching Losses
QPROP's `effmot` does not account for the Electronic Speed Controller (ESC). In real-world operation, an ESC wastes approximately 5% to 10% of the battery energy simply through transistor switching losses (MOSFET heat) and phase alignment timing.
*   **Correction:** To get true battery-to-shaft efficiency, multiply the QPROP `effmot` output by **~0.95**. Alternatively, you can mathematically add the ESC's internal resistance to your `Rmotor` value.

### 2. Thermal Degradation (Hot Copper)
Manufacturers typically measure `Rmotor` (Internal Resistance) in a laboratory when the motor is cold (20°C). During flight, the motor coils heat up significantly. As copper temperature increases, its electrical resistance increases, which actively lowers the motor's efficiency during prolonged flight.
*   **Correction:** For a conservative, "worst-case scenario" flight model, artificially increase the `Rmotor` value in your `.motor` file by **10% to 15%** above the manufacturer's datasheet value.

By applying these two corrections, your digital twin will closely mimic physical flight telemetry.
