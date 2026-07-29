function Start-Restore {

    # Repository
    $Repo = "azure:restic-kedarwin:/"

    # Restore destination
    $RestorePath = "C:\RestoreTest"

    $ResticExe = " C:\Users\user\AppData\Local\Microsoft\WinGet\Links\restic.exe"

    Write-BackupLog "Restore started"

    if (Test-Path $RestorePath) {
        Remove-Item $RestorePath -Recurse -Force
    }

    New-Item -ItemType Directory -Path $RestorePath -Force | Out-Null

    $Output = & $ResticExe -r $Repo restore latest --target $RestorePath 2>&1

    $ExitCode = $LASTEXITCODE

    $Output | ForEach-Object {
        Write-BackupLog $_
    }

    if ($ExitCode -eq 0) {
        Write-BackupLog "Restore successful"
    }
    else {
        Write-BackupLog "Restore FAILED with exit code $ExitCode"
    }
}