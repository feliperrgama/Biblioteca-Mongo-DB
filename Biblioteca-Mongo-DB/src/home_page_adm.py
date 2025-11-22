from os import system
from src.linha_function import linha
from src.loadgin_animation import loadingAnimation
from mysql.connector import connect, Error
import time
import re
from tabulate import tabulate


def adm_home_page():
    system('clear')
    print('===== HOME PAGE - ADM =====')
    linha(50, '-')
    print('< 1 > Responder Solicitações')
    print('< 2 > Adicionar livros ao sistema')
    print('< 3 > Remover livros do sistema')
    print('< 4 > Ver lista de livros cadastrados no sistema')
    print('< 5 > Ver lista de livros disponíveis')
    print('< 6 > Sair')
    opc = int(input('-> [ ]\b\b'))
    loadingAnimation()
    return  opc


def switch_case(opc):
    match opc:
        case 1:
            responseRequests()
        case 2:
            addBook()
        case 3:
            removeBook()
        case 4:
            seeBooksInSistem()
        case 5:
            showBooks1()
        case 6:
            system('clear')
            print('Message: Saindo...')
            loadingAnimation()
        case _:
            print('Opção inválida!\nTente outra vez...')
            loadingAnimation()
            switch_case(adm_home_page())
    pass


def opc_more_book(string):
    string_copy = string

    system('clear')
    print(f'Deseja {string} mais um livro?')
    print('< 1 > Sim')
    print('< 2 > Não')
    opc = int(input('-> [ ]\b\b'))

    if opc == 1:
        loadingAnimation()
        if string == 'adicionar':
            addBook()
        elif string == 'remover':
            removeBook()
    elif opc == 2:
        system('clear')
        print('Message: Voltando para a home page...')
        time.sleep(2)
        loadingAnimation()
        switch_case(adm_home_page())
    else:
        print('Opção inválida, tente novamente...')
        loadingAnimation()
        opc_more_book(string_copy)
    pass



# RESPONDER SOLICITAÇÕES ================================

def responseRequests():
    system('clear')

    print('===== SOLICITAÇÕES =====')
    linha(50, '-')
    try:
        with connect(
            host="localhost",
            port=3306,
            username="felipe",
            password="1234",
            database="Biblioteca"
        ) as connector:
            select_solicitacoes_query = """
            select 
                s.id,
                u.id_user,
                u._name,
                l.id_book,
                l.title
            from Solicitacao s
            join Usuario u on s.id_user = u.id_user
            join Livro l on s.id_book = l.id_book
            """
            with connector.cursor() as cursor:
                cursor.execute(select_solicitacoes_query)
                result = cursor.fetchall()
                
                dados = []
                for row in result:
                    tupla = list(row)
                    dados.append(tupla)

                connector.commit()

                headers = ["ID", "ID Usuário", "Usuário","ID Livro", "Livro"]

                if not dados:
                    print('Não há solicitações feitas!')
                    time.sleep(1)
                    loadingAnimation()

                    system('clear')
                    print('Message: Voltando para a home page...')
                    time.sleep(1)
                    loadingAnimation()
                    switch_case(adm_home_page())
                else:
                    print(tabulate(dados, headers=headers, tablefmt="fancy_grid"))

                    id = int(input('\nDigite o id da solicitação que você deseja responder: '))
                    tupla_id = (id,)

                    loadingAnimation()

                    system('clear')

                    print('< 1 > Aceitar solicitação de empréstimo')
                    print('< 2 > Recusar solicitação de empréstimo')
                    opc = int(input('-> [ ]\b\b'))

                    time.sleep(1.5)
                    loadingAnimation()

                    if opc == 1:
                        insert_guarda_query = """
                        insert into Guarda (id_user, id_book)
                        values (%s, %s)
                        """
                        values = [tupla[1], tupla[3]]
                        cursor.execute(insert_guarda_query, values)

                        id_book_tupla = (tupla[3],)
                        update_collum_status_livro_query = """
                        update Livro set _status = 2 where id_book = %s
                        """
                        cursor.execute(update_collum_status_livro_query, id_book_tupla)

                        delete_solicitation_query = """
                        delete from Solicitacao where id = %s
                        """
                        cursor.execute(delete_solicitation_query, tupla_id)

                        connector.commit()

                        system('clear')
                        print('Message: Solicitação Aceita!')
                        time.sleep(1.5)
                        loadingAnimation()

                        system('clear')
                        resp = input('Deseja realizar responder outra solicitação? (s/n): ')

                        if resp == 's' or resp == 'S':
                            system('clear')
                            print('Message: Voltando para a página de solicitações...')
                            time.sleep(1)
                            loadingAnimation()
                            responseRequests()
                        else:
                            system('clear')
                            print('Message: Voltando para a home page...')
                            time.sleep(1)
                            loadingAnimation()
                            switch_case(adm_home_page())
                    else:
                        cursor.execute(delete_solicitation_query, tupla_id)
                        connector.commit()

                        system('clear')
                        print('Message: Solicitação Recusada!')
                        time.sleep(1.5)
                        loadingAnimation()              

                        system('clear')
                        resp = input('\n\nDeseja realizar responder outra solicitação? (s/n): ')

                        if resp == 's' or resp == 'S':
                            system('clear')
                            print('Message: Voltando para a página de solicitações...')
                            time.sleep(1)
                            loadingAnimation()
                            responseRequests()
                        else:
                            system('clear')
                            print('Message: Voltando para a home page...')
                            time.sleep(1)
                            loadingAnimation()
                            switch_case(adm_home_page())
    except Error as e:
        print(f'Detalhes do erro: \n{e}\n\n')
    
    pass


# RESPONDER SOLICITAÇÕES ================================

# ADICIONAR LIVROS ====================================
def addBook():
    system('clear')

    padrao_re = r'^\d{4}$'

    print('===== ADICIONAR LIVROS AO SISTEMA =====')
    linha(50, '-')
    title = input('Título do livro: ')
    autor = input('Autor: ')
    publish_age = int(input('Ano de publicação (AAAA): '))
    _status = int(input('Status\n< 1 > Disponível\n< 2 > Indisponível\n-> [ ]\b\b'))

    try:
        with connect(
            host="localhost",
            port=3306,
            user="felipe",
            password="1234",
            database="Biblioteca"
        ) as connector:
            add_livro_query = """
            insert into Livro(title, autor, publish_age, _status)
            values(%s, %s, %s, %s)
            """
            values = [title, autor, publish_age, _status]

            with connector.cursor() as cursor:
                cursor.execute(add_livro_query, values)
                connector.commit()
            
    except Error as e:
        print('Erro na conexão ao Banco da dados')
        print(f'Detalhes do erro:\n{e}\n\n')
        return False
    
    loadingAnimation()
        
    system('clear')

    print('Message: O livro foi adicionado com sucesso!')
        
    time.sleep(2.5)

    loadingAnimation()
    
    opc_more_book('adicionar')

    pass
# ADICIONAR LIVROS ====================================

# REMOVER LIVROS ====================================
def removeBook():
    system('clear')

    print('===== REMOVER LIVRO DO SISTEMA =====')
    linha(50, '-')
    title = input('Título do livro que deseja remover: ')
    autor = input('Autor do livro que deseja remover: ')
    publish_age = int(input('Ano de publicação do livro que deseja remover: '))

    loadingAnimation()

    try:
        with connect(
            host="localhost",
            port=3306,
            user="felipe",
            password="1234",
            database="Biblioteca"
        ) as connector:
            mostrar_livro_desejado_query = """
            select id_book, title, autor, publish_age from Livro where title = %s or autor = %s or publish_age = %s;
            """
            values = [title, autor, publish_age]

            with connector.cursor() as cursor:
                cursor.execute(mostrar_livro_desejado_query, values)
                resultado = cursor.fetchall()
                
                print()
                # print('ID\t|  Título\t|  Autor\t|  Ano de Publicação')
                # linha(70, '-')
                lista = []
                for row in resultado:
                    tupla = list(row)
                    lista.append(tupla)

                headers = ["Id", "Título", "Autor", "Ano de Publicação"]

                print(tabulate(lista, headers=headers, tablefmt="fancy_grid"))
                print()

                connector.commit()

            print('O livro que deseja remover está nesta lista?')
            print('< 1 > Sim')
            print('< 2 > Não')
            validation = int(input('-> [ ]\b\b'))
            loadingAnimation()
            print()

            if validation == 1:
                id = int(input('digite o id do livro que você deseja excluir: '))

                tupla_id = (id,)

                system('clear')
                warning = input('Alert: Certeza que deseja excluir este livro? (s/n): ')

                if warning == 's' or warning == 'S':
                    delete_book_query = """
                    delete from Livro where id_book = %s
                    """
                    with connector.cursor() as cursor:
                        cursor.execute(delete_book_query, tupla_id)
                        connector.commit()

                    loadingAnimation()
                    system('clear')

                    print('Message: O livro foi excluído com sucesso!')
                    time.sleep(2.5)

                    opc_more_book('remover')
                else:
                    system('clear')
                    print('Message: Voltando para a seleção do livro para a exclusão...')
                    loadingAnimation()
                    removeBook()
            elif validation == 2:
                system('clear')
                print('< 1 > Exluir um livro')
                print('< 2 > Voltar para a home page')
                select = int(input('-> [ ]\b\b'))

                if select == 1:
                    system('clear')
                    print('Message: Voltando para a seleção do livro para a exclusão...')
                    time.sleep(2)
                    loadingAnimation()
                    removeBook()
                elif select == 2:
                    system('clear')
                    print('Message: Voltando para a home page...')
                    time.sleep(2)
                    loadingAnimation()
                    switch_case(adm_home_page())


    except Error as e:
        print('Erro de conexão com o Banco de dados')
        print(f'Detalhe do erro:\n{e}\n\n')

    pass


#  REMOVER LIVROS ====================================



# VER LISTA DE LIRVOS CADASTRADOS NO SISTEMA =======================================

def seeBooksInSistem():
    system('clear')

    print('===== VER LIVROS CADASTRADOS =====')
    linha(60, '-')
    
    try:
        with connect(
            host="localhost",
            port=3306,
            username="felipe",
            password="1234",
            database="Biblioteca"
        ) as connector:
            see_books_query = """
            select * from Livro;
            """
            with connector.cursor() as cursor:
                cursor.execute(see_books_query)

                result = cursor.fetchall()
                dados = []

                for row in result:
                    tupla = list(row)
                    if tupla[1] == 1:
                        tupla[1] = 'Disponível'
                    elif tupla[1] == 2:
                        tupla[1] = 'Indisponível'
                    dados.append(tupla)

                headers = ["ID", "Status", "Título", "Autor", "Ano de Publicação"]

                print(tabulate(dados, headers=headers, tablefmt="fancy_grid"))

                connector.commit()

                print('\n\nDeseja remover algum desses livros?')
                print('< 1 > Sim')
                print('< 2 > Não')
                opc = int(input('-> [ ]\b\b'))

                if opc == 1:
                    id = int(input('digite o id do livro que você deseja excluir: '))
                    tupla_id = (id,)
                    loadingAnimation()

                    system('clear')
                    alert = input('Alert: Certeza que deseja remover este livro? (s/n): ')
                    loadingAnimation()

                    if alert == 's' or alert == 'S':
                        delete_book_query = """
                        delete from Livro where id_book = %s
                        """
                        cursor.execute(delete_book_query, tupla_id)
                        connector.commit()

                        system('clear')
                        print('Message: Livro removido com sucesso!')
                        time.sleep(2.5)
                        loadingAnimation()

                        seeBooksInSistem()
                    else:
                        print('\n\n< 1 > Voltar para a home page')
                        opc = int(input('-> [ ]\b\b'))

                        if opc == 1:
                            switch_case(adm_home_page())

                else:
                    system('clear')
                    print('Message: Voltando para a home page...')
                    time.sleep(2)
                    loadingAnimation()
                    switch_case(adm_home_page())

    except Error as e:
        print(f'Detalhes do erro: {e}')

    pass

# VER LISTA DE LIRVOS CADASTRADOS NO SISTEMA =======================================


# VER LISTA DE LIVROS DISPONÍVEIS ==================================================

def showBooks1():
    system('clear')
    print('===== VER LIVROS DISPONÍVEIS PARA EMPRÉSTIMO =====')
    linha(70, '-')
    
    try:
        with connect(
            host="localhost",
            username="felipe",
            port=3306,
            password="1234",
            database="Biblioteca"
        ) as connector:
            show_disponible_books_query = """
            select * from Livro;
            """
            with connector.cursor() as cursor:
                cursor.execute(show_disponible_books_query)
                result = cursor.fetchall()
    
                dados = []
    
                for row in result:
                    tupla = list(row)
                    if tupla[1] == 1:
                        tupla[1] = 'Disponível'
                        dados.append(tupla)
                    elif tupla[1] == 2:
                        tupla[1] == 'Indisponível'
                
                headers = ["ID", "Status", "Título", "Autor", "Ano de Publicação"]
    
                print(tabulate(dados, headers=headers, tablefmt="fancy_grid"))
            
            print('\n\n< 1 > Voltar para a home page')
            opc = int(input('-> [ ]\b\b'))
    
            if opc == 1:
                system('clear')
                print('Message: Voltando para a home page...')
                time.sleep(2)
                loadingAnimation()
                switch_case(adm_home_page())
    
    except Error as e:
        print(f'Detalhes do erro: {e}')

    pass


# VER LISTA DE LIVROS DISPONÍVEIS ==================================================

if __name__ == "__main__":
    switch_case(adm_home_page())
