from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)
ARQUIVO = "vendedores.json"

def carregar_vendedores():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def salvar_vendedores(vendedores):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(vendedores, f, ensure_ascii=False, indent=4)

@app.route("/")
def index():
    vendedores = carregar_vendedores()
    return render_template("index.html", vendedores=vendedores)

@app.route("/adicionar", methods=["POST"])
def adicionar():
    nome = request.form["nome"].strip()
    vendedores = carregar_vendedores()
    if nome and nome.lower() not in (v.lower() for v in vendedores):
        vendedores.append(nome)
        salvar_vendedores(vendedores)
    return redirect(url_for("index"))

@app.route("/editar/<nome>", methods=["GET", "POST"])
def editar(nome):
    vendedores = carregar_vendedores()
    if request.method == "POST":
        novo_nome = request.form["novo_nome"].strip()
        for i, v in enumerate(vendedores):
            if v.lower() == nome.lower():
                vendedores[i] = novo_nome
                salvar_vendedores(vendedores)
                break
        return redirect(url_for("index"))
    return render_template("editar.html", nome=nome)

@app.route("/remover/<nome>")
def remover(nome):
    vendedores = carregar_vendedores()
    vendedores = [v for v in vendedores if v.lower() != nome.lower()]
    salvar_vendedores(vendedores)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
