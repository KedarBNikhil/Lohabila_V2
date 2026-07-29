function Start-RestoreEngine {

    param(
        [Parameter(Mandatory)]
        [PSCustomObject]$SnapshotContext,

        [string]$RestorePath = "C:\BackupAgent\RestoreTest",

        [string]$ResticExe = $script:BackupConfig.Tools.ResticExe
    )

    Write-Host "=== RESTORE STARTED ==="
    Write-Host "Source      : $($SnapshotContext.Source)"
    Write-Host "Snapshot ID : $($SnapshotContext.SnapshotId)"
    Write-Host "Repo        : $($SnapshotContext.Repo)"
    Write-Host "Artifact    : $($SnapshotContext.ArtifactPath)"

    if (-not $SnapshotContext.SnapshotId) {
        throw "Invalid SnapshotContext: SnapshotId is missing"
    }

    if (-not $SnapshotContext.Repo) {
        throw "Invalid SnapshotContext: Repo is missing"
    }

    # Clean restore target
    if (Test-Path $RestorePath) {
        Remove-Item $RestorePath -Recurse -Force
    }

    New-Item -ItemType Directory -Path $RestorePath -Force | Out-Null

    # Execute restore (deterministic snapshot only)
    $output = & $ResticExe -r $SnapshotContext.Repo restore $SnapshotContext.SnapshotId --target $RestorePath 2>&1
    $exitCode = $LASTEXITCODE

    $output | ForEach-Object { Write-Host $_ }

    if ($exitCode -ne 0) {
        throw "Restore FAILED with exit code $exitCode"
    }

    Write-Host "Restore SUCCESS"

    return [PSCustomObject]@{
       RestoreId        = $restoreId
       Status           = "Success"
       SnapshotId       = $SnapshotContext.SnapshotId
       SnapshotTime     = $SnapshotContext.SnapshotTimestamp
       Source           = $SnapshotContext.Source
       RestorePath      = $RestorePath
       StartTime        = $startTime
       EndTime          = Get-Date
       Duration         = $duration
       LogPath          = $restoreLogPath
    }
}