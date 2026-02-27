Param(
    [Parameter(Mandatory = $true)]
    [string]$RepoName,

    [string]$Description = "SME Valuation MCP",

    [switch]$Private,

    [string]$GithubUser = ""
)

$ErrorActionPreference = "Stop"

if (-not $env:GITHUB_TOKEN) {
    throw "Missing GITHUB_TOKEN environment variable. Set it before running this script."
}

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

if (-not (Test-Path ".git")) {
    throw "No git repository found in $root"
}

$body = @{
    name        = $RepoName
    description = $Description
    private     = [bool]$Private
    has_issues  = $true
    has_wiki    = $false
} | ConvertTo-Json

$headers = @{
    Authorization = "Bearer $($env:GITHUB_TOKEN)"
    Accept        = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
}

Write-Host "[github] Creating repository '$RepoName'..."
$response = Invoke-RestMethod -Method Post -Uri "https://api.github.com/user/repos" -Headers $headers -Body $body -ContentType "application/json"

$cloneUrl = $response.clone_url
if (-not $cloneUrl) {
    throw "GitHub API did not return clone_url"
}

if ($GithubUser -and $cloneUrl -like "https://github.com/*") {
    $cloneUrl = "https://github.com/$GithubUser/$RepoName.git"
}

Write-Host "[git] Setting main branch..."
git branch -M main

$remoteExists = (git remote) -contains "origin"
if ($remoteExists) {
    git remote set-url origin $cloneUrl
} else {
    git remote add origin $cloneUrl
}

Write-Host "[git] Pushing to origin/main..."
git push -u origin main

Write-Host "[done] Published: $cloneUrl"
