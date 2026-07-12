import argparse
import os
import sys
import matplotlib.pyplot as plt

# Enable ANSI escape colors on Windows terminal
if os.name == 'nt':
    os.system("color")

def cmd_prop(args):
    """Generates a QMIL (.mil) template interactively."""
    print("\033[92m--- Create QMIL Propeller Template ---\033[0m")
    
    name = args.name if args.name else input("Enter propeller name (e.g., custom_prop): ").strip()
    if not name:
        print("\033[91m[-] Error: Propeller name is required.\033[0m")
        return
        
    radius = input("Tip radius in meters [Default 0.15]: ").strip() or "0.15"
    speed = input("Cruise speed in m/s [Default 15.0]: ").strip() or "15.0"
    rpm = input("Design RPM [Default 5000]: ").strip() or "5000"
    
    # Prompt for Power OR Thrust
    power = input("Target Power in Watts [Default 50.0] (Enter 0 if designing for Thrust instead): ").strip() or "50.0"
    thrust = "0.0"
    if float(power) == 0.0:
        thrust = input("Target Thrust in Newtons [Default 10.0]: ").strip() or "10.0"
        
    cl0 = input("Airfoil CL0 (0.0 for Symmetric, 0.4 for Clark Y) [Default 0.4]: ").strip() or "0.4"
    
    filename = name if name.endswith(".mil") else f"{name}.mil"
    
    template = f"""{name} QMIL Template

 2       ! Nblades

 {cl0}  6.2832    ! CL0    CL_a 
-0.8000  1.2000    ! CLmin  CLmax

 0.01000   0.008  0.006  0.40  ! CD0    CD2u   CD2l  CLCD0
 150000.0 -0.500               ! REref  REexp

  0.0  0.5  1.0   ! XIdes   
  0.6  0.5  0.4   ! CLdes   

  0.02    !  hub radius(m)
  {radius}    !  tip radius(m)
  {speed}     !  speed(m/s)    
  {rpm}  !  rpm           

  {thrust}     !  Thrust(N)   
  {power}    !  Power(W)    

 0   0.0  ! Ldes    KQdes
  30      ! Nout    
"""
    with open(filename, 'w') as f:
        f.write(template)
    print(f"\n\033[92m[+] Successfully generated geometry template: {filename}\033[0m")
    if float(power) > 0:
        print(f"    (Designed for {power} Watts of Power)")
    else:
        print(f"    (Designed for {thrust} Newtons of Thrust)")

def cmd_motor(args):
    """Generates a QPROP motor (.txt) file interactively."""
    print("\033[92m--- Create QPROP Motor File ---\033[0m")
    
    name = args.name if args.name else input("Enter motor name (e.g., Tarot_3515): ").strip()
    if not name:
        print("\033[91m[-] Error: Motor name is required.\033[0m")
        return
        
    kv = input("Motor Kv (rpm/Volt) [Default 400]: ").strip() or "400"
    io = input("No-load Current Io (Amps) [Default 0.5]: ").strip() or "0.5"
    rm = input("Motor Resistance Rmotor (Ohms) [Default 0.085]: ").strip() or "0.085"
    
    filename = name if name.endswith(".txt") else f"{name}.txt"
    
    template = f"""{name}
  {rm}  Rmotor (Ohms)
  {io}  Io     (Amps)
  {kv}  Kv     (rpm/Volt)
"""
    with open(filename, 'w') as f:
        f.write(template)
    print(f"\n\033[92m[+] Successfully generated motor file: {filename}\033[0m")

def cmd_apc(args):
    """Converts APC .PE0 data to QPROP metric .prop data."""
    input_file = args.input_pe0
    output_file = args.output_prop if args.output_prop.endswith(".prop") else f"{args.output_prop}.prop"

    if not os.path.exists(input_file):
        print(f"\033[91m[-] Error: Could not find APC file '{input_file}'\033[0m")
        sys.exit(1)
        
    prop_name = os.path.basename(output_file)
    header = f"""{prop_name} (Metric Converted from APC)

 2         ! Nblades

 0.65  6.25  ! CL0     CL_a
 -0.5  1.6   ! CLmin   CLmax

 0.013  0.050  0.015 0.85  !  CD0    CD2u   CD2l   CLCD0 
 175000  -0.4              !  REref  REexp

 1.0     1.0      1.0  !  Rfac   Cfac   Bfac
 0.0     0.0      0.0  !  Radd   Cadd   Badd  

#  r(meters)  chord(meters)  beta(deg)
"""
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()

        data_lines = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 14:
                try:
                    station_in = float(parts[0])
                    chord_in = float(parts[1])
                    twist = float(parts[8])
                    
                    if station_in >= 1.0:
                        data_lines.append(f" {station_in * 0.0254:8.5f}  {chord_in * 0.0254:8.5f}  {twist:8.5f}\n")
                except ValueError:
                    pass

        with open(output_file, 'w') as f:
            f.write(header)
            f.writelines(data_lines)

        print(f"\033[92m[+] Successfully converted APC file and saved to: {output_file}\033[0m")
    except Exception as e:
        print(f"\033[91m[-] Error during conversion: {e}\033[0m")

def cmd_graph(args):
    """Parses a QPROP text output file and graphs the requested variables."""
    if not os.path.exists(args.file):
        print(f"\033[91m[-] Error: Output file '{args.file}' not found.\033[0m")
        sys.exit(1)
        
    # Read and parse the file
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeError:
        try:
            with open(args.file, 'r', encoding='utf-16le') as f:
                lines = f.readlines()
        except UnicodeError:
            with open(args.file, 'r') as f:
                lines = f.readlines()
        
    headers = []
    data_matrix = []
    header_lines = []
    
    qprop_version = "QPROP Version Unknown"
    prop_name = "Unknown Propeller"
    motor_name = "Unknown Motor"
    
    for line in lines:
        line_strip = line.strip()
        
        if line_strip.startswith("#"):
            header_lines.append(line_strip.replace("#", "").strip())
            
        # Find the header row
        if "V(m/s)" in line_strip and "rpm" in line_strip:
            clean_line = line_strip.replace("#", "").strip()
            headers = clean_line.split()
            continue
            
        # Parse data rows (ignore comments and empty lines)
        if headers and line_strip and not line_strip.startswith("#"):
            try:
                row_data = [float(val) for val in line_strip.split()]
                if len(row_data) >= len(headers):
                    data_matrix.append(row_data)
            except ValueError:
                pass # Non-numeric row, skip

    # Assign metadata based on QPROP standard header structure
    if len(header_lines) > 2:
        qprop_version = header_lines[0] if header_lines[0] else qprop_version
        prop_name = header_lines[2] if len(header_lines) > 2 and header_lines[2] else prop_name
        motor_name = header_lines[4] if len(header_lines) > 4 and header_lines[4] else motor_name

    if not data_matrix:
        print("\033[91m[-] Error: Could not find valid QPROP data table in the file.\033[0m")
        sys.exit(1)
        
    # Find column indices
    try:
        x_idx = headers.index(args.x_var)
    except ValueError:
        print(f"\033[91m[-] Error: X variable '{args.x_var}' not found in headers.\033[0m")
        print(f"    Available headers: {', '.join(headers)}")
        sys.exit(1)
        
    y_indices = []
    for y_var in args.y_vars:
        try:
            y_indices.append((y_var, headers.index(y_var)))
        except ValueError:
            print(f"\033[93m[-] Warning: Y variable '{y_var}' not found. Skipping.\033[0m")
            
    if not y_indices:
        print("\033[91m[-] Error: No valid Y variables provided to plot.\033[0m")
        sys.exit(1)
        
    # Extract columns
    x_data = [row[x_idx] for row in data_matrix]
    
    # Plotting - Strict AVL / X11 Dark Aesthetic
    plt.style.use('dark_background')
    plt.rcParams['font.family'] = 'monospace'
    plt.rcParams['axes.linewidth'] = 1.0
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['xtick.top'] = True
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.color'] = 'white'
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['grid.linewidth'] = 0.5
    plt.rcParams['grid.alpha'] = 0.3
    
    fig, ax1 = plt.subplots(figsize=(10, 7), facecolor='black')
    ax1.set_facecolor('black')
    
    # Plot first Y variable on primary axis
    color1 = 'lime'
    name1, idx1 = y_indices[0]
    y1_data = [row[idx1] for row in data_matrix]
    
    ax1.set_xlabel(args.x_var, fontweight='normal', fontsize=11, color='white')
    ax1.set_ylabel(name1, color=color1, fontweight='normal', fontsize=11)
    line1, = ax1.plot(x_data, y1_data, color=color1, marker='', linewidth=1.5, label=name1)
    ax1.tick_params(axis='y', labelcolor=color1, colors='white')
    ax1.tick_params(axis='x', colors='white')
    
    lines = [line1]
    
    # Plot subsequent Y variables on secondary axes (if provided)
    if len(y_indices) > 1:
        colors = ['red', 'dodgerblue', 'yellow', 'magenta']
        for i, (name, idx) in enumerate(y_indices[1:]):
            ax2 = ax1.twinx()
            
            # Offset the spine for multiple secondary axes
            if i > 0:
                ax2.spines['right'].set_position(('outward', 50 * i))
                
            y_data = [row[idx] for row in data_matrix]
            color = colors[i % len(colors)]
            
            ax2.set_ylabel(name, color=color, fontweight='normal', fontsize=11)
            line, = ax2.plot(x_data, y_data, color=color, marker='', linewidth=1.5, label=name)
            ax2.tick_params(axis='y', labelcolor=color, direction='in')
            # Hide the grid for secondary axes so they don't overlap messy lines
            ax2.grid(False)
            lines.append(line)

    # Add Metadata Text in three distinct colors (AVL Style)
    ax1.text(0.02, 0.97, qprop_version, transform=ax1.transAxes, color='lime', fontsize=10, verticalalignment='top')
    ax1.text(0.02, 0.93, f"Prop : {prop_name}", transform=ax1.transAxes, color='red', fontsize=10, verticalalignment='top')
    ax1.text(0.02, 0.89, f"Motor: {motor_name}", transform=ax1.transAxes, color='dodgerblue', fontsize=10, verticalalignment='top')

    plt.title(f"{prop_name} Analysis", fontweight='normal', fontsize=12, color='white', loc='left')
    
    # AVL-style borderless legend with colored text matching the lines
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper right', bbox_to_anchor=(1.0, 1.05), frameon=False, labelcolor='linecolor')
    
    fig.subplots_adjust(top=0.9, right=0.85)
    
    print("\033[92m[+] Launching external graph window...\033[0m")
    plt.show()

def main():
    C_GREEN = '\033[92m'
    C_BLUE = '\033[94m'
    C_RED = '\033[91m'
    C_RESET = '\033[0m'
    C_BOLD = '\033[1m'

    help_epilog = f"""
{C_BOLD}{C_GREEN}============================================================{C_RESET}
{C_BOLD}{C_RED}  qtool / QPROP WORKFLOW COMMANDS{C_RESET}
{C_BOLD}{C_GREEN}============================================================{C_RESET}
{C_BLUE}1. Create Geometry & Motor Templates:{C_RESET}
   > qtool prop
   > qtool motor

{C_BLUE}2. Generate Propeller Geometry (Native QMIL):{C_RESET}
   > qmil myprop.mil myprop.prop

{C_BLUE}3. Analyze Propeller & Motor (Native QPROP):{C_RESET}
   > qprop myprop.prop motor.txt 0,30,1 0 22.2 > output.txt

{C_BLUE}4. Generate AVL-Style Performance Graphs:{C_RESET}
   > qtool graph output.txt "V(m/s)" "T(N)" "eff" "Pshaft(W)"

{C_BLUE}5. Convert APC Wind Tunnel Data:{C_RESET}
   > qtool apc 15x8E-PERF.PE0 15x8_metric.prop

{C_BOLD}{C_GREEN}============================================================{C_RESET}
{C_BOLD}{C_RED}  QPROP SYNTAX{C_RESET}
{C_BOLD}{C_GREEN}============================================================{C_RESET}
{C_BLUE}A. Full System (Prop + Motor) - Solve for RPM:{C_RESET}
   > qprop myprop.prop motor.txt 15 0 22.2
   (Speed=15, RPM=0, Volts=22.2)

{C_BLUE}B. Full System - Solve for Voltage:{C_RESET}
   > qprop myprop.prop motor.txt 15 5000 0
   (Speed=15, RPM=5000, Volts=0)

{C_BLUE}C. Windmill Mode (Regenerative braking):{C_RESET}
   > qprop myprop.prop motor.txt 15 0 -22.2
   (Speed=15, RPM=0, Volts=-22.2)

{C_BLUE}D. Propeller Only (No Motor) - Solve for Thrust/Power:{C_RESET}
   > qprop myprop.prop 15 5000
   (Speed=15, RPM=5000)

{C_BLUE}E. Parameter Sweep (Graphing Mode):{C_RESET}
   > qprop myprop.prop motor.txt 0,30,1 0 22.2
   (Sweeps Speed from 0 to 30 m/s in steps of 1)
{C_BOLD}{C_GREEN}============================================================{C_RESET}
"""

    parser = argparse.ArgumentParser(
        description=f"{C_BOLD}{C_RED}qtool: The Terminal Command Line tool for QPROP/QMIL.{C_RESET}",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=help_epilog
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Subparser for 'prop'
    parser_temp = subparsers.add_parser("prop", help="Interactively generate a QMIL .mil propeller geometry template")
    parser_temp.add_argument("name", type=str, nargs='?', default=None, help="Optional: Name of the propeller")

    # Subparser for 'motor'
    parser_motor = subparsers.add_parser("motor", help="Interactively generate a QPROP motor .txt file")
    parser_motor.add_argument("name", type=str, nargs='?', default=None, help="Optional: Name of the motor")
    
    # Subparser for 'apc'
    parser_apc = subparsers.add_parser("apc", help="Convert APC .PE0 data to QPROP metric .prop format")
    parser_apc.add_argument("input_pe0", type=str, help="Path to the input APC .PE0 file")
    parser_apc.add_argument("output_prop", type=str, help="Name of the output .prop file")
    
    # Subparser for 'graph'
    parser_graph = subparsers.add_parser("graph", help="Parse QPROP output and generate external plots")
    parser_graph.add_argument("file", type=str, help="The text file containing raw QPROP terminal output")
    parser_graph.add_argument("x_var", type=str, help="The exact header name for the X-axis (e.g. 'V(m/s)')")
    parser_graph.add_argument("y_vars", type=str, nargs='+', help="One or more header names for the Y-axis (e.g. 'T(N)' 'eff')")

    args = parser.parse_args()
    
    if args.command == "prop":
        cmd_prop(args)
    elif args.command == "motor":
        cmd_motor(args)
    elif args.command == "apc":
        cmd_apc(args)
    elif args.command == "graph":
        cmd_graph(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
