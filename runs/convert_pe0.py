import os

pe0_path = r"C:\Users\KARSHAK_Tamal\Downloads\PE0-FILES_WEB-202602\PE0-FILES_WEB\15x8E-PERF.PE0"
prop_path = r"C:\Users\KARSHAK_Tamal\Downloads\qprop1.22 (1)\Qprop\runs\15x8e.prop"

header = """APC 15x8E

 2         ! Nblades

 0.65  6.25  ! CL0     CL_a
 -0.5  1.6   ! CLmin   CLmax

 0.013  0.050  0.015 0.85  !  CD0    CD2u   CD2l   CLCD0 
 175000  -0.4              !  REref  REexp

 0.0254  0.0254   1.0  !  Rfac   Cfac   Bfac  (0.0254 converts inches to meters)
 0.0     0.0      0.0  !  Radd   Cadd   Badd  

#  r(in)  chord(in)  beta(deg)
"""

with open(pe0_path, 'r') as f:
    lines = f.readlines()

data_lines = []
for line in lines:
    parts = line.split()
    if len(parts) >= 14:
        try:
            station = float(parts[0])
            chord = float(parts[1])
            twist = float(parts[8])
            # Only include the aerodynamic portion of the blade (skip the plastic center hub)
            if station >= 1.0:
                data_lines.append(f" {station:7.4f}  {chord:7.4f}  {twist:7.4f}\n")
        except ValueError:
            pass

with open(prop_path, 'w') as f:
    f.write(header)
    f.writelines(data_lines)

print(f"Successfully converted {pe0_path} to {prop_path}")
