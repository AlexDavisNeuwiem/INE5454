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

            if not titulo:
                continue

            dados = {
                'NUMBER': str(receita_nr),
                'TITLE': titulo.text.strip()
            }

            resposta.append(dados)
            receita_nr += 1

        return resposta
