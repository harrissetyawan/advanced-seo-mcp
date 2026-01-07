from fastmcp import FastMCP
from typing import Dict, Any, List, Optional
from .providers.onpage_analyzer import analyze_onpage
from .providers.technical_auditor import check_technical_health
from .providers.reporter import generate_markdown_report
from .providers.psi_analyzer import analyze_speed
from .providers.competitor_analyzer import analyze_competitors
from .providers.sitemap_auditor import audit_sitemap
from .providers.ahrefs_scraper import (
    get_backlinks_data, 
    generate_keywords, 
    get_traffic_data, 
    check_keyword_difficulty
)

mcp = FastMCP("Advanced SEO MCP")

@mcp.tool()
def generate_audit_report(url: str, include_ahrefs: bool = True) -> str:
    """
    Generates a full SEO audit report (Markdown) and saves it locally.
    Combines On-Page, Technical, Ahrefs data into a single file.
    
    Args:
        url: The URL to analyze.
        include_ahrefs: Whether to fetch backlink/traffic data using CapSolver (Default: True).
        
    Returns:
        The absolute file path of the saved report.
    """
    return generate_markdown_report(url, include_ahrefs)

@mcp.tool()
def analyze_page_speed(url: str, strategy: str = "mobile") -> Dict[str, Any]:
    """
    Analyzes site speed using Google PageSpeed Insights.
    Requires GOOGLE_PSI_API_KEY in .env.
    
    Args:
        url: URL to test.
        strategy: 'mobile' or 'desktop'.
    """
    return analyze_speed(url, strategy)

@mcp.tool()
def compare_competitors(my_domain: str, competitor_domain: str) -> Dict[str, Any]:
    """
    Compares SEO metrics (Backlinks, Traffic, DR) of two domains.
    Requires CAPSOLVER_API_KEY.
    """
    return analyze_competitors(my_domain, competitor_domain)

@mcp.tool()
def bulk_sitemap_audit(url: str, limit: int = 5) -> Dict[str, Any]:
    """
    Scans the sitemap and runs On-Page audit on multiple pages.
    Useful for finding site-wide issues (e.g., missing H1s).
    
    Args:
        url: Domain URL (e.g. 'example.com').
        limit: Max number of pages to scan (Default: 5). High numbers take time!
    """
    return audit_sitemap(url, limit)

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
