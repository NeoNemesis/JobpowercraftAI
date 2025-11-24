"""
GitHub Repository Analyzer
Hämtar och analyserar GitHub-repositories för att generera en sammanfattning av tekniker och projekt.
"""

import requests
from typing import Dict, List, Optional
from loguru import logger
from collections import Counter


class GitHubAnalyzer:
    """Analyserar GitHub-repositories och genererar teknologisammanfattning"""

    def __init__(self, github_username: str, github_token: Optional[str] = None):
        """
        Initialisera GitHub Analyzer

        Args:
            github_username: GitHub användarnamn
            github_token: GitHub Personal Access Token (valfritt, men rekommenderat för högre rate limits)
        """
        self.username = github_username
        self.token = github_token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if github_token:
            self.headers["Authorization"] = f"token {github_token}"

    def get_repositories(self, max_repos: int = 50) -> List[Dict]:
        """
        Hämta användarens repositories

        Args:
            max_repos: Maximalt antal repositories att hämta

        Returns:
            List av repository-dictionaries
        """
        try:
            url = f"{self.base_url}/users/{self.username}/repos"
            params = {
                "per_page": max_repos,
                "sort": "updated",
                "direction": "desc"
            }

            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()

            repos = response.json()
            logger.info(f"✅ Hämtade {len(repos)} repositories från GitHub")
            return repos

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Fel vid hämtning av repositories: {e}")
            return []

    def get_repository_languages(self, repo_name: str) -> Dict[str, int]:
        """
        Hämta programmeringsspråk för ett specifikt repository

        Args:
            repo_name: Repository-namnet

        Returns:
            Dictionary med språk och antal bytes
        """
        try:
            url = f"{self.base_url}/repos/{self.username}/{repo_name}/languages"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Fel vid hämtning av språk för {repo_name}: {e}")
            return {}

    def analyze_all_repositories(self) -> Dict:
        """
        Analysera alla repositories och sammanfatta teknologier

        Returns:
            Dictionary med sammanfattning av teknologier och projekt
        """
        repos = self.get_repositories()

        if not repos:
            logger.warning("⚠️ Inga repositories hittades")
            return {
                "total_repos": 0,
                "languages": {},
                "technologies": [],
                "project_summary": ""
            }

        # Samla alla språk
        all_languages = Counter()
        technologies = set()
        project_descriptions = []

        for repo in repos:
            # Hämta språk för varje repo
            languages = self.get_repository_languages(repo['name'])
            all_languages.update(languages)

            # Samla projektbeskrivningar
            if repo.get('description'):
                project_descriptions.append({
                    'name': repo['name'],
                    'description': repo['description'],
                    'stars': repo.get('stargazers_count', 0),
                    'url': repo.get('html_url', '')
                })

            # Identifiera teknologier från repo-namn och beskrivning
            repo_text = f"{repo['name']} {repo.get('description', '')}".lower()

            # Vanliga teknologier att leta efter
            tech_keywords = {
                'react': 'React',
                'vue': 'Vue.js',
                'angular': 'Angular',
                'node': 'Node.js',
                'express': 'Express.js',
                'django': 'Django',
                'flask': 'Flask',
                'spring': 'Spring Boot',
                'docker': 'Docker',
                'kubernetes': 'Kubernetes',
                'aws': 'AWS',
                'azure': 'Azure',
                'mongodb': 'MongoDB',
                'postgresql': 'PostgreSQL',
                'mysql': 'MySQL',
                'redis': 'Redis',
                'api': 'REST API',
                'graphql': 'GraphQL',
                'tensorflow': 'TensorFlow',
                'pytorch': 'PyTorch',
                'ai': 'AI/ML',
                'machine learning': 'Machine Learning',
                'deep learning': 'Deep Learning',
            }

            for keyword, tech_name in tech_keywords.items():
                if keyword in repo_text:
                    technologies.add(tech_name)

        # Sortera språk efter användning
        sorted_languages = dict(sorted(all_languages.items(), key=lambda x: x[1], reverse=True))

        # Skapa sammanfattning
        top_projects = sorted(project_descriptions, key=lambda x: x['stars'], reverse=True)[:5]

        summary = self._generate_summary(repos, sorted_languages, technologies, top_projects)

        return {
            "total_repos": len(repos),
            "languages": sorted_languages,
            "technologies": sorted(list(technologies)),
            "top_projects": top_projects,
            "project_summary": summary
        }

    def _generate_summary(self, repos: List, languages: Dict, technologies: set, top_projects: List) -> str:
        """Generera en kort sammanfattning av GitHub-aktivitet"""

        # Räkna huvudspråk
        if languages:
            top_language = list(languages.keys())[0]
            lang_list = ", ".join(list(languages.keys())[:5])
        else:
            top_language = "Python"
            lang_list = "Python, JavaScript"

        summary_parts = []

        # Huvudtext
        summary_parts.append(f"Aktiv GitHub-utvecklare med {len(repos)} publika repositories.")
        summary_parts.append(f"Primära programmeringsspråk: {lang_list}.")

        # Teknologier
        if technologies:
            tech_list = ", ".join(sorted(list(technologies))[:6])
            summary_parts.append(f"Erfarenhet av teknologier som {tech_list}.")

        # Topp-projekt
        if top_projects:
            summary_parts.append(f"Noterbara projekt inkluderar {top_projects[0]['name']} ({top_projects[0]['description']}).")

        return " ".join(summary_parts)

    def get_formatted_skills_summary(self) -> str:
        """
        Returnera en formaterad lista av färdigheter från GitHub

        Returns:
            Formaterad sträng med färdigheter
        """
        analysis = self.analyze_all_repositories()

        skills = []

        # Lägg till språk
        for lang in list(analysis['languages'].keys())[:10]:
            skills.append(lang)

        # Lägg till teknologier
        skills.extend(analysis['technologies'])

        return ", ".join(sorted(set(skills)))


def analyze_github_profile(github_url: str, github_token: Optional[str] = None) -> Dict:
    """
    Analysera en GitHub-profil från URL

    Args:
        github_url: GitHub profil-URL (t.ex. https://github.com/NeoNemesis)
        github_token: GitHub Personal Access Token (valfritt)

    Returns:
        Dictionary med analys-resultat
    """
    # Extrahera användarnamn från URL
    username = github_url.rstrip('/').split('/')[-1]

    analyzer = GitHubAnalyzer(username, github_token)
    return analyzer.analyze_all_repositories()


if __name__ == "__main__":
    # Test
    result = analyze_github_profile("https://github.com/NeoNemesis")
    print(f"Total repositories: {result['total_repos']}")
    print(f"Languages: {list(result['languages'].keys())[:5]}")
    print(f"Technologies: {result['technologies'][:5]}")
    print(f"\nSummary:\n{result['project_summary']}")
