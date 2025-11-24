"""
Uppdatera CV med information från GitHub
Hämtar projekt och teknologier från GitHub och uppdaterar plain_text_resume.yaml
"""

import yaml
from pathlib import Path
from src.github_analyzer import analyze_github_profile
from loguru import logger


def update_resume_with_github(
    resume_path: Path = Path("data_folder/plain_text_resume.yaml"),
    github_token: str = None
):
    """
    Uppdatera CV-filen med GitHub-information

    Args:
        resume_path: Sökväg till plain_text_resume.yaml
        github_token: GitHub Personal Access Token (valfritt)
    """

    # Läs nuvarande CV
    try:
        with open(resume_path, 'r', encoding='utf-8') as f:
            resume_data = yaml.safe_load(f)
    except Exception as e:
        logger.error(f"❌ Kunde inte läsa CV-fil: {e}")
        return

    # Hämta GitHub URL från CV
    github_url = resume_data.get('personal_information', {}).get('github')

    if not github_url:
        logger.error("❌ Ingen GitHub URL hittad i CV:t")
        return

    logger.info(f"🔍 Analyserar GitHub-profil: {github_url}")

    # Analysera GitHub
    analysis = analyze_github_profile(github_url, github_token)

    if analysis['total_repos'] == 0:
        logger.warning("⚠️ Inga repositories hittades")
        return

    logger.info(f"✅ Hittade {analysis['total_repos']} repositories")
    logger.info(f"📊 Språk: {', '.join(list(analysis['languages'].keys())[:5])}")
    logger.info(f"🛠️ Teknologier: {', '.join(analysis['technologies'][:5])}")

    # Uppdatera eller lägg till GitHub-sektion i achievements
    github_achievement = {
        'name': 'Aktiv Open-Source Bidragsgivare',
        'description': analysis['project_summary']
    }

    # Kontrollera om achievements finns
    if 'achievements' not in resume_data:
        resume_data['achievements'] = []

    # Lägg till eller uppdatera GitHub achievement
    github_exists = False
    for achievement in resume_data['achievements']:
        if 'Open-Source' in achievement.get('name', '') or 'GitHub' in achievement.get('name', ''):
            achievement['name'] = github_achievement['name']
            achievement['description'] = github_achievement['description']
            github_exists = True
            break

    if not github_exists:
        resume_data['achievements'].insert(0, github_achievement)

    # Lägg till top-projekt om de inte redan finns
    existing_project_names = [p.get('name', '') for p in resume_data.get('projects', [])]

    for top_project in analysis['top_projects'][:3]:
        if top_project['name'] not in existing_project_names:
            new_project = {
                'name': top_project['name'],
                'description': top_project['description'],
                'link': top_project['url']
            }

            if 'projects' not in resume_data:
                resume_data['projects'] = []

            resume_data['projects'].insert(0, new_project)
            logger.info(f"➕ Lade till projekt: {top_project['name']}")

    # Spara uppdaterad CV
    try:
        with open(resume_path, 'w', encoding='utf-8') as f:
            yaml.dump(resume_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        logger.info(f"✅ CV uppdaterat med GitHub-information!")
        logger.info(f"📝 Fil sparad: {resume_path}")

    except Exception as e:
        logger.error(f"❌ Kunde inte spara CV-fil: {e}")


if __name__ == "__main__":
    import sys

    # Kan köras med: python update_from_github.py [GITHUB_TOKEN]
    github_token = sys.argv[1] if len(sys.argv) > 1 else None

    if github_token:
        logger.info("🔑 Använder GitHub token för högre rate limits")
    else:
        logger.info("ℹ️ Kör utan GitHub token (lägre rate limits)")
        logger.info("💡 Tips: Skapa en GitHub Personal Access Token för bättre prestanda")

    update_resume_with_github(github_token=github_token)

    print("\n" + "="*60)
    print("✅ KLAR! Ditt CV har uppdaterats med GitHub-information.")
    print("="*60)
    print("\n📋 Nästa steg:")
    print("1. Granska data_folder/plain_text_resume.yaml")
    print("2. Generera ett nytt CV med: python main.py")
    print("="*60)
