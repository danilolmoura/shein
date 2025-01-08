import random

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configura banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shein.db'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = True
db = SQLAlchemy(app)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(), nullable=False)
    preco = db.Column(db.Float(), nullable=False)
    categoria = db.Column(db.String(), nullable=False)
    # descricao = db.Column(db.String(), nullable=True)

    def __repr__(self):
        return f'<Produto {self.id} {self.nome}>'

with app.app_context():
    db.create_all()

categorias= {
    "roupas": "Roupas",
    "feminino": "Feminino",
    "plus_size": "Plus Size",
    "masculino": "Masculino",
    "bebe_maternidade": "Bebê & Maternidade",
    "sapatos_bolsas": "Sapatos e Bolsa",
    "unissex": "Unissex",
    "maquiagem": "Maquiagem",
    "todos":"Todos"
}


@app.route("/")
def index():
    return render_template('index.html', categorias=categorias)


@app.route("/produtos/cadastrar", methods=['GET', 'POST'])
def adicionar_produtos():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        categoria = request.form['categoria']
        # descricao = request.form['descricao']

        produto = Produto(nome=nome, preco=preco, categoria=categoria)

        db.session.add(produto)
        db.session.commit()

        return redirect(url_for('produtos'))

    return render_template('produtos_cadastrar.html', categorias=categorias)


@app.route("/produtos/", defaults={"categoria": None}, methods=['GET', 'POST'])
@app.route("/produtos/<categoria>")
def produtos(categoria):
    # produtos = 
    if request.method == 'POST': 
        categoria = request.form.get('categoria')
        faixa_preco = request.form.get('faixa_preco')
        if categoria == "todos":
            categoria = None
        print(faixa_preco)
        produtos = Produto.query.filter(Produto.categoria==categoria).filter(Produto.preco<=faixa_preco).all()
    else:
        produtos = Produto.query.all()
        

    return render_template('produtos.html', produtos = produtos,categorias=categorias,total_produtos=len(produtos))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=4000)
