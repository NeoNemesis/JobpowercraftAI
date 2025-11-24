#!/usr/bin/env python3
"""
AI Generator för Modern Design 2 - Creative Bold Design
Skapar HTML-innehåll som matchar den kreativa sidopanel-designen.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import base64

# Lägg till projektets root till Python path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.libs.resume_and_cover_builder.llm.llm_generate_resume import LLMResumer
from src.libs.resume_and_cover_builder.utils import LoggerChatModel, image_to_base64
from src.libs.resume_and_cover_builder.config import global_config
from langchain_openai import ChatOpenAI
from loguru import logger

class ModernDesign2Generator:
    """
    AI Generator specifikt för Modern Design 2 kreativa sidopanel-design.
    Genererar HTML-innehåll som matchar den kreativa layouten med färgglad sidopanel.
    """
    
    def __init__(self, api_key: str, resume_object: Any):
        self.api_key = api_key
        self.resume_object = resume_object
        
        # Skapa LLM-instans med SAMMA TIMEOUT SOM URSPRUNGLIG
        self.llm = LoggerChatModel(
            ChatOpenAI(
                model_name="gpt-4o-mini",
                openai_api_key=api_key,
                temperature=0.4,
                timeout=60
            )
        )
        
        # Modern Design 2 använder befintlig HTML-struktur men med kreativ CSS
        self.load_css_style()
    
    def load_css_style(self):
        """Laddar CSS-stil för Modern Design 2"""
        try:
            css_path = Path(__file__).parent / "style_modern2.css"
            with open(css_path, 'r', encoding='utf-8') as f:
                self.css_content = f.read()
                
            logger.info("Modern Design 2 CSS laddad framgångsrikt")
            
        except Exception as e:
            logger.error(f"Fel vid laddning av Modern Design 2 CSS: {e}")
            raise
    
    def generate_personal_information_section(self, job_description: Optional[str] = None) -> str:
        """Genererar personlig information sektion - anpassad för kreativ design"""
        
        personal_info = self.resume_object.personal_information
        
        prompt = f"""
Du är en expert på att skriva CV-sektioner för KREATIVA DESIGNER. Skapa en personlig information sektion för en kreativ CV med färgglad sidopanel.

PERSONLIG DATA:
Namn: {personal_info.name if personal_info else 'N/A'}
Email: {personal_info.email if personal_info else 'N/A'}
Telefon: {personal_info.phone if personal_info else 'N/A'}
Stad: {personal_info.city if personal_info else 'N/A'}

JOBBESKRIVNING (för anpassning):
{job_description or "Ingen specifik jobbeskrivning"}

INSTRUKTIONER:
1. Skapa en KREATIV och MODERN personlig sektion
2. Använd HTML-struktur som fungerar med färgglad sidopanel-design
3. Fokusera på KREATIVITET och INNOVATION
4. Anpassa till jobbeskrivningen om given
5. Använd professionell men kreativ ton

STRUKTUR:
<section id="personal-info">
    <h1>[Fullständigt namn]</h1>
    <h2>[Kreativ jobbtitel]</h2>
    <p>[Kreativ professionell sammanfattning som framhäver innovation och kreativitet]</p>
    <div>
        <span>📧 [email]</span>
        <span>📱 [telefon]</span>
        <span>📍 [stad]</span>
    </div>
</section>

SPRÅK: Svenska
Generera ENDAST HTML-koden, ingen förklaring:
"""
        
        try:
            response = self.llm([{"role": "user", "content": prompt}])
            return response.strip()
        except Exception as e:
            logger.error(f"Fel vid generering av personlig information: {e}")
            return self._fallback_personal_info()
    
    def generate_experience_section(self, job_description: Optional[str] = None) -> str:
        """Genererar arbetslivserfarenhet - anpassad för kreativ design"""
        
        experience_data = self.resume_object.experience_details
        
        prompt = f"""
Du är en expert på att skriva CV-sektioner för KREATIVA DESIGNER. Skapa en arbetslivserfarenhet sektion för en kreativ CV.

ERFARENHETSDATA:
{self._format_experience_data(experience_data)}

JOBBESKRIVNING (för anpassning):
{job_description or "Ingen specifik jobbeskrivning"}

INSTRUKTIONER:
1. Skapa KREATIV och ENGAGERANDE beskrivning av arbetslivserfarenhet
2. Framhäv INNOVATION, KREATIVITET och PROBLEMLÖSNING
3. Använd AKTIVA VERB och KONKRETA RESULTAT
4. Anpassa till jobbeskrivningen för att visa relevans
5. Kreativ men professionell ton

STRUKTUR:
<section id="experience">
    <h2>Experience</h2>
    <div class="entry">
        <div class="entry-title">[Kreativ jobbtitel]</div>
        <div class="entry-company">[Företag]</div>
        <div class="entry-location">[Plats]</div>
        <div class="entry-year">[Period]</div>
        <div class="entry-description">[Kreativ beskrivning som framhäver innovation och resultat]</div>
    </div>
</section>

SPRÅK: Svenska
Generera ENDAST HTML-koden, ingen förklaring:
"""
        
        try:
            response = self.llm([{"role": "user", "content": prompt}])
            return response.strip()
        except Exception as e:
            logger.error(f"Fel vid generering av erfarenhetssektion: {e}")
            return self._fallback_experience_section()
    
    def generate_education_section(self, job_description: Optional[str] = None) -> str:
        """Genererar utbildningssektion - anpassad för kreativ design"""
        
        education_data = self.resume_object.education_details
        
        prompt = f"""
Du är en expert på att skriva CV-sektioner för KREATIVA DESIGNER. Skapa en utbildningssektion för en kreativ CV.

UTBILDNINGSDATA:
{self._format_education_data(education_data)}

JOBBESKRIVNING (för anpassning):
{job_description or "Ingen specifik jobbeskrivning"}

INSTRUKTIONER:
1. Framhäv KREATIVA och TEKNISKA kurser
2. Fokusera på INNOVATION och MODERN TEKNIK
3. Anpassa till jobbeskrivningen om given
4. Kreativ presentation av utbildning

STRUKTUR:
<section id="education">
    <h2>Education</h2>
    <div class="entry">
        <div class="entry-title">[Utbildningsnamn med fokus på kreativitet/teknik]</div>
        <div class="entry-company">[Institution]</div>
        <div class="entry-location">[Plats]</div>
        <div class="entry-year">[Period]</div>
        <div class="entry-description">[Kreativ beskrivning av relevanta kurser och projekt]</div>
    </div>
</section>

SPRÅK: Svenska
Generera ENDAST HTML-koden, ingen förklaring:
"""
        
        try:
            response = self.llm([{"role": "user", "content": prompt}])
            return response.strip()
        except Exception as e:
            logger.error(f"Fel vid generering av utbildningssektion: {e}")
            return self._fallback_education_section()
    
    def generate_skills_section(self, job_description: Optional[str] = None) -> str:
        """Genererar färdighetssektion - anpassad för kreativ design"""
        
        # Samla alla färdigheter från olika källor
        skills = []
        if self.resume_object.interests:
            skills.extend(self.resume_object.interests[:8])  # Top 8 intressen
        
        # Lägg till tekniska färdigheter från erfarenheter
        if self.resume_object.experience_details:
            for exp in self.resume_object.experience_details:
                if hasattr(exp, 'skills_acquired') and exp.skills_acquired:
                    skills.extend(exp.skills_acquired[:3])  # Top 3 från varje jobb
        
        prompt = f"""
Du är en expert på att skriva CV-sektioner för KREATIVA DESIGNER. Skapa en färdighetssektion för en kreativ CV.

FÄRDIGHETSDATA:
{', '.join(skills[:12]) if skills else 'Inga färdigheter listade'}

JOBBESKRIVNING (för anpassning):
{job_description or "Ingen specifik jobbeskrivning"}

INSTRUKTIONER:
1. Skapa VISUELLT TILLTALANDE färdighetssektion
2. Gruppera färdigheter i KREATIVA KATEGORIER
3. Framhäv TEKNISKA och KREATIVA färdigheter
4. Anpassa till jobbeskrivningen om given
5. Använd modern och kreativ presentation

STRUKTUR:
<section id="skills">
    <h2>Skills & Expertise</h2>
    <ul>
        <li>[Kreativ/Teknisk färdighet]</li>
        <li>[Kreativ/Teknisk färdighet]</li>
        <li>[Kreativ/Teknisk färdighet]</li>
    </ul>
</section>

SPRÅK: Svenska
Generera ENDAST HTML-koden, ingen förklaring:
"""
        
        try:
            response = self.llm([{"role": "user", "content": prompt}])
            return response.strip()
        except Exception as e:
            logger.error(f"Fel vid generering av färdighetssektion: {e}")
            return self._fallback_skills_section()
    
    def generate_languages_section(self) -> str:
        """Genererar språksektion - anpassad för kreativ design"""
        
        languages = self.resume_object.languages
        
        prompt = f"""
Du är en expert på att skriva CV-sektioner för KREATIVA DESIGNER. Skapa en språksektion för en kreativ CV.

SPRÅKDATA:
{self._format_languages_data(languages)}

INSTRUKTIONER:
1. Skapa KREATIV presentation av språkkunskaper
2. Använd VISUELLT TILLTALANDE format
3. Framhäv INTERNATIONELL kompetens
4. Modern och kreativ stil

STRUKTUR:
<section id="languages">
    <h2>Languages</h2>
    <ul>
        <li>[Språk] - [Kreativ beskrivning av nivå]</li>
    </ul>
</section>

SPRÅK: Svenska
Generera ENDAST HTML-koden, ingen förklaring:
"""
        
        try:
            response = self.llm([{"role": "user", "content": prompt}])
            return response.strip()
        except Exception as e:
            logger.error(f"Fel vid generering av språksektion: {e}")
            return self._fallback_languages_section()
    
    def generate_complete_cv(self, job_description: Optional[str] = None) -> str:
        """Genererar komplett CV för Modern Design 2 - SAMMA INTERFACE SOM URSPRUNGLIG"""
        
        logger.info("Genererar komplett CV för Modern Design 2")
        
        try:
            # Generera alla sektioner med kreativ AI
            personal_html = self.generate_personal_information_section(job_description)
            experience_html = self.generate_experience_section(job_description)
            education_html = self.generate_education_section(job_description)
            skills_html = self.generate_skills_section(job_description)
            languages_html = self.generate_languages_section()
            
            # Kombinera alla sektioner (SAMMA STRUKTUR SOM URSPRUNGLIG)
            body_html = f"""
<body>
    {personal_html}
    {experience_html}
    {education_html}
    {skills_html}
    {languages_html}
</body>
"""
            
            # Använd global HTML-template och injicera CSS (SAMMA SOM URSPRUNGLIG)
            from string import Template
            global_html_template = Template(global_config.html_template)
            
            complete_html = global_html_template.safe_substitute(
                body=body_html,
                style_css=self.css_content
            )
            
            logger.info("Modern Design 2 CV genererat framgångsrikt")
            return complete_html
            
        except Exception as e:
            logger.error(f"Fel vid generering av komplett Modern Design 2 CV: {e}")
            raise
    
    def _format_education_data(self, education_data: List) -> str:
        """Formaterar utbildningsdata för AI-prompt"""
        if not education_data:
            return "Ingen utbildningsdata tillgänglig"
        
        formatted = []
        for edu in education_data:
            formatted.append(f"- {edu.education_level} vid {edu.institution}, {edu.location} ({edu.start_date}-{edu.year_of_completion})")
        
        return "\n".join(formatted)
    
    def _format_experience_data(self, experience_data: List) -> str:
        """Formaterar erfarenhetsdata för AI-prompt"""
        if not experience_data:
            return "Ingen arbetslivserfarenhet tillgänglig"
        
        formatted = []
        for exp in experience_data:
            formatted.append(f"""
Jobbtitel: {exp.position}
Företag: {exp.company}
Period: {exp.employment_period}
Plats: {exp.location}
Beskrivning: {exp.key_responsibilities[0].description if exp.key_responsibilities else 'Ingen beskrivning'}
""")
        
        return "\n".join(formatted)
    
    def _format_languages_data(self, languages: List) -> str:
        """Formaterar språkdata för AI-prompt"""
        if not languages:
            return "Ingen språkdata tillgänglig"
        
        formatted = []
        for lang in languages:
            if hasattr(lang, 'language') and hasattr(lang, 'proficiency'):
                formatted.append(f"- {lang.language}: {lang.proficiency}")
            else:
                formatted.append(f"- {lang}")
        
        return "\n".join(formatted)
    
    # Fallback-metoder för när AI-generering misslyckas
    def _fallback_personal_info(self) -> str:
        """Fallback för personlig information"""
        return '''<section id="personal-info">
    <h1>Kreativ Professionell</h1>
    <h2>Designer & Utvecklare</h2>
    <p>Innovativ och kreativ professionell med passion för modern design och teknik.</p>
    <div>
        <span>📧 email@example.com</span>
        <span>📱 070-123 45 67</span>
        <span>📍 Stockholm</span>
    </div>
</section>'''
    
    def _fallback_experience_section(self) -> str:
        """Fallback för erfarenhetssektion"""
        return '''<section id="experience">
    <h2>Experience</h2>
    <div class="entry">
        <div class="entry-title">Kreativ Yrkesroll</div>
        <div class="entry-company">Innovativt Företag</div>
        <div class="entry-location">Stockholm</div>
        <div class="entry-year">2020-2024</div>
        <div class="entry-description">Ledde kreativa projekt och utvecklade innovativa lösningar.</div>
    </div>
</section>'''
    
    def _fallback_education_section(self) -> str:
        """Fallback för utbildningssektion"""
        return '''<section id="education">
    <h2>Education</h2>
    <div class="entry">
        <div class="entry-title">Kreativ Utbildning</div>
        <div class="entry-company">Teknisk Högskola</div>
        <div class="entry-location">Sverige</div>
        <div class="entry-year">2020-2024</div>
        <div class="entry-description">Fokus på kreativ design och modern teknik.</div>
    </div>
</section>'''
    
    def _fallback_skills_section(self) -> str:
        """Fallback för färdighetssektion"""
        return '''<section id="skills">
    <h2>Skills & Expertise</h2>
    <ul>
        <li>Kreativ Design</li>
        <li>Modern Teknik</li>
        <li>Innovation</li>
        <li>Problemlösning</li>
    </ul>
</section>'''
    
    def _fallback_languages_section(self) -> str:
        """Fallback för språksektion"""
        return '''<section id="languages">
    <h2>Languages</h2>
    <ul>
        <li>Svenska - Modersmål</li>
        <li>Engelska - Flytande</li>
    </ul>
</section>'''


def create_modern_design2_cv(api_key: str, resume_object: Any, job_description: Optional[str] = None) -> str:
    """
    Huvudfunktion för att skapa CV med Modern Design 2
    
    Args:
        api_key: OpenAI API-nyckel
        resume_object: Resume-objekt med data
        job_description: Valfri jobbeskrivning för anpassning
    
    Returns:
        Komplett HTML-sträng för CV:et
    """
    generator = ModernDesign2Generator(api_key, resume_object)
    return generator.generate_complete_cv(job_description)


if __name__ == "__main__":
    # Test-kod för att verifiera generatorn
    print("🧪 TESTAR MODERN DESIGN 2 GENERATOR")
    print("=" * 50)
    print("⚠️ Detta är en test-version. Integrera med riktigt resume-objekt för produktion.")
