# מעבדת Active Directory — הצטרפות לדומיין (AWS)

## רקע

Terraform מקים **תשתית בלבד**: VPC, רשת, Security Group, ושתי מכונות **Windows Server 2022** ב-AWS.  
את **Active Directory** וה-**Domain Join** אתם מגדירים ידנית — כך לומדים מה באמת קורה מאחורי הקלעים.

> בייצור, מחשב "לקוח" הוא לרוב Windows 10/11. במעבדה זו שתי מכונות Server — אותו עיקרון join, פשוט יותר ב-AWS.

---

## דרישות מוקדמות

- חשבון AWS עם הרשאות EC2/VPC
- Terraform מותקן (>= 1.5)
- AWS CLI מוגדר (`aws configure`)
- Key Pair באזור שבחרתם
- קובץ `terraform.tfvars` ממולא (ראו `terraform.tfvars.example`)

---

## שלב 0 — פריסת תשתית (Terraform)

```powershell
cd terraform/aws-domain-lab
copy terraform.tfvars.example terraform.tfvars
# ערכו admin_cidr ו-key_pair_name

terraform init
terraform plan
terraform apply
```

שמרו את ה-outputs:

```powershell
terraform output
```

חשוב במיוחד:
- `dc_public_ip` / `member_public_ip` — ל-RDP
- `dc_private_ip` — ל-DNS ו-join

### קבלת סיסמת Administrator

המתינו **4–5 דקות** אחרי עליית המכונות, ואז:

```powershell
aws ec2 get-password-data `
  --region eu-west-1 `
  --instance-id <DC_INSTANCE_ID> `
  --priv-file C:\path\to\your-key.pem
```

או: AWS Console → EC2 → Instance → Connect → Get Windows password.

---

## שלב 1 — אימות חיבוריות (לפני AD)

התחברו ב-RDP לשתי המכונות (`mstsc`).

על **DC**, ב-PowerShell:

```powershell
ping <member_private_ip>
Test-NetConnection <member_private_ip> -Port 3389
```

על **Member**:

```powershell
ping <dc_private_ip>
Test-NetConnection <dc_private_ip> -Port 3389
```

אם ping נכשל — בדקו Security Group ו-Windows Firewall לפני שממשיכים.

---

## פורטי Active Directory (תיאוריה)

| פורט | פרוטוקול | שימוש |
|------|----------|--------|
| 53 | TCP/UDP | DNS |
| 88 | TCP/UDP | Kerberos |
| 135 | TCP | RPC |
| 389 | TCP/UDP | LDAP |
| 445 | TCP | SMB |
| 636 | TCP | LDAPS |
| 3268/3269 | TCP | Global Catalog |

במעבדה, Terraform פותח תעבורה מלאה **בין מכונות באותו Security Group** (`self`). בייצור מצמצמים לפורטים הנדרשים בלבד.

---

## שלב 2 — התקנת Domain Controller

על מכונת **DC** בלבד, העתיקו את `scripts/01-install-ad-dc.ps1` והריצו ב-PowerShell **כמנהל**:

```powershell
$safe = Read-Host "DSRM password" -AsSecureString
.\01-install-ad-dc.ps1 -DomainName "lab.local" -SafeModePassword $safe
```

השרת יאתחל. אחרי האתחול התחברו שוב ב-RDP ובדקו:

```powershell
Get-ADDomain
Get-Service ADWS, NTDS, DNS
```

---

## שלב 3 — הצטרפות Member לדומיין

על מכונת **Member**, הריצו `02-configure-dns-and-join.ps1`:

```powershell
$cred = Get-Credential   # LAB\Administrator + סיסמה
.\02-configure-dns-and-join.ps1 `
    -DomainName "lab.local" `
    -DcIpAddress "<dc_private_ip>" `
    -Credential $cred
```

אחרי reboot, התחברו כמשתמש דומיין ובדקו:

```powershell
systeminfo | findstr /B /C:"Domain"
nltest /dsgetdc:lab.local
```

---

## תרגילים

1. צרו OU בשם `Students` ב-ADUC ומשתמש `student01`.
2. הוסיפו את `student01` לקבוצת `Domain Users` ובדקו התחברות מה-Member.
3. הריצו את סקריפט התחזוקה מ-[windows-server/Windows-Server-Maintenance.md](../../../windows-server/Windows-Server-Maintenance.md) על שתי המכונות.
4. רשמו בטבלה: מה ההבדל בין `dc_private_ip` ל-`dc_public_ip`?

---

## ניקוי (חובה)

```powershell
terraform destroy
```

שתי מכונות `t3.large` עולות כסף כל שעה שהן פעילות.

---

## קישורים

- [README של Terraform](../README.md)
- [מעבדת CMD](../../../cmd/CMD_Lab_Day1.md)
- [מעבדת PowerShell](../../../powershell/PS_Lab_Day1.md)
