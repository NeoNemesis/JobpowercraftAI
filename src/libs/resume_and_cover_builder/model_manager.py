#!/usr/bin/env python3
"""
ModelManager - Hanterar val mellan olika CV-modeller/mappar
Varje mapp har sin egen AI-modell och logik som är specialiserad för den designen.
"""

import os
import inquirer
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from loguru import logger

class ModelManager:
    """
    Hanterar val mellan olika CV-modeller och deras isolerade logik.
    Varje modell har sin egen mapp med specialiserad AI och struktur.
    """
    
    def __init__(self):
        self.selected_model = None
        self.selected_template = None
        
        # Definiera alla tillgängliga modeller/mappar
        current_file = Path(__file__).resolve()
        base_dir = current_file.parent
        
        self.models = {
            "URSPRUNGLIGA": {
                "name": "Ursprungliga Stilar",
                "description": "Klassiska CV-stilar med befintlig AI-logik",
                "directory": base_dir / "resume_style",
                "ai_module": "standard_ai",
                "templates": self._get_original_styles()
            },
            "MODERN_DESIGN_1": {
                "name": "Modern Design 1",
                "description": "Tvåkolumns layout med vertikal accent-linje",
                "directory": base_dir / "moderndesign1",
                "ai_module": "moderndesign1.ai_generator",
                "templates": self._get_moderndesign1_templates()
            },
            "MODERN_DESIGN_2": {
                "name": "Modern Design 2", 
                "description": "Kreativ design med färgglad sidopanel",
                "directory": base_dir / "moderndesign2",
                "ai_module": "moderndesign2.ai_generator",
                "templates": self._get_moderndesign2_templates()
            }
        }
        
        logger.info(f"ModelManager initialiserad med {len(self.models)} modeller")
    
    def _get_original_styles(self) -> List[str]:
        """Hämtar alla ursprungliga stilar från resume_style mappen"""
        styles = []
        styles_dir = Path(__file__).parent / "resume_style"
        
        if styles_dir.exists():
            for css_file in styles_dir.glob("*.css"):
                try:
                    with open(css_file, 'r', encoding='utf-8') as f:
                        first_line = f.readline().strip()
                        if first_line.startswith("/*") and first_line.endswith("*/"):
                            style_name = first_line[2:-2].strip()
                            styles.append(style_name)
                except Exception as e:
                    logger.warning(f"Kunde inte läsa stil från {css_file}: {e}")
        
        return styles
    
    def _get_moderndesign1_templates(self) -> List[str]:
        """Hämtar alla mallar från moderndesign1 mappen"""
        templates = []
        design1_dir = Path(__file__).parent / "moderndesign1"
        
        if design1_dir.exists():
            # Kolla efter CSS-filer
            for css_file in design1_dir.glob("*.css"):
                try:
                    with open(css_file, 'r', encoding='utf-8') as f:
                        first_line = f.readline().strip()
                        if first_line.startswith("/*") and first_line.endswith("*/"):
                            template_name = first_line[2:-2].strip()
                            templates.append(template_name)
                except Exception as e:
                    logger.warning(f"Kunde inte läsa mall från {css_file}: {e}")
            
            # Om inga CSS-kommentarer hittades, lägg till standard
            if not templates:
                templates.append("Modern Design 1 - Default")
        
        return templates
    
    def _get_moderndesign2_templates(self) -> List[str]:
        """Hämtar alla mallar från moderndesign2 mappen"""
        # Modern Design 2 har en huvuddesign: Kreativ Sidopanel
        templates = ["Modern Design 2 - Creative Bold"]
        
        logger.debug("Modern Design 2 mallar laddade: Creative Bold")
        return templates
    
    def select_model_interactive(self) -> Optional[str]:
        """
        Låter användaren välja modell interaktivt
        
        Returns:
            Vald modell-ID eller None om avbrutet
        """
        try:
            # Skapa val-lista med beskrivningar
            choices = []
            for model_id, model_info in self.models.items():
                choice_text = f"{model_info['name']} - {model_info['description']}"
                choices.append((choice_text, model_id))
            
            questions = [
                inquirer.List(
                    "model",
                    message="Välj CV-modell/design:",
                    choices=[choice[0] for choice in choices],
                    default=choices[0][0] if choices else None
                )
            ]
            
            answer = inquirer.prompt(questions)
            if answer:
                selected_text = answer['model']
                # Hitta motsvarande model_id
                for choice_text, model_id in choices:
                    if choice_text == selected_text:
                        self.selected_model = model_id
                        logger.info(f"Vald modell: {model_id} ({self.models[model_id]['name']})")
                        return model_id
            
            return None
            
        except (KeyboardInterrupt, EOFError):
            logger.info("Modell-val avbrutet av användare")
            return None
    
    def select_template_for_model(self, model_id: str) -> Optional[str]:
        """
        Låter användaren välja mall inom en specifik modell
        
        Args:
            model_id: ID för vald modell
            
        Returns:
            Vald mall-namn eller None om avbrutet
        """
        if model_id not in self.models:
            logger.error(f"Okänd modell: {model_id}")
            return None
        
        model_info = self.models[model_id]
        templates = model_info["templates"]
        
        if not templates:
            logger.warning(f"Inga mallar hittades för modell {model_id}")
            return None
        
        if len(templates) == 1:
            # Om bara en mall finns, välj den automatiskt
            self.selected_template = templates[0]
            logger.info(f"Använder enda tillgängliga mall: {templates[0]}")
            return templates[0]
        
        try:
            questions = [
                inquirer.List(
                    "template",
                    message=f"Välj mall för {model_info['name']}:",
                    choices=templates,
                    default=templates[0]
                )
            ]
            
            answer = inquirer.prompt(questions)
            if answer:
                selected = answer['template']
                self.selected_template = selected
                logger.info(f"Vald mall: {selected}")
                return selected
            
            return None
            
        except (KeyboardInterrupt, EOFError):
            logger.info("Mall-val avbrutet av användare")
            return None
    
    def get_model_info(self, model_id: str) -> Optional[Dict]:
        """Hämtar information om en specifik modell"""
        return self.models.get(model_id)
    
    def get_available_models(self) -> Dict[str, Dict]:
        """Hämtar alla tillgängliga modeller"""
        return self.models
    
    def get_ai_generator_for_model(self, model_id: str, api_key: str, resume_object: Any):
        """
        Skapar rätt AI-generator för vald modell
        
        Args:
            model_id: ID för vald modell
            api_key: OpenAI API-nyckel
            resume_object: Resume-data
            
        Returns:
            Specialiserad AI-generator för modellen
        """
        if model_id not in self.models:
            raise ValueError(f"Okänd modell: {model_id}")
        
        model_info = self.models[model_id]
        
        if model_id == "MODERN_DESIGN_1":
            from .moderndesign1.ai_generator import ModernDesign1Generator
            return ModernDesign1Generator(api_key, resume_object)
            
        elif model_id == "MODERN_DESIGN_2":
            from .moderndesign2.ai_generator import ModernDesign2Generator
            return ModernDesign2Generator(api_key, resume_object)
            
        elif model_id == "URSPRUNGLIGA":
            # Använd standard ResumeGenerator för ursprungliga stilar
            from .resume_generator import ResumeGenerator
            generator = ResumeGenerator()
            generator.set_resume_object(resume_object)
            return generator
            
        else:
            raise ValueError(f"Ingen AI-generator definierad för modell: {model_id}")
    
    def create_cv_with_selected_model(self, api_key: str, resume_object: Any, job_description: Optional[str] = None) -> str:
        """
        Skapar CV med vald modell och mall
        
        Args:
            api_key: OpenAI API-nyckel
            resume_object: Resume-data
            job_description: Valfri jobbeskrivning
            
        Returns:
            Komplett HTML för CV:et
        """
        if not self.selected_model:
            raise ValueError("Ingen modell vald. Anropa select_model_interactive() först.")
        
        if not self.selected_template:
            raise ValueError("Ingen mall vald. Anropa select_template_for_model() först.")
        
        logger.info(f"🤖 Skapar CV med modell: {self.selected_model}, mall: {self.selected_template}")
        
        try:
            # Hämta specialiserad AI-generator
            ai_generator = self.get_ai_generator_for_model(self.selected_model, api_key, resume_object)
            
            if self.selected_model == "MODERN_DESIGN_1":
                logger.info("🟢 Använder Modern Design 1 specialiserad generator")
                html_content = ai_generator.generate_complete_cv(job_description)
                
            elif self.selected_model == "MODERN_DESIGN_2":
                logger.info("🟡 Använder Modern Design 2 specialiserad generator")
                html_content = ai_generator.generate_complete_cv(job_description)
                
            elif self.selected_model == "URSPRUNGLIGA":
                logger.info("🔵 Använder ursprunglig ResumeGenerator")
                from .style_manager import StyleManager
                style_manager = StyleManager()
                style_manager.set_selected_style(self.selected_template)
                style_path = style_manager.get_style_path()
                
                if not style_path:
                    raise ValueError(f"Kunde inte hitta sökväg för stil: {self.selected_template}")
                
                if job_description:
                    html_content = ai_generator.create_resume_job_description_text(style_path, job_description)
                else:
                    html_content = ai_generator.create_resume(style_path)
            
            else:
                raise ValueError(f"Okänd modell: {self.selected_model}")
            
            # Validera att HTML genererades
            if not html_content or len(html_content.strip()) < 100:
                raise ValueError(f"AI-generator producerade för lite innehåll: {len(html_content)} tecken")
            
            logger.info(f"✅ CV HTML genererat framgångsrikt: {len(html_content)} tecken")
            return html_content
            
        except Exception as e:
            logger.error(f"❌ Fel vid CV-generering med {self.selected_model}: {e}")
            logger.error(f"   Modell: {self.selected_model}")
            logger.error(f"   Mall: {self.selected_template}")
            logger.error(f"   Jobbeskrivning: {'Ja' if job_description else 'Nej'}")
            raise


class ModelAwareResumeSystem:
    """
    Huvudsystem som koordinerar alla modeller och deras AI-generatorer
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.model_manager = ModelManager()
        self.resume_object = None
        
        # MODERN DESIGN 1 använder sin egen isolerade API-hantering
        # Andra modeller kan fortfarande använda global_config om behövs
        logger.info("ModelAwareResumeSystem initialiserat")
    
    def set_resume_object(self, resume_object: Any):
        """Sätter resume-objekt för alla modeller"""
        self.resume_object = resume_object
        logger.info("Resume object satt för alla modeller")
    
    def interactive_model_and_template_selection(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Interaktiv process för att välja modell och mall
        
        Returns:
            Tuple med (model_id, template_name) eller (None, None) om avbrutet
        """
        # Steg 1: Välj modell
        selected_model = self.model_manager.select_model_interactive()
        if not selected_model:
            return None, None
        
        # Steg 2: Välj mall inom modellen
        selected_template = self.model_manager.select_template_for_model(selected_model)
        if not selected_template:
            return None, None
        
        return selected_model, selected_template
    
    def generate_cv_with_job_description(self, job_url: str) -> Tuple[str, str]:
        """
        Genererar CV baserat på jobb-URL med vald modell - ANVÄNDER SHARED JOB SCRAPER
        
        Args:
            job_url: URL till jobbet
            
        Returns:
            Tuple med (base64_pdf, suggested_name)
        """
        if not self.resume_object:
            raise ValueError("Resume object måste sättas innan CV kan genereras")
        
        if not self.model_manager.selected_model or not self.model_manager.selected_template:
            raise ValueError("Modell och mall måste väljas innan CV kan genereras")
        
        logger.info(f"Genererar CV för jobb: {job_url}")
        logger.info(f"Använder modell: {self.model_manager.selected_model}")
        logger.info(f"Använder mall: {self.model_manager.selected_template}")
        
        # ANVÄND SHARED JOB SCRAPER för konsistent jobbskrapning
        from src.libs.resume_and_cover_builder.shared_job_scraper import scrape_job_unified
        from src.utils.chrome_utils import init_browser, HTML_to_PDF
        
        # 1. Skrapa jobbet - använd modell-specifik scraper för Modern Design 1
        logger.info(f"🔍 DEBUG: self.model_manager.selected_model = '{self.model_manager.selected_model}' (type: {type(self.model_manager.selected_model)})")
        logger.info(f"🔍 DEBUG: Jämför med 'MODERN_DESIGN_1': {self.model_manager.selected_model == 'MODERN_DESIGN_1'}")
        
        if self.model_manager.selected_model == "MODERN_DESIGN_1":
            logger.info("🎨 Modern Design 1: Använder ISOLERAD standalone generering")
            # Använd helt isolerad Modern Design 1 (som förenklad version)
            from src.libs.resume_and_cover_builder.moderndesign1.standalone import generate_modern_design1_with_resume_object
            result_base64, suggested_name = generate_modern_design1_with_resume_object(job_url, self.resume_object)
            
            # Returnera direkt - ingen HTML-konvertering behövs
            return result_base64, suggested_name
            
        else:
            # Använd gemensam scraper för andra modeller
            logger.info("📄 Använder gemensam scraper för andra modeller")
            job, suggested_name = scrape_job_unified(self.api_key, job_url)
            
            # 2. Generera HTML med vald modells AI-generator
            html_content = self.model_manager.create_cv_with_selected_model(
                self.api_key, 
                self.resume_object, 
                job.description
            )
        
        # 3. Konvertera till PDF
        driver = init_browser()
        try:
            result_base64 = HTML_to_PDF(html_content, driver)
            logger.info(f"PDF genererat framgångsrikt: {suggested_name}")
            return result_base64, suggested_name
        finally:
            driver.quit()
    
    def generate_standard_cv(self) -> str:
        """
        Genererar standard CV utan jobbeskrivning
        
        Returns:
            Komplett HTML för CV:et
        """
        if not self.resume_object:
            raise ValueError("Resume object måste sättas innan CV kan genereras")
        
        if not self.model_manager.selected_model or not self.model_manager.selected_template:
            raise ValueError("Modell och mall måste väljas innan CV kan genereras")
        
        logger.info("Genererar standard CV")
        logger.info(f"Använder modell: {self.model_manager.selected_model}")
        logger.info(f"Använder mall: {self.model_manager.selected_template}")
        
        return self.model_manager.create_cv_with_selected_model(
            self.api_key, 
            self.resume_object, 
            None
        )
    
    def get_model_statistics(self) -> Dict[str, Any]:
        """Hämtar statistik om alla modeller"""
        stats = {}
        
        for model_id, model_info in self.model_manager.models.items():
            stats[model_id] = {
                "name": model_info["name"],
                "description": model_info["description"],
                "directory_exists": model_info["directory"].exists(),
                "template_count": len(model_info["templates"]),
                "templates": model_info["templates"]
            }
        
        return stats


def demonstrate_hierarchical_flow():
    """Demonstrerar det hierarkiska flödet"""
    
    print("🔄 HIERARKISKT FLÖDE - STEG FÖR STEG")
    print("=" * 60)
    
    flow_steps = [
        {
            "step": "1️⃣ FÖRSTA FRÅGAN - VAD VILL DU GÖRA?",
            "options": [
                "Generate Resume",
                "Generate Resume Tailored for Job Description", 
                "Generate Tailored Cover Letter for Job Description",
                "Generate and Send Job Application via Email"
            ],
            "logic": "Avgör vilken huvudfunktion som ska köras"
        },
        {
            "step": "2️⃣ ANDRA FRÅGAN - VILKEN MODELL/DESIGN?",
            "options": [
                "Ursprungliga Stilar - Klassiska CV-stilar med befintlig AI-logik",
                "Modern Design 1 - Tvåkolumns layout med vertikal accent-linje", 
                "Modern Design 2 - Kreativ design med färgglad sidopanel"
            ],
            "logic": "Avgör vilken mapp och AI-modell som ska användas"
        },
        {
            "step": "3️⃣ TREDJE FRÅGAN - VILKEN MALL INOM MODELLEN?",
            "options": {
                "Ursprungliga": ["Modern Blue", "Modern Grey", "Default", "Clean Blue", "Cloyola Grey"],
                "Modern Design 1": ["Modern Design 1", "Modern Design 1 - Two Column Layout"],
                "Modern Design 2": ["Modern Design 2"]
            },
            "logic": "Avgör specifik stil/mall inom vald modell"
        },
        {
            "step": "4️⃣ FJÄRDE FRÅGAN - JOBB-URL (om job-tailored)",
            "options": ["Ange URL till jobbet"],
            "logic": "Avgör jobbspecifik anpassning"
        }
    ]
    
    for step_info in flow_steps:
        print(f"\n{step_info['step']}")
        print(f"🎯 Logik: {step_info['logic']}")
        print("📋 Alternativ:")
        
        if isinstance(step_info['options'], dict):
            for category, options in step_info['options'].items():
                print(f"   📁 {category}:")
                for option in options:
                    print(f"      • {option}")
        else:
            for option in step_info['options']:
                print(f"   • {option}")
    
    print(f"\n🎯 ISOLERAD LOGIK PER MODELL:")
    print("   📁 URSPRUNGLIGA → Använder befintlig StyleManager + ResumeGenerator")
    print("   📁 MODERN_DESIGN_1 → Använder ModernDesign1Generator + template.html")
    print("   📁 MODERN_DESIGN_2 → Använder ModernDesign2Generator (framtida)")
    
    print(f"\n⚡ FÖRDELAR MED DENNA STRUKTUR:")
    print("   ✅ Varje design har sin egen optimerade AI-logik")
    print("   ✅ Ingen risk för konflikt mellan olika stilar")
    print("   ✅ Lätt att lägga till nya modeller/designs")
    print("   ✅ Tydlig separation av ansvar")
    print("   ✅ Skalbar arkitektur")


if __name__ == "__main__":
    # Test av ModelManager
    print("🧪 TESTAR MODEL MANAGER")
    print("=" * 50)
    
    manager = ModelManager()
    
    # Visa alla modeller
    stats = ModelAwareResumeSystem("dummy_key").get_model_statistics()
    
    print("📊 TILLGÄNGLIGA MODELLER:")
    for model_id, info in stats.items():
        print(f"\n🎨 {info['name']}")
        print(f"   📝 {info['description']}")
        print(f"   📁 Mapp finns: {'✅' if info['directory_exists'] else '❌'}")
        print(f"   📋 Antal mallar: {info['template_count']}")
        if info['templates']:
            print("   🎯 Mallar:")
            for template in info['templates']:
                print(f"      • {template}")
    
    # Demonstrera flödet
    demonstrate_hierarchical_flow()
