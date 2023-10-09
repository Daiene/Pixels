import mysql.connector
from datetime import datetime




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




def findUserByEmail(email):
    sql = f"SELECT * FROM usuario WHERE user_email = '{email}'"
    mycursor.execute(sql)   
    user = mycursor.fetchone()
    return user




def createUser(name, email, password, confirmPassword):
    user = findUserByEmail(email)
    if user:
        print("email ja cadastrado")
        return
    if password != confirmPassword:
        print("senha nao confere") 
        return
    sql = "INSERT INTO usuario (user_name, user_email, user_password) VALUES (%s, %s, %s)"
    val = (name, email, password)
    print("USUARIO CADASTRADO COM SUCESSO!")
    mycursor.execute(sql, val)




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


def check_info(page, name, email, password, confirmPassword):
    user = findUserByEmail(email)

    if page == "cadastro":
        if name == "" or email == "" or password == "" or confirmPassword == "":
            warn = "Preencha todos os campos!"
            return False, warn
        
        elif password != confirmPassword:
            warn = "As senhas não estão iguais!"
            return False, warn
        
        else:
            warn=""
            return True, warn
    
    elif page == "login":
        if email == "" or password == "":
            warn = "Preencha todos os campos!"
            return False, warn
        
        elif user == None or user[3] != password:
            warn = "Email ou Senha incorreta!"
            return False, warn
        
        else:
            warn=""
            return True, warn