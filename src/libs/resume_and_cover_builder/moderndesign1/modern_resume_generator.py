"""
ModernDesign1ResumeGenerator - SAMMA INTERFACE som ResumeGenerator
Men använder Modern Design 1 AI-generator
"""

from pathlib import Path
from typing import Any
from loguru import logger
# ai_generator borttagen - använder nu smart_data_generator via facade

class ModernDesign1ResumeGenerator:
    """
    Modern Design 1 Resume Generator - SAMMA INTERFACE som ResumeGenerator
    Men använder ModernDesign1Generator internt
    """
    
    def __init__(self):
        self.resume_object = None
        logger.debug("🎨 ModernDesign1ResumeGenerator initialiserad")
    
    def set_resume_object(self, resume_object):
        """
        Sätt resume object - SAMMA INTERFACE som ResumeGenerator
        
        Args:
            resume_object: Resume object
        """
        self.resume_object = resume_object
        logger.debug("🎨 Modern Design 1: Resume object satt")
    
    def create_resume(self, style_path: Path) -> str:
        """
        Skapa CV - SAMMA INTERFACE som ResumeGenerator
        
        Args:
            style_path: Sökväg till CSS-fil (ignoreras för Modern Design 1)
            
        Returns:
            str: HTML för CV:et
        """
        if not self.resume_object:
            raise ValueError("Resume object måste sättas innan CV kan genereras")
        
        logger.info("🎨 Modern Design 1: Genererar CV utan jobbeskrivning")
        
        # Använd ModernDesign1Generator (behöver API-nyckel)
        # Detta kommer att anropas från ModernDesign1Facade som har API-nyckeln
        raise NotImplementedError("create_resume ska anropas via ModernDesign1Facade")
    
    def create_resume_job_description_text(self, style_path: Path, job_description: str) -> str:
        """
        Skapa jobbanpassat CV - SAMMA INTERFACE som ResumeGenerator
        
        Args:
            style_path: Sökväg till CSS-fil (ignoreras för Modern Design 1)
            job_description: Jobbeskrivning
            
        Returns:
            str: HTML för CV:et
        """
        if not self.resume_object:
            raise ValueError("Resume object måste sättas innan CV kan genereras")
        
        logger.info("🎨 Modern Design 1: Genererar jobbanpassat CV")
        
        # Använd ModernDesign1Generator (behöver API-nyckel)
        # Detta kommer att anropas från ModernDesign1Facade som har API-nyckeln
        raise NotImplementedError("create_resume_job_description_text ska anropas via ModernDesign1Facade")
