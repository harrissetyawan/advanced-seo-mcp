from typing import Dict, Any, List
from .ahrefs_scraper import get_backlinks_data, get_traffic_data

def analyze_competitors(domain1: str, domain2: str) -> Dict[str, Any]:
    """
    Compares two domains using Ahrefs data (Backlinks, DR, Traffic).
    
    Args:
        domain1: Your domain.
        domain2: Competitor's domain.
        
    Returns:
        Comparison dictionary.
    """
    results = {}
    
    # Analyze Domain 1
    d1_bl = get_backlinks_data(domain1) or {}
    d1_tr = get_traffic_data(domain1) or {}
    
    # Analyze Domain 2
    d2_bl = get_backlinks_data(domain2) or {}
    d2_tr = get_traffic_data(domain2) or {}
    
    # Helper to safe get
    def get_val(data, *keys):
        curr = data
        for k in keys:
            if isinstance(curr, dict):
                curr = curr.get(k, {})
            else:
                return 0
        return curr if isinstance(curr, (int, float)) else 0

    comparison = {
        "domain_rating": {
            domain1: get_val(d1_bl, 'overview', 'domainRating'),
            domain2: get_val(d2_bl, 'overview', 'domainRating'),
            "winner": domain1 if get_val(d1_bl, 'overview', 'domainRating') > get_val(d2_bl, 'overview', 'domainRating') else domain2
        },
        "total_backlinks": {
            domain1: get_val(d1_bl, 'overview', 'backlinks'),
            domain2: get_val(d2_bl, 'overview', 'backlinks'),
            "diff": get_val(d1_bl, 'overview', 'backlinks') - get_val(d2_bl, 'overview', 'backlinks')
        },
        "monthly_traffic": {
            domain1: get_val(d1_tr, 'traffic', 'monthly'),
            domain2: get_val(d2_tr, 'traffic', 'monthly'),
            "winner": domain1 if get_val(d1_tr, 'traffic', 'monthly') > get_val(d2_tr, 'traffic', 'monthly') else domain2
        },
        "traffic_value": {
            domain1: get_val(d1_tr, 'traffic', 'value'),
            domain2: get_val(d2_tr, 'traffic', 'value'),
        }
    }
    
    return {
        "domains": [domain1, domain2],
        "comparison": comparison,
        "raw_data": {
            domain1: {"backlinks": d1_bl, "traffic": d1_tr},
            domain2: {"backlinks": d2_bl, "traffic": d2_tr}
        }
    }
