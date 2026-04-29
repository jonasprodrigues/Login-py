from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "chave_secreta_123"

# usuário fake (pra teste)
USUARIO = "admin"
SENHA = "123"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        if usuario == USUARIO and senha == SENHA:
            session["user"] = usuario
            return redirect("/home")
        else:
            return render_template("login.html", erro="Login inválido")

    return render_template("login.html")


@app.route("/home")
def home():
    if "user" not in session:
        return redirect("/")
    return render_template("home.html", user=session["user"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run()
