from src.recipe_scrapper import RecipeScraper
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
            'AUTHOR': '',
            'PREP_TIME': '',
            'INGREDIENTS': [],
            'INSTRUCTIONS': []
        }

        recipe_html = self.soup.find_all("div", class_="current-recipe")

        title= recipe_html[0].select_one("div", class_="layout__item title svelte-ar8gac")
        print(f"TÍTULO = {title}")

        author = recipe_html[0].select_one("div", class_="byline svelte-176rmbi")
        print(f"AUTOR = {author}")

        prep = recipe_html[0].select_one("dd", class_="facts__value svelte-ar8gac")
        print(f"PREPARO = {prep.text.strip()}")

        ingr = recipe_html[0].select_one("section", class_="layout__item ingredients svelte-ar8gac")
        print(f"INGREDIENTES = {ingr}")

        inst = recipe_html[0].select_one("section", class_="layout__item directions svelte-ar8gac")
        print(f"INSTRUÇÕES = {inst}")

        return result


    def run(self):
            finish = True
            page_number = 0

            # Percorre as URLs procurando por receitas
            while(finish):
                # Retorna a próxima URL
                self.fetch_content()

                # self.save_html()
                # Extrai as receitas do site
                recipe_list, finish = self.extract_recipes()

                for link in recipe_list:
                    recipe = self.extract_details(link)
                    self.recipes.extend(recipe)

                # TODO: Remover
                if page_number == 5:
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