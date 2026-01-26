<#
check.ps1 - Project Code Quality Runner

This script runs all local code quality checks in a consistent order:
1. Formatting (isort, black)
2. Linting (ruff, pylint)
3. Type checking (mypy)
4. Security analysis (bandit)

It is intended to be used by developers before committing code
and mirrors the checks executed in CI.

Usage examples:
- Run all checks:
  .\check.ps1

- Run checks only on source code:
  .\check.ps1 -Target src/

- Run only linting on tests:
  .\check.ps1 tests/ -SkipFormat -SkipType -SkipSecurity

- Run all checks without stopping on first failure:
  .\check.ps1 -Target . -ContinueOnError

- Run formatting and security checks only:
  .\check.ps1 -SkipLint -SkipType
#>


param(
    [string]$Target = ".",
    [switch]$ContinueOnError,
    [switch]$SkipFormat,
    [switch]$SkipLint,
    [switch]$SkipType,
    [switch]$SkipSecurity
)

Write-Host "=== Code Quality Checks ===" -ForegroundColor Cyan
Write-Host "Target: $Target" -ForegroundColor Yellow
if ($ContinueOnError) { Write-Host "Mode: Continue on errors" -ForegroundColor Magenta }

$all_passed = $true

# 1. Formatting
if (-not $SkipFormat) {
    Write-Host "`n=== 1. FORMATTING ===" -ForegroundColor Green
    
    Write-Host "> isort" -ForegroundColor Cyan
    isort $Target
    if ($LASTEXITCODE -ne 0) { 
        $all_passed = $false
        if (-not $ContinueOnError) { exit 1 }
    }
    
    Write-Host "> black" -ForegroundColor Cyan
    black $Target
    if ($LASTEXITCODE -ne 0) { 
        $all_passed = $false
        if (-not $ContinueOnError) { exit 1 }
    }
}

# 2. Linting
if (-not $SkipLint) {
    Write-Host "`n=== 2. LINTING ===" -ForegroundColor Green
    
    Write-Host "> ruff" -ForegroundColor Cyan
    ruff check $Target
    if ($LASTEXITCODE -ne 0) { 
        $all_passed = $false
        if (-not $ContinueOnError) { exit 1 }
    }
    
    Write-Host "> pylint" -ForegroundColor Cyan
    pylint $Target
    if ($LASTEXITCODE -ne 0) { 
        $all_passed = $false
        if (-not $ContinueOnError) { exit 1 }
    }
}

# 3. Type Checking
if (-not $SkipType) {
    Write-Host "`n=== 3. TYPE CHECKING ===" -ForegroundColor Green
    Write-Host "> mypy" -ForegroundColor Cyan
    mypy $Target
    if ($LASTEXITCODE -ne 0) { 
        $all_passed = $false
        if (-not $ContinueOnError) { exit 1 }
    }
}

# 4. Security
if (-not $SkipSecurity) {
    Write-Host "`n=== 4. SECURITY ===" -ForegroundColor Green
    Write-Host "> bandit (with config)" -ForegroundColor Cyan
    bandit -c .bandit.yml -r $Target
    if ($LASTEXITCODE -ne 0) { 
        $all_passed = $false
        if (-not $ContinueOnError) { exit 1 }
    }
}

if ($all_passed) {
    Write-Host "`n✅ ALL CHECKS PASSED!" -ForegroundColor Green
} else {
    Write-Host "`n⚠️  SOME CHECKS FAILED" -ForegroundColor Red
    if ($ContinueOnError) { exit 1 }
}
