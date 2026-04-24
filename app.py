from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
import os
from datetime import datetime
import shutil
import pandas as pd

app = Flask(__name__)

# ✅ CORS CORREGIDO (IMPORTANTE)
CORS(app, resources={r"/*": {"origins": "*"}})

# ================================
# CONFIG
# ================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
ARCHIVO = os.path.join(DATA_DIR, "contactos.json")
BACKUP_DIR = os.path.join(DATA_DIR, "backup")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)

# Crear archivo si no existe
if not os.path.exists(ARCHIVO):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump([], f)

# ================================
# FUNCIONES
# ================================

def leer_datos():
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def guardar_datos(datos):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def crear_backup():
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    destino = os.path.join(BACKUP_DIR, f"contactos_{fecha}.json")
    shutil.copy(ARCHIVO, destino)

# ================================
# RUTAS
# ================================

@app.route('/')
def home():
    return "Servidor funcionando - Komp Solar"

# ================================
# FORMULARIO
# ================================

@app.route('/contacto', methods=['POST'])
def contacto():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "message": "No hay datos"})

        # VALIDACIÓN
        if not data.get("nombre") or not data.get("email"):
            return jsonify({"success": False, "message": "Datos incompletos"})

        ahora = datetime.now()

        nuevo = {
            "id": ahora.strftime("%Y%m%d%H%M%S"),
            "nombre": data.get("nombre"),
            "email": data.get("email"),
            "telefono": data.get("telefono"),
            "mensaje": data.get("mensaje"),
            "fecha": ahora.strftime("%Y-%m-%d"),
            "hora": ahora.strftime("%H:%M:%S"),
            "timestamp": ahora.isoformat()
        }

        contactos = leer_datos()

        # MÁS RECIENTE ARRIBA
        contactos.insert(0, nuevo)

        guardar_datos(contactos)
        crear_backup()

        print("✔ Nuevo contacto:", nuevo)

        return jsonify({"success": True})

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"success": False, "message": "Error en servidor"})
    
















# ================================
# PANEL CLIENTES (OCULTO)
# ================================

@app.route('/admin-clientes-93847')
def clientes():
    contactos = leer_datos()

    html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Panel Clientes</title>

<style>
:root{{
    --fondo:#000;
    --card:#0d0d0d;
    --card-hover:#1a1a1a;
    --primario:#ff7a00;
    --primario-hover:#ff9500;
    --texto:#fff;
    --gris:#aaa;
}}

body{{
    font-family: Arial, Helvetica, sans-serif;
    background: var(--fondo);
    color: var(--texto);
    padding:20px;
}}

h2{{
    text-align:center;
    margin-bottom:25px;
    color: var(--primario);
}}

.top-bar{{
    display:flex;
    justify-content:space-between;
    margin-bottom:20px;
    flex-wrap:wrap;
}}

input{{
    padding:10px;
    width:260px;
    border-radius:6px;
    border:1px solid #222;
    background:#000;
    color:white;
}}

.boton{{
    background:var(--primario);
    color:white;
    padding:10px 18px;
    border-radius:6px;
    text-decoration:none;
    font-weight:bold;
}}

table{{
    width:100%;
    border-collapse:collapse;
    background:var(--card);
}}

th, td{{
    padding:12px;
    text-align:center;
}}

th{{
    background:var(--primario);
}}

tr:nth-child(even){{
    background:var(--card-hover);
}}
</style>

</head>
<body>

<h2>📊 Panel de Clientes</h2>

<div class="top-bar">
    <input type="text" id="buscador" placeholder="Buscar cliente...">
    <a href="/admin-exportar-93847" class="boton">📥 Excel</a>
</div>

<table id="tabla">
<tr>
<th>Nombre</th>
<th>Email</th>
<th>Teléfono</th>
<th>Fecha</th>
<th>Hora</th>
</tr>
"""

    for c in contactos:
        html += f"""
<tr>
<td>{c['nombre']}</td>
<td>{c['email']}</td>
<td>{c['telefono']}</td>
<td>{c['fecha']}</td>
<td>{c['hora']}</td>
</tr>
"""

    html += """
</table>

<script>
const buscador = document.getElementById("buscador");
const filas = document.querySelectorAll("#tabla tr");

buscador.addEventListener("keyup", function() {
    const texto = buscador.value.toLowerCase();

    filas.forEach((fila, i) => {
        if(i === 0) return;
        fila.style.display = fila.innerText.toLowerCase().includes(texto) ? "" : "none";
    });
});
</script>

</body>
</html>
"""

    return html







# ================================
# REPORTE
# ================================

@app.route('/admin-reporte-93847')
def reporte():
    contactos = leer_datos()

    total = len(contactos)
    conteo_por_dia = {}
    conteo_por_hora = {}

    for c in contactos:
        fecha = c.get("fecha")
        hora = c.get("hora")[:2]

        conteo_por_dia[fecha] = conteo_por_dia.get(fecha, 0) + 1
        conteo_por_hora[hora] = conteo_por_hora.get(hora, 0) + 1

    html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
body{{background:#000;color:#fff;font-family:Arial;padding:20px}}
h2{{color:#ff7a00;text-align:center}}
.card{{background:#111;padding:20px;margin:10px;border-radius:10px}}
.total{{font-size:28px;color:#ff7a00;text-align:center}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}
li{{background:#1a1a1a;margin:5px;padding:8px;border-radius:5px}}
</style>
</head>

<body>

<h2>📊 Reporte</h2>

<div class="card total">Total: {total}</div>

<div class="grid">

<div class="card">
<h3>Por día</h3>
<ul>
"""

    for f in sorted(conteo_por_dia.keys(), reverse=True):
        html += f"<li>{f}: {conteo_por_dia[f]}</li>"

    html += "</ul></div><div class='card'><h3>Por hora</h3><ul>"

    for h in sorted(conteo_por_hora.keys()):
        html += f"<li>{h}:00 - {conteo_por_hora[h]}</li>"

    html += "</ul></div></div></body></html>"

    return html















# ================================
# EXPORTAR EXCEL
# ================================

@app.route('/admin-exportar-93847')
def exportar():
    contactos = leer_datos()

    if not contactos:
        return "No hay datos"

    contactos = sorted(contactos, key=lambda x: x["timestamp"], reverse=True)

    df = pd.DataFrame(contactos, columns=[
        "nombre",
        "email",
        "telefono",
        "mensaje",
        "fecha",
        "hora"
    ])

    df.columns = ["Nombre","Correo","Teléfono","Mensaje","Fecha","Hora"]

    archivo_excel = os.path.join(DATA_DIR, "clientes.xlsx")

    with pd.ExcelWriter(archivo_excel, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Clientes")

        sheet = writer.sheets["Clientes"]

        # 🔥 ESTILO PRO
        from openpyxl.styles import Font, PatternFill

        for cell in sheet[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill(start_color="FF7A00", fill_type="solid")

        # Ajuste ancho automático
        for col in sheet.columns:
            max_length = max(len(str(cell.value)) if cell.value else 0 for cell in col)
            sheet.column_dimensions[col[0].column_letter].width = max_length + 3

    return send_file(archivo_excel, as_attachment=True)








# ================================
# START
# ================================

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)