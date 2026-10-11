<#
.SYNOPSIS
  Build the Part D conflict lab, the same way every time (Windows PowerShell 5.1 or PowerShell 7).
.DESCRIPTION
  Mirror of setup_conflict.sh. Creates ./conflict-lab with branches main and feature/strict-gate,
  then runs `git merge feature/strict-gate` so the repo is left STOPPED IN A CONFLICTED MERGE.
  settings.py and report.py conflict; CHANGELOG.md merges by itself.
  Setup commits use fixed names and dates so the repo is identical on every machine.
  The merge commit you make yourself uses YOUR Git identity (git config --global user.name ...).
.EXAMPLE
  .\setup_conflict.ps1                  # builds .\conflict-lab, mid-conflict
  .\setup_conflict.ps1 -Dir my-folder   # another folder name or path
  .\setup_conflict.ps1 -Force           # rebuild an existing conflict-lab (only lab repos are removed)
  .\setup_conflict.ps1 -NoMerge         # build the diverged branches, do NOT run the merge yet
.NOTES
  If scripts are blocked:  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  Files are written with LF endings and no BOM so they match the bash version.
#>
param(
    [string]$Dir = "conflict-lab",
    [switch]$Force,
    [switch]$NoMerge
)
$ErrorActionPreference = "Stop"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) { Write-Error "git is not installed or not on PATH"; exit 1 }

if (Test-Path $Dir) {
    if ($Force -and (Test-Path (Join-Path $Dir ".git")) -and (Test-Path (Join-Path $Dir "settings.py")) -and (Test-Path (Join-Path $Dir "report.py"))) {
        Remove-Item -Recurse -Force $Dir      # only ever removes a folder that looks like THIS lab
    } else {
        Write-Error "Folder '$Dir' already exists. Re-run with -Force to rebuild it (only lab repos are removed)."; exit 1
    }
}

# Text with LF endings and no BOM (Set-Content / Out-File would add CRLF or a BOM on Windows PowerShell 5.1).
function Write-Lf([string]$Path, [string[]]$Lines) {
    $full = Join-Path (Get-Location).Path $Path
    [System.IO.File]::WriteAllText($full, (($Lines -join "`n") + "`n"), (New-Object System.Text.UTF8Encoding($false)))
}
# Native git does not throw on a non-zero exit; call it through this helper.
$script:AllowFail = $false
function Invoke-Git { & git @args; if ($LASTEXITCODE -ne 0 -and -not $script:AllowFail) { throw "git $($args -join ' ') failed ($LASTEXITCODE)" } }
# Commit with a fixed author and date so the setup is reproducible.
function Commit-As([string]$Message, [string]$Author, [string]$Date) {
    $env:GIT_AUTHOR_NAME = $Author;    $env:GIT_AUTHOR_EMAIL = "setup@example.com";    $env:GIT_AUTHOR_DATE = "$Date +0000"
    $env:GIT_COMMITTER_NAME = $Author; $env:GIT_COMMITTER_EMAIL = "setup@example.com"; $env:GIT_COMMITTER_DATE = "$Date +0000"
    Invoke-Git commit -q -a -m $Message
    Remove-Item Env:GIT_AUTHOR_NAME, Env:GIT_AUTHOR_EMAIL, Env:GIT_AUTHOR_DATE, Env:GIT_COMMITTER_NAME, Env:GIT_COMMITTER_EMAIL, Env:GIT_COMMITTER_DATE
}

$start = Get-Location
New-Item -ItemType Directory -Path $Dir | Out-Null
Set-Location $Dir

$ErrorActionPreference = "Continue"      # old Git writes to stderr here; do not treat that as a script error
& git init -q -b main 2>$null
$ErrorActionPreference = "Stop"
if ($LASTEXITCODE -ne 0) { Invoke-Git init -q; Invoke-Git checkout -q -b main }     # -b needs Git 2.28+
Invoke-Git config core.autocrlf false          # local to this repo: identical files on Windows and Linux
Invoke-Git config merge.conflictstyle merge    # classic markers (<<<<<<< ======= >>>>>>>)

function Settings([string]$Threshold, [string]$Suites) {
    Write-Lf "settings.py" @(
        '# Nightly smoke run: shared team settings',
        "PASS_THRESHOLD = $Threshold   # percent of tests that must pass for a GREEN run",
        'RETRIES = 1',
        'TIMEOUT_SECONDS = 30',
        'REPORT_FORMAT = "text"',
        'REPORT_DIR = "out"',
        "SUITES = $Suites")
}
function Report([string[]]$Extra) {
    $head = @(
        '"""Print the verdict for the nightly smoke run."""',
        'from settings import PASS_THRESHOLD, SUITES',
        '',
        '',
        'def verdict(rate):',
        '    return "GREEN" if rate >= PASS_THRESHOLD else "RED"')
    $tail = @(
        '',
        '',
        'def main():',
        '    print("Suites:", ", ".join(SUITES))',
        '    print("Verdict for 93.0%:", verdict(93.0))',
        '',
        '',
        'if __name__ == "__main__":',
        '    main()')
    Write-Lf "report.py" ($head + $Extra + $tail)
}

# ---- common ancestor ----
Settings "90" '["login", "search"]'
Report @()
Write-Lf "CHANGELOG.md" @('# Changelog', '', '## Unreleased', '- Nightly smoke run reports a GREEN or RED verdict')
Invoke-Git add -A
Commit-As "Add nightly gate settings and report" "Team Lead" "2026-01-05T09:00:00"

# ---- feature/strict-gate: Sam wants a stricter gate and the payments suite ----
Invoke-Git switch -q -c feature/strict-gate
Settings "95" '["login", "search", "payments"]'
Report @('', '', 'def failing_suites(results):', '    """Names of suites that have at least one failed test, sorted."""', '    return sorted({r["suite"] for r in results if r["status"] == "fail"})')
Write-Lf "CHANGELOG.md" @('# Changelog', '', '## Unreleased', '- Nightly smoke run reports a GREEN or RED verdict', '- Strict gate: payments suite added, threshold raised (Sam)')
Commit-As "Add strict gate and payments suite" "Sam" "2026-01-05T11:00:00"

# ---- main: Priya lowers the gate and adds the checkout suite ----
Invoke-Git switch -q main
Settings "92" '["login", "search", "checkout"]'
Report @('', '', 'def summary_line(passed, total):', '    """One line for the morning email, e.g. "3/4 passed (75.0%)"."""', '    return f"{passed}/{total} passed ({passed / total * 100:.1f}%)"')
Write-Lf "CHANGELOG.md" @('# Changelog (team: QE Foundations)', '', '## Unreleased', '- Nightly smoke run reports a GREEN or RED verdict')
Commit-As "Lower gate and add checkout suite" "Priya" "2026-01-05T10:30:00"

Write-Host "Lab repo ready in: $((Get-Location).Path)"
Invoke-Git log --oneline --graph --all

if (-not $NoMerge) {
    Write-Host ""
    Write-Host "--- git merge feature/strict-gate ---"
    $script:AllowFail = $true               # a conflict exits non-zero: that is the point
    Invoke-Git merge feature/strict-gate
    $script:AllowFail = $false
    Write-Host "--- git status -s ---"
    Invoke-Git status -s
    Write-Host ""
    Write-Host "You are now in the middle of a conflicted merge. cd $Dir and start Part D."
} else {
    Write-Host ""
    Write-Host "Next: cd $Dir ; then run:  git merge feature/strict-gate"
}
Set-Location $start
