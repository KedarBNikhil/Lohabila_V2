function Start-Backup {

param(

        [Parameter(Mandatory)]
        $PreFlightResults

    )

    # Repository path
    $Repo = "azure:restic-v1-testing:/"
    $ResticExe = Join-Path $script:BackupConfig.Paths.Tools "restic.exe"

# Ensure RESTIC is never interactive
if (-not $env:RESTIC_PASSWORD) {
    $env:RESTIC_PASSWORD = Get-DPAPISecret -Path $script:BackupConfig.Secrets.ResticPassword
}

if (-not $env:RESTIC_PASSWORD) {
    throw "RESTIC_PASSWORD is missing. Cannot proceed with backup."
}

    $Date = Get-Date -Format "yyyy-MM-dd"

    Write-BackupLog "Backup started"

    $BackupSources = $script:BackupConfig.BackupSettings.BackupSources

    $Output = & $ResticExe -r $Repo backup @BackupSources --json --no-cache --no-lock 2>&1

    $ExitCode = $LASTEXITCODE

    $Output | ForEach-Object {
        Write-BackupLog $_
    }

    # -----------------------------
    # Extract Snapshot ID
    # -----------------------------
    $ExpectedSnapshotId = $null

    $jsonOutput = @()

    $jsonOutput = foreach ($line in $Output) {

        try {

            $line | ConvertFrom-Json

        }
        catch {

            Write-BackupLog "JSON parse error."
            Write-BackupLog $_.Exception.Message
            throw
        }
    }

    $summary = $jsonOutput | Where-Object {
        $_.message_type -eq "summary"
    }

    $ExpectedSnapshotId = $summary.snapshot_id

    if ($ExitCode -eq 0) {

        if (-not $ExpectedSnapshotId) {

            Write-BackupLog "ERROR: Backup succeeded but Snapshot ID could not be extracted."
            throw "Snapshot ID extraction failed."
        }

        Write-BackupLog "Backup successful"
        Write-BackupLog "Expected Snapshot ID: $ExpectedSnapshotId"
        Write-BackupLog "Starting validation"

        $ValidationResult = Start-Validation -Repo $Repo -ExpectedSnapshotId $ExpectedSnapshotId

        Write-BackupLog "Validation completed"

        $ReportPath = BackupReport -ValidationResult $ValidationResult -Repo $Repo

        $LogPath = "C:\BackupAgent\logs\backup-$Date.log"

        Upload-Artifact -File $ReportPath -BlobFolder "reports"

        try {
            Remove-Item $ReportPath -Force -ErrorAction Stop
        }
        catch {
            Write-BackupLog "Failed to delete local report: $($_.Exception.Message)"
        }

        Upload-Artifact -File $LogPath -BlobFolder "logs"
    }
    else {

        Write-BackupLog "Backup FAILED with exit code $ExitCode"
        Write-BackupLog "Validation skipped due to backup failure"
        Write-BackupLog "Report skipped due to backup failure"
    }
}