"""
Aplicacion de ejemplo para el TPI de DevSecOps (ASI 2026 - UTN FRLP).
Version CORREGIDA: sin las vulnerabilidades intencionales.
"""
import os
import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)

# [FIX 1] El secreto se lee de una variable de entorno, no del codigo
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN")

db = sqlite3.connect(":memory:", check_same_thread=False)
db.execute("CREATE TABLE productos (id INTEGER PRIMARY KEY, nombre TEXT, precio REAL)")
db.executemany(
    "INSERT INTO productos (nombre, precio) VALUES (?, ?)",
    [("Teclado", 25000), ("Mouse", 12000), ("Monitor", 180000), ("Notebook", 950000)],
)
db.commit()


@app.after_request
def cabeceras_de_seguridad(respuesta):
    # Extra: cabeceras de seguridad (reduce las alertas de ZAP)
    respuesta.headers["X-Content-Type-Options"] = "nosniff"
    respuesta.headers["X-Frame-Options"] = "DENY"
    respuesta.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none'"
    respuesta.headers["Referrer-Policy"] = "no-referrer"
    respuesta.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
    respuesta.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    respuesta.headers["Cache-Control"] = "no-store"
    return respuesta


@app.route("/")
def inicio():
    return (
        "<h1>Tienda demo DevSecOps</h1>"
        "<p>Buscar productos: <a href='/productos?nombre=Mouse'>/productos?nombre=Mouse</a></p>"
    )


@app.route("/productos")
def buscar_productos():
    nombre = request.args.get("nombre", "")
    # [FIX 2] Consulta parametrizada: el dato del usuario nunca se mezcla con el SQL
    filas = db.execute(
        "SELECT id, nombre, precio FROM productos WHERE nombre LIKE ?",
        ("%" + nombre + "%",),
    ).fetchall()
    return jsonify([{"id": f[0], "nombre": f[1], "precio": f[2]} for f in filas])


@app.route("/admin")
def admin():
    if not ADMIN_TOKEN or request.headers.get("X-Admin-Token") != ADMIN_TOKEN:
        return jsonify({"error": "no autorizado"}), 401
    total = db.execute("SELECT COUNT(*) FROM productos").fetchone()[0]
    return jsonify({"productos_cargados": total})


@app.route("/salud")
def salud():
    return jsonify({"estado": "ok"})


if __name__ == "__main__":
    # [FIX 3] Sin modo debug y solo en localhost (en el contenedor se usa gunicorn)
    app.run(host='0.0.0.0', port=5000, debug=False)
