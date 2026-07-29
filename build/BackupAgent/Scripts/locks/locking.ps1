Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# -----------------------------
# Paths (scoped, not global)
# -----------------------------
$script:LockDirectory = "C:\BackupAgent\scripts\locks"
$script:BackupLockFile = Join-Path $script:LockDirectory "backup.lock"

# -----------------------------
# Helper: Read Lock
# -----------------------------
function Get-LockData {
    if (-not (Test-Path $script:BackupLockFile)) {
        return $null
    }

    try {
        return Get-Content $script:BackupLockFile -Raw | ConvertFrom-Json
    }
    catch {
        throw "Lock file is corrupted or unreadable."
    }
}

# -----------------------------
# Helper: Check if process exists safely
# -----------------------------
function Test-ProcessAlive {
    param([int]$Pid)

    try {
        $p = Get-Process -Id $Pid -ErrorAction Stop
        return $true
    }
    catch {
        return $false
    }
}

# -----------------------------
# Test if lock is stale
# -----------------------------
function Test-StaleBackupLock {

    $lock = Get-LockData
    if (-not $lock) {
        return $true
    }

    if (-not $lock.PID) {
        return $true
    }

    $pid = [int]$lock.PID

    if (-not (Test-ProcessAlive -Pid $pid)) {
        return $true
    }

    # Validate process start time to avoid PID reuse issue
    try {
        $process = Get-Process -Id $pid -ErrorAction Stop
        $currentStart = $process.StartTime.ToUniversalTime().ToString("o")

        if ($lock.ProcessStartTime -ne $currentStart) {
            return $true
        }

        return $false
    }
    catch {
        return $true
    }
}

# -----------------------------
# Acquire Lock
# -----------------------------
function Acquire-BackupLock {

    if (-not (Test-Path $script:LockDirectory)) {
        New-Item -ItemType Directory -Path $script:LockDirectory -Force | Out-Null
    }

    $lockExists = Test-Path $script:BackupLockFile

    if ($lockExists) {

        if (Test-StaleBackupLock) {
            Remove-Item $script:BackupLockFile -Force -ErrorAction SilentlyContinue
        }
        else {
            throw [System.InvalidOperationException]::new(
                "Another backup process is already running."
            )
        }
    }

    # Create new lock
    $process = Get-Process -Id $PID

    $lockObject = [PSCustomObject]@{
        Operation        = "Backup"
        PID              = $PID
        ProcessStartTime = $process.StartTime.ToUniversalTime().ToString("o")
        StartedUtc       = (Get-Date).ToUniversalTime().ToString("o")
        Machine          = $env:COMPUTERNAME
        User             = $env:USERNAME
    }

    $lockObject | ConvertTo-Json | Set-Content $script:BackupLockFile -Encoding UTF8

    Write-Host "Backup lock acquired."
}

# -----------------------------
# Release Lock
# -----------------------------
function Release-BackupLock {

    if (Test-Path $script:BackupLockFile) {
try{
        Remove-Item $script:BackupLockFile -Force -ErrorAction SilentlyContinue
        Write-Host "Backup lock released."
    }
catch{
 Write-Host "WARNING: Failed to release lock: $($_.Exception.Message)"
        }
}
}