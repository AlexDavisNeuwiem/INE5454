from src.recipe_scrapper import RecipeScraper


class RecipeTinEats(RecipeScraper):
    def extract_recipes(self):
        receitas_html = self.soup.find_all("article")
        resposta = []
        receita_nr = 1

        for receita in receitas_html:
            titulo = receita.find("h2", {"class" : "entry-title"})

            if not titulo:
                continue

            dados = {
                'NUMERO': str(receita_nr),
                'TITULO': titulo.text.strip()
            }

            resposta.append(dados)
            receita_nr += 1

        return resposta
