from flask import Flask, redirect, render_template, request, session
from service import *

app = Flask(__name__)
app.secret_key = 'kauegatao'

@app.route('/')
def home():

    name = ""
    email = ""
    access = check_session(session.get("email"))

    if access:
        cad = findUserByEmail(session.get("email"))
        if cad is not None:
            name = cad[1]
            email = cad[2]
            return render_template('index.html', access=access, title="Home", name=name, email=email)
    
    return render_template('index.html', access=False, title="Home", name=name)


@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():

    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        info, warn = check_cadastro(name, email, password, confirmPassword)

        if info:
            createUser(name, email, password)
        else:
            return render_template('cadastro.html', title="Cadastro", warn=warn)
        return redirect('/login')
    
    if request.method == 'GET':
        return render_template('cadastro.html', title="Cadastro", warn="")



@app.route('/login', methods=['POST', 'GET'])
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
    email = ""
    access = check_session(session.get("email"))
    if access:
        cad = findUserByEmail(session.get("email"))
        if cad is not None:
            name = cad[1]
            email = cad[2]
            return render_template('blog.html', access=access, title="Home", name=name, email=email)
    
    return render_template('blog.html', access=False, title="Home", name=name)




# ROTA DE TESTE
@app.route('/proadisus')
def proadi_sus():

    name = ""
    email = ""
    access = check_session(session.get("email"))

    if access:
        cad = findUserByEmail(session.get("email"))
        if cad is not None:
            name = cad[1]
            email = cad[2]
            return render_template('proadi_sus.html', access=access, title="Home", name=name, email=email)
    
    return redirect('/login')




@app.route('/dados')
def dados():
    name = ""
    email = ""
    access = check_session(session.get("email"))

    if access:
        cad = findUserByEmail(session.get("email"))
        if cad is not None:
            name = cad[1]
            email = cad[2]
            return render_template('dados_nefrologia.html', access=access, title="Home", name=name, email=email)
    
    return render_template('dados_nefrologia.html', access=False, title="Home", name=name)




@app.route('/perfil')
def perfil():
    name = ""
    email = ""
    access = check_session(session.get("email"))

    if access:
        cad = findUserByEmail(session.get("email"))
        if cad is not None:
            name = cad[1]
            email = cad[2]
            return render_template('perfil.html', access=access, title="Home", name=name, email=email)
    
    return redirect('/login')
    


@app.route('/hospital')
def hospital():
    name = ""
    email = ""
    access = check_session(session.get("email"))

    if access:
        cad = findUserByEmail(session.get("email"))
        if cad is not None:
            name = cad[1]
            email = cad[2]
            return render_template('hospital.html', access=access, title="Home", name=name, email=email)
    
    return render_template('hospital.html', access=False, title="Home", name=name)



@app.route('/postagem')
def postagem():
    name = ""
    email = ""
    access = check_session(session.get("email"))
    
    if access:
        cad = findUserByEmail(session.get("email"))
        if cad is not None:
            name = cad[1]
            email = cad[2]
            return render_template('postagem.html', access=access, title="Home", name=name, email=email)
    
    return render_template('postagem.html', access=False, title="Home", name=name)



if __name__ == '__main__':
    app.run(debug=True)