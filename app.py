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
    descricao = db.Column(db.String(), nullable=True)

    def __repr__(self):
        return f'<Produto {self.id} {self.nome}>'


with app.app_context():
    db.create_all()

# Fim banco de dados


categorias = {
    "roupas": "Roupas",
    "feminino": "Feminino",
    "plus_size": "Plus Size",
    "masculino": "Masculino",
    "bebe_maternidade": "Bebê & Maternidade",
    "sapatos_bolsas": "Sapatos e Bolsa",
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

        produto = Produto(nome=nome, preco=preco, categoria=categoria)

        db.session.add(produto)
        db.session.commit()

        return redirect(url_for('produtos'))

    return render_template('produtos_cadastrar.html', categorias=categorias)


@app.route("/produtos/", defaults={"categoria": None})
@app.route("/produtos/<categoria>")
def produtos(categoria):
    produtos = Produto.query.all()

    if categoria != None:
        itens_filtrados = []

        for produto in produtos:
            if produto['categoria'] == categoria:
                itens_filtrados.append(produto)
        
        produtos = itens_filtrados


    return render_template('produtos.html', produtos = produtos)


# @app.route("/produtos/<categoria>")
# def categorias():
#     produtos = [
#         {
#             "nome": "vestido",
#             "preco": 79.99,
#             "categoria": "roupas",
#         },
#         {
#             "nome": "Havaianas",
#             "preco": 49.99,
#             "categoria": "calçados",
#         },
#     ]

#     return render_template('produtos.html', produtos = produtos)


if __name__ == '__main__':
    app.run(debug=True)
