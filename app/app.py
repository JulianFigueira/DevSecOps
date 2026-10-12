import os
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL
        )
    ''')
    cursor.execute("INSERT INTO productos (nombre, precio) VALUES ('Laptop', 1200.0)")
    cursor.execute("INSERT INTO productos (nombre, precio) VALUES ('Mouse', 25.0)")
    cursor.execute("INSERT INTO productos (nombre, precio) VALUES ('Teclado', 45.0)")
    conn.commit()
    return conn

# Inicializar base de datos en memoria
db_conn = init_db()

@app.route('/')
def inicio():
    return jsonify({"mensaje": "API Demo DevSecOps - Version Corregida"})

@app.route('/salud')
def salud():
    return jsonify({"status": "ok"})

@app.route('/buscar')
def buscar():
    q = request.args.get('q', '')
    cursor = db_conn.cursor()
    # Consulta parametrizada para evitar SQL Injection
    cursor.execute("SELECT id, nombre, precio FROM productos WHERE nombre LIKE ?", (f"%{q}%",))
    resultados = [{"id": row[0], "nombre": row[1], "precio": row[2]} for row in cursor.fetchall()]
    return jsonify(resultados)

@app.route('/admin')
def admin():
    auth_header = request.headers.get('Authorization')
    admin_token = os.environ.get('ADMIN_TOKEN')
    
    if not admin_token or auth_header != f"Bearer {admin_token}":
        return jsonify({"error": "No autorizado"}), 401
        
    return jsonify({"mensaje": "Bienvenido al panel de administracion"})

if __name__ == '__main__':
    # host='0.0.0.0' es imprescindible para responder en el puerto mapeado del contenedor Docker
    app.run(host='0.0.0.0', port=5000, debug=False)
