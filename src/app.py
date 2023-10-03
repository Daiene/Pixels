from flask import Flask, render_template

app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/esqueceu_senha')
def esqueceu_senha():
    return render_template('esqueceu_senha.html')

if __name__ == '__main__':
    app.run(debug=True)