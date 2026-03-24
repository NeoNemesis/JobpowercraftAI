"""
ModernDesign2ResumeGenerator - SAMMA INTERFACE som ResumeGenerator
Men använder Modern Design 2 kreativa generator
"""

from pathlib import Path
from typing import Any
from loguru import logger

class ModernDesign2ResumeGenerator:
    """
    Modern Design 2 Resume Generator - SAMMA INTERFACE som ResumeGenerator
    Men använder kreativ sidopanel-design
    """
    
    def __init__(self):
        self.resume_object = None
        logger.debug("🎨 ModernDesign2ResumeGenerator initialiserad")
    
    def set_resume_object(self, resume_object):
        """
        Sätt resume object - SAMMA INTERFACE som ResumeGenerator
        
        Args:
            resume_object: Resume object
        """
        self.resume_object = resume_object
        logger.debug("🎨 Modern Design 2: Resume object satt")
    
    def create_resume(self, style_path: Path) -> str:
        """
        Skapa CV - SAMMA INTERFACE som ResumeGenerator
        
        Args:
            style_path: Sökväg till CSS-fil
            
        Returns:
            str: HTML för CV:et
        """
        if not self.resume_object:
            raise ValueError("Resume object måste sättas innan CV kan genereras")
        
        logger.info("🎨 Modern Design 2: Genererar CV utan jobbeskrivning")
        raise NotImplementedError("create_resume ska anropas via ModernDesign2Facade")
    
    def create_resume_job_description_text(self, style_path: Path, job_description: str) -> str:
        """
        Skapa jobbanpassat CV - SAMMA INTERFACE som ResumeGenerator
        
        Args:
            style_path: Sökväg till CSS-fil
            job_description: Jobbeskrivning
            
        Returns:
            str: HTML för CV:et
        """
        if not self.resume_object:
            raise ValueError("Resume object måste sättas innan CV kan genereras")
        
        logger.info("🎨 Modern Design 2: Genererar jobbanpassat CV")
        raise NotImplementedError("create_resume_job_description_text ska anropas via ModernDesign2Facade")





