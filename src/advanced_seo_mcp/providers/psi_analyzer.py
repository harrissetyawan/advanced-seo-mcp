import requests
import os
from typing import Dict, Any, Optional

def analyze_speed(url: str, strategy: str = "mobile") -> Dict[str, Any]:
    """
    Analyzes URL performance using Google PageSpeed Insights API.
    
    Args:
        url: The URL to analyze.
        strategy: 'mobile' or 'desktop' (default: 'mobile').
        
    Returns:
        Dictionary containing Core Web Vitals and Performance Score.
    """
    api_key = os.environ.get("GOOGLE_PSI_API_KEY")
    if not api_key:
        return {"error": "GOOGLE_PSI_API_KEY is missing in .env file"}

    endpoint = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    params = {
        "url": url,
        "strategy": strategy,
        "key": api_key,
        "category": ["performance", "seo"]
    }

    try:
        resp = requests.get(endpoint, params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        
        lighthouse = data.get("lighthouseResult", {})
        audits = lighthouse.get("audits", {})
        categories = lighthouse.get("categories", {})
        
        # Helper to get numeric value safely
        def get_metric(name):
            return audits.get(name, {}).get("displayValue", "N/A")
            
        result = {
            "strategy": strategy,
            "performance_score": int(categories.get("performance", {}).get("score", 0) * 100),
            "seo_score": int(categories.get("seo", {}).get("score", 0) * 100),
            "core_web_vitals": {
                "lcp": get_metric("largest-contentful-paint"),
                "fcp": get_metric("first-contentful-paint"),
                "cls": get_metric("cumulative-layout-shift"),
                "inp": get_metric("interaction-to-next-paint") # Interaction to Next Paint
            },
            "screenshot": lighthouse.get("audits", {}).get("final-screenshot", {}).get("details", {}).get("data")
        }
        return result
        
    except Exception as e:
        return {"error": f"PageSpeed Analysis Failed: {str(e)}"}
