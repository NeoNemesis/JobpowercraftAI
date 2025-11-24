"""
Cover Letter Generator för Modern Design 1
✅ Genererar professionella personliga brev
✅ AI-anpassning till jobbeskrivning
✅ Samma design-språk som CV:et
"""

from pathlib import Path
from typing import Any, Optional
from datetime import datetime
from loguru import logger
from .language_detector import detect_job_language
from .isolated_utils import create_isolated_llm, image_to_base64

class ModernDesign1CoverLetterGenerator:
    """
    Generator för personliga brev med Modern Design 1 stil
    """
    
    def __init__(self, resume_object: Any, api_key: str):
        self.resume_object = resume_object
        self.api_key = api_key
        self.language = 'sv'
        self.llm = create_isolated_llm(api_key) if api_key else None
        logger.info("📧 ModernDesign1CoverLetterGenerator initialiserad")
    
    def _get_profile_image_base64(self) -> str:
        """Hämtar profilbild som base64"""
        try:
            possible_paths = [
                "assets/victorvilches.png",
                "assets/Vilchesab.png",
                "data_folder/profil_no_bg.png",
                "data_folder/profil.jpg",
                "data_folder/profile.png"
            ]
            
            for path in possible_paths:
                if Path(path).exists():
                    return image_to_base64(path)
            
            return ""
        except Exception as e:
            logger.error(f"❌ Fel vid profilbild: {e}")
            return ""
    
    def _get_translations(self) -> dict:
        """Översättningar för olika språk"""
        return {
            'sv': {
                'job_title': 'DATAINGENJÖR • SYSTEMUTVECKLARE',
                'recipient_title': 'Rekryteringsteam',
                'job_application': 'Jobbansökan för',
                'salutation': 'Bästa rekryteringsteam,',
                'section1_title': 'Om Mig',
                'section2_title': 'Varför',
                'section3_title': 'Varför Jag',
                'closing': 'Med vänlig hälsning,',
                'attachment': 'Bilaga: Curriculum Vitae',
                'quote': 'Innovation är att se vad alla har sett och tänka vad ingen har tänkt.'
            },
            'en': {
                'job_title': 'COMPUTER ENGINEER • SYSTEM DEVELOPER',
                'recipient_title': 'Recruitment Team',
                'job_application': 'Job Application for',
                'salutation': 'Dear Hiring Manager,',
                'section1_title': 'About Me',
                'section2_title': 'Why',
                'section3_title': 'Why Me',
                'closing': 'Sincerely,',
                'attachment': 'Attached: Curriculum Vitae',
                'quote': 'Innovation is seeing what everyone has seen and thinking what no one has thought.'
            }
        }
    
    def _generate_personal_info(self) -> tuple:
        """Hämtar personlig information"""
        try:
            personal_info = self.resume_object.personal_information
            if not personal_info:
                return self._get_fallback_personal_info()
            
            name = getattr(personal_info, 'name', 'Victor')
            surname = getattr(personal_info, 'surname', 'Vilches')
            full_name = f"{name} {surname} C."
            
            email = getattr(personal_info, 'email', 'victorvilches@protonmail.com')
            phone = getattr(personal_info, 'phone', '707978547')
            address = getattr(personal_info, 'address', 'Kvarnängsgatan 24')
            city = getattr(personal_info, 'city', 'Uppsala')
            zip_code = getattr(personal_info, 'zip_code', '75420')
            country = getattr(personal_info, 'country', 'Sverige')
            website = getattr(personal_info, 'website', 'vilchesab.se')
            
            # Formatera kontaktinfo
            contact_parts = []
            contact_parts.append(f'<div>📍 {address}, {city}, {zip_code}, {country}</div>')
            contact_parts.append(f'<div>📱 {phone}</div>')
            contact_parts.append(f'<div>📧 {email}</div>')
            contact_parts.append(f'<div>🌐 {website}</div>')
            
            contact_html = '\n                    '.join(contact_parts)
            
            return full_name, contact_html
            
        except Exception as e:
            logger.error(f"❌ Fel vid personlig info: {e}")
            return self._get_fallback_personal_info()
    
    def _get_fallback_personal_info(self) -> tuple:
        """Fallback personlig info"""
        contact_html = '''<div>📍 Uppsala, Sverige</div>
                    <div>📱 070-XXX XX XX</div>
                    <div>📧 email@example.com</div>
                    <div>🌐 website.se</div>'''
        return "Victor Vilches C.", contact_html
    
    def _ai_generate_cover_letter_content(self, job_description: str, company_name: str, position_title: str) -> dict:
        """Använder AI för att generera personligt brev innehåll"""
        try:
            # Bygg prompt
            lang_name = "Swedish" if self.language == 'sv' else "English"
            translations = self._get_translations()[self.language]
            
            prompt = f"""You are a professional cover letter writer. Generate content for a modern cover letter.

Job Description:
{job_description[:800]}

Company: {company_name}
Position: {position_title}

Applicant Background:
- Computer Engineering student (2 of 3 years completed)
- System integration specialist
- Full-stack web developer
- Entrepreneur (owns construction company)
- Experience in healthcare and IT

Instructions:
1. Write in {lang_name}
2. Create THREE compelling sections:
   - Section 1 ({translations['section1_title']}): Brief introduction and current role
   - Section 2 ({translations['section2_title']} {company_name}): Why interested in THIS company
   - Section 3 ({translations['section3_title']}): Why YOU are the perfect fit
3. Be PROFESSIONAL but ENGAGING
4. Each section should be EXACTLY 2-3 sentences (KEEP IT SHORT!)
5. Show ENTHUSIASM and CONCRETE SKILLS
6. Match the job requirements
7. TOTAL LENGTH: Cover letter MUST fit on ONE page

Return ONLY a JSON object with these keys (no markdown, no explanations):
{{
    "section1": "text here",
    "section2": "text here",
    "section3": "text here"
}}
"""
            
            ai_response = self.llm.invoke(prompt)
            
            # Försök parsa JSON
            import json
            import re
            
            # Rensa bort markdown om det finns
            cleaned = ai_response.replace('```json', '').replace('```', '').strip()
            
            # Hitta JSON-objekt
            json_match = re.search(r'\{[^{}]*"section1"[^{}]*\}', cleaned, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                content = json.loads(json_str)
                logger.info("✅ AI-genererat cover letter innehåll")
                return content
            else:
                logger.warning("⚠️ Kunde inte parsa AI-svar, använder fallback")
                return self._get_fallback_content(company_name, position_title)
                
        except Exception as e:
            logger.error(f"❌ AI-generering misslyckades: {e}")
            return self._get_fallback_content(company_name, position_title)
    
    def _get_fallback_content(self, company_name: str, position_title: str) -> dict:
        """Fallback innehåll - KORTARE VERSION"""
        if self.language == 'en':
            return {
                "section1": f"I am writing to express my strong interest in the {position_title} position at {company_name}. As a Computer Engineering student with hands-on experience in system integration and full-stack development, I am excited to contribute to your team.",
                "section2": f"I am particularly drawn to {company_name} because of your innovative approach to technology. Your focus on modern solutions aligns perfectly with my passion for system integration and development.",
                "section3": "With my combination of academic knowledge and practical experience in web development, databases, and system administration, I am confident I can make valuable contributions. My entrepreneurial background has taught me project management and the importance of delivering quality results."
            }
        else:
            return {
                "section1": f"Jag skriver för att uttrycka mitt starka intresse för {position_title}-rollen hos {company_name}. Som Dataingenjörsstudent med praktisk erfarenhet av systemintegration och fullstack-utveckling ser jag fram emot att bidra till ert team.",
                "section2": f"Jag är särskilt intresserad av {company_name} på grund av er innovativa approach till teknik. Ert fokus på moderna lösningar passar perfekt med min passion för systemintegration och modern utveckling.",
                "section3": "Med min kombination av akademisk kunskap och praktisk erfarenhet av webbutveckling, databaser och systemadministration är jag övertygad om att jag kan göra värdefulla bidrag. Min entreprenörsbakgrund har lärt mig projektledning och vikten av att leverera kvalitetsresultat."
            }
    
    def generate_cover_letter_html(self, job_description: str, company_name: str, 
                                   position_title: str, company_address: str = "") -> str:
        """
        Genererar komplett personligt brev HTML
        
        Args:
            job_description: Jobbeskrivning
            company_name: Företagsnamn
            position_title: Position/titel
            company_address: Företagsadress (valfritt)
        
        Returns:
            Komplett HTML för personligt brev
        """
        try:
            # Detektera språk
            self.language = detect_job_language(job_description)
            logger.info(f"🌍 Cover Letter språk: {self.language}")
            
            # Hämta översättningar
            translations = self._get_translations()[self.language]
            
            # Hämta personlig info
            full_name, contact_html = self._generate_personal_info()
            
            # Hämta profilbild
            profile_image = self._get_profile_image_base64()
            
            # Generera datum
            current_date = datetime.now()
            if self.language == 'en':
                date_str = current_date.strftime("%B %d, %Y")
            else:
                months_sv = ['januari', 'februari', 'mars', 'april', 'maj', 'juni',
                            'juli', 'augusti', 'september', 'oktober', 'november', 'december']
                date_str = f"{current_date.day} {months_sv[current_date.month-1]} {current_date.year}"
            
            # AI-generera innehåll
            if self.llm:
                content = self._ai_generate_cover_letter_content(job_description, company_name, position_title)
            else:
                content = self._get_fallback_content(company_name, position_title)
            
            # Formatera företagsinfo
            if not company_address:
                company_address = "" if self.language == 'en' else ""
            
            # Formatera jobbansökningstitel
            job_app_title = f"{translations['job_application']} {position_title}"
            
            # Ladda template
            template_path = Path(__file__).parent / "cover_letter_template.html"
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()
            
            # Ersätt placeholders
            from string import Template
            template_obj = Template(template)
            
            complete_html = template_obj.substitute(
                profile_image=profile_image,
                full_name=full_name,
                job_title=translations['job_title'],
                contact_info=contact_html,
                quote=translations['quote'],
                date=date_str,
                recipient_title=translations['recipient_title'],
                company_name=company_name.upper(),
                company_address=company_address,
                job_application_title=job_app_title,
                salutation=translations['salutation'],
                section1_title=translations['section1_title'],
                section1_content=content.get('section1', ''),
                section2_title=f"{translations['section2_title']} {company_name}?",
                section2_content=content.get('section2', ''),
                section3_title=translations['section3_title'],
                section3_content=content.get('section3', ''),
                closing_text=translations['closing'],
                attachment_text=translations['attachment']
            )
            
            logger.info(f"✅ Cover Letter genererat ({len(complete_html)} tecken)")
            return complete_html
            
        except Exception as e:
            logger.error(f"❌ Fel vid cover letter-generering: {e}")
            raise

