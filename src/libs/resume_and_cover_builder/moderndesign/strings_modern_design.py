"""
AI Prompt Templates for Modern Design CV Generation
"""

# Import templates directly
from template_modern_design import *

# Header Prompt
prompt_header = """
You are a resume expert. Create a professional header section for this resume.

Personal Information:
- Name: {personal_information_name}
- Email: {personal_information_email}
- Phone: {personal_information_phone}
- Location: {personal_information_location}
- Website: {personal_information_website}

Job Description: {job_description}

Create:
1. Full name (formatted professionally)
2. Job role/title that matches the job description
3. Brief personal summary (2-3 sentences) tailored to the job

Return ONLY the filled template:
{header_template}
"""

# Work Experience Prompt
prompt_work_experience = """
You are a resume expert. Create a work experience section tailored to this job.

Work Experience Details: {experience_details}
Job Description: {job_description}

For each relevant position:
1. Format dates as "MMM. YYYY - Present" or "MMM. YYYY - MMM. YYYY"
2. Write position title in format: "ROLE - COMPANY - CITY, COUNTRY"
3. Write compelling description (2-3 sentences) highlighting relevance to job
4. Include 2-3 major accomplishments with metrics if available

Use this template for each position:
{work_experience_template}

Return ALL relevant work experiences formatted with the template.
"""

# Education Prompt
prompt_education = """
You are a resume expert. Create an education section.

Education Details: {education_details}
Job Description: {job_description}

For each education entry:
1. Format dates as "YYYY" or "YYYY - YYYY"
2. Format degree as "DEGREE - SCHOOL NAME - CITY, COUNTRY"
3. Include relevant coursework, GPA, or achievements if applicable

Use this template:
{education_template}

Return ALL education entries formatted with the template.
"""

# Skills Prompt
prompt_skills = """
You are a resume expert. Create a skills section with visual rating.

Technical Skills: {technical_skills}
Soft Skills: {soft_skills}
Job Description: {job_description}

For each skill:
1. Choose skill name
2. Rate proficiency from 1-5 dots
3. Format: 5 filled dots = expert, 4 filled = advanced, 3 = intermediate, 2 = beginner

Example:
<div class="skill">
    <div class="skill-label">Python Programming</div>
    <div class="dots">
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot hollow"></div>
    </div>
</div>

Return 5-10 most relevant skills formatted with the template.
"""

# Projects Prompt
prompt_projects = """
You are a resume expert. Create a projects section.

Projects: {projects}
Job Description: {job_description}

For each relevant project:
1. Format dates
2. Write project title
3. Describe project and technologies used
4. Highlight results/impact

Use work-item template structure.
Return 2-4 most relevant projects.
"""

# Achievements Prompt
prompt_achievements = """
You are a resume expert. Create an achievements section.

Achievements: {achievements}
Job Description: {job_description}

List 3-5 most impressive and relevant achievements.
Use work-item template structure without dates if not applicable.
"""

# Certifications Prompt
prompt_certifications = """
You are a resume expert. Create a certifications section.

Certifications: {certifications}
Job Description: {job_description}

List relevant certifications with:
1. Certification name
2. Issuing organization
3. Date obtained

Use work-item template structure.
"""

# Interests Prompt
prompt_interests = """
You are a resume expert. Create an interests section.

Interests: {interests}
Job Description: {job_description}

Select 2-3 interests that:
1. Show cultural fit
2. Demonstrate relevant soft skills
3. Make candidate memorable

Use this template:
{interests_template}
"""

# Languages Prompt
prompt_languages = """
You are a resume expert. Create a languages section.

Languages: {languages}

Format each language with proficiency level:
- Native
- Fluent
- Professional
- Conversational
- Basic

Use simple list format in sidebar style.
"""

# Contact Info Prompt
prompt_contact = """
Create contact information items with appropriate SVG icons.

Contact Details:
- Address: {address}
- Phone: {phone}
- Email: {email}
- Website: {website}

Use these SVG paths:
- Location: M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z
- Phone: M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z
- Email: M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z
- Website: M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z

Return formatted contact items using the template.
"""

# Template references
header_template = MODERN_DESIGN_TEMPLATE
work_experience_template = WORK_EXPERIENCE_ITEM_TEMPLATE
education_template = EDUCATION_ITEM_TEMPLATE
interests_template = INTEREST_ITEM_TEMPLATE
