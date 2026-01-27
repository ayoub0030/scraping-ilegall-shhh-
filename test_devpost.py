import requests
from bs4 import BeautifulSoup

def test_devpost_page():
    url = "https://devpost.com/software/search?query=is%3Awinner+ai+agents"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Check for various possible selectors
        selectors_to_test = [
            '.software-result',
            '.project-card', 
            '.gallery-item',
            '.software-list-item',
            '[class*="software"]',
            '[class*="project"]',
            'a[href*="/software/"]'
        ]
        
        for selector in selectors_to_test:
            items = soup.select(selector)
            print(f"{selector}: {len(items)} items")
            
        # Print first few links to see structure
        links = soup.select('a[href*="/software/"]')
        for i, link in enumerate(links[:3]):
            print(f"Link {i+1}: {link.get('href')} - {link.get_text(strip=True)[:50]}")
            
        # Save HTML for inspection
        with open('devpost_page.html', 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))
        print("HTML saved to devpost_page.html")
    else:
        print(f"Failed to fetch page: {response.status_code}")

if __name__ == "__main__":
    test_devpost_page()
