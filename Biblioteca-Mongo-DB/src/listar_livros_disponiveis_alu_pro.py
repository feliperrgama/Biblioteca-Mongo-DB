import mysql.connector

def listar_livros_disponiveis(usuario_logado):
    """
    Exibe todos os livros disponíveis para empréstimo.
    Acesso permitido apenas para usuários dos perfis Aluno e Professor.
    """

    #  Verifica se o usuário tem permissão
    if usuario_logado['perfil'] not in ('Aluno', 'Professor'):
        print(" Acesso negado. Esta funcionalidade é exclusiva para Alunos e Professores.")
        return

    try:
        # ⚙️ Conexão com o banco de dados
        conexao = mysql.connector.connect(
            host="",
            user="",           
            password="",  
            database="Biblioteca20"
        )

        cursor = conexao.cursor(dictionary=True)

        #  Consulta SQL: apenas livros com status 'Disponível'
        consulta = """
        SELECT 
            titulo,
            autor,
            ano,
            categoria,
            status
        FROM Livro
        WHERE status = 'Disponível';
        """

        cursor.execute(consulta)
        livros = cursor.fetchall()

        # 🧾 Exibição formatada
        print("\n LIVROS DISPONÍVEIS PARA EMPRÉSTIMO \n")
        print(f"{'Título':<35} {'Autor':<25} {'Ano':<6} {'Categoria':<20} {'Status':<12}")
        print("-" * 100)

        if not livros:
            print("Nenhum livro disponível para empréstimo no momento.")
        else:
            for livro in livros:
                print(f"{livro['titulo']:<35} {livro['autor']:<25} {livro['ano']:<6} {livro['categoria']:<20} {livro['status']:<12}")

    except mysql.connector.Error as erro:
        print(f"Erro ao acessar o banco de dados: {erro}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conexao' in locals() and conexao.is_connected():
            conexao.close()


# ==============================
#  SIMULAÇÃO DE LOGIN 
# ==============================
usuario_logado = {
    "id_user": 3,
    "nome": "Carlos",
    "perfil": "Aluno"  # Altere para "Professor" ou "Administrador" para testar o acesso
}

#  Executar a funcionalidade
listar_livros_disponiveis(usuario_logado)

