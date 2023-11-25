from flask import redirect, render_template, request, session, url_for, flash
from service import *
import os


from itsdangerous import URLSafeTimedSerializer

# Chave secreta usada para a geração e verificação do token
SECRET_KEY = 'sua_chave_secreta'

# Salt usado para a geração e verificação do token
SALT = 'link_temporario'

# Crie o serializer com a chave secreta e o salt
serializer = URLSafeTimedSerializer(SECRET_KEY, salt=SALT)



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
        cep = request.form['cep']
        rua = request.form['logradouro']
        estado = request.form['estado'] 
        cidade = request.form['cidade']
        status = False
        permissao = 0

        info, warn = check_cadastro(name, email, password, confirmPassword, dn, cpf, parentesco, profissao, como_chegou)

        if info:
            criando_usuario(name, email, password, dn, cpf, parentesco, profissao, como_chegou, status, permissao,  cep, rua, estado, cidade)
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
            flash('Login bem-sucedido!', 'success')
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




@app.route('/esqueceu_senha', methods=['POST', 'GET'])
def esqueceu_senha():
    '''
        Pagina esqueceu senha
    '''

    if request.method == "POST":
        email = request.form['email']
        print(email)
        user = buscar_usuario_pelo_email(email)
        enviar_email_senha(user)
        
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
        posts_filtrados = [post for post in posts if post[5] == categoria_filtro and post[-1] == True]
    else:
        posts_filtrados = [post for post in posts if post[-1] == True]


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



@app.route('/atualizar_status/<int:post_id>', methods=['PUT'])
def atualizar_status(post_id):
    print(post_id)
    aprovar_post(post_id)
    print("ESTOU PASSANDO POR AQUI")
    return redirect('/gerenciamento_post_adm')



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

######################################

maes = [
    {
        'nome': 'Micielle Soares',
        'imagem_src': '../static/img/quem_somos_imgs/Imagem1.jpg',
        'alt_mae': 'foto-mãe-1',
        'desc_mae': 'Olá meu nome é Micielle Soares tenho 32 anos, casada, natural de São Paulo. Sou mãe do Romeo de 7 anos que tem doença renal crônica decorrente de Nefrite Intersticial diagnosticado com 1 ano e meio de vida. Sou enfermeira, porém me encontro fora do mercado de trabalho devido ao acompanhamento e cuidados diários do Romeo que atualmente está em Hemodiálise, porém em fila para transplante a espera de um SIM.',
    },

    {
        'nome': 'Silviane Moraes',
        'imagem_src': '../static/img/quem_somos_imgs/Imagem2.jpg',
        'alt_mae': 'foto-mãe-2',
        'desc_mae': 'Olá meu nome é Silviane Moraes, tenho 37 anos, casada, natural de São Luís – MA, atualmente há 7 anos residindo em São Paulo devido ao tratamento de hemodiálise da minha filha caçula Ana Clara de 11 anos diagnosticada com Displasia Renal Bilateral com 8 meses de vida e também mãe de Amanda Cristina de 18 anos. Estou fora do mercado de trabalho devido ao acompanhamento e cuidados diários com Ana Clara que atualmente está em hemodiálise.',
    },

    {
        'nome': 'Shirlene Giló',
        'imagem_src': '../static/img/quem_somos_imgs/Imagem3.jpg',
        'alt_mae': 'foto-mãe-3',
        'desc_mae': 'Olá, meu nome é Shirlene Giló tenho 40 anos, sou mãe da Isabel de 12 anos, Davi de 8 e Daniel de 5 aninhos, somos naturais de Alagoas, atualmente em São Paulo há 2 anos. Meu filho Davi é doente renal crônico, no momento encontra-se em hemodiálise diária, aguardando em lista de transplante renal, a espera que alguém DIGA SIM para doação de órgãos. Sou professora, Mãe atípica e típica, esposa, amiga e defensora de que acesso a saúde NÃO deve ser privilégio e SIM um direito TODOS!',
    },

    {
        'nome': 'Vandressa Santos',
        'imagem_src': '../static/img/quem_somos_imgs/Imagem4.jpg',
        'alt_mae': 'foto-mãe-4',
        'desc_mae': 'Olá, meu nome é Vandressa tenho 33 anos e sou natural de Mauá-SP porém moro em Alagoas desde 2005, onde tive três filhos: Kauana 15 anos, Ágatha 13 anos e Mateus 8 anos. Atualmente trabalho de maneira informal com empreendedorismo devido ao grande fluxo de exames ,consultas e terapias no meu dia a dia sendo mãe duplamente atípica (além da doença renal Agatha tem autismo) e ainda me divido aos cuidados das outras duas crianças, escola e afazeres domésticos.',
    },

]

@app.route('/quem_somos')
def quem_somos():
    '''
        Página Quem Somos
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


            return render_template('quem_somos.html', access=access, title="Quem Somos", name=name, email=email, permissao=permissao, maes=maes)
    
    return render_template('quem_somos.html', access=False, title="Quem Somos", name=name, maes=maes)

######################################


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
                
                if atualizando_senha(user, senha_atual, nova_senha, conf_senha):
                    flash('Sua senha foi atualizada!', 'success')
                
                return render_template('perfil.html', access=access, title="Home", name=name, email=email, permissao=permissao)
            
    return redirect('/login')




@app.route("/delete")
def delete():
    '''
        Rota de deletar a conta do usuário
    '''

    user = buscar_usuario_pelo_email(session.get("email"))
    email = user[2]
    deletando_conta(email)
    session["email"] = None

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
            flash('Sua foto foi atualizada!', 'success')
        return redirect('/perfil')
        
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
                status_post = post[-1]
                if status_post == False:
                    print(post[-2])
                    print(user[0])
                    if permissao == True or post[-2] == user[0]:
                        return render_template('postagem.html', access=access, title="post", name=name, email=email,  post=post, comentarios=comentarios, img=img, permissao=permissao, status_post=status_post)
                    else:
                        return redirect('/blog')
                else:
                    return render_template('postagem.html', access=access, title="post", name=name, email=email,  post=post, comentarios=comentarios, img=img, permissao=permissao, status_post=status_post)
                

        return render_template('postagem.html', access=False, title="post", name=name,  post=post)
        
    else:
        return render_template('link_invalido.html')
    
    
        
    



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

        email = session.get("email")

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




@app.route('/gerenciamento_post_adm', methods=["GET", "POST", "PUT", "DELETE"])
def post_adm():
    '''
        Página de Gerenciamento de Post para Adms
    '''
    posts = gerenciamento_post()
    denuncias = todas_denuncias()


    categoria_filtro = request.args.get('estado', default=None)

    if categoria_filtro:
        posts_filtrados = [post for post in posts if post[5] == int(categoria_filtro)]
    else:
        posts_filtrados = posts

    name = ""
    email = ""
    access = check_session(session.get("email"))
    
    if access:
        user = buscar_usuario_pelo_email(session.get("email"))
        if user is not None:
            if user[4] == 1:
                name = user[1]
                email = user[2]
                permissao =  user[4]
                return render_template('gerenciamento_post_adm.html', access=access, title="Home", name=name, email=email, posts=posts_filtrados, permissao=permissao, denuncias=denuncias)
            return redirect('/meus_posts')
    
    return redirect('/login')



@app.route('/meus_posts', methods=["GET", "POST", "PUT"])
def meu_post():
    '''
        Página de Gerenciamento do Usuário
    '''

    name = ""
    email = ""
    access = check_session(session.get("email"))


    if access:
        user = buscar_usuario_pelo_email(session.get("email"))
        if user is not None:
            if user[4] == 0:
                name = user[1]
                email = user[2]
                user_id =user[0]
                posts = posts_usuario(user_id) 
                return render_template('meus_posts.html', access=access, title="Home", name=name, email=email, posts=posts)
            return redirect('/gerenciamento_post_adm')
    
    return redirect('/login')


@app.route('/deletar_post/<int:post_id>', methods=['DELETE'])
def deletar_post(post_id):
    print(post_id)
    deleta_post(post_id)

    return redirect('/gerenciamento_post_adm')



@app.route('/deletar_comentario/<int:com_id>', methods=['DELETE'])
def deletar_comentario(com_id):
    print(com_id)
    deleta_comentario(com_id)
    return redirect('/gerenciamento_post_adm')




@app.route('/deletar_denuncia/<int:com_id>', methods=['PUT'])
def deletar_denuncia(com_id):
    deleta_denuncia(com_id)

    return redirect('/gerenciamento_post_adm')




@app.route('/denunciar/<categoria>/<titulo>/<int:com_id>', methods=['POST'])
def denunciar_comentario(com_id, categoria, titulo):
    print('chamou')
    denuncia_comentario(com_id)


    return redirect(f'/post/{categoria}/{titulo}')


@app.route('/redefinir_senha/<token>', methods=['POST','GET'])
def esqueceu_senha_redefinir(token):

    try:
        if token in tokens_invalidos:
            try:
                serializer.loads(token, salt='link_temporario', max_age=60)
            except:
                tokens_invalidos.remove(token)
            return render_template('link_invalido.html')
        
        
        email = serializer.loads(token, salt='link_temporario', max_age=60)
        
        print(email)
        session['email'] = email
        user = buscar_usuario_pelo_email(email)
    
        
        if request.method == "POST":
            nova_senha = request.form["nova_senha"]
            conf_senha = request.form["conf_nova_senha"]

            if redefinir_senha(user,nova_senha, conf_senha):
                session['email'] = None
                tokens_invalidos.add(token)

                return redirect('/login')


        if request.method == "GET":

            return render_template('redefinir_senha.html', token=token)
    except:
        return render_template('link_invalido.html')





if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)