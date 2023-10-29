# Importando biblioteca e arquivos
from flask import Response
import mysql.connector
from datetime import datetime
import cv2
from PIL import Image
from io import BytesIO
from definitions import *


#############################################################################################################################################################################
# Criando coisas no banco


def create_db():
    '''
        Método de criação do banco de dados
    '''

    with open('db/script.sql', 'r') as sql_file:
        sql_commands = sql_file.read().replace('\n', '').split(';')
        for command in sql_commands:
            mycursor.execute(command)

 

#############################################################################################################################################################################
# Validar informações


def check_cadastro(name, email, password, confirmPassword,  dn, cpf, parentesco, profissao, como_chegou):
    '''
        Método de validar se todas as informações do cadastro estão corretas
    '''  

    user = buscar_email(email)
    print(user)
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

    user = buscar_email(email)

    if email == "" or password == "":
        warn = "Preencha todos os campos!"
        return False, warn
        
    elif user == None or user[3] != password:
        warn = "Email ou Senha incorreta!"
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




def buscar_email(email):
    '''
        Método de encontrar as informações usuário pelo email
    '''

    sql = f"SELECT * FROM usuario WHERE user_email = '{email}'"
    mycursor.execute(sql)   
    user = mycursor.fetchone()
    return user



#############################################################################################################################################################################
# Usuário


def criando_usuario(name, email, password, dn, cpf, parentesco, profissao, como_chegou):
    '''
        Método de criar o usuário no banco
    '''

    # Imagem default
    name_default = "../src/static/img/icons/icon_user.png"
    img_default = cv2.imread(name_default)
    sql = "INSERT INTO usuario (user_name, user_email, user_password, user_photo, user_dn, user_cpf, user_grau_parentesco, user_profissao, user_como_chegou) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (name, email, password, name_default, dn, cpf, parentesco, profissao, como_chegou)
    mycursor.execute(sql, val)
    

    # Imagem com ID
    user_id = mycursor.lastrowid
    name_id = f"../src/static/img/uploads/user_{user_id}.png"
    cv2.imwrite(name_id, img_default)

    update_img_path = "UPDATE usuario SET user_photo = %s WHERE user_id = %s"
    mycursor.execute(update_img_path, (name_id, user_id))
    db.commit()

    print("USUARIO CADASTRADO COM SUCESSO!")
    
    return True




def atualizando_senha(email, nova_senha):
    '''
        Método de alterar a senha do usuário feita na pagina perfil
    '''

    sql = "UPDATE usuario SET user_password = %s WHERE user_email = %s"
    val = (nova_senha, email)
    mycursor.execute(sql, val)
    print("SENHA ALTERADA COM SUCESSO!")




def deletando_conta(email):
    '''
        Método de deletar a conta do usuário feito na pagina perfil
    '''

    sql = "DELETE FROM usuario WHERE user_email = %s"
    val = (email,)
    mycursor.execute(sql, val)
    print("CONTA DELETADA!")



#############################################################################################################################################################################
# Blog


def crir_post(title, content, email, img, category):
    '''
        Método de inserir um post no banco de dados
    '''

    user = buscar_email(email)
    sql = "INSERT into post (post_title, post_content, post_date, post_img,post_category, user_id)"
    val = (title, content, now, img, category, user[0])



#############################################################################################################################################################################
# Imagem Usuário


def carregando_imagem(email):
    '''
        Método de carregar imagem do perfil do banco
    '''

    user = buscar_email(email)
    path_img = user[5]
    img = cv2.imread(path_img)
    image_data = cv2.imencode('.png', img)[1].tobytes()

    return Response(image_data, mimetype='image/png')



#############################################################################################################################################################################
# Crinado Banco de Dados:

create_db()


print()
print('#############################################################################################################################################################################')
print()
print('BANCO DE DADOS CRIADO COM SUCESSO!')
print()
print('#############################################################################################################################################################################')
print()


#############################################################################################################################################################################
# Usuários Padroẽs

# admin
criando_usuario('admin', 'admin@admin.com', '123', '2000-10-31', '11111111111', 'pai', 'dev', 'redes_sociais')