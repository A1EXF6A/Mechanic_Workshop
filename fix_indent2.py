import re

with open('/home/joelpp/Mechanic_Workshop/addons/taller_mecanico_portal/controllers/main.py', 'r') as f:
    lines = f.readlines()

in_func = False
for i, line in enumerate(lines):
    if line.startswith('    def taller_orden_linea_extra_update'):
        in_func = True
        continue
    
    if in_func:
        if line.startswith('    @http.route') or line.startswith('    def '):
            break
            
        if i >= 855 and i <= 873:
            if line.startswith('        '):
                lines[i] = '    ' + line
            elif line.startswith('    '):
                lines[i] = '    ' + line
            elif line.strip() == '':
                pass
            else:
                lines[i] = '    ' + line

with open('/home/joelpp/Mechanic_Workshop/addons/taller_mecanico_portal/controllers/main.py', 'w') as f:
    f.writelines(lines)
