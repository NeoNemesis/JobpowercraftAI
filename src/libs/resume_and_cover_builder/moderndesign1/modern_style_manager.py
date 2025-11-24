"""
ModernDesign1StyleManager - SAMMA INTERFACE som StyleManager
Men hanterar Modern Design 1 stilar
"""

from pathlib import Path
from loguru import logger

class ModernDesign1StyleManager:
    """
    Modern Design 1 Style Manager - SAMMA INTERFACE som StyleManager
    Men returnerar alltid Modern Design 1 CSS-fil
    """
    
    def __init__(self):
        self.selected_style = None
        logger.debug("🎨 ModernDesign1StyleManager initialiserad")
    
    def set_selected_style(self, style_name: str):
        """
        Sätt vald stil - SAMMA INTERFACE som StyleManager
        
        Args:
            style_name: Stilnamn (ignoreras för Modern Design 1)
        """
        self.selected_style = style_name
        logger.info(f"🎨 Modern Design 1: Stil satt till '{style_name}' (använder alltid Modern Design 1 CSS)")
    
    def get_selected_style_path(self) -> Path:
        """
        Hämta sökväg till vald stil - SAMMA INTERFACE som StyleManager
        
        Returns:
            Path: Dummy sökväg (CSS är inbäddad i modern_template.html)
        """
        # Modern Design 1 använder inbäddad CSS i modern_template.html
        # Returnera dummy-sökväg för kompatibilitet
        dummy_path = Path(__file__).parent / "modern_template.html"
        logger.debug(f"🎨 Modern Design 1: CSS är inbäddad i template, returnerar dummy-sökväg: {dummy_path}")
        return dummy_path
    
    def get_style_path(self) -> Path:
        """
        Hämta sökväg till vald stil - EXAKT SAMMA METOD-NAMN som StyleManager
        
        Returns:
            Path: Sökväg till Modern Design 1 CSS-fil
        """
        return self.get_selected_style_path()
    
    def get_available_styles(self) -> list:
        """
        Hämta tillgängliga stilar - SAMMA INTERFACE som StyleManager
        
        Returns:
            list: Lista med Modern Design 1 stil
        """
        return ["Modern Design 1"]
