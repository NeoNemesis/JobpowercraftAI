#!/usr/bin/env python3
"""
Integration för Modern Design 2 med huvudprogrammet
Kopplar ihop AI-generatorn med befintlig logik - SAMMA INTERFACE SOM URSPRUNGLIG
"""

import sys
from pathlib import Path
from typing import Optional, Any

# Lägg till projektets root till Python path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from .ai_generator import ModernDesign2Generator
from loguru import logger

class ModernDesign2Integration:
    """
    Integrationsklass som gör Modern Design 2 kompatibel med befintlig programlogik
    SAMMA INTERFACE SOM URSPRUNGLIG ResumeGenerator
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.generator = None
    
    def set_resume_object(self, resume_object: Any):
        """Sätter resume-objekt och initialiserar generator"""
        self.generator = ModernDesign2Generator(self.api_key, resume_object)
        logger.info("Modern Design 2 generator initialiserad")
    
    def create_resume_job_description_text(self, style_path: Path, job_description: str) -> str:
        """
        Skapar CV baserat på jobbeskrivning - SAMMA INTERFACE SOM ResumeGenerator
        
        Args:
            style_path: Sökväg till CSS-fil (används för att identifiera Modern Design 2)
            job_description: Jobbeskrivning för anpassning
            
        Returns:
            Komplett HTML-sträng för CV:et
        """
        if not self.generator:
            raise ValueError("Resume object måste sättas innan CV kan genereras")
        
        # Kontrollera om detta är Modern Design 2 stil
        if "moderndesign2" in str(style_path).lower() or "modern design 2" in str(style_path).lower():
            logger.info("Använder Modern Design 2 generator")
            return self.generator.generate_complete_cv(job_description)
        else:
            # Fallback till standard-generering om det inte är Modern Design 2
            logger.warning(f"Style path {style_path} matchar inte Modern Design 2, använder fallback")
            return self._fallback_generation(job_description)
    
    def create_resume(self, style_path: Path) -> str:
        """
        Skapar standard CV utan jobbeskrivning - SAMMA INTERFACE SOM ResumeGenerator
        
        Args:
            style_path: Sökväg till CSS-fil
            
        Returns:
            Komplett HTML-sträng för CV:et
        """
        return self.create_resume_job_description_text(style_path, None)
    
    def _fallback_generation(self, job_description: Optional[str] = None) -> str:
        """Fallback-generering om det inte är Modern Design 2"""
        if not self.generator:
            return "<html><body><h1>Fel: Ingen generator tillgänglig</h1></body></html>"
        
        try:
            return self.generator.generate_complete_cv(job_description)
        except Exception as e:
            logger.error(f"Fallback-generering misslyckades: {e}")
            return f"<html><body><h1>Fel vid CV-generering: {e}</h1></body></html>"


def is_modern_design2_style(style_path: Path) -> bool:
    """
    Kontrollerar om en given stil-sökväg är Modern Design 2
    
    Args:
        style_path: Sökväg till CSS-fil
        
    Returns:
        True om det är Modern Design 2, False annars
    """
    if not style_path or not style_path.exists():
        return False
    
    try:
        # Läs första raden för att kontrollera kommentar
        with open(style_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            return "Modern Design 2" in first_line
    except Exception:
        return False


def integrate_with_resume_generator(resume_generator, api_key: str):
    """
    Integrerar Modern Design 2 med befintlig ResumeGenerator
    SAMMA LOGIK SOM Modern Design 1 integration
    
    Args:
        resume_generator: Befintlig ResumeGenerator instans
        api_key: OpenAI API-nyckel
    """
    # Spara ursprungliga metoder
    original_create_resume_job = resume_generator.create_resume_job_description_text
    original_create_resume = resume_generator.create_resume
    
    # Skapa integration-instans
    integration = ModernDesign2Integration(api_key)
    
    def enhanced_create_resume_job_description_text(style_path, job_description):
        """Förbättrad metod som stöder Modern Design 2"""
        
        # Sätt resume object i integration
        if hasattr(resume_generator, 'resume_object') and resume_generator.resume_object:
            integration.set_resume_object(resume_generator.resume_object)
        
        # Kontrollera om det är Modern Design 2
        if is_modern_design2_style(Path(style_path)):
            logger.info("Använder Modern Design 2 integration")
            return integration.create_resume_job_description_text(Path(style_path), job_description)
        else:
            # Använd ursprunglig metod för andra stilar
            logger.info("Använder ursprunglig ResumeGenerator")
            return original_create_resume_job(style_path, job_description)
    
    def enhanced_create_resume(style_path):
        """Förbättrad metod som stöder Modern Design 2"""
        
        # Sätt resume object i integration
        if hasattr(resume_generator, 'resume_object') and resume_generator.resume_object:
            integration.set_resume_object(resume_generator.resume_object)
        
        # Kontrollera om det är Modern Design 2
        if is_modern_design2_style(Path(style_path)):
            logger.info("Använder Modern Design 2 integration")
            return integration.create_resume(Path(style_path))
        else:
            # Använd ursprunglig metod för andra stilar
            logger.info("Använder ursprunglig ResumeGenerator")
            return original_create_resume(style_path)
    
    # Ersätt metoder i resume_generator
    resume_generator.create_resume_job_description_text = enhanced_create_resume_job_description_text
    resume_generator.create_resume = enhanced_create_resume
    
    logger.info("Modern Design 2 integration installerad i ResumeGenerator")
    
    return resume_generator

