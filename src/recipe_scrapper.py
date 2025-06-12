import json
import requests
from bs4 import BeautifulSoup
import os

class RecipeScraper:
    def __init__(self, url, output_dir):
        self.url = url
        self.output_dir = output_dir
        self.soup = None
        self.recipes = []
        self.recipes_num = 0

    def fetch_content(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.soup = BeautifulSoup(response.content, 'html.parser')
        else:
            raise Exception(f"Erro ao acessar {self.url}")
        
    def save_html(self, filename="conteudo_extraido.html"):
        if self.soup:
            path = os.path.join(self.output_dir, filename)
            with open(path, "w", encoding='utf-8') as file:
                file.write(self.soup.prettify())

    def extract_recipes(self):
        """Método genérico, deve ser sobrescrito por classes filhas"""
        raise NotImplementedError("Este método deve ser implementado por subclasses.")

    def save_json(self, data, filename="receitas.json"):
        path = os.path.join(self.output_dir, filename)
        with open(path, "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def run(self):
        self.fetch_content()
        self.save_html()
        self.recipes = self.extract_recipes()
        self.save_json(self.recipes)