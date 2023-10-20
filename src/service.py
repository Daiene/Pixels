from flask import Response
import mysql.connector
from datetime import datetime
import cv2

db = mysql.connector.connect(
host="localhost",
user="root",
passwd="fatec",

)
mycursor = db.cursor()
now = datetime.now()


def create_db():
    with open('db/script.sql', 'r') as sql_file:
        sql_commands = sql_file.read().replace('\n', '').split(';')
        for command in sql_commands:
            mycursor.execute(command)
create_db()


def sendProfileImage(img):
    sql = "INSERT INTO usuario (user_name, user_email, user_password, user_photo) VALUES (%s, %s, %s, %s)"
    val = ("erik", "email", "123", img)
    mycursor.execute(sql, val) 
    


def getProfileImage(email):
    user = findUserByEmail(email)
    imagem_binaria = user[5]

    return Response(imagem_binaria, mimetype='image/png')


def findUserByEmail(email):
    sql = f"SELECT * FROM usuario WHERE user_email = '{email}'"
    mycursor.execute(sql)   
    user = mycursor.fetchone()
    return user




def createUser(name, email, password):

    sql = "INSERT INTO usuario (user_name, user_email, user_password) VALUES (%s, %s, %s)"
    val = (name, email, password)
    print("USUARIO CADASTRADO COM SUCESSO!")
    mycursor.execute(sql, val)
    return True




def createPost(title, content, email):
    user = findUserByEmail(email)
    sql = "INSERT into post (post_title, post_content, post_date, user_id)"
    val = (title, content, now, user[0])




def check_session(session):
    if session is not None:
         access = True
    else:
        access = False
    return access


def check_cadastro(name, email, password, confirmPassword):
    
    user = findUserByEmail(email)
    print(user)
    if user != None:
        warn = "Email já cadastrado!"
        return False, warn

    elif name == "" or email == "" or password == "" or confirmPassword == "":
        warn = "Preencha todos os campos!"
        return False, warn
    
    elif password != confirmPassword:
        warn = "As senhas não estão iguais!"
        return False, warn
    
    elif password != confirmPassword:
        warn = "Senha não confere!" 
        return False, warn
        
    warn=""
    return True, warn
    

def check_login(email, password):
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
