# Datakällor och Referenser för CV och Personliga Brev

## 📁 Huvudreferensfil: `data_folder/plain_text_resume.yaml`

Detta är den **ENDA** källfilen som innehåller ALL information om dig som används för att generera både CV och personliga brev.

---

## 🎯 Vad finns i `plain_text_resume.yaml`?

### 1. **Personal Information** (Personlig information)
```yaml
personal_information:
  name: "Victor"
  surname: "Vilches"
  date_of_birth: "02/12/1987"
  country: "Sverige"
  city: "Uppsala"
  address: "Kvarnängsgatan 24"
  phone: "707978547"
  email: "victorvilches@protonmail.com"
  github: "https://github.com/NeoNemesis"
  linkedin: "https://www.linkedin.com/in/victor-vilches-69a462155/"
  website: "vilchesab.se"
```

### 2. **Education Details** (Utbildning)
```yaml
education_details:
  - education_level: "Dataingenjör - 2 år blandade kurser inom IT"
    institution: "Gävle Universitet, Uppsala"
    field_of_study: "IT och Dataingenjörskap"
    year_of_completion: "2024"
    start_date: "2022"
  
  - education_level: "Programmering"
    institution: "Luleå Tekniska Högskolan"
    year_of_completion: "2021"
  
  - education_level: "Undersköterska"
    institution: "Lundellska skolan"
    year_of_completion: "2019"
```

### 3. **Experience Details** (Arbetslivserfarenhet)

**4 st arbetslivserfarenheter:**

1. **Vilches Entreprenad AB** (2020 - Present)
   - Position: Ägare & Projektledare
   - Skills: Project Management, Construction, Budget Planning

2. **Dataingenjör & Systemutvecklare** (2022 - Present)
   - Egen verksamhet
   - Skills: JavaScript, HTML5, CSS3, PHP, Java, C#, Python, SQL, Git

3. **System- & Nätverksadministratör** (2020 - Present)
   - Egen verksamhet
   - Skills: Linux/Windows Admin, Virtualization, CI/CD, DevOps

4. **Undersköterska** (2018 - 2020)
   - Skills: Teamwork, Communication, Patient Care

### 4. **Projects** (Projekt)
```yaml
projects:
  - name: "Jobbautomatisation för byggföretag"
  - name: "Portfolio API"
  - name: "Pico Ducky"
```

### 5. **Achievements** (Prestationer)
- Entreprenör inom byggbranschen
- Dataingenjör med praktisk erfarenhet
- Fullstack-utvecklare
- System- och nätverksspecialist

### 6. **Certifications** (Certifieringar)
- Webbutveckling I & II
- Databas teknik i SQL
- B-Körkort

### 7. **Languages** (Språkkunskaper)
```yaml
languages:
  - language: "Svenska"
    proficiency: "Modersmål"
  - language: "Engelska"
    proficiency: "Flytande"
  - language: "Spanska"
    proficiency: "Modersmål"
```

### 8. **Interests** (Intressen)
- Construction Technology, Project Management
- Systemintegration, Windows-miljöer
- Webbutveckling, Databaser
- Cybersäkerhet, AI-utveckling
- DevOps, Nätverksadministration

### 9. **Work Preferences** (Arbetspreferenser)
```yaml
work_preferences:
  remote_work: "Yes"
  in_person_work: "Yes"
  open_to_relocation: "Yes"
```

### 10. **Legal Authorization** (Arbetstillstånd)
- EU work authorization: Yes
- Legally allowed to work in EU: Yes

---

## 🤖 Hur används denna data?

### **För CV-generering:**

1. **Läs YAML-filen:**
   ```python
   resume_path = 'data_folder/plain_text_resume.yaml'
   with open(resume_path, 'r', encoding='utf-8') as file:
       plain_text_resume = file.read()
   
   resume_object = Resume(plain_text_resume)
   ```

2. **Modern Design 1 använder:**
   - `resume_object.personal_information` → Namn, kontaktinfo
   - `resume_object.education_details` → Utbildningssektion
   - `resume_object.experience_details` → Arbetslivserfarenhet
   - `resume_object.languages` → Språkkunskaper
   - `resume_object.certifications` → Övriga kunskaper

3. **AI anpassar innehållet:**
   - Läser jobbeskrivning från URL
   - Matchar dina skills mot jobbet
   - Skriver om erfarenheter för att passa rollen
   - Anpassar språk (svenska/engelska)

### **För Personligt Brev:**

1. **Använder samma `plain_text_resume.yaml`**

2. **AI Prompt från:** `src/libs/resume_and_cover_builder/cover_letter_prompt/strings_jobcraft.py`

3. **Genererar brev genom:**
   ```python
   # Analyserar jobbeskrivningen
   # Matchar mot din resume
   # Skriver 3 paragrafer:
   #   1. Introduktion + varför du passar
   #   2. Relevanta skills och erfarenheter
   #   3. Varför du vill jobba där
   ```

---

## 📝 Vilka AI-prompts används?

### **För CV:**
- `src/libs/resume_and_cover_builder/resume_prompt/strings_jobcraft.py`
- `src/libs/resume_and_cover_builder/resume_job_description_prompt/strings_jobcraft.py`

### **För Personligt Brev:**
- `src/libs/resume_and_cover_builder/cover_letter_prompt/strings_jobcraft.py`

---

## 🔄 Dataflöde

```
1. data_folder/plain_text_resume.yaml
   ↓
2. Resume(plain_text_resume) → resume_object
   ↓
3. Jobbeskrivning från URL (via LLMParser)
   ↓
4. AI Generator (LLMResumer / ModernDesign1Generator)
   - Matchar resume_object mot jobbeskrivning
   - Väljer relevanta skills och erfarenheter
   - Anpassar språk och ton
   ↓
5. HTML genereras med CSS från modern_template.html
   ↓
6. PDF skapas (html2pdf)
```

---

## ✏️ Hur uppdaterar du din information?

### **ENDA filen du behöver ändra:**
```
data_folder/plain_text_resume.yaml
```

**Exempel på ändringar:**

#### Lägga till ny arbetslivserfarenhet:
```yaml
experience_details:
  - position: "Ny roll"
    company: "Nytt företag"
    employment_period: "2024 - Present"
    key_responsibilities:
      - responsibility: "Beskrivning av vad du gjorde"
    skills_acquired:
      - "Ny skill 1"
      - "Ny skill 2"
```

#### Uppdatera kontaktinfo:
```yaml
personal_information:
  phone: "NYT TELEFONNUMMER"
  email: "ny@email.com"
```

#### Lägga till ny utbildning:
```yaml
education_details:
  - education_level: "Ny kurs"
    institution: "Ny skola"
    year_of_completion: "2024"
```

---

## 🎯 Sammanfattning

**En fil styr allt:**
- ✅ **`data_folder/plain_text_resume.yaml`** → All din information
- ✅ AI läser denna fil och anpassar innehållet för varje jobb
- ✅ Ingen hårdkodad information i kod-filer
- ✅ Uppdatera en gång, fungerar för alla modeller (Ursprungliga, Modern Design 1, Modern Design 2)

**För personliga brev:**
- ✅ Samma YAML-fil används
- ✅ AI-prompt skriver anpassat brev
- ✅ Matchar automatiskt mot jobbeskrivning

**Inget behov av separata mallar eller exempel-CV!**


