"""
Förbättra CV-beskrivningar med AI
Kör detta script för att få AI:ns förslag på förbättrade beskrivningar
"""

import sys
import yaml
from pathlib import Path
from src.ai_description_improver import improve_cv_descriptions
from loguru import logger


def main():
    """Huvudfunktion"""

    print("\n" + "="*80)
    print("🤖 AI CV DESCRIPTION IMPROVER")
    print("="*80)
    print()

    # Hämta API-nyckel (samma metod som main.py)
    api_key = None

    # Försök läsa från global_config först
    try:
        from src.libs.resume_and_cover_builder.config import global_config
        if global_config.API_KEY:
            api_key = global_config.API_KEY
            print("✅ Använder API-nyckel från global_config")
    except:
        pass

    # Annars läs från secrets.yaml
    if not api_key:
        secrets_path = Path("data_folder/secrets.yaml")
        if not secrets_path.exists():
            print("❌ Kunde inte hitta data_folder/secrets.yaml")
            print("💡 Skapa filen med din API-nyckel:")
            print("   llm_api_key: 'sk-...'")
            return

        with open(secrets_path, 'r', encoding='utf-8') as f:
            secrets = yaml.safe_load(f)
            # Använd samma nyckelnamn som main.py: "llm_api_key"
            api_key = secrets.get('llm_api_key') or secrets.get('openai_api_key')

    if not api_key:
        print("❌ Ingen API-nyckel hittad i secrets.yaml")
        print("💡 Lägg till: llm_api_key: 'sk-...'")
        return

    # Välj språk
    print("📝 Välj språk för förbättringar:")
    print("1. Svenska (sv)")
    print("2. English (en)")
    print()

    choice = input("Välj (1-2) [1]: ").strip() or "1"
    language = "sv" if choice == "1" else "en"

    # Välj läge
    print("\n🔧 Välj läge:")
    print("1. DRY RUN - Visa bara förslag (rekommenderas först)")
    print("2. SPARA - Uppdatera CV:t direkt")
    print()

    mode_choice = input("Välj (1-2) [1]: ").strip() or "1"
    dry_run = mode_choice == "1"

    if not dry_run:
        print("\n⚠️  VARNING: Detta kommer att ÄNDRA din plain_text_resume.yaml!")
        confirm = input("Är du säker? (ja/nej) [nej]: ").strip().lower()
        if confirm not in ['ja', 'yes', 'j', 'y']:
            print("❌ Avbruten")
            return

    print("\n🚀 Startar AI-förbättring...")
    print("="*80 + "\n")

    # Kör förbättring
    improve_cv_descriptions(
        resume_path="data_folder/plain_text_resume.yaml",
        api_key=api_key,
        language=language,
        dry_run=dry_run
    )

    if dry_run:
        print("\n💡 TIPS: Granska förslagen ovan")
        print("📝 Om du gillar dem, kör scriptet igen och välj 'SPARA'")
    else:
        print("\n✅ Ditt CV har uppdaterats!")
        print("📋 Granska: data_folder/plain_text_resume.yaml")
        print("🚀 Generera nytt CV med: python main.py")


if __name__ == "__main__":
    main()
