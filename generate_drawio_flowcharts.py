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

def add_edge(root, id, source, target, label="", parent="1", entryX=None, entryY=None, exitX=None, exitY=None, array_points=None):
    style = "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;fontColor=#ffffff;strokeColor=#ffffff;"
    if entryX is not None and entryY is not None:
        style += f"entryX={entryX};entryY={entryY};entryDx=0;entryDy=0;"
    if exitX is not None and exitY is not None:
        style += f"exitX={exitX};exitY={exitY};exitDx=0;exitDy=0;"
        
    cell = ET.SubElement(root, "mxCell", id=id, value=label, style=style, edge="1", parent=parent, source=source, target=target)
    geom = ET.SubElement(cell, "mxGeometry", relative="1", **{"as": "geometry"})
    if array_points:
        arr = ET.SubElement(geom, "Array", **{"as": "points"})
        for (px, py) in array_points:
            ET.SubElement(arr, "mxPoint", x=str(px), y=str(py))
    return cell

def n_start_end(root, id, text, x, y):
    return add_cell(root, id, text, "ellipse;whiteSpace=wrap;html=1;fillColor=#3F7A1A;strokeColor=#ffffff;fontColor=#ffffff;", x, y, 80, 80)

def n_process(root, id, text, x, y, width=120, height=60):
    return add_cell(root, id, text, "rounded=1;whiteSpace=wrap;html=1;fillColor=#185FA5;strokeColor=#ffffff;fontColor=#ffffff;", x, y, width, height)

def n_decision(root, id, text, x, y, width=120, height=80):
    return add_cell(root, id, text, "rhombus;whiteSpace=wrap;html=1;fillColor=#1a1a1a;strokeColor=#ffffff;fontColor=#ffffff;", x, y, width, height)

def n_io(root, id, text, x, y, width=120, height=60):
    return add_cell(root, id, text, "shape=parallelogram;perimeter=parallelogramPerimeter;whiteSpace=wrap;html=1;fixedSize=1;fillColor=#1a1a1a;strokeColor=#ffffff;fontColor=#ffffff;", x, y, width, height)


def build_flujo_principal(diagram):
    root = add_root(diagram)
    n_start_end(root, "inicio", "Inicio", 500, 50)
    n_io(root, "login", "Ingresar\nCredenciales", 480, 180)
    n_decision(root, "auth", "¿Login OK?", 480, 280)
    
    n_decision(root, "rol", "¿Qué rol\ntiene?", 480, 420)
    
    n_process(root, "rh", "Gestión Empleados", 100, 550)
    n_process(root, "emp", "Portal Personal\n(Asistencia)", 300, 550)
    n_process(root, "con", "Liq. Nómina", 500, 550)
    n_process(root, "ger", "Dashboard\nReportes", 700, 550)
    n_process(root, "sys", "Configuración", 900, 550)
    
    add_edge(root, "e1", "inicio", "login")
    add_edge(root, "e2", "login", "auth")
    add_edge(root, "e3", "auth", "rol", "Sí")
    add_edge(root, "e4", "auth", "login", "No", exitX=0, exitY=0.5, entryX=0, entryY=0.5, array_points=[(400, 320), (400, 210)])
    
    add_edge(root, "e5", "rol", "rh", "Admin RRHH")
    add_edge(root, "e6", "rol", "emp", "Empleado")
    add_edge(root, "e7", "rol", "con", "Contador")
    add_edge(root, "e8", "rol", "ger", "Gerente")
    add_edge(root, "e9", "rol", "sys", "Admin Sist")

def build_flujo_login(diagram):
    root = add_root(diagram)
    n_start_end(root, "s", "Inicio", 400, 50)
    n_decision(root, "d1", "¿Olvidó su\ncontraseña?", 380, 160)
    
    # Normal Login
    n_io(root, "in1", "Ingresa Email\ny Password", 200, 280)
    n_process(root, "p1", "Consultar BD", 200, 380)
    n_decision(root, "d2", "¿Datos OK?", 180, 480)
    n_process(root, "p2", "Generar JWT / Sesión", 200, 600)
    n_start_end(root, "end1", "Fin\n(Redirige)", 220, 700)
    
    add_edge(root, "e1", "s", "d1")
    add_edge(root, "e2", "d1", "in1", "No")
    add_edge(root, "e3", "in1", "p1")
    add_edge(root, "e4", "p1", "d2")
    add_edge(root, "e5", "d2", "in1", "No", exitX=0, exitY=0.5, entryX=0, entryY=0.5, array_points=[(100, 520), (100, 310)])
    add_edge(root, "e6", "d2", "p2", "Sí")
    add_edge(root, "e7", "p2", "end1")
    
    # Reset
    n_io(root, "in2", "Ingresa Email", 580, 280)
    n_process(root, "p3", "Generar Token y\nEnviar Correo", 580, 380)
    n_start_end(root, "end2", "Fin", 600, 500)
    
    add_edge(root, "e8", "d1", "in2", "Sí")
    add_edge(root, "e9", "in2", "p3")
    add_edge(root, "e10", "p3", "end2")

def build_flujo_empleados(diagram):
    root = add_root(diagram)
    n_start_end(root, "s", "Inicio", 400, 50)
    n_process(root, "p1", "Ver Listado\nEmpleados", 380, 160)
    n_decision(root, "d1", "¿Acción?", 380, 260)
    
    # Create / Edit
    n_io(root, "in1", "Llenar Formulario", 200, 380)
    n_process(root, "p2", "Activar Cámara\n(Biometría)", 200, 480)
    n_decision(root, "d2", "¿Rostro\nDetectado?", 180, 580)
    n_process(root, "p3", "Guardar Descriptor JSON", 200, 700)
    n_process(root, "p4", "Guardar Empleado (BD)", 200, 800)
    
    add_edge(root, "e1", "s", "p1")
    add_edge(root, "e2", "p1", "d1")
    add_edge(root, "e3", "d1", "in1", "Crear / Editar")
    add_edge(root, "e4", "in1", "p2")
    add_edge(root, "e5", "p2", "d2")
    add_edge(root, "e6", "d2", "p2", "No", exitX=0, exitY=0.5, entryX=0, entryY=0.5, array_points=[(100, 620), (100, 510)])
    add_edge(root, "e7", "d2", "p3", "Sí")
    add_edge(root, "e8", "p3", "p4")
    
    # Delete / Status
    n_process(root, "p5", "Inactivar / Borrar", 580, 380)
    add_edge(root, "e9", "d1", "p5", "Borrar")
    add_edge(root, "e10", "p5", "p1", "Refrescar", exitX=1, exitY=0.5, entryX=1, entryY=0.5, array_points=[(750, 410), (750, 190)])
    add_edge(root, "e11", "p4", "p1", "Refrescar", exitX=0, exitY=0.5, entryX=0, entryY=0.25, array_points=[(30, 830), (30, 175)])

def build_flujo_asistencia(diagram):
    root = add_root(diagram)
    n_start_end(root, "s", "Inicio", 400, 50)
    n_process(root, "p1", "Solicitar Permisos\nCámara y GPS", 380, 150)
    n_decision(root, "d1", "¿Concedidos?", 380, 250)
    
    n_process(root, "err1", "Mostrar Error", 600, 260)
    n_start_end(root, "end1", "Fin", 620, 360)
    
    n_process(root, "p2", "Capturar Foto", 380, 380)
    n_process(root, "p3", "face-api.js\nComparar rostro", 380, 470)
    n_decision(root, "d2", "¿Similitud\n> 80%?", 380, 560)
    
    n_process(root, "p4", "Obtener GPS Lat/Lng", 380, 680)
    n_decision(root, "d3", "¿Dentro de 100m?", 380, 780)
    
    n_process(root, "p5", "Guardar Asistencia", 380, 900)
    n_start_end(root, "end2", "Fin", 400, 1000)
    
    add_edge(root, "e1", "s", "p1")
    add_edge(root, "e2", "p1", "d1")
    add_edge(root, "e3", "d1", "err1", "No")
    add_edge(root, "e4", "err1", "end1")
    
    add_edge(root, "e5", "d1", "p2", "Sí")
    add_edge(root, "e6", "p2", "p3")
    add_edge(root, "e7", "p3", "d2")
    add_edge(root, "e8", "d2", "p2", "No", exitX=0, exitY=0.5, entryX=0, entryY=0.5, array_points=[(300, 600), (300, 410)])
    
    add_edge(root, "e9", "d2", "p4", "Sí")
    add_edge(root, "e10", "p4", "d3")
    add_edge(root, "e11", "d3", "err1", "No", exitX=1, exitY=0.5, entryX=0.5, entryY=1, array_points=[(660, 820)])
    
    add_edge(root, "e12", "d3", "p5", "Sí")
    add_edge(root, "e13", "p5", "end2")

def build_flujo_nomina(diagram):
    root = add_root(diagram)
    n_start_end(root, "s", "Inicio", 400, 50)
    n_io(root, "i1", "Seleccionar\nMes y Año", 380, 160)
    n_process(root, "p1", "Consultar Asistencias\ny Empleados", 380, 260)
    n_process(root, "p2", "Calcular: Días, HE,\nSalud, Pensión", 380, 360)
    n_io(root, "o1", "Mostrar Tabla\nResultados", 380, 460)
    
    n_decision(root, "d1", "¿Acción a\nrealizar?", 380, 560)
    
    n_process(root, "p3", "Generar PDF\n(jsPDF)", 200, 680)
    n_process(root, "p4", "Enviar por\nCorreo", 200, 780)
    
    n_process(root, "p5", "Formatear txt", 580, 680)
    n_process(root, "p6", "Descargar ACH", 580, 780)
    
    n_start_end(root, "end", "Fin", 400, 900)
    
    add_edge(root, "e1", "s", "i1")
    add_edge(root, "e2", "i1", "p1")
    add_edge(root, "e3", "p1", "p2")
    add_edge(root, "e4", "p2", "o1")
    add_edge(root, "e5", "o1", "d1")
    
    add_edge(root, "e6", "d1", "p3", "Desprendibles PDF")
    add_edge(root, "e7", "p3", "p4")
    add_edge(root, "e8", "p4", "end")
    
    add_edge(root, "e9", "d1", "p5", "Exportar ACH")
    add_edge(root, "e10", "p5", "p6")
    add_edge(root, "e11", "p6", "end")

def build_flujo_reportes(diagram):
    root = add_root(diagram)
    n_start_end(root, "s", "Inicio", 400, 50)
    n_process(root, "p1", "Cargar métricas\ngenerales (API)", 380, 150)
    n_io(root, "o1", "Renderizar Chart.js\n(Barras, Torta)", 380, 250)
    n_decision(root, "d1", "¿Aplicar\nFiltros?", 380, 360)
    
    n_io(root, "i1", "Ingresar\nFechas/Cargos", 600, 370)
    n_process(root, "p2", "Recargar datos\n(API)", 600, 250)
    
    n_start_end(root, "end", "Fin", 400, 500)
    
    add_edge(root, "e1", "s", "p1")
    add_edge(root, "e2", "p1", "o1")
    add_edge(root, "e3", "o1", "d1")
    add_edge(root, "e4", "d1", "end", "No")
    
    add_edge(root, "e5", "d1", "i1", "Sí")
    add_edge(root, "e6", "i1", "p2")
    add_edge(root, "e7", "p2", "o1")

def build_flujo_config(diagram):
    root = add_root(diagram)
    n_start_end(root, "s", "Inicio", 400, 50)
    n_process(root, "p1", "Consultar config\nactual en BD", 380, 150)
    n_io(root, "o1", "Mostrar formulario\n(SMMLV, Radio GPS)", 380, 250)
    n_decision(root, "d1", "¿Modificar?", 380, 360)
    
    n_io(root, "i1", "Ingresar\nnuevos valores", 600, 370)
    n_process(root, "p2", "Validar formato\n(Números)", 600, 480)
    n_decision(root, "d2", "¿Datos OK?", 600, 580)
    
    n_process(root, "p3", "Actualizar BD", 600, 700)
    n_process(root, "err", "Mostrar Error", 850, 600)
    
    n_start_end(root, "end", "Fin", 400, 720)
    
    add_edge(root, "e1", "s", "p1")
    add_edge(root, "e2", "p1", "o1")
    add_edge(root, "e3", "o1", "d1")
    add_edge(root, "e4", "d1", "end", "No")
    
    add_edge(root, "e5", "d1", "i1", "Sí")
    add_edge(root, "e6", "i1", "p2")
    add_edge(root, "e7", "p2", "d2")
    
    add_edge(root, "e8", "d2", "err", "No")
    add_edge(root, "e9", "err", "i1", exitX=0.5, exitY=0, entryX=1, entryY=0.5, array_points=[(910, 400)])
    
    add_edge(root, "e10", "d2", "p3", "Sí")
    add_edge(root, "e11", "p3", "end")


mxfile = ET.Element("mxfile", host="Electron", version="22.1.2", type="device")

pages = [
    ("Navegación General por Rol", build_flujo_principal),
    ("Flujo: Login y Recuperación", build_flujo_login),
    ("Flujo: Gestión de Empleados", build_flujo_empleados),
    ("Flujo: Registro de Asistencia", build_flujo_asistencia),
    ("Flujo: Liquidación de Nómina", build_flujo_nomina),
    ("Flujo: Reportes y Dashboard", build_flujo_reportes),
    ("Flujo: Configuración Global", build_flujo_config)
]

for idx, (name, func) in enumerate(pages):
    diagram = ET.SubElement(mxfile, "diagram", id=f"flow_{idx}", name=name)
    graph = create_mxgraph()
    func(graph)
    diagram.append(graph)

xml_str = ET.tostring(mxfile, encoding="utf-8").decode("utf-8")
with open("/home/patrickortiz/Documentos/softvar/flujos_interfaces.drawio", "w", encoding="utf-8") as f:
    f.write(xml_str)
print("Archivo de flujos generado exitosamente.")
