import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from fake_useragent import UserAgent
from typing import Dict, Any, List

def analyze_onpage(url: str) -> Dict[str, Any]:
    """
    Performs a comprehensive on-page SEO analysis of a given URL.
    """
    if not url.startswith('http'):
        url = 'https://' + url

    try:
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return {"error": f"Failed to fetch URL: {str(e)}"}

    soup = BeautifulSoup(response.content, 'lxml')
    
    result = {
        "url": url,
        "status_code": response.status_code,
        "load_time_ms": int(response.elapsed.total_seconds() * 1000),
        "meta": {},
        "headings": {},
        "content": {},
        "links": {},
        "images": {}
    }

    # Meta Tags
    title = soup.title.string if soup.title else None
    result["meta"]["title"] = {
        "content": title,
        "length": len(title) if title else 0,
        "optimal": 30 <= len(title) <= 60 if title else False
    }

    desc_tag = soup.find('meta', attrs={'name': 'description'})
    description = desc_tag['content'] if desc_tag else None
    result["meta"]["description"] = {
        "content": description,
        "length": len(description) if description else 0,
        "optimal": 120 <= len(description) <= 160 if description else False
    }

    result["meta"]["canonical"] = soup.find('link', rel='canonical')['href'] if soup.find('link', rel='canonical') else None
    result["meta"]["robots"] = soup.find('meta', attrs={'name': 'robots'})['content'] if soup.find('meta', attrs={'name': 'robots'}) else "index, follow"

    # Headings
    headings = {}
    for i in range(1, 7):
        tags = soup.find_all(f'h{i}')
        headings[f'h{i}'] = [tag.get_text(strip=True) for tag in tags]
    
    result["headings"] = {
        "counts": {k: len(v) for k, v in headings.items()},
        "h1_check": "Pass" if len(headings['h1']) == 1 else "Fail (Should have exactly one H1)",
        "structure": headings
    }

    # Content
    text = soup.get_text(separator=' ', strip=True)
    word_count = len(text.split())
    result["content"] = {
        "word_count": word_count,
        "thin_content": word_count < 300
    }

    # Links
    all_links = soup.find_all('a', href=True)
    internal_links = []
    external_links = []
    domain = urlparse(url).netloc

    for link in all_links:
        href = link['href']
        full_url = urljoin(url, href)
        parsed_href = urlparse(full_url)
        
        if parsed_href.netloc == domain:
            internal_links.append(full_url)
        else:
            external_links.append(full_url)

    result["links"] = {
        "total": len(all_links),
        "internal": len(internal_links),
        "external": len(external_links),
        "internal_sample": internal_links[:5],
        "external_sample": external_links[:5]
    }

    # Images
    images = soup.find_all('img')
    missing_alt = [img['src'] for img in images if not img.get('alt')]
    
    result["images"] = {
        "total": len(images),
        "missing_alt_count": len(missing_alt),
        "missing_alt_sample": missing_alt[:5]
    }

    return result
