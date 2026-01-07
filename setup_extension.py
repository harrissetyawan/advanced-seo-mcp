import os
import sys
import json
from pathlib import Path

def setup():
    """
    Generates a system-specific gemini-extension.json file.
    """
    # 1. Get Project Root
    project_root = Path(__file__).parent.absolute()
    
    # 2. Detect Virtual Environment Python
    if sys.platform == "win32":
        venv_python = project_root / ".venv" / "Scripts" / "python.exe"
    else:
        venv_python = project_root / ".venv" / "bin" / "python"

    if not venv_python.exists():
        print(f"❌ Virtual environment not found at: {venv_python}")
        print("   Please run: python3 -m venv .venv && source .venv/bin/activate && pip install .")
        return

    # 3. Create Configuration Dictionary
    config = {
        "name": "Advanced SEO (Ahrefs & PSI)",
        "version": "0.1.0",
        "description": "Professional SEO suite: On-Page, Technical, Ahrefs Data, Speed Tests & Reporting",
        "mcpServers": [
            {
                "id": "advanced-seo-mcp",
                "command": str(venv_python),
                "args": [
                    "-m",
                    "advanced_seo_mcp.server"
                ],
                "env": {
                    "PYTHONPATH": str(project_root / "src")
                }
            }
        ]
    }

    # 4. Write File
    output_path = project_root / "gemini-extension.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    print("✅ Configuration generated successfully!")
    print(f"📄 File: {output_path}")
    print("\n🚀 To install in Gemini CLI, run:")
    print(f"   ln -s \"{project_root}\" ~/.gemini/extensions/advanced-seo-mcp")
    print("   (Then restart your Gemini session)")

if __name__ == "__main__":
    setup()
