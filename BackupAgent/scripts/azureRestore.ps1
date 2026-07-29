function Get-AzureBaseSnapshot {

    param(
        [Parameter(Mandatory)]
        [string]$AzureReportPath,

        [Parameter(Mandatory)]
        [string]$AzureLogPath
    )

    # -----------------------------
    # 1. Prefer Azure REPORT
    # -----------------------------
    if (Test-Path $AzureReportPath) {
        try {
            $report = Get-Content $AzureReportPath -Raw | ConvertFrom-Json

            if ($report.SnapshotId) {
                return [PSCustomObject]@{
                    SnapshotId   = $report.SnapshotId
                    Repo          = $report.Repo
                    Source        = "Azure"
                    ArtifactType  = "Report"
                    ArtifactPath  = $AzureReportPath
                    Timestamp     = Get-Date
                }
            }
        } catch {
            Write-Host "Azure report parsing failed, falling back..."
        }
    }

    # -----------------------------
    # 2. Azure RESTIC JSON LOG
    # -----------------------------
    if (Test-Path $AzureLogPath) {

        $lines = Get-Content $AzureLogPath

        $jsonObjects = foreach ($line in $lines) {
            try {
                $line | ConvertFrom-Json
            } catch {
                continue
            }
        }

        $summary = $jsonObjects | Where-Object { $_.message_type -eq "summary" }

        if ($summary.snapshot_id) {
            return [PSCustomObject]@{
                SnapshotId   = $summary.snapshot_id
                Repo          = "azure:restic-kedarwin:/"
                Source        = "Azure"
                ArtifactType  = "ResticJSON"
                ArtifactPath  = $AzureLogPath
                Timestamp     = Get-Date
            }
        }
    }

    throw "No valid snapshot found in Azure artifacts"
}