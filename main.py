# main.py
import sys
import os
import subprocess
import json
from typing import Dict, List, Optional, Any
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from config import AppConfig, StyleConfig
from database_manager import db_manager

class OptionsDialog(QDialog):
    """Diálogo para mostrar opções de um payload/exploit"""
    
    def __init__(self, item_type: str, item_name: str, options_data: Dict, parent=None):
        super().__init__(parent)
        self.item_type = item_type
        self.item_name = item_name
        self.options_data = options_data
        self.inputs = {}
        self.values = {}
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(f'⚙️ Opções - {self.item_name}')
        self.setGeometry(200, 200, 900, 700)
        self.setStyleSheet(StyleConfig.get_style())
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Título
        title_label = QLabel(f'📦 {self.item_name}')
        title_label.setStyleSheet(f'font-size: 16px; font-weight: bold; color: {AppConfig.COLORS["primary"]};')
        layout.addWidget(title_label)
        
        # Descrição
        if self.options_data.get('description'):
            desc_label = QLabel(f'📝 {self.options_data["description"]}')
            desc_label.setStyleSheet(f'color: {AppConfig.COLORS["text_secondary"]};')
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)
        
        # Scroll area para opções
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_widget.setLayout(scroll_layout)
        
        # Opções Básicas
        if self.options_data.get('basic_options'):
            basic_group = QGroupBox('⚙️ Opções Básicas')
            basic_layout = QVBoxLayout()
            
            for opt in self.options_data['basic_options']:
                opt_widget = self.create_option_widget(opt)
                if opt_widget:
                    basic_layout.addWidget(opt_widget)
            
            basic_group.setLayout(basic_layout)
            scroll_layout.addWidget(basic_group)
        
        # Opções Avançadas
        if self.options_data.get('advanced_options'):
            adv_group = QGroupBox('🔧 Opções Avançadas')
            adv_layout = QVBoxLayout()
            
            for opt in self.options_data['advanced_options']:
                opt_widget = self.create_option_widget(opt)
                if opt_widget:
                    adv_layout.addWidget(opt_widget)
            
            adv_group.setLayout(adv_layout)
            scroll_layout.addWidget(adv_group)
        
        # Opções de Evasão
        if self.options_data.get('evasion_options'):
            eva_group = QGroupBox('🛡️ Opções de Evasão')
            eva_layout = QVBoxLayout()
            
            for opt in self.options_data['evasion_options']:
                opt_widget = self.create_option_widget(opt)
                if opt_widget:
                    eva_layout.addWidget(opt_widget)
            
            eva_group.setLayout(eva_layout)
            scroll_layout.addWidget(eva_group)
        
        # Campos Required destacados
        if self.options_data.get('required_options'):
            required_label = QLabel(f"⚠️ Campos obrigatórios: {', '.join(self.options_data['required_options'])}")
            required_label.setStyleSheet(f'color: {AppConfig.COLORS["error"]}; font-weight: bold;')
            scroll_layout.addWidget(required_label)
        
        # Se não tem opções, mostrar mensagem
        if not self.options_data.get('basic_options') and \
           not self.options_data.get('advanced_options') and \
           not self.options_data.get('evasion_options'):
            no_opts = QLabel('ℹ️ Nenhuma opção disponível para este item')
            no_opts.setStyleSheet(f'color: {AppConfig.COLORS["text_secondary"]};')
            scroll_layout.addWidget(no_opts)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # Botões
        btn_layout = QHBoxLayout()
        
        generate_btn = QPushButton('⚡ Gerar com estas opções')
        generate_btn.setObjectName('generateBtn')
        generate_btn.clicked.connect(self.apply_and_close)
        btn_layout.addWidget(generate_btn)
        
        cancel_btn = QPushButton('❌ Cancelar')
        cancel_btn.clicked.connect(self.close)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
    
    def create_option_widget(self, option: Dict) -> QWidget:
        """Cria widget para uma opção"""
        name = option.get('name', '')
        required = option.get('required', 'no')
        description = option.get('description', '')
        current = option.get('current_setting', '')
        
        # Verificar se é required
        is_required = required.lower() == 'yes'
        
        widget = QWidget()
        layout = QHBoxLayout()
        widget.setLayout(layout)
        
        # Label com indicador
        label_text = name
        if is_required:
            label_text += ' *'
        label = QLabel(label_text)
        label.setMinimumWidth(150)
        label.setStyleSheet(f'font-weight: bold; color: {"#ff6b6b" if is_required else AppConfig.COLORS["text"]};')
        layout.addWidget(label)
        
        # Input
        input_field = QLineEdit()
        if current:
            input_field.setText(current)
        input_field.setPlaceholderText(description[:50] + '...' if len(description) > 50 else description)
        input_field.setMinimumHeight(AppConfig.UI_CONFIG['input_height'])
        input_field.textChanged.connect(lambda: self.on_input_changed(name))
        layout.addWidget(input_field)
        
        # Descrição curta com tooltip
        desc_label = QLabel(description[:30] + '...' if len(description) > 30 else description)
        desc_label.setToolTip(description)
        desc_label.setStyleSheet(f'color: {AppConfig.COLORS["text_secondary"]}; font-size: 10px;')
        desc_label.setMinimumWidth(100)
        layout.addWidget(desc_label)
        
        # Status para required
        if is_required:
            status_label = QLabel('⚠️')
            status_label.setStyleSheet(f'color: {AppConfig.COLORS["error"]};')
            status_label.setToolTip('Campo obrigatório')
            layout.addWidget(status_label)
        
        # Armazenar referência
        self.inputs[name] = input_field
        
        return widget
    
    def on_input_changed(self, name):
        """Callback quando um input muda"""
        pass
    
    def apply_and_close(self):
        """Aplica as configurações e fecha"""
        # Coletar valores
        self.values = {}
        for name, input_field in self.inputs.items():
            self.values[name] = input_field.text()
        
        # Verificar campos required
        required = self.options_data.get('required_options', [])
        missing = []
        for req in required:
            if req in self.inputs and not self.inputs[req].text():
                missing.append(req)
        
        if missing:
            reply = QMessageBox.question(
                self, '⚠️ Campos obrigatórios',
                f'Os seguintes campos são obrigatórios e estão vazios:\n{", ".join(missing)}\n\nDeseja continuar mesmo assim?',
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return
        
        self.accept()

class SettingsDialog(QDialog):
    """Diálogo de configurações"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.color_buttons = {}
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('⚙️ Configurações')
        self.setGeometry(300, 300, 700, 600)
        self.setStyleSheet(StyleConfig.get_style())
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Tabs de configurações
        tabs = QTabWidget()
        
        # Geral
        general_tab = self.create_general_tab()
        tabs.addTab(general_tab, '⚙️ Geral')
        
        # Cores
        colors_tab = self.create_colors_tab()
        tabs.addTab(colors_tab, '🎨 Cores')
        
        layout.addWidget(tabs)
        
        # Botões
        btn_layout = QHBoxLayout()
        apply_btn = QPushButton('✅ Aplicar')
        apply_btn.clicked.connect(self.apply_settings)
        btn_layout.addWidget(apply_btn)
        
        reset_btn = QPushButton('🔄 Resetar')
        reset_btn.clicked.connect(self.reset_settings)
        btn_layout.addWidget(reset_btn)
        
        cancel_btn = QPushButton('❌ Cancelar')
        cancel_btn.clicked.connect(self.close)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
    
    def create_general_tab(self):
        """Cria aba geral"""
        tab = QWidget()
        layout = QVBoxLayout()  # Mudado de QGridLayout para QVBoxLayout
        tab.setLayout(layout)
        
        # Grupo de tamanho
        size_group = QGroupBox('📐 Tamanho da Janela')
        size_layout = QGridLayout()
        
        size_layout.addWidget(QLabel('Largura:'), 0, 0)
        self.width_spin = QSpinBox()
        self.width_spin.setRange(800, 2000)
        self.width_spin.setValue(AppConfig.WINDOW_WIDTH)
        size_layout.addWidget(self.width_spin, 0, 1)
        
        size_layout.addWidget(QLabel('Altura:'), 1, 0)
        self.height_spin = QSpinBox()
        self.height_spin.setRange(600, 1500)
        self.height_spin.setValue(AppConfig.WINDOW_HEIGHT)
        size_layout.addWidget(self.height_spin, 1, 1)
        
        size_group.setLayout(size_layout)
        layout.addWidget(size_group)
        
        # Grupo de opções
        options_group = QGroupBox('⚙️ Opções')
        options_layout = QVBoxLayout()
        
        self.auto_load_check = QCheckBox('🔄 Carregar automaticamente ao iniciar')
        self.auto_load_check.setChecked(AppConfig.SETTINGS.get('auto_load', True))
        options_layout.addWidget(self.auto_load_check)
        
        self.confirm_check = QCheckBox('✅ Confirmar antes de gerar')
        self.confirm_check.setChecked(AppConfig.SETTINGS.get('confirm_generate', True))
        options_layout.addWidget(self.confirm_check)
        
        self.preview_check = QCheckBox('💻 Mostrar preview do comando')
        self.preview_check.setChecked(AppConfig.SETTINGS.get('show_preview', True))
        options_layout.addWidget(self.preview_check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        layout.addStretch()
        
        return tab
    
    def create_colors_tab(self):
        """Cria aba de cores"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Seletores de cor
        color_group = QGroupBox('🎨 Cores do Tema')
        color_layout = QGridLayout()
        
        colors = [
            ('Primária', 'primary'),
            ('Secundária', 'secondary'),
            ('Fundo', 'background'),
            ('Fundo Claro', 'background_light'),
            ('Borda', 'border'),
            ('Texto', 'text'),
            ('Erro', 'error'),
        ]
        
        for i, (name, key) in enumerate(colors):
            color_layout.addWidget(QLabel(f'{name}:'), i, 0)
            btn = QPushButton()
            btn.setStyleSheet(f'background-color: {AppConfig.COLORS.get(key, "#00ff41")}; border: 2px solid #00ff41;')
            btn.setFixedSize(100, 35)
            btn.clicked.connect(lambda checked, k=key: self.pick_color(k))
            color_layout.addWidget(btn, i, 1)
            self.color_buttons[key] = btn
        
        color_group.setLayout(color_layout)
        layout.addWidget(color_group)
        
        # Tema pré-definido
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel('🎭 Tema:'))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['Futurista', 'Clássico', 'Matrix', 'Cyberpunk', 'Retro', 'Dark'])
        self.theme_combo.setMinimumHeight(35)
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        theme_layout.addWidget(self.theme_combo)
        layout.addLayout(theme_layout)
        
        layout.addStretch()
        
        return tab
    
    def pick_color(self, key):
        """Abre seletor de cor"""
        color = QColorDialog.getColor()
        if color.isValid():
            hex_color = color.name()
            AppConfig.COLORS[key] = hex_color
            if key in self.color_buttons:
                self.color_buttons[key].setStyleSheet(f'background-color: {hex_color}; border: 2px solid #00ff41;')
    
    def change_theme(self, theme):
        """Muda tema pré-definido"""
        themes = {
            'Futurista': {
                'primary': '#00ff41',
                'secondary': '#00aa33',
                'tertiary': '#33ff66',
                'background': '#0a0a0a',
                'background_light': '#0d0d0d',
                'background_dark': '#050505',
                'border': '#1a3a2a',
                'text': '#00ff41',
                'text_secondary': '#888888',
                'text_dark': '#0a0a0a',
                'error': '#ff0044',
                'error_hover': '#ff3366',
            },
            'Clássico': {
                'primary': '#2196F3',
                'secondary': '#1976D2',
                'tertiary': '#42A5F5',
                'background': '#1e1e1e',
                'background_light': '#2d2d2d',
                'background_dark': '#0d0d0d',
                'border': '#333333',
                'text': '#ffffff',
                'text_secondary': '#888888',
                'text_dark': '#000000',
                'error': '#ff4444',
                'error_hover': '#ff6666',
            },
            'Matrix': {
                'primary': '#00ff00',
                'secondary': '#00cc00',
                'tertiary': '#33ff33',
                'background': '#000000',
                'background_light': '#001a00',
                'background_dark': '#000000',
                'border': '#003300',
                'text': '#00ff00',
                'text_secondary': '#008800',
                'text_dark': '#000000',
                'error': '#ff0000',
                'error_hover': '#ff3333',
            },
            'Cyberpunk': {
                'primary': '#ff00ff',
                'secondary': '#cc00cc',
                'tertiary': '#ff33ff',
                'background': '#0a0a0a',
                'background_light': '#1a0a1a',
                'background_dark': '#050005',
                'border': '#330033',
                'text': '#ff00ff',
                'text_secondary': '#880088',
                'text_dark': '#000000',
                'error': '#ff0044',
                'error_hover': '#ff3366',
            },
            'Retro': {
                'primary': '#ff8800',
                'secondary': '#cc6600',
                'tertiary': '#ffaa33',
                'background': '#2a1a0a',
                'background_light': '#3a2a1a',
                'background_dark': '#1a0a00',
                'border': '#664422',
                'text': '#ff8800',
                'text_secondary': '#886644',
                'text_dark': '#000000',
                'error': '#ff0044',
                'error_hover': '#ff3366',
            },
            'Dark': {
                'primary': '#666666',
                'secondary': '#444444',
                'tertiary': '#888888',
                'background': '#0a0a0a',
                'background_light': '#1a1a1a',
                'background_dark': '#000000',
                'border': '#333333',
                'text': '#cccccc',
                'text_secondary': '#666666',
                'text_dark': '#000000',
                'error': '#ff4444',
                'error_hover': '#ff6666',
            }
        }
        
        if theme in themes:
            colors = themes[theme]
            for key, value in colors.items():
                if key in AppConfig.COLORS:
                    AppConfig.COLORS[key] = value
                    if key in self.color_buttons:
                        self.color_buttons[key].setStyleSheet(f'background-color: {value}; border: 2px solid #00ff41;')
    
    def apply_settings(self):
        """Aplica as configurações"""
        # Tamanho da janela
        width = self.width_spin.value()
        height = self.height_spin.value()
        if self.parent:
            self.parent.resize(width, height)
            AppConfig.WINDOW_WIDTH = width
            AppConfig.WINDOW_HEIGHT = height
        
        # Configurações
        AppConfig.SETTINGS['auto_load'] = self.auto_load_check.isChecked()
        AppConfig.SETTINGS['confirm_generate'] = self.confirm_check.isChecked()
        AppConfig.SETTINGS['show_preview'] = self.preview_check.isChecked()
        
        # Aplicar estilo
        if self.parent:
            self.parent.setStyleSheet(StyleConfig.get_style())
        
        QMessageBox.information(self, '✅ Sucesso', 'Configurações aplicadas!')
        self.close()
    
    def reset_settings(self):
        """Reseta configurações"""
        reply = QMessageBox.question(
            self, '🔄 Resetar',
            'Deseja resetar todas as configurações?',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Resetar cores
            default_colors = {
                'primary': '#00ff41',
                'secondary': '#00aa33',
                'tertiary': '#33ff66',
                'background': '#0a0a0a',
                'background_light': '#0d0d0d',
                'background_dark': '#050505',
                'border': '#1a3a2a',
                'text': '#00ff41',
                'text_secondary': '#888888',
                'text_dark': '#0a0a0a',
                'error': '#ff0044',
                'error_hover': '#ff3366',
            }
            
            for key, value in default_colors.items():
                AppConfig.COLORS[key] = value
                if key in self.color_buttons:
                    self.color_buttons[key].setStyleSheet(f'background-color: {value}; border: 2px solid #00ff41;')
            
            # Resetar tamanhos
            self.width_spin.setValue(1400)
            self.height_spin.setValue(900)
            
            self.theme_combo.setCurrentText('Futurista')
            
            QMessageBox.information(self, '✅ Sucesso', 'Configurações resetadas!')

class MsfvenomGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(AppConfig.THREAD_CONFIG['max_threads'])
        self.all_data = {'payloads': [], 'exploits': [], 'encoders': [], 'formats': [], 'platforms': [], 'archs': []}
        self.is_closing = False
        self.current_selected_type = 'payloads'
        self.current_item_info = {}
        self.initUI()
        self.setup_connections()
        self.load_database()
    
    def initUI(self):
        """Inicializa a interface"""
        self.setWindowTitle(AppConfig.WINDOW_TITLE)
        self.setGeometry(100, 100, AppConfig.WINDOW_WIDTH, AppConfig.WINDOW_HEIGHT)
        self.setMinimumSize(AppConfig.WINDOW_MIN_WIDTH, AppConfig.WINDOW_MIN_HEIGHT)
        
        self.setStyleSheet(StyleConfig.get_style())
        
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(AppConfig.UI_CONFIG['spacing'])
        main_layout.setContentsMargins(
            AppConfig.UI_CONFIG['padding'],
            AppConfig.UI_CONFIG['padding'],
            AppConfig.UI_CONFIG['padding'],
            AppConfig.UI_CONFIG['padding']
        )
        central_widget.setLayout(main_layout)
        
        # Top toolbar
        toolbar = self.create_toolbar()
        main_layout.addLayout(toolbar)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedHeight(AppConfig.UI_CONFIG['progress_height'])
        main_layout.addWidget(self.progress_bar)
        
        # Main content splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(3)
        main_layout.addWidget(splitter)
        
        # Left panel
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        splitter.setSizes(AppConfig.UI_CONFIG['splitter_sizes'])
        
        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.status_label = QLabel('🤖 Sistema Pronto')
        self.statusBar.addWidget(self.status_label)
        
        self.thread_indicator = QLabel('🟢')
        self.statusBar.addPermanentWidget(self.thread_indicator)
        self.thread_count_label = QLabel('0 threads')
        self.statusBar.addPermanentWidget(self.thread_count_label)
        
        self.update_thread_info()
    
    def create_toolbar(self):
        """Cria a barra de ferramentas"""
        layout = QHBoxLayout()
        layout.setSpacing(AppConfig.UI_CONFIG['spacing'])
        
        title = QLabel('⚡ MSFVenom Automation')
        title.setStyleSheet(f'font-size: {AppConfig.FONTS["size_xlarge"]}px; font-weight: bold; color: {AppConfig.COLORS["primary"]};')
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Search
        layout.addWidget(QLabel('🔍 Buscar:'))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Pesquisar...')
        self.search_input.setMinimumWidth(200)
        self.search_input.setMinimumHeight(35)
        layout.addWidget(self.search_input)
        
        # Filter
        layout.addWidget(QLabel('📋 Tipo:'))
        self.type_filter = QComboBox()
        self.type_filter.addItems(['All', 'Payloads', 'Exploits', 'Encoders'])
        self.type_filter.setMinimumHeight(35)
        self.type_filter.currentTextChanged.connect(self.on_type_changed)
        layout.addWidget(self.type_filter)
        
        # Refresh DB
        refresh_btn = QPushButton('🔄 Refresh DB')
        refresh_btn.setFixedHeight(AppConfig.UI_CONFIG['button_height'])
        refresh_btn.clicked.connect(self.refresh_database)
        layout.addWidget(refresh_btn)
        
        # Settings
        settings_btn = QPushButton('⚙️')
        settings_btn.setFixedHeight(AppConfig.UI_CONFIG['button_height'])
        settings_btn.setFixedWidth(AppConfig.UI_CONFIG['button_height'])
        settings_btn.clicked.connect(self.open_settings)
        layout.addWidget(settings_btn)
        
        # Generate
        self.generate_btn = QPushButton('⚡ Generate')
        self.generate_btn.setObjectName('generateBtn')
        self.generate_btn.setFixedHeight(AppConfig.UI_CONFIG['button_height'] + 5)
        self.generate_btn.setMinimumWidth(150)
        self.generate_btn.clicked.connect(self.generate_payload)
        layout.addWidget(self.generate_btn)
        
        return layout
    
    def create_left_panel(self):
        """Cria o painel esquerdo"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel('📦 Itens Disponíveis:'))
        self.item_count_label = QLabel('0 itens')
        self.item_count_label.setStyleSheet(f'color: {AppConfig.COLORS["text_secondary"]};')
        header_layout.addStretch()
        header_layout.addWidget(self.item_count_label)
        layout.addLayout(header_layout)
        
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.ExtendedSelection)
        self.list_widget.itemDoubleClicked.connect(self.show_options_dialog)
        layout.addWidget(self.list_widget)
        
        # Info display
        info_tabs = QTabWidget()
        info_tabs.setMaximumHeight(AppConfig.UI_CONFIG['info_height'])
        
        info_tab = QWidget()
        info_layout = QVBoxLayout()
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        info_tab.setLayout(info_layout)
        info_layout.addWidget(self.info_text)
        info_tabs.addTab(info_tab, 'ℹ️ Informações')
        
        cmd_tab = QWidget()
        cmd_layout = QVBoxLayout()
        self.command_preview = QTextEdit()
        self.command_preview.setReadOnly(True)
        self.command_preview.setStyleSheet('background-color: #0a0a0a; font-family: monospace;')
        cmd_layout.addWidget(self.command_preview)
        cmd_tab.setLayout(cmd_layout)
        info_tabs.addTab(cmd_tab, '💻 Comando')
        
        layout.addWidget(info_tabs)
        
        return widget
    
    def create_right_panel(self):
        """Cria o painel direito"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        tabs = QTabWidget()
        
        # Configurações tab
        config_tab = self.create_config_tab()
        tabs.addTab(config_tab, '⚙️ Configurações')
        
        # Templates tab
        templates_tab = self.create_templates_tab()
        tabs.addTab(templates_tab, '📝 Templates')
        
        # Advanced tab
        advanced_tab = self.create_advanced_tab()
        tabs.addTab(advanced_tab, '🔧 Avançado')
        
        # Database tab
        db_tab = self.create_database_tab()
        tabs.addTab(db_tab, '🗄️ Database')
        
        layout.addWidget(tabs)
        
        return widget
    
    def create_config_tab(self):
        """Cria a aba de configurações"""
        tab = QWidget()
        layout = QGridLayout()
        tab.setLayout(layout)
        
        self.inputs = {}
        self.current_fields = []
        row = 0
        
        fields = [
            ('🌐 LHOST:', 'lhost_input', '192.168.1.100'),
            ('🚪 LPORT:', 'lport_input', '4444'),
            ('🎯 RHOST:', 'rhost_input', ''),
            ('🔌 RPORT:', 'rport_input', ''),
            ('📦 Format:', 'format_input', 'exe'),
            ('💾 Output:', 'output_input', 'payload.exe'),
            ('🔐 Encoder:', 'encoder_input', ''),
            ('🔄 Iterations:', 'iterations_input', '5'),
            ('🖥️ Platform:', 'platform_input', 'windows'),
            ('🏗️ Architecture:', 'arch_input', 'x86'),
        ]
        
        for label_text, attr_name, default_value in fields:
            label = QLabel(label_text)
            label.setStyleSheet('font-weight: bold; font-size: 12px;')
            input_field = QLineEdit()
            input_field.setText(default_value)
            input_field.setPlaceholderText(f'Digite {label_text.replace(":", "").strip()}')
            input_field.setMinimumHeight(AppConfig.UI_CONFIG['input_height'])
            
            layout.addWidget(label, row, 0)
            layout.addWidget(input_field, row, 1)
            
            self.inputs[attr_name] = input_field
            self.current_fields.append(attr_name)
            row += 1
        
        # Opções extras
        layout.addWidget(QLabel('📝 Opções Extras:'), row, 0)
        self.extra_options = QTextEdit()
        self.extra_options.setPlaceholderText('Exemplo: -b "\\x00" --smallest')
        self.extra_options.setMaximumHeight(60)
        layout.addWidget(self.extra_options, row, 1)
        
        return tab
    
    def create_templates_tab(self):
        """Cria a aba de templates"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        templates_group = QGroupBox('📋 Templates')
        templates_layout = QVBoxLayout()
        
        self.template_combo = QComboBox()
        templates = list(AppConfig.TEMPLATES.keys()) + ['Custom']
        self.template_combo.addItems(templates)
        self.template_combo.setMinimumHeight(35)
        self.template_combo.currentTextChanged.connect(self.load_template)
        templates_layout.addWidget(self.template_combo)
        
        self.template_desc = QTextEdit()
        self.template_desc.setReadOnly(True)
        self.template_desc.setMaximumHeight(100)
        self.template_desc.setStyleSheet(f'background-color: {AppConfig.COLORS["background"]}; color: {AppConfig.COLORS["text_secondary"]};')
        self.template_desc.setPlainText('Selecione um template')
        templates_layout.addWidget(self.template_desc)
        
        templates_group.setLayout(templates_layout)
        layout.addWidget(templates_group)
        
        layout.addStretch()
        
        return tab
    
    def create_advanced_tab(self):
        """Cria a aba avançada"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        checkbox_group = QGroupBox('🚀 Opções')
        checkbox_layout = QGridLayout()
        
        self.checkboxes = {}
        for i, (text, attr, flag) in enumerate(AppConfig.ADVANCED_OPTIONS):
            checkbox = QCheckBox(text)
            checkbox.setObjectName(flag)
            checkbox.setStyleSheet('padding: 5px;')
            row = i // 2
            col = i % 2
            checkbox_layout.addWidget(checkbox, row, col)
            self.checkboxes[attr] = checkbox
        
        checkbox_group.setLayout(checkbox_layout)
        layout.addWidget(checkbox_group)
        
        layout.addWidget(QLabel('🏴 Flags Custom:'))
        self.custom_flags = QLineEdit()
        self.custom_flags.setPlaceholderText('--add-flag1 --add-flag2')
        self.custom_flags.setMinimumHeight(AppConfig.UI_CONFIG['input_height'])
        layout.addWidget(self.custom_flags)
        
        layout.addStretch()
        
        return tab
    
    def create_database_tab(self):
        """Cria a aba do banco de dados"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Informações do DB
        info_group = QGroupBox('📊 Informações do Database')
        info_layout = QGridLayout()
        
        info_layout.addWidget(QLabel('📁 Pasta:'), 0, 0)
        db_path_label = QLabel(db_manager.db_path)
        db_path_label.setStyleSheet(f'color: {AppConfig.COLORS["text_secondary"]};')
        info_layout.addWidget(db_path_label, 0, 1)
        
        info_layout.addWidget(QLabel('📄 Arquivos:'), 1, 0)
        files_list = []
        for cmd in ['payloads', 'exploits', 'encoders', 'formats', 'platforms', 'archs']:
            file_path = db_manager._get_file_path(cmd)
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                files_list.append(f'{cmd}.txt ({size} bytes)')
            else:
                files_list.append(f'{cmd}.txt (não criado)')
        
        files_label = QLabel('\n'.join(files_list))
        files_label.setStyleSheet(f'color: {AppConfig.COLORS["text_secondary"]}; font-size: 10px;')
        info_layout.addWidget(files_label, 1, 1)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Botões de ação
        btn_group = QGroupBox('🛠️ Ações')
        btn_layout = QVBoxLayout()
        
        generate_all_btn = QPushButton('📥 Gerar Todos os Arquivos')
        generate_all_btn.setMinimumHeight(35)
        generate_all_btn.clicked.connect(self.generate_all_db_files)
        btn_layout.addWidget(generate_all_btn)
        
        clear_db_btn = QPushButton('🗑️ Limpar Database')
        clear_db_btn.setMinimumHeight(35)
        clear_db_btn.clicked.connect(self.clear_database)
        btn_layout.addWidget(clear_db_btn)
        
        btn_group.setLayout(btn_layout)
        layout.addWidget(btn_group)
        
        # Status
        self.db_status_label = QLabel('✅ Database pronto')
        self.db_status_label.setStyleSheet(f'color: {AppConfig.COLORS["success"]};')
        layout.addWidget(self.db_status_label)
        
        layout.addStretch()
        
        return tab
    
    def setup_connections(self):
        """Configura conexões"""
        self.search_input.textChanged.connect(self.filter_list)
        self.type_filter.currentTextChanged.connect(self.filter_list)
        self.list_widget.itemClicked.connect(self.on_item_selected)
        self.template_combo.currentTextChanged.connect(self.load_template)
    
    def load_database(self):
        """Carrega o banco de dados"""
        self.set_controls_enabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        
        self.update_status('📥 Carregando database...')
        
        try:
            # Carregar todas as listas
            data = db_manager.get_all_lists()
            
            for key, value in data.items():
                if key in self.all_data:
                    self.all_data[key] = value
            
            self.update_list()
            self.item_count_label.setText(f'{self.list_widget.count()} itens')
            total_items = sum(len(v) for v in self.all_data.values())
            self.update_status(f'✅ Database carregado: {total_items} itens')
            
        except Exception as e:
            self.show_error(f'Erro ao carregar database: {str(e)}')
        
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 100)
        self.set_controls_enabled(True)
    
    def refresh_database(self):
        """Atualiza o banco de dados"""
        reply = QMessageBox.question(
            self, '🔄 Atualizar Database',
            'Deseja atualizar todos os arquivos do database?',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.load_database()
    
    def generate_all_db_files(self):
        """Gera todos os arquivos do database"""
        reply = QMessageBox.question(
            self, '📥 Gerar Database',
            'Deseja gerar todos os arquivos do database?',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.set_controls_enabled(False)
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)
            
            commands = ['payloads', 'exploits', 'encoders', 'formats', 'platforms', 'archs']
            total = len(commands)
            current = 0            
            for cmd in commands:
                current += 1
                self.update_status(f'📥 Gerando {cmd}.txt... ({current}/{total})')
                
                try:
                    db_manager.get_or_create_list(cmd, force_update=True)
                except Exception as e:
                    print(f'Erro ao gerar {cmd}.txt: {str(e)}')
            
            # Recarregar dados
            self.load_database()
            self.update_status('✅ Todos os arquivos gerados!')
            self.progress_bar.setVisible(False)
            self.set_controls_enabled(True)
    
    def clear_database(self):
        """Limpa o database"""
        reply = QMessageBox.question(
            self, '🗑️ Limpar Database',
            'Deseja remover todos os arquivos do database?',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            import shutil
            try:
                if os.path.exists(db_manager.db_path):
                    shutil.rmtree(db_manager.db_path)
                    os.makedirs(db_manager.db_path)
                    db_manager.clear_cache()
                    self.update_status('🗑️ Database limpo!')
                    self.load_database()
            except Exception as e:
                self.show_error(f'Erro ao limpar database: {str(e)}')
    
    def on_type_changed(self, text):
        """Muda os campos baseado no tipo selecionado"""
        pass
    
    def update_list(self):
        """Atualiza a lista de itens"""
        self.list_widget.clear()
        
        search_text = self.search_input.text().lower()
        filter_type = self.type_filter.currentText()
        
        type_mapping = {
            'Payloads': 'payloads',
            'Exploits': 'exploits',
            'Encoders': 'encoders'
        }
        
        for type_name, items in self.all_data.items():
            if filter_type != 'All':
                mapped = type_mapping.get(filter_type, '')
                if type_name != mapped:
                    continue
            
            # Pular tipos que não são para exibição
            if type_name in ['formats', 'platforms', 'archs'] and filter_type == 'All':
                continue
            
            sorted_items = sorted(items)
            icon_map = {
                'payloads': '🚀',
                'exploits': '⚡',
                'encoders': '🔐',
                'formats': '📦',
                'platforms': '🖥️',
                'archs': '🏗️'
            }
            icon = icon_map.get(type_name, '📄')
            
            for item in sorted_items:
                if search_text and search_text not in item.lower():
                    continue
                
                display_text = f'{icon} {item}'
                list_item = QListWidgetItem(display_text)
                list_item.setData(Qt.UserRole, {'type': type_name, 'name': item})
                self.list_widget.addItem(list_item)
    
    def filter_list(self):
        """Filtra a lista"""
        self.update_list()
        self.item_count_label.setText(f'{self.list_widget.count()} itens')
    
    # Em MsfvenomGUI, atualize o método on_item_selected:
    def on_item_selected(self, item):
        """Item selecionado"""
        data = item.data(Qt.UserRole)
        if not data:
            return
        
        self.current_selected_type = data['type']
        item_name = data['name']
        
        # Mostrar informações básicas
        self.info_text.setText(f'📌 {item_name}\n\n🔄 Carregando informações...')
        
        # Buscar informações - agora suporta todos os tipos
        info = db_manager.get_item_info(data['type'], item_name)
        
        if 'error' in info:
            self.info_text.setText(f'📌 {item_name}\n\n⚠️ {info["error"]}')
            return
        
        # Mostrar informações
        info_text = f'📌 {item_name}\n\n'
        
        if info.get('description'):
            info_text += f'📝 {info["description"]}\n\n'
        
        if info.get('basic_options'):
            info_text += '⚙️ Opções Básicas:\n'
            for opt in info['basic_options']:
                req = '✅' if opt.get('required', '').lower() == 'yes' else '⬜'
                desc = opt.get('description', '')
                current = opt.get('current_setting', '')
                info_text += f'  {req} {opt["name"]}'
                if current:
                    info_text += f' [{current}]'
                info_text += f': {desc}\n'
            info_text += '\n'
        
        if info.get('required_options'):
            info_text += f'📌 Required: {", ".join(info["required_options"])}\n'
        
        self.info_text.setText(info_text)
        self.current_item_info = info

# Atualize o método show_options_dialog:

    def show_options_dialog(self, item):
        """Mostra diálogo de opções (duplo clique)"""
        data = item.data(Qt.UserRole)
        if not data:
            return
        
        # Buscar informações - agora suporta todos os tipos
        info = db_manager.get_item_info(data['type'], data['name'])
        
        if 'error' in info:
            self.show_error(info['error'])
            return
        
        # Mostrar diálogo
        dialog = OptionsDialog(data['type'], data['name'], info, self)
        if dialog.exec_() == QDialog.Accepted:
            values = dialog.values
            
            for key, value in values.items():
                if value:
                    if key == 'LHOST' and 'lhost_input' in self.inputs:
                        self.inputs['lhost_input'].setText(value)
                    elif key == 'LPORT' and 'lport_input' in self.inputs:
                        self.inputs['lport_input'].setText(value)
                    elif key == 'RHOST' and 'rhost_input' in self.inputs:
                        self.inputs['rhost_input'].setText(value)
                    elif key == 'RPORT' and 'rport_input' in self.inputs:
                        self.inputs['rport_input'].setText(value)
                    elif key == 'PAYLOAD' and data['type'] == 'exploits':
                        self.search_and_select_payload(value)
                    elif key == 'AndroidHideAppIcon' and 'format_input' in self.inputs:
                        # Se for Android, adicionar flag
                        if value.lower() == 'true':
                            self.extra_options.append('--android-hide-app-icon')
                                
    def search_and_select_payload(self, payload_name):
        """Busca e seleciona um payload na lista"""
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            data = item.data(Qt.UserRole)
            if data and data['type'] == 'payloads' and data['name'] == payload_name:
                self.list_widget.setCurrentItem(item)
                self.on_item_selected(item)
                break
    
    def load_template(self, template_name):
        """Carrega template"""
        if template_name in AppConfig.TEMPLATES:
            template = AppConfig.TEMPLATES[template_name]
            self.template_desc.setPlainText(template['desc'])
            
            for field, value in template['values'].items():
                if field in self.inputs:
                    self.inputs[field].setText(value)
            
            self.search_template_payload(template_name)
        else:
            self.template_desc.setPlainText('Configuração personalizada')
    
    def search_template_payload(self, template_name):
        """Busca payload do template"""
        search_map = {
            'Windows Reverse TCP': 'windows/meterpreter/reverse_tcp',
            'Windows Reverse HTTPS': 'windows/meterpreter/reverse_https',
            'Linux Reverse TCP': 'linux/x86/shell_reverse_tcp',
            'Android Reverse TCP': 'android/meterpreter/reverse_tcp',
            'Python Reverse TCP': 'python/meterpreter/reverse_tcp',
            'PHP Reverse TCP': 'php/meterpreter_reverse_tcp'
        }
        
        if template_name in search_map:
            payload = search_map[template_name]
            for i in range(self.list_widget.count()):
                item = self.list_widget.item(i)
                data = item.data(Qt.UserRole)
                if data and data['name'] == payload:
                    self.list_widget.setCurrentItem(item)
                    self.on_item_selected(item)
                    break
    
    def generate_payload(self):
        """Gera payload"""
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, '⚠️ Aviso', 'Selecione um payload/exploit')
            return
        
        cmd = self.build_command(selected_items[0])
        self.command_preview.setText(' '.join(cmd))
        
        if AppConfig.SETTINGS.get('confirm_generate', True):
            reply = QMessageBox.question(
                self, '🚀 Confirmar',
                f'Executar?\n\n{" ".join(cmd)}',
                QMessageBox.Yes | QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return
        
        self.execute_command(cmd)
    
    def build_command(self, selected_item):
        """Constrói comando"""
        cmd = ['msfvenom']
        
        data = selected_item.data(Qt.UserRole)
        if data['type'] == 'payloads':
            cmd.extend(['-p', data['name']])
        elif data['type'] == 'exploits':
            cmd.extend(['-e', data['name']])
        elif data['type'] == 'encoders':
            cmd.extend(['-e', data['name']])
        
        # Opções
        options = {
            'lhost_input': 'LHOST',
            'lport_input': 'LPORT',
            'rhost_input': 'RHOST',
            'rport_input': 'RPORT'
        }
        
        for field, flag in options.items():
            if field in self.inputs and self.inputs[field].text():
                cmd.append(f'{flag}={self.inputs[field].text()}')
        
        # Format e output
        if 'format_input' in self.inputs and self.inputs['format_input'].text():
            cmd.extend(['-f', self.inputs['format_input'].text()])
        if 'output_input' in self.inputs and self.inputs['output_input'].text():
            cmd.extend(['-o', self.inputs['output_input'].text()])
        if 'encoder_input' in self.inputs and self.inputs['encoder_input'].text():
            cmd.extend(['-e', self.inputs['encoder_input'].text()])
        if 'iterations_input' in self.inputs and self.inputs['iterations_input'].text():
            cmd.extend(['-i', self.inputs['iterations_input'].text()])
        if 'platform_input' in self.inputs and self.inputs['platform_input'].text():
            cmd.extend(['--platform', self.inputs['platform_input'].text()])
        if 'arch_input' in self.inputs and self.inputs['arch_input'].text():
            cmd.extend(['-a', self.inputs['arch_input'].text()])
        
        # Extra options
        if hasattr(self, 'extra_options') and self.extra_options.toPlainText():
            extra = self.extra_options.toPlainText().split()
            cmd.extend(extra)
        
        # Checkboxes
        for attr, checkbox in self.checkboxes.items():
            if checkbox.isChecked():
                cmd.append(checkbox.objectName())
        
        # Custom flags
        if self.custom_flags.text():
            custom = self.custom_flags.text().split()
            cmd.extend(custom)
        
        return cmd
    
    def execute_command(self, cmd):
        """Executa comando"""
        try:
            self.update_status('⏳ Executando comando...')
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(timeout=AppConfig.THREAD_CONFIG['timeout_generate'])
            
            if process.returncode == 0:
                # Salvar saída em arquivo
                output_file = self.inputs.get('output_input', QLineEdit()).text()
                if output_file:
                    with open(output_file, 'wb') as f:
                        f.write(stdout.encode('utf-8') if stdout else b'')
                
                QMessageBox.information(
                    self, '✅ Sucesso!',
                    f'Payload gerado com sucesso!\n\nArquivo: {output_file}\nTamanho: {len(stdout)} bytes'
                )
                self.update_status('✅ Payload gerado com sucesso!')
            else:
                self.show_error(stderr)
                
        except subprocess.TimeoutExpired:
            process.kill()
            self.show_error('⏰ Timeout ao gerar payload')
        except Exception as e:
            self.show_error(str(e))
    
    def open_settings(self):
        """Abre diálogo de configurações"""
        dialog = SettingsDialog(self)
        dialog.exec_()
    
    def set_controls_enabled(self, enabled):
        """Habilita/desabilita controles"""
        self.generate_btn.setEnabled(enabled)
        self.list_widget.setEnabled(enabled)
        self.search_input.setEnabled(enabled)
        self.type_filter.setEnabled(enabled)
    
    def update_status(self, message):
        """Atualiza status"""
        self.status_label.setText(f'🤖 {message}')
    
    def show_error(self, error_msg):
        """Mostra erro"""
        QMessageBox.critical(self, '❌ Erro', str(error_msg))
        self.update_status(f'Erro: {error_msg}')
    
    def update_thread_info(self):
        """Atualiza info de threads"""
        active = self.threadpool.activeThreadCount()
        self.thread_count_label.setText(f'{active} threads')
        self.thread_indicator.setText('🟢' if active == 0 else '🟡')
    
    def closeEvent(self, event):
        """Fechamento"""
        self.is_closing = True
        
        if self.threadpool.activeThreadCount() > 0:
            reply = QMessageBox.question(
                self, '⚠️ Atenção',
                'Tarefas em execução. Esperar ou encerrar?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            
            if reply == QMessageBox.Yes:
                self.threadpool.waitForDone(AppConfig.THREAD_CONFIG['wait_timeout'])
            else:
                self.threadpool.clear()
        
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    app.aboutToQuit.connect(lambda: print("\n🔚 Encerrando..."))
    
    window = MsfvenomGUI()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
