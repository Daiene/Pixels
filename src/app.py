from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
     return render_template('index.html')

@app.route('/cadastro', methods=['post'])
def cadastro():
    email = request.form.get['email']
    password = request.form.get['password']
    confirmPassword = request.get['confirmPassword']        

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

if __name__ == '__main__':
    app.run()