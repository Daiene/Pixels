from flask import Flask, render_template, request
from service import *

app = Flask(__name__)



@app.route('/')
def home():
     return render_template('index.html')




@app.route('/cadastro', methods = ['POST', 'GET'])
def cadastro():
    if request.method == "POST":
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']
            confirmPassword = request.form['confirmPassword']
            createUser(name, email, password, confirmPassword)
            return render_template('index.html')
    if request.method == 'GET':
        return render_template('cadastro.html')




@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        dblogin(email, password)
        return render_template('index.html')
    if request.method == "GET":
        return render_template('login.html')




@app.route('/esqueceu_senha')
def esqueceu_senha():
    return render_template('esqueceu_senha.html')




@app.route('/blog')
def blog():
    return render_template('blog.html')




@app.route('/proadisus')
def proadi_sus():
    return render_template('proadisus.html')




if __name__ == '__main__':
    app.run(debug=True)