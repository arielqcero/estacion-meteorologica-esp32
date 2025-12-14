from flask import Flask, request, jsonify
from handlers import procesar_datos
from db import get_latest
from db import get_connection, get_latest, insert_record

app = Flask(__name__)

# Ruta donde el ESP32 envía los datos
@app.route("/data", methods=["POST"])
def recibir_datos():
    data = request.get_json()
    print("📥 Datos recibidos en /data:", data)

    response, code = procesar_datos(data)
    return jsonify(response), code

# Ruta para consultar el último registro
@app.route("/latest", methods=["GET"])
def ultimo_registro():
    row = get_latest()
    if not row:
        return jsonify({"error": "No hay registros aún"}), 404
    respuesta = {
        "id": row["id"],
        "estado": row["estado"],
        "fechaHora": row["fechaHora"],
        "bateria": {
            "volt": row["bateriaVolt"],
            "porcentaje": row["bateriaPorc"]
        },
        "sensores": {
            "temperatura": row["temperatura"],
            "humedad": row["humedad"],
            "presion": row["presion"],
            "luz": row["luz"],
            "viento": row["velocViento"]
        },
        "proxEnvio": row["proxEnvio"]
    }
    return jsonify(respuesta)

@app.route("/")
def dashboard():
    return open("dashboard.html", encoding="utf-8").read()

@app.route("/graficos")
def graficos():
    return open("graficos.html", encoding="utf-8").read()

@app.route("/history", methods=["GET"])
def history():
    inicio = request.args.get("inicio")
    fin = request.args.get("fin")

    conn = get_connection()
    cur = conn.cursor()

    if inicio and fin:
        cur.execute("""
            SELECT * FROM registros
            WHERE fechaHora BETWEEN ? AND ?
            ORDER BY fechaHora ASC
        """, (inicio, fin))
    else:
        cur.execute("""
            SELECT * FROM registros
            ORDER BY fechaHora ASC
            LIMIT 200
        """)

    rows = cur.fetchall()
    conn.close()

    return jsonify([dict(r) for r in rows])


#esta parte de codigo siempre al final...
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
