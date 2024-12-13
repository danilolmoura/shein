from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/produtos")
def produtos():
    produtos = [
        {
            "nome": "vestido",
            "preco": 79.99,
            "categoria": "roupas",

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
        }
    ]

    return render_template('produtos.html', produtos = produtos)


if __name__ == '__main__':
    app.run(debug=True)