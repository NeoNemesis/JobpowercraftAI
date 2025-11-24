"""
AI-driven Description Improver
Förbättrar CV-beskrivningar automatiskt med AI, men utan att överdriva.
Fokus på klarhet, konkrethet och professionalism.
"""

from typing import Optional, List
from loguru import logger
import openai


class AIDescriptionImprover:
    """Förbättrar CV-beskrivningar med AI på ett balanserat sätt"""

    def __init__(self, api_key: str):
        """
        Initialisera AI Description Improver

        Args:
            api_key: OpenAI API-nyckel
        """
        self.api_key = api_key
        openai.api_key = api_key

    def improve_responsibility(
        self,
        original: str,
        language: str = "sv",
        job_context: Optional[str] = None
    ) -> str:
        """
        Förbättra en ansvarsområdesbeskrivning

        Args:
            original: Original beskrivning
            language: Språk ('sv' eller 'en')
            job_context: Jobbkontext för anpassning (valfritt)

        Returns:
            Förbättrad beskrivning
        """

        language_instruction = "Swedish" if language == "sv" else "English"

        prompt = f"""You are a professional CV writer. Improve the following work responsibility description.

CRITICAL RULES:
1. DO NOT exaggerate or add false information
2. Keep it factual and honest
3. Make it more specific and concrete
4. Use action verbs (Led, Developed, Implemented, Designed, etc.)
5. If possible, suggest where quantifiable metrics could be added (use brackets like [X+] for numbers)
6. Keep it concise (max 2 lines)
7. Output in {language_instruction}

Original description:
"{original}"

{f'Job context: {job_context}' if job_context else ''}

Improved description (one sentence, honest and concrete):"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional CV writer who improves descriptions while staying factual and honest. Never exaggerate."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,  # Låg temperatur för mer konservativa förbättringar
                max_tokens=150
            )

            improved = response.choices[0].message.content.strip()

            # Ta bort citattecken om AI:n lade till dem
            improved = improved.strip('"').strip("'")

            logger.info(f"✅ Förbättrad beskrivning: {improved[:50]}...")
            return improved

        except Exception as e:
            logger.error(f"❌ Fel vid förbättring: {e}")
            return original  # Returnera original om något går fel

    def improve_all_responsibilities(
        self,
        responsibilities: List[str],
        language: str = "sv",
        job_context: Optional[str] = None
    ) -> List[str]:
        """
        Förbättra alla ansvarsområden

        Args:
            responsibilities: Lista med ansvarsområden
            language: Språk
            job_context: Jobbkontext

        Returns:
            Lista med förbättrade ansvarsområden
        """
        improved = []

        for i, resp in enumerate(responsibilities, 1):
            logger.info(f"🔄 Förbättrar beskrivning {i}/{len(responsibilities)}")
            improved_resp = self.improve_responsibility(resp, language, job_context)
            improved.append(improved_resp)

        return improved

    def suggest_metrics(self, description: str, position: str) -> str:
        """
        Föreslå mätbara metriker för en beskrivning

        Args:
            description: Beskrivning
            position: Position/roll

        Returns:
            Beskrivning med föreslagna metriker i brackets
        """

        prompt = f"""Given this work description, suggest realistic quantifiable metrics that could be added.
Use brackets [X+] or [Y%] to indicate where numbers could go.

Position: {position}
Description: {description}

Example input: "Developed web applications"
Example output: "Developed [5+] web applications for [3] clients"

Be realistic and conservative with suggestions. Only suggest metrics that are commonly trackable.

Improved description with metric suggestions:"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=100
            )

            result = response.choices[0].message.content.strip()
            return result.strip('"').strip("'")

        except Exception as e:
            logger.error(f"❌ Fel vid metrikförslag: {e}")
            return description


def improve_cv_descriptions(
    resume_path: str,
    api_key: str,
    language: str = "sv",
    dry_run: bool = True
):
    """
    Förbättra alla beskrivningar i CV:t

    Args:
        resume_path: Sökväg till plain_text_resume.yaml
        api_key: OpenAI API-nyckel
        language: Språk
        dry_run: Om True, visa bara förslag utan att spara
    """
    import yaml
    from pathlib import Path

    # Läs CV
    with open(resume_path, 'r', encoding='utf-8') as f:
        resume_data = yaml.safe_load(f)

    improver = AIDescriptionImprover(api_key)

    print("\n" + "="*80)
    print("🤖 AI DESCRIPTION IMPROVER - BALANSERAD VERSION")
    print("="*80)
    print("ℹ️  Denna AI förbättrar beskrivningar UTAN att överdriva")
    print("✅ Fokus på klarhet, konkrethet och ärlighet")
    print("="*80 + "\n")

    # Förbättra varje position
    for exp in resume_data.get('experience_details', []):
        position = exp.get('position', 'Position')
        company = exp.get('company', 'Company')

        print(f"\n📋 {position} - {company}")
        print("-" * 80)

        responsibilities = exp.get('key_responsibilities', [])

        if not responsibilities:
            continue

        improved_responsibilities = []

        for i, resp_obj in enumerate(responsibilities, 1):
            original = resp_obj.get('responsibility', '') if isinstance(resp_obj, dict) else str(resp_obj)

            print(f"\n{i}. ORIGINAL:")
            print(f"   {original}")

            improved = improver.improve_responsibility(
                original,
                language=language,
                job_context=f"{position} at {company}"
            )

            print(f"\n   FÖRBÄTTRAD:")
            print(f"   {improved}")

            # Visa metrikförslag
            with_metrics = improver.suggest_metrics(improved, position)
            if '[' in with_metrics and ']' in with_metrics:
                print(f"\n   💡 MED METRIKER (fyll i själv):")
                print(f"   {with_metrics}")

            improved_responsibilities.append(improved)

        if not dry_run:
            # Uppdatera
            exp['key_responsibilities'] = [
                {'responsibility': r} for r in improved_responsibilities
            ]

    if not dry_run:
        # Spara
        with open(resume_path, 'w', encoding='utf-8') as f:
            yaml.dump(resume_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        print("\n" + "="*80)
        print("✅ CV UPPDATERAT!")
        print("="*80)
    else:
        print("\n" + "="*80)
        print("ℹ️  DRY RUN - Inga ändringar sparade")
        print("💡 Kör med dry_run=False för att spara ändringar")
        print("="*80)


if __name__ == "__main__":
    import sys
    from pathlib import Path
    import yaml

    # Hämta API-nyckel (samma metod som main.py)
    api_key = None

    # Försök läsa från global_config först
    try:
        from src.libs.resume_and_cover_builder.config import global_config
        if global_config.API_KEY:
            api_key = global_config.API_KEY
    except:
        pass

    # Annars läs från secrets.yaml
    if not api_key:
        secrets_path = Path("data_folder/secrets.yaml")
        if secrets_path.exists():
            with open(secrets_path, 'r', encoding='utf-8') as f:
                secrets = yaml.safe_load(f)
                # Använd samma nyckelnamn som main.py: "llm_api_key"
                api_key = secrets.get('llm_api_key') or secrets.get('openai_api_key')

    if not api_key:
        print("❌ Ingen API-nyckel hittad")
        print("💡 Lägg till 'llm_api_key: YOUR_KEY' i data_folder/secrets.yaml")
        sys.exit(1)

    # Kör förbättring
    improve_cv_descriptions(
        resume_path="data_folder/plain_text_resume.yaml",
        api_key=api_key,
        language="sv",
        dry_run=True  # Ändra till False för att spara
    )
