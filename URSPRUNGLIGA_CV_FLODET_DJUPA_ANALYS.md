# Det Ursprungliga CV-Flödet - Djupgående Teknisk Analys

## 🎯 Översikt

Det ursprungliga CV-flödet är ett sofistikerat system som använder **Facade Pattern**, **Template Pattern**, och **AI-driven innehållsgenerering** för att skapa skräddarsydda CV:n baserat på jobbeskrivningar.

---

## 🏗️ Arkitektur och Design Patterns

### **1. Facade Pattern (ResumeFacade)**
- **Syfte:** Förenklar komplexa interaktioner mellan flera komponenter
- **Implementering:** `src/libs/resume_and_cover_builder/resume_facade.py`
- **Ansvar:** Koordinerar alla delar av CV-genereringen under en enkel interface

### **2. Template Pattern (HTML Template System)**
- **Syfte:** Separerar struktur från innehåll
- **Implementering:** `global_config.html_template` + CSS-filer
- **Ansvar:** Ger konsekvent HTML-struktur med varierande stilar

### **3. Strategy Pattern (LLM Generators)**
- **Syfte:** Olika AI-strategier för olika typer av innehåll
- **Implementering:** `LLMResumer`, `LLMResumeJobDescription`, `LLMCoverLetterJobDescription`
- **Ansvar:** Specialiserad AI-generering för varje CV-sektion

---

## 🔄 Detaljerat Flöde - Steg för Steg

### **STEG 1: Initiering och Konfiguration**

```python
# 1. Läs användarens data
plain_text_resume = file.read('data_folder/plain_text_resume.yaml')
resume_object = Resume(plain_text_resume)

# 2. Initiera komponenter
style_manager = StyleManager()
resume_generator = ResumeGenerator()
driver = init_browser()  # Chrome WebDriver för PDF-generering

# 3. Skapa ResumeFacade
resume_facade = ResumeFacade(
    api_key=llm_api_key,
    style_manager=style_manager,
    resume_generator=resume_generator,
    resume_object=resume_object,
    output_path=Path("data_folder/output")
)
```

**Vad händer:**
- `ResumeFacade.__init__()` konfigurerar `global_config` med alla sökvägar
- `global_config` blir den centrala konfigurationspunkten för hela systemet
- Alla komponenter får tillgång till samma konfiguration

### **STEG 2: Jobb-länkning och Dataextraktion**

```python
resume_facade.set_driver(driver)
resume_facade.link_to_job(job_url)
```

**Detaljerat vad som händer:**

1. **WebDriver Navigation:**
   ```python
   self.driver.get(job_url)
   self.driver.implicitly_wait(10)
   body_element = self.driver.find_element("tag name", "body")
   body_element = body_element.get_attribute("outerHTML")
   ```

2. **AI-driven Jobbparsing:**
   ```python
   self.llm_job_parser = LLMParser(openai_api_key=global_config.API_KEY)
   self.llm_job_parser.set_body_html(body_element)
   
   self.job = Job()
   self.job.role = self.llm_job_parser.extract_role()
   self.job.company = self.llm_job_parser.extract_company_name()
   self.job.description = self.llm_job_parser.extract_job_description()
   self.job.location = self.llm_job_parser.extract_location()
   ```

**Vad händer:**
- WebDriver hämtar hela HTML-sidan från jobb-URL:en
- `LLMParser` använder AI för att extrahera strukturerad information
- `Job`-objektet fylls med extraherade data

### **STEG 3: CV-generering med AI**

```python
result_base64, suggested_name = resume_facade.create_resume_pdf_job_tailored()
```

**Detaljerat flöde:**

#### **3A: Style Management**
```python
style_path = self.style_manager.get_style_path()
if style_path is None:
    raise ValueError("You must choose a style before generating the PDF.")
```

#### **3B: Resume Generator Orchestration**
```python
html_resume = self.resume_generator.create_resume_job_description_text(
    style_path, 
    self.job.description
)
```

**Vad händer i `create_resume_job_description_text`:**

1. **Module Loading:**
   ```python
   strings = load_module(
       global_config.STRINGS_MODULE_RESUME_JOB_DESCRIPTION_PATH, 
       global_config.STRINGS_MODULE_NAME
   )
   ```

2. **LLM Generator Creation:**
   ```python
   gpt_answerer = LLMResumeJobDescription(global_config.API_KEY, strings)
   gpt_answerer.set_job_description_from_text(job_description_text)
   ```

3. **Template Application:**
   ```python
   return self._create_resume(gpt_answerer, style_path)
   ```

#### **3C: _create_resume Metoden**

```python
def _create_resume(self, gpt_answerer: Any, style_path):
    # 1. Sätt resume-objektet i AI-generatorn
    gpt_answerer.set_resume(self.resume_object)
    
    # 2. Läs HTML template
    template = Template(global_config.html_template)
    
    # 3. Läs CSS-fil
    with open(style_path, "r") as f:
        style_css = f.read()
    
    # 4. Generera HTML-innehåll med AI
    body_html = gpt_answerer.generate_html_resume()
    
    # 5. Kombinera template + CSS + innehåll
    return template.substitute(body=body_html, style_css=style_css)
```

### **STEG 4: AI-driven HTML-generering**

**Vad händer i `generate_html_resume()`:**

```python
def generate_html_resume(self) -> str:
    header = self.generate_header()
    education = self.generate_education_section()
    work_experience = self.generate_work_experience_section()
    projects = self.generate_projects_section()
    achievements = self.generate_achievements_section()
    certifications = self.generate_certifications_section()
    additional_skills = self.generate_additional_skills_section()
    
    return f"{header}{education}{work_experience}{projects}{achievements}{certifications}{additional_skills}"
```

**Varje sektion genereras med AI:**

1. **Prompt Creation:**
   ```python
   education_prompt_template = self._preprocess_template_string(
       self.strings.prompt_education
   )
   ```

2. **LangChain Chain:**
   ```python
   prompt = ChatPromptTemplate.from_template(education_prompt_template)
   chain = prompt | self.llm_cheap | StrOutputParser()
   ```

3. **AI Invocation med Data:**
   ```python
   output = chain.invoke({
       "education_details": self.resume.education_details,
       "job_description": self.job_description
   })
   ```

### **STEG 5: HTML Template System**

**Global HTML Template (`global_config.html_template`):**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume</title>
    <link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;600&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" /> 
    <style>
        $style_css
    </style>
</head>
<body>
$body
</body>
</html>
```

**Template Substitution:**
```python
return template.substitute(body=body_html, style_css=style_css)
```

### **STEG 6: PDF-generering**

```python
result = HTML_to_PDF(html_resume, self.driver)
self.driver.quit()
return result, suggested_name
```

**HTML_to_PDF Process:**
1. WebDriver navigerar till en lokal HTML-fil
2. Använder Chrome's print-funktionalitet
3. Konverterar till PDF med hög kvalitet
4. Returnerar PDF som base64

---

## 🧠 AI-prompt System

### **Prompt Templates (src/libs/resume_and_cover_builder/resume_prompt/strings_jobcraft.py)**

Varje sektion har sin egen prompt-template:

```python
# Exempel: Education Section
prompt_education = """
You are an expert resume writer. Create an education section based on the provided education details and job description.

Education Details: {education_details}
Job Description: {job_description}

Focus on:
- Relevance to the job
- Academic achievements
- Relevant coursework

{template_to_use}  # HTML template från template_base.py
"""
```

### **Template System (template_base.py)**

Varje prompt innehåller en HTML-template:

```html
<section id="education">
    <h2>Education</h2>
    <div class="entry">
      <div class="entry-header">
          <span class="entry-name">[University Name]</span>
          <span class="entry-location">[Location]</span>
      </div>
      <div class="entry-details">
          <span class="entry-title">[Degree] in [Field of Study] | Grade: [Your Grade]</span>
          <span class="entry-year">[Start Year] – [End Year]</span>
      </div>
      <ul class="compact-list">
          <li>[Course Name] → Grade: [Grade]</li>
      </ul>
    </div>
</section>
```

---

## 🔧 Global Configuration System

### **GlobalConfig Class**

```python
class GlobalConfig:
    def __init__(self):
        self.STRINGS_MODULE_RESUME_PATH: Path = None
        self.STRINGS_MODULE_RESUME_JOB_DESCRIPTION_PATH: Path = None
        self.STRINGS_MODULE_COVER_LETTER_JOB_DESCRIPTION_PATH: Path = None
        self.STRINGS_MODULE_NAME: str = None
        self.STYLES_DIRECTORY: Path = None
        self.LOG_OUTPUT_FILE_PATH: Path = None
        self.API_KEY: str = None
        self.html_template = """..."""
```

### **Konfiguration i ResumeFacade**

```python
def __init__(self, api_key, style_manager, resume_generator, resume_object, output_path):
    lib_directory = Path(__file__).resolve().parent
    global_config.STRINGS_MODULE_RESUME_PATH = lib_directory / "resume_prompt/strings_jobcraft.py"
    global_config.STRINGS_MODULE_RESUME_JOB_DESCRIPTION_PATH = lib_directory / "resume_job_description_prompt/strings_jobcraft.py"
    global_config.STRINGS_MODULE_COVER_LETTER_JOB_DESCRIPTION_PATH = lib_directory / "cover_letter_prompt/strings_jobcraft.py"
    global_config.STRINGS_MODULE_NAME = "strings_jobcraft"
    global_config.STYLES_DIRECTORY = lib_directory / "resume_style"
    global_config.LOG_OUTPUT_FILE_PATH = output_path
    global_config.API_KEY = api_key
```

---

## 📊 Dataflöde Diagram

```
1. plain_text_resume.yaml
   ↓
2. Resume Object Creation
   ↓
3. ResumeFacade Initialization
   ↓
4. WebDriver + Job URL
   ↓
5. LLMParser (AI Job Extraction)
   ↓
6. Job Object (structured data)
   ↓
7. ResumeGenerator.create_resume_job_description_text()
   ↓
8. LLMResumeJobDescription (AI Generator)
   ↓
9. Parallel AI Generation:
   - Header Section
   - Education Section  
   - Work Experience Section
   - Projects Section
   - Achievements Section
   - Certifications Section
   - Additional Skills Section
   ↓
10. HTML Assembly
    ↓
11. Template + CSS Combination
    ↓
12. HTML_to_PDF Conversion
    ↓
13. Base64 PDF Output
```

---

## 🎨 Style Management System

### **StyleManager**

```python
class StyleManager:
    def __init__(self):
        self.selected_style = None
        self.styles_directory = global_config.STYLES_DIRECTORY
    
    def get_style_path(self) -> Path:
        return self.styles_directory / f"{self.selected_style}.css"
```

### **CSS Integration**

1. **CSS-fil läsning:**
   ```python
   with open(style_path, "r") as f:
       style_css = f.read()
   ```

2. **CSS injection i HTML:**
   ```html
   <style>
       $style_css
   </style>
   ```

---

## 🔄 Parallel Processing

### **Concurrent AI Generation**

```python
def generate_html_resume(self) -> str:
    with ThreadPoolExecutor(max_workers=6) as executor:
        # Skicka alla sektioner parallellt till AI
        futures = {
            executor.submit(self.generate_header): 'header',
            executor.submit(self.generate_education_section): 'education',
            executor.submit(self.generate_work_experience_section): 'work_experience',
            executor.submit(self.generate_projects_section): 'projects',
            executor.submit(self.generate_achievements_section): 'achievements',
            executor.submit(self.generate_certifications_section): 'certifications',
            executor.submit(self.generate_additional_skills_section): 'additional_skills'
        }
        
        # Samla resultat
        results = {}
        for future in as_completed(futures):
            section_name = futures[future]
            try:
                results[section_name] = future.result()
            except Exception as exc:
                logger.error(f'{section_name} generated an exception: {exc}')
        
        # Kombinera i rätt ordning
        return (results['header'] + results['education'] + 
                results['work_experience'] + results['projects'] + 
                results['achievements'] + results['certifications'] + 
                results['additional_skills'])
```

---

## 📝 Logging och Debugging

### **LoggerChatModel**

```python
class LoggerChatModel:
    def __init__(self, chat_model):
        self.chat_model = chat_model
    
    def invoke(self, input_data):
        # Logga input
        logger.debug(f"AI Input: {input_data}")
        
        # Anropa AI
        result = self.chat_model.invoke(input_data)
        
        # Logga output
        logger.debug(f"AI Output: {result}")
        
        return result
```

### **Log Configuration**

```python
# Varje AI-generator har sin egen log-fil
log_folder = 'log/resume/gpt_resume'
log_path = Path(log_folder).resolve()
logger.add(log_path / "gpt_resume.log", rotation="1 day", compression="zip", retention="7 days", level="DEBUG")
```

---

## 🚀 Hur man Anpassar för Nya Modeller

### **1. Skapa Ny Facade**

```python
class ModernDesign2Facade:
    def __init__(self, api_key, style_manager, resume_generator, resume_object, output_path):
        # SAMMA global_config setup som ResumeFacade
        lib_directory = Path(__file__).resolve().parent
        global_config.STRINGS_MODULE_RESUME_PATH = lib_directory / "resume_prompt/strings_jobcraft.py"
        # ... samma konfiguration
        
        self.style_manager = style_manager
        self.resume_generator = resume_generator
        self.resume_generator.set_resume_object(resume_object)
        self.output_path = output_path
        self.driver = None
        self.job = None
    
    def set_driver(self, driver):
        self.driver = driver
    
    def link_to_job(self, job_url):
        # EXAKT samma logik som ResumeFacade
        self.driver.get(job_url)
        # ... samma jobbparsing
    
    def create_resume_pdf_job_tailored(self) -> tuple:
        # Använd din egen AI-generator
        html_resume = self._create_modern_design2_resume(style_path, self.job.description)
        
        suggested_name = hashlib.md5(self.job.link.encode()).hexdigest()[:10]
        
        result = HTML_to_PDF(html_resume, self.driver)
        self.driver.quit()  # Viktigt!
        return result, suggested_name
```

### **2. Skapa AI Generator**

```python
class ModernDesign2Generator:
    def __init__(self, resume_object):
        self.resume_object = resume_object
    
    def generate_complete_cv_html(self, job_description: str) -> str:
        # Din egen logik för CV-generering
        # Kan använda:
        # - Samma AI-system som ursprungliga
        # - Egen template-system
        # - Direkt data-mapping
        # - Hybrid-approach
        
        return complete_html
```

### **3. Template System**

```python
# Antingen använd global_config.html_template:
template = Template(global_config.html_template)
return template.substitute(body=body_html, style_css=style_css)

# Eller skapa egen template:
custom_template = """
<!DOCTYPE html>
<html>
<head>
    <style>$custom_css</style>
</head>
<body>
$custom_body
</body>
</html>
"""
```

### **4. Integration i main.py**

```python
def create_modern_design2_cv(job_url: str, resume_object, llm_api_key: str, selected_template: str) -> tuple:
    logger.info("🎨 Modern Design 2: Startar eget flöde")
    
    try:
        from src.libs.resume_and_cover_builder.moderndesign2.modern_design2_facade import ModernDesign2Facade
        
        # SAMMA komponenter som ursprungliga
        style_manager = StyleManager()
        resume_generator = ResumeGenerator()
        driver = init_browser()
        
        # Använd din facade
        modern_facade = ModernDesign2Facade(
            api_key=llm_api_key,
            style_manager=style_manager,
            resume_generator=resume_generator,
            resume_object=resume_object,
            output_path=Path("data_folder/output")
        )
        
        modern_facade.set_driver(driver)
        modern_facade.link_to_job(job_url)
        
        result_base64, suggested_name = modern_facade.create_resume_pdf_job_tailored()
        
        return result_base64, suggested_name
    except Exception as e:
        logger.error(f"❌ Modern Design 2: {e}")
        raise
```

---

## 🔑 Kritiska Komponenter för Replikation

### **1. Global Configuration**
- **MÅSTE** använda `global_config` för konsekvent konfiguration
- **MÅSTE** sätta alla sökvägar i `__init__`
- **MÅSTE** ge tillgång till `API_KEY` för alla komponenter

### **2. WebDriver Management**
- **MÅSTE** använda `init_browser()` för Chrome-instans
- **MÅSTE** använda `HTML_to_PDF()` för PDF-generering
- **MÅSTE** anropa `driver.quit()` i facaden

### **3. Job Parsing**
- **MÅSTE** använda `LLMParser` för jobbextraktion
- **MÅSTE** skapa `Job`-objekt med extraherade data
- **MÅSTE** använda `link_to_job()` metoden

### **4. AI Integration**
- **KAN** använda samma `LLMResumeJobDescription` system
- **KAN** skapa egen AI-generator med samma interface
- **KAN** använda `LoggerChatModel` för debugging

### **5. Template System**
- **KAN** använda `global_config.html_template`
- **KAN** skapa egen template med `Template.substitute()`
- **KAN** integrera CSS via `$style_css` placeholder

---

## 📋 Checklista för Ny Modell

- [ ] **Facade:** Skapa facade som implementerar samma interface som `ResumeFacade`
- [ ] **Global Config:** Sätt `global_config` i facade `__init__`
- [ ] **WebDriver:** Använd `init_browser()` och `HTML_to_PDF()`
- [ ] **Job Parsing:** Använd `LLMParser` och `link_to_job()`
- [ ] **AI Generator:** Skapa generator som kan använda `resume_object` + `job_description`
- [ ] **Template:** Implementera HTML template system (global eller egen)
- [ ] **CSS:** Integrera CSS-filer via template system
- [ ] **PDF Output:** Returnera base64 PDF + suggested_name
- [ ] **Error Handling:** Implementera try/catch med logging
- [ ] **Integration:** Lägg till i `main.py` med samma interface

---

## 🎯 Sammanfattning

Det ursprungliga CV-flödet är ett **högt avancerat system** som:

1. **Använder Facade Pattern** för att förenkla komplexa interaktioner
2. **AI-driven innehållsgenerering** med parallell bearbetning
3. **Template-baserat HTML-system** för konsekvent struktur
4. **Global konfiguration** för centraliserad hantering
5. **WebDriver-integration** för högkvalitativ PDF-generering
6. **Strukturerad jobbparsing** med AI-extraktion
7. **Omfattande logging** för debugging och monitoring

**För att anpassa andra modeller behöver du replikera denna arkitektur medan du behåller flexibiliteten att implementera egen AI-logik och templates.**

---

## 🔄 Modern Design 1 - Hybrid Approach Rekommendation

### **Nuvarande Implementation Analys**

**Styrkor:**
- ✅ Exakt samma flöde som ursprungliga (`ModernDesign1Facade` följer `ResumeFacade` 100%)
- ✅ Språkdetektering med automatisk anpassning (svenska/engelska)
- ✅ Isolerad arkitektur utan `global_config` konflikter
- ✅ Konsistent datahantering via `resume_object`
- ✅ Fungerande PDF-generering med `HTML_to_PDF`

**Svagheter:**
- ❌ Begränsad enkel enkolumns layout
- ❌ Hårdkodad innehåll med mindre flexibilitet
- ❌ Ingen AI-anpassning till specifika jobb
- ❌ Saknar professionell tvåkolumns design

### **Rekommenderad Hybrid Approach**

**BEHÅLL från nuvarande:**
1. **Facade Architecture** - `modern_facade.py` (exakt samma flöde som ursprungliga)
2. **Language Detection** - `language_detector.py` (fungerar perfekt)
3. **Isolated Utils** - `isolated_utils.py` (ingen konflikt)
4. **PDF Generation** - WebDriver och `HTML_to_PDF` integration

**FÖRBÄTTRA med:**
1. **Tvåkolumns Layout** - Professionell design (35% vänster, 65% höger)
2. **AI-baserad Innehållsgenerering** - Jobbspecifik anpassning
3. **Flexibel Template-struktur** - Stöder olika innehållstyper
4. **Förbättrad CSS** - Moderna designelement

### **Föreslagen Ny Struktur**

```
src/libs/resume_and_cover_builder/moderndesign1/
├── modern_facade.py              # BEHÅLL - exakt samma som nu
├── hybrid_generator.py           # NY - kombinerar data + AI
├── modern_template.html          # NY - tvåkolumns layout
├── language_detector.py          # BEHÅLL - fungerar bra
├── isolated_utils.py             # BEHÅLL - ingen konflikt
├── ai_prompts.py                 # NY - AI-prompts för jobbspecifik anpassning
└── style_manager.py              # BEHÅLL - fungerar bra
```

### **Hybrid Generator Logik**

```python
class HybridModernDesign1Generator:
    def __init__(self, resume_object: Any):
        self.resume_object = resume_object
        self.language = 'sv'  # Standard svenska
    
    def generate_complete_cv_html(self, job_description: str) -> str:
        # 1. Språkdetektering (behåll från nuvarande)
        self.language = detect_job_language(job_description)
        
        # 2. Data-baserad grund (behåll från nuvarande)
        base_content = self._generate_base_content_from_data()
        
        # 3. AI-anpassning (ny - för jobbspecifik innehåll)
        tailored_content = self._generate_ai_tailored_content(job_description, base_content)
        
        # 4. Tvåkolumns layout (ny - professionell design)
        return self._assemble_two_column_layout(tailored_content)
```

### **Integration Considerations**

**För att Modern Design 1 ska fungera optimalt med ursprungliga flödet:**

1. **Behåll exakt samma facade interface** - `ModernDesign1Facade` ska vara identisk med `ResumeFacade`
2. **Använd samma global_config setup** - För konsekvent konfiguration
3. **Implementera samma WebDriver management** - `init_browser()`, `HTML_to_PDF()`, `driver.quit()`
4. **Använd samma job parsing** - `LLMParser` och `link_to_job()` metod
5. **Kombinera data + AI** - Använd `resume_object` som grund + AI för jobbspecifik anpassning

### **Template System Förbättringar**

**Nuvarande:** Enkel enkolumns layout
```html
<div class="cv-container">
    <div class="profile-section">
        <div class="profile-image">...</div>
    </div>
    <div class="content">$body</div>
    <div class="footer">...</div>
</div>
```

**Rekommenderad:** Tvåkolumns professionell layout
```html
<div class="cv-container">
    <div class="vertical-line"></div>
    <div class="left-column">
        <div class="profile-image">...</div>
        <div class="section">$education</div>
        <div class="section">$skills</div>
        <div class="section">$languages</div>
        <div class="section">$contact</div>
    </div>
    <div class="right-column">
        <div class="header">$header</div>
        <div class="experience">$work_experience</div>
    </div>
</div>
```

### **AI Integration Strategy**

**Fas 1: Data-baserad grund** (behåll från nuvarande)
- Använd `resume_object` för grundläggande information
- Språkdetektering för automatisk anpassning
- Konsistent datahantering

**Fas 2: AI-anpassning** (ny funktionalitet)
- Jobbspecifik innehållsgenerering
- Anpassning av sektioner baserat på jobbeskrivning
- Dynamisk innehållsoptimering

**Fas 3: Layout-assembling** (förbättrad design)
- Tvåkolumns professionell layout
- Responsiv design för olika skärmstorlekar
- Print-optimerad CSS

### **Implementation Roadmap**

1. **Behåll nuvarande facade** - Ingen ändring i `modern_facade.py`
2. **Skapa hybrid generator** - Kombinera data + AI approach
3. **Utveckla tvåkolumns template** - Professionell layout
4. **Implementera AI prompts** - Jobbspecifik anpassning
5. **Testa integration** - Verifiera att flödet fungerar identiskt
6. **Optimera CSS** - Modern design med print-support

**Resultat:** Modern Design 1 som fungerar exakt som ursprungliga flödet men med förbättrad design och AI-anpassning.
