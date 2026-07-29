function Get-CustomerBaseRestore {

    param(
       
        [Parameter(Mandatory)]
        [string]$LogPath
    )

    if (-not (Test-Path $LogPath)) {
        throw "Backup log not found: $LogPath"
    }

    # Read latest log
    $lines = Get-Content $LogPath

    # Find the latest Snapshot ID line
    $snapshotLine = $lines |
        Where-Object { $_ -match "Expected Snapshot ID:" } |
        Select-Object -Last 1

    if (-not $snapshotLine) {
        throw "Snapshot ID not found in backup log."
    }

    # Extract snapshot ID
    $snapshotId = ($snapshotLine -replace '.*Expected Snapshot ID:\s*', '').Trim()

    return [PSCustomObject]@{
        SnapshotId = $snapshotId
        Repo       = $script:BackupConfig.Azure.Repository
        Source     = "Customer"
        Artifact   = $LogPath
    }
}