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
  
  # Tabela existente de cliques
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS cliques (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT NOT NULL
        )
    """)
  
  # Nova tabela para o carrossel dinâmico de produtos
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos_dinamicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            preco_antigo TEXT NOT NULL,
            preco_novo TEXT NOT NULL,
            imagem_url TEXT NOT NULL
        )
    """)
  
  # Insere os teus produtos atuais como exemplo inicial se a tabela estiver vazia
  cursor.execute("SELECT COUNT(*) FROM produtos_dinamicos")
  if cursor.fetchone()[0] == 0:
    produtos_iniciais = [
        ("Ar Condicionado Split Inverter 18000 BTUs Hisense Hi-Efficiency Frio AS - 220V", "R$ R$3.554,44", "R$ 2.650,40", "/static/foto2.jpeg"),
        ("Sofá 3 Lugares Retrátil Lubeck Linho Cinza", "R$ 1.089,99", "R$ 649,99", "/static/sofa.jpeg"),
        ("Lava Louças Brastemp 8 Serviços Preta - BLF08AE Preto", "R$ 1.943,00", "R$ 1.749,00", "/static/foto3.jpeg"),
        ("Samsung Smart TV 65 MiniLED 4K M75H + Soundbar Samsung HW-B400F Combo", "R$ 4.749,00", "R$ 3.464,00", "/static/foto4.jpeg"),
        ("Tênis Nike Air Monarch Iv Masculino", "R$ 699,99", "R$ 489,99", "/static/foto5.jpeg"),
        ("Torneira Banheiro Bica Alta Aço Inox Preto Fosco Quente e Fria", "R$ 147,99", "R$ 105,44", "/static/torneira.jpeg"),
        ("Monitor Gamer Tcl 25 Qd-mini Led Full Hd G64 300hz 25g64", "R$ 2.300", "R$ 989,10", "/static/tela.jpeg"),
        ("Downy Amaciante de Roupas Concentrado Líquido Brisa Suave 3L", "R$ 74,77", "R$ 43,10", "/static/downy.jpeg"),
        ("Kit Edredom Casal + Jogo Lençol 3 Peças Micropercal 400 Fios", "R$ 188,36", "R$ 161,00", "/static/edredom.jpeg")

    ]
    cursor.executemany(
        "INSERT INTO produtos_dinamicos (titulo, preco_antigo, preco_novo, imagem_url) VALUES (?, ?, ?, ?)",
        produtos_iniciais
    )

  conn.commit()
  conn.close()


@app.route("/")
def index():
  db_path = os.path.join(basedir, "cliques.db")
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()
  cursor.execute("SELECT titulo, preco_antigo, preco_novo, imagem_url FROM produtos_dinamicos ORDER BY id DESC")
  produtos_db = cursor.fetchall()
  conn.close()

  produtos = []
  for p in produtos_db:
    produtos.append({
        "titulo": p[0],
        "preco_antigo": p[1],
        "preco_novo": p[2],
        "imagem_url": p[3]
    })

  return render_template("index.html", produtos=produtos)


# Nova rota de transição (Obrigado / Redirecionando)
@app.route("/redirecionar")
def redirecionar():
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

  link_whatsapp = "https://chat.whatsapp.com/BlfLXEyAKUK4Ki9TiDw8JR"
  return render_template("obrigado.html", link_whatsapp=link_whatsapp)


# Mantida caso queira redirecionamento direto antigo
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
