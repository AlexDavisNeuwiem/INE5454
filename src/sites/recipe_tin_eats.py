import json
import requests
from bs4 import BeautifulSoup


resposta_html = requests.get("https://www.recipetineats.com/recipes/").content

conteudo_extraido = BeautifulSoup(resposta_html, 'html.parser')

# print(conteudo_extraido.prettify())

with open("src/dados/recipe_tin_eats/conteudo_extraido_rte.html", "w") as file:
  file.write(conteudo_extraido.prettify())

receitas = conteudo_extraido.find_all("article")

resposta = []
receita_nr = 1

for receita in receitas:

  titulo = receita.find("h2", {"class" : "entry-title"})

  if not titulo:
    break

  tit = titulo.text
  # print("Título:", tit)

  dados = {'NUMERO': str(receita_nr), 'TITULO': tit}

  resposta.append(dados)
  receita_nr += 1

with open("src/dados/recipe_tin_eats/receitas_rte.json", "w") as file:
  file.write(str(json.dumps(resposta, indent=4)))