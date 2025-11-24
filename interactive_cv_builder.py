"""
Interaktiv CV-Builder med AI
Ställer frågor om din erfarenhet och genererar professionella beskrivningar
baserat på VERKLIGA fakta (ingen överdrift!)
"""

import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional
from loguru import logger
import openai


class InteractiveCVBuilder:
    """Interaktiv CV-builder som samlar in verklig data genom frågor"""

    def __init__(self, api_key: str):
        """Initialisera med OpenAI API-nyckel"""
        self.api_key = api_key
        openai.api_key = api_key
        self.collected_data = {}

    def interview_position(self, position: str, company: str, existing_data: Dict) -> Dict:
        """
        Genomför intervju för en specifik position

        Args:
            position: Position/roll
            company: Företag
            existing_data: Befintlig data från YAML

        Returns:
            Dictionary med samlad data
        """
        print("\n" + "="*80)
        print(f"📋 INTERVJU FÖR: {position} at {company}")
        print("="*80)
        print("💡 Svara ärligt och konkret. Om du inte vet exakt, uppskatta realistiskt.")
        print("💡 Tryck Enter för att hoppa över en fråga.")
        print("="*80 + "\n")

        data = {
            'position': position,
            'company': company,
            'period': existing_data.get('employment_period', ''),
            'metrics': {},
            'achievements': [],
            'technologies': [],
            'context': {}
        }

        # === GRUNDLÄGGANDE FRÅGOR ===
        print("📊 GRUNDLÄGGANDE INFORMATION:\n")

        # Antal projekt
        num_projects = input(f"❓ Hur många projekt arbetade du med i denna roll? [uppskatta]: ").strip()
        if num_projects:
            data['metrics']['num_projects'] = num_projects

        # Kunder/användare
        num_clients = input(f"❓ Hur många kunder/klienter arbetade du med? [uppskatta]: ").strip()
        if num_clients:
            data['metrics']['num_clients'] = num_clients

        # Teamstorlek
        team_size = input(f"❓ Hur stor var ditt team? (t.ex. '1' om ensam, '5' om 5 personer): ").strip()
        if team_size:
            data['metrics']['team_size'] = team_size

        # Budget (om relevant)
        if 'projektledare' in position.lower() or 'ägare' in position.lower():
            budget = input(f"❓ Typisk projektbudget eller årsomsättning? (SEK, t.ex. 500000): ").strip()
            if budget:
                data['metrics']['budget'] = budget

        # === RESULTAT & IMPACT ===
        print("\n📈 RESULTAT & PÅVERKAN:\n")

        time_saved = input(f"❓ Hur mycket tid/pengar sparade dina lösningar? (%, t.ex. '30%'): ").strip()
        if time_saved:
            data['metrics']['efficiency_improvement'] = time_saved

        satisfaction = input(f"❓ Kundnöjdhet eller feedback? (%, t.ex. '95%'): ").strip()
        if satisfaction:
            data['metrics']['customer_satisfaction'] = satisfaction

        # === TEKNOLOGIER ===
        print("\n💻 TEKNOLOGIER & VERKTYG:\n")
        print(f"Nuvarande teknologier: {', '.join(existing_data.get('skills_acquired', [])[:5])}")

        additional_tech = input(f"❓ Några andra viktiga teknologier du använde? (kommaseparerat): ").strip()
        if additional_tech:
            data['technologies'] = [t.strip() for t in additional_tech.split(',')]

        # === ACHIEVEMENTS ===
        print("\n🏆 ACHIEVEMENTS:\n")

        achievement = input(f"❓ Vad är du mest stolt över i denna roll? (kort beskrivning): ").strip()
        if achievement:
            data['achievements'].append(achievement)

        # === KONTEXT ===
        print("\n📝 KONTEXT:\n")

        challenges = input(f"❓ Vilka var de största utmaningarna? (kort): ").strip()
        if challenges:
            data['context']['challenges'] = challenges

        solutions = input(f"❓ Hur löste du dem? (kort): ").strip()
        if solutions:
            data['context']['solutions'] = solutions

        print("\n✅ Intervju klar för denna position!")

        return data

    def generate_improved_responsibilities(
        self,
        position: str,
        interview_data: Dict,
        original_responsibilities: List[str],
        language: str = "sv"
    ) -> List[str]:
        """
        Generera förbättrade ansvarsområden baserat på intervjudata

        Args:
            position: Position
            interview_data: Data från intervju
            original_responsibilities: Ursprungliga ansvarsområden
            language: Språk

        Returns:
            Lista med förbättrade beskrivningar
        """

        # Bygg en prompt med VERKLIG data
        metrics_text = "\n".join([f"- {k}: {v}" for k, v in interview_data['metrics'].items()])
        achievements_text = "\n".join([f"- {a}" for a in interview_data['achievements']])
        context_text = json.dumps(interview_data['context'], indent=2)

        prompt = f"""You are a professional CV writer. Create improved work responsibility descriptions based on REAL data provided.

Position: {position}
Company: {interview_data['company']}
Period: {interview_data['period']}

REAL METRICS PROVIDED:
{metrics_text if metrics_text else "- No specific metrics provided"}

ACHIEVEMENTS:
{achievements_text if achievements_text else "- None specified"}

CONTEXT:
{context_text if context_text != '{}' else "- None provided"}

ORIGINAL RESPONSIBILITIES:
{chr(10).join([f"{i+1}. {r}" for i, r in enumerate(original_responsibilities)])}

INSTRUCTIONS:
1. Create {len(original_responsibilities)} improved responsibility descriptions
2. Incorporate the REAL metrics where relevant (use exact numbers provided)
3. Use action verbs (Led, Developed, Implemented, Managed, etc.)
4. Be specific and concrete
5. DO NOT exaggerate or add false information
6. Keep each description to 1-2 lines maximum
7. Output in {"Swedish" if language == "sv" else "English"}

Format as a numbered list:
1. [First improved responsibility with metrics]
2. [Second improved responsibility with metrics]
...

Improved responsibilities:"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional CV writer who creates compelling but honest descriptions based on real data. Never exaggerate."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.4,
                max_tokens=800
            )

            result = response.choices[0].message.content.strip()

            # Parse numbered list
            improved = []
            for line in result.split('\n'):
                line = line.strip()
                # Remove numbering (1., 2., etc.)
                if line and any(line.startswith(f"{i}.") for i in range(1, 20)):
                    cleaned = line.split('.', 1)[1].strip()
                    improved.append(cleaned)

            logger.info(f"✅ Genererade {len(improved)} förbättrade beskrivningar")
            return improved if improved else original_responsibilities

        except Exception as e:
            logger.error(f"❌ Fel vid generering: {e}")
            return original_responsibilities

    def save_interview_data(self, data: Dict, filename: str = "cv_interview_data.json"):
        """Spara intervjudata för framtida användning"""
        filepath = Path("data_folder") / filename

        # Läs befintlig data
        all_data = {}
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                all_data = json.load(f)

        # Lägg till ny data
        key = f"{data['position']}_{data['company']}"
        all_data[key] = data

        # Spara
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)

        logger.info(f"💾 Intervjudata sparad: {filepath}")


def run_interactive_cv_builder(
    resume_path: str = "data_folder/plain_text_resume.yaml",
    api_key: str = None,
    language: str = "sv",
    save_changes: bool = False
):
    """
    Kör interaktiv CV-builder

    Args:
        resume_path: Sökväg till CV-fil
        api_key: OpenAI API-nyckel
        language: Språk
        save_changes: Om True, spara ändringar direkt
    """

    if not api_key:
        # Försök läsa från global_config först
        try:
            from src.libs.resume_and_cover_builder.config import global_config
            if global_config.API_KEY:
                api_key = global_config.API_KEY
                logger.info("✅ Använder API-nyckel från global_config")
        except:
            pass

    if not api_key:
        # Annars läs från secrets.yaml (samma som main.py)
        secrets_path = Path("data_folder/secrets.yaml")
        if secrets_path.exists():
            with open(secrets_path, 'r', encoding='utf-8') as f:
                secrets = yaml.safe_load(f)
                # Använd samma nyckelnamn som main.py: "llm_api_key"
                api_key = secrets.get('llm_api_key') or secrets.get('openai_api_key')
                if api_key:
                    logger.info("✅ Använder API-nyckel från secrets.yaml")

    if not api_key:
        print("❌ Ingen API-nyckel hittad")
        print("💡 Lägg till 'llm_api_key: YOUR_KEY' i data_folder/secrets.yaml")
        return

    # Läs CV
    with open(resume_path, 'r', encoding='utf-8') as f:
        resume_data = yaml.safe_load(f)

    builder = InteractiveCVBuilder(api_key)

    print("\n" + "="*80)
    print("🎤 INTERAKTIV CV-BUILDER MED AI")
    print("="*80)
    print("Detta verktyg ställer frågor om din erfarenhet och skapar")
    print("professionella beskrivningar baserat på VERKLIGA fakta!")
    print("="*80 + "\n")

    # Välj vilka positioner att intervjua
    experience_details = resume_data.get('experience_details', [])

    print("📋 Välj vilka positioner du vill förbättra:\n")
    for i, exp in enumerate(experience_details, 1):
        print(f"{i}. {exp.get('position', 'Position')} - {exp.get('company', 'Company')}")

    print(f"{len(experience_details) + 1}. ALLA positioner")
    print("0. Avbryt")
    print()

    choice = input("Välj (0-{}): ".format(len(experience_details) + 1)).strip()

    if choice == "0":
        print("❌ Avbruten")
        return

    # Bestäm vilka positioner
    if choice == str(len(experience_details) + 1):
        positions_to_process = list(range(len(experience_details)))
    else:
        try:
            positions_to_process = [int(choice) - 1]
        except:
            print("❌ Ogiltigt val")
            return

    # Intervjua varje position
    for idx in positions_to_process:
        exp = experience_details[idx]
        position = exp.get('position', 'Position')
        company = exp.get('company', 'Company')

        # Genomför intervju
        interview_data = builder.interview_position(position, company, exp)

        # Spara intervjudata
        builder.save_interview_data(interview_data)

        # Generera förbättrade beskrivningar
        print("\n🤖 AI genererar förbättrade beskrivningar baserat på din data...\n")

        original_resp = exp.get('key_responsibilities', [])
        original_texts = [
            r.get('responsibility', '') if isinstance(r, dict) else str(r)
            for r in original_resp
        ]

        improved_resp = builder.generate_improved_responsibilities(
            position,
            interview_data,
            original_texts,
            language
        )

        # Visa resultat
        print("\n" + "="*80)
        print("📊 RESULTAT:")
        print("="*80 + "\n")

        for i, (original, improved) in enumerate(zip(original_texts, improved_resp), 1):
            print(f"{i}. ORIGINAL:")
            print(f"   {original}\n")
            print(f"   FÖRBÄTTRAD:")
            print(f"   ✨ {improved}\n")
            print("-" * 80 + "\n")

        # Uppdatera CV-data
        if save_changes:
            exp['key_responsibilities'] = [
                {'responsibility': r} for r in improved_resp
            ]

    if save_changes:
        # Spara uppdaterad CV
        with open(resume_path, 'w', encoding='utf-8') as f:
            yaml.dump(resume_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        print("\n" + "="*80)
        print("✅ CV UPPDATERAT OCH SPARAT!")
        print("="*80)
    else:
        print("\n" + "="*80)
        print("ℹ️  ÄNDRINGAR EJ SPARADE (dry run)")
        print("💡 Kör igen och välj att spara om du gillar resultaten")
        print("="*80)

    print(f"\n💾 Intervjudata sparad i: data_folder/cv_interview_data.json")
    print("📝 Du kan använda denna data för framtida CV-genereringar!")


if __name__ == "__main__":
    import sys

    # Läs argument
    save = "--save" in sys.argv or "-s" in sys.argv
    lang = "en" if "--english" in sys.argv else "sv"

    run_interactive_cv_builder(
        language=lang,
        save_changes=save
    )
