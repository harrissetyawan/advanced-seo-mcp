import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, List

def check_broken_links(url: str, limit: int = 20) -> Dict[str, Any]:
    """
    Scans a page for broken internal/external links.
    """
    if not url.startswith('http'):
        url = 'https://' + url
    
    domain = urlparse(url).netloc
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.content, 'lxml')
        links = soup.find_all('a', href=True)
        
        targets = []
        for link in links:
            href = link['href']
            full_url = urljoin(url, href)
            # Skip mailto, tel, javascript
            if full_url.startswith(('http', 'https')):
                targets.append(full_url)
        
        # Unique links, limited
        unique_targets = list(set(targets))[:limit]
        
        broken = []
        working = []
        
        def check_link(target):
            try:
                # Use HEAD request for speed
                r = requests.head(target, headers=headers, timeout=5, allow_redirects=True)
                if r.status_code >= 400:
                    return {"url": target, "status": r.status_code, "status_text": "Broken"}
                return {"url": target, "status": r.status_code, "status_text": "OK"}
            except Exception as e:
                return {"url": target, "status": 0, "status_text": str(e)}

        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(check_link, unique_targets))
            
        for res in results:
            if res['status'] >= 400 or res['status'] == 0:
                broken.append(res)
            else:
                working.append(res)
                
        return {
            "total_scanned": len(unique_targets),
            "broken_count": len(broken),
            "broken_links": broken,
            "working_count": len(working)
        }
        
    except Exception as e:
        return {"error": str(e)}
