from PyQt5.QtWidgets import (QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton,
                             QFrame, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class ResultsScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.found_recipes = []
        self.init_ui()
    
    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
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
        
        main_layout.addLayout(header_layout)
        
        # Área de scroll para as receitas
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #ecf0f1;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #bdc3c7;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #95a5a6;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Widget que conterá todas as receitas
        self.scroll_widget = QWidget()
        self.scroll_widget.setStyleSheet("background-color: transparent;")
        
        # Layout para as receitas dentro do scroll
        self.recipes_layout = QVBoxLayout(self.scroll_widget)
        self.recipes_layout.setSpacing(15)
        self.recipes_layout.setContentsMargins(0, 0, 0, 0)
        
        # Configurar o scroll area
        self.scroll_area.setWidget(self.scroll_widget)
        
        # Adicionar o scroll area ao layout principal
        main_layout.addWidget(self.scroll_area)
        
        self.setLayout(main_layout)
    
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
                margin: 2px;
            }
            QFrame:hover {
                border-color: #3498db;
                background-color: #f8f9fa;
            }
        """)
        card.setMinimumHeight(200)  # Altura mínima para cada card
        card.setMaximumHeight(400)  # Altura máxima para manter consistência
        
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(15, 10, 15, 10)
        
        # Título da receita
        title = recipe_data.get('TITULO', 'Título não disponível')
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setWordWrap(True)
        title_label.setMaximumHeight(50)  # Limita a altura do título
        
        # Layout para informações secundárias (número e fonte)
        info_layout = QHBoxLayout()
        
        # Número da receita
        numero = recipe_data.get('NUMERO', 'N/A')
        numero_label = QLabel(f"Receita #{numero}")
        numero_label.setFont(QFont("Arial", 10))
        numero_label.setStyleSheet("color: #7f8c8d;")
        
        # Fonte da receita
        source = recipe_data.get('SOURCE', 'Desconhecida')
        source_label = QLabel(f"Fonte: {source.replace('_', ' ').replace('src/dados/', '').replace('/receitas', '').title()}")
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
                max-width: 140px;
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
            
            # Adiciona um espaçador no final para melhor aparência
            self.recipes_layout.addStretch()
        
        # Volta o scroll para o topo
        self.scroll_area.verticalScrollBar().setValue(0)
    
    def select_recipe(self, recipe_data):
        """Lida com a seleção de uma receita"""
        title = recipe_data.get('TITULO', 'Receita sem título')
        numero = recipe_data.get('NUMERO', 'N/A')
        source = recipe_data.get('SOURCE', 'Desconhecida')
        print(f"Receita selecionada: #{numero} - {title} (Fonte: {source})")
        # Aqui você pode implementar a lógica adicional quando uma receita é selecionada
    
    def go_back(self):
        self.main_window.show_search_screen()