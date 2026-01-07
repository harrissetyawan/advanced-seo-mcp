import json
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from typing import Dict, Any, List

def validate_schema(url: str) -> Dict[str, Any]:
    """
    Extracts and validates JSON-LD Schema Markup from a URL.
    """
    if not url.startswith('http'):
        url = 'https://' + url
        
    try:
        ua = UserAgent()
        resp = requests.get(url, headers={'User-Agent': ua.random}, timeout=10)
        soup = BeautifulSoup(resp.content, 'lxml')
        
        schemas = soup.find_all('script', type='application/ld+json')
        results = []
        
        for script in schemas:
            try:
                # Remove comments or CDATA if present
                content = script.string if script.string else script.text
                data = json.loads(content)
                results.append({
                    "valid": True,
                    "type": data.get('@type', 'Unknown'),
                    "context": data.get('@context', 'Unknown'),
                    "raw": data
                })
            except json.JSONDecodeError as e:
                results.append({
                    "valid": False,
                    "error": f"JSON Decode Error: {str(e)}",
                    "content_snippet": content[:50] + "..." if content else "Empty"
                })
                
        return {
            "found_count": len(schemas),
            "schemas": results,
            "has_valid_schema": any(s['valid'] for s in results)
        }
    except Exception as e:
        return {"error": str(e)}
