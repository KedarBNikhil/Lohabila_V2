function Upload-Artifact {

    param(
        [Parameter(Mandatory)]
        [string]$File,

        [string]$BlobFolder = "reports"
    )

$StorageAccount = Get-DPAPISecret -Path $script:BackupConfig.Secrets.AzureAccountName
$StorageKey     = Get-DPAPISecret -Path $script:BackupConfig.Secrets.AzureAccountKey
$SasToken       = Get-DPAPISecret -Path $script:BackupConfig.Secrets.SasToken

$AzCopy = $script:BackupConfig.Tools.AzCopyExe

    if (!(Test-Path $AzCopy)) {
        throw "AzCopy not found."
    }

    $env:AZCOPY_ACCOUNT_NAME = $StorageAccount
    $env:AZCOPY_ACCOUNT_KEY  = $StorageKey
    $Container = $script:BackupConfig.Azure.Container

    $BlobName = "$BlobFolder/$(Split-Path $File -Leaf)"

    $Destination = "https://$StorageAccount.blob.core.windows.net/$Container/$BlobName`?$SasToken"

    & $AzCopy copy `
        $File `
        $Destination `
        --overwrite=true

    if ($LASTEXITCODE -ne 0) {
        throw "AzCopy upload failed."
    }
}