import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QStackedWidget, QFrame)
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
    
    def search_recipes(self):
        recipe_name = self.recipe_input.text().strip()
        if recipe_name:
            # Aqui você pode implementar a lógica de pesquisa
            # Por enquanto, apenas passa para a tela de resultados
            self.main_window.show_results_screen(recipe_name)


class ResultsScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
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
        
        # Container para as receitas
        recipes_layout = QVBoxLayout()
        recipes_layout.setSpacing(15)
        
        # Três opções de receita
        self.recipe_cards = []
        for i in range(3):
            card = self.create_recipe_card(f"Receita {i + 1}", f"Descrição da receita {i + 1}")
            self.recipe_cards.append(card)
            recipes_layout.addWidget(card)
        
        # Layout principal
        layout.addLayout(header_layout)
        layout.addLayout(recipes_layout)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def create_recipe_card(self, title, description):
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
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        
        # Descrição da receita
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Arial", 12))
        desc_label.setStyleSheet("color: #7f8c8d;")
        desc_label.setWordWrap(True)
        
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
        select_btn.clicked.connect(lambda: self.select_recipe(title))
        
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addWidget(select_btn, alignment=Qt.AlignRight)
        
        card.setLayout(layout)
        return card
    
    def update_results(self, search_term):
        self.results_title.setText(f'Resultados para: "{search_term}"')
        
        # Aqui você pode implementar a lógica para atualizar as receitas
        # com base no termo pesquisado
        for i, card in enumerate(self.recipe_cards):
            # Exemplo de como atualizar os cards
            layout = card.layout()
            title_label = layout.itemAt(0).widget()
            desc_label = layout.itemAt(1).widget()
            
            title_label.setText(f"Receita de {search_term} - Opção {i + 1}")
            desc_label.setText(f"Uma deliciosa receita de {search_term.lower()} com ingredientes especiais")
    
    def select_recipe(self, recipe_name):
        # Aqui você pode implementar a lógica quando uma receita é selecionada
        print(f"Receita selecionada: {recipe_name}")
    
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
    
    def show_results_screen(self, search_term):
        self.results_screen.update_results(search_term)
        self.stacked_widget.setCurrentWidget(self.results_screen)


def main():
    app = QApplication(sys.argv)
    
    # Configurar fonte padrão da aplicação
    font = QFont("Arial", 10)
    app.setFont(font)
    
    window = RecipeApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()