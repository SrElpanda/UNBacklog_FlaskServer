from flask import Flask, request, jsonify
import psycopg2
import os
import urllib.parse
from flask_cors import CORS  


app = Flask(__name__)
CORS(app)

# Configura tus credenciales aquí
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

def conectar():
    return psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )

def buscar_tramites(query):
    conn = conectar()
    cur = conn.cursor()
    like = f"%{query}%"
    cur.execute("SELECT titulo, descripcion FROM tramites WHERE titulo ILIKE %s OR descripcion ILIKE %s", (like, like))
    resultados = cur.fetchall()
    cur.close()
    conn.close()
    return [{"titulo": t, "descripcion": d} for t, d in resultados]

@app.route("/api/tramites")
def tramites():
    q = request.args.get("q", "")
    return jsonify(buscar_tramites(q))

if __name__ == "__main__":
    app.run(debug=True)