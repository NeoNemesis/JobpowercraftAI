# JobpowercraftAI

**AI-powered job application automation** — search multiple job boards, and generate a tailored CV and cover letter for every position, in minutes.

---

## Features

- **Multi-platform search** — LinkedIn, Indeed, Arbetsförmedlingen (and easy to extend)
- **AI-tailored documents** — GPT-4o-mini rewrites your CV and cover letter to match each job description
- **Modern PDF design** — clean, ATS-friendly layout generated with ReportLab
- **Duplicate detection** — never processes the same job twice
- **Works in any language** — job ads and output documents match the language of the posting
- **Single entry point** — just run `python run.py`

---

## Requirements

| Requirement | Version |
|---|---|
| Python | 3.10+ |
| Google Chrome | Latest |
| OpenAI API key | Any tier |

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/NeoNemesis/JobpowercraftAI.git
cd JobpowercraftAI
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the setup wizard

```bash
python run.py
```

The wizard will ask you for:

1. **OpenAI API key** — get one at <https://platform.openai.com/api-keys>
2. **Your resume** — fill in `data_folder/plain_text_resume.yaml` with your details
3. **Job preferences** — edit `data_folder/work_preferences.yaml` to set positions, locations, and filters

### 5. Start searching

```bash
python run.py
# Choose option 1 — Search jobs
```

Documents are saved to `data_folder/output/job_master/`.

---

## Configuration Files

Both files are created automatically from templates during setup. They are excluded from git (`.gitignore`) so your personal data is never committed.

### `data_folder/plain_text_resume.yaml`

Your resume in structured YAML. Sections:
- `personal_information` — name, contact, links
- `professional_summary` — 2-3 sentence summary
- `cover_letter_profile` — base text for cover letters
- `education_details`, `experience_details` — your background
- `projects`, `achievements`, `certifications`, `languages`, `technical_skills`
- `legal_authorization`, `work_preferences`, `salary_expectations`

Copy from the included template:
```bash
cp data_folder/plain_text_resume.example.yaml data_folder/plain_text_resume.yaml
```

### `data_folder/work_preferences.yaml`

Controls what jobs are searched for:
```yaml
remote: true
hybrid: true
onsite: true

positions:
  - "Software Engineer"
  - "Backend Developer"

locations:
  - "Berlin"
  - "Remote"

experience_level:
  entry: true
  mid_senior_level: true

company_blacklist:
  - "CompanyToSkip"

title_blacklist:
  - "internship"
```

Copy from the included template:
```bash
cp data_folder/work_preferences.example.yaml data_folder/work_preferences.yaml
```

---

## Output Structure

```
data_folder/output/job_master/
├── Job_001_CompanyName_JobTitle/
│   ├── CV_CompanyName_JobTitle_Modern_Design_1.pdf
│   ├── Cover_Letter_CompanyName_JobTitle_Modern_Design_1.pdf
│   └── job_info.txt          ← application URL and instructions
├── found_jobs.json
└── processed_jobs.json       ← tracks already-processed jobs (no duplicates)
```

---

## Environment Variables

Create a `.env` file in the project root (the setup wizard does this automatically):

```env
OPENAI_API_KEY=sk-...
```

A template is provided at `.env.example`.

---

## Troubleshooting

**`ModuleNotFoundError`** — make sure your virtual environment is activated and you ran `pip install -r requirements.txt`.

**`ChromeDriver` errors** — make sure Google Chrome is installed. The `webdriver-manager` package handles the driver automatically.

**API key errors** — check that your OpenAI API key is valid and has available credits.

**Rate limits** — the tool adds short delays between requests to avoid being blocked by job sites.

---

## Re-running Setup

```bash
python run.py --setup
```

---

## License

MIT License — free to use, modify, and distribute.

---

*Built with Python, Selenium, OpenAI API, and ReportLab.*
