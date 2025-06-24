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





        instruction_group = recipe_html[0].select("div", class_= "tasty-recipes-instructions")
        # print(f'INSTRUCTION GROUP: {instruction_group}')
        for i, grupo in enumerate(instruction_group):
            grupos_de_instrucoes = []
            instruction_div = grupo.select("li", id=re.compile("^instruction-step-"))

            for instruction_item in instruction_div:
                # print(f'INSTRUCTION ITEM: {instruction_item.text.strip()}')

                grupos_de_instrucoes.append(instruction_item.get_text(strip=True))
         
            if grupos_de_instrucoes:
                instructions.append(grupos_de_instrucoes)

        return prep_time, ingredients, instructions[4]
        

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
                self.next_page()
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
            self.next_page()
            page_number += 1
            
        # Salva o arquivo json
        self.save_json(self.recipes)

    def next_page(self):
        if "/page/" not in self.url:
            self.url += "/page/1"
        url_base, page_number_str = self.url.split('/page/')
        page_number_int = int(page_number_str) + 1
        self.url = f"{url_base}/page/{page_number_int}"