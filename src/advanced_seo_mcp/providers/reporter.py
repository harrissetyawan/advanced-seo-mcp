import os
from datetime import datetime
from typing import Dict, Any
from pathlib import Path
from .onpage_analyzer import analyze_onpage
from .technical_auditor import check_technical_health
from .ahrefs_scraper import get_backlinks_data, get_traffic_data

def generate_markdown_report(url: str, include_ahrefs: bool = True) -> str:
    """
    Runs all analysis tools for a URL and saves a formatted Markdown report.
    Returns the file path of the generated report.
    """
    domain = url.replace('https://', '').replace('http://', '').strip('/')
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report_filename = f"seo_report_{domain.replace('.', '_')}_{timestamp}.md"
    
    # Ensure reports directory exists in the user's current execution directory or project root
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    file_path = report_dir / report_filename

    # 1. Run Analyses
    print(f"🔍 Analyzing On-Page SEO for {url}...")
    onpage = analyze_onpage(url)
    
    print(f"🛠️ Checking Technical Health...")
    tech = check_technical_health(url)
    
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
    md = f"# SEO Audit Report: {domain}\n"
    md += f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    md += f"**URL:** {url}\n\n"

    # Executive Summary
    md += "## 📋 Executive Summary\n"
    md += f"- **HTTP Status:** {onpage.get('status_code')}\n"
    md += f"- **Load Time:** {onpage.get('load_time_ms')}ms\n"
    if ahrefs and ahrefs.get('overview'):
        md += f"- **Domain Rating (DR):** {ahrefs['overview'].get('domainRating', 'N/A')}\n"
        md += f"- **Total Backlinks:** {ahrefs['overview'].get('backlinks', 'N/A')}\n"
    if traffic and traffic.get('traffic'):
        md += f"- **Est. Monthly Traffic:** {traffic['traffic'].get('monthly', 0)}\n"
        md += f"- **Traffic Value:** ${traffic['traffic'].get('value', 0)}\n"

    # On-Page
    md += "\n## 🔍 On-Page SEO Analysis\n"
    meta = onpage.get('meta', {})
    md += "### Meta Tags\n"
    md += f"- **Title:** `{meta.get('title', {}).get('content', 'MISSING')}` ({meta.get('title', {}).get('length')} chars)\n"
    md += f"- **Description:** `{meta.get('description', {}).get('content', 'MISSING')}` ({meta.get('description', {}).get('length')} chars)\n"
    md += f"- **Canonical:** `{meta.get('canonical', 'MISSING')}`\n"
    
    content = onpage.get('content', {})
    md += f"\n### Content\n"
    md += f"- **Word Count:** {content.get('word_count')}\n"
    md += f"- **Thin Content Risk:** {'⚠️ YES' if content.get('thin_content') else '✅ NO'}\n"

    headings = onpage.get('headings', {})
    md += f"\n### Heading Structure\n"
    md += f"- **H1 Check:** {headings.get('h1_check')}\n"
    for tag, texts in headings.get('structure', {}).items():
        if texts:
            md += f"- **{tag.upper()}:** {len(texts)} found (First: *{texts[0] if texts else ''}*)\n"

    # Technical
    md += "\n## 🛠️ Technical Health\n"
    md += f"- **Robots.txt:** {'✅ Found' if tech['robots_txt'].get('exists') else '❌ Missing'}\n"
    md += f"- **Sitemap:** {'✅ Found' if tech['sitemap'].get('found') else '❌ Not found in common paths'}\n"
    sec = tech.get('security', {})
    md += f"- **HTTPS:** {'✅ Yes' if sec.get('https') else '❌ No'}\n"
    md += f"- **HSTS:** {'✅ Yes' if sec.get('hsts') else '❌ No'}\n"

    # Backlinks Detail
    if ahrefs and ahrefs.get('backlinks'):
        md += "\n## 🔗 Top Backlinks (Ahrefs)\n"
        md += "| DR | Anchor | Source URL |\n"
        md += "|----|--------|------------|\n"
        for link in ahrefs['backlinks'][:10]:
            md += f"| {link.get('domainRating')} | {link.get('anchor', '')[:30]}... | {link.get('urlFrom')} |\n"

    # Save File
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(md)
    
    return str(file_path.absolute())
