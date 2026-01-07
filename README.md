# 🚀 Advanced SEO MCP Server

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/status-stable-purple?style=for-the-badge)
![MCP](https://img.shields.io/badge/MCP-FastMCP-orange?style=for-the-badge)

**Powering AI Agents with Advanced SEO Intelligence**

</div>

## 📖 Overview

**Advanced SEO MCP** is a robust Model Context Protocol (MCP) server designed to equip AI agents (Cursor, Claude, Gemini) with professional-grade SEO capabilities. It combines **On-Page analysis**, **Technical Audits**, **Google PageSpeed Insights**, and **Ahrefs Data** (via CapSolver) into a unified interface.

## ✨ Key Features

### 🔍 1. Deep On-Page Analysis
- **Meta Tags:** Title, Description, Canonical.
- **Content:** Heading hierarchy (H1-H6), word count, "thin content" check.
- **Keyword Density:** TF-IDF style keyword analysis.
- **Schema Validation:** Checks JSON-LD structured data for errors.

### 🛠️ 2. Technical & Speed Audits
- **Technical Health:** `robots.txt`, `sitemap.xml`, security headers (HSTS, HTTPS).
- **Broken Link Checker:** Scans for 404 links on the page.
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
- `uv` (Recommended) or `pip`

### Installation

```bash
git clone https://github.com/halilertekin/advanced-seo-mcp.git
cd advanced-seo-mcp

# Setup Virtual Environment
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

### Configuration

Rename `.env.example` to `.env` and add your keys:

```bash
mv .env.example .env
```

```ini
# Required for Backlinks, Keywords, Traffic
CAPSOLVER_API_KEY="your_capsolver_key"

# Required for PageSpeed Analysis
GOOGLE_PSI_API_KEY="your_google_psi_key"
```

---

## 🔌 Integration Guide

### ♊ Gemini CLI (Easiest)

If you have the Gemini CLI installed:

```bash
ln -s $(pwd) ~/.gemini/extensions/advanced-seo-mcp
```
*Restart your Gemini CLI session to see the new tools.*

### 🖱️ Cursor (AI Editor)

1. Go to **Settings** > **MCP**.
2. Click **"Add New MCP Server"**.
3. Use the absolute path to your virtual environment python:
   - **Type:** `command`
   - **Command:** `/ABSOLUTE/PATH/TO/advanced-seo-mcp/.venv/bin/python`
   - **Args:** `-m advanced_seo_mcp.server`
   - **Environment Variables:**
     - `PYTHONPATH`: `/ABSOLUTE/PATH/TO/advanced-seo-mcp/src`

### 🤖 Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "advanced-seo": {
      "command": "/ABSOLUTE/PATH/TO/advanced-seo-mcp/.venv/bin/python",
      "args": ["-m", "advanced_seo_mcp.server"],
      "env": {
        "PYTHONPATH": "/ABSOLUTE/PATH/TO/advanced-seo-mcp/src"
      }
    }
  }
}
```

---

## 📚 Tools Reference

| Tool | Description |
|------|-------------|
| `generate_audit_report` | **Best!** Generates a full Markdown SEO report. |
| `onpage_audit` | Analyzes content, meta tags, and structure. |
| `analyze_page_speed` | Google PageSpeed Insights (Mobile/Desktop). |
| `check_schema_markup` | Validates JSON-LD Schema. |
| `check_broken_links_on_page` | Finds broken (404) links. |
| `compare_competitors` | Compares Backlinks/Traffic of 2 domains. |
| `bulk_sitemap_audit` | Scans sitemap and audits multiple pages. |
| `get_backlinks` | Gets DR and top backlinks (Ahrefs). |
| `keyword_ideas` | Generates keywords (Ahrefs). |

## 📝 License
MIT