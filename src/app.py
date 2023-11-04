from flask import Flask, Response, redirect, render_template, request, session, url_for
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
        cad = buscar_usuario_pelo_email(session.get("email"))
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
            cad = buscar_usuario_pelo_email(session.get("email"))
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
            cad = buscar_usuario_pelo_email(session.get("email"))
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

    posts = todos_posts()

    name = ""
    email = ""
    access = check_session(session.get("email"))
    if access:
        cad = buscar_usuario_pelo_email(session.get("email"))
        if cad is not None:
            name = cad[1]
            email = cad[2]
            return render_template('blog.html', access=access, title="Home", name=name, email=email, posts=posts)
    
    return render_template('blog.html', access=False, title="Home", name=name, posts=posts)





@app.route('/proadisus')
def proadi_sus():
    '''
        Página Pradisus
    '''


    name = ""
    email = ""
    access = check_session(session.get("email"))

    if access:
        cad = buscar_usuario_pelo_email(session.get("email"))
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
        cad = buscar_usuario_pelo_email(session.get("email"))
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
        cad = buscar_usuario_pelo_email(session.get("email"))
        if cad is not None:
            name = cad[1]
            email = cad[2]
            return render_template('perfil.html', access=access, title="Home", name=name, email=email)
    
    return redirect('/login')
    



@app.route('/hospital', methods=["POST", "GET"])
def hospital():
    '''
        Página de Hositais
    '''
    if request.method == "POST":
        estado_escolhido = request.form["estado"]
        resultados = filtrar_por_estado(estado_escolhido)
        return render_template('hospital.html', access=False, title="Hospital", estado=resultados)
    else:
        resultados = filtrar_por_estado(estado_escolhido="")
        return render_template('hospital.html', access=False, title="Hospital", estado=resultados)




@app.route('/postagem', methods=["POST", "GET"])
def postagem():
    '''
        Página de Post
    '''
    

    return render_template('postagem.html')

    




@app.route('/troca_passwd', methods=["POST"])
def troca_passwd():
    '''
        Rota para trocar a senha do usuário
    '''

    user = buscar_usuario_pelo_email(session.get("email"))
    senha = user[3]
    email = user[2]
    access = check_session(session.get("email"))
    if access:
        cad = buscar_usuario_pelo_email(session.get("email"))
        if cad is not None:
            name = cad[1]
        if request.method == "POST":
            senha_atual = request.form["senha_atual"]
            nova_senha = request.form["nova_senha"]
            conf_senha = request.form["conf_nova_senha"]

            if senha_atual == senha and nova_senha == conf_senha:
                atualizando_senha(email, nova_senha)

            return render_template('perfil.html', access=access, title="Home", name=name, email=email)
            
    return redirect('/')




@app.route("/delete", methods=["POST"])
def delete():
    '''
        Rota de deletar a conta do usuário
    '''

    user = buscar_usuario_pelo_email(session.get("email"))
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
        user = buscar_usuario_pelo_email(session.get("email"))

        if imagem:
            imagem.filename = f"user_{user[0]}.png"
            image_path = os.path.join("../src/static/img/user_uploads/", imagem.filename)
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

    user = buscar_usuario_pelo_email(session.get("email"))
    email = user[2]
    img = carregando_imagem(email)

    return img

@app.route('/exibir_capa/<int:post_id>')
def exibir_capa(post_id):
    '''
        Rota para carregar capa do post
    '''
    print('Passou aqui')
    img = carregando_capa(post_id)
    return img


@app.route('/post/<categoria>/<titulo>', methods=["POST", "GET"])
def mostrar_post(categoria, titulo):
    '''
    Rota do post individual, é uma rota dinamica que renderiza o post pela categoria e titulo
    '''
    name = ""
    email = ""
    access = check_session(session.get("email"))
    posts = todos_posts()
    comentarios = todos_comentarios()
    img = None
    
    post = None
    for item in posts:
        if item[5] == categoria and item[1] == titulo:
            post = item
            break
    
    if post:        
        if access:
            cad = buscar_usuario_pelo_email(session.get("email"))
            if cad is not None:
                if request.method == 'POST':
                    comentario = request.form['comentario']
                    email = session.get("email")
                    img = carregando_imagem(cad[2])
                    post_id = item[0]
                    cria_comentario( comentario, email, post_id)
                    return redirect(url_for('mostrar_post', categoria=categoria, titulo=titulo))
                name = cad[1]
                email = cad[2]
                return render_template('postagem.html', access=access, title="post", name=name, email=email,  post=post, comentarios=comentarios, img=img)
        
        return render_template('postagem.html', access=False, title="post", name=name,  post=post)
        
    else:
        return "Post não encontrado", 404
    
    
        
    



@app.route('/post/criar_post', methods=["POST", "GET"])
def criar():
    '''
        Rota para criação de posts 
    '''

    name = ""
    email = ""
    access = check_session(session.get("email"))

    if not access:
        return redirect('/login')

    if request.method == 'POST':
        titulo = request.form['titulo']
        imagem = request.files['imagem']
        conteudo = request.form['conteudo']
        categoria = request.form['categoria']

        email = session.get("email") # Pega o email pela sessão, ou seja o autor é definido automaticamente pela sessão.

        post_id = criar_post(titulo, conteudo, email, categoria)

        if imagem:
            imagem.filename = f"post_{post_id}.png"
            image_path = os.path.join("../src/static/img/post_uploads/", imagem.filename)
            imagem.save(image_path)


        url = f'/post/{categoria}/{titulo}'

        return redirect(url)
    else:
        if access:
            cad = buscar_usuario_pelo_email(session.get("email"))
            if cad is not None:
                name = cad[1]
                email = cad[2]
                return render_template('criar_post.html', access=access, title="Criar post", name=name, email=email)
        
        return render_template('criar_post.html', access=False, title="Criar post", name=name)




@app.route('/post/todos_posts')
def mostrar_informacoes():
    '''
        Rota teste para verificar os posts enviados, podendo usar filtro
    '''

    posts = todos_posts()

    categoria_filtro = request.args.get('categoria', default=None)

    if categoria_filtro:
        posts_filtrados = [post for post in posts if post[5] == categoria_filtro]
    else:
        posts_filtrados = posts

    print(posts)

    return render_template('exibir_posts.html', posts=posts_filtrados, categoria_filtro=categoria_filtro)



if __name__ == '__main__':
    app.run(debug=True)