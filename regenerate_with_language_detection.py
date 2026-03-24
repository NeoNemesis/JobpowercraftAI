"""
Regenerera alla befintliga jobb med förbättrad språkdetektering
✅ Läser FULL jobbeskrivning från Indeed
✅ Detekterar korrekt språk (Svenska/Engelska)
✅ Genererar CV och personligt brev på rätt språk
"""

import os
import sys
import base64
import json
from pathlib import Path
from dotenv import load_dotenv

# Fix encoding for Windows terminal
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Ladda environment variables
load_dotenv()

# Lägg till src till Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

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

print("="*80)
print("🔄 REGENERERAR ALLA JOBB MED FÖRBÄTTRAD SPRÅKDETEKTERING")
print("="*80)

# Initialisera browser
print("\n🌐 Initialiserar browser...")
if BROWSER_POOL_AVAILABLE:
    driver = get_browser()
    print("✅ Browser pool aktiverad (13x snabbare!)")
else:
    driver = init_browser()
    print("✅ Standard browser initialiserad")

# Ladda CV data
print("\n📄 Laddar CV-data...")
resume_yaml = Path('data_folder/plain_text_resume.yaml')
with open(resume_yaml, 'r', encoding='utf-8') as f:
    yaml_content = f.read()
resume_object = Resume(yaml_content)
print(f"✅ CV laddat: {resume_object.personal_information.name}")

# Initialisera Modern Design 1 system
print("\n🎨 Initialiserar Modern Design 1 system...")
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
print(f"\n📂 Hittade {len(job_folders)} jobb att regenerera")

# Regenerera varje jobb
for i, job_folder in enumerate(job_folders, 1):
    print("\n" + "="*80)
    print(f"🔄 Regenererar jobb {i}/{len(job_folders)}: {job_folder.name}")
    print("="*80)

    # Läs job_info.txt för att få URL
    job_info_file = job_folder / "job_info.txt"
    if not job_info_file.exists():
        print(f"⚠️ Ingen job_info.txt hittades, hoppar över")
        continue

    # Extrahera URL från job_info.txt
    with open(job_info_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # URL finns oftast på första raden eller efter "URL:"
        url = None
        for line in content.split('\n'):
            if 'indeed.com' in line:
                url = line.strip()
                # Ta bort alla möjliga prefix
                if 'URL:' in url:
                    url = url.split('URL:', 1)[1].strip()
                elif 'Indeed URL:' in url:
                    url = url.split('Indeed URL:', 1)[1].strip()
                # Ta bort eventuella mellanslag i början/slutet
                url = url.strip()
                break

        if not url:
            print(f"⚠️ Ingen Indeed URL hittades i job_info.txt, hoppar över")
            continue

    print(f"\n🔗 URL: {url}")

    try:
        # Hämta jobbinformation med FÖRBÄTTRAD språkdetektering
        print(f"\n📥 Hämtar jobbinformation med FULL text för språkdetektering...")
        modern_facade.link_to_job(url)

        # Visa vad som extraherades
        print(f"   🏢 Företag: {modern_facade.job.company}")
        print(f"   💼 Roll: {modern_facade.job.role}")
        print(f"   📍 Plats: {modern_facade.job.location}")
        if hasattr(modern_facade, 'full_job_text'):
            print(f"   📄 Full text: {len(modern_facade.full_job_text)} tecken")
        print(f"   📝 Beskrivning: {len(modern_facade.job.description)} tecken")

        # Generera CV
        print("\n📝 Genererar CV med korrekt språkdetektering...")
        cv_base64, _ = modern_facade.create_resume_pdf_job_tailored(ask_questions=False)

        # Hitta existerande CV-fil
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

        # Generera personligt brev
        print("\n💌 Genererar personligt brev med korrekt språkdetektering...")
        cover_base64, _ = modern_facade.create_cover_letter()

        # Hitta existerande brev
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

    except Exception as e:
        print(f"\n❌ Fel vid regenerering: {e}")
        import traceback
        traceback.print_exc()
        continue

print("\n" + "="*80)
print("✅ ALLA JOBB REGENERERADE MED FÖRBÄTTRAD SPRÅKDETEKTERING!")
print("="*80)

# Cleanup browser
if BROWSER_POOL_AVAILABLE:
    cleanup_browser(driver)
    print("\n✅ Browser återlämnad till pool")
else:
    driver.quit()
    print("\n✅ Browser stängd")

print("\n🎉 Klar! Alla dokument har nu korrekt språk baserat på jobbeskrivningen.")
