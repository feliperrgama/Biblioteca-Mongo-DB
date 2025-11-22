import mysql.connector
from src.login_page import login
from src.loadgin_animation import loadingAnimation
from os import system

DB_CONFIG = {
    "host": "localhost",
    "user": "felipe",
    "password": "1234",
    "database": "Biblioteca"
}

def salvar_usuario(nome, email, senha, perfil):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Usuario (_password, _name, email) VALUES (%s, %s, %s)", (senha, nome, email))
        conn.commit()
        id_user = cursor.lastrowid
        if perfil.lower() == "aluno":
            cursor.execute("INSERT INTO Aluno (id_user) VALUES (%s)", (id_user,))
        else:
            cursor.execute("INSERT INTO Professor (id_user) VALUES (%s)", (id_user,))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Usuário {nome} cadastrado como {perfil}!")
        loadingAnimation()
        login()
    except mysql.connector.Error as err:
        print(f"❌ Erro: {err}")
    
    pass

def cadastro_terminal():
    system('clear')
    nome = input("Nome completo: ").strip()
    email = input("E-mail: ").strip()
    senha = input("Senha: ").strip()
    perfil = input("Perfil (Aluno/Professor): ").strip()
    if not nome or not email or not senha or perfil.lower() not in ["aluno","professor"]:
        print("❌ Campos inválidos!")
        return
    salvar_usuario(nome, email, senha, perfil)

    pass

if __name__ == "__main__":
    cadastro_terminal()
