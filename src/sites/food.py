from src.recipe_scrapper import RecipeScraper
from enums import URLs
import json


class Food(RecipeScraper):
    def extract_recipes(self):
        receitas_html = self.soup.select_one('script[type="application/ld+json"]')
        
        resposta = []
      
        if not receitas_html:
            print("Tag não encontrada. Fim da coleta.")
            return [], False

        for receita in receitas_html:
            data = json.loads(receita)
            items = data.get('itemListElement', [])
            for item in items:
                url = item.get('url')
                if url:
                    resposta.append(url)
        return resposta, True

    def extract_details(self, link):
        self.url = link
        self.fetch_content()

        result = {
            'TITLE': '',
            'LINK': link,
            'AUTHOR': '',
            'PREP_TIME': '',
            'INGREDIENTS': [],
            'INSTRUCTIONS': []
        }

        recipe_html = self.soup.find_all("div", class_="current-recipe")

        title= recipe_html[0].select_one("h1", class_="svelte-1muv3s8")
        result['TITLE'] = title.text.strip()

        author_div = recipe_html[0].find("div", class_="byline svelte-176rmbi")
        author = author_div.select_one("a", class_="svelte-176rmbi")
        result['AUTHOR'] = author.text.strip()

        prep = recipe_html[0].select_one("dd", class_="facts__value svelte-ar8gac")
        result['PREP_TIME'] = prep.text.strip()

        ingr_section = recipe_html[0].select_one("section", class_="layout__item ingredients svelte-ar8gac")
        ingredients = []
        quantity = []

       
        ingr_text = ingr_section.find_all("span", class_="ingredient-text svelte-ar8gac")
        ingr_quant = ingr_section.find_all("span", class_="ingredient-quantity svelte-ar8gac")

        for ingredient_text in ingr_text:
            ingredients.append(ingredient_text.text.strip())

        for ingredient_quantity in ingr_quant:
            quantity.append(ingredient_quantity.text.strip())

        for i in range(len(ingredients)):
            result['INGREDIENTS'].append(quantity[i] + ' ' + ingredients[i])
        
        inst = recipe_html[0].find_all("ul", class_="direction-list svelte-ar8gac")
        instructions = []
        
        
        for instruction_text in inst:
            instructions.append(instruction_text.text.strip().replace('.', '.\n'))
    
        result['INSTRUCTIONS'] = instructions

        return result


    def run(self):
            finish = True
            page_number = 0

            # Percorre as URLs procurando por receitas
            while(finish):
                # Retorna a próxima URL
                self.fetch_content()

                # Extrai as receitas do site
                url_tmp = self.url
                recipe_list, finish = self.extract_recipes()

                for link in recipe_list:
                    recipe = self.extract_details(link)
                    self.recipes.append(recipe)
                
                self.url = url_tmp

                # Finaliza o webscrapping
                print(f'FOOD: {page_number}')   
                if page_number == URLs.PAGE_LIMIT.value:
                    break
                page_number += 1

                # Segue para a próxima página      
                self.next_page()

                
            # Salva o arquivo json
            self.save_json(self.recipes)

    def next_page(self):
        if "&pn=" not in self.url:
            self.url += "&pn=1"
        url_base, page_number_str = self.url.split('&pn=')
        page_number_int = int(page_number_str) + 1
        self.url = f"{url_base}&pn={page_number_int}"