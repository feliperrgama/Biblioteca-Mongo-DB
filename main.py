#Menu principal content

from src.login_page import login
from src.loadgin_animation import loadingAnimation
from os import system
from src.cadastro import cadastro_terminal, salvar_usuario
import src.home_page_adm
import src.home_page_aluno
import src.home_page_professor
import src.db_connection
from src.linha_function import linha

def main_menu():
    system('clear')
    print('===== Welcome to the SGB =====')
    linha(50, '-')
    print('< 1 > Login')
    print('< 2 > Cadastro')
    opc = int(input('-> [ ]\b\b'))
    return opc

def switch_case(opc):
    match opc:
        case 1:
            system('clear')
            print('Message: Indo para a tela de login...')
            loadingAnimation()
            login()
        case 2:
            system('clear')
            print('Message: Indo para a tela de cadastro...')
            loadingAnimation()
            cadastro_terminal()
        case _:
            system('clear')
            print('Message: Opção inválida! Tente outra vez...')
            loadingAnimation()
            main_menu()
            opc = 0
    

switch_case(main_menu())
