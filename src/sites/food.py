from src.recipe_scrapper import RecipeScraper


class Food(RecipeScraper):
    def extract_recipes(self):
        receitas_html = self.soup.find_all("div", {"class" : "smart-info-wrap"})
        resposta = []
        receita_nr = 1

        for receita in receitas_html:
            titulo = receita.find("h2", {"class" : "title"})

            if not titulo:
                continue

            dados = {
                'NUMBER': str(receita_nr),
                'TITLE': titulo.text.strip()
            }

            resposta.append(dados)
            receita_nr += 1

        return resposta
