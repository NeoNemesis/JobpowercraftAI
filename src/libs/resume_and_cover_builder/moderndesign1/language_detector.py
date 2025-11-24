"""
Språkdetektering för jobbeskrivningar
Detekterar om en jobbeskrivning är på svenska eller engelska
"""

import re
from typing import Optional
from loguru import logger

class LanguageDetector:
    """
    Detekterar språk i jobbeskrivningar för att anpassa CV-innehåll
    """
    
    def __init__(self):
        # Svenska nyckelord som är vanliga i jobbeskrivningar
        self.swedish_keywords = {
            'common_words': [
                'och', 'att', 'är', 'för', 'med', 'som', 'vi', 'du', 'har', 'kan',
                'ska', 'kommer', 'vara', 'till', 'av', 'på', 'i', 'det', 'en', 'ett'
            ],
            'job_terms': [
                'arbete', 'jobb', 'tjänst', 'roll', 'position', 'anställning',
                'företag', 'organisation', 'team', 'kollegor', 'ansvar',
                'erfarenhet', 'kunskap', 'kompetens', 'utbildning', 'kvalifikationer',
                'utveckling', 'möjlighet', 'karriär', 'lön', 'förmåner'
            ],
            'tech_terms': [
                'programmering', 'utveckling', 'systemutveckling', 'webbdesign',
                'databas', 'säkerhet', 'nätverk', 'administration', 'teknisk',
                'mjukvara', 'hårdvara', 'applikation', 'system', 'plattform'
            ]
        }
        
        # Engelska nyckelord
        self.english_keywords = {
            'common_words': [
                'and', 'to', 'is', 'for', 'with', 'as', 'we', 'you', 'have', 'can',
                'will', 'be', 'of', 'in', 'the', 'a', 'an', 'that', 'this', 'or'
            ],
            'job_terms': [
                'work', 'job', 'position', 'role', 'employment', 'career',
                'company', 'organization', 'team', 'colleagues', 'responsibility',
                'experience', 'knowledge', 'skills', 'education', 'qualifications',
                'development', 'opportunity', 'salary', 'benefits', 'requirements'
            ],
            'tech_terms': [
                'programming', 'development', 'software', 'web', 'database',
                'security', 'network', 'administration', 'technical', 'system',
                'application', 'platform', 'framework', 'technology', 'coding'
            ]
        }
    
    def detect_language(self, job_description: str) -> str:
        """
        Detekterar språk i jobbeskrivning

        Args:
            job_description: Jobbeskrivningens text

        Returns:
            str: 'sv' för svenska, 'en' för engelska
        """
        if not job_description or len(job_description.strip()) < 50:
            logger.warning("⚠️ För kort jobbeskrivning för språkdetektering, använder svenska som standard")
            logger.debug(f"Jobbeskrivning längd: {len(job_description.strip()) if job_description else 0}")
            return 'sv'

        # Normalisera text
        text = job_description.lower()
        text = re.sub(r'[^\w\s]', ' ', text)  # Ta bort interpunktion
        words = text.split()

        if len(words) < 10:
            logger.warning("⚠️ För få ord för språkdetektering, använder svenska som standard")
            logger.debug(f"Antal ord: {len(words)}, Första orden: {' '.join(words[:10])}")
            return 'sv'

        # Räkna matchningar för varje språk
        swedish_score = self._calculate_language_score(words, self.swedish_keywords)
        english_score = self._calculate_language_score(words, self.english_keywords)

        # Logga resultat MED exempel på hittade ord
        logger.info(f"🔍 Språkdetektering - Svenska: {swedish_score}, Engelska: {english_score}")
        logger.debug(f"📝 Första 100 tecken av jobbeskrivning: {job_description[:100]}")

        # Bestäm språk - om poängen är lika, föredra svenska
        if swedish_score >= english_score:
            detected_language = 'sv'
            confidence = swedish_score / (swedish_score + english_score) * 100 if (swedish_score + english_score) > 0 else 50
        else:
            detected_language = 'en'
            confidence = english_score / (swedish_score + english_score) * 100

        logger.info(f"🌍 Detekterat språk: {detected_language} (säkerhet: {confidence:.1f}%)")
        return detected_language
    
    def _calculate_language_score(self, words: list, keywords: dict) -> int:
        """Beräknar språkpoäng baserat på nyckelordsmatchningar"""
        score = 0
        total_words = len(words)
        
        # Räkna matchningar i varje kategori
        for category, keyword_list in keywords.items():
            matches = sum(1 for word in words if word in keyword_list)
            
            # Vikta olika kategorier
            if category == 'common_words':
                weight = 3  # Vanliga ord är mest viktiga
            elif category == 'job_terms':
                weight = 2  # Jobbtermer är viktiga
            else:  # tech_terms
                weight = 1  # Tekniska termer är mindre viktiga
            
            score += matches * weight
        
        return score
    
    def get_language_name(self, language_code: str) -> str:
        """Returnerar språknamn från språkkod"""
        names = {
            'sv': 'Svenska',
            'en': 'English'
        }
        return names.get(language_code, 'Svenska')


def detect_job_language(job_description: Optional[str]) -> str:
    """
    Enkel funktion för att detektera jobbeskrivningens språk
    
    Args:
        job_description: Jobbeskrivningens text
        
    Returns:
        str: 'sv' för svenska, 'en' för engelska
    """
    if not job_description:
        return 'sv'
    
    detector = LanguageDetector()
    return detector.detect_language(job_description)

