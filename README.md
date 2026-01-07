# 🚀 Advanced SEO MCP Server

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/status-stable-purple?style=for-the-badge)
![MCP](https://img.shields.io/badge/MCP-FastMCP-orange?style=for-the-badge)

**Powering AI Agents with Advanced SEO Intelligence**

</div>

## 📖 Overview

**Advanced SEO MCP** is a robust Model Context Protocol (MCP) server designed to equip AI agents with professional-grade SEO capabilities. It combines **On-Page analysis**, **Technical Audits**, **Google PageSpeed Insights**, and **Ahrefs Data** into a unified interface.

## ✨ Key Features

### 🔍 1. Deep On-Page Analysis
Analyze the content structure of any URL.
- **Meta Tags:** Title, Description, Canonical.
- **Content:** Heading hierarchy (H1-H6), word count, "thin content" check.

### 🛠️ 2. Technical & Speed Audits
- **Technical Health:** `robots.txt`, `sitemap.xml`, and security headers.
- **Bulk Sitemap Audit:** Scans multiple pages from a sitemap automatically.
- **PageSpeed Insights:** Real-time Core Web Vitals (LCP, CLS, INP) via Google API.

### 📊 3. Ahrefs Intelligence (via CapSolver)
- **Backlink Explorer:** Domain Rating (DR), total backlinks.
- **Keyword Research:** Generate keyword ideas and questions.
- **Traffic Estimator:** Monthly organic traffic estimates.
- **Competitor Analysis:** Head-to-head comparison of two domains.

### 📝 4. Auto-Reporting
- **Markdown Reports:** Generates a comprehensive `.md` audit report with a single command.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- `uv` or `pip`

### Installation

```bash
git clone https://github.com/yourusername/advanced-seo-mcp.git
cd advanced-seo-mcp
uv pip install .
```

### Configuration

Rename `.env.example` to `.env` and add your keys:

```bash
# Required for Backlinks, Keywords, Traffic
CAPSOLVER_API_KEY="your_capsolver_key"

# Required for PageSpeed Analysis
GOOGLE_PSI_API_KEY="your_google_psi_key"
```

### ♊ Adding to Gemini CLI

```bash
gemini install .
```

---

## 📚 Tools Reference

| Tool | Description | Requires Key |
|------|-------------|--------------|
| `generate_audit_report` | **Best!** Generates a full Markdown SEO report. | ✅ CapSolver |
| `onpage_audit` | Analyzes content, meta tags, and structure. | ❌ No |
| `technical_health_check` | Checks robots.txt, sitemap, security headers. | ❌ No |
| `analyze_page_speed` | Google PageSpeed Insights (Mobile/Desktop). | ✅ Google PSI |
| `compare_competitors` | Compares Backlinks/Traffic of 2 domains. | ✅ CapSolver |
| `bulk_sitemap_audit` | Scans sitemap and audits multiple pages. | ❌ No |
| `get_backlinks` | Gets DR and top backlinks. | ✅ CapSolver |
| `keyword_ideas` | Generates keywords and questions. | ✅ CapSolver |

## 📝 License
MIT
