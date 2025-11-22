from flask import Flask, render_template, request, jsonify
from mysql.connector import connect, Error

app = Flask(__name__) # Recomendação da documentação

# 1 - Criar a 1ª página do site
# toda página tem um route e uma função
# route -> O caminho que vem depois do meu domínio ex: youtube.com/route, route = usuarios. Qual link vai abrir qual página
# função -> O que eu quero exibir em tal route.
# template -> front

#decorator -> uma linha de código que atribui uma nova funcionalidade para a a função que vem logo em baixo dela.
# @app.route('/') 
# def homepage():
#     return render_template("index.html")


@app.route('/login')
def login():
    return render_template("/src-front/login.html")


@app.route('/login_adm')
def loginAMD():
    return render_template('//src-front/login.html')



@app.route('/login_verification', methods = ['POST'])
def loginVerification():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Requisição inválida'}), 400
    
    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return jsonify({'message': "Estão faltando campos obrigatórios"}), 400
    
    try:
        with connect(
            host="localhost",
            user="felipe",
            password="1234",
            database="Biblioteca"
        ) as connector:
            with connector.cursor() as cursor:
                select_from_Usuario_query = """
                select email, _password, _name from Usuario where email = %s and _password = %s
                """
                cursor.execute(select_from_Usuario_query, (email, password))
                result = cursor.fetchone()

                connector.commit()

                dados = list(result)

                print(f'email: {dados[0]} | password: {dados[1]}')

                if dados[0] and dados[1]:
                    return jsonify({
                        'message': 'Login efetuado com sucesso!',
                        'username': dados[2]
                    }), 200
                
                if not dados[0] and dados[1]:
                    return jsonify({'message': 'Usuário inexistente!'}), 401



    except Error as err:
        print(f'[ERROR] Erro: {err}')
        return jsonify({'message': 'Erro interno'}), 500




@app.route('/register')
def register():
    return render_template('/src-front/register.html')



@app.route('/registrar_user', methods = ['POST'])
def registrar():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Requisição inválida'}), 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    select = data.get('select')

    if not all([username, email, password, select]):
        return jsonify({'message': 'Estão faltando campos obrigatórios'}), 400
    
    try:
        with connect(
            host="localhost",
            user="felipe",
            password="1234",
            database="Biblioteca"
        ) as connector:
            register_user_query = """
            insert into Usuario (_name, email, _password) values (%s, %s, %s)
            """
            with connector.cursor() as cursor:
                cursor.execute(register_user_query, (username, email, password))

                connector.commit()

                cursor.execute("SELECT LAST_INSERT_ID()")
                id = cursor.fetchone()[0]
                
                if select == '1':
                    register_aluno_query = """
                    insert into Aluno (id_user) values (%s) 
                    """
                    cursor.execute(register_aluno_query, (id, ))
                elif select == '2':
                    register_prof_query = """
                    insert into Professor (id_user) values (%s) 
                    """
                    cursor.execute(register_prof_query, (id, ))
                
                connector.commit()

                return jsonify({"message": "Usuário cadastrado com sucesso"}), 201

    except Error as err:
        print(f'Erro em relação ao banco de dados:\n{err}\n\n')
        return jsonify({"message": "Erro interno"})




@app.route('/usuarios/<nome_do_usuario>')
def users(nome_do_usuario):
    username = request.get_data()
    return render_template("/src-front/home_page_user.html", nome_do_usuario=nome_do_usuario)
    



@app.route('/solicitar_livros_user')
def solicitarLivros():
    return render_template("/src-front/solicitar_livros.html")


@app.route('/solicitar', methods=['POST'])
def solicitacao():
    print("📩 Requisição recebida:", request.data)
    print("📩 Content-Type:", request.content_type)
    dados = request.get_json(silent=True)
    print("📦 Dados parseados:", dados)

    if not dados:
        return jsonify({'message': 'Requisição inválida'}), 400
    
    id_book = dados.get('id_book')
    email = dados.get('email')
    
    if not all([id_book, email]):
        return jsonify({'message': 'Faltam valores obrigatórios'}), 400
    
    try:
        with connect(
            host="localhost",
            user="felipe",
            password="1234",
            database="Biblioteca"
        ) as connector:
            with connector.cursor() as cursor:
                select_user_query = """
                select id_user from Usuario where email = %s
                """
                cursor.execute(select_user_query, (email, ))
                tupla_id_user = cursor.fetchone()

                if not tupla_id_user:
                    return jsonify({'message': 'Usuário não encontrado!'}), 404

                id_user = list(tupla_id_user)

                insert_solicitacao_query = """
                insert into Solicitacao (id_book, id_user) values (%s, %s)
                """
                values = (id_book, id_user[0])
                cursor.execute(insert_solicitacao_query, values)
                print("[LOG] Adicionado com sucesso!")
                connector.commit()

                return jsonify({'message': 'Solicitação feita com sucesso!', 'user': id_user}), 200

    except Error as err:
        print(f'[ERRO] {err}')
        return jsonify({'message': 'erro ao conectar com o server'}), 500



@app.route('/filter_table_livros', methods=['POST'])
def filtragem():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'Requisição inválida'}), 401
    
    title = data.get("title")

    try:
        with connect(
            host="localhost",
            user="felipe",
            password="1234",
            database="Biblioteca"
        ) as connector:
            with connector.cursor(dictionary=True) as cursor:
                select_livro_filter_query = """
                select * from Livro where title like %s
                """

                cursor.execute(select_livro_filter_query, (f"%{title}%", ))
                result = cursor.fetchall()

                return jsonify(result), 200


    except Error as err:
        print('Erro ao conectar com o banco de dados')
        return jsonify({'message': 'Erro com o servidor'}), 500


@app.route('/table_livros')
def tabela():
    try:
        with connect(
            host="localhost",
            user="felipe",
            password="1234",
            database="Biblioteca"
        ) as connector:
            with connector.cursor(dictionary=True) as cursor:
                select_livros_query = """
                select id_book, _status, autor, title, publish_age from Livro
                """
                cursor.execute(select_livros_query)
                result = cursor.fetchall()

                connector.commit()

                return jsonify(result), 200

    except Error as err:    
        print('[ERRO] Erro ao tentar buscar os livros')
        print(f'Error: {err}')
        return jsonify({'message': 'Erro interno no servidor'}), 500


# @app.route('/livro_user')
# def livrosUser():
#     data = request.get_json()

#     if not data:
#         print('[ERRO] Requisição inválida')
#         return jsonify({'message': 'Requisição inválida'}), 400

#     email = data.get("email")

#     try:
#         with connect(
#             host="localhost",
#             user="felipe",
#             password="1234",
#             database="Biblioteca"
#         ) as connector:
#             with connector.cursor() as cursor:
#                 select_livros_users_query = """
#                 select * from Livro where email = 
#                 """
#     except Error as err:
#         print(f'[ERRO]\n!!!!!!!!!!! {err} !!!!!!!!!!\n')
#         return jsonify({'message': 'Erro de conexão com o Banco de dados'})

@app.route('/livros_disponiveis')
def livrosDisponiveis():
    return render_template("/src-front/livros_disponiveis.html")

@app.route('/livros_adm')
def livrosAMD():
    return render_template("/src-front/livros_cadastrados_adm.html")


@app.route('/devolver_livro')
def devolver():
    return render_template("/src-front/devolver_livro.html")



@app.route('/<string:nome>')
def error(nome):
    return f'Página ({nome}) não encontrada!'



# Colocar site no ar
if __name__ == "__main__":
    app.run(debug = True)



