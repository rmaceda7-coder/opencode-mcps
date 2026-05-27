# PDF Generation Guide

## Quick Methods to Generate PDF

### Method 1: Using Pandoc (Recommended)

1. **Install Pandoc:**
   ```powershell
   # Using winget
   winget install JohnMacFarlane.Pandoc
   
   # OR using chocolatey
   choco install pandoc
   
   # OR download from
   # https://pandoc.org/installing.html
   ```

2. **Run the generation script:**
   ```powershell
   cd C:\Users\ramiro.maceda\AppData\Local\Temp\opencode\sql-server-mcp
   .\generate_pdf_simple.ps1
   ```

### Method 2: Using Microsoft Word

1. Open `docs\COMPLETE_GUIDE.md` in a text editor
2. Copy all content
3. Open Microsoft Word
4. Paste content
5. Word will format the markdown automatically
6. File → Save As → PDF
7. Save as `SQL_Server_MCP_Complete_Guide.pdf`

### Method 3: Using VS Code

1. Install "Markdown PDF" extension in VS Code
2. Open `docs\COMPLETE_GUIDE.md`
3. Right-click in editor
4. Select "Markdown PDF: Export (pdf)"
5. PDF will be generated in the same folder

### Method 4: Online Converters

Upload `docs\COMPLETE_GUIDE.md` to any of these:

- **Markdown to PDF:** https://www.markdowntopdf.com/
- **CloudConvert:** https://cloudconvert.com/md-to-pdf
- **Dillinger.io:** https://dillinger.io/ (export as PDF)

### Method 5: Python Script (if Python installed)

```powershell
# Install dependencies
pip install markdown pdfkit

# Create convert.py
@"
import markdown
import pdfkit

with open('docs/COMPLETE_GUIDE.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

html = markdown.markdown(md_content)
pdfkit.from_string(html, 'docs/SQL_Server_MCP_Complete_Guide.pdf')
"@ | Out-File convert.py

# Run
python convert.py
```

## Manual PDF Generation (No Tools Required)

1. Open `docs\COMPLETE_GUIDE.md` in any browser:
   - Chrome, Edge, Firefox all support markdown rendering with extensions
   
2. Install markdown viewer extension:
   - Chrome: "Markdown Viewer"
   - Edge: "Markdown Viewer"
   
3. Open the file in browser
4. Press Ctrl+P (Print)
5. Select "Save as PDF"
6. Save the file

## Troubleshooting

### Pandoc: "pdf-engine not found"
- Install wkhtmltopdf: https://wkhtmltopdf.org/downloads.html
- Or use xelatex: Install MiKTeX from https://miktex.org/

### Permission Denied
- Run PowerShell as Administrator
- Or use: `Set-ExecutionPolicy Bypass -Scope Process`

### File Not Found
- Ensure you're in the correct directory
- Check the path: `docs\COMPLETE_GUIDE.md` exists

## File Location

After generation, the PDF will be at:
```
C:\Users\ramiro.maceda\AppData\Local\Temp\opencode\sql-server-mcp\docs\SQL_Server_MCP_Complete_Guide.pdf
```
