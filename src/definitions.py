from pathlib import Path
from flask import Flask
import mysql.connector
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer


#############################################################################################################################################################################

# Variáveis de path

BASE_DIR = Path(__file__).resolve().parent
BASE_DIR = str(BASE_DIR).replace("C:", "")
path_uploads = "/static/img/uploads/"
#############################################################################################################################################################################

# Configurando o banco de dados
db = mysql.connector.connect(
host="localhost",
user="root",
passwd="fatec",
)

mycursor = db.cursor()
now = datetime.now()
#############################################################################################################################################################################

# Varáveis do Flask

app = Flask(__name__)
app.secret_key = 'APIMAES'
app.config['SECRET_KEY'] = 'sua_chave_secreta'
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
#############################################################################################################################################################################

# Arquivos de Dados

csv_file = 'static/clinicas.csv'
#############################################################################################################################################################################

# Configuração da conta do Email
email_send = 'pixels1dsm@gmail.com'
email_password = 'hoch orfs trqy wipw'