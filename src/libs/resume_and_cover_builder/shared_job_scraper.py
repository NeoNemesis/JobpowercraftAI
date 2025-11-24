#!/usr/bin/env python3
"""
SHARED JOB SCRAPER - Gemensam jobbskrapning för alla modeller
Säkerställer konsistent jobbdata-extraktion oavsett vilken modell som används
"""

import hashlib
from pathlib import Path
from typing import Tuple, Optional
from loguru import logger

from src.utils.chrome_utils import init_browser
from src.libs.resume_and_cover_builder.llm.llm_job_parser import LLMParser
from src.job import Job
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class SharedJobScraper:
    """
    Gemensam jobbskrapning som alla modeller använder.
    Säkerställer konsistent beteende och felhantering.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.driver = None
        self.job_parser = None
        
    def scrape_job_from_url(self, job_url: str) -> Tuple[Job, str]:
        """
        Skrapar jobb från URL och returnerar Job-objekt + suggested_name
        SAMMA LOGIK SOM URSPRUNGLIG ResumeFacade.link_to_job()
        
        Args:
            job_url: URL till jobbet
            
        Returns:
            Tuple[Job, str]: (Job-objekt, suggested_name för PDF)
        """
        logger.info(f"🌐 Startar jobbskrapning från URL: {job_url}")
        
        try:
            # 1. Initiera WebDriver (SAMMA SOM URSPRUNGLIG)
            self.driver = init_browser()
            self.driver.get(job_url)
            self.driver.implicitly_wait(10)  # Samma timeout som ursprunglig
            
            # Vänta på att sidan laddas med explicit wait
            try:
                wait = WebDriverWait(self.driver, 15)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                logger.debug("Sida laddad framgångsrikt")
            except Exception as e:
                logger.warning(f"Timeout vid sidladdning, fortsätter ändå: {e}")
            
            # 2. Extrahera HTML-innehåll
            body_element = self.driver.find_element("tag name", "body")
            body_html = body_element.get_attribute("outerHTML")
            
            logger.debug(f"HTML extraherat: {len(body_html)} tecken")
            
            # 3. Använd LLMParser för att extrahera jobbinformation (SAMMA SOM URSPRUNGLIG)
            self.job_parser = LLMParser(openai_api_key=self.api_key)
            self.job_parser.set_body_html(body_html)
            
            # 4. Skapa Job-objekt (EXAKT SAMMA LOGIK SOM ResumeFacade)
            job = Job()
            job.role = self.job_parser.extract_role()
            job.company = self.job_parser.extract_company_name()
            job.description = self.job_parser.extract_job_description()
            job.location = self.job_parser.extract_location()
            job.link = job_url
            
            # 5. Generera suggested_name (SAMMA SOM URSPRUNGLIG)
            suggested_name = hashlib.md5(job_url.encode()).hexdigest()[:10]
            
            logger.info(f"✅ Jobb extraherat: {job.role} på {job.company} i {job.location}")
            logger.info(f"📄 Suggested name: {suggested_name}")
            
            return job, suggested_name
            
        except Exception as e:
            logger.error(f"❌ Fel vid jobbskrapning: {e}")
            raise
        finally:
            # Stäng WebDriver
            if self.driver:
                self.driver.quit()
                self.driver = None
    
    def validate_job_data(self, job: Job) -> bool:
        """
        Validerar att jobbdata är komplett
        
        Args:
            job: Job-objekt att validera
            
        Returns:
            bool: True om data är giltig
        """
        required_fields = ['role', 'company', 'description']
        
        for field in required_fields:
            value = getattr(job, field, None)
            if not value or value.strip() == "":
                logger.warning(f"⚠️ Saknar eller tom data för: {field}")
                return False
        
        logger.info("✅ Jobbdata validerad - alla obligatoriska fält finns")
        return True
    
    def get_job_summary(self, job: Job) -> str:
        """
        Skapar en sammanfattning av jobbdata för logging
        
        Args:
            job: Job-objekt
            
        Returns:
            str: Formaterad sammanfattning
        """
        return f"""
🎯 JOBB-SAMMANFATTNING:
   • Roll: {job.role or 'N/A'}
   • Företag: {job.company or 'N/A'}
   • Plats: {job.location or 'N/A'}
   • Beskrivning: {len(job.description)} tecken
   • URL: {job.link or 'N/A'}
"""

def create_shared_scraper(api_key: str) -> SharedJobScraper:
    """
    Factory-funktion för att skapa SharedJobScraper
    
    Args:
        api_key: OpenAI API-nyckel
        
    Returns:
        SharedJobScraper: Konfigurerad scraper-instans
    """
    return SharedJobScraper(api_key)

# Convenience-funktion för enkel användning
def scrape_job_unified(api_key: str, job_url: str) -> Tuple[Job, str]:
    """
    Enkel funktion för att skrapa jobb - kan användas av alla modeller
    
    Args:
        api_key: OpenAI API-nyckel
        job_url: URL till jobbet
        
    Returns:
        Tuple[Job, str]: (Job-objekt, suggested_name)
    """
    scraper = create_shared_scraper(api_key)
    job, suggested_name = scraper.scrape_job_from_url(job_url)
    
    # Validera data
    if not scraper.validate_job_data(job):
        logger.warning("⚠️ Jobbdata är ofullständig men fortsätter ändå")
    
    # Logga sammanfattning
    logger.info(scraper.get_job_summary(job))
    
    return job, suggested_name

if __name__ == "__main__":
    # Test av shared scraper
    print("🧪 TESTAR SHARED JOB SCRAPER")
    print("=" * 50)
    print("⚠️ Detta är en test-version. Använd med riktig API-nyckel för produktion.")
    
    # Exempel på användning
    print("\n📋 EXEMPEL PÅ ANVÄNDNING:")
    print("from src.libs.resume_and_cover_builder.shared_job_scraper import scrape_job_unified")
    print("job, suggested_name = scrape_job_unified(api_key, job_url)")
    print("print(f'Jobb: {job.role} på {job.company}')")
