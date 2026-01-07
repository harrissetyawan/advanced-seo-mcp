from fastmcp import FastMCP
from typing import Dict, Any, List, Optional
from .providers.onpage_analyzer import analyze_onpage
from .providers.technical_auditor import check_technical_health
from .providers.ahrefs_scraper import (
    get_backlinks_data, 
    generate_keywords, 
    get_traffic_data, 
    check_keyword_difficulty
)

mcp = FastMCP("Advanced SEO MCP")

@mcp.tool()
def onpage_audit(url: str) -> Dict[str, Any]:
    """
    Performs a detailed on-page SEO audit of a specific URL.
    Checks meta tags, heading structure, word count, internal/external links, and image alt tags.
    Does NOT require an API key.
    
    Args:
        url: The full URL to analyze (e.g. 'https://example.com/blog/post-1')
    """
    return analyze_onpage(url)

@mcp.tool()
def technical_health_check(url: str) -> Dict[str, Any]:
    """
    Checks technical SEO aspects of a domain/URL.
    Verifies robots.txt, sitemap.xml, and security headers (HTTPS, HSTS).
    Does NOT require an API key.
    
    Args:
        url: The domain or URL to check.
    """
    return check_technical_health(url)

@mcp.tool()
def get_backlinks(domain: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves backlink data for a domain using Ahrefs (Requires CAPSOLVER_API_KEY).
    Returns domain rating, total backlinks, and a list of top referring pages.
    
    Args:
        domain: The domain to analyze (e.g. 'example.com')
    """
    try:
        return get_backlinks_data(domain)
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def keyword_ideas(keyword: str, country: str = "us") -> Optional[List[Dict[str, Any]]]:
    """
    Generates keyword ideas and questions based on a seed keyword (Requires CAPSOLVER_API_KEY).
    
    Args:
        keyword: The seed keyword.
        country: Two-letter country code (default: 'us').
    """
    try:
        return generate_keywords(keyword, country)
    except Exception as e:
        return [{"error": str(e)}]

@mcp.tool()
def estimate_traffic(domain: str, country: str = "None") -> Optional[Dict[str, Any]]:
    """
    Estimates monthly search traffic and value for a domain (Requires CAPSOLVER_API_KEY).
    
    Args:
        domain: The domain to check.
        country: Optional country filter.
    """
    try:
        return get_traffic_data(domain, country)
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def check_difficulty(keyword: str, country: str = "us") -> Optional[Dict[str, Any]]:
    """
    Checks keyword difficulty and returns SERP analysis (Requires CAPSOLVER_API_KEY).
    
    Args:
        keyword: The keyword to analyze.
        country: Two-letter country code (default: 'us').
    """
    try:
        return check_keyword_difficulty(keyword, country)
    except Exception as e:
        return {"error": str(e)}

def main():
    mcp.run()

if __name__ == "__main__":
    main()
