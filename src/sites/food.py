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
            #print(f'URL: {receita}')
            data = json.loads(receita)
            items = data.get('itemListElement', [])
            for item in items:
                url = item.get('url')
                if url:
                    resposta.append(url)
        print(resposta)





        # script = receitas_html.select('script[type="application/ld+json"]')
        # print(receitas_html)
        # for receita in receitas_html:
        #     div2 = receita.find("div", class_="tile-stream clearfix fdStream")
        #     # print(f'DIV2: {div2}')
        #     if div2:
        #         details = div2.select("div", class_="details")
        #         # print(details)
        #         div_title = details.select("div", class_="title")
        #         print(f'DIV_TITLE: {div_title}')
            # if div2:
            #     receita_tag = div2.select_one("h2", class_ = "title")
            #     print(f'RECEITA_TAG: {receita_tag}')
            #     titulo = receita_tag.get("title", "")


            # print(f'LINK_TAG: {titulo}')

            # if link_tag:
            #     # Extraindo o título e o link
            #     title = link_tag.text.strip()
            #     link = link_tag.get('href', '')

            
            # self.recipes_num += 1

            # dados = {
            #     'NUMBER': self.recipes_num,
            #     'TITLE': "title",
            #     'LINK': "link",
            #     'AUTHOR': '',
            #     'PREP_TIME': '',
            #     'INGREDIENTS': '',
            #     'INSTRUCTIONS': ''
            # }

            # resposta.append(dados)

        return resposta, True

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