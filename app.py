from datetime import datetime
import os
import sqlite3
from flask import Flask, redirect, render_template

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(basedir, "templates"),
    static_folder=os.path.join(basedir, "static"),
)


def init_db():
  db_path = os.path.join(basedir, "cliques.db")
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS cliques (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT NOT NULL
        )
    """)
  conn.commit()
  conn.close()


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/registrar-clique")
def registrar_clique():
  data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  db_path = os.path.join(basedir, "cliques.db")
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()
  cursor.execute("INSERT INTO cliques (data_hora) VALUES (?)", (data_hora,))
  conn.commit()

  cursor.execute("SELECT COUNT(*) FROM cliques")
  total = cursor.fetchone()[0]
  conn.close()

  print(
      f"\n >>> [SUCESSO] Clique salvo! Total de cliques no banco: {total} em"
      f" {data_hora} <<<\n"
  )

  # Substitua pelo link real do seu grupo do WhatsApp quando estiver pronto
  link_whatsapp = "https://chat.whatsapp.com/BlfLXEyAKUK4Ki9TiDw8JR"
  return redirect(link_whatsapp)


@app.route("/ver-cliques")
def ver_cliques():
  db_path = os.path.join(basedir, "cliques.db")
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM cliques")
  registros = cursor.fetchall()
  conn.close()

  return (
      f"<h1>Total de cliques guardados: {len(registros)}</h1>"
      f"<p>Registros: {registros}</p>"
  )


if __name__ == "__main__":
  init_db()
  app.run(debug=True, port=5000)
