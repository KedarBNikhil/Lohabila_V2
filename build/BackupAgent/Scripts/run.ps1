param(
    [ValidateSet("backup","report")]
    [string]$Action = "backup"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

. "$PSScriptRoot\..\Config\InstallConfig.ps1"
. "$PSScriptRoot\Common.ps1"

Initialize-BackupConfiguration
Initialize-AzureEnvironment

if (-not (Ensure-ResticRepository)) {
    throw "Unable to verify or initialize Restic repository."
}

if (-not (Test-Path $script:BackupConfig.Tools.ResticExe)) {
    throw "Restic.exe missing at: $($script:BackupConfig.Tools.ResticExe)"
}

. "$PSScriptRoot\locks\locking.ps1"
. "$PSScriptRoot\preflightcheck.ps1"
. "$PSScriptRoot\backup.ps1"
. "$PSScriptRoot\validation.ps1"
. "$PSScriptRoot\report.ps1"
. "$PSScriptRoot\upload.ps1"


Write-Host "Azure environment variables configured."

Acquire-BackupLock

try {

    $PreFlight = Invoke-PreFlightChecks

    if (-not $PreFlight.Passed) {

        Write-BackupLog "PreFlight failed. Backup will not start."
        throw "PreFlight checks failed."
    }

    Write-Host "PreFlight checks PASSED. Starting backup..."
    Write-BackupLog "PreFlight checks PASSED. Starting backup..."

    switch ($Action) {

        "backup" {
            Start-Backup -PreFlightResults $PreFlight.Results
        }

        "report" {
            BackupReport
        }
    }

}
finally {
    Release-BackupLock
}