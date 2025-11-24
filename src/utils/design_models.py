"""
Design Model Enumerations

CODE QUALITY FIX: Replaces magic strings with type-safe Enums.

Before: if selected_model == "MODERN_DESIGN_1":  # Typo risk
After: if selected_model == DesignModel.MODERN_DESIGN_1:  # Type-safe

Benefits:
- IDE autocomplete
- Compile-time error detection
- No typo risks
- Self-documenting code
"""
from enum import Enum, auto
from typing import Dict, List


class DesignModel(Enum):
    """
    Enumeration of available CV design models.
    
    Each model has its own facade, style manager, and templates.
    """
    ORIGINAL = "URSPRUNGLIGA"
    MODERN_DESIGN_1 = "MODERN_DESIGN_1"
    MODERN_DESIGN_2 = "MODERN_DESIGN_2"
    
    def __str__(self) -> str:
        """Return the string value for display."""
        return self.value
    
    @property
    def display_name(self) -> str:
        """Get human-readable display name."""
        display_names = {
            DesignModel.ORIGINAL: "Ursprungliga (Klassiska mallar)",
            DesignModel.MODERN_DESIGN_1: "Modern Design 1 (Professionella)",
            DesignModel.MODERN_DESIGN_2: "Modern Design 2 (Kreativa sidopanel)",
        }
        return display_names[self]
    
    @property
    def description(self) -> str:
        """Get detailed description of the design model."""
        descriptions = {
            DesignModel.ORIGINAL: "Klassiska CV-mallar med tidlös design. Fungerar för alla branscher.",
            DesignModel.MODERN_DESIGN_1: "Moderna professionella mallar med clean design. Perfekt för tech och business.",
            DesignModel.MODERN_DESIGN_2: "Kreativa mallar med sidopanel och gradients. Står ut från mängden!",
        }
        return descriptions[self]
    
    @classmethod
    def from_string(cls, value: str) -> 'DesignModel':
        """
        Convert string to DesignModel enum.
        
        Args:
            value: String representation of the model
            
        Returns:
            DesignModel: Corresponding enum value
            
        Raises:
            ValueError: If value doesn't match any model
        """
        for model in cls:
            if model.value == value:
                return model
        
        # Try case-insensitive match
        for model in cls:
            if model.value.lower() == value.lower():
                return model
        
        raise ValueError(
            f"Unknown design model: '{value}'. "
            f"Valid options: {', '.join(m.value for m in cls)}"
        )
    
    @classmethod
    def get_all_models(cls) -> List['DesignModel']:
        """Get list of all available design models."""
        return list(cls)
    
    @classmethod
    def get_choices_dict(cls) -> Dict[str, str]:
        """
        Get dictionary suitable for inquirer choices.
        
        Returns:
            Dict mapping display names to enum values
        """
        return {
            model.display_name: model.value
            for model in cls
        }


class GenerationMode(Enum):
    """
    Enumeration of document generation modes.
    """
    STANDARD_RESUME = "standard_resume"
    TAILORED_RESUME = "tailored_resume"
    COVER_LETTER = "cover_letter"
    EMAIL_APPLICATION = "email_application"
    
    def __str__(self) -> str:
        return self.value
    
    @property
    def display_name(self) -> str:
        """Get human-readable display name."""
        display_names = {
            GenerationMode.STANDARD_RESUME: "Generate Resume",
            GenerationMode.TAILORED_RESUME: "Generate Resume Tailored for Job Description",
            GenerationMode.COVER_LETTER: "Generate Tailored Cover Letter for Job Description",
            GenerationMode.EMAIL_APPLICATION: "Generate and Send Job Application via Email",
        }
        return display_names[self]
    
    @property
    def requires_job_url(self) -> bool:
        """Check if this mode requires a job URL."""
        return self in [
            GenerationMode.TAILORED_RESUME,
            GenerationMode.COVER_LETTER,
            GenerationMode.EMAIL_APPLICATION,
        ]
    
    @property
    def requires_email_config(self) -> bool:
        """Check if this mode requires email configuration."""
        return self == GenerationMode.EMAIL_APPLICATION
    
    @classmethod
    def from_string(cls, value: str) -> 'GenerationMode':
        """Convert display name or value to GenerationMode enum."""
        # Try exact match on display name
        for mode in cls:
            if mode.display_name == value:
                return mode
        
        # Try exact match on value
        for mode in cls:
            if mode.value == value:
                return mode
        
        raise ValueError(
            f"Unknown generation mode: '{value}'. "
            f"Valid options: {', '.join(m.display_name for m in cls)}"
        )
    
    @classmethod
    def get_all_modes(cls) -> List['GenerationMode']:
        """Get list of all available generation modes."""
        return list(cls)
    
    @classmethod
    def get_choices_list(cls) -> List[str]:
        """Get list of display names suitable for inquirer choices."""
        return [mode.display_name for mode in cls]


# Convenience functions
def validate_design_model(model_str: str) -> DesignModel:
    """
    Validate and convert string to DesignModel.
    
    Args:
        model_str: String representation of model
        
    Returns:
        DesignModel: Validated enum value
        
    Raises:
        ValueError: If model is invalid
    """
    try:
        return DesignModel.from_string(model_str)
    except ValueError as e:
        from loguru import logger
        logger.error(f"Invalid design model: {model_str}")
        raise


def get_model_display_names() -> List[str]:
    """Get list of all model display names for UI."""
    return [model.display_name for model in DesignModel]


def get_mode_display_names() -> List[str]:
    """Get list of all generation mode display names for UI."""
    return [mode.display_name for mode in GenerationMode]


# Export main classes
__all__ = [
    'DesignModel',
    'GenerationMode',
    'validate_design_model',
    'get_model_display_names',
    'get_mode_display_names',
]

