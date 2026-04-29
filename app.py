from flask import Flask, render_template, request, redirect, session
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = "chave_secreta_123"


# -----------------------------
# BANCO DE DADOS
# -----------------------------
def conectar():
    return sqlite3.connect("usuarios.db")


def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE,
            senha TEXT
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# CRIAR ADMIN AUTOMÁTICO
# -----------------------------
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


def criar_admin():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE usuario='admin'")
    admin = cursor.fetchone()

    if not admin:
        cursor.execute(
            "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",
            ("admin", hash_senha("123"))
        )
        conn.commit()

    conn.close()


criar_tabela()
criar_admin()


# -----------------------------
# LOGIN
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = hash_senha(request.form["senha"])

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE usuario=? AND senha=?",
            (usuario, senha)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session["user"] = usuario
            return redirect("/home")
        else:
            return render_template("login.html", erro="Login inválido")

    return render_template("login.html")


# -----------------------------
# HOME
# -----------------------------
@app.route("/home")
def home():
    if "user" not in session:
        return redirect("/")
    return render_template("home.html", user=session["user"])


# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# -----------------------------
# CADASTRO
# -----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = hash_senha(request.form["senha"])

        conn = conectar()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",
                (usuario, senha)
            )
            conn.commit()
        except:
            return "Usuário já existe"

        conn.close()
        return redirect("/")

    return render_template("register.html")


# -----------------------------
# ESQUECI SENHA (simples)
# -----------------------------
@app.route("/forgot")
def forgot():
    return render_template("forgot.html")


if __name__ == "__main__":
    app.run()
