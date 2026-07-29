function Invoke-PreFlightChecks {

    $results = @()

    # Run all checks (we will plug them in)
  $Checks = @(
    "Test-InternetConnectivity",
    "Test-AzureConnectivity",
    "Test-DiskSpace"
)

foreach ($Check in $Checks) {
    $results += & $Check
}

foreach ($r in $results) {
    Write-PreFlightLog $r
}

    # Evaluate results
$criticalFailures = @(
    $results | Where-Object {
        $_.Passed -eq $false -and $_.Severity -eq "Critical"
    }
)

$warnings = @(
    $results | Where-Object {
        $_.Passed -eq $false -and $_.Severity -eq "Warning"
    }
)
    # Log summary
    Write-Host "PreFlight Summary:"
    $results | ForEach-Object {
        Write-Host "$($_.Name): $($_.Passed) - $($_.Message)"
    }

    if ($criticalFailures.Count -gt 0) {
        throw "PreFlight failed. Critical checks did not pass."
    }

    return [PSCustomObject]@{

    Passed = ($criticalFailures.Count -eq 0)

    Results = $results

    CriticalFailures = $criticalFailures

    Warnings = $warnings
}
}

# Testing Internet

function Test-InternetConnectivity {

    try {
        $ping = Test-Connection -ComputerName "8.8.8.8" -Count 1 -Quiet

        if ($ping) {
            return [PSCustomObject]@{
                Name     = "Internet Connectivity"
                Passed   = $true
                Severity = "Critical"
                Message  = "Internet reachable"
            }
        }
        else {
            return [PSCustomObject]@{
                Name     = "Internet Connectivity"
                Passed   = $false
                Severity = "Critical"
                Message  = "No internet connectivity"
            }
        }
    }
    catch {
        return [PSCustomObject]@{
            Name     = "Internet Connectivity"
            Passed   = $false
            Severity = "Critical"
            Message  = $_.Exception.Message
        }
    }
}

#Testing Azure Connection

function Test-AzureConnectivity {

    try {
        $result = Test-NetConnection "login.microsoftonline.com" -Port 443

        if ($result.TcpTestSucceeded) {
            return [PSCustomObject]@{
                Name     = "Azure Connectivity"
                Passed   = $true
                Severity = "Critical"
                Message  = "Azure endpoint reachable"
            }
        }

        return [PSCustomObject]@{
            Name     = "Azure Connectivity"
            Passed   = $false
            Severity = "Critical"
            Message  = "Cannot reach Azure"
        }
    }
    catch {
        return [PSCustomObject]@{
            Name     = "Azure Connectivity"
            Passed   = $false
            Severity = "Critical"
            Message  = $_.Exception.Message
        }
    }
}

#Disk space

function Test-DiskSpace {

    $drive = "D:\"

    $freeGB = (Get-PSDrive D).Free / 1GB

    if ($freeGB -gt 1) {
        return [PSCustomObject]@{
            Name     = "Disk Space"
            Passed   = $true
            Severity = "Critical"
            Message  = "Sufficient space: $([math]::Round($freeGB,2)) GB"
        }
    }

    return [PSCustomObject]@{
        Name     = "Disk Space"
        Passed   = $false
        Severity = "Critical"
        Message  = "Low disk space: $([math]::Round($freeGB,2)) GB"
    }
}

function Write-PreFlightLog {
    param($Check)

    Write-BackupLog "[PREFLIGHT] $($Check.Name) | Passed: $($Check.Passed) | $($Check.Message)"
}

