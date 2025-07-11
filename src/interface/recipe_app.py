from PyQt5.QtWidgets import QMainWindow, QStackedWidget

from src.interface.results_screen import ResultsScreen
from src.interface.search_screen import SearchScreen
from src.interface.recipe_detail_screen import RecipeDetailScreen


class RecipeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_search_term = ""
        self.current_found_recipes = []
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Pesquisador de Receitas")
        self.setGeometry(300, 300, 900, 700)  # Aumentei um pouco o tamanho da janela
        
        # Widget principal com pilha de telas
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Criar as telas
        self.search_screen = SearchScreen(self)
        self.results_screen = ResultsScreen(self)
        self.detail_screen = RecipeDetailScreen(self)
        
        # Adicionar as telas ao stack
        self.stacked_widget.addWidget(self.search_screen)
        self.stacked_widget.addWidget(self.results_screen)
        self.stacked_widget.addWidget(self.detail_screen)
        
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
        
        # Salvar o estado atual para poder voltar
        self.current_search_term = search_term
        self.current_found_recipes = found_recipes
        
        self.results_screen.update_results(search_term, found_recipes)
        self.stacked_widget.setCurrentWidget(self.results_screen)
    
    def show_results_screen_from_detail(self):
        """Volta para a tela de resultados mantendo os dados anteriores"""
        self.stacked_widget.setCurrentWidget(self.results_screen)
    
    def show_recipe_detail(self, recipe_data):
        """Mostra os detalhes de uma receita específica"""
        self.detail_screen.update_recipe_detail(recipe_data)
        self.stacked_widget.setCurrentWidget(self.detail_screen)