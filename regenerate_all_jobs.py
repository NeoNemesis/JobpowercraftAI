#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 REGENERERA ALLA JOBB MED NYA REGLER
======================================
✅ 15% anpassning av CV-text (inte 0%, inte 100%)
✅ Inget blandspråk (svenska ELLER engelska, inte blandat)
✅ Ingen jobbeskrivning i personliga brev
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

    # Extrahera information från job_info.txt
    with open(job_info_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extrahera titel, företag och URL
    title = None
    company = None
    url = None

    for line in content.split('\n'):
        if line.startswith('Titel:'):
            title = line.split('Titel:', 1)[1].strip()
        elif line.startswith('Företag:'):
            company = line.split('Företag:', 1)[1].strip()
        elif 'indeed.com' in line or 'linkedin.com' in line or 'arbetsformedlingen.se' in line:
            url = line.strip()
            if 'URL:' in url:
                url = url.split('URL:', 1)[1].strip()
            elif 'Indeed URL:' in url:
                url = url.split('Indeed URL:', 1)[1].strip()

    if not url:
        print(f"⚠️ Ingen URL hittades")
        return False

    print(f"📝 Titel: {title}")
    print(f"🏢 Företag: {company}")
    print(f"🔗 URL: {url}")

    try:
        # Hämta jobbinformation
        print(f"\n📥 Hämtar jobbinformation...")
        modern_facade.link_to_job(url)

        # Generera CV med 15% anpassning
        print(f"\n📝 Genererar CV (15% anpassning, inget blandspråk)...")
        cv_base64, _ = modern_facade.create_resume_pdf_job_tailored(ask_questions=False)

        safe_company = ''.join(c if c.isalnum() or c in (' ', '_') else '_' for c in company)[:30]
        safe_title = ''.join(c if c.isalnum() or c in (' ', '_') else '_' for c in title)[:30]
        cv_path = job_folder / f"CV_{safe_company}_{safe_title}_Modern_Design_1.pdf"

        with open(cv_path, 'wb') as f:
            f.write(base64.b64decode(cv_base64))

        cv_size_kb = cv_path.stat().st_size / 1024
        print(f"   ✅ CV sparat: {cv_path.name} ({cv_size_kb:.1f} KB)")

        # Generera personligt brev (CLEAN, ingen jobbeskrivning)
        print(f"\n💌 Genererar personligt brev (CLEAN, ingen jobbeskrivning)...")
        cover_base64, _ = modern_facade.create_cover_letter()

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
    print("🔄 REGENERERA ALLA JOBB MED NYA REGLER")
    print("="*80)
    print("✅ 15% anpassning av CV (inte 0%, inte 100%)")
    print("✅ Inget blandspråk (svenska ELLER engelska)")
    print("✅ Ingen jobbeskrivning i personliga brev")
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

        # Hitta alla jobbmappar
        job_folders = sorted([f for f in output_dir.iterdir() if f.is_dir() and f.name.startswith('Job_')])
        print(f"\n📂 Hittade {len(job_folders)} jobbmappar")

        successful = 0
        for i, job_folder in enumerate(job_folders, 1):
            if regenerate_job(job_folder, driver, modern_facade, i):
                successful += 1

        print("\n" + "="*80)
        print("✅ KLART!")
        print("="*80)
        print(f"Regenererade: {successful}/{len(job_folders)} jobb")
        print(f"📁 Dokument: {output_dir.absolute()}")
        print("="*80)
        print("\n💡 Granska och kontrollera:")
        print("   ✅ Inget blandspråk i CV eller brev")
        print("   ✅ Personliga brev utan jobbeskrivning")
        print("   ✅ CV text max 15% ändrad från original")

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
