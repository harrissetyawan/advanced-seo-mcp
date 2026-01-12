# 🚀 Advanced SEO MCP Server

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/status-stable-purple?style=for-the-badge)
![MCP](https://img.shields.io/badge/MCP-FastMCP-orange?style=for-the-badge)

**Powering AI Agents with Advanced SEO Intelligence**

</div>

## 📖 Overview

**Advanced SEO MCP** is a robust Model Context Protocol (MCP) server designed to equip AI agents with professional-grade SEO capabilities. It combines **On-Page analysis**, **Technical Audits**, **Google PageSpeed Insights**, and **Ahrefs Data** (via CapSolver) into a unified interface.

---

## 🚀 Installation

### Option 1: One-Command Install (Recommended)

If you have [uv](https://github.com/astral-sh/uv) installed, you can install this extension directly with Gemini CLI. `uv` handles all Python dependencies automatically.

```bash
gemini extensions install https://github.com/halilertekin/advanced-seo-mcp
```

*Note: You will need to configure your API keys in the `.env` file inside the extension directory after installation.*

### Option 2: Manual Developer Setup

If you want to modify the code or don't use `uv`, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/halilertekin/advanced-seo-mcp.git
    cd advanced-seo-mcp
    ```

2.  **Create virtual environment & Install:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    pip install -e .
    ```

3.  **Setup Configuration:**
    Run the setup script to generate the local configuration:
    ```bash
    python setup_extension.py
    ```

4.  **Link to Gemini:**
    ```bash
    ln -s $(pwd) ~/.gemini/extensions/advanced-seo-mcp
    ```

---

## 🔑 Configuration

This server requires API keys for full functionality.

1.  Create a `.env` file in the project root (or rename `.env.example`):
    ```bash
    cp .env.example .env
    ```

2.  Add your API keys:
    ```ini
    # Required for Ahrefs Tools (Backlinks, Keywords, Traffic)
    # Get key: https://dashboard.capsolver.com/
    CAPSOLVER_API_KEY="your_capsolver_key"

    # Required for PageSpeed Insights
    # Get key: https://developers.google.com/speed/docs/insights/v5/get-started
    GOOGLE_PSI_API_KEY="your_google_psi_key"
    ```

---

## 📚 Tools Reference

| Tool | Description |
|------|-------------|
| `generate_audit_report` | **Best!** Generates a full Markdown SEO report combining all metrics. |
| `onpage_audit` | Analyzes content structure, meta tags, and density. |
| `analyze_page_speed` | Google PageSpeed Insights analysis (Mobile/Desktop). |
| `check_schema_markup` | Validates JSON-LD Schema implementation. |
| `check_broken_links_on_page` | Scans page for broken (404) internal/external links. |
| `compare_competitors` | Compares Backlinks/Traffic/DR of 2 domains. |
| `bulk_sitemap_audit` | Scans sitemap and performs quick audit on multiple pages. |
| `get_backlinks` | Retrieves Domain Rating & Top Backlinks (Ahrefs Data). |
| `keyword_ideas` | Generates keyword ideas & questions (Ahrefs Data). |

## 📝 License
MIT