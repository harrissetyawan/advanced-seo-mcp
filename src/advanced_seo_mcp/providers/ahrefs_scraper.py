import requests
import json
import time
import urllib.parse
from datetime import datetime
from typing import List, Optional, Any, Dict, Tuple, cast, Literal

from ..utils.capsolver import get_capsolver_token
from ..utils.cache import save_signature, get_signature

def iso_to_timestamp(iso_date_string: str) -> float:
    """Converts an ISO 8601 date string to a unix timestamp."""
    if iso_date_string.endswith('Z'):
        iso_date_string = iso_date_string[:-1] + '+00:00'
    dt = datetime.fromisoformat(iso_date_string)
    return dt.timestamp()

# --- Backlinks Logic ---

def get_signature_and_overview(token: str, domain: str) -> Tuple[Optional[str], Optional[str], Optional[Dict[str, Any]]]:
    """
    Fetches the signed input signature and overview data from Ahrefs free tools API.
    Used internally to authenticate subsequent data requests.
    """
    url = "https://ahrefs.com/v4/stGetFreeBacklinksOverview"
    payload = {
        "captcha": token,
        "mode": "subdomains",
        "url": domain
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            return None, None, None
        
        data = response.json()
        if isinstance(data, list) and len(data) > 1:
            second_element = data[1]
            signature = second_element['signedInput']['signature']
            valid_until = second_element['signedInput']['input']['validUntil']
            overview_data = second_element['data']
            
            save_signature(domain, signature, valid_until, overview_data)
            return signature, valid_until, overview_data
    except Exception:
        pass
    return None, None, None

def get_backlinks_data(domain: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves backlink data for a domain.
    
    This function handles the entire flow:
    1. Checks local cache for a valid Ahrefs session signature.
    2. If missing or expired, solves the Turnstile CAPTCHA using CapSolver to get a new token.
    3. Fetches a new signature from Ahrefs.
    4. Requests the top backlinks list using the signature.
    
    Args:
        domain (str): The domain to analyze (e.g., "example.com").
        
    Returns:
        Optional[Dict[str, Any]]: A dictionary containing 'overview' stats (DR, total links)
        and 'backlinks' (list of top referring pages), or None if failed.
        
    Raises:
        Exception: If CAPTCHA solving fails or signature cannot be retrieved.
    """
    # Try cache first
    signature, valid_until, overview_data = get_signature(domain)
    
    # Check validity
    if signature and valid_until:
        valid_until_ts = iso_to_timestamp(valid_until)
        if time.time() > valid_until_ts:
            signature = None # Expired

    if not signature:
        site_url = f"https://ahrefs.com/backlink-checker/?input={domain}&mode=subdomains"
        token = get_capsolver_token(site_url)
        if not token:
            raise Exception(f"Failed to get verification token for domain: {domain}")
        
        signature, valid_until, overview_data = get_signature_and_overview(token, domain)
        if not signature:
            raise Exception(f"Failed to get signature for domain: {domain}")

    # Fetch List
    url = "https://ahrefs.com/v4/stGetFreeBacklinksList"
    payload = {
        "reportType": "TopBacklinks",
        "signedInput": {
            "signature": signature,
            "input": {
                "validUntil": valid_until,
                "mode": "subdomains",
                "url": f"{domain}/"
            }
        }
    }
    headers = {"Content-Type": "application/json"}
    
    resp = requests.post(url, json=payload, headers=headers)
    if resp.status_code != 200:
        return None
    
    data = resp.json()
    backlinks = []
    if data and len(data) > 1 and "topBacklinks" in data[1]:
        raw_links = data[1]["topBacklinks"].get("backlinks", [])
        for bl in raw_links:
            backlinks.append({
                "anchor": bl.get("anchor", ""),
                "domainRating": bl.get("domainRating", 0),
                "title": bl.get("title", ""),
                "urlFrom": bl.get("urlFrom", ""),
                "urlTo": bl.get("urlTo", ""),
                "edu": bl.get("edu", False),
                "gov": bl.get("gov", False),
            })

    return {
        "overview": overview_data,
        "backlinks": backlinks
    }

# --- Keywords Logic ---

def _coerce_int(value: Any) -> int:
    """Helper to parse volume numbers like '1.2k' or '5m' into integers."""
    if value is None: return 0
    if isinstance(value, (int, float)): return int(value)
    if isinstance(value, str):
        cleaned = value.replace(',', '').lower().strip()
        try:
            if cleaned.endswith('k'): return int(float(cleaned[:-1]) * 1000)
            if cleaned.endswith('m'): return int(float(cleaned[:-1]) * 1000000)
            return int(float(cleaned))
        except: return 0
    return 0

def format_keyword_ideas(keyword_data: Optional[List[Any]]) -> List[Dict[str, Any]]:
    """Formats raw Ahrefs keyword JSON into a clean list of dictionaries."""
    if not keyword_data or len(keyword_data) < 2: return []
    data = keyword_data[1]
    result = []
    
    for key in ["allIdeas", "questionIdeas"]:
        if key in data and "results" in data[key]:
            for idea in data[key]["results"]:
                result.append({
                    "type": key,
                    "keyword": idea.get('keyword', 'No keyword'),
                    "country": idea.get('country', '-'),
                    "difficulty": idea.get('difficultyLabel'), # Keep original label for now
                    "volume": _coerce_int(idea.get('volumeLabel')),
                    "updatedAt": idea.get('updatedAt', '-')
                })
    return result

def generate_keywords(keyword: str, country: str = "us", search_engine: str = "Google") -> Optional[List[Dict[str, Any]]]:
    """
    Generates keyword ideas and questions for a seed keyword.
    
    Args:
        keyword (str): The seed keyword (e.g. "seo tools").
        country (str): 2-letter country code (default: "us").
        search_engine (str): Search engine context (default: "Google").
        
    Returns:
        Optional[List[Dict[str, Any]]]: A list of keyword objects containing volume, difficulty, etc.
    """
    site_url = f"https://ahrefs.com/keyword-generator/?country={country}&input={urllib.parse.quote(keyword)}"
    token = get_capsolver_token(site_url)
    if not token:
        raise Exception("Failed to get captcha token")
        
    url = "https://ahrefs.com/v4/stGetFreeKeywordIdeas"
    payload = {
        "withQuestionIdeas": True,
        "captcha": token,
        "searchEngine": search_engine,
        "country": country,
        "keyword": ["Some", keyword]
    }
    
    resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
    if resp.status_code != 200: return None
    return format_keyword_ideas(resp.json())

# --- Traffic Logic ---

def get_traffic_data(domain_or_url: str, country: str = "None", mode: str = "subdomains") -> Optional[Dict[str, Any]]:
    """
    Estimates monthly organic search traffic and traffic value.
    
    Args:
        domain_or_url (str): Domain to check.
        country (str): Country code filter (or "None" for global).
        mode (str): "subdomains", "exact", or "prefix".
        
    Returns:
        Optional[Dict[str, Any]]: Traffic stats and top performing pages.
    """
    site_url = f"https://ahrefs.com/traffic-checker/?input={domain_or_url}&mode={mode}"
    token = get_capsolver_token(site_url)
    if not token: raise Exception("Failed to get captcha token")

    url = "https://ahrefs.com/v4/stGetFreeTrafficOverview"
    params = {
        "input": json.dumps({
            "captcha": token,
            "country": country,
            "protocol": "None",
            "mode": mode,
            "url": domain_or_url
        })
    }
    headers = {
        "accept": "*/*", 
        "content-type": "application/json",
        "referer": site_url
    }
    
    resp = requests.get(url, params=params, headers=headers)
    if resp.status_code != 200: return None
    
    data = resp.json()
    if isinstance(data, list) and len(data) > 1:
        traffic_data = data[1]
        return {
            "traffic": {
                "monthly": traffic_data.get("traffic", {}).get("trafficMonthlyAvg", 0),
                "value": traffic_data.get("traffic", {}).get("costMontlyAvg", 0)
            },
            "top_pages": traffic_data.get("top_pages", []),
            "top_countries": traffic_data.get("top_countries", [])
        }
    return None

# --- Keyword Difficulty Logic ---

def check_keyword_difficulty(keyword: str, country: str = "us") -> Optional[Dict[str, Any]]:
    """
    Checks the Keyword Difficulty (KD) score and SERP analysis.
    
    Args:
        keyword (str): The keyword to analyze.
        country (str): 2-letter country code (default: "us").
        
    Returns:
        Optional[Dict[str, Any]]: Object containing 'difficulty' score (0-100) and 'serp' results.
    """
    site_url = f"https://ahrefs.com/keyword-difficulty/?country={country}&input={urllib.parse.quote(keyword)}"
    token = get_capsolver_token(site_url)
    if not token: raise Exception("Failed to get captcha token")

    url = "https://ahrefs.com/v4/stGetFreeSerpOverviewForKeywordDifficultyChecker"
    payload = {
        "captcha": token,
        "country": country,
        "keyword": keyword
    }
    headers = {
        "accept": "*/*",
        "content-type": "application/json; charset=utf-8",
        "referer": site_url
    }
    
    resp = requests.post(url, json=payload, headers=headers)
    if resp.status_code != 200: return None
    
    data = resp.json()
    if isinstance(data, list) and len(data) > 1:
        kd_data = data[1]
        return {
            "difficulty": kd_data.get("difficulty", 0),
            "serp": kd_data.get("serp", {}).get("results", [])
        }
    return None