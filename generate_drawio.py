import xml.etree.ElementTree as ET

def create_mxgraph():
    return ET.Element("mxGraphModel", dx="1000", dy="800", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="1200", pageHeight="800", math="0", shadow="0", background="#1e1e1e")

def add_root(graph):
    root = ET.SubElement(graph, "root")
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")
    return root

def add_cell(root, id, value, style, x, y, width, height, parent="1"):
    cell = ET.SubElement(root, "mxCell", id=id, value=value, style=style, vertex="1", parent=parent)
    ET.SubElement(cell, "mxGeometry", x=str(x), y=str(y), width=str(width), height=str(height), **{"as": "geometry"})
    return cell

def add_edge(root, id, source, target, style="endArrow=classic;html=1;fontColor=#ffffff;strokeColor=#ffffff;", parent="1"):
    cell = ET.SubElement(root, "mxCell", id=id, style=style, edge="1", parent=parent, source=source, target=target)
    ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})
    return cell

def build_modulos_rol(diagram):
    root = add_root(diagram)
    roles = ["Admin RRHH", "Empleado", "Contador", "Gerente", "Admin Sistema"]
    modulos = ["Gestión Empleados", "Control Asistencia", "Portal Personal", "Liquidación Nómina", "Dashboard y Reportes", "Configuración"]
    
    for i, rol in enumerate(roles):
        add_cell(root, f"r_{i}", rol, "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;fillColor=#1a1a1a;strokeColor=#ffffff;fontColor=#ffffff;", 100, 100 + i*120, 40, 80)
        
    for i, mod in enumerate(modulos):
        add_cell(root, f"m_{i}", mod, "rounded=1;whiteSpace=wrap;html=1;fillColor=#185FA5;strokeColor=#ffffff;fontColor=#ffffff;", 500, 100 + i*100, 150, 60)
        
    # Links
    links = {
        0: [0, 1, 3, 4, 5],
        1: [1, 2],
        2: [3, 4],
        3: [4],
        4: [5]
    }
    
    edge_id = 0
    for r_idx, m_list in links.items():
        for m_idx in m_list:
            add_edge(root, f"edge_{edge_id}", f"r_{r_idx}", f"m_{m_idx}")
            edge_id += 1

def build_casos_uso(diagram):
    root = add_root(diagram)
    
    # System boundary
    add_cell(root, "sys", "SoftVar - Casos de Uso", "swimlane;whiteSpace=wrap;html=1;fillColor=#2d2d2d;strokeColor=#ffffff;fontColor=#ffffff;startSize=30;", 300, 50, 500, 700)
    
    # Actors
    add_cell(root, "act_rh", "Admin RRHH", "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;strokeColor=#ffffff;fontColor=#ffffff;", 100, 150, 40, 80)
    add_cell(root, "act_emp", "Empleado", "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;strokeColor=#ffffff;fontColor=#ffffff;", 100, 350, 40, 80)
    add_cell(root, "act_con", "Contador", "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;strokeColor=#ffffff;fontColor=#ffffff;", 100, 550, 40, 80)
    add_cell(root, "act_ger", "Gerente", "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;strokeColor=#ffffff;fontColor=#ffffff;", 900, 200, 40, 80)
    add_cell(root, "act_sys", "Admin Sist", "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;strokeColor=#ffffff;fontColor=#ffffff;", 900, 400, 40, 80)
    
    # Use cases
    casos = [
        ("uc1", "Gestionar Empleados", 350, 100),
        ("uc2", "Registrar Asistencia (Biometría)", 350, 200),
        ("uc3", "Ver Historial Asistencias", 350, 300),
        ("uc4", "Generar Nómina", 350, 400),
        ("uc5", "Exportar Desprendibles y ACH", 350, 500),
        ("uc6", "Ver Dashboard y Reportes", 350, 600),
        ("uc7", "Configurar Parámetros", 600, 350)
    ]
    
    for c in casos:
        add_cell(root, c[0], c[1], "ellipse;whiteSpace=wrap;html=1;fillColor=#1a1a1a;strokeColor=#ffffff;fontColor=#ffffff;", c[2], c[3], 150, 60)
        
    add_edge(root, "eu1", "act_rh", "uc1")
    add_edge(root, "eu2", "act_rh", "uc2")
    add_edge(root, "eu3", "act_emp", "uc2")
    add_edge(root, "eu4", "act_emp", "uc3")
    add_edge(root, "eu5", "act_con", "uc4")
    add_edge(root, "eu6", "act_con", "uc5")
    add_edge(root, "eu7", "act_ger", "uc6")
    add_edge(root, "eu8", "act_con", "uc6")
    add_edge(root, "eu9", "act_sys", "uc7")


def draw_browser(root, title):
    add_cell(root, "browser", title, "swimlane;whiteSpace=wrap;html=1;fillColor=#333333;strokeColor=#ffffff;fontColor=#ffffff;startSize=30;", 100, 50, 1000, 700)
    # Sidebar
    if title not in ["/login", "/reset-password"]:
        add_cell(root, "sidebar", "Menú Lateral\n- Empleados\n- Asistencia\n- Nómina\n- Reportes\n- Config", "rounded=0;whiteSpace=wrap;html=1;fillColor=#1a1a1a;strokeColor=#ffffff;fontColor=#ffffff;align=center;", 100, 80, 200, 670)

def build_login(diagram):
    root = add_root(diagram)
    draw_browser(root, "/login")
    add_cell(root, "box", "Acceso al Sistema", "rounded=1;whiteSpace=wrap;html=1;fillColor=#1a1a1a;strokeColor=#ffffff;fontColor=#ffffff;align=top;", 400, 200, 400, 350)
    add_cell(root, "inp1", "Email", "rounded=1;whiteSpace=wrap;html=1;fillColor=#2a2a2a;strokeColor=#ffffff;fontColor=#aaaaaa;", 450, 280, 300, 40)
    add_cell(root, "inp2", "Contraseña", "rounded=1;whiteSpace=wrap;html=1;fillColor=#2a2a2a;strokeColor=#ffffff;fontColor=#aaaaaa;", 450, 340, 300, 40)
    add_cell(root, "btn", "Ingresar", "rounded=1;whiteSpace=wrap;html=1;fillColor=#185FA5;strokeColor=#ffffff;fontColor=#ffffff;", 450, 420, 300, 40)
    add_cell(root, "lnk", "¿Olvidaste tu contraseña?", "text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontColor=#378ADD;", 450, 480, 300, 30)

def build_reset(diagram):
    root = add_root(diagram)
    draw_browser(root, "/reset-password")
    add_cell(root, "box", "Recuperar Contraseña", "rounded=1;whiteSpace=wrap;html=1;fillColor=#1a1a1a;strokeColor=#ffffff;fontColor=#ffffff;align=top;", 400, 200, 400, 250)
    add_cell(root, "inp1", "Ingresa tu Email", "rounded=1;whiteSpace=wrap;html=1;fillColor=#2a2a2a;strokeColor=#ffffff;fontColor=#aaaaaa;", 450, 280, 300, 40)
    add_cell(root, "btn", "Enviar enlace de recuperación", "rounded=1;whiteSpace=wrap;html=1;fillColor=#185FA5;strokeColor=#ffffff;fontColor=#ffffff;", 450, 360, 300, 40)

def build_listado(diagram):
    root = add_root(diagram)
    draw_browser(root, "/empleados")
    add_cell(root, "h1", "Listado de Empleados", "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontColor=#ffffff;fontSize=24;", 350, 100, 400, 40)
    add_cell(root, "btn", "+ Nuevo Empleado", "rounded=1;whiteSpace=wrap;html=1;fillColor=#185FA5;strokeColor=#ffffff;fontColor=#ffffff;", 900, 100, 150, 40)
    add_cell(root, "inp", "🔍 Buscar empleado...", "rounded=1;whiteSpace=wrap;html=1;fillColor=#2a2a2a;strokeColor=#ffffff;fontColor=#aaaaaa;", 350, 160, 300, 40)
    
    table_html = "<table width='100%' border='1' style='border-collapse:collapse;color:white;'><tr><th>Cédula</th><th>Nombre</th><th>Cargo</th><th>Acciones</th></tr><tr><td>1001</td><td>Juan Perez</td><td>Desarrollador</td><td>[Editar] [Borrar]</td></tr><tr><td>1002</td><td>Maria Lopez</td><td>Diseñadora</td><td>[Editar] [Borrar]</td></tr></table>"
    add_cell(root, "tbl", table_html, "text;html=1;strokeColor=#ffffff;fillColor=#1a1a1a;align=left;verticalAlign=top;whiteSpace=wrap;rounded=0;", 350, 230, 700, 400)

def build_form_emp(diagram):
    root = add_root(diagram)
    draw_browser(root, "/empleados/nuevo - /empleados/editar")
    add_cell(root, "h1", "Formulario Empleado", "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontColor=#ffffff;fontSize=24;", 350, 100, 400, 40)
    
    add_cell(root, "f1", "Nombres", "rounded=1;whiteSpace=wrap;html=1;fillColor=#2a2a2a;strokeColor=#ffffff;", 350, 180, 200, 40)
    add_cell(root, "f2", "Apellidos", "rounded=1;whiteSpace=wrap;html=1;fillColor=#2a2a2a;strokeColor=#ffffff;", 580, 180, 200, 40)
    add_cell(root, "f3", "Cédula", "rounded=1;whiteSpace=wrap;html=1;fillColor=#2a2a2a;strokeColor=#ffffff;", 350, 250, 200, 40)
    add_cell(root, "f4", "Cargo", "rounded=1;whiteSpace=wrap;html=1;fillColor=#2a2a2a;strokeColor=#ffffff;", 580, 250, 200, 40)
    add_cell(root, "f5", "Salario Base", "rounded=1;whiteSpace=wrap;html=1;fillColor=#2a2a2a;strokeColor=#ffffff;", 350, 320, 200, 40)
    add_cell(root, "f6", "Banco y Cuenta", "rounded=1;whiteSpace=wrap;html=1;fillColor=#2a2a2a;strokeColor=#ffffff;", 580, 320, 200, 40)
    
    add_cell(root, "cam", "[Componente de Captura Biométrica]\n📷 Activar Cámara", "rounded=1;whiteSpace=wrap;html=1;fillColor=#1a1a1a;strokeColor=#ffffff;dashed=1;", 820, 180, 230, 180)
    
    add_cell(root, "btn", "Guardar Empleado", "rounded=1;whiteSpace=wrap;html=1;fillColor=#3B6D11;strokeColor=#ffffff;fontColor=#ffffff;", 350, 420, 200, 40)

def build_asistencia(diagram):
    root = add_root(diagram)
    draw_browser(root, "/asistencia")
    add_cell(root, "h1", "Registro de Asistencia Biométrico", "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontColor=#ffffff;fontSize=24;", 350, 100, 500, 40)
    
    add_cell(root, "cam", "Video Feed (face-api.js)\n\n👤\nAnalizando rostro...", "rounded=1;whiteSpace=wrap;html=1;fillColor=#1a1a1a;strokeColor=#378ADD;fontColor=#ffffff;strokeWidth=4;", 400, 180, 500, 350)
    
    add_cell(root, "gps", "📍 Validación GPS (100m radio) - OK", "text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontColor=#3B6D11;", 400, 550, 500, 30)
    
    add_cell(root, "btn", "Marcar Entrada / Salida", "rounded=1;whiteSpace=wrap;html=1;fillColor=#185FA5;strokeColor=#ffffff;fontColor=#ffffff;", 500, 610, 300, 50)

def build_nomina(diagram):
    root = add_root(diagram)
    draw_browser(root, "/nomina")
    add_cell(root, "h1", "Liquidación de Nómina", "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontColor=#ffffff;fontSize=24;", 350, 100, 400, 40)
    
    add_cell(root, "b1", "Generar PDF Masivo", "rounded=1;whiteSpace=wrap;html=1;fillColor=#185FA5;strokeColor=#ffffff;fontColor=#ffffff;", 700, 100, 160, 40)
    add_cell(root, "b2", "Exportar ACH (.txt)", "rounded=1;whiteSpace=wrap;html=1;fillColor=#3B6D11;strokeColor=#ffffff;fontColor=#ffffff;", 880, 100, 160, 40)
    
    add_cell(root, "filt", "Filtro Mes/Año: [ Select ▼ ]", "rounded=1;whiteSpace=wrap;html=1;fillColor=#2a2a2a;strokeColor=#ffffff;", 350, 170, 250, 40)
    
    table_html = "<table width='100%' border='1' style='border-collapse:collapse;color:white;'><tr><th>Empleado</th><th>Salario Base</th><th>HE</th><th>Deducciones</th><th>Neto Pagar</th></tr><tr><td>Juan Perez</td><td>$2M</td><td>$50k</td><td>$160k</td><td>$1.89M</td></tr><tr><td>Maria Lopez</td><td>$3M</td><td>$0</td><td>$240k</td><td>$2.76M</td></tr></table>"
    add_cell(root, "tbl", table_html, "text;html=1;strokeColor=#ffffff;fillColor=#1a1a1a;align=left;verticalAlign=top;whiteSpace=wrap;rounded=0;", 350, 240, 700, 350)

def build_reportes(diagram):
    root = add_root(diagram)
    draw_browser(root, "/reportes - Dashboard")
    add_cell(root, "h1", "Dashboard Gerencial", "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontColor=#ffffff;fontSize=24;", 350, 100, 400, 40)
    
    add_cell(root, "k1", "Total Empleados\n45", "rounded=1;whiteSpace=wrap;html=1;fillColor=#1a1a1a;strokeColor=#ffffff;fontSize=18;", 350, 170, 200, 80)
    add_cell(root, "k2", "Asistencia Hoy\n95%", "rounded=1;whiteSpace=wrap;html=1;fillColor=#1a1a1a;strokeColor=#ffffff;fontSize=18;", 580, 170, 200, 80)
    add_cell(root, "k3", "Costo Nómina Mes\n$ 115M", "rounded=1;whiteSpace=wrap;html=1;fillColor=#1a1a1a;strokeColor=#ffffff;fontSize=18;", 810, 170, 200, 80)
    
    add_cell(root, "ch1", "[ Gráfica Barras: Asistencia Semanal ]", "rounded=1;whiteSpace=wrap;html=1;fillColor=#1a1a1a;strokeColor=#ffffff;dashed=1;", 350, 280, 430, 250)
    add_cell(root, "ch2", "[ Gráfico Torta: Distrib. Cargos ]", "rounded=1;whiteSpace=wrap;html=1;fillColor=#1a1a1a;strokeColor=#ffffff;dashed=1;", 810, 280, 220, 250)

def build_config(diagram):
    root = add_root(diagram)
    draw_browser(root, "/configuracion")
    add_cell(root, "h1", "Configuración del Sistema", "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontColor=#ffffff;fontSize=24;", 350, 100, 400, 40)
    
    add_cell(root, "l1", "SMMLV Actual", "text;html=1;strokeColor=none;fillColor=none;fontColor=#ffffff;", 350, 180, 200, 30)
    add_cell(root, "i1", "$ 1.300.000", "rounded=1;whiteSpace=wrap;html=1;fillColor=#2a2a2a;strokeColor=#ffffff;", 550, 175, 200, 40)
    
    add_cell(root, "l2", "Auxilio Transporte", "text;html=1;strokeColor=none;fillColor=none;fontColor=#ffffff;", 350, 250, 200, 30)
    add_cell(root, "i2", "$ 162.000", "rounded=1;whiteSpace=wrap;html=1;fillColor=#2a2a2a;strokeColor=#ffffff;", 550, 245, 200, 40)
    
    add_cell(root, "l3", "Tolerancia GPS (metros)", "text;html=1;strokeColor=none;fillColor=none;fontColor=#ffffff;", 350, 320, 200, 30)
    add_cell(root, "i3", "100", "rounded=1;whiteSpace=wrap;html=1;fillColor=#2a2a2a;strokeColor=#ffffff;", 550, 315, 200, 40)
    
    add_cell(root, "btn", "Guardar Configuración", "rounded=1;whiteSpace=wrap;html=1;fillColor=#185FA5;strokeColor=#ffffff;fontColor=#ffffff;", 350, 420, 200, 40)


mxfile = ET.Element("mxfile", host="Electron", version="22.1.2", type="device")

pages = [
    ("Separación Módulos por Rol", build_modulos_rol),
    ("Casos de Uso por Rol", build_casos_uso),
    ("Interfaz - Login", build_login),
    ("Interfaz - Recuperar Pass", build_reset),
    ("Interfaz - Listado Empleados", build_listado),
    ("Interfaz - Formulario Empleado", build_form_emp),
    ("Interfaz - Registro Asistencia", build_asistencia),
    ("Interfaz - Liq. Nómina", build_nomina),
    ("Interfaz - Dashboard Reportes", build_reportes),
    ("Interfaz - Configuración", build_config)
]

for idx, (name, func) in enumerate(pages):
    diagram = ET.SubElement(mxfile, "diagram", id=f"page_{idx}", name=name)
    graph = create_mxgraph()
    func(graph)
    diagram.append(graph)

xml_str = ET.tostring(mxfile, encoding="utf-8").decode("utf-8")
with open("/home/patrickortiz/Documentos/softvar/interfaces_y_casos_uso.drawio", "w", encoding="utf-8") as f:
    f.write(xml_str)
print("Archivo generado exitosamente.")
