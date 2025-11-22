from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient

uri = "mongodb://felipe:1234@localhost:27017/"
client = MongoClient(uri)
db_connection = client["Biblioteca"]
adm_collection = db_connection["Adm"]
user_collection = db_connection["Users"]

app = Flask(__name__)

# ROTA PARA A TELA INICIAL DO SISTEMA
@app.route('/')
def indexPage():
    return render_template("index.html")
# ROTA PARA A TELA INICIAL DO SISTEMA




# ROTA QUE DIRECIONA PARA A TELA DE LOGIN
@app.route('/login')
def loginPage():
    return render_template('login.html')
# ROTA QUE DIRECIONA PARA A TELA DE LOGIN



# ROTA QUE DIRECIONA PARA A TELA DE CADASTRO
@app.route('/register')
def registerPage():
    return render_template('register.html')
# ROTA QUE DIRECIONA PARA A TELA DE CADASTRO



# ROTA QUE DIRECIONA PARA A TELA DE LOGIN DO ADM
@app.route('/login_adm')
def loginAdmPage():
    return render_template('login_adm.html')
# ROTA QUE DIRECIONA PARA A TELA DE LOGIN DO ADM



# FAZENDO VERIFICAÇÃO DE LOGIN DO ADM
@app.route('/login/verification/adm', methods=['POST'])
def loginVerificationAdm():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Requisição inválida - 400 Bad Request"}), 400
    
    user = data.get("user")
    password = data.get("password")

    if not all([user, password]):
        return jsonify({"message": "Falta de informações - 400 Bad Request"}), 400
    
    
    query = {
        "user": user,
        "password": password
    }

    adm = adm_collection.find_one(query)

    if adm:
        print("\n\nLogin efetuado com sucesso!\n\n")
        return jsonify({"sucess": True, "message": "Login efetuado com sucesso"}), 200
    else:
        print("Login não foi bem sucedido")
        return jsonify({"sucess": False, "message": "Usuário não cadastrado no banco"}), 404
# FAZENDO VERIFICAÇÃO DE LOGIN DO ADM




# FAZENDO VERIFICAÇÃO DE LOGIN DO USUÁRIO
@app.route('/login/verification/user', methods=['POST'])
def loginVerificationUser():
    data = request.get_json()

    if not data:
        print('ERRO -> Sem dados de login')
        return jsonify({"message": "Não há dados do login"}), 400
    
    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        print("ERRO -> Estão faltando as informações do login!"), 401

    query = {
        "email": email,
        "password": password
    }

    user = user_collection.find_one(query)

    if user:
        print('Login bem sucedido!')
        return jsonify({"sucess": True, "message": "Login efetuado com sucesso!"}), 200
    else:
        print("Usuário não encontrado")
        return jsonify({"sucess": False, "message": "Usuário não cadastrado no banco!"}), 404









if __name__ == "__main__":
    app.run(debug=True)
