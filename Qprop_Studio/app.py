import os
import subprocess
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
QPROP_DIR = r"c:\Users\KARSHAK_Tamal\Downloads\qprop1.22 (1)\Qprop\runs"

@app.route('/')
def index():
    # Find all motor text files to populate the dropdown
    motors = [f for f in os.listdir(QPROP_DIR) if f.endswith('.txt')]
    return render_template('index.html', motors=motors)

@app.route('/design', methods=['POST'])
def design_prop():
    data = request.json
    
    radius = data.get('radius', 0.15)
    speed = data.get('speed', 5.0)
    rpm = data.get('rpm', 3000.0)
    power = data.get('power', 50.0)
    cl0 = data.get('cl0', 0.4)

    mil_content = f"""Web Generated Prop

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
    
    mil_path = os.path.join(QPROP_DIR, "web_design.mil")
    prop_path = os.path.join(QPROP_DIR, "web_design.prop")
    
    with open(mil_path, 'w') as f:
        f.write(mil_content)
        
    try:
        qmil_exe = os.path.join(QPROP_DIR, "qmil.exe")
        result = subprocess.run([qmil_exe, "web_design.mil", "web_design.prop"], cwd=QPROP_DIR, capture_output=True, text=True, check=True)
        with open(prop_path, 'r') as f:
            prop_data = f.read()
            
        return jsonify({'status': 'success', 'log': result.stdout, 'prop_data': prop_data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/analyze', methods=['POST'])
def analyze_prop():
    data = request.json
    motor_file = data.get('motor', 'Tarot 3515.txt')
    voltage = data.get('voltage', 22.2)
    max_speed = data.get('max_speed', 30)
    
    prop_path = "web_design.prop"
    if not os.path.exists(os.path.join(QPROP_DIR, prop_path)):
        return jsonify({'status': 'error', 'message': 'Please generate a propeller first!'})
        
    try:
        qprop_exe = os.path.join(QPROP_DIR, "qprop.exe")
        cmd = [qprop_exe, prop_path, motor_file, f"0,{max_speed},1", "0", str(voltage)]
        result = subprocess.run(cmd, cwd=QPROP_DIR, capture_output=True, text=True)
        
        # Parse the Qprop Output Table
        parsed_data = []
        parsing = False
        for line in result.stdout.split('\n'):
            if "V(m/s)" in line:
                parsing = True
                continue
            if parsing and line.strip() and not line.startswith('#') and not "radius" in line:
                parts = line.split()
                if len(parts) >= 16:
                    parsed_data.append({
                        'v': float(parts[0]),
                        'thrust': float(parts[3]),
                        'pelec': float(parts[15]),
                        'eff': float(parts[14])
                    })
                    
        return jsonify({'status': 'success', 'data': parsed_data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
