import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="fatec",
  database="pixels"
)

mycursor = mydb.cursor()



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
    mycursor.execute(sql, val)

def login(email, password):
    user = findUserByEmail(email)
    if user[3] != password:
        print('Senha incorreta')
        return
    print('Usuario logado')
    
    
login('erik@gmail.com', '223')