function EmailBackupReport {

    param(
        [Parameter(Mandatory = $true)]
        [string]$ReportPath,

        [Parameter(Mandatory = $true)]
        [string]$CustomerEmail,

        [Parameter(Mandatory = $true)]
        [string]$ApiKey,

        [string]$FromEmail = "backup-agent@yourcompany.com",
        [string]$Subject = "Backup Report"
    )

$ApiKey = $env:EMAILREPORT_APIKEY

    if (!(Test-Path $ReportPath)) {
        throw "Report file not found: $ReportPath"
    }

    $ReportContent = Get-Content -Path $ReportPath -Raw

    # ---- API Payload (SendGrid-style structure) ----
    $Body = @{
        personalizations = @(
            @{
                to = @(
                    @{ email = $CustomerEmail }
                )
                subject = $Subject
            }
        )
        from = @{
            email = $FromEmail
        }
        content = @(
            @{
                type  = "text/plain"
                value = $ReportContent
            }
        )
    } | ConvertTo-Json -Depth 10

    # ---- HTTP Request ----
    try {
        $Response = Invoke-RestMethod `
            -Uri "https://api.sendgrid.com/v3/mail/send" `
            -Method Post `
            -Headers @{
                Authorization = "Bearer $ApiKey"
                "Content-Type" = "application/json"
            } `
            -Body $Body

        Write-Host "Email sent successfully to $CustomerEmail"
    }
    catch {
        Write-Host "Email sending failed: $($_.Exception.Message)"
        throw
    }
}