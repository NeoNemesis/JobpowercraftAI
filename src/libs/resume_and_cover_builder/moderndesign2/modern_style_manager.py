"""
ModernDesign2StyleManager - SAMMA INTERFACE som StyleManager
Men hanterar Modern Design 2 stilar
"""

from pathlib import Path
from loguru import logger

class ModernDesign2StyleManager:
    """
    Modern Design 2 Style Manager - SAMMA INTERFACE som StyleManager
    Men returnerar alltid Modern Design 2 CSS-fil
    """
    
    def __init__(self):
        self.selected_style = None
        logger.debug("🎨 ModernDesign2StyleManager initialiserad")
    
    def set_selected_style(self, style_name: str):
        """
        Sätt vald stil - SAMMA INTERFACE som StyleManager
        
        Args:
            style_name: Stilnamn (ignoreras för Modern Design 2)
        """
        self.selected_style = style_name
        logger.info(f"🎨 Modern Design 2: Stil satt till '{style_name}' (använder kreativ sidopanel-design)")
    
    def get_selected_style_path(self) -> Path:
        """
        Hämta sökväg till vald stil - SAMMA INTERFACE som StyleManager
        
        Returns:
            Path: Dummy sökväg (CSS är i template)
        """
        dummy_path = Path(__file__).parent / "improved_template.html"
        logger.debug(f"🎨 Modern Design 2: CSS är i template, returnerar dummy-sökväg: {dummy_path}")
        return dummy_path
    
    def get_style_path(self) -> Path:
        """
        Hämta sökväg till vald stil - EXAKT SAMMA METOD-NAMN som StyleManager
        
        Returns:
            Path: Sökväg till Modern Design 2 CSS-fil
        """
        return self.get_selected_style_path()
    
    def get_available_styles(self) -> list:
        """
        Hämta tillgängliga stilar - SAMMA INTERFACE som StyleManager
        
        Returns:
            list: Lista med Modern Design 2 stil
        """
        return ["Modern Design 2 - Creative Bold"]


