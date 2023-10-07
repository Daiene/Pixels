from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
     return render_template('index.html')

@app.route('/cadastro', methods = ['POST', 'GET'])
def cadastro():
    if request.method == 'GET':
        return render_template('cadastro.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/esqueceu_senha')
def esqueceu_senha():
    return render_template('esqueceu_senha.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/proadisus')
def proadi_sus():
    return render_template('proadisus.html')

@app.route('/dados')
def dados():
    return render_template('dados_nefrologia.html')

if __name__ == '__main__':
    app.run(debug=True)