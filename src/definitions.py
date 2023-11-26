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
passwd="",
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
tokens_invalidos = set()
#############################################################################################################################################################################

maes = [
    {
        'nome': 'Micielle Soares',
        'imagem_src': '../static/img/quem_somos_imgs/Imagem1.jpg',
        'alt_mae': 'foto-mãe-1',
        'desc_mae': 'Olá meu nome é Micielle Soares tenho 32 anos, casada, natural de São Paulo. Sou mãe do Romeo de 7 anos que tem doença renal crônica decorrente de Nefrite Intersticial diagnosticado com 1 ano e meio de vida. Sou enfermeira, porém me encontro fora do mercado de trabalho devido ao acompanhamento e cuidados diários do Romeo que atualmente está em Hemodiálise, porém em fila para transplante a espera de um SIM.',
    },

    {
        'nome': 'Silviane Moraes',
        'imagem_src': '../static/img/quem_somos_imgs/Imagem2.jpg',
        'alt_mae': 'foto-mãe-2',
        'desc_mae': 'Olá meu nome é Silviane Moraes, tenho 37 anos, casada, natural de São Luís – MA, atualmente há 7 anos residindo em São Paulo devido ao tratamento de hemodiálise da minha filha caçula Ana Clara de 11 anos diagnosticada com Displasia Renal Bilateral com 8 meses de vida e também mãe de Amanda Cristina de 18 anos. Estou fora do mercado de trabalho devido ao acompanhamento e cuidados diários com Ana Clara que atualmente está em hemodiálise.',
    },

    {
        'nome': 'Shirlene Giló',
        'imagem_src': '../static/img/quem_somos_imgs/Imagem3.jpg',
        'alt_mae': 'foto-mãe-3',
        'desc_mae': 'Olá, meu nome é Shirlene Giló tenho 40 anos, sou mãe da Isabel de 12 anos, Davi de 8 e Daniel de 5 aninhos, somos naturais de Alagoas, atualmente em São Paulo há 2 anos. Meu filho Davi é doente renal crônico, no momento encontra-se em hemodiálise diária, aguardando em lista de transplante renal, a espera que alguém DIGA SIM para doação de órgãos. Sou professora, Mãe atípica e típica, esposa, amiga e defensora de que acesso a saúde NÃO deve ser privilégio e SIM um direito TODOS!',
    },

    {
        'nome': 'Vandressa Santos',
        'imagem_src': '../static/img/quem_somos_imgs/Imagem4.jpg',
        'alt_mae': 'foto-mãe-4',
        'desc_mae': 'Olá, meu nome é Vandressa tenho 33 anos e sou natural de Mauá-SP porém moro em Alagoas desde 2005, onde tive três filhos: Kauana 15 anos, Ágatha 13 anos e Mateus 8 anos. Atualmente trabalho de maneira informal com empreendedorismo devido ao grande fluxo de exames ,consultas e terapias no meu dia a dia sendo mãe duplamente atípica (além da doença renal Agatha tem autismo) e ainda me divido aos cuidados das outras duas crianças, escola e afazeres domésticos.',
    },

]