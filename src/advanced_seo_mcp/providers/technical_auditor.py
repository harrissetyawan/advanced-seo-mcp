import requests
from urllib.parse import urlparse, urljoin
from fake_useragent import UserAgent
from typing import Dict, Any

def check_technical_health(url: str) -> Dict[str, Any]:
    """
    Performs a technical SEO audit of a given domain or URL.
    
    This function checks for the existence of critical technical SEO files
    and security headers. Specifically, it validates:
    
    1. **robots.txt**: Checks if it exists and returns the file size.
    2. **sitemap.xml**: Scans common paths (e.g., /sitemap.xml, /sitemap_index.xml) 
       to find a valid sitemap.
    3. **Security Headers**:
        - Checks for HTTPS enforcement.
        - Checks for HSTS (Strict-Transport-Security).
        - Checks for Clickjacking protection (X-Frame-Options).
        - Checks for MIME-type sniffing protection (X-Content-Type-Options).

    Args:
        url (str): The URL or domain to audit (e.g., "https://example.com" or "example.com").

    Returns:
        Dict[str, Any]: A dictionary containing the results of the audit:
            {
                "url": str,
                "robots_txt": {"exists": bool, "url": str, "size": int},
                "sitemap": {"found": bool, "url": str},
                "security": {
                    "https": bool,
                    "hsts": bool,
                    "x_frame_options": str,
                    "x_content_type_options": str
                }
            }
    """
    if not url.startswith('http'):
        url = 'https://' + url
    
    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    
    result = {
        "url": url,
        "robots_txt": {},
        "sitemap": {},
        "security": {}
    }

    # Check robots.txt
    robots_url = urljoin(base_url, '/robots.txt')
    try:
        r_resp = requests.get(robots_url, headers=headers, timeout=5)
        result["robots_txt"] = {
            "exists": r_resp.status_code == 200,
            "url": robots_url,
            "size": len(r_resp.content) if r_resp.status_code == 200 else 0
        }
    except:
        result["robots_txt"] = {"exists": False, "error": "Request failed"}

    # Check sitemap.xml
    # Common locations to check
    sitemap_candidates = ['/sitemap.xml', '/sitemap_index.xml', '/wp-sitemap.xml']
    found_sitemap = None
    
    for path in sitemap_candidates:
        sitemap_url = urljoin(base_url, path)
        try:
            s_resp = requests.head(sitemap_url, headers=headers, timeout=5)
            if s_resp.status_code == 200:
                found_sitemap = sitemap_url
                break
        except:
            continue
            
    result["sitemap"] = {
        "found": found_sitemap is not None,
        "url": found_sitemap if found_sitemap else "Not found in common locations"
    }

    # Security Headers
    try:
        resp = requests.head(url, headers=headers, timeout=5)
        sec_headers = resp.headers
        result["security"] = {
            "https": parsed.scheme == 'https',
            "hsts": 'Strict-Transport-Security' in sec_headers,
            "x_frame_options": sec_headers.get('X-Frame-Options', 'Missing'),
            "x_content_type_options": sec_headers.get('X-Content-Type-Options', 'Missing')
        }
    except:
        result["security"] = {"error": "Could not fetch headers"}

    return result