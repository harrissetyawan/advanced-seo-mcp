import os
from datetime import datetime
from typing import Dict, Any
from pathlib import Path
from .onpage_analyzer import analyze_onpage
from .technical_auditor import check_technical_health
from .ahrefs_scraper import get_backlinks_data, get_traffic_data
from .schema_validator import validate_schema
from .link_inspector import check_broken_links
from .content_analyzer import analyze_keywords
from .psi_analyzer import analyze_speed

def generate_markdown_report(url: str, include_ahrefs: bool = True) -> str:
    """
    Runs all analysis tools for a URL and saves a formatted Markdown report.
    Returns the file path of the generated report.
    """
    domain = url.replace('https://', '').replace('http://', '').strip('/')
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_filename = f"seo_report_{domain.replace('.', '_')}_{timestamp}.md"
    
    # Ensure reports directory exists
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    file_path = report_dir / report_filename

    # 1. Run Analyses
    print(f"🔍 Analyzing On-Page SEO for {url}...")
    onpage = analyze_onpage(url)
    
    print(f"🛠️ Checking Technical Health...")
    tech = check_technical_health(url)
    
    print(f"🧩 Validating Schema Markup...")
    schema = validate_schema(url)
    
    print(f"🔗 Inspecting Links (Broken Checker)...")
    links = check_broken_links(url, limit=20)
    
    print(f"📝 Analyzing Content & Keywords...")
    content_analysis = analyze_keywords(url)
    
    print(f"🚀 Measuring Page Speed (PSI)...")
    speed = analyze_speed(url, strategy='mobile')
    
    ahrefs = None
    traffic = None
    if include_ahrefs:
        try:
            print(f"🔗 Fetching Backlinks via CapSolver...")
            ahrefs = get_backlinks_data(domain)
            print(f"📈 Estimating Traffic...")
            traffic = get_traffic_data(domain)
        except Exception as e:
            print(f"⚠️ Ahrefs data skipped: {e}")

    # 2. Build Markdown Content
    md_parts = []
    md_parts.append(f"# SEO Audit Report: {domain}")
    md_parts.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    md_parts.append(f"**URL:** {url}\n")

    # Executive Summary
    md_parts.append("## 📋 Executive Summary")
    md_parts.append(f"- **HTTP Status:** {onpage.get('status_code')}")
    
    load_time = onpage.get('load_time_ms', 0)
    md_parts.append(f"- **Load Time:** {load_time}ms")
    
    if "error" not in speed:
        md_parts.append(f"- **Mobile Performance:** {speed.get('performance_score')}/100")
        lcp = speed.get('core_web_vitals', {}).get('lcp', 'N/A')
        cls = speed.get('core_web_vitals', {}).get('cls', 'N/A')
        md_parts.append(f"- **Core Web Vitals:** LCP: {lcp}, CLS: {cls}")
    
    if ahrefs and ahrefs.get('overview'):
        md_parts.append(f"- **Domain Rating (DR):** {ahrefs['overview'].get('domainRating', 'N/A')}")
    if traffic and traffic.get('traffic'):
        md_parts.append(f"- **Est. Monthly Traffic:** {traffic['traffic'].get('monthly', 0)}")

    # On-Page
    md_parts.append("\n## 🔍 On-Page SEO Analysis")
    meta = onpage.get('meta', {})
    md_parts.append("### Meta Tags")
    md_parts.append(f"- **Title:** `{meta.get('title', {}).get('content', 'MISSING')}`")
    md_parts.append(f"- **Description:** `{meta.get('description', {}).get('content', 'MISSING')}`")
    
    # Content & Keywords
    md_parts.append("\n### 📝 Content & Keywords")
    md_parts.append(f"- **Total Words:** {content_analysis.get('total_words', 0)}\n")
    
    md_parts.append("| Keyword | Count | Density |")
    md_parts.append("|---|---|---|")
    for kw in content_analysis.get('top_keywords', []):
        md_parts.append(f"| {kw['word']} | {kw['count']} | {kw['density']} |")

    # Schema
    md_parts.append("\n## 🧩 Schema Markup")
    if schema.get('has_valid_schema'):
        md_parts.append("✅ **Valid Schema Found**")
        for s in schema.get('schemas', []):
            if s['valid']:
                md_parts.append(f"- Type: `{s.get('type')}`")
    else:
        md_parts.append("❌ **No Valid Schema Found**")

    # Broken Links
    md_parts.append("\n## 🔗 Link Health (Sample 20)")
    md_parts.append(f"- **Scanned:** {links.get('total_scanned')}")
    md_parts.append(f"- **Broken:** {links.get('broken_count')}")
    if links.get('broken_links'):
        md_parts.append("\n**Broken Links Found:**")
        for l in links['broken_links']:
            md_parts.append(f"- `[{l['status']}]` {l['url']}")
    else:
        md_parts.append("✅ No broken links found in sample.")

    # Technical
    md_parts.append("\n## 🛠️ Technical Health")
    exists_robots = '✅ Found' if tech['robots_txt'].get('exists') else '❌ Missing'
    md_parts.append(f"- **Robots.txt:** {exists_robots}")
    
    exists_sitemap = '✅ Found' if tech['sitemap'].get('found') else '❌ Not found'
    md_parts.append(f"- **Sitemap:** {exists_sitemap}")

    # Backlinks Detail
    if ahrefs and ahrefs.get('backlinks'):
        md_parts.append("\n## 🔗 Top Backlinks (Ahrefs)")
        md_parts.append("| DR | Anchor | Source URL |")
        md_parts.append("|----|--------|------------|")
        for link in ahrefs['backlinks'][:10]:
            anchor = link.get('anchor', '')[:30]
            if anchor: anchor += "..."
            md_parts.append(f"| {link.get('domainRating')} | {anchor} | {link.get('urlFrom')} |")

    # Save File
    final_content = "\n".join(md_parts)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(final_content)
    
    return str(file_path.absolute())
