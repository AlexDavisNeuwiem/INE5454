import json

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QScrollArea, QFrame,
                             QTextEdit, QSplitter)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class RecipeDetailScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_recipe = None
        self.init_ui()
    
    def init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Header com título e botão voltar
        header_layout = QHBoxLayout()
        
        back_btn = QPushButton("← Voltar aos Resultados")
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
        
        header_layout.addWidget(back_btn)
        header_layout.addStretch()
        
        main_layout.addLayout(header_layout)
        
        # Área de scroll para o conteúdo da receita
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
        
        # Widget que conterá o conteúdo da receita
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background-color: transparent;")
        
        # Layout para o conteúdo da receita
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(20)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Configurar o scroll area
        self.scroll_area.setWidget(self.content_widget)
        main_layout.addWidget(self.scroll_area)
        
        self.setLayout(main_layout)
    
    def create_info_section(self, title, content, is_text_area=False):
        """Cria uma seção de informação com título e conteúdo"""
        section = QFrame()
        section.setFrameStyle(QFrame.Box)
        section.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 15px;
                margin: 5px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Título da seção
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        
        # Conteúdo da seção
        if is_text_area:
            content_widget = QTextEdit()
            content_widget.setPlainText(content)
            content_widget.setReadOnly(True)
            content_widget.setFont(QFont("Arial", 11))
            content_widget.setStyleSheet("""
                QTextEdit {
                    border: 1px solid #ddd;
                    border-radius: 6px;
                    padding: 10px;
                    background-color: #f8f9fa;
                }
            """)
            content_widget.setMinimumHeight(150)
        else:
            content_widget = QLabel(content)
            content_widget.setFont(QFont("Arial", 11))
            content_widget.setStyleSheet("color: #34495e; line-height: 1.6;")
            content_widget.setWordWrap(True)
            content_widget.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        layout.addWidget(title_label)
        layout.addWidget(content_widget)
        
        section.setLayout(layout)
        return section
    
    def clear_content(self):
        """Remove todo o conteúdo anterior"""
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def format_list_content(self, content):
        """Formata o conteúdo de listas para exibição"""
        
        if content is None:
            return "Não disponível"
            
        if isinstance(content, list):
            if not content:
                return "Não disponível"
            # Se é uma lista de strings, junta com quebras de linha
            formatted_items = []
            for i, item in enumerate(content):
                if item is not None and str(item).strip():
                    formatted_items.append(f"{str(item).strip()}")
            result = '\n'.join(formatted_items) if formatted_items else "Não disponível"
            return result
        else:
            result = str(content) if content else "Não disponível"
            return result
    
    def update_recipe_detail(self, recipe_data):
        """Atualiza a tela com os detalhes da receita"""
        
        # Limpa o conteúdo anterior
        self.clear_content()
        self.current_recipe = recipe_data

        # Título principal da receita
        title = self.current_recipe.get('TITLE')
        title_section = self.create_info_section("Título da Receita", f"{title}")
        self.content_layout.addWidget(title_section)
        
        # Número da receita
        numero = self.current_recipe.get('NUMBER')
        numero_section = self.create_info_section("Número da Receita", f"#{numero}")
        self.content_layout.addWidget(numero_section)
        
        # Autor
        author = self.current_recipe.get('AUTHOR', '')
        if author:
            author_section = self.create_info_section("Autor", author)
            self.content_layout.addWidget(author_section)
        
        # Tempo de preparo
        prep_time = self.current_recipe.get('PREP_TIME')
        if prep_time and str(prep_time).strip() and str(prep_time) != 'ERROR':
            prep_time_section = self.create_info_section("Tempo de Preparo", str(prep_time))
            self.content_layout.addWidget(prep_time_section)
        
        # Link da receita original
        link = self.current_recipe.get('LINK')
        if link and str(link).strip():
            link_section = self.create_info_section("Link Original", str(link))
            self.content_layout.addWidget(link_section)
        
        # Ingredientes
        ingredients = self.current_recipe.get('INGREDIENTS')
        if ingredients:
            ingredients_content = self.format_list_content(ingredients)
            ingredients_section = self.create_info_section("Ingredientes", ingredients_content, is_text_area=True)
            self.content_layout.addWidget(ingredients_section)
        
        # Instruções
        instructions = self.current_recipe.get('INSTRUCTIONS')
        if instructions:
            instructions_content = self.format_list_content(instructions)
            instructions_section = self.create_info_section("Instruções", instructions_content, is_text_area=True)
            self.content_layout.addWidget(instructions_section)
        
        # Adiciona um espaçador no final
        self.content_layout.addStretch()
        
        # Volta o scroll para o topo
        self.scroll_area.verticalScrollBar().setValue(0)
    
    def go_back(self):
        """Volta para a tela de resultados"""
        self.main_window.show_results_screen_from_detail()