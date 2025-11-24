#!/usr/bin/env python3
"""
Hjälpscript för att förbättra din resume data
Ger förslag på hur du kan göra dina beskrivningar mer impaktfulla
"""

import yaml
from pathlib import Path

def analyze_resume_data(yaml_path: str = "data_folder/plain_text_resume.yaml"):
    """Analyserar och ger förbättringsförslag"""
    
    print("🔍 ANALYSERAR DIN RESUME DATA...")
    print("=" * 60)
    
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    print("\n📊 NUVARANDE INNEHÅLL:")
    print("-" * 60)
    
    # Personal Information
    if 'personal_information' in data:
        print(f"✅ Personlig information: {len(data['personal_information'])} fält")
    
    # Education
    if 'education_details' in data:
        print(f"✅ Utbildning: {len(data['education_details'])} poster")
        for edu in data['education_details']:
            print(f"   - {edu.get('education_level', 'N/A')}")
    
    # Experience
    if 'experience_details' in data:
        print(f"✅ Arbetslivserfarenhet: {len(data['experience_details'])} poster")
        for exp in data['experience_details']:
            print(f"   - {exp.get('position', 'N/A')} @ {exp.get('company', 'N/A')}")
            resp_count = len(exp.get('key_responsibilities', []))
            print(f"     Ansvar: {resp_count} punkter")
            
            # Analysera kvalitet
            if resp_count < 3:
                print(f"     ⚠️ FÖRBÄTTRINGSFÖRSLAG: Lägg till fler responsibilities (rekommenderat: 4-6)")
            
            for resp in exp.get('key_responsibilities', []):
                text = resp.get('responsibility', '')
                if len(text) < 50:
                    print(f"     ⚠️ För kort beskrivning: '{text[:40]}...'")
                    print(f"        TIPS: Lägg till konkreta siffror och resultat!")
    
    # Projects
    if 'projects' in data:
        print(f"✅ Projekt: {len(data['projects'])} poster")
    else:
        print(f"⚠️ Projekt: INGA - Lägg till dina projekt!")
        print(f"   FÖRSLAG: Lägg till GitHub-projekt, webbsidor, eller andra tekniska projekt")
    
    # Achievements
    if 'achievements' in data:
        print(f"✅ Prestationer: {len(data['achievements'])} poster")
    else:
        print(f"💡 Prestationer: INGA - Överväg att lägga till!")
        print(f"   EXEMPEL: 'Ökade efficiency med 30%', 'Ledde team om 5 personer'")
    
    # Certifications
    if 'certifications' in data:
        print(f"✅ Certifieringar: {len(data['certifications'])} poster")
        for cert in data['certifications']:
            print(f"   - {cert.get('name', 'N/A')}")
    
    # Languages
    if 'languages' in data:
        print(f"✅ Språk: {len(data['languages'])} poster")
        for lang in data['languages']:
            print(f"   - {lang.get('language', 'N/A')}: {lang.get('proficiency', 'N/A')}")
    
    # Interests
    if 'interests' in data:
        print(f"✅ Intressen: {len(data['interests'])} poster")
        if len(data['interests']) < 3:
            print(f"   💡 TIPS: Lägg till fler intressen (visar personlighet!)")
    
    print("\n" + "=" * 60)
    print("🎯 FÖRBÄTTRINGSFÖRSLAG:")
    print("-" * 60)
    
    suggestions = []
    
    # Kontrollera om responsibilities har siffror
    has_numbers = False
    if 'experience_details' in data:
        for exp in data['experience_details']:
            for resp in exp.get('key_responsibilities', []):
                text = resp.get('responsibility', '')
                if any(char.isdigit() for char in text):
                    has_numbers = True
                    break
    
    if not has_numbers:
        suggestions.append("1. ✨ LÄGG TILL KONKRETA SIFFROR i dina responsibilities")
        suggestions.append("   Exempel: '40% snabbare', '5+ projekt', '1000+ användare'")
    
    if 'projects' not in data or len(data.get('projects', [])) == 0:
        suggestions.append("2. 🚀 LÄGG TILL PROJEKT från GitHub eller portfolio")
    
    if 'achievements' not in data or len(data.get('achievements', [])) == 0:
        suggestions.append("3. 🏆 LÄGG TILL ACHIEVEMENTS/PRESTATIONER")
    
    # Kontrollera skills variation
    if 'experience_details' in data:
        all_skills = set()
        for exp in data['experience_details']:
            skills = exp.get('skills_acquired', [])
            all_skills.update(skills)
        
        if len(all_skills) < 10:
            suggestions.append(f"4. 📚 LÄGG TILL FLER SKILLS (nuvarande: {len(all_skills)}, rekommenderat: 15-20)")
    
    for suggestion in suggestions:
        print(suggestion)
    
    print("\n" + "=" * 60)
    print("💡 TIPS FÖR BÄTTRE CV:")
    print("-" * 60)
    print("""
1. Använd AKTIVA VERB: "Utvecklade", "Implementerade", "Ledde", "Ökade"
2. Inkludera KONKRETA RESULTAT: "Ökade efficiency med 30%"
3. Lägg till TEKNOLOGIER: "med React, Node.js och PostgreSQL"
4. Visa IMPACT: "som resulterade i 50% färre buggar"
5. Var SPECIFIK: Inte bara "Jobbade med projekt" utan "Ledde 3 fullstack-projekt med 5-person team"
    """)
    
    return data

if __name__ == "__main__":
    data = analyze_resume_data()
    
    print("\n🎯 Vill du ha en FÖRBÄTTRAD VERSION av din resume?")
    print("Kör: python improve_resume_data.py --upgrade")


