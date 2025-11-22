from loading_animation import loadingAnimation
from time import sleep
from mysql.connector import connect, Error
from os import system
from linha_function import linha
from tabulate import tabulate

def devolverLivro(id_user):
    id_user_tupla = (id_user,)

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
                    #VOLTAR PARA A HOME PAGE AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
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
                            devolverLivro(1) #COLOCAR ID AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
                        else:
                            loadingAnimation()
                            system('clear')
                            print('Message: Voltando para a página de devolução de livros...')
                            loadingAnimation()
                            devolverLivro(1) #COLOCAR AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII

                    elif opc == 2:
                        loadingAnimation()
                        system('clear')
                        print('Messgae: Voltando para a home page...')
                        #voltar para a home page do usuário aquiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
                    
    except Error as e:
        print(f'Detalhes do erro no contexto do banco de dados:\n{e}\n\n')

devolverLivro(1)