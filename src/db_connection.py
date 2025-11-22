import mysql.connector

def db_connection():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="felipe",        
            password="1234",
            database="Biblioteca"
        )

        if conexao.is_connected():
            return conexao

    except mysql.connector.Error as err:
        print(f"Erro ao conectar: {err}")
        return None
    
    pass

if __name__=="__main__":
    conexao = db_connection()
    if conexao:
        print("Teste concluído – conexão funcionando.")
        conexao.close()
    else:
        print("Falha na conexão.")

   