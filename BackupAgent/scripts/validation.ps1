function Start-Validation{

param (
    [string]$Repo,
    [string]$ExpectedSnapshotId = $null
)

$ResticExe = $script:BackupConfig.Tools.ResticExe

# -----------------------------
# Retrieve secrets (DPAPI)
# -----------------------------
$StorageAccount = Get-DPAPISecret -Path $script:BackupConfig.Secrets.AzureAccountName
$StorageKey     = Get-DPAPISecret -Path $script:BackupConfig.Secrets.AzureAccountKey
$ResticPassword = Get-DPAPISecret -Path $script:BackupConfig.Secrets.ResticPassword

# -----------------------------
# Result object
# -----------------------------
$result = [ordered]@{
    Timestamp = Get-Date
    RepoPath = $Repo
    RepoIntegrity = "UNKNOWN"
    SnapshotValidation = "UNKNOWN"
    LatestSnapshotId = $null
    ExpectedSnapshotId = $ExpectedSnapshotId
    Details = @()
}

# -----------------------------
# Level 1: Repository Integrity Check
# -----------------------------
try {
   $checkOutput = & $ResticExe check 2>&1

    if ($LASTEXITCODE -ne 0) {
        $result.RepoIntegrity = "FAIL"
        $result.Details += "Repository integrity check failed"
        $result.Details += $checkOutput
    }
    else {
        $result.RepoIntegrity = "PASS"
        $result.Details += "Repository integrity OK"
    }
}
catch {
    $result.RepoIntegrity = "FAIL"
    $result.Details += $_.Exception.Message
}

# If repo itself is broken, stop early

if ($result.RepoIntegrity -eq "FAIL") {
    return $result
}

# -----------------------------
# Level 2: Snapshot Validation
# -----------------------------
try {
    $snapshots = & $ResticExe -r $Repo snapshots --json 2>$null | ConvertFrom-Json

    if (-not $snapshots -or $snapshots.Count -eq 0) {

        $result.SnapshotValidation = "FAIL"
        $result.Details += "No snapshots found"
    }

    else {
        $latest = $snapshots | Sort-Object time -Descending | Select-Object -First 1
        $latestId = $latest.id

        $result.LatestSnapshotId = $latestId

        if ($ExpectedSnapshotId) {

            $result.ExpectedSnapshotId = $ExpectedSnapshotId

            if ($latestId -eq $ExpectedSnapshotId){

                $result.SnapshotValidation = "PASS"
                $result.Details += "Snapshot comparison successful."
            }
            else {

                $result.SnapshotValidation = "FAIL"
                $result.Details += "Snapshot comparison failed."
                $result.Details += "Expected Snapshot : $ExpectedSnapshotId"
                $result.Details += "Azure Snapshot    : $latestId"
            }

        }
        else {

            $result.SnapshotValidation = "FAIL"
            $result.Details += "Expected Snapshot ID not supplied."
        }
    }

}
catch {

    $result.SnapshotValidation = "FAIL"
    $result.Details += $_.Exception.Message
}

return [PSCustomObject]$result
}