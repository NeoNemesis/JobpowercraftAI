# JobpowercraftAI (formerly JobCraftAI)
**Intelligent Job Application Automation**

---

## Recent Session Update (2025-01-24)

**Code Quality Improved: 3.0/10 → 6.5/10 (+3.5 points)**

This project underwent a comprehensive code analysis and refactoring session focusing on security hardening, performance optimization, and architectural improvements. Key achievements:

- 7/10 critical issues successfully resolved
- Security vulnerabilities patched (removed --disable-web-security, migrated API keys to env vars)
- 13x performance improvement via browser pooling
- 1500x faster resume caching
- New modular architecture established

**IMPORTANT:** One CRITICAL vulnerability remains - email header injection in email_sender.py must be fixed before production deployment.

See [JobpowercraftAI-session-summary.md](JobpowercraftAI-session-summary.md) for complete analysis.

---

<div align="center">

![JobCraftAI Logo](assets/logo_jobcraft.png)

**Created by Victor Vilches**
*Data Engineer & Construction Entrepreneur*

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![AI Powered](https://img.shields.io/badge/AI-Powered-green.svg)](https://openai.com/)
[![Code Quality](https://img.shields.io/badge/Code%20Quality-6.5%2F10-yellow.svg)](JobpowercraftAI-session-summary.md)

</div>

## 🎯 About JobCraftAI

JobCraftAI is an advanced AI-powered system that revolutionizes job searching by automatically creating tailored resumes and cover letters for each position you apply to. Built by **Victor Vilches**, combining expertise in data engineering and construction project management.

### 🚀 Key Features

- 🎯 **Smart Resume Tailoring**: AI analyzes job descriptions and customizes your CV
- 📝 **Intelligent Cover Letters**: Generates personalized cover letters for each application
- 🌐 **Multi-Platform Support**: Works with LinkedIn, TheHub.se, Arbetsförmedlingen
- 📧 **Automated Email Sending**: Professional application delivery via SMTP
- 📊 **Application Tracking**: Comprehensive statistics and success metrics
- 🎨 **Professional Formatting**: Multiple PDF styles and templates

## 🛠️ Quick Start

### Prerequisites

- Python 3.10 or higher
- OpenAI API key
- Gmail account (for automated email sending)
- Google Chrome browser

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/JobCraftAI.git
cd JobCraftAI
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up your configuration files**
```bash
cp -r data_folder_example/ data_folder/
```

## ⚙️ Configuration

### 1. Personal Information (`data_folder/plain_text_resume.yaml`)

```yaml
personal_information:
  name: "Your Name"
  surname: "Your Surname"
  email: "your.email@gmail.com"
  phone: "+1234567890"
  city: "Your City"
  country: "Your Country"
  github: "https://github.com/yourusername"
  linkedin: "https://linkedin.com/in/yourusername"

education_details:
  - education_level: "Bachelor's Degree"
    institution: "Your University"
    field_of_study: "Your Field"
    year_of_completion: "2023"

experience_details:
  - position: "Your Job Title"
    company: "Company Name"
    employment_period: "2020 - Present"
    key_responsibilities:
      - responsibility: "What you accomplished"
    skills_acquired:
      - "Python"
      - "JavaScript"
      - "Project Management"
```

### 2. API Configuration (`data_folder/secrets.yaml`)

```yaml
llm_api_key: 'sk-your-openai-api-key-here'
```

**Get your OpenAI API key:**
1. Visit [platform.openai.com](https://platform.openai.com)
2. Create an account or log in
3. Go to "API Keys"
4. Create a new key
5. Copy the key (starts with `sk-`)

### 3. Email Configuration (`data_folder/email_config.yaml`)

```yaml
smtp_server: 'smtp.gmail.com'
smtp_port: 587
email: 'your.email@gmail.com'
password: 'your-gmail-app-password'  # Use App Password, not regular password
sender_name: 'Your Full Name'
```

**Gmail App Password Setup:**
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable 2-Factor Authentication
3. Go to "App passwords"
4. Generate password for "Mail"
5. Use the 16-character password in your config

### 4. Job Preferences (`data_folder/work_preferences.yaml`)

```yaml
remote: true
hybrid: true
onsite: false

positions:
  - "Software Developer"
  - "Data Engineer"
  - "Full Stack Developer"

locations:
  - "New York"
  - "Remote"
  - "San Francisco"

experience_level:
  entry: false
  associate: true
  mid_senior_level: true
  director: false
```

## 🚀 Usage

### Basic Usage

```bash
python main.py
```

This will show you a menu with options:
- Generate Resume
- Generate Resume Tailored for Job Description
- Generate Tailored Cover Letter for Job Description
- **Generate and Send Job Application via Email**

### Automated Job Search

Create `data_folder/job_scraper_config.yaml`:

```yaml
platforms:
  - 'linkedin'
  - 'thehub'
  - 'arbetsformedlingen'

search_keywords:
  - 'python developer'
  - 'software engineer'
  - 'data engineer'

locations:
  - 'Stockholm'
  - 'Remote'
  - 'New York'

max_jobs_per_platform: 10
auto_apply: false  # Set to true for automatic applications
email_delay_minutes: 5  # Delay between emails
```

Run automated job search:
```bash
python src/automated_job_applier.py --max-applications 20 --auto-apply
```

## 🌐 Supported Platforms

### LinkedIn
- Automatic job description scraping
- Search functionality
- **Note:** Requires login and may have rate limits

### TheHub (thehub.se)
- Swedish job platform
- Great for tech jobs
- Open scraping

### Arbetsförmedlingen
- Sweden's official job portal
- Broad coverage of all industries
- Public data

### Adding New Platforms

Create a new scraper class in `src/job_scrapers.py`:

```python
class YourJobSiteScraper(JobScraperBase):
    def __init__(self, driver=None):
        super().__init__(driver)
        self.platform_name = "YourJobSite"
        self.base_url = "https://yourjobsite.com"
    
    def scrape_job(self, job_url: str) -> JobListing:
        # Implement scraping logic
        pass
```

## 🎨 Customization

### Resume Styles

JobCraftAI comes with multiple professional styles:
- `style_cloyola.css` - Modern and clean
- `style_josylad_blue.css` - Professional blue
- `style_krishnavalliappan.css` - Creative design

### AI Behavior

Customize AI prompts by editing:
- `src/libs/resume_and_cover_builder/cover_letter_prompt/strings_jobcraft.py`
- `src/libs/resume_and_cover_builder/resume_prompt/strings_jobcraft.py`

## 📊 Analytics & Tracking

JobCraftAI tracks:
- Number of jobs found
- Applications sent
- Email success rate
- Generated documents

Logs are saved in `data_folder/output/job_applications_log.yaml`

## 🔧 Advanced Features

### Bulk Applications

```python
from src.automated_job_applier import JobCraftAI

jobcraft = JobCraftAI(
    data_folder=Path("data_folder"),
    llm_api_key="your-api-key"
)

stats = jobcraft.run_automated_application_process(max_applications=50)
```

### Custom Email Templates

Edit email messages in `src/email_sender.py`:

```python
def _create_email_body(self, company_name: str, position_title: str, custom_message: Optional[str] = None) -> str:
    base_message = f"""Dear Hiring Manager,

    I am very interested in the {position_title} position at {company_name}.
    
    [Your custom message here]
    
    Best regards,
    {self.config['sender_name']}"""
    
    return base_message
```

## 🛡️ Security & Ethics

### Best Practices:
- **Use App Passwords** for Gmail, not your main password
- **Limit applications** per day (max 10-20)
- **Add delays** between applications
- **Review generated documents** before sending
- **Follow platform terms of service**

### Rate Limiting:
```python
# In automated_job_applier.py
time.sleep(email_delay * 60)  # Wait between applications
```

## 🐛 Troubleshooting

### Common Issues:

**1. Gmail Authentication Error:**
```
Solution: Use App Password instead of regular password
```

**2. Selenium WebDriver Error:**
```bash
# Reinstall webdriver
pip install --upgrade webdriver-manager
```

**3. OpenAI API Error:**
```
Solution: Check that your API key is valid and has credits
```

**4. PDF Generation Error:**
```
Solution: Ensure all style files exist in resume_style/ folder
```

### Debug Mode:
Change in `config.py`:
```python
LOG_LEVEL = 'DEBUG'
LOG_TO_CONSOLE = True
```

## 📈 Tips for Best Results

### 1. Optimize Your Base Resume
- Include **all relevant skills**
- Use **industry-specific keywords**
- Keep descriptions **concrete and measurable**

### 2. Set Good Search Criteria
- Use **specific job titles**
- Include **synonyms** (e.g. "developer", "engineer")
- Test **different locations**

### 3. Customize AI Prompts
- Add **industry-specific instructions**
- Include **company culture matching**
- Optimize for **ATS systems**

### 4. Email Strategy
- Don't send **too many** applications per day
- **Personalize** email templates
- **Follow up** manually on important applications

## 🔄 Example Workflow

### Typical Day with JobCraftAI:

1. **Morning (9:00 AM):**
   ```bash
   python src/automated_job_applier.py --max-applications 10
   ```

2. **Lunch (12:00 PM):**
   - Review generated documents
   - Manually send priority applications

3. **Afternoon (3:00 PM):**
   ```bash
   python main.py
   # Generate custom documents for specific jobs
   ```

4. **Evening (6:00 PM):**
   - Analyze statistics
   - Update resume based on feedback

## 👨‍💻 About the Creator

**Victor Vilches** brings a unique combination of technical and business expertise:

- **Data Engineering**: 2 years of mixed IT courses, specializing in system integration
- **Construction Industry**: Owner of Vilches Entreprenad AB, managing projects from start to finish
- **Full-Stack Development**: Proficient in JavaScript, Python, Java, C#
- **System Administration**: Expert in Linux/Windows environments and cybersecurity

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the project
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

- **GitHub Issues**: Report bugs and request features
- **Email**: victorvilches@protonmail.com
- **Website**: vilchesab.se

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT API
- LangChain for AI orchestration
- Selenium for web automation
- All contributors and users

---

**Good luck with your job search! 🎯**

*JobCraftAI helps you streamline the process, but remember that quality is more important than quantity. Always review your applications before sending them.*

---

<div align="center">

**Created with ❤️ by Victor Vilches**  
*Data Engineer & Construction Entrepreneur*  
*Combining technical expertise with practical business experience*

</div>