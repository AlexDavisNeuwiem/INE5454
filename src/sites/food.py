import json
import requests
from bs4 import BeautifulSoup


# resposta_html = requests.get("https://www.food.com/recipe?ref=nav").content
resposta_html = requests.get("https://www.food.com/ideas/easy-lunch-recipes-7007?ref=nav#c-821312").content

conteudo_extraido = BeautifulSoup(resposta_html, 'html.parser')

# print(conteudo_extraido.prettify())

with open("src/dados/food/conteudo_extraido_food.html", "w") as file:
  file.write(conteudo_extraido.prettify())

receitas = conteudo_extraido.find_all("div", {"class" : "smart-info-wrap"})

print(receitas)
resposta = []
receita_nr = 1

# Este loop faz o scraping do titulo da pagina da receita em especifico
# Sera refatorado para posibilitar extrair outros dados especificos da receita
for receita in receitas:
  titulo = receita.find("h2", {"class" : "title"})
  
  tit = titulo.text
  print("Título:", tit)
#   print("....")

  dados = {'NUMERO': str(receita_nr), 'TITULO': tit}

  resposta.append(dados)
  receita_nr += 1

with open("src/dados/food/receitas_food.json", "w") as file:
  file.write(str(json.dumps(resposta, indent=4)))
