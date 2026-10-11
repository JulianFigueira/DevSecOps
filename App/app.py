import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)

# [VULN 1] Credencial escrita en el codigo -> la detecta Gitleaks
ADMIN_TOKEN = "tok_9f2Kx7LmQ4vR8nZ1wE6yT3pBhJ5c"

# Base de datos en memoria con datos de ejemplo
db = sqlite3.connect(":memory:", check_same_thread=False)
db.execute("CREATE TABLE productos (id INTEGER PRIMARY KEY, nombre TEXT, precio REAL)")
db.executemany(
    "INSERT INTO productos (nombre, precio) VALUES (?, ?)",
    [("Teclado", 25000), ("Mouse", 12000), ("Monitor", 180000), ("Notebook", 950000)],
)
db.commit()


@app.route("/")
def inicio():
    return (
        "<h1>Tienda demo DevSecOps</h1>"
        "<p>Buscar productos: <a href='/productos?nombre=Mouse'>/productos?nombre=Mouse</a></p>"
    )


@app.route("/productos")
def buscar_productos():
    nombre = request.args.get("nombre", "")
    # [VULN 2] Consulta SQL armada concatenando texto -> la detecta Bandit (B608)
    consulta = "SELECT id, nombre, precio FROM productos WHERE nombre LIKE '%" + nombre + "%'"
    filas = db.execute(consulta).fetchall()
    return jsonify([{"id": f[0], "nombre": f[1], "precio": f[2]} for f in filas])


@app.route("/admin")
def admin():
    if request.headers.get("X-Admin-Token") != ADMIN_TOKEN:
        return jsonify({"error": "no autorizado"}), 401
    total = db.execute("SELECT COUNT(*) FROM productos").fetchone()[0]
    return jsonify({"productos_cargados": total})


@app.route("/salud")
def salud():
    return jsonify({"estado": "ok"})


if __name__ == "__main__":
    # [VULN 3] Modo debug activado -> lo detecta Bandit (B201)
    app.run(host="0.0.0.0", port=5000, debug=True)