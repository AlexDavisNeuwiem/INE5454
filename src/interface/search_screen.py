import json

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, 
                             QLabel, QLineEdit, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class SearchScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Título
        title = QLabel("Pesquisar Receitas")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        
        # Campo de entrada
        self.recipe_input = QLineEdit()
        self.recipe_input.setPlaceholderText("Digite o nome da receita que deseja pesquisar...")
        self.recipe_input.setFont(QFont("Arial", 12))
        self.recipe_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        self.recipe_input.returnPressed.connect(self.search_recipes)
        
        # Botão de pesquisa
        search_btn = QPushButton("Pesquisar")
        search_btn.setFont(QFont("Arial", 12, QFont.Bold))
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        search_btn.clicked.connect(self.search_recipes)
        
        # Layout dos elementos
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(self.recipe_input)
        layout.addWidget(search_btn, alignment=Qt.AlignCenter)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def load_recipes_from_json(self):
        """Carrega as receitas de múltiplos arquivos JSON"""
        json_files = [
            'src/dados/recipe_tin_eats/receitas.json',
            'src/dados/pinch_of_yum/receitas.json', 
            'src/dados/food/receitas.json'
        ]
        
        all_recipes = []
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as file:
                    recipes = json.load(file)
                    # Adiciona informação sobre a fonte das receitas
                    for recipe in recipes:
                        recipe['SOURCE'] = json_file.replace('receitas_', '').replace('.json', '')
                    all_recipes.extend(recipes)
                    print(f"Carregadas {len(recipes)} receitas de {json_file}")
            except FileNotFoundError:
                print(f"Arquivo {json_file} não encontrado!")
            except json.JSONDecodeError:
                print(f"Erro ao decodificar o arquivo {json_file}!")
        
        print(f"Total de receitas carregadas: {len(all_recipes)}")
        return all_recipes
    
    def search_in_recipes(self, search_term):
        """Busca receitas que contenham o termo pesquisado no título"""
        recipes = self.load_recipes_from_json()
        found_recipes = []
        
        search_term_lower = search_term.lower()
        
        for recipe in recipes:
            title = recipe.get('TITLE', '').lower()
            if title and (search_term_lower in title):
                found_recipes.append(recipe)
        
        return found_recipes
    
    def search_recipes(self):
        recipe_name = self.recipe_input.text().strip()
        
        if recipe_name:
            # Busca as receitas no arquivo JSON
            found_recipes = self.search_in_recipes(recipe_name)
            
            if found_recipes:
                # Passa as receitas encontradas para a tela de resultados
                self.main_window.show_results_screen(recipe_name, found_recipes)
            else:
                # Se não encontrou nada, passa lista vazia
                self.main_window.show_results_screen(recipe_name, [])