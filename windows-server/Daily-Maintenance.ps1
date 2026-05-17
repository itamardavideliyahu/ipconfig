#Requires -Version 5.1
<#
.SYNOPSIS
    Simple daily Windows Server health check (training script).
.DESCRIPTION
    Read-only checks: OS info, disks, services, network, recent event log errors.
    Saves a report under logs\ next to this script.
.NOTES
    Run as Administrator for full Event Log access (optional for other checks).
    If blocked: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
#>

$LogDir = Join-Path $PSScriptRoot "logs"
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir | Out-Null
}
$LogFile = Join-Path $LogDir ("maintenance_{0:yyyyMMdd_HHmmss}.log" -f (Get-Date))

function Write-Report {
    param([string]$Text)
    Write-Host $Text
    Add-Content -Path $LogFile -Value $Text -Encoding UTF8
}

Write-Report "========================================"
Write-Report "  Daily Maintenance Report"
Write-Report "  $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Report "========================================"
Write-Report ""

Write-Report "--- System ---"
Write-Report "Computer: $env:COMPUTERNAME"
Write-Report "User:     $env:USERNAME"

$os = Get-CimInstance Win32_OperatingSystem
Write-Report "OS:       $($os.Caption)"
Write-Report "Version:  $($os.Version)"

$uptime = (Get-Date) - $os.LastBootUpTime
Write-Report ("Uptime:   {0} days, {1} hours, {2} minutes" -f $uptime.Days, $uptime.Hours, $uptime.Minutes)
Write-Report ""

Write-Report "--- Disk space (GB) ---"
Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | ForEach-Object {
    $freeGB  = [math]::Round($_.FreeSpace / 1GB, 2)
    $totalGB = [math]::Round($_.Size / 1GB, 2)
    $usedPct = if ($_.Size -gt 0) { [math]::Round((1 - $_.FreeSpace / $_.Size) * 100, 1) } else { 0 }
    $status  = if ($usedPct -ge 90) { " [LOW SPACE]" } else { " [OK]" }
    Write-Report ("Drive {0}: {1} GB free of {2} GB ({3} pct used){4}" -f `
        $_.DeviceID, $freeGB, $totalGB, $usedPct, $status)
}
Write-Report ""

Write-Report "--- Services ---"
$services = @(
    "EventLog",
    "LanmanServer",
    "LanmanWorkstation",
    "W32Time",
    "Dnscache",
    "Spooler"
)
foreach ($name in $services) {
    $svc = Get-Service -Name $name -ErrorAction SilentlyContinue
    if ($svc) {
        $mark = if ($svc.Status -eq "Running") { "[OK]" } else { "[!]" }
        Write-Report ("{0} {1}: {2}" -f $mark, $svc.Name, $svc.Status)
    }
    else {
        Write-Report "[?] $name : not found"
    }
}
Write-Report ""

Write-Report "--- Network ---"
$gateway = (Get-NetRoute -DestinationPrefix "0.0.0.0/0" -ErrorAction SilentlyContinue |
    Sort-Object RouteMetric |
    Select-Object -First 1).NextHop
if ($gateway) {
    Write-Report "Gateway: $gateway"
    if (Test-Connection -ComputerName $gateway -Count 2 -Quiet) {
        Write-Report "[OK] Ping to gateway succeeded"
    }
    else {
        Write-Report "[!] Ping to gateway failed"
    }
}
else {
    Write-Report "[?] No default gateway found"
}

if (Test-Connection -ComputerName "8.8.8.8" -Count 2 -Quiet) {
    Write-Report "[OK] Ping to 8.8.8.8 succeeded"
}
else {
    Write-Report "[!] No reply from 8.8.8.8"
}
Write-Report ""

Write-Report "--- Last 5 System errors/warnings (24h) ---"
try {
    $errors = Get-WinEvent -FilterHashtable @{
        LogName   = "System"
        Level     = 2, 3
        StartTime = (Get-Date).AddHours(-24)
    } -MaxEvents 5 -ErrorAction Stop
    foreach ($e in $errors) {
        Write-Report ("{0} | {1} | Source: {2}" -f $e.TimeCreated, $e.LevelDisplayName, $e.ProviderName)
    }
    if (-not $errors) {
        Write-Report "[OK] No errors/warnings in the last 24 hours"
    }
}
catch {
    Write-Report "[?] Could not read Event Log (try Run as Administrator)"
}
Write-Report ""

Write-Report "========================================"
Write-Report "Done. Log saved to:"
Write-Report $LogFile
Write-Report "========================================"
