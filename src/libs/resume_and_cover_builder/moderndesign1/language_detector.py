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

        # Kolla först efter svenska tecken (å, ä, ö) - stark indikator på svenska
        swedish_chars = sum(1 for c in job_description.lower() if c in 'åäö')

        # Räkna också totala tecken för att få procent
        total_chars = len(job_description)
        swedish_char_percent = (swedish_chars / total_chars * 100) if total_chars > 0 else 0

        # Om mer än 0.5% av tecknen är å, ä, ö - DEFINITIVT svenska
        if swedish_char_percent > 0.5:
            logger.info(f"🇸🇪 Hittade {swedish_chars} svenska tecken (å, ä, ö) = {swedish_char_percent:.2f}% av texten - använder svenska")
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
        logger.debug(f"📝 Första 200 tecken av jobbeskrivning: {job_description[:200]}")

        # BALANSERAD DETEKTERING:
        # Om inga svenska tecken (å, ä, ö) finns OCH engelska har fler poäng -> engelska
        # Om svenska tecken finns ELLER svenska har fler poäng -> svenska
        # Om lika: kolla procentuell skillnad (minst 20% skillnad för att vara säker)

        if swedish_chars == 0 and english_score > swedish_score:
            # Inga svenska tecken och engelska har fler poäng
            detected_language = 'en'
            confidence = english_score / (swedish_score + english_score) * 100
            logger.info(f"🌍 Detekterat språk: {detected_language} (säkerhet: {confidence:.1f}%) - Inga svenska tecken + engelska har fler poäng")
        elif swedish_score > english_score:
            # Svenska har fler poäng
            detected_language = 'sv'
            confidence = swedish_score / (swedish_score + english_score) * 100
            logger.info(f"🌍 Detekterat språk: {detected_language} (säkerhet: {confidence:.1f}%) - Svenska har fler poäng")
        else:
            # Lika eller oklart - kolla procentuell skillnad
            total_score = swedish_score + english_score
            if total_score > 0:
                sv_percent = (swedish_score / total_score) * 100
                en_percent = (english_score / total_score) * 100

                # Om engelska har minst 55% av poängen -> engelska
                if en_percent >= 55:
                    detected_language = 'en'
                    logger.info(f"🌍 Detekterat språk: {detected_language} (engelska: {en_percent:.1f}%, svenska: {sv_percent:.1f}%)")
                else:
                    # Default till svenska när det är oklart (vi är i Sverige)
                    detected_language = 'sv'
                    logger.info(f"🌍 Detekterat språk: {detected_language} (engelska: {en_percent:.1f}%, svenska: {sv_percent:.1f}%) - Default till svenska")
            else:
                detected_language = 'sv'
                logger.info(f"🌍 Detekterat språk: {detected_language} - Default (inga matchningar)")

        return detected_language
    
    def _calculate_language_score(self, words: list, keywords: dict) -> int:
        """Beräknar språkpoäng baserat på nyckelordsmatchningar"""
        score = 0
        total_words = len(words)
        matched_words = []

        # Räkna matchningar i varje kategori
        for category, keyword_list in keywords.items():
            category_matches = [word for word in words if word in keyword_list]
            matches = len(category_matches)

            # Vikta olika kategorier
            if category == 'common_words':
                weight = 3  # Vanliga ord är mest viktiga
            elif category == 'job_terms':
                weight = 2  # Jobbtermer är viktiga
            else:  # tech_terms
                weight = 1  # Tekniska termer är mindre viktiga

            score += matches * weight

            # Spara några exempel för loggning
            if category_matches:
                matched_words.extend(list(set(category_matches))[:3])  # Max 3 exempel per kategori

        # Logga exempel på matchade ord (max 10 totalt)
        if matched_words:
            logger.debug(f"   Exempel på matchade ord: {', '.join(matched_words[:10])}")

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

