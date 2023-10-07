import mysql.connector
from datetime import datetime

now = datetime.now()

def create_db():
    with open('db/script.sql', 'r') as sql_file:
        sql_commands = sql_file.read().replace('\n', '').split(';')
        for command in sql_commands:
            mycursor.execute(command)


db = mysql.connector.connect(
host="localhost",
user="root",
passwd="fatec",
)

mycursor = db.cursor()
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




def dblogin(email, password):
    user = findUserByEmail(email)
    if user == None or user[3] != password:
        print('e-mail ou senha incorreta')
        return False
    print('USUARIO LOGADO COM SUCESSO!')
    return True



def createPost(title, content, email):
    user = findUserByEmail(email)
    sql = "INSERT into post (post_title, post_content, post_date, user_id)"
    val = (title, content, now, user[0])

