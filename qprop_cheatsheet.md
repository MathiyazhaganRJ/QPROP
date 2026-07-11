# QPROP Command Line Cheatsheet

QPROP requires you to define the state of the physics environment. Depending on whether you include a motor file, and which variables you lock with `0`, you can execute several different types of analysis. 

The standard syntax is:
`qprop.exe [prop_file] [motor_file] [Speed] [RPM] [Voltage]`

---

## 1. Full System Analysis (Propeller + Motor)
These are the most common commands used to test your drone's full powertrain.

### A. Lock Speed & Voltage (Solve for RPM)
**Command:** `qprop.exe myprop.prop mymotor.txt 15 0 22.2`
* **Inputs:** Airspeed = 15 m/s, RPM = Floats (`0`), Battery = 22.2V.
* **Outputs:** Calculates the exact RPM the motor will settle at, how much Thrust it generates, and how many Amps it pulls. 
* **Use Case:** Testing performance at a specific throttle position (Voltage) and flight speed.

### B. Lock Speed & RPM (Solve for Voltage)
**Command:** `qprop.exe myprop.prop mymotor.txt 15 5000 0`
* **Inputs:** Airspeed = 15 m/s, RPM = 5000, Battery = Floats (`0`).
* **Outputs:** Calculates how many Volts (Throttle %) are required to force the motor to exactly 5000 RPM under that aerodynamic load.
* **Use Case:** Validating real-world flight logs where you know the RPM and Speed, but want to calculate the electrical power consumed.

---

## 2. 1D Parameter Sweeps (Generating Curves)
Instead of a single number, you can replace *one* variable with a range `min,max,step` to generate a data curve for graphing.

### C. Airspeed Sweep (Find Top Speed / Pitch Speed)
**Command:** `qprop.exe myprop.prop mymotor.txt 0,30,1 0 22.2`
* **Inputs:** Airspeed = Sweeps 0 to 30 m/s, RPM = Floats, Battery = 22.2V.
* **Outputs:** A table showing Thrust dropping off as speed increases.
* **Use Case:** Finding static thrust (at 0 m/s), top speed (when Thrust = Drag), and Pitch Speed (when Thrust = 0).

### D. Voltage Sweep (Find Cruise Throttle)
**Command:** `qprop.exe myprop.prop mymotor.txt 15 0 10,22,1`
* **Inputs:** Airspeed = 15 m/s, RPM = Floats, Voltage = Sweeps 10V to 22V.
* **Outputs:** A table showing how Thrust and Amps increase as you push the throttle stick forward.
* **Use Case:** Finding the exact throttle position required to generate your required cruise thrust.

### E. RPM Sweep (Testing RPM Governors)
**Command:** `qprop.exe myprop.prop mymotor.txt 15 3000,8000,500 0`
* **Inputs:** Airspeed = 15 m/s, RPM = Sweeps 3000 to 8000, Voltage = Floats.
* **Outputs:** Calculates the voltage required to hit every RPM step.
* **Use Case:** Mostly used for helicopter rotors or variable-pitch propellers running on RPM governors.

---

## 3. Propeller-Only Analysis (No Motor)
If you want to test the pure aerodynamics of a propeller without electrical motor math (e.g., a wind-tunnel test or a free-spinning windmilling prop), you simply omit the motor file!

### F. Lock Speed & RPM (Solve for Mechanical Torque)
**Command:** `qprop.exe myprop.prop 15 5000` *(Notice there is no 0 or Voltage at the end)*
* **Inputs:** Airspeed = 15 m/s, RPM = 5000.
* **Outputs:** Calculates the Thrust (Newtons) and Mechanical Torque (N-m) of the blade. It outputs **no** electrical data (No Volts, No Amps, No Pelec).
* **Use Case:** Wind tunnel testing, or calculating the drag of a dead, free-spinning propeller on a glider.

---

## 4. Multi-Dimensional Sweeps (Performance Maps)
If you need to test every possible combination of Speed, RPM, and Voltage simultaneously, you use a parameter file.

### G. The Matrix Sweep
**Command:** `qprop.exe myprop.prop mymotor.txt param2`
* **Inputs:** You provide a text file (like `param2`) containing nested ranges for Speed, RPM, and Voltage.
* **Outputs:** A massive database table of every possible flight state.
* **Use Case:** Generating aerodynamic look-up tables to feed into JSBSim, ArduPilot SITL, or X-Plane flight simulators.
