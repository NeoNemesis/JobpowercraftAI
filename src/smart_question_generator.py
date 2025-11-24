"""
Smart Question Generator
Analyserar jobbeskrivning och genererar relevanta frågor för CV-anpassning
"""

import openai
from typing import List, Dict, Optional
from loguru import logger
import json


class SmartQuestionGenerator:
    """Genererar relevanta frågor baserat på jobbeskrivning"""

    def __init__(self, api_key: str):
        """Initialisera med OpenAI API-nyckel"""
        self.api_key = api_key
        openai.api_key = api_key

    def analyze_job_and_generate_questions(
        self,
        job_description: str,
        resume_data: Dict,
        max_questions: int = 5
    ) -> List[Dict]:
        """
        Analysera jobbeskrivning och generera relevanta frågor

        Args:
            job_description: Jobbeskrivningens text
            resume_data: Befintlig CV-data från plain_text_resume.yaml
            max_questions: Max antal frågor (default: 5)

        Returns:
            Lista med frågor och metadata
        """

        # Extrahera kandidatens erfarenheter för kontext
        experiences = self._extract_experience_summary(resume_data)

        prompt = f"""You are an expert CV writer and recruiter. Analyze this job description and generate {max_questions} HIGHLY RELEVANT questions to ask the candidate.

The questions should help TAILOR the CV to THIS SPECIFIC JOB by gathering concrete metrics and details.

JOB DESCRIPTION:
{job_description[:1500]}

CANDIDATE'S BACKGROUND:
{experiences}

INSTRUCTIONS:
1. Analyze what THIS job emphasizes (technical skills? leadership? specific technologies?)
2. Generate {max_questions} questions that will help quantify the candidate's relevant experience
3. Questions should be SPECIFIC to this job (not generic)
4. Focus on metrics that matter for THIS role
5. Questions should be answerable with numbers or concrete examples

QUESTION TYPES TO CONSIDER:
- If job mentions specific technology → Ask about experience with that technology
- If job emphasizes leadership → Ask about team size, projects led, outcomes
- If job requires certifications → Ask if candidate has them
- If job mentions metrics/KPIs → Ask for candidate's relevant metrics
- If job requires industry experience → Ask about relevant projects

OUTPUT FORMAT (JSON):
{{
  "job_focus": "Brief analysis of what this job emphasizes (2-3 keywords)",
  "questions": [
    {{
      "question": "The question in Swedish",
      "context": "Why this question is relevant to this job",
      "metric_type": "number|percentage|list|text",
      "example_answer": "Example of a good answer"
    }}
  ]
}}

Generate the questions:"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at analyzing job descriptions and generating relevant questions to tailor CVs. Always output valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.5,
                max_tokens=1200,
                response_format={"type": "json_object"}
            )

            result = response.choices[0].message.content
            data = json.loads(result)

            logger.info(f"✅ Genererade {len(data.get('questions', []))} frågor")
            logger.info(f"🎯 Jobbfokus: {data.get('job_focus', 'Okänd')}")

            return data

        except Exception as e:
            logger.error(f"❌ Fel vid frågegenerering: {e}")
            # Fallback till generiska frågor
            return self._get_fallback_questions()

    def _extract_experience_summary(self, resume_data: Dict) -> str:
        """Extrahera en kort sammanfattning av kandidatens erfarenhet"""

        summary_parts = []

        # Positioner
        experiences = resume_data.get('experience_details', [])
        if experiences:
            positions = [exp.get('position', '') for exp in experiences[:3]]
            summary_parts.append(f"Positioner: {', '.join(positions)}")

        # Skills
        all_skills = set()
        for exp in experiences:
            skills = exp.get('skills_acquired', [])
            all_skills.update(skills[:5])

        if all_skills:
            summary_parts.append(f"Skills: {', '.join(list(all_skills)[:10])}")

        return " | ".join(summary_parts) if summary_parts else "Ingen tidigare erfarenhet angiven"

    def _get_fallback_questions(self) -> Dict:
        """Fallback-frågor om AI misslyckas"""
        return {
            "job_focus": "Generell",
            "questions": [
                {
                    "question": "Hur många projekt har du arbetat med som är relevanta för denna roll?",
                    "context": "För att kvantifiera erfarenhet",
                    "metric_type": "number",
                    "example_answer": "5"
                },
                {
                    "question": "Vilka konkreta resultat uppnådde du i dina projekt? (t.ex. %, antal användare)",
                    "context": "För att visa impact",
                    "metric_type": "text",
                    "example_answer": "Ökade effektivitet med 30%"
                },
                {
                    "question": "Har du arbetat i team? Hur stor var teamet?",
                    "context": "För att visa samarbetsförmåga",
                    "metric_type": "number",
                    "example_answer": "3-5"
                }
            ]
        }

    def ask_questions_interactive(self, questions_data: Dict) -> Dict:
        """
        Ställ frågor interaktivt till användaren

        Args:
            questions_data: Data från analyze_job_and_generate_questions

        Returns:
            Dictionary med svar
        """

        print("\n" + "="*80)
        print("🎯 JOBBANPASSADE FRÅGOR")
        print("="*80)
        print(f"Detta jobb fokuserar på: {questions_data.get('job_focus', 'Okänd')}")
        print("\n💡 Svara på frågorna för att anpassa ditt CV till detta jobb.")
        print("💡 Tryck Enter för att hoppa över en fråga.\n")
        print("="*80 + "\n")

        answers = {}

        for i, q_data in enumerate(questions_data.get('questions', []), 1):
            question = q_data['question']
            context = q_data.get('context', '')
            example = q_data.get('example_answer', '')

            print(f"❓ FRÅGA {i}/{len(questions_data['questions'])}:")
            print(f"   {question}")

            if context:
                print(f"   💡 Varför: {context}")

            if example:
                print(f"   📝 Exempel: {example}")

            answer = input("\n   → Ditt svar: ").strip()

            if answer:
                answers[f"question_{i}"] = {
                    "question": question,
                    "answer": answer,
                    "metric_type": q_data.get('metric_type', 'text')
                }
                print("   ✅ Sparat!\n")
            else:
                print("   ⏭️  Hoppade över\n")

            print("-" * 80 + "\n")

        print("="*80)
        print(f"✅ Samlade in {len(answers)} svar!")
        print("="*80 + "\n")

        return answers


def analyze_and_ask_for_job(
    job_description: str,
    resume_data: Dict,
    api_key: str
) -> Dict:
    """
    Huvudfunktion: Analysera jobb och ställ frågor

    Args:
        job_description: Jobbeskrivning
        resume_data: CV-data från YAML
        api_key: OpenAI API-nyckel

    Returns:
        Dictionary med svar
    """

    generator = SmartQuestionGenerator(api_key)

    # 1. Analysera och generera frågor
    print("\n🔍 Analyserar jobbeskrivning...")
    questions_data = generator.analyze_job_and_generate_questions(
        job_description,
        resume_data,
        max_questions=5
    )

    # 2. Ställ frågor
    answers = generator.ask_questions_interactive(questions_data)

    # 3. Returnera både frågor och svar för CV-generering
    return {
        "job_focus": questions_data.get('job_focus', ''),
        "questions": questions_data.get('questions', []),
        "answers": answers
    }


if __name__ == "__main__":
    # Test
    import yaml
    from pathlib import Path

    # Läs API-nyckel
    secrets_path = Path("data_folder/secrets.yaml")
    with open(secrets_path, 'r') as f:
        secrets = yaml.safe_load(f)
        api_key = secrets.get('llm_api_key')

    # Läs CV
    resume_path = Path("data_folder/plain_text_resume.yaml")
    with open(resume_path, 'r') as f:
        resume_data = yaml.safe_load(f)

    # Test med exempel-jobb
    test_job = """
    Vi söker en erfaren Python Developer för att bygga AI-drivna lösningar.

    Krav:
    - 3+ års erfarenhet av Python
    - Erfarenhet av Django eller Flask
    - Kunskap om databaser (PostgreSQL, MongoDB)
    - Har arbetat med RESTful APIs

    Meriterande:
    - Machine Learning erfarenhet
    - Docker/Kubernetes
    """

    result = analyze_and_ask_for_job(test_job, resume_data, api_key)

    print("\n📊 RESULTAT:")
    print(f"Jobbfokus: {result['job_focus']}")
    print(f"Antal svar: {len(result['answers'])}")
