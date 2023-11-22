# Importando biblioteca e arquivos
from flask import Response, request
import mysql.connector
from datetime import datetime
import cv2
from definitions import *
import csv
from werkzeug.security import check_password_hash, generate_password_hash
from email.message import EmailMessage
import ssl
import smtplib


#######################################################################################################
# Criando coisas no banco


def create_db():
    '''
        Método de criação do banco de dados
    '''

    with open('db/script.sql', 'r') as sql_file:
        sql_commands = sql_file.read().replace('\n', '').split(';')
        for command in sql_commands:
            mycursor.execute(command)

 

#######################################################################################################
# Validar informações


def check_cadastro(name, email, password, confirmPassword,  dn, cpf, parentesco, profissao, como_chegou):
    '''
        Método de validar se todas as informações do cadastro estão corretas
    '''  

    user = buscar_usuario_pelo_email(email)
    if user != None:
        warn = "Email já cadastrado!"
        return False, warn

    elif name == "" or email == "" or password == "" or confirmPassword == "" or dn == "" or cpf == "" or parentesco == "" or profissao == "" or como_chegou == "":
        warn = "Preencha todos os campos!"
        return False, warn
    
    elif len(cpf) != 11:
        warn = "CPF inválido"
        return False, warn
    
    elif password != confirmPassword:
        warn = "As senhas não estão iguais!"
        return False, warn
        
    warn=""
    return True, warn




def check_login(email, password):
    '''
        Método de de validar se as informações de login estão corretas
    '''

    user = buscar_usuario_pelo_email(email)

    if email == "" or password == "":
        warn = "Preencha todos os campos!"
        return False, warn

    elif user == None or check_password_hash(user[3], password) == False:
        warn = "Email ou Senha incorreta!"
        return False, warn
    
    elif check_email(user) == False:
        warn = "Valide seu email para logar!"
        return False, warn

    else:
        warn=""
        return True, warn
    



def check_session(session):
    '''
        Método de checar a sessão do usuário
    '''

    if session is not None:
         access = True
    else:
        access = False
    return access




def buscar_usuario_pelo_email(email):
    '''
        Método de encontrar as informações usuário pelo email
    '''

    sql = f"SELECT * FROM usuario WHERE user_email = '{email}'"
    mycursor.execute(sql)   
    user = mycursor.fetchone()
    return user



#######################################################################################################
# Usuário


def criando_usuario(name, email, password, dn, cpf, parentesco, profissao, como_chegou, status, permissao):
    '''
        Método de criar o usuário no banco
    '''

    # Imagem default
    name_default = "../src/static/img/icons/icon_user.png"
    img_default = cv2.imread(name_default)
    hash_password = generate_password_hash(password)
    sql = "INSERT INTO usuario (user_name, user_email, user_password, user_photo, user_dn, user_cpf, user_grau_parentesco, user_profissao, user_como_chegou, user_status, user_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (name, email, hash_password, name_default, dn, cpf, parentesco, profissao, como_chegou, status, permissao)
    mycursor.execute(sql, val)
    

    # Imagem com ID
    user_id = mycursor.lastrowid
    name_id = f"../src/static/img/user_uploads/user_{user_id}.png"
    cv2.imwrite(name_id, img_default)

    update_img_path = "UPDATE usuario SET user_photo = %s WHERE user_id = %s"
    mycursor.execute(update_img_path, (name_id, user_id))
    db.commit()

    user = buscar_usuario_pelo_email(email)
    if not user[-1]:
        enviando_email(user)

    print();print(f"USUARIO {user[1]} CADASTRADO COM SUCESSO!");print()




def atualizando_senha(user, senha_atual, nova_senha, conf_senha):
    '''
        Método de alterar a senha do usuário feita na pagina perfil
    '''

    usuarios = chamando_todos_usuarios()
    
    for usuario in usuarios:
        if check_password_hash(usuario[3], senha_atual):
            if nova_senha == conf_senha:
                sql = "UPDATE usuario SET user_password = %s WHERE user_email = %s"
                val = (generate_password_hash(nova_senha), user[2])
                mycursor.execute(sql, val)
                print("SENHA ALTERADA COM SUCESSO!")
                return True




def deletando_conta(email):
    '''
        Método de deletar a conta do usuário feito na pagina perfil
    '''
    print('PASSOO')
    sql = "DELETE FROM usuario WHERE user_email = %s"
    val = (email,)
    mycursor.execute(sql, val)
    print();print("CONTA DELETADA!");print()




def chamando_todos_usuarios():
    sql = "SELECT * from usuario;"
    mycursor.execute(sql)
    usuarios = mycursor.fetchall()

    return usuarios


#######################################################################################################
# Blog

def buscar_post_por_id(post_id):
    sql = f"SELECT * FROM post WHERE post_id = '{post_id}'"
    mycursor.execute(sql)   
    post = mycursor.fetchone()
    return post




def criar_post(titulo, conteudo, email, categoria):
    '''
        Método de inserir um post no banco de dados
    '''

    name_default = "../src/static/img/icons/icon_user.png"
    user = buscar_usuario_pelo_email(email)
    sql = "INSERT into post (post_title, post_content, post_date, post_img, post_category, user_id) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (titulo, conteudo, now, name_default, categoria, user[0])
    mycursor.execute(sql, val)


    post_id = mycursor.lastrowid
    name_default = f"../src/static/img/post_uploads/post_{post_id}.png"

    update_img_path = "UPDATE post SET post_img = %s WHERE post_id = %s"
    mycursor.execute(update_img_path, (name_default, post_id))
    db.commit()

    return post_id


def deleta_post(post_id):
    print('PASSOO')
    sql = "DELETE FROM post WHERE post_id = %s"
    val = (post_id,)
    mycursor.execute(sql, val)
    print();print("POST DELETADO!");print()




def cria_comentario(comentario, email, post_id):
    user = buscar_usuario_pelo_email(email)
    sql = "INSERT into comentario (com_content, com_date, post_id, user_id ) VALUES (%s, %s, %s, %s)"
    val = (comentario, now,  post_id, user[0])
    mycursor.execute(sql, val)
    db.commit()




def todos_posts_aprovados():

    # Pega todos os posts para enviar para o front-end  
    sql = "SELECT p.post_id, p.post_title, p.post_content, p.post_date, p.post_img, p.post_category, u.user_name FROM post p INNER JOIN usuario u ON p.user_id = u.user_id WHERE p.post_status = TRUE ORDER BY p.post_id DESC;"
    mycursor.execute(sql)
    posts = mycursor.fetchall()

    return posts

def todos_posts():

    # SQL para selecionar todos os posts
    sql = "SELECT * FROM post"

    # Executando a consulta para obter todos os posts
    mycursor.execute(sql)

    # Obtendo os resultados da consulta
    posts = mycursor.fetchall()

    return posts

def gerenciamento_post():

    # SQL para selecionar todos os posts
    sql = "select p.*, u.user_name as autor From post as p, usuario as u where p.user_id=u.user_id;"

    # Executando a consulta para obter todos os posts
    mycursor.execute(sql)

    # Obtendo os resultados da consulta
    posts = mycursor.fetchall()

    return posts

def posts_usuario(user_id):

    # SQL para selecionar todos os posts
    sql = f"SELECT * FROM post WHERE user_id ={user_id};"

    # Executando a consulta para obter todos os posts
    mycursor.execute(sql)

    # Obtendo os resultados da consulta
    posts = mycursor.fetchall()

    return posts


def todos_comentarios():

    # Pega todos os comentarios para enviar para o front-end  
    
    sql = "SELECT c.com_content, c.com_date, c.post_id, c.user_id, u.user_name, u.user_id, c.com_id FROM comentario c INNER JOIN usuario u ON c.user_id = u.user_id;"
    mycursor.execute(sql)
    comentarios = mycursor.fetchall()

    return comentarios


def todas_denuncias():
    sql = "SELECT * FROM comentario WHERE denunciado = TRUE"
    mycursor.execute(sql)
    denuncias = mycursor.fetchall()
    
    return denuncias


def denuncia_comentario(com_id):
    print('passou aqui')
    sql = "UPDATE comentario SET denunciado = TRUE WHERE com_id = %s"
    val = (com_id)
    mycursor.execute(sql, (val,))
    db.commit()



def deleta_comentario(com_id):
    sql = "DELETE FROM comentario WHERE com_id = %s"
    val = (com_id)
    mycursor.execute(sql, (val,))
    db.commit()


def aprovar_post(post_id):
    sql = "UPDATE post SET post_status = TRUE WHERE post_id = %s"
    val = (post_id,)  # Adicionando vírgula para criar uma tupla
    mycursor.execute(sql, val)
    db.commit()

    


#######################################################################################################
# Imagem Usuário


def carregando_imagem(email):
    '''
        Método de carregar imagem do perfil do banco
    '''

    user = buscar_usuario_pelo_email(email)
    path_img = user[5]
    img = cv2.imread(path_img)
    image_data = cv2.imencode('.png', img)[1].tobytes()

    return Response(image_data, mimetype='image/png')




def carregando_capa(post_id):
    '''
        Método de carregar imagem do perfil do banco
    '''

    post = buscar_post_por_id(post_id)
    path_img = str(post[4]).replace('b', '')
    img = cv2.imread(path_img)
    if img is not None:
        # Tente codificar a imagem em um formato diferente, por exemplo, '.jpeg'
        image_data = cv2.imencode('.jpeg', img)[1].tobytes()
        return Response(image_data, mimetype='image/jpeg')
    else:
        return "Erro ao carregar a imagem", 500


#######################################################################################################
# Hospitais

def filtrar_por_estado(estado_escolhido):
    resultados = []
    with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            if estado_escolhido:
                
                if estado_escolhido == "Selecione o Estado":
                    for row in reader:
                        resultados.append(row)
                
                else:
                    for row in reader:
                        
                        if row['Estado'] == estado_escolhido:
                            resultados.append(row)
            else:
                for row in reader:
                    resultados.append(row)
    return resultados


#######################################################################################################
# Validação de Email

def check_email(user):
    '''
        Método de chegar se o email do usuário está válido ou não
    '''
    
    sql = f"SELECT user_status FROM usuario WHERE user_id = {user[0]}"
    mycursor.execute(sql)
    status = mycursor.fetchall()
    if status[0][0] == 0:
        return False
    
    return True




def enviando_email(user):
    '''
        Método de enviar email de validação para o usuário em que cria conta
    '''

    name = user[1]
    email = user[2]
    ip = request.host.split(':')[0]
    link_unico = generate_password_hash(str(user[0]))
    subject = f'Validação de Email Rim do Amor'
    body=f'''
        Olá {name} você esta tentando criar uma conta em nossa site.
        Para isso por favor acesse o link:
        {ip}:5000/validacao/{link_unico}
    '''

    em = EmailMessage()
    em['From'] = email_send
    em['To'] = email
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_send, email_password)
        smtp.sendmail(email_password, email, em.as_string())



def validar_email(link_unico):
    '''
        Método de validar o email do usuário com o link enviado pelo email
    '''

    usuarios = chamando_todos_usuarios()

    for usuario in usuarios:
        if check_password_hash(link_unico, str(usuario[0])):
            sql = f"UPDATE usuario SET user_status=TRUE WHERE user_id={usuario[0]}"
            mycursor.execute(sql)

            return usuario[2]


#######################################################################################################
# Crinado Banco de Dados:

create_db()


print();print('BANCO DE DADOS CRIADO COM SUCESSO!');print()


#######################################################################################################
# Usuários Padroẽs

# admin
criando_usuario('admin', 'admin@admin.com', '123', '2000-10-31', '11111111111', 'pai', 'dev', 'redes_sociais', True, 1)
criando_usuario('Maria', 'maria@maria.com', '123', '2000-10-31', '11111111111', 'mae', 'dev', 'redes_sociais', True, 0)

# Post teste 

def postar6():
    sql = "INSERT INTO post (post_title, post_content, post_date, post_img, post_category, user_id, post_status) VALUES (%s, %s, %s, %s, %s, %s, TRUE)"

    post_values = [
        ("Crianças com Doença Renal Crônica: Causas e Sintomas", "A doença renal crônica em crianças é uma condição séria que afeta o funcionamento dos rins desde cedo. Neste artigo, exploramos as causas e sintomas dessa condição, bem como opções de tratamento disponíveis.", "2023-11-02", "img1.png", "relato", 1),
        ("Dicas para o Cuidado de Crianças com Doença Renal Crônica", "Cuidar de uma criança com doença renal crônica pode ser desafiador. Este guia fornece dicas úteis para pais e cuidadores sobre como proporcionar o melhor cuidado possível para essas crianças.", "2023-11-02", "img2.png", "relato", 1),
        ("A Importância da Nutrição para Crianças com Doença Renal Crônica", "A dieta desempenha um papel crucial no gerenciamento da doença renal crônica em crianças. Este artigo explora a importância da nutrição e fornece orientações sobre uma dieta saudável para essas crianças.", "2023-11-02", "img3.png", "relato", 1),
        ("Superando Desafios: Histórias Inspiradoras de Crianças com Doença Renal Crônica", "Conheça histórias inspiradoras de crianças que enfrentaram a doença renal crônica com coragem e determinação. Suas jornadas oferecem esperança e inspiração a outras famílias enfrentando desafios semelhantes.", "2023-11-02", "img4.png", "relato", 1),
        ("Recursos de Apoio para Famílias de Crianças com Doença Renal Crônica", "Navegar pela jornada da doença renal crônica em crianças pode ser avassalador. Este guia lista recursos de apoio disponíveis para famílias, incluindo grupos de apoio, organizações e informações úteis.", "2023-11-02", "img5.png", "relato", 1)
    ]

    for values in post_values:
        mycursor.execute(sql, values)

    # Commit the changes to the database
    db.commit()

postar6()