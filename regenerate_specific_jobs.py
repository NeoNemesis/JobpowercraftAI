#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 REGENERERA SPECIFIKA JOBB
============================
Regenerera Job 2, 3, 4, 5 med ÄRLIG CV-anpassning (ingen överdrift!)
"""

import os
import sys
import base64
from pathlib import Path
from dotenv import load_dotenv

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

# Lägg till src till path
sys.path.insert(0, str(Path(__file__).parent))

# Import AIHawk modules
from src.resume_schemas.resume import Resume
from src.libs.resume_and_cover_builder.moderndesign1.modern_facade import ModernDesign1Facade
from src.libs.resume_and_cover_builder.moderndesign1.modern_style_manager import ModernDesign1StyleManager
from src.libs.resume_and_cover_builder.moderndesign1.modern_resume_generator import ModernDesign1ResumeGenerator

# Browser pool support
try:
    from src.utils.browser_pool import get_browser, cleanup_browser
    BROWSER_POOL_AVAILABLE = True
except ImportError:
    from src.utils.chrome_utils import init_browser
    BROWSER_POOL_AVAILABLE = False

def regenerate_job(job_folder: Path, driver, modern_facade, job_number: int):
    """Regenerera ett specifikt jobb"""

    print("\n" + "="*80)
    print(f"🔄 REGENERERAR {job_folder.name}")
    print("="*80)

    # Läs job_info.txt
    job_info_file = job_folder / "job_info.txt"
    if not job_info_file.exists():
        print(f"⚠️ Ingen job_info.txt hittades")
        return False

    # Extrahera URL
    with open(job_info_file, 'r', encoding='utf-8') as f:
        content = f.read()

    url = None
    for line in content.split('\n'):
        if 'indeed.com' in line or 'linkedin.com' in line or 'arbetsformedlingen.se' in line:
            url = line.strip()
            # Ta bort prefix
            if 'URL:' in url:
                url = url.split('URL:', 1)[1].strip()
            elif 'Indeed URL:' in url:
                url = url.split('Indeed URL:', 1)[1].strip()
            url = url.strip()
            break

    if not url:
        print(f"⚠️ Ingen URL hittades i job_info.txt")
        return False

    print(f"🔗 URL: {url}")

    try:
        # Hämta jobbinformation
        print(f"\n📥 Hämtar jobbinformation...")
        modern_facade.link_to_job(url)

        print(f"   🏢 Företag: {modern_facade.job.company}")
        print(f"   💼 Roll: {modern_facade.job.role}")
        print(f"   📍 Plats: {modern_facade.job.location}")

        # Generera CV med ÄRLIG anpassning
        print(f"\n📝 Genererar ÄRLIGT CV (ingen överdrift!)...")
        cv_base64, _ = modern_facade.create_resume_pdf_job_tailored(ask_questions=False)

        # Hitta befintlig CV-fil
        existing_cv = list(job_folder.glob("CV_*.pdf"))
        if existing_cv:
            cv_path = existing_cv[0]
            print(f"   ♻️  Skriver över: {cv_path.name}")
        else:
            safe_company = ''.join(c if c.isalnum() or c in (' ', '_') else '_' for c in modern_facade.job.company)[:30]
            safe_title = ''.join(c if c.isalnum() or c in (' ', '_') else '_' for c in modern_facade.job.role)[:30]
            cv_path = job_folder / f"CV_{safe_company}_{safe_title}_Modern_Design_1.pdf"

        with open(cv_path, 'wb') as f:
            f.write(base64.b64decode(cv_base64))

        cv_size_kb = cv_path.stat().st_size / 1024
        print(f"   ✅ CV sparat: {cv_path.name} ({cv_size_kb:.1f} KB)")

        # Generera personligt brev (CLEAN version)
        print(f"\n💌 Genererar CLEAN personligt brev...")
        cover_base64, _ = modern_facade.create_cover_letter()

        # Hitta befintlig fil
        existing_cover = list(job_folder.glob("Personligt_Brev_*.pdf"))
        if existing_cover:
            cover_path = existing_cover[0]
            print(f"   ♻️  Skriver över: {cover_path.name}")
        else:
            safe_company = ''.join(c if c.isalnum() or c in (' ', '_') else '_' for c in modern_facade.job.company)[:30]
            safe_title = ''.join(c if c.isalnum() or c in (' ', '_') else '_' for c in modern_facade.job.role)[:30]
            cover_path = job_folder / f"Personligt_Brev_{safe_company}_{safe_title}_Modern_Design_1.pdf"

        with open(cover_path, 'wb') as f:
            f.write(base64.b64decode(cover_base64))

        cover_size_kb = cover_path.stat().st_size / 1024
        print(f"   ✅ Personligt brev sparat: {cover_path.name} ({cover_size_kb:.1f} KB)")

        print(f"\n✅ Jobb regenererat framgångsrikt!")
        return True

    except Exception as e:
        print(f"\n❌ Fel vid regenerering: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main entry point"""
    print("\n" + "="*80)
    print("🔄 REGENERERA JOB 2, 3, 4, 5 MED ÄRLIG ANPASSNING")
    print("="*80)
    print("✅ Ingen överdrift av IT-erfarenhet")
    print("✅ Behåller essensen av varje jobb")
    print("✅ Clean personliga brev")
    print("="*80)

    # Ladda CV
    print("\n📄 Laddar CV-data...")
    resume_yaml = Path('data_folder/plain_text_resume.yaml')
    with open(resume_yaml, 'r', encoding='utf-8') as f:
        yaml_content = f.read()
    resume_object = Resume(yaml_content)
    print(f"✅ CV laddat: {resume_object.personal_information.name}")

    # Starta browser
    print("\n🌐 Startar browser...")
    if BROWSER_POOL_AVAILABLE:
        driver = get_browser()
        print("✅ Browser pool aktiverad")
    else:
        driver = init_browser()
        print("✅ Browser startad")

    try:
        # Initialisera Modern Design 1
        print("\n🎨 Initialiserar Modern Design 1...")
        api_key = os.getenv('OPENAI_API_KEY')
        style_manager = ModernDesign1StyleManager()
        resume_generator = ModernDesign1ResumeGenerator()
        output_dir = Path('data_folder/output/job_master')

        modern_facade = ModernDesign1Facade(
            api_key=api_key,
            style_manager=style_manager,
            resume_generator=resume_generator,
            resume_object=resume_object,
            output_path=output_dir
        )
        modern_facade.set_driver(driver)
        print("✅ Modern Design 1 redo")

        # Jobb att regenerera
        jobs_to_regenerate = [
            'Job_002_Läkemedelsverket_Systemutvecklare frontend C',
            'Job_003_Läkemedelsverket_Systemutvecklare backend CN',
            'Job_004_Försvarsmakten_Junior systemutvecklare till F',
            'Job_005_Sigma Group_Software Developer Net C'
        ]

        successful = 0
        for i, job_name in enumerate(jobs_to_regenerate, 2):
            job_folder = output_dir / job_name
            if not job_folder.exists():
                print(f"\n⚠️ Jobbmapp finns inte: {job_name}")
                continue

            if regenerate_job(job_folder, driver, modern_facade, i):
                successful += 1

        print("\n" + "="*80)
        print("✅ KLART!")
        print("="*80)
        print(f"Regenererade: {successful}/{len(jobs_to_regenerate)} jobb")
        print(f"📁 Dokument: {output_dir.absolute()}")
        print("="*80)
        print("\n💡 Granska CV:na och kontrollera att:")
        print("   ✅ Inga överdrifter av IT-erfarenhet")
        print("   ✅ Vårdjobben beskrivs som vårdjobb")
        print("   ✅ Byggjobbet beskrivs som byggjobb")
        print("   ✅ Egna IT-projekt beskrivs korrekt")

    except Exception as e:
        print(f"\n❌ Fel: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        print("\n🧹 Stänger browser...")
        if BROWSER_POOL_AVAILABLE:
            cleanup_browser()
        else:
            driver.quit()
        print("✅ Klart!")

if __name__ == "__main__":
    main()
