from flask import Flask, redirect, render_template, request, session
from service import *
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
def home():
        name=""
        access=check_session(session["email"])
        if access == True:
            name = findUserByEmail(session["email"])
            if name is not None:
                name=name[1]
            return render_template('index.html', access=access, title="Home", name=name)
        else:
            return render_template('index.html', access=access, title="Home", name=name)




@app.route('/cadastro', methods = ['POST', 'GET'])
def cadastro():
    if request.method == "POST":
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            confirmPassword = request.form['confirmPassword']
            info, warn = check_cadastro(name, email, password, confirmPassword)
            if info == True:
                createUser(name, email, password)
            else:
                return render_template('cadastro.html', title="Cadastro", warn=warn)
            return redirect('/login')
    if request.method == 'GET':
        return render_template('cadastro.html', title="Cadastro", warn="")




@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        info, warn = check_login(email, password)
        if info:
            session["email"] = request.form.get("email")
            return redirect("/")
        return render_template("login.html", warn=warn)
    if request.method == "GET":
        return render_template('login.html', title="Login")




@app.route("/logout")
def logout():
    session["email"] = None
    return redirect("/")




@app.route('/esqueceu_senha')
def esqueceu_senha():
    return render_template('esqueceu_senha.html', title="Esqueceu Senha")




@app.route('/blog')
def blog():
    name = ""
    access=check_session( session["email"])
    name = findUserByEmail(session["email"])
    if name is not None:
        name = name[1]
    return render_template('blog.html', access=access, title="Blog", name=name)




# ROTA DE TESTE
@app.route('/proadisus')
def proadi_sus():
    access=check_session( session["email"])
    if access == False:
        return redirect('/login')
    else:
        return render_template('proadisus.html', access=access, title="ProadiSUS")




@app.route('/dados')
def dados():
    access=check_session( session["email"])
    return render_template('dados_nefrologia.html', access=access, title="Dados")



def main():
    session["email"] = None
    app.run(debug=True)



@app.route('/perfil')
def perfil():
    access=check_session(session["email"])
    if access == False:
        return redirect('/login')
    else:
        name = findUserByEmail(session["email"])
        if name is not None:
            name = name[1]
        return render_template('perfil.html', access=access, title="Perfil", name=name)



if __name__ == '__main__':
    main()