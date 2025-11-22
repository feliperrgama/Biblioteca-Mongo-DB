from mysql.connector import connect, Error
from time import sleep
from os import system
from src.loadgin_animation import loadingAnimation
from tabulate import tabulate
from src.linha_function import linha

# ==========================================
#  Função 1 – Solicitar livro
# ==========================================
def solicitar_livro(usuario_logado, user):
    system('clear')
    print("\n===== SOLICITAR LIVRO =====")
    linha(60, '-')

    try:
        with connect(
            host="localhost",
            user="felipe",
            password="1234",
            database="Biblioteca"
        ) as conexao:
            with conexao.cursor() as cursor:
                
                # Mostra os livros disponíveis
                sql_select_livro = """
                select id_book, title, autor from Livro where _status = 1
                """
                cursor.execute(sql_select_livro)
                livros = cursor.fetchall()

                dados = []
                for row in livros:
                    lista = list(row)
                    dados.append(lista)

                headers = ["ID", "Título", "Autor"]

                if not livros:
                    print("Nenhum livro disponível para empréstimo.")
                    sleep(1)
                    loadingAnimation()
                    system('clear')
                    print('Message: Voltando para a home page...')
                    loadingAnimation()
                    home_professor(user)
                else:
                    print("\nLivros disponíveis:")
                    print(tabulate(dados, headers=headers, tablefmt="fancy_grid"))

                    id_escolhido = int(input("\nDigite o ID do livro que deseja solicitar: "))
                    tupla_to_solicitation = (user, id_escolhido)
                    verification = """
                    select id_book, title, autor, publish_age from Livro where id_book = %s and _status = 1
                    """
                    # Verifica se o ID é válido e o livro está disponível
                    cursor.execute(verification, (id_escolhido,))
                    livro = cursor.fetchall()
                    data = []
                    for row1 in livro:
                        lista1 = list(row1)
                        data.append(lista1)

                    headers1 = ["ID", "Título", "Autor", "Ano de Publicação"]

                    loadingAnimation()

                    system('clear')
                    print(tabulate(data, headers=headers1, tablefmt="fancy_grid"))
                    opc = input('Deseja solicitar este livro? (s/n): ')


                    if opc == 's' or opc == 'S':
                        system('clear')
                        # Atualiza o status do livro e registra o empréstimo
                        solicitar_emprestimo = """
                        insert into Solicitacao (id_user, id_book) values (%s, %s)
                        """
                        cursor.execute(solicitar_emprestimo, tupla_to_solicitation)
                        conexao.commit()
                        print('Message: Solicitação enviada com sucesso!')
                        sleep(1)
                        loadingAnimation()
                        system('clear')
                        print('Message: Voltando para a home page...')
                        loadingAnimation()
                        home_professor(user)
                    else:
                        system('clear')
                        print("Message: ID inválido ou livro não disponível. Tente outra vez...")
                        loadingAnimation()
                        home_professor(user)
    except Error as e:
        print(f'Detalhes do erro:\n{e}\n\n')

# ==========================================
#  Função 2 – Ver lista de livros disponíveis
# ==========================================
def ver_livros_disponiveis(usuario_logado, user):
    system('clear')
    print("\n=== LISTA DE LIVROS DISPONÍVEIS ===")

    try:
        with connect(
            host="localhost",
            user="felipe",
            password="1234",
            database="Biblioteca"
        ) as conexao:
            with conexao.cursor() as cursor:
                select_lista_query = """
                select id_book, title, autor, publish_age FROM Livro WHERE _status = 1
                """
                cursor.execute(select_lista_query)
                livros = cursor.fetchall()

                dados = []
                for row in livros:
                    lista = list(row)
                    dados.append(lista)

                conexao.commit()

                headers = ["ID", "Título", "Autor", "Ano de Publicação"]

                if not livros:
                    print("Nenhum livro disponível no momento.")
                    sleep(1)
                    loadingAnimation()
                    home_professor(user)
                else:
                    # print(f"\n{'Título':<35} {'Autor':<25} {'Ano':<6} {'Categoria':<20}")
                    # print("-" * 90)
                    # for livro in livros:
                    #     print(f"{livro['titulo']:<35} {livro['autor']:<25} {livro['ano']:<6} {livro['categoria']:<20}")
                    print(tabulate(dados, headers=headers, tablefmt="fancy_grid"))

                input("\nPressione ENTER para voltar ao menu...")
                home_professor(user)
    except Error as e:
        print(f'Detalhes do erro com o banco:\n{e}\n\n')



# ==========================================
#  Função 3 – Devolver livro
# ==========================================
def devolver_livro(usuario_logado, user):
    id_user_tupla = (user,)

    system('clear') 
    print('===== DEVOLVER LIVRO =====')
    linha(50, '-')
    print('Seu(s) livro(s)')
    try:
        with connect(
            host="localhost",
            port=3306,
            username="felipe",
            password="1234",
            database="Biblioteca"
        ) as connector:
            select_table_guarda_query = """
            select 
                g.id,
                u.id_user,
                u._name,
                l.id_book,
                l.title
            from Guarda g
            join Usuario u on g.id_user = u.id_user
            join Livro l on g.id_book = l.id_book
            where u.id_user = %s
            """
            with connector.cursor() as cursor:
                cursor.execute(select_table_guarda_query, id_user_tupla)
                result = cursor.fetchall()  
                dados = []
                for row in result:
                    list_row = list(row)
                    dados.append(list_row)

                connector.commit()  
                if not dados:
                    print('Não há livros com você!')
                    sleep(2)
                    print('\nMessage: Voltando para a home page...')
                    loadingAnimation()
                    home_professor(user)
                else:
                    headers = ["ID", "ID Usuário", "Usuário", "ID Livro", "Livro"]
                    print(tabulate(dados, headers=headers, tablefmt="fancy_grid"))  
                    print('\n< 1 > Devolver livro')
                    print('< 2 > Voltar para a home page')
                    opc = int(input('-> [ ]\b\b'))  
                    if opc == 1:
                        id_book = int(input('\nDigite o id do livro que você deseja devolver: '))
                        id_book_tupla = (id_book,)  
                        loadingAnimation()
                        system('clear')
                        alert = input('Alert: Certeza que deseja devolver este livro? (s/n): ') 
                        if alert == 's' or alert == 'S':
                            delete_livro_guarda_query = """
                            delete from Guarda where id_book = %s 
                            """
                            cursor.execute(delete_livro_guarda_query, id_book_tupla)
                            livro_disponivel_query = """
                            update Livro set _status = 1 where id_book = %s
                            """
                            cursor.execute(livro_disponivel_query, id_book_tupla)
                            connector.commit()  
                            loadingAnimation()
                            system('clear')
                            print('Message: Livro devolvido com sucesso!')
                            loadingAnimation()
                            system('clear')
                            print('Message: Voltando para a página de devolução de livros...')
                            loadingAnimation()
                            devolver_livro(user, user)
                        else:
                            loadingAnimation()
                            system('clear')
                            print('Message: Voltando para a página de devolução de livros...')
                            loadingAnimation()
                            devolver_livro(user, user)   
                    elif opc == 2:
                        loadingAnimation()
                        system('clear')
                        print('Message: Voltando para a home page...')
                        loadingAnimation()
                        home_professor(user)

    except Error as e:
        print(f'Detalhes do erro no contexto do banco de dados:\n{e}\n\n')  


# ==========================================
#  HOME PAGE DO PROFESSOR
# ==========================================
def home_professor(usuario_logado):
    user = usuario_logado
    system('clear')
    print("===== HOME PAGE - PROFESSOR =====")
    linha(60, '-')
    print("< 1 > Solicitar Livros")
    print("< 2 > Ver Lista de Livros Disponíveis")
    print("< 3 > Devolver Livro")
    print("< 0 > Sair")
    opcao = input("-> [ ]\b\b")
    loadingAnimation()
    if opcao == "1":
        solicitar_livro(usuario_logado, user)
    elif opcao == "2":
        ver_livros_disponiveis(usuario_logado, user)
    elif opcao == "3":
        devolver_livro(usuario_logado, user)
    elif opcao == "0":
        system('clear')
        print("Saindo da Home Page...")
        loadingAnimation()
    else:
        print(" Opção inválida. Tente novamente.")
        sleep(1)
    pass

if __name__ == "__main__":
    home_professor()
