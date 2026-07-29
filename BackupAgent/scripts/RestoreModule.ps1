 param(
        [Parameter(Mandatory)]
        [ValidateSet("CustomerRestore", "AzureRestore")]
        [string]$Action,

        # Customer inputs
        [string]$CustomerLogPath,

        # Azure inputs
        [string]$AzureReportPath,
        [string]$AzureLogPath
    )

# Import internal components

. "$PSScriptRoot\..\Config\InstallConfig.ps1"
. "$PSScriptRoot\Common.ps1"
 Initialize-AzureEnvironment

. "$PSScriptRoot\restoreEngine.ps1"
. "$PSScriptRoot\customerBaseRestore.ps1"
. "$PSScriptRoot\azureRestore.ps1"

Write-Host "Azure environment variables configured."

    switch ($Action) {

        "CustomerRestore" {
            $ctx = Get-CustomerBaseRestore `
                -LogPath $CustomerLogPath

            return Start-RestoreEngine -SnapshotContext $ctx
        }

        "AzureRestore" {
            $ctx = Get-AzureBaseSnapshot `
                -AzureReportPath $AzureReportPath `
                -AzureLogPath $AzureLogPath

            return Start-RestoreEngine -SnapshotContext $ctx
        }
    }