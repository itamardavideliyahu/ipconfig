# מעבדת PowerShell - יום 1 (Windows)

## רקע קצר
**PowerShell** היא שפת סקריפטינג ושורת פקודה מתקדמת של Microsoft, חזקה בהרבה מ-CMD.  
בניגוד ל-CMD שעובד עם **טקסט**, PowerShell עובד עם **אובייקטים** - כלומר לכל פקודה יש מידע מובנה שאפשר לסנן, למיין ולעבד בצורה חכמה.

ב-Windows קיימות שתי דרכים לעבוד עם PS:
| סביבה | תיאור | מתי משתמשים? |
|---|---|---|
| **PowerShell Console** | חלון שחור, עבודה ישירה עם פקודות | הרצה מהירה, עבודה שוטפת |
| **PowerShell ISE** | עורך גרפי עם צבעים, עזרה ורצועת פקודות | כתיבת סקריפטים, למידה |

המעבדה מיועדת לתלמידים **ללא ניסיון קודם** ב-PowerShell.

---

## מטרות למידה
- להבין את ההבדל בין PowerShell Console ל-ISE ומתי להשתמש בכל אחד.
- להכיר את מבנה הפקודות (`Verb-Noun`) ואת מערכת העזרה המובנית.
- לנווט במערכת קבצים ולבצע פעולות בסיסיות עם קבצים ותיקיות.
- לעבוד עם אובייקטים: סינון, מיון ובחירת מאפיינים.
- לכתוב ולהריץ סקריפט `.ps1` ראשון ב-ISE.

---

## דרישות מוקדמות
- מחשב Windows 10/11 עם PowerShell 5.1 לפחות (מובנה במערכת).
- הרשאות משתמש רגיל מספיקות לרוב המשימות.
- לא נדרש ידע קודם ב-CMD, אך מועיל.

---

## חוקי מעבדה
1. עובדים רק בתוך תיקיית התרגול, לא מוחקים קבצים מחוץ אליה.
2. אחרי כל שלב - צילום מסך של הפקודות והתוצאה.
3. אם פקודה לא עובדת: לבדוק שגיאות כתיב, רווחים, ונתיב.
4. לא מעתיקים פתרון בלי לכתוב מה כל פקודה עושה.

---

## חלק א' - היכרות עם הסביבות

### פתיחת PowerShell Console
1. לחצו `Win + R`, הקלידו `powershell` ולחצו Enter.
2. לחלופין: חפשו `PowerShell` בתפריט התחל.
3. שימו לב: השורה מתחילה ב-`PS C:\Users\...>` - זהו ה-**prompt** של PS.

> **הבדל ממשי מ-CMD:** הפקודה `dir` עדיין עובדת (alias), אבל הפקודה האמיתית היא `Get-ChildItem`.

---

### פתיחת PowerShell ISE
1. חפשו `PowerShell ISE` בתפריט התחל.
2. לחלופין: ב-PowerShell Console הקלידו `ise` ולחצו Enter.

**הכרת ממשק ה-ISE:**
```
┌─────────────────────────────────────────────┐
│  Script Pane (למעלה)   ← כותבים כאן סקריפטים│
│─────────────────────────────────────────────│
│  Console Pane (למטה)   ← מריצים ורואים פלט  │
│─────────────────────────────────────────────│
│  Commands Panel (ימין) ← חיפוש פקודות      │
└─────────────────────────────────────────────┘
```

| חלק | תפקיד |
|---|---|
| **Script Pane** (למעלה) | כותבים כאן קוד/סקריפט, שומרים כ-`.ps1` |
| **Console Pane** (למטה) | שולחים פקודות בודדות, רואים תוצאות |
| **Commands Panel** (ימין) | מאגר כל הפקודות עם תיאור וחתימה |

> **טיפ ISE:** לחצו `F5` להרצת הסקריפט כולו. `F8` מריץ רק שורה מסומנת.

---

## הכנה ראשונית (5 דקות)

פתחו **PowerShell Console** והקלידו:

```powershell
$env:USERNAME
$env:COMPUTERNAME
$PSVersionTable.PSVersion
```

צרו תיקיית עבודה:

```powershell
cd $env:USERPROFILE\Desktop
New-Item -ItemType Directory -Name PS_LAB
cd PS_LAB
```

בדיקה:

```powershell
Get-Location
Get-ChildItem
```

---

## שלב 1 - מבנה פקודות ועזרה מובנית (15 דקות)

### Verb-Noun: הסוד של PowerShell
כל פקודה ב-PS בנויה כך: **פועל-עצם** (Verb-Noun).

| פועל | משמעות | דוגמה |
|---|---|---|
| `Get` | קבל/הצג מידע | `Get-Process` |
| `Set` | הגדר/שנה | `Set-Location` |
| `New` | צור חדש | `New-Item` |
| `Remove` | מחק | `Remove-Item` |
| `Copy` | העתק | `Copy-Item` |
| `Move` | הזז | `Move-Item` |

### משימות
1. הריצו `Get-Command` - ראו כמה פקודות קיימות.
2. הריצו `Get-Command Get-*` - רק פקודות שמתחילות ב-Get.
3. הריצו `Get-Help Get-Process` - קראו את תיאור הפקודה.
4. הריצו `Get-Help Get-Process -Examples` - ראו דוגמאות שימוש.
5. הריצו `Get-Alias dir` - ראו שהפקודה `dir` היא כינוי (alias).

### רמז - Aliases נפוצים
```powershell
Get-Alias dir    # -> Get-ChildItem
Get-Alias cd     # -> Set-Location
Get-Alias cls    # -> Clear-Host
Get-Alias cat    # -> Get-Content
Get-Alias echo   # -> Write-Output
```

> **חשוב:** בסקריפטים - תמיד כתבו את השם המלא (`Get-ChildItem`).  
> בקונסול - מותר להשתמש ב-aliases לנוחות.

---

## שלב 2 - ניווט במערכת קבצים (15 דקות)

### משימות
1. צרו את מבנה התיקיות הבא:

```text
PS_LAB
|-- Day1
|   |-- Notes
|   |-- Tasks
|-- Temp
```

2. עברו לתיקיית `Notes` בעזרת `Set-Location` (או `cd`).
3. הציגו את הנתיב הנוכחי עם `Get-Location` (או `pwd`).
4. חזרו תיקיה אחת אחורה: `cd ..`
5. הציגו עץ תיקיות: `Get-ChildItem -Recurse`

### פקודות אפשריות
```powershell
New-Item -ItemType Directory -Name Day1
New-Item -ItemType Directory -Path Day1\Notes
New-Item -ItemType Directory -Path Day1\Tasks
New-Item -ItemType Directory -Name Temp

cd Day1\Notes
Get-Location
cd ..
Get-ChildItem -Recurse
```

> **השווה ל-CMD:**
> | CMD | PowerShell |
> |---|---|
> | `mkdir` | `New-Item -ItemType Directory` |
> | `cd` | `Set-Location` |
> | `dir` | `Get-ChildItem` |
> | `tree` | `Get-ChildItem -Recurse` |

---

## שלב 3 - עבודה עם קבצים ותוכן (20 דקות)

### משימות
1. בתוך `Day1\Tasks`, צרו קובץ `todo.txt`.
2. הוסיפו לקובץ 3 שורות משימות.
3. הציגו את תוכן הקובץ.
4. הוסיפו שורה נוספת לקובץ קיים (ללא מחיקת התוכן).
5. העתיקו את הקובץ ל-`todo_backup.txt`.
6. שנו שם ל-`todo_day1.txt`.
7. העבירו את קובץ הגיבוי לתיקיית `Temp`.

### דוגמה
```powershell
cd Day1\Tasks

# יצירת קובץ עם תוכן
Set-Content -Path todo.txt -Value "משימה 1: ללמוד Get-Help"

# הוספת שורות (ללא מחיקה)
Add-Content -Path todo.txt -Value "משימה 2: ללמוד Get-ChildItem"
Add-Content -Path todo.txt -Value "משימה 3: ללמוד Set-Content"

# הצגת תוכן
Get-Content todo.txt

# העתקה, שינוי שם, העברה
Copy-Item todo.txt todo_backup.txt
Rename-Item todo.txt todo_day1.txt
Move-Item todo_backup.txt ..\..\Temp
```

> **הבדל חשוב:**
> - `Set-Content` = יוצר/מחליף תוכן (כמו `>` ב-CMD)
> - `Add-Content` = מוסיף תוכן לסוף הקובץ (כמו `>>` ב-CMD)

---

## שלב 4 - כוח האובייקטים: Where-Object ו-Select-Object (20 דקות)

### מה זה אובייקט ב-PS?
כשאתם מריצים `Get-Process`, PS לא מחזיר לכם טקסט - הוא מחזיר **רשימת אובייקטים**.  
לכל אובייקט יש **מאפיינים** (Properties) כמו: שם, מזהה, שימוש בזיכרון.

```
┌─────────────────────────────────────────┐
│ Get-Process -> רשימת Process Objects     │
│                                         │
│ כל Process יש לו:                       │
│   .Name     = שם התהליך                 │
│   .Id       = מזהה (PID)               │
│   .CPU      = שימוש ב-CPU              │
│   .WorkingSet = שימוש בזיכרון          │
└─────────────────────────────────────────┘
```

### ה-Pipeline: `|`
ה-**pipe** (`|`) מעביר אובייקטים מפקודה לפקודה - כמו מסוע.

```powershell
Get-Process | Where-Object {$_.Name -eq "notepad"}
#     ↑               ↑              ↑
# הפק מידע       סנן לפי תנאי    הרכיב הנוכחי
```

### משימות
1. הציגו את כל התהליכים:
   ```powershell
   Get-Process
   ```

2. הציגו רק את **שמות** התהליכים:
   ```powershell
   Get-Process | Select-Object Name
   ```

3. הציגו את **5 התהליכים שצורכים הכי הרבה CPU**:
   ```powershell
   Get-Process | Sort-Object CPU -Descending | Select-Object -First 5
   ```

4. חפשו תהליך ספציפי (לדוגמה `explorer`):
   ```powershell
   Get-Process | Where-Object { $_.Name -eq "explorer" }
   ```

5. הציגו קבצים מ-`Day1\Tasks` עם גודל קובץ:
   ```powershell
   Get-ChildItem Day1\Tasks | Select-Object Name, Length
   ```

6. מיינו קבצים לפי גודל:
   ```powershell
   Get-ChildItem Day1\Tasks | Sort-Object Length
   ```

### מפת אופרטורי השוואה ב-PS
| אופרטור | משמעות | דוגמה |
|---|---|---|
| `-eq` | שווה | `$_.Name -eq "notepad"` |
| `-ne` | לא שווה | `$_.Name -ne "svchost"` |
| `-gt` | גדול מ | `$_.CPU -gt 10` |
| `-lt` | קטן מ | `$_.Length -lt 1000` |
| `-like` | דומה ל (wildcard) | `$_.Name -like "note*"` |
| `-match` | regex | `$_.Name -match "^sys"` |

---

## שלב 5 - כתיבת סקריפט ב-ISE (20 דקות)

עברו ל-**PowerShell ISE**.

### חלק א': הרצה ישירה מ-Console Pane
ב-Console Pane (למטה) הקלידו ובדקו:
```powershell
Write-Host "שלום עולם!" -ForegroundColor Green
Write-Host "שם המחשב: $env:COMPUTERNAME" -ForegroundColor Cyan
```

### חלק ב': כתיבת סקריפט ב-Script Pane
ב-Script Pane (למעלה) כתבו את הסקריפט הבא:

```powershell
# system_info.ps1 - מידע בסיסי על המערכת
Write-Host "=== מידע מערכת ===" -ForegroundColor Yellow

Write-Host "שם משתמש:  $env:USERNAME"
Write-Host "שם מחשב:   $env:COMPUTERNAME"
Write-Host "גרסת PS:   $($PSVersionTable.PSVersion)"
Write-Host "תאריך:     $(Get-Date -Format 'dd/MM/yyyy HH:mm')"

Write-Host ""
Write-Host "=== 5 תהליכים עם הכי הרבה CPU ===" -ForegroundColor Yellow
Get-Process | Sort-Object CPU -Descending | Select-Object Name, Id, CPU -First 5

Write-Host ""
Write-Host "=== קבצים בתיקיית העבודה ===" -ForegroundColor Yellow
Get-ChildItem "$env:USERPROFILE\Desktop\PS_LAB" -Recurse | Select-Object Name, Length
```

**שמירה והרצה:**
1. שמרו: `Ctrl+S` → שמרו בתוך `PS_LAB` בשם `system_info.ps1`
2. הריצו: `F5`
3. אם מבקש הרשאת הרצה, הריצו בקונסול:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   ואז `F5` שוב.

> **הסבר ExecutionPolicy:**  
> Windows חוסם הרצת סקריפטים כברירת מחדל מטעמי אבטחה.  
> `RemoteSigned` מאפשר הרצת סקריפטים מקומיים שכתבתם אתם.

---

## שלב 6 - שמירת פלט לקבצים (10 דקות)

### שיטות שמירת פלט
```powershell
# שיטה 1: הפנייה רגילה (ממיר לטקסט)
Get-Process > processes.txt

# שיטה 2: Out-File (גמיש יותר)
Get-Process | Out-File -FilePath processes.txt

# שיטה 3: Export-Csv (לקובץ CSV - ניתן לפתוח ב-Excel!)
Get-Process | Export-Csv -Path processes.csv -NoTypeInformation

# שיטה 4: ConvertTo-Json (לפורמט JSON)
Get-Process | Select-Object Name, Id | ConvertTo-Json | Out-File processes.json
```

### משימות
1. שמרו את רשימת התהליכים לקובץ `processes.txt`.
2. שמרו את **5 התהליכים הכבדים ביותר** לקובץ `top5.txt`.
3. **בונוס:** ייצאו את התהליכים לקובץ CSV ופתחו אותו ב-Excel.

---

## שלב 7 - מיני אתגר מסכם (20 דקות)

### תרחיש
אתם "אנליסטים" שצריכים להכין דוח מערכת מסודר בפורמט PS.

### משימות
1. צרו תיקיה בשם `Report` תחת `PS_LAB`.
2. כתבו סקריפט `collect_report.ps1` ב-ISE שעושה את הבא:
   - שומר שם משתמש ושם מחשב לקובץ `identity.txt`
   - שומר את 10 התהליכים הכבדים ביותר ל-`top_processes.txt`
   - שומר רשימת ממשקי רשת ל-`network.txt`
   - מציג בסוף "הדוח הושלם!" בצבע ירוק

### תבנית להתחיל ממנה
```powershell
# collect_report.ps1

$reportPath = "$env:USERPROFILE\Desktop\PS_LAB\Report"

# --- identity ---
"משתמש: $env:USERNAME"    | Out-File "$reportPath\identity.txt"
"מחשב:  $env:COMPUTERNAME" | Add-Content "$reportPath\identity.txt"
"תאריך: $(Get-Date)"       | Add-Content "$reportPath\identity.txt"

# --- תהליכים ---
# כתבו כאן את הפקודה לשמירת 10 תהליכים כבדים ביותר לפי CPU

# --- רשת ---
Get-NetIPConfiguration | Out-File "$reportPath\network.txt"

# --- סיום ---
Write-Host "הדוח הושלם!" -ForegroundColor Green
```

3. הריצו את הסקריפט עם `F5`.
4. אמתו שהתיקיית `Report` מכילה את כל הקבצים:
   ```powershell
   Get-ChildItem "$env:USERPROFILE\Desktop\PS_LAB\Report"
   ```

---

## משימות בונוס (בסגנון "האקרי")

### בונוס 1 - Process Hunter
מצאו את כל התהליכים שצורכים יותר מ-50MB זיכרון:
```powershell
Get-Process | Where-Object { $_.WorkingSet -gt 50MB } | Select-Object Name, Id, @{Name="MB";Expression={[math]::Round($_.WorkingSet/1MB,1)}} | Sort-Object MB -Descending
```
- שמרו את הפלט ל-`heavy_processes.txt`.
- כמה תהליכים כאלה קיימים?

### בונוס 2 - File Detective
בלי `Get-ChildItem -Recurse`, מצאו ידנית תיקייה מקוננת עמוקה וחפשו קובץ:
```powershell
Get-ChildItem -Path C:\Windows -Filter "*.log" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 10
```
כמה קבצי `.log` נמצאו ב-`C:\Windows`?

### בונוס 3 - Log Analyzer
צרו קובץ `security.log` עם 15 שורות, כולל מילות מפתח `LOGIN`, `FAILED`, `SUCCESS`:
```powershell
# יצירת הלוג
$lines = @(
    "2026-05-06 08:01 LOGIN SUCCESS user=admin",
    "2026-05-06 08:05 LOGIN FAILED user=guest",
    "2026-05-06 08:10 LOGIN FAILED user=unknown",
    "2026-05-06 08:15 LOGIN SUCCESS user=john"
    # הוסיפו עוד 11 שורות בעצמכם...
)
$lines | Out-File security.log

# חלצו רק שורות FAILED
Get-Content security.log | Where-Object { $_ -match "FAILED" }
```
- כמה ניסיונות כושלים היו? השתמשו ב-`.Count`

### בונוס 4 - ISE Snippet
ב-ISE, כתבו סקריפט שמקבל **קלט מהמשתמש** ומציג ברכה:
```powershell
$name = Read-Host "הכנס את שמך"
$hour = (Get-Date).Hour
if ($hour -lt 12) {
    Write-Host "בוקר טוב, $name!" -ForegroundColor Yellow
} elseif ($hour -lt 18) {
    Write-Host "צהריים טובים, $name!" -ForegroundColor Cyan
} else {
    Write-Host "ערב טוב, $name!" -ForegroundColor Magenta
}
```

---

## קריטריוני הצלחה
- כל התלמידים יודעים לפתוח גם PS Console וגם ISE.
- כל תלמיד כתב לפחות סקריפט `.ps1` אחד ב-ISE והריץ עם `F5`.
- כל תלמיד השתמש ב-pipeline (`|`) עם לפחות שתי פקודות.
- הוגשה תיקיית `Report` מלאה עם כל הקבצים הנדרשים.
- כל תלמיד יכול להסביר את ההבדל בין `Set-Content` ל-`Add-Content`.

---

## שאלות רפלקציה לסיום
1. מה ההבדל העיקרי בין PowerShell ל-CMD?
2. למה PS עובד עם אובייקטים ולא טקסט - מה היתרון?
3. מה תפקיד ה-pipeline (`|`) ומתי נשתמש בו?
4. מתי תעדיפו לעבוד ב-Console ומתי ב-ISE?
5. למה חשוב `ExecutionPolicy` ומה הסיכון בשינוי שלו?

---

## הרחבה לשיעור הבא

### 1) משתנים ופרמטרים
```powershell
# משתנה פשוט
$name = "Alice"
$age  = 25
Write-Host "$name בת $age"

# מערך (Array)
$colors = @("אדום", "ירוק", "כחול")
$colors[0]          # גישה לאיבר ראשון
$colors.Count       # כמות איברים

# Hash Table (מילון)
$user = @{
    Name = "Bob"
    Role = "Admin"
    Age  = 30
}
$user["Name"]       # גישה לערך
$user.Role          # גישה אלטרנטיבית
```

### 2) לולאות ב-PowerShell
```powershell
# ForEach-Object (pipeline)
1..5 | ForEach-Object { Write-Host "מספר: $_" }

# foreach (קלאסי)
$fruits = @("תפוח", "בננה", "תפוז")
foreach ($fruit in $fruits) {
    Write-Host "פרי: $fruit"
}

# for
for ($i = 1; $i -le 5; $i++) {
    Write-Host "ספירה: $i"
}
```

### 3) תנאים ופונקציות
```powershell
# if / elseif / else
$score = 75
if ($score -ge 90) {
    Write-Host "מצוין!"
} elseif ($score -ge 60) {
    Write-Host "עובר"
} else {
    Write-Host "כישלון"
}

# פונקציה
function Get-Greeting {
    param([string]$Name)
    return "שלום, $Name!"
}

Get-Greeting -Name "דוד"
```

---

## טבלת סיכום פקודות יום 1

| משימה | CMD | PowerShell |
|---|---|---|
| הצג תיקייה | `dir` | `Get-ChildItem` |
| עבור לתיקייה | `cd path` | `Set-Location path` |
| צור תיקייה | `mkdir name` | `New-Item -ItemType Directory -Name name` |
| צור קובץ עם תוכן | `echo text > file` | `Set-Content -Path file -Value text` |
| הוסף תוכן | `echo text >> file` | `Add-Content -Path file -Value text` |
| הצג תוכן קובץ | `type file` | `Get-Content file` |
| העתק | `copy src dst` | `Copy-Item src dst` |
| העבר | `move src dst` | `Move-Item src dst` |
| מחק | `del file` | `Remove-Item file` |
| שנה שם | `ren old new` | `Rename-Item old new` |
| מידע מערכת | `systeminfo` | `Get-ComputerInfo` |
| רשימת תהליכים | `tasklist` | `Get-Process` |
| רשת | `ipconfig` | `Get-NetIPConfiguration` |
| נקה מסך | `cls` | `Clear-Host` |
| עזרה | `help cmd` | `Get-Help Cmdlet` |
