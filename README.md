# 🚀 Advanced SEO MCP Server

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/status-stable-purple?style=for-the-badge)
![MCP](https://img.shields.io/badge/MCP-FastMCP-orange?style=for-the-badge)

**Powering AI Agents with Advanced SEO Intelligence**

</div>

## 📖 Overview

**Advanced SEO MCP** is a robust Model Context Protocol (MCP) server designed to equip AI agents (like Claude Desktop, Cursor, etc.) with professional-grade SEO capabilities. Unlike simple scrapers, this tool combines **On-Page analysis**, **Technical Audits**, and **Ahrefs Data** (via CapSolver) into a unified, agent-friendly interface.

It features a smart **caching layer** (SQLite) to minimize API costs and maximize performance.

## ✨ Key Features

### 🔍 1. Deep On-Page Analysis
Analyze the content structure of any URL without external APIs.
- **Meta Tags Audit:** Title, Description, Canonical, Robots.
- **Content Hierarchy:** H1-H6 structure visualization.
- **Content Quality:** Word count, "thin content" detection.
- **Link Profile:** Internal vs. External link ratios.
- **Image Audit:** Identification of images missing Alt tags.

### 🛠️ 2. Technical Health Check
Perform rapid technical audits on domains.
- **Security Headers:** HSTS, X-Frame-Options, SSL/HTTPS check.
- **Crawling:** Validation of `robots.txt` and `sitemap.xml` presence/accessibility.

### 📊 3. Ahrefs Intelligence (Powered by CapSolver)
Access premium SEO data using CapSolver to bypass protections legally.
- **Backlink Explorer:** Domain Rating (DR), total backlinks, and referring domains.
- **Keyword Research:** Generate keyword ideas, question-based queries, and search volumes.
- **Traffic Estimator:** Monthly traffic estimates and traffic value.
- **Keyword Difficulty (KD):** SERP overview and difficulty scores.

### ⚡ 4. Smart Caching
- **Cost Efficiency:** Caches expensive scraping results locally (`~/.advanced_seo_mcp_cache.db`).
- **Performance:** Instant results for repeated queries.

---

## 🏗️ Architecture

```mermaid
graph TD
    User[AI Agent / Client] -->|MCP Protocol| Server[MCP Server (FastMCP)]
    Server -->|Route| Provider1[OnPage Analyzer]
    Server -->|Route| Provider2[Technical Auditor]
    Server -->|Route| Provider3[Ahrefs Scraper]
    
    Provider1 -->|Request| TargetURL[Target Website]
    Provider2 -->|Request| TargetURL
    
    Provider3 -->|Captcha Solve| Utils[CapSolver Utils]
    Utils -->|API Call| CapSolverAPI[CapSolver.com]
    
    Provider3 -->|Check| Cache[(SQLite Cache)]
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) (Recommended) or pip
- A [CapSolver](https://capsolver.com) API Key (for Ahrefs features only)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/advanced-seo-mcp.git
   cd advanced-seo-mcp
   ```

2. **Install dependencies:**
   ```bash
   # Using uv (faster)
   uv pip install .
   
   # Or using standard pip
   pip install .
   ```

### Configuration

Set your CapSolver API key as an environment variable. This is required only if you plan to use the Backlink, Keyword, or Traffic tools. The On-Page and Technical tools work freely without it.

```bash
export CAPSOLVER_API_KEY="your_capsolver_key_here"
```

---

## 📚 Tools Reference

### `onpage_audit`
Performs a comprehensive content and structure audit.
- **Arguments:** `url` (str)
- **Returns:** JSON object with meta tags, headings, content stats, and link counts.

### `technical_health_check`
Checks the technical foundation of a website.
- **Arguments:** `url` (str)
- **Returns:** JSON object with robots.txt status, sitemap status, and security headers.

### `get_backlinks` 🔐
Retrieves backlink profile and Domain Rating.
- **Arguments:** `domain` (str)
- **Requires:** `CAPSOLVER_API_KEY`

### `keyword_ideas` 🔐
Generates related keywords and questions.
- **Arguments:** `keyword` (str), `country` (str, default="us")
- **Requires:** `CAPSOLVER_API_KEY`

### `estimate_traffic` 🔐
Estimates organic search traffic.
- **Arguments:** `domain` (str), `country` (str, optional)
- **Requires:** `CAPSOLVER_API_KEY`

### `check_difficulty` 🔐
Analyzes how hard it is to rank for a keyword.
- **Arguments:** `keyword` (str), `country` (str, default="us")
- **Requires:** `CAPSOLVER_API_KEY`

*(🔐 = Requires CapSolver API Key)*

---

## 🔌 Integration Guide

To use these tools in your AI editor or agent, you need to register this MCP server.

### 🔑 1. API Key Setup (Crucial)
1. Get your API Key from [CapSolver Dashboard](https://dashboard.capsolver.com/).
2. Rename `.env.example` to `.env` in this folder:
   ```bash
   mv .env.example .env
   ```
3. Paste your key into the `.env` file.

### 🖱️ 2. Adding to Cursor (AI Editor)

1. Open **Cursor Settings** > **General** > **MCP**.
2. Click **"Add New MCP Server"**.
3. Fill in the details:
   - **Name:** `Advanced SEO`
   - **Type:** `command` (stdio)
   - **Command:** `uv` (ensure `uv` is installed, or use full path to python)
   - **Args:**
     ```text
     run
     --directory
     /ABSOLUTE/PATH/TO/advanced-seo-mcp
     advanced-seo
     ```
   - **Environment Variables:**
     - Key: `CAPSOLVER_API_KEY`
     - Value: `your_actual_key_here` (or rely on the .env file if supported by your runner)

### 🤖 3. Adding to Claude Desktop

Edit your configuration file:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add this entry:

```json
{
  "mcpServers": {
    "advanced-seo": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/ABSOLUTE/PATH/TO/advanced-seo-mcp", 
        "advanced-seo"
      ],
      "env": {
        "CAPSOLVER_API_KEY": "CAP-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
      }
    }
  }
}
```
*(Note: Replace `/ABSOLUTE/PATH/TO/...` with the actual full path to this folder)*

---

## 💻 Development

### Running Locally

To run the MCP server locally for testing or development:

```bash
# Run the server
python -m advanced_seo_mcp.server
```

### Project Structure

```text
src/
└── advanced_seo_mcp/
    ├── server.py              # Main Entry Point & Tool Definitions
    ├── providers/             # Logic Providers
    │   ├── onpage_analyzer.py    # BeautifulSoup Logic
    │   ├── technical_auditor.py  # Request/Header Logic
    │   └── ahrefs_scraper.py     # Scraper Logic
    └── utils/
        ├── cache.py           # SQLite Caching
        └── capsolver.py       # Captcha Solving Logic
```

## 📝 License

This project is licensed under the MIT License.