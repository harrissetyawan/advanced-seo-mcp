import requests
from urllib.parse import urlparse, urljoin
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from .onpage_analyzer import analyze_onpage

def fetch_sitemap_urls(domain_url: str) -> List[str]:
    """Finds sitemap and extracts URLs."""
    if not domain_url.startswith('http'):
        domain_url = 'https://' + domain_url
        
    base = f"{urlparse(domain_url).scheme}://{urlparse(domain_url).netloc}"
    candidates = ['/sitemap.xml', '/sitemap_index.xml', '/wp-sitemap.xml']
    
    sitemap_content = None
    
    for path in candidates:
        try:
            resp = requests.get(urljoin(base, path), timeout=10)
            if resp.status_code == 200:
                sitemap_content = resp.content
                break
        except: pass
        
    if not sitemap_content:
        return []

    try:
        root = ET.fromstring(sitemap_content)
        # Handle namespaces if present (e.g. {http://www.sitemaps.org/schemas/sitemap/0.9}url)
        urls = []
        for child in root:
            # Very basic XML parsing, works for standard sitemaps
            for sub in child:
                if 'loc' in sub.tag:
                    urls.append(sub.text)
            if 'loc' in child.tag: # for urlset/url structure
                 urls.append(child.text)
                 
        # Filter None and duplicates
        return list(set([u for u in urls if u]))
    except:
        return []

def audit_sitemap(url: str, limit: int = 5) -> Dict[str, Any]:
    """
    Fetches sitemap and runs On-Page audit on first N URLs.
    
    Args:
        url: Domain URL.
        limit: Max pages to analyze (default 5 to prevent overload).
        
    Returns:
        Summary of audits.
    """
    urls = fetch_sitemap_urls(url)
    if not urls:
        return {"error": "No sitemap found or empty sitemap."}
    
    selected_urls = urls[:limit]
    results = []
    
    issues = {
        "missing_h1": [],
        "missing_meta_desc": [],
        "thin_content": [],
        "slow_pages": [] # > 2s load time
    }
    
    for page_url in selected_urls:
        data = analyze_onpage(page_url)
        results.append(data)
        
        # Aggregate Issues
        if "error" not in data:
            if data['headings']['counts']['h1'] == 0:
                issues['missing_h1'].append(page_url)
            
            if not data['meta']['description']['content']:
                issues['missing_meta_desc'].append(page_url)
                
            if data['content']['thin_content']:
                issues['thin_content'].append(page_url)
                
            if data['load_time_ms'] > 2000:
                issues['slow_pages'].append(page_url)

    return {
        "total_scanned": len(selected_urls),
        "total_in_sitemap": len(urls),
        "issues_summary": {k: len(v) for k, v in issues.items()},
        "issue_details": issues,
        "raw_results": results
    }
