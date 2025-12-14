from db import insert_record

def procesar_datos(data):
    print("🔧 procesar_datos recibió:", data)

    # Campos obligatorios
    campos = [
        "estado", "fechaHora", "bateriaVolt", "bateriaPorc",
        "temperatura", "humedad", "presion", "luz",
        "velocViento", "proxEnvio"
    ]

    # Validación
    for campo in campos:
        if campo not in data:
            return {"status": "error", "message": f"Falta campo: {campo}"}, 400

    # Crear tupla para insertar en DB
    registro = (
        data["estado"],
        data["fechaHora"],
        data["bateriaVolt"],
        data["bateriaPorc"],
        data["temperatura"],
        data["humedad"],
        data["presion"],
        data["luz"],
        data["velocViento"],
        data["proxEnvio"]
    )

    insert_record(registro)

    return {"status": "ok", "message": "Datos recibidos"}, 201