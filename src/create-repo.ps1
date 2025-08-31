#!/usr/bin/env pwsh
# Steam Dataset 2025 - Repository Structure Setup
# Creates the complete directory structure and readme-pending.md files

Write-Host "🎮 Steam Dataset 2025 - Repository Structure Setup" -ForegroundColor Cyan

# Define the complete directory structure from README.md
$directories = @(
    "src",
    "scripts", 
    "database",
    "analytics",
    "api",
    "config",
    "docs",
    "tests",
    "docker",
    "examples"
)

# Simple readme-pending.md content
$readmePendingContent = @"
# README Pending

Documentation for this directory will be added during development.

**Created**: $(Get-Date -Format 'yyyy-MM-dd')
**Project**: Steam Dataset 2025
"@

# Create directories and readme files
foreach ($dir in $directories) {
    # Create directory
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✅ Created: $dir" -ForegroundColor Green
    } else {
        Write-Host "📁 Exists: $dir" -ForegroundColor Yellow
    }
    
    # Create readme-pending.md
    $readmePath = Join-Path $dir "readme-pending.md"
    if (-not (Test-Path $readmePath)) {
        Set-Content -Path $readmePath -Value $readmePendingContent -Encoding UTF8
        Write-Host "📝 Added readme-pending.md to: $dir" -ForegroundColor Green
    }
}

Write-Host "Repository structure setup complete! 🚀" -ForegroundColor Green