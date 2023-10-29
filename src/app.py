from flask import Flask, Response, redirect, render_template, request, session
from service import *
import numpy as np
from io import BytesIO
from PIL import Image
import os


@app.route('/')
def home():
    '''
        Página Home
    '''

    name = ""
    email = ""
    access = check_session(session.get("email"))

    if access:
        cad = buscar_email(session.get("email"))
        if cad is not None:
            name = cad[1]
            email = cad[2]
            return render_template('index.html', access=access, title="Home", name=name, email=email)
    
    return render_template('index.html', access=False, title="Home", name=name)




@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    '''
        Página Cadastro
    '''

    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        dn= request.form['dn']
        cpf = request.form['cpf']
        parentesco = request.form['parentesco']
        profissao = request.form['profissao']
        como_chegou = request.form['como_chegou']
        info, warn = check_cadastro(name, email, password, confirmPassword, dn, cpf, parentesco, profissao, como_chegou)

        if info:
            criando_usuario(name, email, password, dn, cpf, parentesco, profissao, como_chegou)
        else:
            return render_template('cadastro.html', title="Cadastro", warn=warn)
        
        session["email"] = request.form.get("email")
        return redirect("/")
    
    if request.method == 'GET':
        name = ""
        email = ""
        access = check_session(session.get("email"))

        if access:
            cad = buscar_email(session.get("email"))
            if cad is not None:
                name = cad[1]
                email = cad[2]
                return redirect("/")
        
        return render_template('cadastro.html', access=False, title="Home", name=name)




@app.route('/login', methods=['POST', 'GET'])
def login():
    '''
        Página Login
    '''
    
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
            cad = buscar_email(session.get("email"))
            if cad is not None:
                name = cad[1]
                email = cad[2]
                return render_template('index.html', access=access, title="Home", name=name, email=email)

        return render_template('login.html', access=False, title="Home", name=name)




@app.route("/logout")
def logout():
    '''
        Rota para fazer logout do usuário
    '''

    session["email"] = None
    return redirect("/")




@app.route('/esqueceu_senha')
def esqueceu_senha():
    '''
        Pagina esqueceu senha
    '''

    return render_template('esqueceu_senha.html', title="Esqueceu Senha")




@app.route('/blog')
def blog():
    '''
        Página Blog
    '''

    name = ""
    email = ""
    access = check_session(session.get("email"))
    if access:
        cad = buscar_email(session.get("email"))
        if cad is not None:
            name = cad[1]
            email = cad[2]
            return render_template('blog.html', access=access, title="Home", name=name, email=email)
    
    return render_template('blog.html', access=False, title="Home", name=name)





@app.route('/proadisus')
def proadi_sus():
    '''
        Página Pradisus
    '''


    name = ""
    email = ""
    access = check_session(session.get("email"))

    if access:
        cad = buscar_email(session.get("email"))
        if cad is not None:
            name = cad[1]
            email = cad[2]
            return render_template('proadi_sus.html', access=access, title="Home", name=name, email=email)
    
    return redirect('/login')




@app.route('/dados')
def dados():
    '''
        Página de Dados
    '''

    name = ""
    email = ""
    access = check_session(session.get("email"))

    if access:
        cad = buscar_email(session.get("email"))
        if cad is not None:
            name = cad[1]
            email = cad[2]
            return render_template('dados_nefrologia.html', access=access, title="Home", name=name, email=email)
    
    return render_template('dados_nefrologia.html', access=False, title="Home", name=name)




@app.route('/perfil')
def perfil():
    '''
        Página de Perfil
    '''

    name = ""
    email = ""
    access = check_session(session.get("email"))

    if access:
        cad = buscar_email(session.get("email"))
        if cad is not None:
            name = cad[1]
            email = cad[2]
            print(cad[5])
            return render_template('perfil.html', access=access, title="Home", name=name, email=email)
    
    return redirect('/login')
    



@app.route('/hospital')
def hospital():
    '''
        Página de Hositais
    '''

    name = ""
    email = ""
    access = check_session(session.get("email"))

    if access:
        cad = buscar_email(session.get("email"))
        if cad is not None:
            name = cad[1]
            email = cad[2]
            return render_template('hospital.html', access=access, title="Home", name=name, email=email)
    
    return render_template('hospital.html', access=False, title="Home", name=name)




@app.route('/postagem')
def postagem():
    '''
        Página de Post
    '''

    name = ""
    email = ""
    access = check_session(session.get("email"))
    
    if access:
        cad = buscar_email(session.get("email"))
        if cad is not None:
            name = cad[1]
            email = cad[2]
            return render_template('postagem.html', access=access, title="Home", name=name, email=email)
    
    return render_template('postagem.html', access=False, title="Home", name=name)




@app.route('/troca_passwd', methods=["POST"])
def troca_passwd():
    '''
        Rota para trocar a senha do usuário
    '''

    user = buscar_email(session.get("email"))
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
    '''
        Rota de deletar a conta do usuário
    '''

    user = buscar_email(session.get("email"))
    email = user[2]
    print(type(email))
    if request.method == "POST":
        deletando_conta(email)
    
    return redirect("/")




@app.route('/carregar_imagem', methods=["POST", "GET"])
def carregar_imagem():
    '''
        Rota de para definir a imagem de perfil do usuário
    '''

    if request.method == "POST":
        imagem = request.files['imagem']
        user = buscar_email(session.get("email"))

        if imagem:
            imagem.filename = f"user_{user[0]}.png"
            image_path = os.path.join("../src/static/img/uploads/", imagem.filename)
            imagem.save(image_path)

        return redirect('/perfil')
    else:
        pass
    return redirect('/perfil')




@app.route('/exibir_imagem')
def exibir_imagem():
    '''
        Rota para carregar a imagem do usuário
    '''

    user = buscar_email(session.get("email"))
    email = user[2]
    img = carregando_imagem(email)

    return img



if __name__ == '__main__':
    app.run(debug=True)