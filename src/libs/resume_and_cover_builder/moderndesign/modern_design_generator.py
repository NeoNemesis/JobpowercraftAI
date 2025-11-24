"""
Modern Design Generator - AI-driven CV content generation
"""

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from loguru import logger
from pathlib import Path

class ModernDesignGenerator:
    def __init__(self, api_key: str, strings_module):
        self.llm_cheap = ChatOpenAI(
            model_name="gpt-4o-mini",
            openai_api_key=api_key,
            temperature=0.4
        )
        self.strings = strings_module
        self.resume = None
        self.job_description = None
        
    def set_resume(self, resume):
        self.resume = resume
        
    def set_job_description(self, job_description: str):
        self.job_description = job_description
        
    def generate_header(self) -> str:
        """Generate header with name, title, and summary"""
        prompt = ChatPromptTemplate.from_template(self.strings.prompt_header)
        chain = prompt | self.llm_cheap | StrOutputParser()
        
        return chain.invoke({
            "personal_information_name": self.resume.personal_information.name,
            "personal_information_email": self.resume.personal_information.email,
            "personal_information_phone": self.resume.personal_information.phonePrefix + self.resume.personal_information.phone,
            "personal_information_location": f"{self.resume.personal_information.city}, {self.resume.personal_information.country}",
            "personal_information_website": getattr(self.resume.personal_information, 'website', ''),
            "job_description": self.job_description,
            "header_template": self.strings.header_template
        })
    
    def generate_work_experience(self) -> str:
        """Generate work experience section"""
        prompt = ChatPromptTemplate.from_template(self.strings.prompt_work_experience)
        chain = prompt | self.llm_cheap | StrOutputParser()
        
        return chain.invoke({
            "experience_details": self.resume.experience_details,
            "job_description": self.job_description,
            "work_experience_template": self.strings.work_experience_template
        })
    
    def generate_education(self) -> str:
        """Generate education section"""
        prompt = ChatPromptTemplate.from_template(self.strings.prompt_education)
        chain = prompt | self.llm_cheap | StrOutputParser()
        
        return chain.invoke({
            "education_details": self.resume.education_details,
            "job_description": self.job_description,
            "education_template": self.strings.education_template
        })
    
    def generate_skills(self) -> str:
        """Generate skills section with dots rating"""
        prompt = ChatPromptTemplate.from_template(self.strings.prompt_skills)
        chain = prompt | self.llm_cheap | StrOutputParser()
        
        return chain.invoke({
            "technical_skills": getattr(self.resume, 'technical_skills', []),
            "soft_skills": getattr(self.resume, 'soft_skills', []),
            "job_description": self.job_description
        })
    
    def generate_contact_info(self) -> str:
        """Generate contact information with icons"""
        prompt = ChatPromptTemplate.from_template(self.strings.prompt_contact)
        chain = prompt | self.llm_cheap | StrOutputParser()
        
        return chain.invoke({
            "address": f"{self.resume.personal_information.city}, {self.resume.personal_information.country}",
            "phone": self.resume.personal_information.phonePrefix + self.resume.personal_information.phone,
            "email": self.resume.personal_information.email,
            "website": getattr(self.resume.personal_information, 'website', '')
        })
    
    def generate_projects(self) -> str:
        """Generate projects section"""
        prompt = ChatPromptTemplate.from_template(self.strings.prompt_projects)
        chain = prompt | self.llm_cheap | StrOutputParser()
        
        return chain.invoke({
            "projects": getattr(self.resume, 'projects', []),
            "job_description": self.job_description
        })
    
    def generate_achievements(self) -> str:
        """Generate achievements section"""
        prompt = ChatPromptTemplate.from_template(self.strings.prompt_achievements)
        chain = prompt | self.llm_cheap | StrOutputParser()
        
        return chain.invoke({
            "achievements": getattr(self.resume, 'achievements', []),
            "job_description": self.job_description
        })
    
    def generate_certifications(self) -> str:
        """Generate certifications section"""
        prompt = ChatPromptTemplate.from_template(self.strings.prompt_certifications)
        chain = prompt | self.llm_cheap | StrOutputParser()
        
        return chain.invoke({
            "certifications": getattr(self.resume, 'certifications', []),
            "job_description": self.job_description
        })
    
    def generate_interests(self) -> str:
        """Generate interests section"""
        prompt = ChatPromptTemplate.from_template(self.strings.prompt_interests)
        chain = prompt | self.llm_cheap | StrOutputParser()
        
        return chain.invoke({
            "interests": getattr(self.resume, 'interests', []),
            "job_description": self.job_description,
            "interests_template": self.strings.interests_template
        })
    
    def generate_languages(self) -> str:
        """Generate languages section"""
        prompt = ChatPromptTemplate.from_template(self.strings.prompt_languages)
        chain = prompt | self.llm_cheap | StrOutputParser()
        
        return chain.invoke({
            "languages": getattr(self.resume, 'languages', [])
        })
    
    def generate_complete_resume(self) -> str:
        """Generate complete resume HTML"""
        logger.info("Generating Modern Design Resume...")
        
        try:
            # Generate all sections
            contact_info = self.generate_contact_info()
            header_content = self.generate_header()
            work_exp = self.generate_work_experience()
            education = self.generate_education()
            skills = self.generate_skills()
            projects = self.generate_projects()
            achievements = self.generate_achievements()
            certifications = self.generate_certifications()
            interests = self.generate_interests()
            languages = self.generate_languages()
            
            # Parse header content to extract components
            # For now, we'll use simple extraction
            full_name = self.resume.personal_information.name
            job_role = "SOFTWARE ENGINEER"  # This should be extracted from AI response
            personal_summary = "Experienced software engineer with expertise in modern technologies."  # This should be extracted from AI response
            
            # Combine into final template
            from template_modern_design import MODERN_DESIGN_TEMPLATE
            
            final_html = MODERN_DESIGN_TEMPLATE.replace("{{CONTACT_INFO}}", contact_info)
            final_html = final_html.replace("{{FULL_NAME}}", full_name)
            final_html = final_html.replace("{{JOB_ROLE}}", job_role)
            final_html = final_html.replace("{{PERSONAL_SUMMARY}}", personal_summary)
            final_html = final_html.replace("{{WORK_EXPERIENCE}}", work_exp)
            final_html = final_html.replace("{{EDUCATION}}", education)
            final_html = final_html.replace("{{SKILLS}}", skills)
            final_html = final_html.replace("{{PROJECTS_SECTION}}", projects)
            final_html = final_html.replace("{{ACHIEVEMENTS_SECTION}}", achievements)
            final_html = final_html.replace("{{CERTIFICATIONS_SECTION}}", certifications)
            final_html = final_html.replace("{{INTERESTS_SECTION}}", interests)
            final_html = final_html.replace("{{LANGUAGES_SECTION}}", languages)
            
            logger.info("✅ Modern Design Resume generated successfully")
            return final_html
            
        except Exception as e:
            logger.error(f"❌ Error generating Modern Design Resume: {e}")
            raise
