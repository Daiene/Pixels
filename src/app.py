from flask import Flask, Response, redirect, render_template, request, session
from service import *
import numpy as np
from io import BytesIO
from PIL import Image

app = Flask(__name__)

app.secret_key = 'kauegatao'


@app.route('/definir', methods=["POST", "GET"])
def definir():
    if request.method == "POST":
        imagem = request.files['imagem']
        user = findUserByEmail(session.get("email"))

        if imagem:
            with Image.open(imagem) as img:
                img = img.resize((128, 128))
                img_bytes = BytesIO()
                img.save(img_bytes, format='png')  # Escolha o formato apropriado
                img_bytes = img_bytes.getvalue()
            sendProfileImage(user, img_bytes)
    else:
        pass
    return redirect('/perfil')


@app.route('/imagem')
def exibir_imagem():
    user = findUserByEmail(session.get("email"))
    email = user[2]
    img = getProfileImage(email)

    return img


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
        
        session["email"] = request.form.get("email")
        return redirect("/")
    
    if request.method == 'GET':
        name = ""
        email = ""
        access = check_session(session.get("email"))

        if access:
            cad = findUserByEmail(session.get("email"))
            if cad is not None:
                name = cad[1]
                email = cad[2]
                return redirect("/")
        
        return render_template('cadastro.html', access=False, title="Home", name=name)




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
        name = ""
        email = ""
        access = check_session(session.get("email"))

        if access:
            cad = findUserByEmail(session.get("email"))
            if cad is not None:
                name = cad[1]
                email = cad[2]
                return render_template('index.html', access=access, title="Home", name=name, email=email)

        return render_template('login.html', access=False, title="Home", name=name)




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


@app.route('/troca_passwd', methods=["POST"])
def troca_passwd():
    user = findUserByEmail(session.get("email"))
    senha = user[3]
    email = user[2]
    if request.method == "POST":
        senha_atual = request.form["senha_atual"]
        nova_senha = request.form["nova_senha"]
        conf_senha = request.form["conf_nova_senha"]

        if senha_atual == senha and nova_senha == conf_senha:
            atualizando_senha(email, nova_senha)
    
    return redirect('/perfil')


@app.route("/delete", methods=["POST"])
def delete():
    user = findUserByEmail(session.get("email"))
    email = user[2]
    print(type(email))
    if request.method == "POST":
        deletando_conta(email)
    
    return redirect("/")
    

if __name__ == '__main__':
    app.run(debug=True)