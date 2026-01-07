import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import string
from typing import Dict, Any, List

def analyze_keywords(url: str, target_keyword: str = None) -> Dict[str, Any]:
    """
    Analyzes keyword density and TF-IDF like metrics.
    """
    if not url.startswith('http'):
        url = 'https://' + url
        
    try:
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        soup = BeautifulSoup(resp.content, 'lxml')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
            
        text = soup.get_text()
        
        # Normalize text
        # Remove punctuation and lowercase
        translator = str.maketrans('', '', string.punctuation)
        clean_text = text.translate(translator).lower()
        words = [w for w in clean_text.split() if len(w) > 2] # Ignore short words
        
        total_words = len(words)
        word_counts = Counter(words)
        
        top_keywords = word_counts.most_common(10)
        
        result = {
            "total_words": total_words,
            "top_keywords": [{"word": w, "count": c, "density": f"{(c/total_words)*100:.2f}%"} for w, c in top_keywords],
            "target_analysis": None
        }
        
        if target_keyword:
            target = target_keyword.lower()
            count = clean_text.count(target)
            density = (count / total_words) * 100 if total_words > 0 else 0
            
            result["target_analysis"] = {
                "keyword": target,
                "count": count,
                "density": f"{density:.2f}%",
                "recommendation": "Good" if 1 <= density <= 2.5 else ("Low" if density < 1 else "High (Spam Risk)")
            }
            
        return result
        
    except Exception as e:
        return {"error": str(e)}
