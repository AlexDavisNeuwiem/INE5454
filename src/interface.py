import sys
import json
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QStackedWidget, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from src.sites.food import Food
from src.sites.pinch_of_yum import PinchOfYum
from src.sites.recipe_tin_eats import RecipeTinEats

from enums import URLs

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
            title = recipe.get('TITULO', '').lower()
            if search_term_lower in title:
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


class ResultsScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.found_recipes = []
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header com título e botão voltar
        header_layout = QHBoxLayout()
        
        back_btn = QPushButton("← Voltar")
        back_btn.setFont(QFont("Arial", 10))
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        back_btn.clicked.connect(self.go_back)
        
        self.results_title = QLabel("Resultados da pesquisa")
        self.results_title.setAlignment(Qt.AlignCenter)
        self.results_title.setFont(QFont("Arial", 20, QFont.Bold))
        self.results_title.setStyleSheet("color: #2c3e50;")
        
        header_layout.addWidget(back_btn)
        header_layout.addStretch()
        header_layout.addWidget(self.results_title)
        header_layout.addStretch()
        header_layout.addWidget(QLabel())  # Espaço para manter o título centralizado
        
        # Container para as receitas (será criado dinamicamente)
        self.recipes_layout = QVBoxLayout()
        self.recipes_layout.setSpacing(15)
        
        # Layout principal
        layout.addLayout(header_layout)
        layout.addLayout(self.recipes_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def create_recipe_card(self, recipe_data):
        """Cria um card de receita baseado nos dados do JSON"""
        card = QFrame()
        card.setFrameStyle(QFrame.Box)
        card.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 10px;
            }
            QFrame:hover {
                border-color: #3498db;
                background-color: #f8f9fa;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        # Título da receita
        title = recipe_data.get('TITULO', 'Título não disponível')
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setWordWrap(True)
        
        # Layout para informações secundárias (número e fonte)
        info_layout = QHBoxLayout()
        
        # Número da receita
        numero = recipe_data.get('NUMERO', 'N/A')
        numero_label = QLabel(f"Receita #{numero}")
        numero_label.setFont(QFont("Arial", 10))
        numero_label.setStyleSheet("color: #7f8c8d;")
        
        # Fonte da receita
        source = recipe_data.get('SOURCE', 'Desconhecida')
        source_label = QLabel(f"Fonte: {source.replace('_', ' ').title()}")
        source_label.setFont(QFont("Arial", 10))
        source_label.setStyleSheet("color: #27ae60; font-weight: bold;")
        
        info_layout.addWidget(numero_label)
        info_layout.addStretch()
        info_layout.addWidget(source_label)
        
        # Botão de seleção
        select_btn = QPushButton("Selecionar Receita")
        select_btn.setFont(QFont("Arial", 10))
        select_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        select_btn.clicked.connect(lambda: self.select_recipe(recipe_data))
        
        layout.addWidget(title_label)
        layout.addLayout(info_layout)
        layout.addWidget(select_btn, alignment=Qt.AlignRight)
        
        card.setLayout(layout)
        return card
    
    def clear_recipes_layout(self):
        """Remove todos os widgets do layout de receitas"""
        while self.recipes_layout.count():
            child = self.recipes_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def update_results(self, search_term, found_recipes):
        """Atualiza a tela com os resultados da pesquisa"""
        self.found_recipes = found_recipes
        
        # Conta receitas por fonte
        source_counts = {}
        for recipe in found_recipes:
            source = recipe.get('SOURCE', 'Desconhecida')
            source_counts[source] = source_counts.get(source, 0) + 1
        
        # Monta o título com informações sobre as fontes
        title_text = f'Resultados para: "{search_term}" ({len(found_recipes)} receitas encontradas)'
        if source_counts:
            print(f'SOURCE: {source}')
            sources_info = " | ".join([f"{source.replace('_', ' ').replace('src/dados/', '').replace('/receitas', '').title()}: {count}" 
                                     for source, count in source_counts.items()])
            title_text += f"\n{sources_info}"
            print(f'INFO: {sources_info}')
        
        self.results_title.setText(title_text)
        
        # Limpa os resultados anteriores
        self.clear_recipes_layout()
        
        if not found_recipes:
            # Se não encontrou receitas, mostra mensagem
            no_results_label = QLabel("Nenhuma receita encontrada com esse termo em nenhum dos arquivos.")
            no_results_label.setAlignment(Qt.AlignCenter)
            no_results_label.setFont(QFont("Arial", 14))
            no_results_label.setStyleSheet("color: #7f8c8d; margin: 20px;")
            self.recipes_layout.addWidget(no_results_label)
        else:
            # Ordena receitas por fonte para melhor organização
            found_recipes.sort(key=lambda x: x.get('SOURCE', ''))
            
            # Cria cards para cada receita encontrada
            for recipe in found_recipes:
                card = self.create_recipe_card(recipe)
                self.recipes_layout.addWidget(card)
    
    def select_recipe(self, recipe_data):
        """Lida com a seleção de uma receita"""
        title = recipe_data.get('TITULO', 'Receita sem título')
        numero = recipe_data.get('NUMERO', 'N/A')
        source = recipe_data.get('SOURCE', 'Desconhecida')
        print(f"Receita selecionada: #{numero} - {title} (Fonte: {source})")
        # Aqui você pode implementar a lógica adicional quando uma receita é selecionada
    
    def go_back(self):
        self.main_window.show_search_screen()


class RecipeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Pesquisador de Receitas")
        self.setGeometry(300, 300, 800, 600)
        
        # Widget principal com pilha de telas
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Criar as telas
        self.search_screen = SearchScreen(self)
        self.results_screen = ResultsScreen(self)
        
        # Adicionar as telas ao stack
        self.stacked_widget.addWidget(self.search_screen)
        self.stacked_widget.addWidget(self.results_screen)
        
        # Começar com a tela de pesquisa
        self.stacked_widget.setCurrentWidget(self.search_screen)
        
        # Estilo geral da aplicação
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ecf0f1;
            }
        """)
    
    def show_search_screen(self):
        self.stacked_widget.setCurrentWidget(self.search_screen)
        # Limpar o campo de pesquisa
        self.search_screen.recipe_input.clear()
        self.search_screen.recipe_input.setFocus()
    
    def show_results_screen(self, search_term, found_recipes=None):
        """Atualizada para receber as receitas encontradas"""
        if found_recipes is None:
            found_recipes = []
        self.results_screen.update_results(search_term, found_recipes)
        self.stacked_widget.setCurrentWidget(self.results_screen)


def main():

    # Create scraper instances
    scraperRTE = RecipeTinEats(
        url=URLs.RECIPE_TIN_EATS.value,
        output_dir=URLs.RTE_OUTPUT_DIR.value
    )
    scraperPOY = PinchOfYum(
        url=URLs.PINCH_OF_YUM.value,
        output_dir=URLs.POY_OUTPUT_DIR.value
    )
    scraperFOOD = Food(
        url=URLs.FOOD.value,
        output_dir=URLs.FOOD_OUTPUT_DIR.value
    )

    # Create threads for each scraper
    thread_rte = threading.Thread(target=scraperRTE.run)
    thread_poy = threading.Thread(target=scraperPOY.run)
    thread_food = threading.Thread(target=scraperFOOD.run)

    # Start all threads
    thread_rte.start()
    thread_poy.start()
    thread_food.start()

    # Wait for all threads to complete
    thread_rte.join()
    thread_poy.join()
    thread_food.join()

    app = QApplication(sys.argv)
    
    # Configurar fonte padrão da aplicação
    font = QFont("Arial", 10)
    app.setFont(font)
    
    window = RecipeApp()
    window.show()
    
    sys.exit(app.exec_())