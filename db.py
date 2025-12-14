import sqlite3

DB_NAME = "estacion.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def insert_record(registro):
    conn = get_connection()
    cur = conn.cursor()

    # Crear tabla si no existe
    cur.execute("""
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estado TEXT,
            fechaHora TEXT,
            bateriaVolt REAL,
            bateriaPorc INTEGER,
            temperatura REAL,
            humedad REAL,
            presion REAL,
            luz REAL,
            velocViento REAL,
            proxEnvio TEXT
        )
    """)

    # Insertar registro
    cur.execute("""
        INSERT INTO registros (
            estado, fechaHora, bateriaVolt, bateriaPorc,
            temperatura, humedad, presion, luz,
            velocViento, proxEnvio
        ) VALUES (?,?,?,?,?,?,?,?,?,?)
    """, registro)

    conn.commit()
    conn.close()

def get_latest():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM registros
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cur.fetchone()
    conn.close()

    if row:
        return dict(row)
    return None