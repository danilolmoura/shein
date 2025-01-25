import os
import random

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configura banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shein.db'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = True
db = SQLAlchemy(app)
UPLOAD_FOLDER="static/uploads"

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(), nullable=False)
    preco = db.Column(db.Float(), nullable=False)
    categoria = db.Column(db.String(), nullable=False)
    imagem= db.Column(db.String(), nullable=True) 
    descricao = db.Column(db.String(), nullable=True)

    def __repr__(self):
        return f'<Produto {self.id} {self.nome}>'

carrinho_produto=db.Table("carrinho_produto",
    db.Column ("carrinho_id",db.Integer, db.ForeignKey("carrinho.id"),primary_key=True),
    db.Column ("produto_id",db.Integer, db.ForeignKey("produto.id"),primary_key=True))

class Carrinho(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    produtos= db.Relationship("Produto",secondary=carrinho_produto)


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
    'acessorio': "Acessório",
    "todos":"Todos"
}

def produto_com_desconto(preco):
    desconto = 0.25 
    preco_com_desconto = preco * (1 - desconto)
    return f"{preco_com_desconto:.2f}"

def adicionar_produto_carrinho(produto_id):
    print("________")
    print("________")
    produto=Produto.query.get(produto_id)
    carrinho=Carrinho.query.first()
    carrinho.produtos.append(produto)
    db.session.add(carrinho)
    db.session.commit()

@app.route("/")
def index():
    return render_template('index.html', categorias=categorias)

@app.route("/adicionar_carrinho",  methods=["POST"])
def adicionar_carrinho():
    produto_id=request.form.get("produto_id") 
    adicionar_produto_carrinho(produto_id) 
    return render_template('index.html', categorias=categorias) 


@app.route("/produtos/cadastrar", methods=['GET', 'POST'])
def adicionar_produtos():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        categoria = request.form['categoria']
        descricao = request.form['descricao']
        imagem=request.files.get("imagem") 
        import pdb 
        pdb.set_trace()
        
        imagem_endereco=None
        if imagem:
            filename=secure_filename(imagem.filename)
            imagem_endereco=os.path.join(UPLOAD_FOLDER, filename)
            imagem.save(imagem_endereco)
        

        url_imagem = f"/{imagem_endereco}"
        produto = Produto(nome=nome, preco=preco, categoria=categoria,descricao=descricao,imagem=url_imagem)
    

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
        
    carrinho = Carrinho.query.first()
    

    return render_template(
        'produtos.html',
        produtos = produtos,
        categorias=categorias,
        total_produtos=len(produtos), 
        produto_com_desconto=produto_com_desconto, 
        produtos_carrinho=carrinho.produtos,
        adicionar_carrinho=adicionar_carrinho)
 

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=4000)


