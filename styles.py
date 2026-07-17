# styles.py
from config import StyleConfig

class FuturisticStyle:
    """Tema Black Futurista usando config.py"""
    
    @staticmethod
    def get_style():
        """Retorna o estilo da aplicação"""
        return StyleConfig.get_style()
