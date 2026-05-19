#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Point DNS to the DC and join the domain (student lab script).
.PARAMETER DomainName
    DNS domain name, e.g. lab.local
.PARAMETER DcIpAddress
    Private IP of the Domain Controller (from terraform output dc_private_ip).
.PARAMETER Credential
    Domain administrator credential (LAB\Administrator).
.NOTES
    Run on the MEMBER instance only, after the DC is promoted and DNS works.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$DomainName = "lab.local",

    [Parameter(Mandatory = $true)]
    [string]$DcIpAddress,

    [Parameter(Mandatory = $true)]
    [PSCredential]$Credential
)

$ErrorActionPreference = "Stop"

Write-Host "=== Domain join ===" -ForegroundColor Cyan
Write-Host "Domain:     $DomainName"
Write-Host "DC DNS IP:  $DcIpAddress"
Write-Host "Computer:   $env:COMPUTERNAME"

$adapter = Get-NetAdapter | Where-Object Status -eq "Up" | Select-Object -First 1
if (-not $adapter) {
    throw "No active network adapter found."
}

Write-Host "Setting DNS server on adapter $($adapter.Name)..."
Set-DnsClientServerAddress -InterfaceIndex $adapter.ifIndex -ServerAddresses $DcIpAddress

Write-Host "Testing DNS to DC..."
$dnsTest = Resolve-DnsName -Name $DomainName -Server $DcIpAddress -ErrorAction SilentlyContinue
if (-not $dnsTest) {
    Write-Warning "DNS lookup for $DomainName failed. Verify the DC is up and AD DNS is running."
}

Write-Host "Joining domain (reboot required)..."
Add-Computer -DomainName $DomainName -Credential $Credential -Restart -Force
