function BackupReport{

param(
           
           $PreFlightResults,
           $ValidationResult,
            [string]$BackupStatus,
           $Repo
)

$ResticExe = $script:BackupConfig.Tools.ResticExe

Write-Host "Generating backup report..."

# ----------------------------
# 1. Get latest snapshot (SOURCE OF TRUTH)
# ----------------------------

$SnapshotId   = $ValidationResult.LatestSnapshotId
$SnapshotTime = $null
$MachineName = $null
$Paths = $null

# ----------------------------
# 2. Get repository stats (SOURCE OF TRUTH)
# ----------------------------
$statsOutput = & $ResticExe -r $Repo stats latest 2>&1

# Parse minimal safe values (not fragile deep parsing)
$TotalFiles = ($statsOutput | Select-String "Files processed" | ForEach-Object { $_.Line }) -join ""
$TotalSize  = ($statsOutput | Select-String "Total Size" | ForEach-Object { $_.Line }) -join ""

# ----------------------------
# 3. Determine backup status from last run log (minimal dependency)
# ----------------------------
$logFile = Join-Path $script:BackupConfig.Paths.Logs "backup-$(Get-Date -Format 'yyyy-MM-dd').log"
$lastLines = Get-Content $logFile -Tail 50

$BackupStatus = if ($lastLines -match "Backup successful") { "SUCCESS" } else { "UNKNOWN" }

$ValidationStatus = "PASS"

if ($ValidationResult.RepoIntegrity -ne "PASS") {
    $ValidationStatus = "FAIL"
}
elseif ($ValidationResult.SnapshotValidation -eq "FAIL") {
    $ValidationStatus = "FAIL"
}
elseif ($ValidationResult.SnapshotValidation -eq "WARN") {
    $ValidationStatus = "WARN"
}

# ----------------------------
# 4. Build report
# ----------------------------
$Report = @"

Backup Report
=============

Device: $MachineName
Date: $(Get-Date)

Backup Status: $BackupStatus
Snapshot ID: $SnapshotId
Backup Time: $SnapshotTime
Validation Status: $ValidationStatus

Validation Results
------------------
Repository Integrity: $($ValidationResult.RepoIntegrity)
Snapshot Validation: $($ValidationResult.SnapshotValidation)
Validated Snapshot: $($ValidationResult.LatestSnapshotId)

Repository Stats:
$statsOutput

Source Path: $Paths

Recovery:
Latest snapshot $SnapshotId available for restore

Validation Details:
$($ValidationResult.Details -join "`r`n")

"@

# ----------------------------
# 5. Save report
# ----------------------------
$ReportPath = Join-Path $script:BackupConfig.Paths.Reports "BackupReport-$(Get-Date -Format 'yyyy-MM-dd').txt"

New-Item -ItemType Directory -Path "C:\BackupAgent\reports" -Force | Out-Null
$Report | Out-File -FilePath $ReportPath -Encoding UTF8

Write-Host "Report generated: $ReportPath"

return $ReportPath
}