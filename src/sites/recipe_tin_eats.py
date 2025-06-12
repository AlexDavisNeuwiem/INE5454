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
            # titulo = receita.find("h2", {"class" : "entry-title"})
            # link = receita.find("h2", {"class" : "entry-title"})

            if link_tag:
                # 5. Extraímos o título e o link da mesma tag
                titulo = link_tag.text.strip()
                link = link_tag.get('href', '') # .get() é mais seguro que [], evita erro se href não existir

            
            self.recipes_num += 1
            dados = {
                'NUMERO': self.recipes_num,
                'TITULO': titulo,
                'LINK': link
            }

            resposta.append(dados)

        return resposta, True

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
            self.recipes.extend(recipe_list)
            print(numero_pagina_int)
            if numero_pagina_int == 80:
                    break

            
            # Segue para a próxima página      
            url_base, numero_pagina_str = self.url.split('=')
            # print(numero_pagina_str)
            numero_pagina_int = int(numero_pagina_str) + 1
            self.url = f"{url_base}={numero_pagina_int}"

            
        # Salva o arquivo json
        self.save_json(self.recipes)