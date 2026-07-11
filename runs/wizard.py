import os
import subprocess

QPROP_DIR = r"c:\Users\KARSHAK_Tamal\Downloads\qprop1.22 (1)\Qprop\runs"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("==================================================")
    print("         QPROP / QMIL TERMINAL WIZARD             ")
    print("==================================================")

def create_qmil_template():
    print("\n--- Create QMIL Design Template ---")
    name = input("Enter propeller name (e.g., custom_prop): ").strip()
    if not name:
        return
        
    radius = input("Tip radius in meters [Default 0.15]: ").strip() or "0.15"
    speed = input("Cruise speed in m/s [Default 15.0]: ").strip() or "15.0"
    rpm = input("Design RPM [Default 5000]: ").strip() or "5000"
    power = input("Target Power in Watts [Default 50.0]: ").strip() or "50.0"
    cl0 = input("Airfoil CL0 (0.0 for Symmetric, 0.4 for Clark Y) [Default 0.4]: ").strip() or "0.4"
    
    filename = f"{name}.mil"
    filepath = os.path.join(QPROP_DIR, filename)
    
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

  0.0     !  Thrust(N)   
  {power}    !  Power(W)    

 0   0.0  ! Ldes    KQdes
  30      ! Nout    
"""
    with open(filepath, 'w') as f:
        f.write(template)
    print(f"\n[SUCCESS] Created {filename}! You can now open it to manually edit advanced values, or run it.")
    input("Press Enter to continue...")

def create_motor_template():
    print("\n--- Create Motor Template ---")
    name = input("Enter motor name (e.g., Tarot_3515): ").strip()
    if not name:
        return
        
    r_motor = input("Internal Resistance (Ohms) [Default 0.085]: ").strip() or "0.085"
    i_idle = input("Idle Current (Amps) [Default 0.5]: ").strip() or "0.5"
    kv = input("KV Rating (rpm/Volt) [Default 400]: ").strip() or "400"
    
    filename = f"{name}.txt"
    filepath = os.path.join(QPROP_DIR, filename)
    
    template = f"""{name}

 1     ! motor type (brushless DC)

 {r_motor}     ! Rmotor (Ohms)
 {i_idle}       ! Io     (Amps)
 {kv}      ! Kv     (rpm/Volt)
"""
    with open(filepath, 'w') as f:
        f.write(template)
    print(f"\n[SUCCESS] Created {filename}!")
    input("Press Enter to continue...")

def run_qmil():
    print("\n--- Run QMIL (Design Propeller) ---")
    files = [f for f in os.listdir(QPROP_DIR) if f.endswith('.mil')]
    if not files:
        print("No .mil files found! Create a template first.")
        input("Press Enter to continue...")
        return
        
    print("Available Templates:")
    for i, f in enumerate(files):
        print(f"[{i}] {f}")
        
    choice = input("Select template number: ").strip()
    try:
        selected_file = files[int(choice)]
        out_file = selected_file.replace('.mil', '.prop')
        print(f"\nRunning: qmil.exe {selected_file} {out_file}")
        
        qmil_exe = os.path.join(QPROP_DIR, "qmil.exe")
        subprocess.run([qmil_exe, selected_file, out_file], cwd=QPROP_DIR)
        
        print(f"\n[SUCCESS] Geometry saved to {out_file}")
    except (ValueError, IndexError):
        print("Invalid selection.")
    input("Press Enter to continue...")

def run_qprop():
    print("\n--- Run QPROP (Analyze Performance) ---")
    
    props = [f for f in os.listdir(QPROP_DIR) if f.endswith('.prop')]
    motors = [f for f in os.listdir(QPROP_DIR) if f.endswith('.txt')]
    
    print("\nAvailable Propellers:")
    for i, f in enumerate(props):
        print(f"[{i}] {f}")
    prop_choice = int(input("Select propeller number: ").strip())
    
    print("\nAvailable Motors:")
    for i, f in enumerate(motors):
        print(f"[{i}] {f}")
    motor_choice = int(input("Select motor number: ").strip())
    
    speed = input("Airspeed sweep (e.g., 0,30,1) [Default 0,30,1]: ").strip() or "0,30,1"
    voltage = input("Battery Voltage (e.g., 22.2): ").strip() or "22.2"
    
    prop_file = props[prop_choice]
    motor_file = motors[motor_choice]
    
    print(f"\nRunning: qprop.exe {prop_file} '{motor_file}' {speed} 0 {voltage}")
    
    qprop_exe = os.path.join(QPROP_DIR, "qprop.exe")
    subprocess.run([qprop_exe, prop_file, motor_file, speed, "0", voltage], cwd=QPROP_DIR)
    
    input("\nPress Enter to return to menu...")

def main():
    while True:
        clear_screen()
        print_header()
        print("[1] Create new QMIL (.mil) Template")
        print("[2] Create new Motor (.txt) Template")
        print("[3] Run QMIL (Generate Propeller Geometry)")
        print("[4] Run QPROP (Analyze Propeller & Motor)")
        print("[5] Exit")
        print("==================================================")
        
        choice = input("Select an option: ").strip()
        
        if choice == '1':
            create_qmil_template()
        elif choice == '2':
            create_motor_template()
        elif choice == '3':
            run_qmil()
        elif choice == '4':
            run_qprop()
        elif choice == '5':
            break

if __name__ == "__main__":
    main()
