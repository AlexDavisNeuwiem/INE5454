from src.recipe_scrapper import RecipeScraper


class PinchOfYum(RecipeScraper):
    def extract_recipes(self):
        receitas_html = self.soup.find_all("article")
        resposta = []
        receita_nr = 1

        for receita in receitas_html:
            titulo = receita.find("h3", {
                "class": "font-domaine text-2xl normal-case tracking-normal leading-tighter text-black"
            })

            if not titulo:
                continue

            dados = {
                'NUMBER': str(receita_nr),
                'TITLE': titulo.text.strip()
            }

            resposta.append(dados)
            receita_nr += 1

        return resposta, True

    def run(self):

        # Parte Nova =============================
        finish = True
        numero_pagina_int = 1

        # Percorre as URLs procurando por receitas
        while(finish):
            # Retorna a próxima URL
            try:
                self.fetch_content()
            except:
                print(f"Página {numero_pagina_int} foi bloqueada!")
                continue

            # self.save_html()
            # Extrai as receitas do site
            recipe_list, finish = self.extract_recipes()

            # url_tmp = self.url
            # for recipe in recipe_list:
            #     title, author, prep_time, ingredients, instructions = self.extract_details(recipe['LINK'])
            #     recipe['TITLE'] = title
            #     recipe['AUTHOR'] = author
            #     recipe['PREP_TIME'] = prep_time
            #     recipe['INGREDIENTS'] = ingredients
            #     recipe['INSTRUCTIONS'] = instructions
            # self.url = url_tmp
            self.recipes.extend(recipe_list)
            print(f'POY: {numero_pagina_int}')
            
            if numero_pagina_int == 1:
                self.url += "/page/1"
                
            if numero_pagina_int == 3:
                break
            
            # Segue para a próxima página      
            url_base, numero_pagina_str = self.url.split('/page/')
            numero_pagina_int = int(numero_pagina_str) + 1
            self.url = f"{url_base}/page/{numero_pagina_int}"
            print(self.url)

            
        # Salva o arquivo json
        self.save_json(self.recipes)