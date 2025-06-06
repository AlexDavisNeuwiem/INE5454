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
    
    def update_recipe_detail(self, recipe_data):
        """Atualiza a tela com os detalhes da receita"""
        self.current_recipe = recipe_data
        
        # Limpa o conteúdo anterior
        self.clear_content()
        
        # Título principal da receita
        title = recipe_data.get('TITULO', 'Receita sem título')
        main_title = QLabel(title)
        main_title.setAlignment(Qt.AlignCenter)
        main_title.setFont(QFont("Arial", 20, QFont.Bold))
        main_title.setStyleSheet("""
            color: #2c3e50; 
            background-color: #ecf0f1; 
            padding: 20px; 
            border-radius: 10px;
            margin-bottom: 20px;
        """)
        main_title.setWordWrap(True)
        
        self.content_layout.addWidget(main_title)
        
        # Informações básicas
        info_layout = QHBoxLayout()
        
        # Número da receita
        numero = recipe_data.get('NUMERO', 'N/A')
        numero_section = self.create_info_section("Número da Receita", f"#{numero}")
        numero_section.setMaximumWidth(200)
        
        # Fonte
        source = recipe_data.get('SOURCE', 'Desconhecida')
        source_clean = source.replace('_', ' ').replace('src/dados/', '').replace('/receitas', '').title()
        source_section = self.create_info_section("Fonte", source_clean)
        source_section.setMaximumWidth(200)
        
        info_layout.addWidget(numero_section)
        info_layout.addWidget(source_section)
        info_layout.addStretch()
        
        self.content_layout.addLayout(info_layout)
        
        # Outras informações disponíveis
        fields_to_show = [
            ('CATEGORIA', 'Categoria'),
            ('TEMPO_PREPARO', 'Tempo de Preparo'),
            ('PORCOES', 'Porções'),
            ('DIFICULDADE', 'Dificuldade'),
            ('DESCRICAO', 'Descrição'),
            ('INGREDIENTES', 'Ingredientes'),
            ('MODO_PREPARO', 'Modo de Preparo'),
            ('DICAS', 'Dicas'),
            ('INFORMACOES_NUTRICIONAIS', 'Informações Nutricionais'),
            ('TAGS', 'Tags'),
            ('URL', 'URL Original')
        ]
        
        for field_key, field_title in fields_to_show:
            field_value = recipe_data.get(field_key)
            if field_value and field_value != 'N/A' and field_value.strip():
                # Campos que devem ser exibidos em área de texto
                text_area_fields = ['INGREDIENTES', 'MODO_PREPARO', 'DICAS', 'DESCRICAO']
                is_text_area = field_key in text_area_fields
                
                # Formatar o conteúdo se necessário
                if isinstance(field_value, list):
                    if field_key == 'TAGS':
                        content = ', '.join(field_value)
                    else:
                        content = '\n'.join([f"• {item}" for item in field_value])
                else:
                    content = str(field_value)
                
                section = self.create_info_section(field_title, content, is_text_area)
                self.content_layout.addWidget(section)
        
        # Adiciona um espaçador no final
        self.content_layout.addStretch()
        
        # Volta o scroll para o topo
        self.scroll_area.verticalScrollBar().setValue(0)
    
    def go_back(self):
        """Volta para a tela de resultados"""
        self.main_window.show_results_screen_from_detail()