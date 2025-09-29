# JobCraftAI - Komplett Användningsguide på Svenska

*Skapad av Victor Vilches - Dataingenjör & Entreprenör*

## 🎯 Översikt

JobCraftAI är ett kraftfullt AI-drivet system som automatiserar din jobbansökningsprocess genom att:
- **Anpassa ditt CV** för specifika jobb med AI
- **Generera personliga brev** som matchar jobbkrav
- **Automatisera email-utskick** med formaterade dokument
- **Söka jobb** på flera plattformar samtidigt

## 🚀 Snabbstart

### 1. Installation
```bash
# Klona projektet
git clone <repository-url>
cd JobCraftAI

# Installera beroenden
pip install -r requirements.txt
```

### 2. Grundkonfiguration

**Kopiera exempel-filerna:**
```bash
cp -r data_folder_example/ data_folder/
```

**Redigera dina filer:**

#### `data_folder/plain_text_resume.yaml`
```yaml
personal_information:
  name: "Ditt Förnamn"
  surname: "Ditt Efternamn"
  email: "din@email.com"
  phone: "+46701234567"
  city: "Stockholm"
  country: "Sverige"
  github: "https://github.com/dinprofil"
  linkedin: "https://www.linkedin.com/in/dinprofil/"

experience_details:
  - position: "Senior Utvecklare"
    company: "TechAB"
    employment_period: "2020 - Present"
    location: "Stockholm, Sverige"
    industry: "Technology"
    key_responsibilities:
      - responsibility: "Utvecklade webbapplikationer med React och Node.js"
      - responsibility: "Ledde team på 5 utvecklare"
    skills_acquired:
      - "React"
      - "Node.js"
      - "Python"
      - "AI/ML"

education_details:
  - education_level: "Civilingenjör"
    institution: "KTH"
    field_of_study: "Datateknik"
    year_of_completion: "2019"
```

#### `data_folder/work_preferences.yaml`
```yaml
remote: true
hybrid: true
onsite: false

positions:
  - "Software Developer"
  - "Full Stack Developer"
  - "AI Engineer"

locations:
  - "Stockholm"
  - "Göteborg"
  - "Remote"

experience_level:
  entry: false
  associate: true
  mid_senior_level: true
  director: false
```

#### `data_folder/secrets.yaml`
```yaml
llm_api_key: 'sk-din-openai-api-nyckel-här'
```

## 📧 Email-konfiguration

### Skapa `data_folder/email_config.yaml`:
```yaml
smtp_server: 'smtp.gmail.com'  # För Gmail
smtp_port: 587
email: 'din@gmail.com'
password: 'ditt-app-lösenord'  # Använd app-specifikt lösenord!
sender_name: 'Ditt Fullständiga Namn'
```

### Gmail Setup:
1. Gå till [Google Account Security](https://myaccount.google.com/security)
2. Aktivera 2-faktor-autentisering
3. Generera ett "App Password" för JobCraftAI
4. Använd detta lösenord i `email_config.yaml`

## 🛠️ Användning

### Grundläggande Användning
```bash
python main.py
```

Systemet kommer fråga dig:
1. **Stil för CV** - Välj från tillgängliga mallar
2. **Jobbeskrivning URL** - Länk till jobbet du söker
3. **Åtgärd** - Vad du vill göra:
   - Generera grundläggande CV
   - Generera anpassat CV för jobbet
   - Generera personligt brev
   - **NYT!** Generera och skicka ansökan via email

### Automatiserad Jobbsökning med JobCraftAI

#### Skapa `data_folder/job_scraper_config.yaml`:
```yaml
platforms:
  - 'linkedin'
  - 'thehub'
  - 'arbetsformedlingen'

search_keywords:
  - 'python developer'
  - 'software engineer'
  - 'full stack developer'
  - 'dataingenjör'
  - 'systemutvecklare'

locations:
  - 'Stockholm'
  - 'Göteborg'
  - 'Uppsala'
  - 'Remote'

max_jobs_per_platform: 10
auto_apply: false  # Sätt till true för automatiska ansökningar
email_delay_minutes: 5  # Fördröjning mellan emails
```

#### Kör JobCraftAI automatiserad sökning:
```bash
python src/automated_job_applier.py --max-applications 20 --auto-apply
```

## 🌐 Plattformar som Stöds

### LinkedIn
- Automatisk scraping av jobbeskrivningar
- Stöd för sökningar
- **Obs:** Kräver inloggning och kan ha begränsningar

### TheHub (thehub.se)
- Svensk jobbplattform
- Bra för tech-jobb
- Öppen scraping

### Arbetsförmedlingen
- Sveriges officiella jobbportal
- Bred täckning av alla branscher
- Offentlig data

### Lägg till Nya Plattformar
Skapa en ny scraper-klass i `src/job_scrapers.py`:

```python
class MinJobbsajt(JobScraperBase):
    def __init__(self, driver=None):
        super().__init__(driver)
        self.platform_name = "MinJobbsajt"
        self.base_url = "https://minjobbsajt.se"
    
    def scrape_job(self, job_url: str) -> JobListing:
        # Implementera scraping-logik
        pass
```

## 🎨 Anpassa CV-stilar

Systemet kommer med flera färdiga stilar i `src/libs/resume_and_cover_builder/resume_style/`:
- `style_cloyola.css` - Modern och ren
- `style_josylad_blue.css` - Professionell blå
- `style_krishnavalliappan.css` - Kreativ design

### Skapa Din Egen Stil
1. Skapa ny CSS-fil i `resume_style/` mappen
2. Använd befintliga stilar som mall
3. Stilen kommer automatiskt att visas i listan

## 🤖 AI-anpassning

Systemet använder OpenAI GPT för att:
- **Analysera jobbeskrivningar** och identifiera nyckelkrav
- **Anpassa CV-innehåll** för att matcha jobbet
- **Generera personliga brev** som är relevanta
- **Optimera språk** för ATS (Applicant Tracking Systems)

### Prompts och Mallar
Du kan anpassa AI-beteendet genom att redigera:
- `src/libs/resume_and_cover_builder/cover_letter_prompt/strings_jobcraft.py`
- `src/libs/resume_and_cover_builder/resume_prompt/strings_jobcraft.py`

## 📊 Spårning och Statistik

Systemet håller reda på:
- Antal jobb hittade
- Ansökningar skickade
- Email-framgångsrate
- Genererade dokument

Loggar sparas i `data_folder/output/job_applications_log.yaml`

## 🔧 Avancerade Funktioner

### Bulk-ansökningar med JobCraftAI
```python
from src.automated_job_applier import JobCraftAI

jobcraft = JobCraftAI(
    data_folder=Path("data_folder"),
    llm_api_key="din-api-nyckel"
)

stats = jobcraft.run_automated_application_process(max_applications=50)
```

### Anpassad Email-mall
Redigera email-meddelandet i `src/email_sender.py`:

```python
def _create_email_body(self, company_name: str, position_title: str, custom_message: Optional[str] = None) -> str:
    base_message = f"""Hej,

    Jag är mycket intresserad av tjänsten som {position_title} på {company_name}.
    
    [Din anpassade text här]
    
    Med vänliga hälsningar,
    {self.config['sender_name']}"""
    
    return base_message
```

## 🛡️ Säkerhet och Etik

### Bästa Praxis:
- **Använd App-lösenord** för Gmail, inte ditt huvudlösenord
- **Begränsa antal ansökningar** per dag (max 10-20)
- **Lägg till fördröjningar** mellan ansökningar
- **Granska genererade dokument** innan du skickar
- **Följ plattformarnas användarvillkor**

### Rate Limiting:
```python
# I automated_job_applier.py
time.sleep(email_delay * 60)  # Vänta mellan ansökningar
```

## 🐛 Felsökning

### Vanliga Problem:

**1. Gmail Authentication Error:**
```
Solution: Använd App Password istället för vanligt lösenord
```

**2. Selenium WebDriver Error:**
```bash
# Installera om webdriver
pip install --upgrade webdriver-manager
```

**3. OpenAI API Error:**
```
Solution: Kontrollera att din API-nyckel är giltig och har kredit
```

**4. PDF Generation Error:**
```
Solution: Kontrollera att alla stilfiler finns i resume_style/ mappen
```

### Debug-läge:
Ändra i `config.py`:
```python
LOG_LEVEL = 'DEBUG'
LOG_TO_CONSOLE = True
```

## 📈 Tips för Bästa Resultat

### 1. Optimera ditt grund-CV
- Inkludera **alla relevanta färdigheter**
- Använd **branschspecifika nyckelord**
- Håll beskrivningar **konkreta och mätbara**

### 2. Ställ in bra sökkriterier
- Använd **specifika jobbtitlar**
- Inkludera **synonymer** (t.ex. "developer", "utvecklare")
- Testa **olika platsangivelser**

### 3. Anpassa AI-prompts
- Lägg till **branschspecifika instruktioner**
- Inkludera **företagskultur-matchning**
- Optimera för **ATS-system**

### 4. Email-strategi
- Skicka **inte för många** ansökningar per dag
- **Personalisera** email-mallar
- **Följ upp** manuellt viktiga ansökningar

## 🔄 Workflow-exempel

### Typisk Dag med JobCraftAI:

1. **Morgon (9:00):**
   ```bash
   python src/automated_job_applier.py --max-applications 10
   ```

2. **Lunch (12:00):**
   - Granska genererade dokument
   - Manuellt skicka prioriterade ansökningar

3. **Eftermiddag (15:00):**
   ```bash
   python main.py
   # Generera anpassade dokument för specifika jobb
   ```

4. **Kväll (18:00):**
   - Analysera statistik
   - Uppdatera CV baserat på feedback

### Veckovis Optimering:
- **Måndag:** Uppdatera sökkriterier
- **Onsdag:** Granska och förbättra AI-prompts  
- **Fredag:** Analysera veckostatistik och justera strategi

## 📞 Support och Bidrag

### Rapportera Problem:
- Skapa issue på GitHub
- Inkludera loggar och felmeddelanden
- Beskriv steg för att återskapa problemet

### Bidra med Kod:
- Fork projektet
- Skapa feature branch
- Skicka pull request

### Community:
- Dela framgångshistorier
- Föreslå förbättringar
- Hjälp andra användare

---

**Lycka till med din jobbsökning! 🎯**

*JobCraftAI hjälper dig att effektivisera processen, men kom ihåg att kvalitet är viktigare än kvantitet. Granska alltid dina ansökningar innan du skickar dem.*

---

**Skapad av Victor Vilches**  
*Dataingenjör & Entreprenör*  
*Kombinerar teknisk expertis med praktisk affärserfarenhet*
