from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError # Importação para tratar erros de e-mail duplicado

# --- CONEXÃO COM MONGODB ---

uri = "mongodb://felipe:1234@localhost:27017/" 
client = MongoClient(uri)
db_connection = client["Biblioteca"] 
adm_collection = db_connection["Adm"] 
user_collection = db_connection["users"] 
# -----------------------------

# FUNÇÃO PARA SALVAR NOVOS USUARIOS NO MONGODB
def salvar_novo_usuario_mongo(nome, email, senha, perfil):
    novo_usuario = {
        "nome": nome,
        "email": email,
        "senha": senha,
        "perfil": perfil
    }
    
    try:
        # Tenta inserir na coleção 'users'
        user_collection.insert_one(novo_usuario)
        return True 
    
    except DuplicateKeyError:
        # Retorna erro se o e-mail já existir (assumindo índice único)
        return "Este e-mail já está cadastrado." 
    
    except Exception as e:
        print(f"Erro ao inserir no MongoDB: {e}")
        return "Erro interno ao salvar usuário."

# Inicialização do Flask (Mantida no server_nosql.py como no seu projeto)
app = Flask(__name__)

# # ROTA PARA A TELA INICIAL DO SISTEMA
@app.route('/')
def indexPage():
    return render_template("index.html")

# # ROTA QUE DIRECIONA PARA A TELA DE LOGIN
@app.route('/login')
def loginPage():
    return render_template('login.html')

# # ROTA QUE DIRECIONA PARA A TELA DE CADASTRO (GET)
@app.route('/register')
def registerPage():
    return render_template('register.html')