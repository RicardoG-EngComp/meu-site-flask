import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Configuração do Banco de Dados PostgreSQL usando variável de ambiente
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo do Banco de Dados
class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    assunto = db.Column(db.String(150), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    data_hora = db.Column(db.Datetime, default=datetime.utcnow)


# Criar tabelas no banco
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/submit_contact", methods=["POST"])
def submit_contact():
    nome = request.form["nome"]
    email = request.form["email"]
    assunto = request.form["assunto"]
    mensagem = request.form["mensagem"]

    novo_contato = Contato(nome=nome, email=email, assunto=assunto, mensagem=mensagem)
    db.session.add(novo_contato)
    db.session.commit()

    flash("Mensagem enviada com sucesso!", "success")
    return redirect(url_for("contato"))

@app.route("/test_db")
def test_db():
    novo_teste = Contato(nome="Teste", email="teste@example.com", assunto="Teste Assunto", mensagem="Teste Mensagem")
    db.session.add(novo_teste)
    db.session.commit()
    return "Teste adicionado com sucesso!"

@app.route("/mensagens")
def mensagens():
    contatos = Contato.query.all()
    return render_template("mensagens.html", contatos=contatos)



if __name__ == "__main__":
    app.run(debug=True)

