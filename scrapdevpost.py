import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_devpost_projects(query, pages=1):
    """
    Scrape les projets gagnants de Devpost basés sur une requête.
    """
    base_url = "https://devpost.com/software/search"
    projects_data = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    for page in range(1, pages + 1):
        params = {
            "query": f"is:winner {query}",
            "page": page
        }
        
        print(f"Scraping page {page}...")
        response = requests.get(base_url, params=params, headers=headers)
        
        if response.status_code != 200:
            print(f"Erreur lors de l'accès à la page {page}: {response.status_code}")
            break
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Trouver tous les conteneurs de projets
        # Note: Les classes peuvent varier légèrement, .gallery-item est la structure standard
        project_items = soup.select('.gallery-item')
        
        for item in project_items:
            title_tag = item.select_one('h5')
            link_tag = item.select_one('a[href*="/software/"]')
            tagline_tag = item.select_one('.tagline')
            
            if title_tag and link_tag:
                project = {
                    "title": title_tag.get_text(strip=True),
                    "url": link_tag['href'],
                    "tagline": tagline_tag.get_text(strip=True) if tagline_tag else "N/A"
                }
                projects_data.append(project)
        
        # Politesse : attendre un peu entre les requêtes
        time.sleep(2)

    return projects_data

if __name__ == "__main__":
    # Exemple : chercher des projets liés à l'IA
    search_query = "ai agents"
    results = scrape_devpost_projects(search_query, pages=1)
    
    print(f"\nTrouvé {len(results)} projets.")
    for p in results[:5]:
        print(f"- {p['title']}: {p['url']}")
        
    # Sauvegarder en JSON
    with open('devpost_projects.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    print("\nDonnées sauvegardées dans 'devpost_projects.json'")