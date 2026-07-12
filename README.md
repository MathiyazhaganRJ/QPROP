# qtool: The Native QPROP/QMIL Assistant

qtool is a native command-line utility built to streamline Mark Drela's original QPROP and QMIL physics engines. It adds interactive template generation, APC wind-tunnel data conversion, and AVL-style graphical plotting—all without breaking the native terminal workflow.

## Installation

Ensure you have Python 3 installed. Navigate to the Qprop root folder and install the required dependencies:

```bash
pip install -r requirements.txt
```
*(Note: `matplotlib` is the only external library required for graphing).*

## Directory Structure
- `/runs/qtool.py` - The core Python script.
- `/runs/qtool.bat` - The Windows batch wrapper (allows you to just type `qtool`).
- `/runs/qprop.exe` & `qmil.exe` - The original MIT Fortran binaries.

---

## 1. Create Geometry & Motor Templates
Instead of copying files manually, use the interactive wizard to generate fresh `.mil` (propeller) and `.motor` (motor) templates.

```bash
qtool prop
qtool motor
```
- **`qtool prop`**: Will interactively prompt you for Tip Radius, Speed, RPM, and your choice of Target Thrust or Target Power.
- **`qtool motor`**: Will prompt you for Kv, No-load Current (Io), and Motor Resistance (Rmotor).
- The resulting `.mil` and `.motor` files will be saved directly in your current directory.

## 2. Generate Propeller Geometry
Once you have your `.mil` file, run Mark Drela's native `qmil.exe` to iteratively solve the nonlinear geometry and output the final `.prop` design file.

```bash
qmil myprop.mil myprop.prop
```

## 3. Analyze the Full System
To test your new propeller attached to a specific motor, use the native `qprop.exe`. 
**CRITICAL:** You must use the `>` operator to save the terminal output into a text file so `qtool` can graph it later.

```bash
# Syntax: qprop [prop_file] [motor_file] [Speed] [RPM] [Voltage]
qprop myprop.prop motor.motor 0,30,1 0 22.2 > output.txt
```
*(In this example, we sweep Airspeed from 0 to 30 m/s in steps of 1, solve for RPM `0`, and fix the Voltage at `22.2`)*

## 4. Generate AVL-Style Graphs
Feed the raw Qprop text file back into `qtool` to generate beautiful, classic X11/AVL-style scientific graphs.

```bash
# Syntax: qtool graph [text_file] [X-Axis] [Y-Axis 1] [Y-Axis 2] ...
qtool graph output.txt "V(m/s)" "T(N)" "eff" "Pshaft(W)"
```
- The graph uses a pitch-black background, pure phosphor colors (Lime, Red, Blue), and mono-spaced fonts exactly matching classic aerospace tools.
- It will automatically extract your Propeller and Motor name and stamp it in the corner of the plot.
- **Note:** The exact header variables (e.g. `V(m/s)`) must exactly match the column headers in the QPROP text file.

## 5. Convert APC Wind Tunnel Data
If you have downloaded `.PE0` wind tunnel data files from APC, you can instantly convert them into QPROP's metric `.prop` format.

```bash
# Syntax: qtool apc [input.PE0] [output.prop]
qtool apc 15x8E-PERF.PE0 15x8_metric.prop
```

---

## The QPROP Physics Cheatsheet

Depending on which variables you lock with `0`, Qprop will perform entirely different physics analyses:

| Analysis Type | Command Syntax | Description |
| :--- | :--- | :--- |
| **Solve for RPM** | `qprop prop.prop motor.motor 15 0 22` | Given 15m/s and 22V, what is the RPM and Thrust? |
| **Solve for Volts** | `qprop prop.prop motor.motor 15 5000 0` | Given 15m/s and 5000 RPM, how many Volts are required? |
| **Windmill Mode** | `qprop prop.prop motor.motor 15 0 -22` | (Negative Volts). Calculates regenerative braking. |
| **Propeller Only** | `qprop prop.prop 15 5000` | Ignores the motor entirely. Pure aerodynamic forces. |
| **Parameter Sweep**| `qprop prop.prop motor.motor 0,30,1 0 22` | Sweeps the speed from 0 to 30 m/s to generate a graph curve. |
