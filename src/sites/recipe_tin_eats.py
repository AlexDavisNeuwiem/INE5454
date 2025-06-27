from src.recipe_scrapper import RecipeScraper
from enums import URLs


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
        ingredients = []
        instructions = []

        recipe_html = self.soup.find_all("div", class_="wprm-recipe-recipe-tin-eats")

        if not recipe_html:
            return title, author, prep_time, ingredients, instructions

        title = recipe_html[0].select_one("h2", id="jump-recipes")
        try:
            title = title.text.strip()
        except:
            title = "ERROR"
        
        author = recipe_html[0].select_one("span.wprm-recipe-details.wprm-recipe-author.wprm-block-text-normal")
        try:
            author = author.text.strip()
        except:
            author = "ERROR"
            
        prep_time = recipe_html[0].select_one("span.wprm-recipe-details.wprm-recipe-details-minutes.wprm-recipe-prep_time.wprm-recipe-prep_time-minutes")
        try:
            prep_time = prep_time.text.strip()
        except:
            prep_time = "ERROR"

        grupos_de_ingredientes = recipe_html[0].select("ul", class_="wprm-recipe-ingredient-group")
        for i, grupo in enumerate(grupos_de_ingredientes):
            # Lista para guardar os ingredientes apenas DESTE grupo
            ingredientes_do_grupo = []

            itens_li = grupo.find_all('li', class_='wprm-recipe-ingredient')
            

            for item in itens_li:
                # Extrai a quantidade
                amount_tag = item.find("span", class_="wprm-recipe-ingredient-amount")
                amount = amount_tag.text.strip() if amount_tag else ""
                
                name_tag = item.find("span", class_="wprm-recipe-ingredient-name")
                name = name_tag.text.strip() if name_tag else ""
                
                # Junta tudo em uma string e adiciona à lista do grupo
                ingrediente_completo = f"{amount} {name}".strip()
                if ingrediente_completo: # Só adiciona se não estiver vazio
                    ingredientes_do_grupo.append(ingrediente_completo)

            # Adiciona a lista de ingredientes deste grupo dicionário principal
            ingredientes_do_grupo_str = ', '.join(ingredientes_do_grupo)
            if ingredientes_do_grupo_str != "":
                ingredients.append(ingredientes_do_grupo_str)
            
        grupos_de_instrucoes = recipe_html[0].select("ul", class_="wprm-recipe-instruction-group")
        for i, grupo in enumerate(grupos_de_instrucoes):
            # Lista para guardar as instruções apenas DESTE grupo
            instrucoes_do_grupo = []

            itens_li = grupo.find_all('li', class_='wprm-recipe-instruction')
            
            for item in itens_li:
                # Extrai o texto da instrução
                instruction_text_tag = item.find("div", class_="wprm-recipe-instruction-text")
                instruction_text = instruction_text_tag.text.strip() if instruction_text_tag else ""
                
                # Adiciona à lista do grupo se não estiver vazio
                if instruction_text: # Só adiciona se não estiver vazio
                    instrucoes_do_grupo.append(instruction_text)

            # Adiciona a lista de instruções deste grupo dicionário principal
            instrucoes_do_grupo_str = ', '.join(instrucoes_do_grupo)
            if instrucoes_do_grupo_str != "":
                instructions.append(instrucoes_do_grupo_str)

        return title, author, prep_time, ingredients, instructions
        
    def run(self):
        finish = True
        page_number = 0

        # Percorre as URLs procurando por receitas
        while(finish):
            # Retorna a próxima URL
            self.fetch_content()

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

            # Finaliza o webscrapping
            print(f'RTE: {page_number}')
            if page_number == URLs.PAGE_LIMIT.value:
                break
            page_number += 1
            
            # Segue para a próxima página      
            self.next_page()

            
        # Salva o arquivo json
        self.save_json(self.recipes)

    def next_page(self):   
        url_base, page_number_str = self.url.split('=')
        page_number_int = int(page_number_str) + 1
        self.url = f"{url_base}={page_number_int}"