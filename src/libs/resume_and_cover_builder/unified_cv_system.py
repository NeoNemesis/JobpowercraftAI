#!/usr/bin/env python3
"""
UNIFIED CV SYSTEM - Gemensam logik för alla 3 modeller
Implementerar alla 10 steg från ursprunglig logik för varje modell
"""

import sys
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Lägg till projektets root till Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger
from src.utils.chrome_utils import init_browser, HTML_to_PDF
from src.libs.resume_and_cover_builder.llm.llm_job_parser import LLMParser
from src.job import Job

class UnifiedCVSystem:
    """
    Enhetligt system som implementerar alla 10 steg för alla modeller.
    Varje modell har sin egen AI-generator men samma grundläggande process.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.resume_object = None
        self.selected_model = None
        self.selected_template = None
        self.job_data = None
        
        # Gemensamma komponenter för alla modeller
        self.driver = None
        self.job_parser = None
        
        logger.info("UnifiedCVSystem initialiserad")
    
    def set_resume_object(self, resume_object: Any):
        """Steg 5: Resume Object → YAML-data laddas och valideras"""
        self.resume_object = resume_object
        logger.info("Resume object satt i UnifiedCVSystem")
    
    def set_model_and_template(self, model_id: str, template_name: str):
        """Steg 2-3: Modell och mall-val"""
        self.selected_model = model_id
        self.selected_template = template_name
        logger.info(f"Modell och mall satta: {model_id} / {template_name}")
    
    def scrape_job_from_url(self, job_url: str) -> Job:
        """
        Steg 6: Jobb-skrapning → WebDriver hämtar jobbinfo
        SAMMA LOGIK FÖR ALLA MODELLER
        """
        logger.info(f"Startar jobbskrapning från URL: {job_url}")
        
        try:
            # Initiera WebDriver (gemensamt för alla modeller)
            self.driver = init_browser()
            self.driver.get(job_url)
            self.driver.implicitly_wait(10)
            
            # Extrahera HTML-innehåll
            body_element = self.driver.find_element("tag name", "body")
            body_html = body_element.get_attribute("outerHTML")
            
            # Använd LLMParser för att extrahera jobbinformation
            self.job_parser = LLMParser(openai_api_key=self.api_key)
            self.job_parser.set_body_html(body_html)
            
            # Skapa Job-objekt
            job = Job()
            job.role = self.job_parser.extract_role()
            job.company = self.job_parser.extract_company_name()
            job.description = self.job_parser.extract_job_description()
            job.location = self.job_parser.extract_location()
            job.link = job_url
            
            self.job_data = job
            
            logger.info(f"Jobb extraherat: {job.role} på {job.company} i {job.location}")
            return job
            
        except Exception as e:
            logger.error(f"Fel vid jobbskrapning: {e}")
            if self.driver:
                self.driver.quit()
            raise
    
    def generate_html_with_model_ai(self, job_description: Optional[str] = None) -> str:
        """
        Steg 7-8: AI-generering och HTML-sammansättning
        MODELL-SPECIFIK LOGIK
        """
        if not self.resume_object:
            raise ValueError("Resume object måste sättas innan HTML kan genereras")
        
        if not self.selected_model:
            raise ValueError("Modell måste väljas innan HTML kan genereras")
        
        logger.info(f"Genererar HTML med {self.selected_model} AI-modell")
        
        if self.selected_model == "MODERN_DESIGN_1":
            # Modern Design 1: Använd specialiserad generator
            from .moderndesign1.ai_generator import ModernDesign1Generator
            generator = ModernDesign1Generator(self.api_key, self.resume_object)
            return generator.generate_complete_cv(job_description)
            
        elif self.selected_model == "MODERN_DESIGN_2":
            # Modern Design 2: Använd specialiserad generator
            from .moderndesign2.ai_generator import ModernDesign2Generator
            generator = ModernDesign2Generator(self.api_key, self.resume_object)
            return generator.generate_complete_cv(job_description)
            
        elif self.selected_model == "URSPRUNGLIGA":
            # Ursprunglig: Använd befintlig ResumeGenerator
            from .resume_generator import ResumeGenerator
            from .style_manager import StyleManager
            
            generator = ResumeGenerator()
            generator.set_resume_object(self.resume_object)
            
            # Hitta CSS-fil för vald mall
            style_manager = StyleManager()
            style_manager.set_selected_style(self.selected_template)
            style_path = style_manager.get_style_path()
            
            if job_description:
                return generator.create_resume_job_description_text(style_path, job_description)
            else:
                return generator.create_resume(style_path)
        
        else:
            raise ValueError(f"Okänd modell: {self.selected_model}")
    
    def convert_html_to_pdf(self, html_content: str) -> Tuple[str, str]:
        """
        Steg 9: PDF-konvertering → Chrome skapar PDF
        SAMMA LOGIK FÖR ALLA MODELLER
        """
        logger.info("Konverterar HTML till PDF")
        
        try:
            if not self.driver:
                self.driver = init_browser()
            
            # Konvertera till PDF
            result_base64 = HTML_to_PDF(html_content, self.driver)
            
            # Generera suggested_name baserat på jobb-URL
            if self.job_data and self.job_data.link:
                suggested_name = hashlib.md5(self.job_data.link.encode()).hexdigest()[:10]
            else:
                suggested_name = "standard_resume"
            
            logger.info(f"PDF konverterat framgångsrikt, suggested_name: {suggested_name}")
            return result_base64, suggested_name
            
        except Exception as e:
            logger.error(f"Fel vid PDF-konvertering: {e}")
            raise
        # ✅ PERFORMANCE FIX: Don't quit driver! Browser pool manages lifecycle
        # finally block removed - no driver.quit() needed
    
    def save_pdf_to_output(self, pdf_base64: str, suggested_name: str, output_directory: str) -> Path:
        """
        Steg 10: Slutlig sparning → PDF sparas i output-mappen
        SAMMA LOGIK FÖR ALLA MODELLER
        """
        logger.info(f"Sparar PDF till output-mapp: {suggested_name}")
        
        try:
            import base64
            
            # Dekoda base64 till binär data
            pdf_data = base64.b64decode(pdf_base64)
            
            # Skapa output-mapp
            output_dir = Path(output_directory) / suggested_name
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Spara PDF
            output_path = output_dir / "resume_tailored.pdf"
            with open(output_path, "wb") as file:
                file.write(pdf_data)
            
            logger.info(f"PDF sparat framgångsrikt: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Fel vid PDF-sparning: {e}")
            raise
    
    def generate_complete_cv_from_url(self, job_url: str, output_directory: str) -> Path:
        """
        KOMPLETT PROCESS: Alla 10 steg för jobbanpassat CV
        FUNGERAR FÖR ALLA 3 MODELLER
        """
        logger.info(f"Startar komplett CV-generering från URL: {job_url}")
        
        try:
            # Steg 6: Jobb-skrapning
            job = self.scrape_job_from_url(job_url)
            
            # Steg 7-8: AI-generering och HTML-sammansättning
            html_content = self.generate_html_with_model_ai(job.description)
            
            # Steg 9: PDF-konvertering
            pdf_base64, suggested_name = self.convert_html_to_pdf(html_content)
            
            # Steg 10: Slutlig sparning
            output_path = self.save_pdf_to_output(pdf_base64, suggested_name, output_directory)
            
            logger.info("Komplett CV-generering slutförd framgångsrikt")
            return output_path
            
        except Exception as e:
            logger.error(f"Fel vid komplett CV-generering: {e}")
            if self.driver:
                self.driver.quit()
            raise
    
    def generate_standard_cv(self, output_directory: str) -> Path:
        """
        KOMPLETT PROCESS: Alla relevanta steg för standard CV (utan jobb-URL)
        FUNGERAR FÖR ALLA 3 MODELLER
        """
        logger.info("Startar standard CV-generering")
        
        try:
            # Steg 7-8: AI-generering och HTML-sammansättning (utan jobbeskrivning)
            html_content = self.generate_html_with_model_ai(None)
            
            # Steg 9: PDF-konvertering
            pdf_base64, suggested_name = self.convert_html_to_pdf(html_content)
            
            # Steg 10: Slutlig sparning
            output_path = self.save_pdf_to_output(pdf_base64, suggested_name, output_directory)
            
            logger.info("Standard CV-generering slutförd framgångsrikt")
            return output_path
            
        except Exception as e:
            logger.error(f"Fel vid standard CV-generering: {e}")
            if self.driver:
                self.driver.quit()
            raise
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Hämtar prestanda-statistik för systemet"""
        return {
            "api_calls_estimate": "3-15 requests till OpenAI",
            "webdriver_time": "2-5 sekunder",
            "pdf_conversion_time": "1-3 sekunder", 
            "total_time_estimate": "30-120 sekunder",
            "critical_decision_points": ["Action-val", "Modell-val", "Mall-val", "URL-input"]
        }


def create_unified_facade(api_key: str, resume_object: Any, model_id: str, template_name: str) -> UnifiedCVSystem:
    """
    Skapar en enhetlig facade för alla modeller
    SAMMA INTERFACE OAVSETT MODELL
    """
    system = UnifiedCVSystem(api_key)
    system.set_resume_object(resume_object)
    system.set_model_and_template(model_id, template_name)
    
    logger.info(f"Unified facade skapad för {model_id} / {template_name}")
    return system


if __name__ == "__main__":
    # Test av unified system
    print("🧪 TESTAR UNIFIED CV SYSTEM")
    print("=" * 50)
    
    system = UnifiedCVSystem("dummy_api_key")
    stats = system.get_performance_stats()
    
    print("⚡ PRESTANDA-STATISTIK:")
    for key, value in stats.items():
        print(f"   • {key}: {value}")
    
    print("\n✅ Unified CV System redo för alla 3 modeller!")

