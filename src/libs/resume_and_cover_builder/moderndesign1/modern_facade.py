"""
ModernDesign1Facade - Följer EXAKT samma pattern som ResumeFacade
Men använder Modern Design 1 specifika komponenter
"""

import hashlib
from pathlib import Path
from typing import Tuple
from loguru import logger

from src.job import Job
from src.utils.chrome_utils import HTML_to_PDF
from src.libs.resume_and_cover_builder.llm.llm_job_parser import LLMParser
from src.libs.resume_and_cover_builder.config import global_config
# ai_generator borttagen - använder nu smart_data_generator

class ModernDesign1Facade:
    """
    Modern Design 1 Facade - SAMMA INTERFACE SOM ResumeFacade
    Men använder Modern Design 1 komponenter internt
    """
    
    def __init__(self, api_key: str, style_manager, resume_generator, resume_object, output_path: Path):
        """
        Initialize ModernDesign1Facade - EXAKT SAMMA SIGNATURE SOM ResumeFacade

        Args:
            api_key (str): The OpenAI API key
            style_manager: The StyleManager instance
            resume_generator: The ResumeGenerator instance
            resume_object: The resume object
            output_path (Path): The output path
        """
        # EXAKT SAMMA global_config INITIERING SOM ResumeFacade
        lib_directory = Path(__file__).resolve().parent.parent
        global_config.STRINGS_MODULE_RESUME_PATH = lib_directory / "resume_prompt/strings_jobcraft.py"
        global_config.STRINGS_MODULE_RESUME_JOB_DESCRIPTION_PATH = lib_directory / "resume_job_description_prompt/strings_jobcraft.py"
        global_config.STRINGS_MODULE_COVER_LETTER_JOB_DESCRIPTION_PATH = lib_directory / "cover_letter_prompt/strings_jobcraft.py"
        global_config.STRINGS_MODULE_NAME = "strings_jobcraft"
        global_config.STYLES_DIRECTORY = lib_directory / "resume_style"
        global_config.LOG_OUTPUT_FILE_PATH = output_path
        global_config.API_KEY = api_key

        self.api_key = api_key
        self.style_manager = style_manager
        self.resume_generator = resume_generator
        self.resume_generator.set_resume_object(resume_object)  # SAMMA SOM ResumeFacade
        self.output_path = output_path
        self.driver = None
        self.job = None  # SAMMA SOM ResumeFacade - Job objekt, inte bara URL
        self.job_specific_answers = None  # Svar på jobbspecifika frågor

        logger.info("🎨 ModernDesign1Facade initialiserad med EXAKT samma global_config som ResumeFacade")
    
    def set_driver(self, driver):
        """Sätt WebDriver - SAMMA SOM ResumeFacade"""
        self.driver = driver
        logger.debug("🌐 WebDriver satt för ModernDesign1Facade")
    
    def link_to_job(self, job_url: str):
        """Länka till jobb - FÖRBÄTTRAD VERSION MED TIMEOUT-HANTERING"""
        try:
            logger.info(f"🔗 Modern Design 1: Länkar till jobb: {job_url}")
            
            # Lägg till timeout för WebDriver-anrop
            self.driver.set_page_load_timeout(30)  # 30 sekunder timeout
            self.driver.get(job_url)
            self.driver.implicitly_wait(10)
            
            body_element = self.driver.find_element("tag name", "body")
            body_element = body_element.get_attribute("outerHTML")
            
            # Skapa LLMParser med timeout
            self.llm_job_parser = LLMParser(openai_api_key=global_config.API_KEY)
            self.llm_job_parser.set_body_html(body_element)

            self.job = Job()
            
            # Extrahera jobbinformation med timeout-hantering
            try:
                self.job.role = self.llm_job_parser.extract_role()
            except Exception as e:
                logger.warning(f"⚠️ Kunde inte extrahera roll: {e}")
                self.job.role = "Dataingenjör"
            
            try:
                self.job.company = self.llm_job_parser.extract_company_name()
            except Exception as e:
                logger.warning(f"⚠️ Kunde inte extrahera företag: {e}")
                self.job.company = "Företag"
            
            try:
                self.job.description = self.llm_job_parser.extract_job_description()
            except Exception as e:
                logger.warning(f"⚠️ Kunde inte extrahera beskrivning: {e}")
                self.job.description = "Vi söker en dataingenjör med erfarenhet av systemintegration och webbutveckling."
            
            try:
                self.job.location = self.llm_job_parser.extract_location()
            except Exception as e:
                logger.warning(f"⚠️ Kunde inte extrahera plats: {e}")
                self.job.location = "Stockholm"
            
            self.job.link = job_url
            logger.info(f"✅ Modern Design 1: Jobb extraherat från URL: {job_url}")
            
        except Exception as e:
            logger.error(f"❌ Modern Design 1: Fel vid jobb-länkning: {e}")
            # Skapa fallback job-objekt
            self.job = Job()
            self.job.role = "Dataingenjör"
            self.job.company = "Företag"
            self.job.description = "Vi söker en dataingenjör med erfarenhet av systemintegration och webbutveckling."
            self.job.location = "Stockholm"
            self.job.link = job_url
            logger.info(f"🔄 Modern Design 1: Använder fallback job-objekt")

    def ask_job_specific_questions(self, ask_questions: bool = True) -> None:
        """
        Ställ jobbspecifika frågor för att anpassa CV:t

        Args:
            ask_questions: Om False, hoppa över frågor (default: True)
        """
        if not ask_questions:
            logger.info("⏭️  Hoppar över jobbspecifika frågor")
            return

        if not self.job or not self.job.description:
            logger.warning("⚠️  Ingen jobbeskrivning tillgänglig, hoppar över frågor")
            return

        try:
            from src.smart_question_generator import analyze_and_ask_for_job
            import yaml

            # Hämta CV-data
            resume_data = {
                'experience_details': [
                    {
                        'position': exp.position if hasattr(exp, 'position') else '',
                        'company': exp.company if hasattr(exp, 'company') else '',
                        'skills_acquired': exp.skills_acquired if hasattr(exp, 'skills_acquired') else []
                    }
                    for exp in (self.resume_generator.resume_object.experience_details or [])
                ]
            }

            logger.info("\n🎯 Analyserar jobb och genererar relevanta frågor...")

            # Ställ frågor
            result = analyze_and_ask_for_job(
                self.job.description,
                resume_data,
                self.api_key
            )

            self.job_specific_answers = result
            logger.info(f"✅ Samlade in {len(result.get('answers', {}))} svar för CV-anpassning")

        except Exception as e:
            logger.error(f"❌ Fel vid frågegenerering: {e}")
            self.job_specific_answers = None

    def create_resume_pdf_job_tailored(self, ask_questions: bool = True) -> Tuple[str, str]:
        """
        Skapa jobbanpassat CV - MED JOBBSPECIFIKA FRÅGOR

        Args:
            ask_questions: Om True, ställ jobbspecifika frågor först

        Returns:
            Tuple[str, str]: (base64_pdf, suggested_name)
        """
        # Ställ jobbspecifika frågor först
        if ask_questions:
            self.ask_job_specific_questions(ask_questions=True)

        # EXAKT SAMMA LOGIK SOM ResumeFacade.create_resume_pdf_job_tailored()
        style_path = self.style_manager.get_style_path()  # SAMMA METOD-NAMN SOM ResumeFacade
        if style_path is None:
            raise ValueError("You must choose a style before generating the PDF.")

        # ANVÄND resume_generator EXAKT som ResumeFacade
        # Men istället för create_resume_job_description_text, använd Modern Design 1 generator
        html_resume = self._create_modern_design1_resume(style_path, self.job.description)

        # Generate a unique name using the job URL hash - EXAKT SOM ResumeFacade
        suggested_name = hashlib.md5(self.job.link.encode()).hexdigest()[:10]
        
        # Generera PDF med timeout-hantering
        try:
            logger.info("📄 Modern Design 1: Genererar PDF...")
            result = HTML_to_PDF(html_resume, self.driver)
            logger.info("✅ Modern Design 1: PDF genererad")
        except Exception as e:
            logger.error(f"❌ Modern Design 1: Fel vid PDF-generering: {e}")
            raise
        # ✅ PERFORMANCE FIX: Don't quit driver! Browser pool manages lifecycle
        # finally block removed - no driver.quit() needed
        
        return result, suggested_name
    
    def _create_modern_design1_resume(self, style_path: Path, job_description: str) -> str:
        """
        Skapa Modern Design 1 CV - MED JOBBSPECIFIKA SVAR

        Args:
            style_path: Sökväg till CSS-fil
            job_description: Jobbeskrivning

        Returns:
            str: Komplett HTML för CV:et (med CSS och struktur)
        """
        if self.job_specific_answers:
            logger.info("🎯 Skapar CV med jobbspecifika svar från frågor")
        else:
            logger.info("🎯 Skapar CV utan jobbspecifika svar")

        # Använd förbättrad generator som matchar exakt design från bilden
        from .improved_generator import ImprovedModernDesign1Generator

        # Skapa generator som använder förbättrad template
        generator = ImprovedModernDesign1Generator(
            self.resume_generator.resume_object,
            global_config.API_KEY
        )

        # Sätt jobbspecifika svar om de finns
        if self.job_specific_answers:
            generator.set_job_specific_answers(self.job_specific_answers)

        # Generera komplett HTML med förbättrad struktur
        complete_html = generator.generate_complete_cv_html(job_description)

        logger.info(f"✅ Modern Design 1 CV genererat: {len(complete_html)} tecken")
        return complete_html
    
    def create_cover_letter(self) -> Tuple[str, str]:
        """
        Skapa personligt brev - SAMMA INTERFACE SOM ResumeFacade
        
        Returns:
            Tuple[str, str]: (base64_pdf, suggested_name)
        """
        if not self.job:
            raise ValueError("Jobb måste länkas innan cover letter kan genereras")
        
        logger.info("📧 Modern Design 1: Skapar personligt brev")
        
        from .cover_letter_generator import ModernDesign1CoverLetterGenerator
        
        generator = ModernDesign1CoverLetterGenerator(
            self.resume_generator.resume_object,
            self.api_key
        )
        
        # Generera HTML
        cover_letter_html = generator.generate_cover_letter_html(
            job_description=self.job.description,
            company_name=self.job.company,
            position_title=self.job.role,
            company_address=""
        )
        
        # Generera PDF
        suggested_name = hashlib.md5(self.job.link.encode()).hexdigest()[:10]
        
        try:
            logger.info("📄 Modern Design 1: Genererar Cover Letter PDF...")
            result = HTML_to_PDF(cover_letter_html, self.driver)
            logger.info("✅ Modern Design 1: Cover Letter PDF genererad")
        except Exception as e:
            logger.error(f"❌ Modern Design 1: Fel vid Cover Letter PDF-generering: {e}")
            raise
        finally:
            try:
                self.driver.quit()
                logger.info("🔒 Modern Design 1: WebDriver stängd")
            except Exception as e:
                logger.warning(f"⚠️ Modern Design 1: Kunde inte stänga WebDriver: {e}")
        
        return result, suggested_name