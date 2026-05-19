#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Install AD DS and create a new forest (student lab script).
.PARAMETER DomainName
    DNS domain name, e.g. lab.local
.PARAMETER SafeModePassword
    DSRM password (Directory Services Restore Mode).
.NOTES
    Run on the DC instance only, after Terraform apply and RDP login.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$DomainName = "lab.local",

    [Parameter(Mandatory = $true)]
    [SecureString]$SafeModePassword
)

$ErrorActionPreference = "Stop"

Write-Host "=== AD DS installation (new forest) ===" -ForegroundColor Cyan
Write-Host "Domain: $DomainName"
Write-Host "Computer: $env:COMPUTERNAME"

$features = @("AD-Domain-Services", "DNS", "RSAT-AD-PowerShell", "GPMC")
Write-Host "Installing Windows features..."
Install-WindowsFeature -Name $features -IncludeManagementTools

Import-Module ADDSDeployment

Write-Host "Promoting server to Domain Controller (this takes several minutes)..."
Install-ADDSForest `
    -DomainName $DomainName `
    -DomainMode Win2016 `
    -ForestMode Win2016 `
    -InstallDns:$true `
    -SafeModeAdministratorPassword $SafeModePassword `
    -Force:$true `
    -NoRebootOnCompletion:$false

Write-Host "Server will reboot. After reboot, log in as LAB\Administrator (domain) or verify with:"
Write-Host "  Get-ADDomain"
Write-Host "  Resolve-DnsName $DomainName"
