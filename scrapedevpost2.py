import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_devpost_projects(query, max_pages=100):
    base_url = "https://devpost.com/software/search"
    projects_data = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    for page in range(1, max_pages + 1):
        params = {
            "query": f"is:winner {query}".strip(),
            "page": page
        }
        
        print(f"Scraping page {page}...")
        response = requests.get(base_url, params=params, headers=headers)
        
        if response.status_code != 200:
            print(f"Error accessing page {page}: {response.status_code}")
            break
            
        # Check if response is JSON
        if 'application/json' in response.headers.get('content-type', ''):
            data = response.json()
            software_list = data.get('software', [])
            
            if not software_list:  # No more results
                print(f"No more projects found on page {page}")
                break
                
            page_projects = 0
            for item in software_list:
                if item.get('winner', False):  # Only include winners
                    project = {
                        "title": item.get('name', 'N/A'),
                        "url": item.get('url', 'N/A'),
                        "tagline": item.get('tagline', 'N/A'),
                        "tags": item.get('tags', []),
                        "like_count": item.get('like_count', 0),
                        "comment_count": item.get('comment_count', 0)
                    }
                    projects_data.append(project)
                    page_projects += 1
            
            print(f"Found {page_projects} winner projects on page {page}")
            if page_projects == 0:  # No winners on this page
                break
        else:
            # Fallback to HTML parsing (original method)
            soup = BeautifulSoup(response.content, 'html.parser')
            project_items = soup.select('.software-result, .project-card')

            if not project_items:  # No more results
                break

            for item in project_items:
                title_tag = item.select_one('h5, h3')
                link_tag = item.select_one('a[href*="/software/"]')
                tagline_tag = item.select_one('.tagline')

                if title_tag and link_tag:
                    url = link_tag['href']
                    if url.startswith("/"):
                        url = f"https://devpost.com{url}"
                    project = {
                        "title": title_tag.get_text(strip=True),
                        "url": url,
                        "tagline": tagline_tag.get_text(strip=True) if tagline_tag else "N/A"
                    }
                    projects_data.append(project)
        
        time.sleep(0.5)  # Further reduced delay

    return projects_data

if __name__ == "__main__":
    # Try different search strategies
    search_queries = [
        "ai", 
        "machine learning", 
        "artificial intelligence",
        "chatbot",
        "automation",
        "bot"
    ]
    
    all_results = []
    
    for query in search_queries:
        print(f"\n=== Searching for: {query} ===")
        results = scrape_devpost_projects(query)
        print(f"Found {len(results)} projects for '{query}'")
        all_results.extend(results)
        
        # Remove duplicates based on URL
        seen_urls = set()
        unique_results = []
        for project in all_results:
            if project['url'] not in seen_urls:
                seen_urls.add(project['url'])
                unique_results.append(project)
        
        all_results = unique_results
        print(f"Total unique projects so far: {len(all_results)}")
    
    print(f"\n=== FINAL RESULTS ===")
    print(f"Total unique projects found: {len(all_results)}")
    
    # Filter for AI agents
    ai_agent_keywords = ['agent', 'agents', 'autonomous', 'assistant', 'chatbot', 'bot']
    ai_agent_projects = []
    
    for project in all_results:
        title_lower = project['title'].lower()
        tagline_lower = project['tagline'].lower()
        
        if any(keyword in title_lower or keyword in tagline_lower 
               for keyword in ai_agent_keywords):
            ai_agent_projects.append(project)
    
    print(f"AI agent projects: {len(ai_agent_projects)}")
    
    # Save both datasets
    with open('all_projects_comprehensive.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=4, ensure_ascii=False)
    
    with open('ai_agents_comprehensive.json', 'w', encoding='utf-8') as f:
        json.dump(ai_agent_projects, f, indent=4, ensure_ascii=False)
    
    print(f"Saved {len(all_results)} total projects to 'all_projects_comprehensive.json'")
    print(f"Saved {len(ai_agent_projects)} AI agent projects to 'ai_agents_comprehensive.json'")
