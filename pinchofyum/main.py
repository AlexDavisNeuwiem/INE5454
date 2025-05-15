import json
import requests
from bs4 import BeautifulSoup


resposta_html = requests.get("https://pinchofyum.com/recipes/dessert").content

conteudo_extraido = BeautifulSoup(resposta_html, 'html.parser')

print(conteudo_extraido.prettify())

with open("dados/conteudo_extraido.html", "w") as file:
  file.write(conteudo_extraido.prettify())

receitas = conteudo_extraido.find_all("article")
print(receitas)

resposta = []
receita_nr = 1

for receita in receitas:

  titulo = receita.find("h3", {"class" : "font-domaine text-2xl normal-case tracking-normal leading-tighter text-black"})

  if not titulo:
    break

  tit = titulo.text
  print("Título:", tit)

  dados = {'NUMERO': str(receita_nr), 'TITULO': tit}

  resposta.append(dados)
  receita_nr += 1

with open("dados/receitas.json", "w") as file:
  file.write(str(json.dumps(resposta, indent=4)))