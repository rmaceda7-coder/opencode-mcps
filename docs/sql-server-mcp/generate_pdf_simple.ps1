# SQL Server MCP - Simple PDF Generator

Write-Host "SQL Server MCP - PDF Generation" -ForegroundColor Cyan
Write-Host "================================`n"

$inputFile = "docs\COMPLETE_GUIDE.md"
$outputFile = "docs\SQL_Server_MCP_Complete_Guide.pdf"

# Method 1: Check for pandoc
$pandocExists = Get-Command pandoc -ErrorAction SilentlyContinue

if ($pandocExists) {
    Write-Host "Pandoc found. Generating PDF..." -ForegroundColor Green
    
    & pandoc $inputFile -o $outputFile --pdf-engine=wkhtmltopdf --toc --toc-depth=3 -V geometry:margin=1in -V fontsize=11pt 2>$null
    
    if (-not $?) {
        Write-Host "First attempt failed. Trying alternative..." -ForegroundColor Yellow
        & pandoc $inputFile -o $outputFile --toc
    }
    
    if (Test-Path $outputFile) {
        Write-Host "`nPDF created successfully: $outputFile" -ForegroundColor Green
        Start-Process $outputFile
    } else {
        Write-Host "PDF generation failed" -ForegroundColor Red
    }
} else {
    Write-Host "Pandoc not found. Please install:" -ForegroundColor Yellow
    Write-Host "  winget install JohnMacFarlane.Pandoc" -ForegroundColor White
    Write-Host "`nOr use online converter with the markdown file at:" -ForegroundColor Yellow
    Write-Host "  $PWD\$inputFile"
}
