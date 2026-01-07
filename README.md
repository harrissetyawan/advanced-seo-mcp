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

## 🚀 Getting Started

### 1. Installation

Clone and install dependencies:

```bash
git clone https://github.com/halilertekin/advanced-seo-mcp.git
cd advanced-seo-mcp

# Create virtual environment and install
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install .
```

### 2. Configuration (API Keys)

Rename the example file and add your keys:

```bash
mv .env.example .env
```

Edit `.env`:
```ini
CAPSOLVER_API_KEY="your_capsolver_key"
GOOGLE_PSI_API_KEY="your_google_psi_key"
```

### 3. Setup (Crucial Step)

Run the setup script to generate the configuration file for your specific machine:

```bash
python setup_extension.py
```

*This will generate a valid `gemini-extension.json` with the correct absolute paths for your system.*

---

## 🔌 Integration Guide

### ♊ Gemini CLI

After running `python setup_extension.py`:

```bash
ln -s $(pwd) ~/.gemini/extensions/advanced-seo-mcp
```
*Restart your Gemini CLI session.*

### 🖱️ Cursor / Claude

The `setup_extension.py` script ensures `gemini-extension.json` has the correct paths. You can manually copy the `command`, `args`, and `env` from that file into your Cursor or Claude settings if needed.

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
