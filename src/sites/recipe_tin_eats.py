from src.recipe_scrapper import RecipeScraper


class RecipeTinEats(RecipeScraper):
    def extract_recipes(self):
        receitas_html = self.soup.find_all("article")
        resposta = []
        receita_nr = 1

        for receita in receitas_html:
            titulo = receita.find("h2", {"class" : "entry-title"})

            print(titulo)

            if not titulo:
                return resposta, False

            dados = {
                'NUMERO': str(receita_nr),
                'TITULO': titulo.text.strip()
            }

            resposta.append(dados)
            receita_nr += 1

        return resposta, True

    def run(self):
        finish = True
        # Percorre as URLs procurando por receitas
        while(finish):
            # Retorna a próxima URL
            self.fetch_content()

            # self.save_html()
            # Extrai as receitas do site
            recipe_list, finish = self.extract_recipes()
            self.recipes.extend(recipe_list)


            # Segue para a próxima página      
            url_base, numero_pagina_str = self.url.split('=')
            # print(url_base)
            # print(numero_pagina_str)
            numero_pagina_int = int(numero_pagina_str) + 1
            self.url = f"{url_base}={numero_pagina_int}"
            # print(f"Próxima URL a ser pesquisada: {self.url}")

            if numero_pagina_int == 81:
                break
            
        # Salva o arquivo json
        self.save_json(self.recipes)