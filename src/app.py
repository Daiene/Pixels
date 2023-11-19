from flask import Flask, Response, redirect, render_template, request, session, url_for
from service import *
import os

@app.route('/')
def home():
    '''
        Página Home
    '''

    name = ""
    email = ""
    permissao = False
    access = check_session(session.get("email"))

    if access:
        user = buscar_usuario_pelo_email(session.get("email"))
        if user is not None:
            name = user[1]
            email = user[2]
            permissao = user[4]


            return render_template('index.html', access=access, title="Home", name=name, email=email, permissao=permissao)
    
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
        status = False
        permissao = 0

        info, warn = check_cadastro(name, email, password, confirmPassword, dn, cpf, parentesco, profissao, como_chegou)

        if info:
            criando_usuario(name, email, password, dn, cpf, parentesco, profissao, como_chegou, status, permissao)
        else:
            return render_template('cadastro.html', title="Cadastro", warn=warn)
        
        return redirect("/validacao")
    
    if request.method == 'GET':
        name = ""
        email = ""
        permissao = False
        access = check_session(session.get("email"))

        if access:
            user = buscar_usuario_pelo_email(session.get("email"))
            if user is not None:
                name = user[1]
                email = user[2]
                permissao = user[4]
                return redirect("/")
        
        return render_template('cadastro.html', access=False, title="Home", name=name)



@app.route('/validacao')
def validacao():
    return render_template('/confirme.html')

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
        permissao = False
        access = check_session(session.get("email"))

        if access:
            user = buscar_usuario_pelo_email(session.get("email"))
            if user is not None:
                name = user[1]
                email = user[2]
                permissao = user[4]
                return render_template('index.html', access=access, title="Home", name=name, email=email, permissao=permissao)

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

    posts = todos_posts_aprovados()

    categoria_filtro = request.args.get('categoria', default=None)
    print(categoria_filtro)

    if categoria_filtro:
        posts_filtrados = [post for post in posts if post[5] == categoria_filtro]
    else:
        posts_filtrados = posts


    name = ""
    email = ""
    permissao = False
    access = check_session(session.get("email"))
    if access:
        user = buscar_usuario_pelo_email(session.get("email"))
        if user is not None:
            name = user[1]
            email = user[2]
            permissao = user[4]
            return render_template('blog.html', access=access, title="Home", name=name, email=email, posts=posts_filtrados, categoria_filtro=categoria_filtro, permissao=permissao)
    
    return render_template('blog.html', access=False, title="Home", name=name, posts=posts_filtrados, categoria_filtro=categoria_filtro)


@app.route('/aprovacoes')
def aprovacoes():

    posts = todos_posts()
    return render_template('aprovacoes.html', posts=posts)



@app.route('/atualizar_status/<int:post_id>', methods=['GET'])
def atualizar_status(post_id):
    print(post_id)
    aprovar_post(post_id)

    return redirect('/aprovacoes')




@app.route('/proadisus')
def proadi_sus():
    '''
        Página Pradisus
    '''


    name = ""
    email = ""
    permissao = False
    access = check_session(session.get("email"))

    if access:
        user = buscar_usuario_pelo_email(session.get("email"))
        if user is not None:
            name = user[1]
            email = user[2]
            permissao = user[4]
            return render_template('proadi_sus.html', access=access, title="Home", name=name, email=email, permissao=permissao)
    
    return redirect('/login')




@app.route('/dados')
def dados():
    '''
        Página de Dados
    '''

    name = ""
    email = ""
    permissao = False
    access = check_session(session.get("email"))

    if access:
        user = buscar_usuario_pelo_email(session.get("email"))
        if user is not None:
            name = user[1]
            email = user[2]
            permissao = user[4]
            return render_template('dados_nefrologia.html', access=access, title="Home", name=name, email=email, permissao=permissao)
    
    return render_template('dados_nefrologia.html', access=False, title="Home", name=name)




@app.route('/perfil')
def perfil():
    '''
        Página de Perfil
    '''

    name = ""
    email = ""
    permissao = False
    access = check_session(session.get("email"))

    if access:
        user = buscar_usuario_pelo_email(session.get("email"))
        if user is not None:
            name = user[1]
            email = user[2]
            permissao = user[4]
            return render_template('perfil.html', access=access, title="Home", name=name, email=email, permissao=permissao)
    
    return redirect('/login')
    



@app.route('/hospital', methods=["POST", "GET"])
def hospital():
    '''
        Página de Hositais
    '''
    name = ""
    email = ""
    permissao = False
    access = check_session(session.get("email"))

    if access:
        user = buscar_usuario_pelo_email(session.get("email"))
        if user == None:
            access = False
            
        if user is not None:
            name = user[1]
            email = user[2]
            permissao = user[4]
    

    if request.method == "POST":
        estado_escolhido = request.form["estado"]
        resultados = filtrar_por_estado(estado_escolhido)
        return render_template('hospital.html', access=access, name=name, email=email, title="Hospital", estado=resultados, permissao=permissao)
    else:
        resultados = filtrar_por_estado(estado_escolhido="")
        return render_template('hospital.html', access=access, name=name, email=email, title="Hospital", estado=resultados, permissao=permissao)




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

    access = check_session(session.get("email"))
    if access:
        user = buscar_usuario_pelo_email(session.get("email"))
        name = user[1]
        email = user[2]
        permissao = user[4]
        if user is not None:

            if request.method == "POST":
                senha_atual = request.form["senha_atual"]
                nova_senha = request.form["nova_senha"]
                conf_senha = request.form["conf_nova_senha"]
                
                atualizando_senha(user, senha_atual, nova_senha, conf_senha)

                return render_template('perfil.html', access=access, title="Home", name=name, email=email, permissao=permissao)
            
    return redirect('/login')




@app.route("/delete", methods=["POST"])
def delete():
    '''
        Rota de deletar a conta do usuário
    '''

    user = buscar_usuario_pelo_email(session.get("email"))
    email = user[2]
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
    posts = todos_posts_aprovados()
    comentarios = todos_comentarios()
    img = None
    
    post = None
    for item in posts:
        if item[5] == categoria and item[1] == titulo:
            post = item
            break
    
    if post:        
        if access:
            user = buscar_usuario_pelo_email(session.get("email"))
            if user is not None:
                if request.method == 'POST':
                    comentario = request.form['comentario']
                    email = session.get("email")
                    img = carregando_imagem(user[2])
                    post_id = item[0]
                    cria_comentario( comentario, email, post_id)
                    return redirect(url_for('mostrar_post', categoria=categoria, titulo=titulo))
                
                name = user[1]
                email = user[2]
                permissao = user[4]
                return render_template('postagem.html', access=access, title="post", name=name, email=email,  post=post, comentarios=comentarios, img=img, permissao=permissao)
        
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
    permissao = False
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


        return redirect('/blog')
    else:
        if access:
            user = buscar_usuario_pelo_email(session.get("email"))
            if user is not None:
                name = user[1]
                email = user[2]
                permissao = user[4]
                return render_template('criar_post.html', access=access, title="Criar post", name=name, email=email, permissao=permissao)
        
        return render_template('criar_post.html', access=False, title="Criar post", name=name)
    
@app.route('/validacao/<link_unico>')
def validacao_link(link_unico):
    email = validar_email(link_unico)
    session['email'] = email
    return redirect('/')

@app.route('/gerenciamento_post_adm')
def post_adm():
    '''
        Página de Gerenciamento de Post para Adms
    '''
    posts = gerenciamento_post()

    name = ""
    email = ""
    access = check_session(session.get("email"))

    if access:
        cad = buscar_usuario_pelo_email(session.get("email"))
        if cad is not None:
            name = cad[1]
            email = cad[2]
            return render_template('gerenciamento_post_adm.html', access=access, title="Home", name=name, email=email, posts=posts)
    
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)