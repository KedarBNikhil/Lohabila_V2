param(
    [Parameter(Mandatory)]
    [string]$ConfigFile
)
Write-Host "===== INSTALL.PS1 ====="
Write-Host $PSCommandPath

# Import installer module
. "$PSScriptRoot\InstallerModule.ps1"

# Package source is simply the extracted folder
$script:InstallerConfig.PackageSourceRoot = Split-Path $PSScriptRoot -Parent

Import-InstallerConfiguration -ConfigFile $ConfigFile

Write-Host "======================================="
Write-Host "      Backup Agent Installer"
Write-Host "======================================="
Write-Host ""

if (-not (Test-Administrator)) {

    Write-Host "ERROR: Please run this installer as Administrator."

    exit 1
}

Write-Host "Administrator privileges verified."

if (-not (Test-PowerShellVersion)) {

    Write-Host "ERROR: PowerShell 5.1 or later is required."

    exit 1
}

Write-Host "PowerShell version verified."

$InstallationState = Get-InstallationState

Write-Host "Installation State : $InstallationState"

if (-not (Test-InstallationPath)) {

    Write-Host "ERROR: Installation path validation failed."

    exit 1
}

Write-Host "Installation path verified."

Write-Host ""
Write-Host "Pre-installation checks completed successfully."

if (-not (Test-PackageIntegrity)) {

    Write-Host "ERROR: Installer package is incomplete."

    exit 1
}

Write-Host "Installer package verified."

if (-not (New-DirectoryStructure)) {

    Write-Host "ERROR: Failed to create directory structure."

    exit 1

}

Write-Host "Directory structure created."

if (-not (Set-BackupAgentSecurity)) {

    Write-Host "ERROR: Failed to apply security permissions."

    exit 1
}

Write-Host "Folder permissions applied."

if (-not (Save-EncryptedCredentials)) {

    Write-Host "Installation cancelled."

    exit 1

}

Write-Host "Credentials encrypted and stored."

if (-not (Write-RegistryInformation)) {

    Write-Host "ERROR: Failed to register Backup Agent."

    exit 1

}

Write-Host "Installation registered successfully."