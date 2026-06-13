# מדריך: הקמת Windows Server + Active Directory ב-AWS
### קורס: AWS & Windows Server AD

---

## סקירה כללית

במעבדה זו נקים שני instances ב-AWS:

| Instance | תפקיד | מערכת הפעלה |
|----------|--------|--------------|
| **DC01** | Domain Controller (שרת AD) | Windows Server 2022 |
| **WS01** | Workstation (תחנת עבודה) | Windows Server 2022 / Windows 10 |

**ארכיטקטורה:**

```
AWS VPC (10.0.0.0/16)
  └── Subnet ציבורית (10.0.1.0/24)
        ├── DC01 – Domain Controller  [IP פרטי: 10.0.1.10]
        └── WS01 – Workstation        [IP פרטי: 10.0.1.20]
```

---

## חלק 1 – הכנת סביבת AWS

### שלב 1.1 – יצירת VPC ו-Subnet

1. היכנסו ל-**AWS Console** → **VPC** → **Create VPC**
2. הגדירות:
   - **Name:** `AD-Lab-VPC`
   - **IPv4 CIDR:** `10.0.0.0/16`
3. צרו **Subnet**:
   - **Name:** `AD-Lab-Subnet`
   - **VPC:** `AD-Lab-VPC`
   - **CIDR:** `10.0.1.0/24`
   - **Availability Zone:** בחרו כלשהי (למשל `eu-west-1a`)
4. צרו **Internet Gateway**, חברו אותו ל-VPC, ועדכנו את **Route Table** להכיל:
   - `0.0.0.0/0 → igw-xxxxxxxx`

---

### שלב 1.2 – מציאת ה-IP הציבורי שלכם

לפני הגדרת ה-Security Group, עליכם לדעת מה ה-IP הציבורי שלכם.

**אופציה א' – PowerShell:**
```powershell
(Invoke-WebRequest -Uri "https://api.ipify.org").Content
```

**אופציה ב' – דפדפן:**
היכנסו ל-[https://whatismyip.com](https://whatismyip.com)

> שמרו את ה-IP שקיבלתם — תצטרכו אותו בשלב הבא.

---

### שלב 1.3 – Security Group

צרו Security Group בשם `AD-Lab-SG` עם חוקי **Inbound** הבאים:

| Protocol | Port | Source | מטרה |
|----------|------|--------|------|
| RDP | 3389 | `YOUR_IP/32` | גישה מרחוק |
| All traffic | All | `10.0.1.0/24` | תקשורת פנימית בין ה-instances |
| ICMP | All | `10.0.1.0/24` | ping בתוך הרשת |

**דוגמה:** אם ה-IP שלכם הוא `84.229.15.42` → הכניסו בשדה Source: `84.229.15.42/32`

> **/32 = רק ה-IP שלכם בלבד — הכי מאובטח.**  
> **אבטחה:** אל תפתחו RDP ל-`0.0.0.0/0` בסביבת ייצור. לצורך המעבדה השתמשו ב-IP שלכם בלבד.

---

## חלק 2 – הקמת DC01 (Domain Controller)

### שלב 2.1 – השקת Instance

1. **EC2** → **Launch Instance**
2. הגדרות:
   - **Name:** `DC01`
   - **AMI:** `Windows Server 2022 Base`
   - **Instance type:** `t3.medium` (מינימום 2 vCPU, 4GB RAM לAD)
   - **Key Pair:** צרו או בחרו Key Pair קיים
   - **Network:** `AD-Lab-VPC` | **Subnet:** `AD-Lab-Subnet`
   - **Auto-assign Public IP:** Enable
   - **Security Group:** `AD-Lab-SG`
3. ב-**Advanced Details** → **User Data** (אופציונלי, להגדרת IP סטטי אוטומטית):

```powershell
<powershell>
# הגדרת IP פרטי סטטי
$adapter = Get-NetAdapter | Where-Object {$_.Status -eq "Up"}
New-NetIPAddress -InterfaceAlias $adapter.Name -IPAddress 10.0.1.10 -PrefixLength 24 -DefaultGateway 10.0.1.1
Set-DnsClientServerAddress -InterfaceAlias $adapter.Name -ServerAddresses 127.0.0.1
</powershell>
```

4. לחצו **Launch Instance**

---

### שלב 2.2 – התחברות ל-DC01

1. המתינו ~3-5 דקות עד שה-instance יהיה במצב `Running`
2. **EC2** → בחרו את DC01 → **Connect** → **RDP Client**
3. לחצו **Get Password** → העלו את קובץ ה-Key Pair → **Decrypt Password**
4. פתחו **Remote Desktop Connection** עם:
   - **Computer:** ה-Public IP של DC01
   - **Username:** `Administrator`
   - **Password:** הסיסמה שהתקבלה

---

### שלב 2.3 – הגדרת IP סטטי (בתוך Windows)

פתחו **PowerShell** כ-Administrator:

```powershell
# בדיקת שם המתאם
Get-NetAdapter

# הגדרת IP סטטי (החליפו את שם המתאם בהתאם)
$adapterName = "Ethernet"
New-NetIPAddress `
    -InterfaceAlias $adapterName `
    -IPAddress 10.0.1.10 `
    -PrefixLength 24 `
    -DefaultGateway 10.0.1.1

# הגדרת DNS לעצמו (כי DC יהיה DNS Server)
Set-DnsClientServerAddress `
    -InterfaceAlias $adapterName `
    -ServerAddresses 127.0.0.1

# שינוי שם המחשב
Rename-Computer -NewName "DC01" -Restart
```

> ה-instance יתחיל מחדש. התחברו שוב לאחר ~2 דקות.

---

### שלב 2.4 – התקנת Active Directory Domain Services

התחברו שוב ל-DC01 ופתחו PowerShell כ-Administrator:

```powershell
# התקנת תפקיד AD DS
Install-WindowsFeature `
    -Name AD-Domain-Services `
    -IncludeManagementTools

# בדיקת ההתקנה
Get-WindowsFeature AD-Domain-Services
```

---

### שלב 2.5 – הקמת Forest ו-Domain חדשים

```powershell
# ייבוא Module
Import-Module ADDSDeployment

# הקמת Forest חדש
Install-ADDSForest `
    -DomainName "corp.lab" `
    -DomainNetbiosName "CORP" `
    -ForestMode "WinThreshold" `
    -DomainMode "WinThreshold" `
    -InstallDns:$true `
    -DatabasePath "C:\Windows\NTDS" `
    -LogPath "C:\Windows\NTDS" `
    -SysvolPath "C:\Windows\SYSVOL" `
    -SafeModeAdministratorPassword (ConvertTo-SecureString "P@ssw0rd123!" -AsPlainText -Force) `
    -Force:$true
```

> **הערה:** ניתן לשנות את `corp.lab` לשם דומיין אחר לפי בחירתכם.  
> לאחר הרצת הפקודה ה-instance יתחיל מחדש אוטומטית.

---

### שלב 2.6 – אימות הקמת הדומיין

לאחר ה-restart, התחברו עם:
- **Username:** `CORP\Administrator`
- **Password:** הסיסמה שהגדרתם

פתחו PowerShell ובדקו:

```powershell
# בדיקת הדומיין
Get-ADDomain

# בדיקת שירות AD
Get-Service ADWS, NTDS, Netlogon, DNS | Select Name, Status

# בדיקת DNS
Resolve-DnsName corp.lab
```

---

### שלב 2.7 – יצירת יוזרים ב-Active Directory

```powershell
# יצירת Organizational Unit
New-ADOrganizationalUnit -Name "Students" -Path "DC=corp,DC=lab"

# יצירת משתמש לדוגמה
New-ADUser `
    -Name "Student01" `
    -GivenName "Student" `
    -Surname "01" `
    -SamAccountName "student01" `
    -UserPrincipalName "student01@corp.lab" `
    -Path "OU=Students,DC=corp,DC=lab" `
    -AccountPassword (ConvertTo-SecureString "Student@123" -AsPlainText -Force) `
    -Enabled $true `
    -PasswordNeverExpires $true

# אימות יצירת המשתמש
Get-ADUser -Identity student01
```

---

## חלק 3 – הקמת WS01 (תחנת עבודה)

### שלב 3.1 – השקת Instance

1. **EC2** → **Launch Instance**
2. הגדרות:
   - **Name:** `WS01`
   - **AMI:** `Windows Server 2022 Base` (או Windows 10 אם זמין)
   - **Instance type:** `t3.small`
   - **Network:** `AD-Lab-VPC` | **Subnet:** `AD-Lab-Subnet`
   - **Auto-assign Public IP:** Enable
   - **Security Group:** `AD-Lab-SG`
3. לחצו **Launch Instance**

---

### שלב 3.2 – הגדרת IP ו-DNS על WS01

התחברו ל-WS01 דרך RDP (אותו תהליך כמו DC01) ופתחו PowerShell כ-Administrator:

```powershell
# הגדרת IP סטטי
$adapterName = "Ethernet"
New-NetIPAddress `
    -InterfaceAlias $adapterName `
    -IPAddress 10.0.1.20 `
    -PrefixLength 24 `
    -DefaultGateway 10.0.1.1

# הגדרת DNS לכתובת DC01 – חשוב מאוד!
Set-DnsClientServerAddress `
    -InterfaceAlias $adapterName `
    -ServerAddresses 10.0.1.10

# שינוי שם המחשב
Rename-Computer -NewName "WS01" -Restart
```

> ה-instance יתחיל מחדש. התחברו שוב לאחר ~2 דקות.

---

### שלב 3.3 – בדיקת קישוריות ל-DC01

לאחר ה-restart, התחברו שוב ל-WS01 ובדקו:

```powershell
# Ping ל-DC01
Test-Connection 10.0.1.10 -Count 3

# בדיקת DNS – אמור להחזיר את DC01
Resolve-DnsName corp.lab

# בדיקת הדומיין זמין
nltest /dsgetdc:corp.lab
```

אם ה-Ping עובד אך ה-DNS לא מגיב — בדקו שה-DNS Server מוגדר ל-`10.0.1.10`.

---

### שלב 3.4 – חיבור WS01 לדומיין

```powershell
# הצטרפות לדומיין
Add-Computer `
    -DomainName "corp.lab" `
    -Credential (Get-Credential) `
    -Restart
```

> בחלון ה-Credential: הכניסו `CORP\Administrator` וסיסמת הדומיין.  
> ה-instance יתחיל מחדש אוטומטית.

---

### שלב 3.5 – כניסה עם משתמש דומיין

לאחר ה-restart, התחברו ל-WS01 עם:
- **Username:** `CORP\student01`
- **Password:** `Student@123`

לאימות בתוך Windows:

```powershell
# בדיקת חברות בדומיין
(Get-WmiObject Win32_ComputerSystem).Domain

# בדיקת המשתמש הנוכחי
whoami

# בדיקת קישוריות ל-DC
nltest /sc_query:corp.lab
```

---

## חלק 4 – ניהול AD מ-DC01

### פקודות שימושיות לניהול

```powershell
# הצגת כל המחשבים בדומיין
Get-ADComputer -Filter * | Select Name, DNSHostName, Enabled

# הצגת כל המשתמשים
Get-ADUser -Filter * | Select Name, SamAccountName, Enabled

# הצגת כל ה-OUs
Get-ADOrganizationalUnit -Filter * | Select Name, DistinguishedName

# הוספת משתמש לקבוצה
Add-ADGroupMember -Identity "Domain Users" -Members "student01"

# איפוס סיסמה למשתמש
Set-ADAccountPassword `
    -Identity "student01" `
    -NewPassword (ConvertTo-SecureString "NewPass@456" -AsPlainText -Force) `
    -Reset
```

### פתיחת כלי ניהול גרפיים

```powershell
# Active Directory Users and Computers
dsa.msc

# DNS Manager
dnsmgmt.msc

# Group Policy Management
gpmc.msc

# Active Directory Sites and Services
dssite.msc
```

---

## חלק 5 – פתרון בעיות נפוצות

### בעיה: WS01 לא מוצאת את הדומיין

```powershell
# בדיקת DNS
Get-DnsClientServerAddress
nslookup corp.lab 10.0.1.10

# בדיקת Security Group – האם פורט 53 (DNS) פתוח?
# בדיקת Security Group – האם All Traffic בין instances פתוח?
```

**פתרון:** ודאו ש-Security Group מאפשר All Traffic מ-`10.0.1.0/24` לשני ה-instances.

---

### בעיה: שגיאת RDP "The connection was denied"

**פתרון:** בדקו שהפורט 3389 פתוח ב-Security Group ל-IP שלכם.

---

### בעיה: "The domain controller is not available"

```powershell
# ב-DC01 – בדיקת שירותים
Get-Service NTDS, Netlogon, DNS | Select Name, Status
Start-Service NTDS, Netlogon, DNS
```

---

### בעיה: שגיאת אימות בהצטרפות לדומיין

- ודאו שה-DNS של WS01 מצביע ל-`10.0.1.10` (DC01)
- ודאו שה-Credential שהכנסתם הוא `CORP\Administrator`
- בדקו שהשעה ב-instances מסונכרנת (Kerberos רגיש לפרשי שעה > 5 דקות)

```powershell
# סנכרון שעה
w32tm /resync /force
```

---

## סיכום – רשימת בדיקה (Checklist)

### DC01
- [ ] IP סטטי: `10.0.1.10`
- [ ] DNS: `127.0.0.1`
- [ ] שם מחשב: `DC01`
- [ ] תפקיד AD DS מותקן
- [ ] Forest ו-Domain `corp.lab` הוקמו
- [ ] DNS עובד מקומית

### WS01
- [ ] IP סטטי: `10.0.1.20`
- [ ] DNS: `10.0.1.10` (DC01)
- [ ] שם מחשב: `WS01`
- [ ] Ping לDC01 עובד
- [ ] DNS מחזיר `corp.lab`
- [ ] WS01 מחוברת לדומיין `corp.lab`
- [ ] כניסה עם משתמש דומיין עובדת

---

## מידע נוסף

| נושא | פקודה / כלי |
|------|-------------|
| ניהול AD גרפי | `dsa.msc` |
| ניהול DNS | `dnsmgmt.msc` |
| Group Policy | `gpmc.msc` |
| בדיקת דומיין | `nltest /dsgetdc:corp.lab` |
| בדיקת Replication | `repadmin /replsummary` |
| לוגים של AD | Event Viewer → Windows Logs → System / Security |

---

*מדריך זה נועד לצרכי הוראה בלבד בסביבת מעבדה. אל תשתמשו בהגדרות אלו בסביבת ייצור.*
