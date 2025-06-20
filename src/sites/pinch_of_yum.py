import re
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
            link_tag = receita.find("a", class_="block md:hover:opacity-60 space-y-2")


            if link_tag:
                link = link_tag.get('href', '')
            dados = {
                'NUMBER': str(receita_nr),
                'TITLE': titulo.text.strip(),
                'LINK': link,
                'PREP_TIME': '',
                'INGREDIENTS': '',
                'INSTRUCTIONS': ''
            }

            resposta.append(dados)
            receita_nr += 1

        return resposta, True

    def extract_details(self, link):
        self.url = link
        prep_time = ''
        ingredients = []
        instructions = []
        
        try:
            self.fetch_content()
        except:
            print(f"Página {link} foi bloqueada!")
            return prep_time, ingredients, instructions
        

        recipe_html = self.soup.find_all("div", id=re.compile("^tasty-recipes-"))

        if not self.url:
            return prep_time, ingredients, instructions
        
        prep_time = recipe_html[0].select_one("span.tasty-recipes-total-time")
        try:
            prep_time = prep_time.text.strip()
        except:
            prep_time = "ERROR"

        grupos_de_ingredientes = recipe_html[0].select('div[data-tasty-recipes-customization="body-color.color"]')
        for i, grupo in enumerate(grupos_de_ingredientes):
            ingredientes_do_grupo = []
            itens_div = grupo.select('li[data-tr-ingredient-checkbox=""]')
            
            for item in itens_div:                

                ingredient_span = item.find("span", class_="tr-ingredient-checkbox-container")  

                ingredient_checkbox = ingredient_span.select('input[name^="ingredient_checkbox_"]')

                for tag in ingredient_checkbox:
                    ingredient = tag.get('aria-label')
                    if ingredient:
                        ingredientes_do_grupo.append(ingredient)
         
            if ingredientes_do_grupo:
                ingredients.append('\n'.join(ingredientes_do_grupo))
             

        # grupos_de_instrucoes = recipe_html[0].select("ul", class_="wprm-recipe-instruction-group")
        # for i, grupo in enumerate(grupos_de_instrucoes):
        #     # Lista para guardar as instruções apenas DESTE grupo
        #     instrucoes_do_grupo = []

        #     itens_li = grupo.find_all('li', class_='wprm-recipe-instruction')
            
        #     # --- Loop Interno (para cada item/linha de instrução) ---
        #     for item in itens_li:
        #         # Extrai o texto da instrução
        #         instruction_text_tag = item.find("div", class_="wprm-recipe-instruction-text")
        #         instruction_text = instruction_text_tag.text.strip() if instruction_text_tag else ""
                
        #         # Adiciona à lista do grupo se não estiver vazio
        #         if instruction_text: # Só adiciona se não estiver vazio
        #             instrucoes_do_grupo.append(instruction_text)

        #     # Adiciona a lista de instruções deste grupo ao nosso dicionário principal
        #     instrucoes_do_grupo_str = ', '.join(instrucoes_do_grupo)
        #     if instrucoes_do_grupo_str != "":
        #         instructions.append(instrucoes_do_grupo_str)

        return prep_time, ingredients, instructions
        

    def run(self):

        # Parte Nova =============================
        finish = True
        page_number = 1

        # Percorre as URLs procurando por receitas
        while(finish):
            # Retorna a próxima URL
            try:
                self.fetch_content()
            except:
                print(f"Página {page_number} foi bloqueada!")
                self.next_page(page_number)
                if page_number == 3:
                    break
                continue

            # self.save_html()
            # Extrai as receitas do site
            recipe_list, finish = self.extract_recipes()

            url_tmp = self.url
            for recipe in recipe_list:
                prep_time, ingredients, instructions = self.extract_details(recipe['LINK'])
                # recipe['TITLE'] = title
                recipe['PREP_TIME'] = prep_time
                recipe['INGREDIENTS'] = ingredients
                recipe['INSTRUCTIONS'] = instructions
            self.url = url_tmp

            self.recipes.extend(recipe_list)

            # TODO: Remover
            print(f'POY: {page_number}')    
            if page_number == 3:
                break
            
            # Segue para a próxima página      
            self.next_page(page_number)
            page_number += 1
            
        # Salva o arquivo json
        self.save_json(self.recipes)

    def next_page(self, page_number):
        if page_number == 1:
            self.url += "/page/1"
        url_base, page_number_str = self.url.split('/page/')
        page_number_int = int(page_number_str) + 1
        self.url = f"{url_base}/page/{page_number_int}"