# SQL Server MCP - Quick Installation Script

param(
    [string]$InstallPath = "C:\MCP\sql-server-mcp",
    [switch]$SkipDependencies
)

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "SQL Server MCP Server - Installation" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

# Check Python
Write-Host "[1/5] Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found!" -ForegroundColor Red
    Write-Host "  Install from: https://www.python.org/downloads/" -ForegroundColor White
    exit 1
}

# Check ODBC Driver
Write-Host "`n[2/5] Checking ODBC Driver..." -ForegroundColor Yellow
$odbcDriver = Get-OdbcDriver | Where-Object {$_.Name -like "*SQL Server*" -and $_.Name -like "*17*"}
if ($odbcDriver) {
    Write-Host "  ✓ ODBC Driver 17 for SQL Server found" -ForegroundColor Green
} else {
    Write-Host "  ✗ ODBC Driver 17 not found!" -ForegroundColor Red
    Write-Host "  Download from: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server" -ForegroundColor White
    $response = Read-Host "  Continue anyway? (y/n)"
    if ($response -ne 'y') { exit 1 }
}

# Copy files
Write-Host "`n[3/5] Copying files..." -ForegroundColor Yellow
if (Test-Path $InstallPath) {
    Write-Host "  Installation path already exists: $InstallPath" -ForegroundColor Yellow
    $response = Read-Host "  Overwrite? (y/n)"
    if ($response -ne 'y') { exit 1 }
    Remove-Item $InstallPath -Recurse -Force
}

Copy-Item -Path $PSScriptRoot -Destination $InstallPath -Recurse -Force
Write-Host "  ✓ Files copied to: $InstallPath" -ForegroundColor Green

# Install dependencies
if (-not $SkipDependencies) {
    Write-Host "`n[4/5] Installing Python dependencies..." -ForegroundColor Yellow
    Set-Location $InstallPath
    pip install -e . 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Failed to install dependencies" -ForegroundColor Red
        Write-Host "  Run manually: pip install -e ." -ForegroundColor White
    }
}

# Configure OpenCode
Write-Host "`n[5/5] Configuring OpenCode..." -ForegroundColor Yellow
$configDir = "$env:USERPROFILE\.config\opencode"
$configFile = "$configDir\config.json"

if (-not (Test-Path $configDir)) {
    New-Item -ItemType Directory -Path $configDir -Force | Out-Null
}

$config = @{
    mcpServers = @{
        "sql-server" = @{
            command = "python"
            args = @("-m", "src.server")
            cwd = $InstallPath.Replace('\', '/')
            env = @{
                PYTHONPATH = $InstallPath.Replace('\', '/')
                LOG_LEVEL = "INFO"
            }
        }
    }
}

if (Test-Path $configFile) {
    Write-Host "  OpenCode config already exists" -ForegroundColor Yellow
    $response = Read-Host "  Add sql-server MCP to existing config? (y/n)"
    if ($response -eq 'y') {
        $existingConfig = Get-Content $configFile | ConvertFrom-Json
        $existingConfig.mcpServers | Add-Member -NotePropertyName "sql-server" -NotePropertyValue $config.mcpServers."sql-server" -Force
        $existingConfig | ConvertTo-Json -Depth 10 | Set-Content $configFile
        Write-Host "  ✓ Configuration updated" -ForegroundColor Green
    }
} else {
    $config | ConvertTo-Json -Depth 10 | Set-Content $configFile
    Write-Host "  ✓ Configuration created" -ForegroundColor Green
}

# Summary
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "============================================`n" -ForegroundColor Cyan

Write-Host "Installation Path: $InstallPath" -ForegroundColor White
Write-Host "Config File: $configFile" -ForegroundColor White

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "  1. Restart OpenCode" -ForegroundColor White
Write-Host "  2. Test connection: query a SQL Server instance" -ForegroundColor White
Write-Host "  3. Read documentation: $InstallPath\README.md" -ForegroundColor White

Write-Host "`nExample Usage:" -ForegroundColor Yellow
Write-Host "  'List tables in DOA-SERVER\INSTANCE database CustomerDB'" -ForegroundColor White

Write-Host "`n"
