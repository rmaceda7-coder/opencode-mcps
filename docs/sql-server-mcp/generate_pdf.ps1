# SQL Server MCP - PDF Generation Script
# This script converts the markdown documentation to PDF

param(
    [string]$InputFile = "docs\COMPLETE_GUIDE.md",
    [string]$OutputFile = "docs\SQL_Server_MCP_Complete_Guide.pdf"
)

Write-Host "SQL Server MCP - PDF Generation" -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

# Check if pandoc is installed
try {
    $pandocVersion = pandoc --version 2>&1 | Select-Object -First 1
    Write-Host "✓ Pandoc found: $pandocVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Pandoc not found!" -ForegroundColor Red
    Write-Host "`nPlease install Pandoc to generate PDF:" -ForegroundColor Yellow
    Write-Host "  1. Download from: https://pandoc.org/installing.html" -ForegroundColor White
    Write-Host "  2. Or install with chocolatey: choco install pandoc" -ForegroundColor White
    Write-Host "  3. Or install with winget: winget install JohnMacFarlane.Pandoc" -ForegroundColor White
    Write-Host "`nAlternatively, use an online converter:" -ForegroundColor Yellow
    Write-Host "  - https://www.markdowntopdf.com/" -ForegroundColor White
    Write-Host "  - https://cloudconvert.com/md-to-pdf" -ForegroundColor White
    exit 1
}

# Check if input file exists
if (-not (Test-Path $InputFile)) {
    Write-Host "✗ Input file not found: $InputFile" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Input file found: $InputFile" -ForegroundColor Green

# Create output directory if it doesn't exist
$outputDir = Split-Path $OutputFile -Parent
if ($outputDir -and -not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

# Generate PDF with pandoc
Write-Host "`nGenerating PDF..." -ForegroundColor Cyan

try {
    # Basic pandoc command
    pandoc $InputFile `
        -o $OutputFile `
        --pdf-engine=wkhtmltopdf `
        --toc `
        --toc-depth=3 `
        -V geometry:margin=1in `
        -V fontsize=11pt `
        -V linkcolor:blue `
        2>&1 | Out-Null
    
    if ($LASTEXITCODE -ne 0) {
        # Try alternative PDF engine
        Write-Host "Trying alternative PDF engine..." -ForegroundColor Yellow
        pandoc $InputFile `
            -o $OutputFile `
            --pdf-engine=xelatex `
            --toc `
            --toc-depth=3 `
            -V geometry:margin=1in `
            -V fontsize=11pt
    }
    
    if (Test-Path $OutputFile) {
        Write-Host "`n✓ PDF generated successfully!" -ForegroundColor Green
        Write-Host "  Output: $OutputFile" -ForegroundColor White
        
        $fileSize = (Get-Item $OutputFile).Length
        $fileSizeKB = [math]::Round($fileSize / 1KB, 2)
        Write-Host "  Size: $fileSizeKB KB" -ForegroundColor White
        
        # Open the PDF
        Write-Host "`nOpening PDF..." -ForegroundColor Cyan
        Start-Process $OutputFile
    } else {
        Write-Host "`n✗ PDF generation failed" -ForegroundColor Red
    }
    
} catch {
    Write-Host "`n✗ Error generating PDF: $_" -ForegroundColor Red
    Write-Host "`nTrying simple conversion..." -ForegroundColor Yellow
    
    # Fallback - simple conversion
    pandoc $InputFile -o $OutputFile
    
    if (Test-Path $OutputFile) {
        Write-Host "✓ Simple PDF generated" -ForegroundColor Green
        Start-Process $OutputFile
    }
}
