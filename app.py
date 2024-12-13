from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    categorias = ["Roupas", "Feminino", "Plus Size", "Masculino", "Bebê & Maternidade", "Sapatos e Bolsas"]

    return render_template('index.html', categorias=categorias)


@app.route("/produtos/", defaults={"categoria": None})
@app.route("/produtos/<categoria>")
def produtos(categoria):
    produtos = [
        {
            "nome": "vestido",
            "preco": 79.99,
            "categoria": "Roupas",
        },
        {
            "nome": "Havaianas",
            "preco": 49.99,
            "categoria": "calçados",
        },
        {
            "nome": "Copo",
            "preco": 2.99,
            "categoria": "utensílios",
        },
        {
            "nome": "Camiseta",
            "preco": 39.99,
            "categoria": "Roupas",
        },
    ]

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