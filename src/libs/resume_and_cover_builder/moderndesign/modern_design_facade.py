"""
Modern Design Facade - Coordinates the Modern Design CV generation process
"""

from pathlib import Path
from string import Template
from .modern_design_generator import ModernDesignGenerator
from ..resume_generator import ResumeGenerator
from src.utils.chrome_utils import HTML_to_PDF
from ..llm.llm_job_parser import LLMParser
from src.job import Job
from ..config import global_config
import hashlib
from loguru import logger

class ModernDesignFacade:
    def __init__(self, api_key, resume_object, output_path):
        """
        Initialize Modern Design Facade
        
        Args:
            api_key: OpenAI API key
            resume_object: Resume data object
            output_path: Output directory path
        """
        self.api_key = api_key
        self.resume_object = resume_object
        self.output_path = output_path
        self.driver = None
        self.job = None
        
        # Configure global_config like ResumeFacade
        lib_directory = Path(__file__).resolve().parent
        global_config.STRINGS_MODULE_RESUME_PATH = lib_directory / "resume_prompt/strings_jobcraft.py"
        global_config.STRINGS_MODULE_RESUME_JOB_DESCRIPTION_PATH = lib_directory / "resume_job_description_prompt/strings_jobcraft.py"
        global_config.STRINGS_MODULE_COVER_LETTER_JOB_DESCRIPTION_PATH = lib_directory / "cover_letter_prompt/strings_jobcraft.py"
        global_config.STRINGS_MODULE_NAME = "strings_jobcraft"
        global_config.STYLES_DIRECTORY = lib_directory.parent / "resume_style"
        global_config.LOG_OUTPUT_FILE_PATH = output_path
        global_config.API_KEY = api_key
        
        # Load strings module
        try:
            import sys
            sys.path.append(str(lib_directory))
            self.strings = __import__('strings_modern_design', fromlist=[''])
            logger.info("✅ Loaded Modern Design strings module")
        except Exception as e:
            logger.error(f"❌ Failed to load strings module: {e}")
            raise
        
        # CSS path
        self.css_path = lib_directory.parent / "resume_style" / "modern_design.css"
        
    def set_driver(self, driver):
        """Set WebDriver instance"""
        self.driver = driver
    
    def link_to_job(self, job_url: str):
        """Parse job from URL - same logic as ResumeFacade"""
        logger.info(f"🔗 Linking to job: {job_url}")
        
        try:
            self.driver.get(job_url)
            self.driver.implicitly_wait(10)
            body_element = self.driver.find_element("tag name", "body")
            body_element = body_element.get_attribute("outerHTML")
            
            self.llm_job_parser = LLMParser(openai_api_key=global_config.API_KEY)
            self.llm_job_parser.set_body_html(body_element)

            self.job = Job()
            self.job.role = self.llm_job_parser.extract_role()
            self.job.company = self.llm_job_parser.extract_company_name()
            self.job.description = self.llm_job_parser.extract_job_description()
            self.job.location = self.llm_job_parser.extract_location()
            self.job.link = job_url
            
            logger.info(f"✅ Job parsed: {self.job.role} at {self.job.company}")
            
        except Exception as e:
            logger.error(f"❌ Failed to parse job: {e}")
            raise
    
    def create_resume_pdf_job_tailored(self) -> tuple:
        """Generate PDF resume with Modern Design"""
        logger.info("🎨 Creating Modern Design resume PDF...")
        
        try:
            # Create generator
            generator = ModernDesignGenerator(self.api_key, self.strings)
            generator.set_resume(self.resume_object)
            generator.set_job_description(self.job.description)
            
            # Generate HTML body
            body_html = generator.generate_complete_resume()
            
            # Read CSS
            if not self.css_path.exists():
                raise FileNotFoundError(f"CSS file not found: {self.css_path}")
                
            with open(self.css_path, "r") as f:
                style_css = f.read()
            
            # Use global HTML template
            template = Template(global_config.html_template)
            final_html = template.substitute(body=body_html, style_css=style_css)
            
            # Convert to PDF
            suggested_name = hashlib.md5(self.job.link.encode()).hexdigest()[:10]
            result = HTML_to_PDF(final_html, self.driver)
            
            # ✅ PERFORMANCE FIX: Don't quit driver! Browser pool manages lifecycle
            
            logger.info("✅ Modern Design PDF generated successfully")
            return result, suggested_name
            
        except Exception as e:
            logger.error(f"❌ Failed to generate Modern Design PDF: {e}")
            # ✅ PERFORMANCE FIX: Don't quit driver! Browser pool manages lifecycle
            raise
