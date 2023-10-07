from flask import Flask, redirect, render_template, request, session
from service import *
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def home():
     return render_template('index.html')


@app.route('/cadastro', methods = ['POST', 'GET'])
def cadastro():
    if request.method == "POST":
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            confirmPassword = request.form['confirmPassword']
            createUser(name, email, password, confirmPassword)
            return render_template('index.html')
    if request.method == 'GET':
        return render_template('cadastro.html')




@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        # verifica se o login é True ou False
        login = dblogin(email, password)
        if login:
            # salva a sessao pelo email
            session["email"] = request.form.get("email")
            # redireciona para a /
            return redirect("/")
        return redirect("/login")
    if request.method == "GET":
        return render_template('login.html')




@app.route("/logout")
def logout():
    session["email"] = None
    return redirect("/")



@app.route('/esqueceu_senha')
def esqueceu_senha():
    return render_template('esqueceu_senha.html')




@app.route('/blog')
def blog():
    return render_template('blog.html')



# ROTA DE TESTE
@app.route('/proadisus')
def proadi_sus():
    # Verifica se está na sessao
    if not session.get("email"):
        return redirect("/login")
    # Pega o o email do usuario pela sessao
    userEmail = session.get("email")
    print(userEmail)
    return render_template('proadisus.html')




@app.route('/dados')
def dados():
    return render_template('dados_nefrologia.html')


if __name__ == '__main__':
    app.run(debug=True)