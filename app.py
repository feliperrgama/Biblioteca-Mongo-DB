from random import randint
from tabulate import tabulate
from mysql.connector import connect, Error

jogos = {
    1: 'Outlast',
    2: 'Rayman',
    3: 'Streets of Rage',
    4: 'Need for speed',
    5: 'Ori'
}


results = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0
}

i = 1
while i <= 9604:
  position = randint(1, len(jogos))

  choose = jogos[position]

  results[position] += 1

  i += 1

print('\n\n===== Tabela das escolhas =====')

headers = ['ID', 'JOGO', 'NÚMERO DE VEZES ESCOLHIDO']

dados = []
id = 1

while id <= len(jogos):
  dados.append([id, jogos[id], results[id]])
  id += 1

print(tabulate(dados, headers=headers, tablefmt="fancy_grid"))

i = 1
soma = 0
while i <= len(results):
  soma = soma + results[i]
  i += 1
print(f'\nSoma dos valores da contagem: {soma}')


lista_from_values = []
lista_from_games = []
for value in results:
  lista = [results[value], value]
  lista_from_values.append(lista)

lista_from_values.sort()


print(f'O maior valor foi de: {lista_from_values[len(lista_from_values) - 1][0]}')
print(f'Logo, o jogo escolhido foi: {jogos[lista_from_values[len(lista_from_values) - 1][1]]}\n\n')



# Salvando o número de rodadas no banco de dados:
try:
  with connect(
    host="localhost",
    username="felipe",
    password="1234",
    port=3306,
    database="Contagem"
  ) as connector:
    query = "insert into Rodada (_name, game, chooses) values (%s, %s, %s)"
    query_select = """
    select id from Rodada;
    """
    with connector.cursor() as cursor:
        cursor.execute(query_select)
        result = cursor.fetchall()
        result_list = list(result)

    if result_list:
        i = 1
        for id in result_list:
          if i == id:
            i += 1

          else:
            with connector.cursor() as cursor:
                cursor.execute(query, ("Rodada - " + str(i), jogos[lista_from_values[len(lista_from_values) - 1][1]], lista_from_values[len(lista_from_values) - 1][0]))
                connector.commit()
    
    else:
        i = 1
        
        with connector.cursor() as cursor:
            cursor.execute(query, ("Rodada - " + str(i), jogos[lista_from_values[len(lista_from_values) - 1][1]], lista_from_values[len(lista_from_values) - 1][0]))
            connector.commit()    
    
    connector.commit()
except Error as e:
  print(f'O erro foi: {e}')

    
