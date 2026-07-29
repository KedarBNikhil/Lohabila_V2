Write-Host "===== INSTALLERMODULE.PS1 ====="
Write-Host $PSCommandPath

# Installer Configuration
$script:InstallerConfig = @{

   InstallRoot = $null
  PackageSourceRoot = $null

    Directories = @(
        "Config",
        "Logs",
        "Reports",
        "Temp",
        "Tools",
        "Modules",
        "Scripts"
    )

PackageItems = @(
    "Modules",
    "Scripts",
    "Tools"
)

Credentials = @{
    AzureAccountName = $null
    AzureAccountKey = $null
    ResticPassword = $null
    SasToken =$null
}

}

function Import-InstallerConfiguration {

    param(
        [Parameter(Mandatory)]
        [string]$ConfigFile
    )

    if (!(Test-Path $ConfigFile)) {
        throw "Configuration file not found: $ConfigFile"
    }

    $script:BackupConfig =
        Get-Content $ConfigFile -Raw |
        ConvertFrom-Json

    $script:InstallerConfig.InstallRoot =
        $script:BackupConfig.installation.install_directory

    $script:InstallerConfig.PackageSourceRoot =
    Split-Path $PSScriptRoot -Parent

if ($script:BackupConfig.repository.azure_account_name) {
    $script:InstallerConfig.Credentials.AzureAccountName =
        $script:BackupConfig.repository.azure_account_name
}

if ($script:BackupConfig.repository.azure_account_key) {
    $script:InstallerConfig.Credentials.AzureAccountKey =
        $script:BackupConfig.repository.azure_account_key
}

if ($script:BackupConfig.repository.repository_password) {
    $script:InstallerConfig.Credentials.ResticPassword =
        $script:BackupConfig.repository.repository_password
}

if ($script:BackupConfig.repository.sas_token) {
    $script:InstallerConfig.Credentials.SasToken =
        $script:BackupConfig.repository.sas_token
}
}

function Test-Administrator {

    <#
        .SYNOPSIS
            Checks whether the current PowerShell session is running with
            administrative privileges.

        .OUTPUTS
            [bool]

        .NOTES
            Returns:
                $true  - Running as Administrator
                $false - Not running as Administrator

            This function performs no installation work.
            It is intended to be reused by:
                - Install.ps1
                - Upgrade.ps1
                - Repair.ps1
    #>

    try {

        $CurrentIdentity = [Security.Principal.WindowsIdentity]::GetCurrent()

        $Principal = New-Object Security.Principal.WindowsPrincipal($CurrentIdentity)

        return $Principal.IsInRole(
            [Security.Principal.WindowsBuiltInRole]::Administrator
        )

    }
    catch {

        return $false

    }
}

function Test-PowerShellVersion {

    <#
        .SYNOPSIS
            Verifies that the installed PowerShell version meets
            the minimum requirement for Backup Agent.

        .OUTPUTS
            [bool]

        .NOTES
            Returns:
                $true  - Supported PowerShell version.
                $false - Unsupported PowerShell version.

            This function performs validation only.
    #>

    try {

        $MinimumVersion = [Version]"5.1"

        $CurrentVersion = $PSVersionTable.PSVersion

        return ($CurrentVersion -ge $MinimumVersion)

    }
    catch {

        return $false

    }
}

function Get-InstallationState {
 <#
        .SYNOPSIS
            Determines the current installation state of Backup Agent.

        .OUTPUTS
            [string]

        .RETURNS
            NotInstalled
            Installed
            Partial
    #>
    
    $Root = $script:InstallerConfig.InstallRoot
    $RequiredItems = @(
        (Join-Path $Root "Modules"),
        (Join-Path $Root "Scripts"),
        (Join-Path $Root "Config"),
        (Join-Path $Root "Config\config.json")
    )

    $Existing = 0

    foreach ($Item in $RequiredItems) {

        if (Test-Path $Item) {
            $Existing++
        }

    }

    switch ($Existing) {

        0 { return "NotInstalled" }

         $RequiredItems.Count { return "Installed" }

        default { return "Partial" }

    }

}

function Test-InstallationPath {

    <#
        .SYNOPSIS
            Validates whether the installation path is suitable.

        .OUTPUTS
            [bool]
    #>

    try {

        $InstallRoot = $script:InstallerConfig.InstallRoot

        if ([string]::IsNullOrWhiteSpace($InstallRoot)) {
            return $false
        }

        $ParentPath = Split-Path $InstallRoot -Parent

        if (-not (Test-Path $ParentPath)) {
            return $false
        }

        $TempFile = Join-Path $ParentPath ([System.Guid]::NewGuid().ToString())

        New-Item -ItemType File -Path $TempFile -Force | Out-Null

        Remove-Item $TempFile -Force

        return $true

    }
    catch {

        return $false

    }
}





function New-DirectoryStructure {

    <#
        .SYNOPSIS
            Creates the Backup Agent directory structure.

        .OUTPUTS
            [bool]
    #>

    try {

        $Root = $script:InstallerConfig.InstallRoot

        if (-not (Test-Path $Root)) {

            New-Item `
                -ItemType Directory `
                -Path $Root `
                -Force | Out-Null

        }

        foreach ($Directory in $script:InstallerConfig.Directories) {

            $FullPath = Join-Path $Root $Directory

            if (-not (Test-Path $FullPath)) {

                New-Item `
                    -ItemType Directory `
                    -Path $FullPath `
                    -Force | Out-Null

            }

        }

        return $true

    }
    catch {

        return $false

    }

}

function Set-DPAPISecret {

    <#
        .SYNOPSIS
            Encrypts and stores a secret using DPAPI.
    #>

    param(
        [Parameter(Mandatory)]
        [string]$Value,

        [Parameter(Mandatory)]
        [string]$Path
    )

    $SecureString = ConvertTo-SecureString `
        -String $Value `
        -AsPlainText `
        -Force

    $Encrypted = $SecureString | ConvertFrom-SecureString

    Set-Content `
        -Path $Path `
        -Value $Encrypted `
        -Encoding UTF8
}

function Save-EncryptedCredentials {

    <#
        .SYNOPSIS
            Saves installer credentials as DPAPI encrypted files.
    #>

    try {

        $ConfigFolder = Join-Path `
            $script:InstallerConfig.InstallRoot `
            "Config"

        $Credentials = $script:InstallerConfig.Credentials

        Set-DPAPISecret `
            -Value $Credentials.AzureAccountName `
            -Path (Join-Path $ConfigFolder "azure-account-name.enc")

        Set-DPAPISecret `
            -Value $Credentials.AzureAccountKey `
            -Path (Join-Path $ConfigFolder "azure-account-key.enc")

        Set-DPAPISecret `
            -Value $Credentials.ResticPassword `
            -Path (Join-Path $ConfigFolder "restic-password.enc")

        Set-DPAPISecret `
            -Value $Credentials.SasToken `
            -Path (Join-Path $ConfigFolder "kedarwinartifacts.enc")

        return $true

    }
    catch {

        Write-Host "ERROR: Failed to save encrypted credentials."

        Write-Host $_.Exception.Message

        return $false

    }

}

function Clear-InstallerCredentials {

    <#
        .SYNOPSIS
            Clears plaintext credentials from installer memory.
    #>

    $Credentials = $script:InstallerConfig.Credentials

    $Credentials.AzureAccountName = $null
    $Credentials.AzureAccountKey = $null
    $Credentials.ResticPassword = $null
    $Credentials.SasToken = $null
}

function Test-PackageIntegrity {

    <#
        .SYNOPSIS
            Validates that the installer package contains all required files.

        .OUTPUTS
            [bool]
    #>

    try {

        $Root = $script:InstallerConfig.PackageSourceRoot

        $RequiredItems = @(
            "Modules\Install.ps1",
            "Modules\InstallerModule.ps1",
             "Modules",
            "Scripts",
            "Tools",
            "Tools\restic.exe",
            "Tools\azcopy.exe"
        )

        $MissingItems = @()

        foreach ($Item in $RequiredItems) {

            $Path = Join-Path $Root $Item

            if (-not (Test-Path $Path)) {
                $MissingItems += $Item
            }

        }

        if ($MissingItems.Count -gt 0) {

            Write-Host ""
            Write-Host "ERROR: Package integrity validation failed."
            Write-Host ""

            foreach ($Missing in $MissingItems) {
                Write-Host "Missing: $Missing"
            }

            return $false
        }

        return $true

    }
    catch {

        Write-Host "ERROR: Package integrity validation failed."
        Write-Host $_.Exception.Message

        return $false
    }
}

function Write-RegistryInformation {

Write-Host "Inside Write-RegistryInformation"
    <#
        .SYNOPSIS
            Registers Backup Agent installation information
            in the Windows Registry.

        .OUTPUTS
            [bool]
    #>

    try {

        $RegistryPath = "HKLM:\Software\Lohabila Systems\BackupAgent"

        if (-not (Test-Path $RegistryPath)) {

            New-Item `
                -Path $RegistryPath `
                -Force | Out-Null

        }

        New-ItemProperty `
            -Path $RegistryPath `
            -Name "InstallDirectory" `
            -Value $script:InstallerConfig.InstallRoot `
            -PropertyType String `
            -Force | Out-Null

        New-ItemProperty `
            -Path $RegistryPath `
            -Name "Version" `
            -Value "2.0.0" `
            -PropertyType String `
            -Force | Out-Null

Write-Host "Registry written successfully."        
      return $true

    }
    catch {

        Write-Host "ERROR: Failed to write registry information."
        Write-Host $_.Exception.Message

        return $false

    }

}

function Set-BackupAgentSecurity {

    <#
        .SYNOPSIS
            Applies NTFS permissions to Backup Agent folders.

        .OUTPUTS
            [bool]
    #>

    try {

        $ProtectedFolders = @(
            "Config",
            "Scripts",
            "Modules"
        )

        foreach ($Folder in $ProtectedFolders) {

            $FolderPath = Join-Path `
                $script:InstallerConfig.InstallRoot `
                $Folder

            if (-not (Test-Path $FolderPath)) {
                continue
            }

            $Acl = Get-Acl $FolderPath

            # Disable inherited permissions
            $Acl.SetAccessRuleProtection($true, $false)

            # Remove existing rules
            foreach ($Rule in @($Acl.Access)) {
                $Acl.RemoveAccessRule($Rule) | Out-Null
            }

            # SYSTEM Full Control
            $SystemRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
                "SYSTEM",
                "FullControl",
                "ContainerInherit,ObjectInherit",
                "None",
                "Allow"
            )

            # Administrators Full Control
            $AdminRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
                "Administrators",
                "FullControl",
                "ContainerInherit,ObjectInherit",
                "None",
                "Allow"
            )

            # Users Read & Execute
            $UsersRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
                "Users",
                "ReadAndExecute",
                "ContainerInherit,ObjectInherit",
                "None",
                "Allow"
            )

            $Acl.AddAccessRule($SystemRule)
            $Acl.AddAccessRule($AdminRule)
            $Acl.AddAccessRule($UsersRule)

            Set-Acl `
                -Path $FolderPath `
                -AclObject $Acl

        }

        return $true

    }
    catch {

        Write-Host "ERROR: Failed to apply folder permissions."
        Write-Host $_.Exception.Message

        return $false

    }

}