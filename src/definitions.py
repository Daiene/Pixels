from pathlib import Path
from flask import Flask
import mysql.connector
from datetime import datetime


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
passwd="",
)

mycursor = db.cursor()
now = datetime.now()
#############################################################################################################################################################################

# Varáveis do Flask

app = Flask(__name__)
app.secret_key = 'APIMAES'
#############################################################################################################################################################################

# Arquivos de Dados

csv_file = '/Users/kaued/OneDrive/Documentos/projetos/FATEC/API/Pixels/src/static/clinicas.csv'