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

    user = findUserByEmail(email)
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

    user = findUserByEmail(email)

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




def findUserByEmail(email):
    '''
        Método de encontrar as informações usuário pelo email
    '''

    sql = f"SELECT * FROM usuario WHERE user_email = '{email}'"
    mycursor.execute(sql)   
    user = mycursor.fetchone()
    return user



#############################################################################################################################################################################
# Usuário


def createUser(name, email, password, dn, cpf, parentesco, profissao, como_chegou):
    '''
        Método de criar o usuário no banco
    '''

    default_img = "../src/static/img/User.png"
    
    with Image.open(default_img) as img:
        img = img.resize((128, 128))
        img_bytes = BytesIO()
        img.save(img_bytes, format='png')  # Escolha o formato apropriado
        img_bytes = img_bytes.getvalue()

    sql = "INSERT INTO usuario (user_name, user_email, user_password, user_photo, user_dn, user_cpf, user_grau_parentesco, user_profissao, user_como_chegou) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (name, email, password, img_bytes, dn, cpf, parentesco, profissao, como_chegou)
    print(val)
    print("USUARIO CADASTRADO COM SUCESSO!")
    mycursor.execute(sql, val)
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


def createPost(title, content, email, img, category):
    '''
        Método de inserir um post no banco de dados
    '''

    user = findUserByEmail(email)
    sql = "INSERT into post (post_title, post_content, post_date, post_img,post_category, user_id)"
    val = (title, content, now, img, category, user[0])



#############################################################################################################################################################################
# Imagem Usuário


def sendProfileImage(user, img):
    '''
        Método de inserrir imagem do perfil ao banco
    '''
    
    email = user[2]
    sql = "UPDATE usuario SET user_photo = %s WHERE user_email = %s"
    val = (img, email)
    mycursor.execute(sql, val) 




def getProfileImage(email):
    '''
        Método de carregar imagem do perfil do banco
    '''

    user = findUserByEmail(email)
    imagem_binaria = user[5]
    return Response(imagem_binaria, mimetype='image/png')



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