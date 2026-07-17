# config.py
"""Arquivo de configuração da aplicação MSFVenom GUI"""

class AppConfig:
    """Configurações da aplicação"""
    
    # Configurações da Janela
    WINDOW_TITLE = "MSFVenom Automation Tool - Futuristic Edition"
    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 900
    WINDOW_MIN_WIDTH = 1000
    WINDOW_MIN_HEIGHT = 700
    
    # Configurações de Cores - Tema Futurista
    COLORS = {
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
        'success': '#00ff41',
        'warning': '#ffaa00',
        'info': '#00aaff',
    }
    
    # Configurações de Fontes
    FONTS = {
        'family': 'Monospace',
        'size_small': 10,
        'size_normal': 11,
        'size_medium': 12,
        'size_large': 14,
        'size_xlarge': 18,
    }
    
    # Configurações de Threads
    THREAD_CONFIG = {
        'timeout_payloads': 60,
        'timeout_exploits': 30,
        'timeout_generate': 60,
        'timeout_info': 20,
        'max_threads': 10,
        'wait_timeout': 5000,
    }
    
    # Configurações de UI
    UI_CONFIG = {
        'splitter_sizes': [500, 900],
        'info_height': 200,
        'progress_height': 25,
        'button_height': 40,
        'input_height': 30,
        'padding': 15,
        'spacing': 10,
        'border_radius': 8,
    }
    
    # Configurações de Payloads
    PAYLOAD_CONFIG = {
        'default_lhost': '192.168.1.100',
        'default_lport': '4444',
        'default_format': 'exe',
        'default_output': 'payload.exe',
        'default_platform': 'windows',
        'default_arch': 'x86',
        'default_shell': 'cmd',
        'default_iterations': '5',
    }
    
    # Templates de Payloads
    TEMPLATES = {
        'Windows Reverse TCP': {
            'desc': 'Payload Windows Reverse TCP padrão\nLHOST: IP do atacante\nLPORT: Porta de conexão',
            'values': {
                'format_input': 'exe',
                'output_input': 'payload.exe',
                'platform_input': 'windows',
                'arch_input': 'x86',
                'lhost_input': '',
                'lport_input': '4444'
            }
        },
        'Windows Reverse HTTPS': {
            'desc': 'Payload Windows Reverse HTTPS (ofuscado)\nLHOST: IP do atacante\nLPORT: Porta HTTPS',
            'values': {
                'format_input': 'exe',
                'output_input': 'payload_https.exe',
                'platform_input': 'windows',
                'arch_input': 'x86',
                'lhost_input': '',
                'lport_input': '443'
            }
        },
        'Linux Reverse TCP': {
            'desc': 'Payload Linux Reverse TCP\nLHOST: IP do atacante\nLPORT: Porta de conexão',
            'values': {
                'format_input': 'elf',
                'output_input': 'payload.elf',
                'platform_input': 'linux',
                'arch_input': 'x86',
                'lhost_input': '',
                'lport_input': '4444'
            }
        },
        'Android Reverse TCP': {
            'desc': 'Payload Android Reverse TCP\nLHOST: IP do atacante\nLPORT: Porta de conexão',
            'values': {
                'format_input': 'apk',
                'output_input': 'payload.apk',
                'platform_input': 'android',
                'arch_input': 'dalvik',
                'lhost_input': '',
                'lport_input': '4444'
            }
        },
        'Python Reverse TCP': {
            'desc': 'Payload Python Reverse TCP\nLHOST: IP do atacante\nLPORT: Porta de conexão',
            'values': {
                'format_input': 'py',
                'output_input': 'payload.py',
                'platform_input': 'python',
                'arch_input': 'python',
                'lhost_input': '',
                'lport_input': '4444'
            }
        },
        'PHP Reverse TCP': {
            'desc': 'Payload PHP Reverse TCP\nLHOST: IP do atacante\nLPORT: Porta de conexão',
            'values': {
                'format_input': 'php',
                'output_input': 'payload.php',
                'platform_input': 'php',
                'arch_input': 'php',
                'lhost_input': '',
                'lport_input': '4444'
            }
        }
    }
    
    # Opções específicas para Android (fora do TEMPLATES)
    ANDROID_OPTIONS = {
        'AndroidHideAppIcon': {
            'flag': '--android-hide-app-icon',
            'description': 'Hide the application icon automatically after launch'
        },
        'AutoRunScript': {
            'flag': '--auto-run-script',
            'description': 'A script to run automatically on session creation'
        },
        'AutoVerifySession': {
            'flag': '--auto-verify-session',
            'description': 'Automatically verify and setup the session'
        }
    }
    
    # Opções Avançadas
    ADVANCED_OPTIONS = [
        ('🔒 Disable NX', 'disable_nx', '-N'),
        ('🎯 Disable ASLR', 'disable_aslr', '-A'),
        ('🔐 Use SSL', 'use_ssl', '--ssl'),
        ('📢 Verbose Output', 'verbose', '-v'),
        ('💾 Keep Original', 'keep', '-k'),
        ('🛡️ Disable DEP', 'disable_dep', '-D'),
    ]
    
    # Campos para Payloads
    PAYLOAD_FIELDS = [
        ('🌐 LHOST:', 'lhost_input', 'default_lhost'),
        ('🚪 LPORT:', 'lport_input', 'default_lport'),
        ('🎯 RHOST:', 'rhost_input', ''),
        ('🔌 RPORT:', 'rport_input', ''),
        ('📦 Format:', 'format_input', 'default_format'),
        ('💾 Output:', 'output_input', 'default_output'),
        ('🔐 Encoder:', 'encoder_input', ''),
        ('🔄 Iterations:', 'iterations_input', 'default_iterations'),
        ('🖥️ Platform:', 'platform_input', 'default_platform'),
        ('🏗️ Architecture:', 'arch_input', 'default_arch'),
        ('🐚 Shell Type:', 'shell_input', 'default_shell'),
    ]
    
    # Campos para Exploits
    EXPLOIT_FIELDS = [
        ('🎯 RHOST:', 'rhost_input', ''),
        ('🔌 RPORT:', 'rport_input', ''),
        ('🌐 LHOST:', 'lhost_input', 'default_lhost'),
        ('🚪 LPORT:', 'lport_input', 'default_lport'),
        ('🔐 Encoder:', 'encoder_input', ''),
        ('🔄 Iterations:', 'iterations_input', 'default_iterations'),
        ('🖥️ Platform:', 'platform_input', 'default_platform'),
        ('🏗️ Architecture:', 'arch_input', 'default_arch'),
        ('📦 Format:', 'format_input', 'default_format'),
        ('💾 Output:', 'output_input', 'payload.exe'),
    ]
    
    # Formatos de saída disponíveis
    OUTPUT_FORMATS = [
        'exe', 'elf', 'apk', 'py', 'php', 'raw', 'c', 'ruby',
        'perl', 'ps1', 'vba', 'vbs', 'hex', 'jar', 'class',
        'war', 'asp', 'aspx', 'jsp', 'jspx', 'pl', 'pm',
        'rb', 'sh', 'bash', 'zsh', 'fish', 'cmd', 'bat',
        'ps1', 'psm1', 'psd1', 'psrc', 'xml', 'yaml',
        'json', 'csv', 'tsv', 'html', 'htm', 'js',
        'dll', 'so', 'dylib', 'sys', 'bin', 'dat'
    ]
    
    # Configurações de Ajustes
    SETTINGS = {
        'window_width': WINDOW_WIDTH,
        'window_height': WINDOW_HEIGHT,
        'theme': 'futuristic',
        'auto_load': True,
        'show_preview': True,
        'confirm_generate': True,
        'save_history': True,
    }

class StyleConfig:
    """Configurações de estilo para a aplicação"""
    
    @staticmethod
    def get_style():
        """Retorna o CSS baseado nas cores do AppConfig"""
        colors = AppConfig.COLORS
        fonts = AppConfig.FONTS
        ui = AppConfig.UI_CONFIG
        
        return f"""
        QMainWindow {{
            background-color: {colors['background']};
            color: {colors['text']};
        }}
        
        QWidget {{
            background-color: {colors['background_light']};
            color: {colors['text']};
            font-family: '{fonts['family']}';
            font-size: {fonts['size_normal']}px;
        }}
        
        QMenuBar {{
            background-color: {colors['background_dark']};
            color: {colors['text']};
            border-bottom: 1px solid {colors['border']};
            padding: 5px;
        }}
        
        QMenuBar::item {{
            background-color: transparent;
            padding: 5px 15px;
            color: {colors['text']};
        }}
        
        QMenuBar::item:selected {{
            background-color: {colors['primary']};
            color: {colors['text_dark']};
        }}
        
        QMenu {{
            background-color: {colors['background_dark']};
            border: 1px solid {colors['primary']};
            color: {colors['text']};
        }}
        
        QMenu::item:selected {{
            background-color: {colors['primary']};
            color: {colors['text_dark']};
        }}
        
        QPushButton {{
            background-color: {colors['secondary']};
            color: {colors['text_dark']};
            border: 2px solid {colors['primary']};
            border-radius: {ui['border_radius']}px;
            padding: 8px 16px;
            font-weight: bold;
            font-size: {fonts['size_medium']}px;
        }}
        
        QPushButton:hover {{
            background-color: {colors['tertiary']};
            border-color: {colors['tertiary']};
        }}
        
        QPushButton:pressed {{
            background-color: {colors['secondary']};
            border-color: {colors['secondary']};
        }}
        
        QPushButton:disabled {{
            background-color: #333333;
            color: #666666;
            border-color: #444444;
        }}
        
        QPushButton#generateBtn {{
            background-color: {colors['error']};
            border-color: {colors['error']};
            font-size: {fonts['size_large']}px;
            font-weight: bold;
            color: #ffffff;
        }}
        
        QPushButton#generateBtn:hover {{
            background-color: {colors['error_hover']};
            border-color: {colors['error_hover']};
        }}
        
        QLineEdit, QTextEdit, QPlainTextEdit {{
            background-color: {colors['background']};
            color: {colors['text']};
            border: 2px solid {colors['border']};
            border-radius: 5px;
            padding: 6px 10px;
            font-family: '{fonts['family']}';
            font-size: {fonts['size_normal']}px;
            selection-background-color: {colors['primary']};
            selection-color: {colors['text_dark']};
        }}
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            border-color: {colors['primary']};
        }}
        
        QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover {{
            border-color: {colors['secondary']};
        }}
        
        QComboBox {{
            background-color: {colors['background']};
            color: {colors['text']};
            border: 2px solid {colors['border']};
            border-radius: 5px;
            padding: 6px 10px;
            font-family: '{fonts['family']}';
        }}
        
        QComboBox:hover {{
            border-color: {colors['primary']};
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {colors['background']};
            color: {colors['text']};
            border: 2px solid {colors['primary']};
            selection-background-color: {colors['primary']};
            selection-color: {colors['text_dark']};
        }}
        
        QListWidget {{
            background-color: {colors['background']};
            color: {colors['text']};
            border: 2px solid {colors['border']};
            border-radius: 5px;
            padding: 5px;
            font-family: '{fonts['family']}';
            font-size: {fonts['size_normal']}px;
        }}
        
        QListWidget::item {{
            padding: 6px 8px;
            border-radius: 3px;
            margin: 1px 0;
        }}
        
        QListWidget::item:selected {{
            background-color: {colors['primary']};
            color: {colors['text_dark']};
            font-weight: bold;
        }}
        
        QListWidget::item:hover:!selected {{
            background-color: {colors['border']};
        }}
        
        QScrollBar:vertical {{
            background-color: {colors['background']};
            border: 1px solid {colors['border']};
            border-radius: 5px;
            width: 10px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {colors['primary']};
            border-radius: 5px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {colors['tertiary']};
        }}
        
        QScrollBar:horizontal {{
            background-color: {colors['background']};
            border: 1px solid {colors['border']};
            border-radius: 5px;
            height: 10px;
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {colors['primary']};
            border-radius: 5px;
            min-width: 20px;
        }}
        
        QTabWidget::pane {{
            background-color: {colors['background_light']};
            border: 2px solid {colors['border']};
            border-radius: 5px;
            padding: 10px;
        }}
        
        QTabBar::tab {{
            background-color: {colors['background']};
            color: {colors['text']};
            border: 2px solid {colors['border']};
            border-bottom: none;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
            padding: 8px 16px;
            margin-right: 3px;
            font-family: '{fonts['family']}';
            font-weight: bold;
        }}
        
        QTabBar::tab:selected {{
            background-color: {colors['primary']};
            color: {colors['text_dark']};
            border-color: {colors['primary']};
        }}
        
        QTabBar::tab:hover:!selected {{
            background-color: {colors['border']};
            border-color: {colors['secondary']};
        }}
        
        QCheckBox {{
            color: {colors['text']};
            spacing: 8px;
            padding: 4px;
        }}
        
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            background-color: {colors['background']};
            border: 2px solid {colors['border']};
            border-radius: 4px;
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {colors['primary']};
            border-color: {colors['primary']};
        }}
        
        QCheckBox::indicator:hover {{
            border-color: {colors['primary']};
        }}
        
        QGroupBox {{
            border: 2px solid {colors['border']};
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 12px;
            font-weight: bold;
            color: {colors['text']};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 20px;
            padding: 0 10px;
            background-color: {colors['background_light']};
            color: {colors['text']};
        }}
        
        QStatusBar {{
            background-color: {colors['background']};
            color: {colors['text']};
            border-top: 1px solid {colors['border']};
            padding: 3px;
        }}
        
        QStatusBar::item {{
            border: none;
        }}
        
        QLabel {{
            color: {colors['text']};
            font-family: '{fonts['family']}';
            font-weight: bold;
        }}
        
        QProgressBar {{
            background-color: {colors['background']};
            border: 2px solid {colors['border']};
            border-radius: 5px;
            text-align: center;
            color: {colors['text']};
            font-weight: bold;
        }}
        
        QProgressBar::chunk {{
            background-color: {colors['primary']};
            border-radius: 3px;
        }}
        
        QToolTip {{
            background-color: {colors['background']};
            color: {colors['text']};
            border: 1px solid {colors['primary']};
            padding: 4px;
            font-family: '{fonts['family']}';
        }}
        
        QSplitter::handle {{
            background-color: {colors['border']};
            width: 2px;
        }}
        
        QSplitter::handle:hover {{
            background-color: {colors['primary']};
        }}
        
        QDialog {{
            background-color: {colors['background_light']};
        }}
        """
