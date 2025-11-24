"""
Document Generation Strategy Pattern

ARCHITECTURE FIX: Eliminates code duplication in main.py

Before: 3 nearly identical functions (create_modern_design1_cv, create_modern_design2_cv, create_original_cv)
After: Single strategy interface with 3 implementations

Benefits:
- Single responsibility principle
- Open/closed principle (easy to add new designs)
- Reduces main.py from 1338 lines to <800 lines
- Eliminates 80%+ code duplication
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Tuple, Optional
from loguru import logger

from src.resume_schemas.resume import Resume
from src.utils.browser_pool import get_browser


class DocumentGenerationStrategy(ABC):
    """
    Abstract base class for document generation strategies.
    
    Each design system (Original, Modern Design 1, Modern Design 2)
    implements this interface with its own facade and generators.
    """
    
    def __init__(self, api_key: str, resume_object: Resume, output_path: Path):
        """
        Initialize strategy with common parameters.
        
        Args:
            api_key: LLM API key
            resume_object: Resume data object
            output_path: Base output directory
        """
        self.api_key = api_key
        self.resume_object = resume_object
        self.output_path = output_path
        self.facade = None
        self.driver = None
    
    @abstractmethod
    def initialize_components(self, selected_template: str):
        """
        Initialize design-specific components (facade, style manager, generator).
        
        Args:
            selected_template: Template name selected by user
        """
        pass
    
    @abstractmethod
    def generate_resume_tailored(self, job_url: str) -> Tuple[str, str]:
        """
        Generate job-tailored resume.
        
        Args:
            job_url: URL of job posting
            
        Returns:
            Tuple[str, str]: (base64_pdf, suggested_name)
        """
        pass
    
    @abstractmethod
    def generate_cover_letter(self, job_url: str) -> Tuple[str, str]:
        """
        Generate job-tailored cover letter.
        
        Args:
            job_url: URL of job posting
            
        Returns:
            Tuple[str, str]: (base64_pdf, suggested_name)
        """
        pass
    
    def generate_standard_resume(self) -> str:
        """
        Generate standard (non-tailored) resume.
        
        Returns:
            str: base64 encoded PDF
        """
        if self.facade is None:
            raise RuntimeError("Components not initialized. Call initialize_components() first.")
        
        return self.facade.create_resume_pdf()
    
    def cleanup(self):
        """Cleanup resources (driver, etc)."""
        # Driver cleanup handled by BrowserPool
        pass


class OriginalDesignStrategy(DocumentGenerationStrategy):
    """Strategy for original/classic design templates."""
    
    def initialize_components(self, selected_template: str):
        """Initialize original design components."""
        logger.info("📄 Initializing Original Design Strategy")
        
        from src.libs.resume_and_cover_builder.resume_generator import ResumeGenerator
        from src.libs.resume_and_cover_builder.style_manager import StyleManager
        from src.libs.resume_and_cover_builder.resume_facade import ResumeFacade
        
        style_manager = StyleManager()
        style_manager.set_selected_style(selected_template)
        
        resume_generator = ResumeGenerator()
        resume_generator.set_resume_object(self.resume_object)
        
        # Use browser pool instead of creating new instance
        self.driver = get_browser()
        
        self.facade = ResumeFacade(
            api_key=self.api_key,
            style_manager=style_manager,
            resume_generator=resume_generator,
            resume_object=self.resume_object,
            output_path=self.output_path
        )
        self.facade.set_driver(self.driver)
        
        logger.info("✅ Original Design components initialized")
    
    def generate_resume_tailored(self, job_url: str) -> Tuple[str, str]:
        """Generate tailored resume using original design."""
        if self.facade is None:
            raise RuntimeError("Components not initialized")
        
        logger.info(f"📄 Generating tailored resume (Original Design) for: {job_url}")
        self.facade.link_to_job(job_url)
        return self.facade.create_resume_pdf_job_tailored()
    
    def generate_cover_letter(self, job_url: str) -> Tuple[str, str]:
        """Generate cover letter using original design."""
        if self.facade is None:
            raise RuntimeError("Components not initialized")
        
        logger.info(f"💌 Generating cover letter (Original Design) for: {job_url}")
        self.facade.link_to_job(job_url)
        return self.facade.create_cover_letter()


class ModernDesign1Strategy(DocumentGenerationStrategy):
    """Strategy for Modern Design 1 (professional modern templates)."""
    
    def initialize_components(self, selected_template: str):
        """Initialize Modern Design 1 components."""
        logger.info("🎨 Initializing Modern Design 1 Strategy")
        
        from src.libs.resume_and_cover_builder.moderndesign1.modern_facade import ModernDesign1Facade
        from src.libs.resume_and_cover_builder.moderndesign1.modern_style_manager import ModernDesign1StyleManager
        from src.libs.resume_and_cover_builder.moderndesign1.modern_resume_generator import ModernDesign1ResumeGenerator
        
        style_manager = ModernDesign1StyleManager()
        style_manager.set_selected_style(selected_template)
        
        resume_generator = ModernDesign1ResumeGenerator()
        
        # Use browser pool
        self.driver = get_browser()
        
        self.facade = ModernDesign1Facade(
            api_key=self.api_key,
            style_manager=style_manager,
            resume_generator=resume_generator,
            resume_object=self.resume_object,
            output_path=self.output_path
        )
        self.facade.set_driver(self.driver)
        
        logger.info("✅ Modern Design 1 components initialized")
    
    def generate_resume_tailored(self, job_url: str) -> Tuple[str, str]:
        """Generate tailored resume using Modern Design 1."""
        if self.facade is None:
            raise RuntimeError("Components not initialized")
        
        logger.info(f"🎨 Generating tailored resume (Modern Design 1) for: {job_url}")
        self.facade.link_to_job(job_url)
        return self.facade.create_resume_pdf_job_tailored()
    
    def generate_cover_letter(self, job_url: str) -> Tuple[str, str]:
        """Generate cover letter using Modern Design 1."""
        if self.facade is None:
            raise RuntimeError("Components not initialized")
        
        logger.info(f"💌 Generating cover letter (Modern Design 1) for: {job_url}")
        self.facade.link_to_job(job_url)
        return self.facade.create_cover_letter()


class ModernDesign2Strategy(DocumentGenerationStrategy):
    """Strategy for Modern Design 2 (creative sidebar templates)."""
    
    def initialize_components(self, selected_template: str):
        """Initialize Modern Design 2 components."""
        logger.info("🎨 Initializing Modern Design 2 Strategy")
        
        from src.libs.resume_and_cover_builder.moderndesign2.modern_facade import ModernDesign2Facade
        from src.libs.resume_and_cover_builder.moderndesign2.modern_style_manager import ModernDesign2StyleManager
        from src.libs.resume_and_cover_builder.moderndesign2.modern_resume_generator import ModernDesign2ResumeGenerator
        
        style_manager = ModernDesign2StyleManager()
        style_manager.set_selected_style(selected_template)
        
        resume_generator = ModernDesign2ResumeGenerator()
        
        # Use browser pool
        self.driver = get_browser()
        
        self.facade = ModernDesign2Facade(
            api_key=self.api_key,
            style_manager=style_manager,
            resume_generator=resume_generator,
            resume_object=self.resume_object,
            output_path=self.output_path
        )
        self.facade.set_driver(self.driver)
        
        logger.info("✅ Modern Design 2 components initialized")
    
    def generate_resume_tailored(self, job_url: str) -> Tuple[str, str]:
        """Generate tailored resume using Modern Design 2."""
        if self.facade is None:
            raise RuntimeError("Components not initialized")
        
        logger.info(f"🎨 Generating tailored resume (Modern Design 2) for: {job_url}")
        self.facade.link_to_job(job_url)
        return self.facade.create_resume_pdf_job_tailored()
    
    def generate_cover_letter(self, job_url: str) -> Tuple[str, str]:
        """Generate cover letter using Modern Design 2."""
        if self.facade is None:
            raise RuntimeError("Components not initialized")
        
        logger.info(f"💌 Generating cover letter (Modern Design 2) for: {job_url}")
        self.facade.link_to_job(job_url)
        return self.facade.create_cover_letter()


class StrategyFactory:
    """
    Factory for creating document generation strategies.
    
    This eliminates the need for if/elif chains in main.py.
    """
    
    _strategies = {
        "URSPRUNGLIGA": OriginalDesignStrategy,
        "MODERN_DESIGN_1": ModernDesign1Strategy,
        "MODERN_DESIGN_2": ModernDesign2Strategy,
    }
    
    @classmethod
    def create_strategy(
        cls,
        model_name: str,
        api_key: str,
        resume_object: Resume,
        output_path: Path
    ) -> DocumentGenerationStrategy:
        """
        Create appropriate strategy based on model name.
        
        Args:
            model_name: Name of design model
            api_key: LLM API key
            resume_object: Resume data
            output_path: Output directory
            
        Returns:
            DocumentGenerationStrategy: Appropriate strategy instance
            
        Raises:
            ValueError: If model_name is unknown
        """
        strategy_class = cls._strategies.get(model_name.upper())
        
        if strategy_class is None:
            available = ', '.join(cls._strategies.keys())
            raise ValueError(
                f"Unknown design model: '{model_name}'. "
                f"Available models: {available}"
            )
        
        logger.info(f"🏭 Creating strategy for: {model_name}")
        return strategy_class(api_key, resume_object, output_path)
    
    @classmethod
    def get_available_models(cls) -> list:
        """Get list of available model names."""
        return list(cls._strategies.keys())


# Export main classes
__all__ = [
    'DocumentGenerationStrategy',
    'OriginalDesignStrategy',
    'ModernDesign1Strategy',
    'ModernDesign2Strategy',
    'StrategyFactory',
]

