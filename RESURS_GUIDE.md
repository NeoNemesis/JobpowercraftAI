# 📚 KOMPLETT RESURSGUIDE - Var applikationen hämtar data

## 🎯 ÖVERSIKT

Applikationen hämtar resurser från **3 huvudplatser**:

```
1. data_folder/plain_text_resume.yaml  ← 🎯 ALLT CV-innehåll
2. assets/                             ← 🖼️ Bilder och resurser
3. src/libs/resume_and_cover_builder/  ← 🎨 Design-templates
```

---

## 📁 1. HUVUDDATAFIL: `data_folder/plain_text_resume.yaml`

### **Detta är din MASTER-data som används för:**
- ✅ Alla CV-generationer
- ✅ Alla personliga brev
- ✅ AI-anpassning till jobb
- ✅ Automatisk översättning svenska/engelska

### **Struktur:**

```yaml
personal_information:
  name: "Victor"
  surname: "Vilches"
  email: "victorvilches@protonmail.com"
  phone: "707978547"
  address: "Kvarnängsgatan 24"
  city: "Uppsala"
  zip_code: "75420"
  country: "Sverige"
  website: "vilchesab.se"
  github: "https://github.com/NeoNemesis"
  linkedin: "https://linkedin.com/in/victor-vilches..."

education_details:
  - education_level: "Dataingenjör - 2 år inom IT"
    institution: "Gävle Universitet, Uppsala"
    field_of_study: "IT och Dataingenjörskap"
    year_of_completion: "2024"
    start_date: "2022"

experience_details:
  - position: "Dataingenjör & Systemutvecklare"
    company: "Egen verksamhet"
    employment_period: "2022 - Present"
    location: "Uppsala, Sverige"
    industry: "Technology & Development"
    key_responsibilities:
      - responsibility: "Din beskrivning här..."
    skills_acquired:
      - "JavaScript"
      - "Python"
      - "SQL"

certifications:
  - name: "Webbutveckling I & II"
    description: "Extra kurser"
  - name: "Databas teknik i SQL"

languages:
  - language: "Svenska"
    proficiency: "Modersmål"
  - language: "Engelska"
    proficiency: "Flytande"

interests:
  - "Systemintegration"
  - "Webbutveckling"
  - "AI-utveckling"

projects:
  - name: "Projekt namn"
    description: "Beskrivning"
    link: "https://github.com/..."
```

---

## 🖼️ 2. BILDER: `assets/`

### **Nuvarande bilder:**
```
assets/
├── victorvilches.png      ← Används av ALLA designs
├── Vilchesab.png          ← Backup
└── resume_schema.yaml     ← Validering
```

### **HUR LÄGGA TILL FLER BILDER:**

**Steg 1: Lägg till bild i assets:**
```bash
# Kopiera din nya bild:
cp /path/to/min_nya_bild.png assets/victor_professional.png
```

**Steg 2: Uppdatera prioritetslistan:**

Redigera `src/libs/resume_and_cover_builder/moderndesign1/improved_generator.py`:

```python
def _get_profile_image_base64(self) -> str:
    possible_paths = [
        "assets/victor_professional.png",  # 🆕 Lägg till först för högsta prioritet!
        "assets/victorvilches.png",
        "assets/Vilchesab.png",
        "data_folder/profil_no_bg.png",
        "data_folder/profil.jpg",
        "data_folder/profile.png"
    ]
```

**Gör samma i `moderndesign2/improved_generator.py`!**

---

## ✨ 3. FÖRBÄTTRA INNEHÅLLET - BEST PRACTICES

### **A) RESPONSIBILITIES - Använd STAR-metoden:**

❌ **DÅLIGT EXEMPEL:**
```yaml
- responsibility: "Jobbade med webbutveckling"
```

✅ **BRA EXEMPEL:**
```yaml
- responsibility: "Utvecklade och lanserade e-handelsplattform med React och Node.js som genererade 50,000 kr i försäljning första månaden och ökade kundnöjdhet med 35%"
```

**STAR-format:**
- **S**ituation: E-handelsplattform
- **T**ask: Utveckla och lansera
- **A**ction: med React och Node.js
- **R**esult: 50,000 kr försäljning, +35% nöjdhet

### **B) ANVÄND KONKRETA SIFFROR:**

```yaml
✅ "Ökade performance med 40%"
✅ "Ledde team om 5 utvecklare"
✅ "Minskade deployment-tid från 2h till 10min"
✅ "Hanterade 1000+ användare dagligen"
✅ "Sparade företaget 200,000 kr årligen"
✅ "Implementerade på 3 månader (2 månader före deadline)"
```

### **C) LÄGG TILL TEKNOLOGIER I BESKRIVNINGAR:**

❌ **FÖRE:**
```yaml
- responsibility: "Byggde webbapplikationer"
```

✅ **EFTER:**
```yaml
- responsibility: "Byggde moderna webbapplikationer med React 18, TypeScript, Next.js 14, och Tailwind CSS, deployade på Vercel med automatisk CI/CD via GitHub Actions"
```

---

## 🚀 4. LÄGGA TILL NYA SEKTIONER I CV

### **Steg 1: Lägg till data i YAML**

```yaml
# I plain_text_resume.yaml, lägg till:

awards:  # 🆕 NY SEKTION!
  - name: "Årets Innovatör 2024"
    issuer: "Tech Summit Stockholm"
    description: "För AI-driven jobbsökningssystem"
    
publications:  # 🆕 NY SEKTION!
  - title: "Building AI-Powered Job Application Systems"
    publisher: "Dev.to"
    date: "2024"
    link: "https://dev.to/..."

volunteer_work:  # 🆕 NY SEKTION!
  - position: "Mentor"
    organization: "Code for Sweden"
    period: "2023 - Present"
    description: "Mentorskap för nya utvecklare"
```

### **Steg 2: Uppdatera resume schema**

Redigera `src/resume_schemas/resume.py`:

```python
class Resume(BaseModel):
    personal_information: Optional[PersonalInformation]
    education_details: Optional[List[EducationDetails]] = None
    experience_details: Optional[List[ExperienceDetails]] = None
    projects: Optional[List[Project]] = None
    achievements: Optional[List[Achievement]] = None
    certifications: Optional[List[Certifications]] = None
    languages: Optional[List[Language]] = None
    interests: Optional[List[str]] = None
    awards: Optional[List[Award]] = None  # 🆕 LÄGG TILL!
```

### **Steg 3: Lägg till i template**

```html
<div class="section">
    <h3 class="section-title">UTMÄRKELSER</h3>
    $awards_content
</div>
```

---

## 🎨 5. SKAPA VARIATIONER AV DIN RESUME

### **Idé: Olika versioner för olika jobb-typer**

```
data_folder/
├── resume_tech_focus.yaml      ← Betona programmering & system
├── resume_manager_focus.yaml   ← Betona projektledning
├── resume_fullstack_focus.yaml ← Betona web-utveckling
└── resume_minimal.yaml         ← Minimalistisk version
```

**Exempel på tech-fokuserad:**

```yaml
experience_details:
  - position: "Senior Full-Stack Developer"  # 🔄 Ändrad titel!
    company: "Egen verksamhet"
    key_responsibilities:
      # Fokusera på TEKNISKA achievements:
      - responsibility: "Arkitekterade och utvecklade microservices-baserad backend med Node.js, Express, och PostgreSQL som hanterar 10,000+ requests/dag"
      - responsibility: "Implementerade real-time features med WebSockets och Redis pub/sub för 500+ samtidiga användare"
```

**Exempel på manager-fokuserad:**

```yaml
experience_details:
  - position: "Technical Project Lead & Owner"  # 🔄 Ändrad titel!
    company: "Vilches Entreprenad AB"
    key_responsibilities:
      # Fokusera på LEDNING:
      - responsibility: "Ledde och koordinerade team om 5-8 personer genom hela projekt-livscykeln från planering till leverans"
      - responsibility: "Hanterade projektbudgetar på upp till 500,000 kr med 95% on-time, on-budget delivery rate"
```

---

## 🔧 6. KÖR ANALYS-SKRIPTET

```powershell
python improve_resume_data.py
```

**Detta visar:**
- ✅ Vad du har nu
- ⚠️ Vad som saknas
- 💡 Förbättringsförslag
- 📊 Kvalitetsanalys

---

## 📋 SNABB CHECKLISTA FÖR BÄTTRE CV:

- [ ] Varje experience har 4-6 key_responsibilities
- [ ] Minst 50% av responsibilities innehåller siffror/resultat
- [ ] Alla responsibilities nämner specifika teknologier
- [ ] Minst 3 projekt tillagda
- [ ] Minst 2 achievements tillagda
- [ ] 15+ skills totalt
- [ ] 3+ intressen
- [ ] Profilbild finns och är professionell

---

## 🎯 NÄSTA STEG:

1. **Kör analys:**
   ```bash
   python improve_resume_data.py
   ```

2. **Redigera din YAML:**
   ```bash
   notepad data_folder/plain_text_resume.yaml
   ```

3. **Testa med nytt innehåll:**
   ```bash
   python main.py
   ```

**Vill du att jag hjälper dig förbättra specifika sektioner?** 🚀


