from src.recipe_scrapper import RecipeScraper

class RecipeTinEats(RecipeScraper):
    def extract_recipes(self):
        receitas_html = self.soup.find_all("article")
        resposta = []
        

        if not receitas_html:
            print("Nenhum 'article' encontrado na página. Fim da coleta.")
            return [], False


        for receita in receitas_html:
            link_tag = receita.find("a", class_="entry-title-link")

            if link_tag:
                # Extraindo o título e o link da mesma tag
                title = link_tag.text.strip()
                link = link_tag.get('href', '')

            
            self.recipes_num += 1

            dados = {
                'NUMBER': self.recipes_num,
                'TITLE': title,
                'LINK': link,
                'AUTHOR': '',
                'PREP_TIME': '',
                'INGREDIENTS': '',
                'INSTRUCTIONS': ''
            }

            resposta.append(dados)

        return resposta, True

    def extract_details(self, link):
        self.url = link + '#recipe'
        self.fetch_content()
        title = ''
        author = '' 
        prep_time = '' 
        ingredients = ''
        instructions = ''

        recipe_html = self.soup.find_all("div", class_="wprm-recipe-recipe-tin-eats")

        if not recipe_html:
            return title, author, prep_time, ingredients, instructions

        title = recipe_html[0].select_one("h2", id="jump-recipes")
        title = title.text.strip()
        
        author = recipe_html[0].select_one("span.wprm-recipe-details.wprm-recipe-author.wprm-block-text-normal")
        author = author.text.strip()
            
        return title, author, prep_time, ingredients, instructions
  
    def run(self):
        finish = True
        numero_pagina_int = 0

        # Percorre as URLs procurando por receitas
        while(finish):
            # Retorna a próxima URL
            self.fetch_content()

            # self.save_html()
            # Extrai as receitas do site
            recipe_list, finish = self.extract_recipes()

            url_tmp = self.url
            for recipe in recipe_list:
                title, author, prep_time, ingredients, instructions = self.extract_details(recipe['LINK'])
                recipe['TITLE'] = title
                recipe['AUTHOR'] = author
                recipe['PREP_TIME'] = prep_time
                recipe['INGREDIENTS'] = ingredients
                recipe['INSTRUCTIONS'] = instructions
            self.url = url_tmp

            self.recipes.extend(recipe_list)
            print(numero_pagina_int)
            
            if numero_pagina_int == 2:
                break

            
            # Segue para a próxima página      
            url_base, numero_pagina_str = self.url.split('=')
            numero_pagina_int = int(numero_pagina_str) + 1
            self.url = f"{url_base}={numero_pagina_int}"

            
        # Salva o arquivo json
        self.save_json(self.recipes)