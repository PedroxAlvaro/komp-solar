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

    html = "<h2>Clientes registrados</h2><table border='1' cellpadding='10'>"
    html += "<tr><th>Nombre</th><th>Email</th><th>Teléfono</th><th>Fecha</th><th>Hora</th></tr>"

    for c in contactos:
        html += f"<tr><td>{c['nombre']}</td><td>{c['email']}</td><td>{c['telefono']}</td><td>{c['fecha']}</td><td>{c['hora']}</td></tr>"

    html += "</table>"

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

    html = f"<h2>📊 Reporte</h2>"
    html += f"<p><strong>Total:</strong> {total}</p>"

    html += "<h3>Por día:</h3><ul>"
    for fecha in sorted(conteo_por_dia.keys(), reverse=True):
        html += f"<li>{fecha}: {conteo_por_dia[fecha]}</li>"
    html += "</ul>"

    html += "<h3>Por hora:</h3><ul>"
    for hora in sorted(conteo_por_hora.keys()):
        html += f"<li>{hora}:00 - {conteo_por_hora[hora]}</li>"
    html += "</ul>"

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

    df = pd.DataFrame(contactos)

    archivo_excel = os.path.join(DATA_DIR, "clientes.xlsx")
    df.to_excel(archivo_excel, index=False)

    return send_file(archivo_excel, as_attachment=True)

# ================================
# START
# ================================

if __name__ == '__main__':
    app.run(debug=True)