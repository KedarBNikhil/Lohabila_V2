function Initialize-BackupConfiguration {

    $script:BackupConfig = @{

        RootPath = $script:InstallConfig.RootPath

        Paths = @{
            Config  = Join-Path $script:InstallConfig.RootPath "Config"
            Logs    = Join-Path $script:InstallConfig.RootPath "Logs"
            Reports = Join-Path $script:InstallConfig.RootPath "Reports"
            Temp    = Join-Path $script:InstallConfig.RootPath "Temp"
            Tools   = Join-Path $script:InstallConfig.RootPath "Tools"
        }

        Secrets = @{
            AzureAccountName = Join-Path $script:InstallConfig.RootPath "Config\azure-account-name.enc"
            AzureAccountKey  = Join-Path $script:InstallConfig.RootPath "Config\azure-account-key.enc"
            ResticPassword   = Join-Path $script:InstallConfig.RootPath "Config\restic-password.enc"
            SasToken         = Join-Path $script:InstallConfig.RootPath "Config\kedarwinartifacts.enc"
        }

        Azure = @{
            Repository = "azure:restic-v1-testing:/"
            Container  = "restic-kedarwinartifacts"
        }

        BackupSettings = @{
            BackupSources = @(
                "C:\BackupAgent"
            )
        }

        Tools = @{
            ResticExe = Join-Path $script:InstallConfig.RootPath "Tools\restic.exe"
            AzCopyExe = Join-Path $script:InstallConfig.RootPath "Tools\azcopy.exe"
        }
    }
}


function Initialize-AzureEnvironment {

    $accountName     = Get-DPAPISecret -Path $script:BackupConfig.Secrets.AzureAccountName
    $accountKey      = Get-DPAPISecret -Path $script:BackupConfig.Secrets.AzureAccountKey
    $resticPassword  = Get-DPAPISecret -Path $script:BackupConfig.Secrets.ResticPassword
    $script:Repo     = $script:BackupConfig.Azure.Repository

    $env:AZURE_ACCOUNT_NAME = $accountName
    $env:AZURE_ACCOUNT_KEY  = $accountKey
    $env:RESTIC_PASSWORD    = $resticPassword
    $env:RESTIC_REPOSITORY  = $script:Repo
}


function Test-ResticRepository {

    try {

        $env:RESTIC_PASSWORD = Get-DPAPISecret `
            -Path $script:BackupConfig.Secrets.ResticPassword

        $Output = & $script:BackupConfig.Tools.ResticExe snapshots 2>&1

        if ($LASTEXITCODE -eq 0) {
            return "RepositoryExists"
        }

        $Message = ($Output | Out-String)

        if ($Message -match "Is there a repository at the following location") {
            return "RepositoryMissing"
        }

        if ($Message -match "wrong password|no key found") {
            return "IncorrectPassword"
        }

        if ($Message -match "Account name") {
            return "AuthenticationFailed"
        }

        if ($Message -match "dial tcp|timeout|connection") {
            return "ConnectionFailed"
        }

        return "UnknownError"
    }
    finally {
        Remove-Item Env:RESTIC_PASSWORD -ErrorAction SilentlyContinue
    }
}


function Initialize-ResticRepository {

    try {

        $env:RESTIC_PASSWORD = Get-DPAPISecret `
            -Path $script:BackupConfig.Secrets.ResticPassword

        & $script:BackupConfig.Tools.ResticExe init

        if ($LASTEXITCODE -ne 0) {
            Write-Host "ERROR: Failed to initialize Restic repository."
            return $false
        }

        Write-Host "Restic repository initialized successfully."
        return $true
    }
    finally {
        Remove-Item Env:RESTIC_PASSWORD -ErrorAction SilentlyContinue
    }
}


function Ensure-ResticRepository {

    $RepositoryStatus = Test-ResticRepository

    switch ($RepositoryStatus) {

        "RepositoryExists" {
            Write-Host "Restic repository verified."
            return $true
        }

        "RepositoryMissing" {
            Write-Host "Repository not found."
            Write-Host "Initializing repository..."
            return (Initialize-ResticRepository)
        }

        "IncorrectPassword" {
            Write-Host "ERROR: Incorrect Restic repository password."
            return $false
        }

        "AuthenticationFailed" {
            Write-Host "ERROR: Azure authentication failed."
            return $false
        }

        "ConnectionFailed" {
            Write-Host "ERROR: Unable to connect to Azure."
            return $false
        }

        default {
            Write-Host "ERROR: Unknown repository status."
            return $false
        }
    }
}


function Get-DPAPISecret {
    param (
        [string]$Path
    )

    $SecureString = Get-Content $Path | ConvertTo-SecureString

    $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecureString)

    try {
        [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
    }
    finally {
        [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($BSTR)
    }
}


function Write-BackupLog {

    param (
        [string]$Message,
        [string]$Level = "INFO"
    )

    $LogFolder = $script:BackupConfig.Paths.Logs

    if (!(Test-Path $LogFolder)) {
        New-Item -ItemType Directory -Path $LogFolder -Force | Out-Null
    }

    $LogFile = Join-Path $LogFolder "backup-$(Get-Date -Format 'yyyy-MM-dd').log"
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $Line = "[$Timestamp] [$Level] $Message"

    Add-Content -Path $LogFile -Value $Line
}

Initialize-BackupConfiguration