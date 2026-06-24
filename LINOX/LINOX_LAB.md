# LINOX LAB — מעבדת לינוקס למתחילים

> **סה"כ זמן:** ~295 דקות | **רמה:** מתחילים | **15 נושאים**

---

## הוראות שימוש

- קרא את ההסבר לפני כל פקודה
- בצע את ה**הדגמות** בעצמך — ראה שהפלט תואם
- השלם את **משימות המעבדה** בכל נושא
- עבוד **מהקל לקשה** — אל תדלג על שלבים

---

# חלק א' — מבוא

---

## נושא 1 — ה-SHELL ⏱ 10 דקות

### מה זה Shell?

ה-Shell הוא הממשק בין המשתמש למערכת ההפעלה.  
כשאתה כותב פקודה ולוחץ Enter — ה-Shell מפרש אותה ומעביר אותה ל-Kernel.

```
[ משתמש ] --> [ Shell (bash) ] --> [ Kernel ] --> [ חומרה ]
```

ה-Shell הנפוץ ביותר בלינוקס הוא **bash** (Bourne Again SHell).

---

### הדגמות

**הצגת ה-Shell הנוכחי:**

```bash
echo $SHELL
```
פלט לדוגמה:
```
/bin/bash
```

**הצגת שם המשתמש:**

```bash
echo $USER
```
פלט לדוגמה:
```
student
```

**הצגת ספריית הבית:**

```bash
echo $HOME
```
פלט לדוגמה:
```
/home/student
```

**הצגת כל משתני הסביבה:**

```bash
env
```
פלט לדוגמה (מקוצר):
```
USER=student
HOME=/home/student
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin
...
```

**הצגת ה-PATH (היכן מחפשים פקודות):**

```bash
echo $PATH
```
פלט לדוגמה:
```
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

---

### משימות מעבדה

- [ ] הרץ `echo $SHELL` — רשום מהו ה-Shell שלך
- [ ] הרץ `env | head -20` — רשום 5 משתני סביבה ותפקידם
- [ ] לחץ **Tab** פעמיים לאחר הקלדת `echo $` — מה מוצג?
- [ ] הרץ `echo $USER` ו-`echo $HOME` — מה ההבדל ביניהם?

---

## נושא 2 — תפריט העזרה הבסיסי ⏱ 10 דקות

### מה זה תפריט עזרה?

לינוקס מגיעה עם מערכת תיעוד מובנית.  
לכל פקודה ניתן לקבל מדריך מפורט ישירות מהטרמינל — בלי צורך בגוגל.

| פקודה | שימוש | מתי להשתמש |
|-------|-------|------------|
| `man <פקודה>` | מדריך מלא ומפורט | כשרוצים תיעוד מקיף |
| `<פקודה> --help` | סיכום קצר של אפשרויות | כשרוצים תזכורת מהירה |
| `whatis <פקודה>` | שורה אחת - מה הפקודה עושה | כשלא בטוחים מה פקודה עושה |
| `apropos <נושא>` | חיפוש פקודות לפי נושא | כשלא יודעים שם הפקודה |

---

### הדגמות

**פתיחת מדריך הפקודה `ls`:**

```bash
man ls
```
> ניווט: חצים למעלה/מטה | `q` לצאת | `/מילה` לחפש

**קבלת עזרה קצרה:**

```bash
ls --help
```
פלט לדוגמה (מקוצר):
```
Usage: ls [OPTION]... [FILE]...
List information about the FILEs.

  -a, --all          do not ignore entries starting with .
  -l                 use a long listing format
  -h, --human-readable  print sizes like 1K 234M 2G
...
```

**מה הפקודה `ls` עושה — בשורה אחת:**

```bash
whatis ls
```
פלט:
```
ls (1)               - list directory contents
```

**חיפוש פקודות הקשורות ל-"copy":**

```bash
apropos copy
```
פלט לדוגמה:
```
cp (1)               - copy files and directories
rsync (1)            - a fast, versatile file-copying tool
scp (1)              - OpenSSH secure file copy
...
```

---

### משימות מעבדה

- [ ] הרץ `man ls` — רשום 3 דגלים (flags) שלא הכרת
- [ ] הרץ `ls --help | head -30` — מה ההבדל מ-`man ls`?
- [ ] הרץ `whatis cp` ו-`whatis rm` — מה מוצג לכל אחד?
- [ ] הרץ `apropos copy | head -10` — כמה פקודות נמצאו?

---

## נושא 3 — מבנה מערכת ההפעלה LINUX ⏱ 30 דקות

### הארכיטקטורה

```
┌─────────────────────────────────────┐
│          משתמשים ותוכנות             │  ◄ User Space
│  (Firefox, bash, Python, LibreOffice)│
├─────────────────────────────────────┤
│              KERNEL                  │  ◄ Kernel Space
│  (ניהול זיכרון, תהליכים, קבצים)      │
├─────────────────────────────────────┤
│             חומרה (Hardware)         │
│      (CPU, RAM, דיסק, רשת)          │
└─────────────────────────────────────┘
```

### עץ הספריות הסטנדרטי (FHS)

```
/                    ← ספריית שורש (Root) — אב כל הספריות
├── bin/             ← פקודות בסיסיות (ls, cp, mv, cat)
├── sbin/            ← פקודות ניהול מערכת (למנהל בלבד)
├── etc/             ← קבצי הגדרות המערכת
├── home/            ← ספריות הבית של המשתמשים
│   └── student/     ← ספריית הבית של המשתמש "student"
├── var/             ← קבצים משתנים (לוגים, מסדי נתונים)
│   └── log/         ← קבצי לוג
├── tmp/             ← קבצים זמניים (נמחקים בכל אתחול)
├── usr/             ← תוכנות ומשאבים של המשתמשים
│   ├── bin/         ← תוכנות משתמש
│   └── lib/         ← ספריות תוכנה
├── lib/             ← ספריות מערכת בסיסיות
├── dev/             ← קבצי התקנים (דיסקים, מדפסות)
├── proc/            ← מידע על תהליכים פעילים (וירטואלי)
├── sys/             ← מידע על חומרה (וירטואלי)
└── mnt/             ← נקודות עגינה (USB, דיסקים חיצוניים)
```

---

### הדגמות

**הצגת מידע על ה-Kernel:**

```bash
uname -a
```
פלט לדוגמה:
```
Linux kali 6.1.0-kali9-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.27-1kali1 x86_64 GNU/Linux
```

> **קריאת הפלט:** `שם-מחשב` `גרסת-kernel` `ארכיטקטורה (x86_64=64bit)` `מערכת הפעלה`

**הצגת פרטי ההפצה:**

```bash
cat /etc/os-release
```
פלט לדוגמה:
```
PRETTY_NAME="Kali GNU/Linux Rolling"
NAME="Kali GNU/Linux"
ID=kali
ID_LIKE=debian
VERSION_ID="2024.1"
HOME_URL="https://www.kali.org/"
```

**הצגת ספריית השורש:**

```bash
ls /
```
פלט לדוגמה:
```
bin   dev  home  lib32  libx32  mnt  proc  run   srv  tmp  var
boot  etc  lib   lib64  media   opt  root  sbin  sys  usr
```

**פרטי ההפצה בפורמט נוח:**

```bash
lsb_release -a
```
פלט לדוגמה:
```
No LSB modules are available.
Distributor ID: Kali
Description:    Kali GNU/Linux Rolling
Release:        2024.1
Codename:       kali-rolling
```

---

### משימות מעבדה

- [ ] הרץ `uname -a` — תעד גרסת Kernel, ארכיטקטורה ושם המכונה
- [ ] הרץ `cat /etc/os-release` — זהה שם ההפצה וגרסתה
- [ ] הרץ `ls /` — עבור על כל ספרייה ורשום את תפקידה
- [ ] הרץ `lsb_release -a` — השווה לפלט של `os-release`

---

# חלק ב' — ניווט

---

## נושא 4 — ניווט בסיסי במערכת ההפעלה LINUX ⏱ 45 דקות

### פקודות הניווט הבסיסיות

| פקודה | שם מלא | תפקיד |
|-------|---------|-------|
| `pwd` | Print Working Directory | הצג את הנתיב הנוכחי |
| `ls` | List | הצג תוכן ספרייה |
| `cd` | Change Directory | שנה ספרייה |

### הבנת נתיבים

```
נתיב מוחלט (Absolute Path) — מתחיל ב-/
דוגמה: /home/student/documents/lab.txt

נתיב יחסי (Relative Path) — מהמיקום הנוכחי
דוגמה: documents/lab.txt  (אם אנחנו ב-/home/student)
```

### קיצורי ניווט חשובים

| קיצור | משמעות |
|-------|--------|
| `~` | ספריית הבית שלי (`/home/username`) |
| `.` | הספרייה הנוכחית |
| `..` | הספרייה האב (למעלה אחד) |
| `-` | הספרייה הקודמת שהיינו בה |

---

### הדגמות

**הצגת הנתיב הנוכחי:**

```bash
pwd
```
פלט:
```
/home/student
```

**הצגת תוכן ספרייה — פורמט בסיסי:**

```bash
ls
```
פלט לדוגמה:
```
Desktop  Documents  Downloads  Music  Pictures  Videos
```

**הצגת תוכן ספרייה — פורמט מפורט עם כל הקבצים (כולל מוסתרים):**

```bash
ls -la
```
פלט לדוגמה:
```
total 48
drwxr-xr-x 6 student student 4096 Jun 20 10:30 .
drwxr-xr-x 3 root    root    4096 Jun 15 09:00 ..
-rw-r--r-- 1 student student  220 Jun 15 09:00 .bash_logout
-rw-r--r-- 1 student student 3526 Jun 15 09:00 .bashrc
drwxr-xr-x 2 student student 4096 Jun 20 10:25 Desktop
drwxr-xr-x 2 student student 4096 Jun 20 10:25 Documents
```

**קריאת פלט `ls -la`:**
```
drwxr-xr-x  6  student  student  4096  Jun 20 10:30  Desktop
│            │  │        │        │     │             └── שם הקובץ/ספרייה
│            │  │        │        │     └────────────── תאריך ושעת שינוי אחרון
│            │  │        │        └──────────────────── גודל בבתים
│            │  │        └───────────────────────────── קבוצה
│            │  └────────────────────────────────────── בעלים
│            └───────────────────────────────────────── מספר קישורים
└────────────────────────────────────────────────────── הרשאות
  d = ספרייה, - = קובץ רגיל, l = קישור סמלי
  rwx = Read, Write, Execute
```

**ניווט לספרייה:**

```bash
cd /var/log
pwd
```
פלט:
```
/var/log
```

**חזרה לספריית הבית:**

```bash
cd ~
pwd
```
פלט:
```
/home/student
```

**ניווט לספרייה אחת למעלה:**

```bash
cd /var/log
cd ..
pwd
```
פלט:
```
/var
```

**חזרה לספרייה הקודמת:**

```bash
cd /etc
cd -
```
פלט:
```
/var   ← חוזר לאחרון
```

**הצגת גדלים קריאים לאדם:**

```bash
ls -lh /usr/bin | head -10
```
פלט לדוגמה:
```
total 156M
-rwxr-xr-x 1 root root  59K Jun 10 14:22 bash
-rwxr-xr-x 1 root root  35K Jun 10 14:22 cat
-rwxr-xr-x 1 root root  67K Jun 10 14:22 cp
```
> `-h` מציג גדלים כ-K, M, G — במקום בתים גולמיים

---

### משימות מעבדה

- [ ] הרץ `pwd` — רשום את הנתיב הנוכחי
- [ ] הרץ `ls -la /home` — הסבר כל עמודה בפלט
- [ ] נווט ל-`/var/log`, הרץ `ls`, ואז חזור home עם `cd ~`
- [ ] הרץ `ls -la` — מה ההבדל בין קבצים שמתחילים ב-`.` לאחרים?
- [ ] נווט ל-`/etc`, ואז עבור ל-`/tmp` עם נתיב יחסי (`cd ../tmp`)
- [ ] הרץ `ls -lh /usr/bin | head -20` — מה הדגל `-h` עושה?

---

# חלק ג' — ניהול קבצים

---

## נושא 5 — יצירת קובץ טקסט ⏱ 30 דקות

### דרכי יצירת קבצים בלינוקס

| שיטה | פקודה | מה היא עושה |
|------|-------|------------|
| קובץ ריק | `touch filename` | יוצר קובץ ריק, מעדכן timestamp אם קיים |
| מתוכן טקסט | `echo "text" > filename` | יוצר קובץ עם תוכן (מחליף אם קיים) |
| הוספה לקובץ | `echo "text" >> filename` | מוסיף שורה לקובץ קיים (לא מוחק) |
| כתיבה אינטראקטיבית | `cat > filename` | כותב כמה שורות עד Ctrl+D |

### אופרטורי הכוון (Redirection)

```
>   מחליף תוכן קיים (OVERWRITE)
>>  מוסיף לסוף הקובץ (APPEND)
```

---

### הדגמות

**הכנה — צור ספריית עבודה:**

```bash
mkdir ~/lab
cd ~/lab
pwd
```
פלט:
```
/home/student/lab
```

**יצירת קובץ ריק:**

```bash
touch myfile.txt
ls -la
```
פלט:
```
-rw-r--r-- 1 student student 0 Jun 20 11:00 myfile.txt
                              ↑
                         גודל 0 = ריק
```

**כתיבת תוכן לקובץ (מחליף):**

```bash
echo "Hello Linux Lab" > myfile.txt
cat myfile.txt
```
פלט:
```
Hello Linux Lab
```

**הוספת שורה לקובץ (לא מוחק):**

```bash
echo "Second Line" >> myfile.txt
cat myfile.txt
```
פלט:
```
Hello Linux Lab
Second Line
```

**מה קורה כשמשתמשים ב-`>` במקום `>>`:**

```bash
echo "REPLACED!" > myfile.txt
cat myfile.txt
```
פלט:
```
REPLACED!
```
> **שים לב:** התוכן הקודם נמחק! השתמש ב-`>>` כשרוצה להוסיף.

**כתיבה אינטראקטיבית (כמה שורות):**

```bash
cat > notes.txt
Line one
Line two
Line three
```
> לחץ **Ctrl+D** לסיום

```bash
cat notes.txt
```
פלט:
```
Line one
Line two
Line three
```

---

### משימות מעבדה

- [ ] צור ספרייה `~/lab` עם `mkdir ~/lab` וכנס אליה עם `cd ~/lab`
- [ ] צור קובץ ריק `touch myfile.txt` — ודא שגודלו 0 עם `ls -la`
- [ ] כתוב `"Hello Linux Lab"` לקובץ עם `>` — הצג תוכן עם `cat`
- [ ] הוסף שורה שנייה עם `>>` — ודא ששתי השורות קיימות
- [ ] צור קובץ `notes.txt` עם `cat >` (כמה שורות, סיים Ctrl+D)

---

## נושא 6 — צפייה ועריכת קובץ טקסט ⏱ 15 דקות

### פקודות צפייה

| פקודה | תפקיד | מתי להשתמש |
|-------|-------|------------|
| `cat file` | הצג כל הקובץ בבת אחת | קבצים קצרים |
| `cat -n file` | הצג עם מספרי שורות | כשצריך לדעת מספר שורה |
| `head -N file` | הצג N שורות ראשונות | תחילת קובץ גדול |
| `tail -N file` | הצג N שורות אחרונות | סוף קובץ / לוגים |
| `less file` | דפדוף בקובץ | קבצים גדולים |
| `more file` | דפדוף בסיסי | קבצים בינוניים |

### עורך הטקסט nano

```bash
nano filename
```

פקודות nano:
```
Ctrl+O   → שמירה (Write Out)
Ctrl+X   → יציאה
Ctrl+K   → גזור שורה
Ctrl+U   → הדבק שורה
Ctrl+W   → חיפוש
Ctrl+G   → עזרה
```

---

### הדגמות

**הצגת כל הקובץ:**

```bash
cat myfile.txt
```
פלט:
```
Hello Linux Lab
Second Line
```

**הצגת קובץ עם מספרי שורות:**

```bash
cat -n myfile.txt
```
פלט:
```
     1	Hello Linux Lab
     2	Second Line
```

**הצגת 1 שורה ראשונה בלבד:**

```bash
head -1 myfile.txt
```
פלט:
```
Hello Linux Lab
```

**הצגת שורה אחרונה בלבד:**

```bash
tail -1 myfile.txt
```
פלט:
```
Second Line
```

**מעקב אחר קובץ לוג בזמן אמת (שימושי מאוד):**

```bash
tail -f /var/log/syslog
```
> עצור עם **Ctrl+C**

**פתיחת קובץ לעריכה ב-nano:**

```bash
nano myfile.txt
```
> הוסף שורה חדשה → Ctrl+O → Enter → Ctrl+X

---

### משימות מעבדה

- [ ] הרץ `cat myfile.txt` — הצג תוכן הקובץ
- [ ] הרץ `head -1 myfile.txt` ו-`tail -1 myfile.txt` — מה ההבדל?
- [ ] פתח `nano myfile.txt` — הוסף שורה, שמור (Ctrl+O), צא (Ctrl+X)
- [ ] הרץ `cat -n myfile.txt` — מה הדגל `-n` מוסיף?

---

## נושא 7 — העתקת קובץ ⏱ 25 דקות

### פקודת `cp` — Copy

```
תחביר: cp [אפשרויות] מקור יעד
```

| דגל | תפקיד |
|-----|-------|
| `-r` | העתק ספרייה שלמה (Recursive) |
| `-p` | שמור הרשאות וזמנים מקוריים |
| `-i` | שאל לפני החלפה |
| `-v` | הצג מה מועתק (Verbose) |

---

### הדגמות

**העתקת קובץ לשם חדש באותה ספרייה:**

```bash
cp myfile.txt myfile_backup.txt
ls -la
```
פלט:
```
-rw-r--r-- 1 student student  32 Jun 20 11:00 myfile.txt
-rw-r--r-- 1 student student  32 Jun 20 11:05 myfile_backup.txt
```

**העתקת קובץ לספרייה אחרת:**

```bash
mkdir backup_dir
cp myfile.txt backup_dir/
ls backup_dir/
```
פלט:
```
myfile.txt
```

**העתקת ספרייה שלמה (חובה להשתמש ב-`-r`):**

```bash
cp -r backup_dir backup_dir2
ls
```
פלט:
```
backup_dir  backup_dir2  myfile.txt  myfile_backup.txt  notes.txt
```

**מה קורה ללא `-r`:**

```bash
cp backup_dir backup_dir3
```
פלט (שגיאה):
```
cp: -r not specified; omitting directory 'backup_dir'
```

**העתקה עם שמירת metadata:**

```bash
cp -p myfile.txt preserved.txt
ls -la myfile.txt preserved.txt
```
פלט:
```
-rw-r--r-- 1 student student 32 Jun 20 11:00 myfile.txt
-rw-r--r-- 1 student student 32 Jun 20 11:00 preserved.txt
                                      ↑
                              אותו timestamp!
```

**העתקה עם אישור לפני החלפה:**

```bash
cp -i myfile.txt myfile_backup.txt
```
פלט:
```
cp: overwrite 'myfile_backup.txt'? 
```
> הקלד `y` לאישור, `n` לביטול

---

### משימות מעבדה

- [ ] העתק `myfile.txt` → `myfile_backup.txt` — ודא שניהם קיימים עם `ls`
- [ ] צור `mkdir backup_dir` והעתק `myfile.txt` לתוכה
- [ ] העתק ספרייה שלמה: `cp -r backup_dir backup_dir2`
- [ ] נסה `cp backup_dir backup_dir3` ללא `-r` — מה הודעת השגיאה?
- [ ] השתמש ב-`cp -i myfile.txt myfile_backup.txt` — מה הדגל `-i` עושה?

---

## נושא 8 — העברת קובץ ⏱ 20 דקות

### פקודת `mv` — Move

```
תחביר: mv [אפשרויות] מקור יעד
```

> **הבדל חשוב מ-`cp`:** `mv` **מוחק** את המקור לאחר ההעברה!

| דגל | תפקיד |
|-----|-------|
| `-i` | שאל לפני החלפה |
| `-v` | הצג מה מועבר |
| `-n` | אל תחלף קובץ קיים |

---

### הדגמות

**העברת קובץ לספרייה אחרת:**

```bash
mv myfile_backup.txt backup_dir/
ls
ls backup_dir/
```
פלט:
```
# ls (ספרייה נוכחית):
backup_dir  backup_dir2  myfile.txt  notes.txt
            ↑ myfile_backup.txt נעלם!

# ls backup_dir/:
myfile.txt  myfile_backup.txt
```

**החזרת קובץ לספרייה הנוכחית (נקודה = כאן):**

```bash
mv backup_dir/myfile_backup.txt .
ls
```
פלט:
```
backup_dir  backup_dir2  myfile.txt  myfile_backup.txt  notes.txt
```

**העברה עם אישור לפני החלפה:**

```bash
mv -i myfile_backup.txt myfile.txt
```
פלט:
```
mv: overwrite 'myfile.txt'?
```
> הקלד `n` לביטול

**ניסיון להעביר לספרייה שלא קיימת:**

```bash
mv myfile.txt nonexistent_dir/myfile.txt
```
פלט:
```
mv: cannot move 'myfile.txt' to 'nonexistent_dir/myfile.txt':
No such file or directory
```

---

### משימות מעבדה

- [ ] העבר `myfile_backup.txt` ל-`backup_dir/` — ודא שנעלם מהמיקום המקורי
- [ ] החזר אותו חזרה עם `mv backup_dir/myfile_backup.txt .`
- [ ] נסה להעביר לספרייה שלא קיימת — רשום הודעת השגיאה
- [ ] השתמש ב-`mv -i` כשיש קובץ קיים ביעד — מה קורה?

---

## נושא 9 — שינוי שם קובץ ⏱ 15 דקות

### איך משנים שם בלינוקס?

בלינוקס **אין** פקודה נפרדת לשינוי שם.  
הפקודה `mv` משמשת לשני הדברים — העברה **ושינוי שם**.

```
mv שם-ישן שם-חדש
```

הסיבה: שינוי שם הוא בעצם "העברה לאותה ספרייה עם שם אחר".

---

### הדגמות

**שינוי שם קובץ:**

```bash
ls
mv myfile.txt renamed_file.txt
ls
```
פלט לפני:
```
myfile.txt  myfile_backup.txt  notes.txt
```
פלט אחרי:
```
myfile_backup.txt  notes.txt  renamed_file.txt
```

**שינוי שם ספרייה:**

```bash
mv backup_dir archive_dir
ls
```
פלט:
```
archive_dir  backup_dir2  myfile_backup.txt  notes.txt  renamed_file.txt
```

**ניסיון לשנות שם קובץ שלא קיים:**

```bash
mv no_such_file.txt new_name.txt
```
פלט:
```
mv: cannot stat 'no_such_file.txt': No such file or directory
```

**שינוי שם עם שינוי סיומת:**

```bash
mv notes.txt notes.bak
ls
```
פלט:
```
archive_dir  backup_dir2  myfile_backup.txt  notes.bak  renamed_file.txt
```

---

### משימות מעבדה

- [ ] שנה שם `myfile_backup.txt` → `old_backup.txt` — ודא עם `ls`
- [ ] שנה שם ספרייה `backup_dir2` → `old_backup_dir` — ודא עם `ls`
- [ ] נסה לשנות שם לקובץ שלא קיים — רשום הודעת השגיאה

---

## נושא 10 — הסתרת קובץ ⏱ 10 דקות

### איך מסתירים קבצים בלינוקס?

בלינוקס, **כל קובץ שמתחיל בנקודה** (`.`) נחשב **מוסתר**.  
אין "תכונת hidden" כמו בוינדוס — פשוט שם שמתחיל ב-`.`

```
קובץ רגיל:   myfile.txt     ← מוצג ב-ls
קובץ מוסתר:  .myfile.txt    ← לא מוצג ב-ls (רק ב-ls -a)
```

קבצי הגדרות מוסתרים נפוצים:
- `.bashrc` — הגדרות ה-bash
- `.bash_history` — היסטוריית פקודות
- `.ssh/` — ספריית SSH

---

### הדגמות

**הסתרת קובץ (הוסף נקודה בהתחלה):**

```bash
mv renamed_file.txt .hidden_file.txt
```

**הקובץ לא מוצג ב-`ls` רגיל:**

```bash
ls
```
פלט:
```
archive_dir  myfile_backup.txt  notes.bak  old_backup.txt  old_backup_dir
                 ↑ .hidden_file.txt לא מופיע!
```

**הקובץ מוצג ב-`ls -a` (all):**

```bash
ls -a
```
פלט:
```
.  ..  .hidden_file.txt  archive_dir  myfile_backup.txt  notes.bak  old_backup.txt  old_backup_dir
```

**ספירת קבצים מוסתרים:**

```bash
ls -la | grep "^\."
```
פלט:
```
drwxr-xr-x 2 student student 4096 Jun 20 11:30 .
drwxr-xr-x 8 student student 4096 Jun 20 11:30 ..
-rw-r--r-- 1 student student   32 Jun 20 11:00 .hidden_file.txt
```

**גילוי קובץ מוסתר:**

```bash
mv .hidden_file.txt visible_file.txt
ls
```
פלט:
```
archive_dir  myfile_backup.txt  notes.bak  old_backup.txt  old_backup_dir  visible_file.txt
```

---

### משימות מעבדה

- [ ] הסתר קובץ: `mv visible_file.txt .hidden_file.txt`
- [ ] הרץ `ls` — האם הקובץ המוסתר מופיע?
- [ ] הרץ `ls -a` — רשום את כל הקבצים המוסתרים שמצאת
- [ ] הרץ `ls -la` — ספור כמה קבצים מוסתרים יש בספריית `lab`

---

## נושא 11 — מחיקת קובץ ⏱ 10 דקות

### פקודת `rm` — Remove

```
תחביר: rm [אפשרויות] קובץ/ספרייה
```

> **אזהרה:** לינוקס **לא** שולחת לסל מחזור! מחיקה = מחיקה סופית!

| דגל | תפקיד |
|-----|-------|
| `-r` | מחק ספרייה שלמה (Recursive) |
| `-i` | שאל לפני כל מחיקה |
| `-v` | הצג מה נמחק |
| `-f` | אל תשאל שאלות (Force) — **מסוכן!** |

---

### הדגמות

**מחיקת קובץ:**

```bash
rm .hidden_file.txt
ls -a
```
פלט:
```
.  ..  archive_dir  myfile_backup.txt  notes.bak  old_backup.txt  old_backup_dir
       ↑ .hidden_file.txt נמחק!
```

**ניסיון למחוק ספרייה ללא `-r` (ייכשל):**

```bash
rm old_backup_dir
```
פלט:
```
rm: cannot remove 'old_backup_dir': Is a directory
```

**מחיקת ספרייה שלמה:**

```bash
rm -r old_backup_dir
ls
```
פלט:
```
archive_dir  myfile_backup.txt  notes.bak  old_backup.txt
```

**מחיקה עם אישור לכל קובץ:**

```bash
rm -ri archive_dir
```
פלט:
```
rm: descend into directory 'archive_dir'? y
rm: remove regular file 'archive_dir/myfile.txt'? y
rm: remove directory 'archive_dir'? y
```

---

> ### ⚠️ אזהרה קריטית
>
> **לעולם אל תרוץ:**
> ```bash
> rm -rf /          # מוחק כל מערכת הקבצים!
> rm -rf /*         # מוחק כל מערכת הקבצים!
> rm -rf ~          # מוחק את כל ספריית הבית שלך!
> ```
> **אין שחזור!** תמיד ודא שאתה בספרייה הנכונה לפני `rm -r`.

---

### משימות מעבדה

- [ ] מחק `notes.bak` — ודא עם `ls -a`
- [ ] נסה `rm archive_dir` ללא `-r` — מה הודעת השגיאה? מה הפתרון?
- [ ] מחק `archive_dir` עם `rm -r` — ודא שנמחקה
- [ ] השתמש ב-`rm -i` כדי למחוק קובץ — מה הדגל `-i` עושה?

---

## נושא 12 — ניתוח קבצים ⏱ 25 דקות

### פקודות ניתוח קבצים

| פקודה | תפקיד |
|-------|-------|
| `file` | זיהוי סוג הקובץ |
| `wc` | ספירת שורות, מילים, תווים |
| `du` | גודל ספרייה/קובץ |
| `stat` | מטא-דאטה מלאה של קובץ |

---

### הדגמות

**זיהוי סוג קובץ:**

```bash
file myfile_backup.txt
```
פלט:
```
myfile_backup.txt: ASCII text
```

```bash
file /bin/bash
```
פלט:
```
/bin/bash: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked...
```

> `file` לא מסתמך על הסיומת — הוא בודק תוכן הקובץ!

**ספירת שורות, מילים ותווים עם `wc`:**

```bash
wc myfile_backup.txt
```
פלט:
```
 2  4 32 myfile_backup.txt
 ↑  ↑  ↑
 │  │  └── תווים (bytes)
 │  └───── מילים (words)
 └──────── שורות (lines)
```

**ספירת שורות בלבד:**

```bash
wc -l myfile_backup.txt
```
פלט:
```
2 myfile_backup.txt
```

**גודל ספרייה:**

```bash
du -sh ~/lab
```
פלט:
```
12K    /home/student/lab
```
> `-s` = סיכום | `-h` = קריא לאדם (K, M, G)

**מטא-דאטה מלאה של קובץ:**

```bash
stat myfile_backup.txt
```
פלט:
```
  File: myfile_backup.txt
  Size: 32              Blocks: 8          IO Block: 4096   regular file
Device: 801h/2049d      Inode: 1234567     Links: 1
Access: (0644/-rw-r--r--)  Uid: ( 1000/student)   Gid: ( 1000/student)
Access: 2024-06-20 11:00:00.000
Modify: 2024-06-20 11:00:00.000
Change: 2024-06-20 11:00:00.000
```

> **שלושה timestamps:**
> - **Access** (atime) — מתי הקובץ נקרא לאחרונה
> - **Modify** (mtime) — מתי התוכן שונה לאחרונה
> - **Change** (ctime) — מתי ה-metadata שונה

**מציאת הקבצים הגדולים ב-/bin:**

```bash
ls -lh /bin | sort -k5 -rh | head -10
```
פלט לדוגמה:
```
-rwxr-xr-x 1 root root  59K Jun 10 bash
-rwxr-xr-x 1 root root  47K Jun 10 cp
-rwxr-xr-x 1 root root  43K Jun 10 mv
```

---

### משימות מעבדה

- [ ] הרץ `file myfile_backup.txt` ו-`file /bin/bash` — מה ההבדל?
- [ ] הרץ `wc myfile_backup.txt` — הסבר כל מספר בפלט
- [ ] הרץ `du -sh ~/lab` — מה גודל ספריית הלאב?
- [ ] הרץ `stat myfile_backup.txt` — שים לב ל-inode, permissions ו-timestamps
- [ ] הרץ `ls -lh /bin | sort -k5 -rh | head -10` — מצא 3 קבצים גדולים

---

# חלק ד' — חיפוש קבצים ותוכנות

---

## נושא 13 — מבוא לחיפוש ⏱ 10 דקות

### כלי החיפוש בלינוקס

| פקודה | חיפוש לפי | מהירות | מציאת קבצים חדשים |
|-------|-----------|--------|-------------------|
| `find` | סריקה בזמן אמת | איטי | כן |
| `locate` | database מוכנה | מהיר מאוד | רק אחרי `updatedb` |
| `which` | תוכנות בלבד | מיידי | כן |
| `whereis` | תוכנות + man pages | מיידי | כן |

---

### הדגמות

**מאיפה נטענת הפקודה `ls`:**

```bash
which ls
```
פלט:
```
/usr/bin/ls
```

**מאיפה נטענת הפקודה `bash` + דפי עזרה:**

```bash
whereis bash
```
פלט:
```
bash: /usr/bin/bash /etc/bash.bashrc /usr/share/man/man1/bash.1.gz
       ↑ בינארי       ↑ קובץ הגדרות    ↑ דף man
```

**זיהוי סוג פקודה:**

```bash
type ls
type cd
type echo
```
פלט:
```
ls is /usr/bin/ls          ← קובץ בינארי (file)
cd is a shell builtin      ← מובנה ב-Shell (builtin)
echo is a shell builtin    ← מובנה ב-Shell (builtin)
```

---

### משימות מעבדה

- [ ] הרץ `which ls` — מאיפה נטענת הפקודה?
- [ ] הרץ `whereis bash` — מה מוחזר מעבר לנתיב הבינארי?
- [ ] הרץ `type ls`, `type cd`, `type echo` — זהה את ההבדלים

---

## נושא 14 — הפקודה `find` ⏱ 20 דקות

### פקודת `find` — חיפוש בזמן אמת

```
תחביר: find [ספרייה] [תנאים]
```

| דגל | דוגמה | תפקיד |
|-----|-------|-------|
| `-name` | `-name "*.txt"` | חיפוש לפי שם (case sensitive) |
| `-iname` | `-iname "*.TXT"` | חיפוש לפי שם (case insensitive) |
| `-type f` | `-type f` | קבצים בלבד |
| `-type d` | `-type d` | ספריות בלבד |
| `-mtime -N` | `-mtime -1` | שונה בN ימים האחרונים |
| `-size +N` | `-size +1M` | גדול מ-N |
| `-maxdepth N` | `-maxdepth 2` | עומק חיפוש מקסימלי |

---

### הדגמות

**מציאת כל קבצי `.txt` תחת home:**

```bash
find ~ -name "*.txt"
```
פלט לדוגמה:
```
/home/student/lab/myfile_backup.txt
/home/student/lab/old_backup.txt
```

**מציאת ספריות בלבד (עד עומק 2):**

```bash
find /var -type d -maxdepth 2
```
פלט לדוגמה:
```
/var
/var/backups
/var/cache
/var/lib
/var/log
/var/spool
/var/tmp
```

**מציאת קבצים שהשתנו ב-24 השעות האחרונות:**

```bash
find /etc -mtime -1 2>/dev/null
```
פלט לדוגמה:
```
/etc/resolv.conf
/etc/hosts
```
> `2>/dev/null` מסתיר שגיאות הרשאה

**מציאת קבצים גדולים מ-1MB:**

```bash
find /usr -size +1M -type f 2>/dev/null | head -10
```
פלט לדוגמה:
```
/usr/lib/libc.so.6
/usr/bin/python3
/usr/share/locale/ru/LC_MESSAGES/bash.mo
```

**חיפוש קבצים ב-lab שלך:**

```bash
find ~/lab -name "*.txt" -type f
```
פלט:
```
/home/student/lab/myfile_backup.txt
/home/student/lab/old_backup.txt
```

---

### טיפ — שילוב `find` עם פקודות אחרות

```bash
# מחק כל קבצי .tmp
find ~/lab -name "*.tmp" -type f -delete

# הצג גודל כל קבצי .txt
find ~ -name "*.txt" -type f -exec ls -lh {} \;
```

---

### משימות מעבדה

- [ ] מצא כל קבצי `.txt` תחת home: `find ~ -name "*.txt"`
- [ ] מצא רק ספריות ב-`/var` (עד עומק 2): `find /var -type d -maxdepth 2`
- [ ] מצא קבצים שהשתנו ב-24 שעות: `find /etc -mtime -1 2>/dev/null`
- [ ] מצא קבצים גדולים מ-1MB: `find /usr -size +1M -type f 2>/dev/null | head -10`
- [ ] חפש ב-lab שלך: `find ~/lab -name "*.txt" -type f` — כמה נמצאו?

---

## נושא 15 — הפקודה `locate` ⏱ 20 דקות

### פקודת `locate` — חיפוש מהיר ממסד נתונים

```
תחביר: locate [אפשרויות] דפוס-חיפוש
```

`locate` מחפש **ב-database** שנבנתה מראש על-ידי `updatedb`.  
**יתרון:** מהיר מאוד.  
**חיסרון:** לא מוצא קבצים שנוצרו לאחר עדכון ה-database.

| דגל | תפקיד |
|-----|-------|
| `-i` | חיפוש ללא רגישות לאותיות גדולות/קטנות |
| `-c` | הצג רק ספירת תוצאות |
| `-n N` | הצג רק N תוצאות ראשונות |
| `-r` | חיפוש עם ביטוי רגולרי |

---

### הדגמות

**חיפוש בסיסי:**

```bash
locate passwd
```
פלט לדוגמה:
```
/etc/passwd
/etc/passwd-
/etc/security/opasswd
/usr/bin/passwd
/usr/share/man/man1/passwd.1.gz
```

**חיפוש ללא רגישות לרישיות:**

```bash
locate -i README
```
פלט לדוגמה:
```
/usr/share/doc/bash/README
/usr/share/doc/vim/README.txt
/usr/share/fonts/README
```

**ספירת תוצאות:**

```bash
locate -c bash
```
פלט:
```
47
```

**עדכון ה-database (דורש הרשאות root):**

```bash
sudo updatedb
```
> לאחר עדכון, locate ימצא גם קבצים חדשים

**בדיקה שהקבצים שיצרת נמצאים עכשיו:**

```bash
sudo updatedb
locate myfile_backup.txt
```
פלט:
```
/home/student/lab/myfile_backup.txt
```

---

### השוואת מהירות: `find` לעומת `locate`

```bash
# locate — מהיר (database)
time locate bash
```
פלט:
```
...תוצאות...
real    0m0.015s    ← 15 מילישניות!
```

```bash
# find — איטי יותר (סריקה אמיתית)
time find / -name bash 2>/dev/null
```
פלט:
```
...תוצאות...
real    0m8.432s    ← 8 שניות!
```

### מתי להשתמש במה?

```
locate → חיפוש מהיר של קבצים ותוכנות ידועות
find   → חיפוש דינמי, עם תנאים מורכבים (גודל, זמן, סוג)
```

---

### משימות מעבדה

- [ ] הרץ `locate passwd` — ציין כמה תוצאות הופיעו
- [ ] הרץ `locate -i readme` — מה הדגל `-i` עושה?
- [ ] הרץ `locate -c bash` — מה ספירת התוצאות?
- [ ] הרץ `sudo updatedb`, ואז `locate myfile_backup.txt` — נמצא?
- [ ] השווה: `time find / -name bash 2>/dev/null` לעומת `time locate bash`

---

# סיכום — טבלת פקודות מהירה

## ניווט

| פקודה | תפקיד |
|-------|-------|
| `pwd` | הצג נתיב נוכחי |
| `ls -la` | הצג תוכן ספרייה מפורט (כולל מוסתרים) |
| `cd /path` | נווט לנתיב מוחלט |
| `cd ~` | חזור לספריית הבית |
| `cd ..` | עלה ספרייה אחת |
| `cd -` | חזור לספרייה הקודמת |

## ניהול קבצים

| פקודה | תפקיד |
|-------|-------|
| `touch file` | צור קובץ ריק |
| `echo "txt" > file` | צור קובץ עם תוכן |
| `echo "txt" >> file` | הוסף תוכן לקובץ קיים |
| `cat file` | הצג תוכן קובץ |
| `head -N file` | הצג N שורות ראשונות |
| `tail -N file` | הצג N שורות אחרונות |
| `nano file` | ערוך קובץ |
| `cp src dst` | העתק קובץ |
| `cp -r dir1 dir2` | העתק ספרייה |
| `mv src dst` | העבר / שנה שם |
| `mv file .file` | הסתר קובץ |
| `rm file` | מחק קובץ |
| `rm -r dir` | מחק ספרייה |
| `file name` | זהה סוג קובץ |
| `wc file` | ספור שורות/מילים/תווים |
| `stat file` | הצג metadata מלאה |
| `du -sh dir` | גודל ספרייה |

## חיפוש

| פקודה | תפקיד |
|-------|-------|
| `which cmd` | מיקום תוכנה |
| `whereis cmd` | מיקום תוכנה + man |
| `type cmd` | סוג פקודה |
| `find ~ -name "*.txt"` | חפש קבצי txt |
| `find /path -type d` | חפש ספריות |
| `find /path -mtime -1` | שונה אתמול |
| `find /path -size +1M` | גדולים מ-1MB |
| `locate name` | חיפוש מהיר |
| `sudo updatedb` | עדכן database של locate |

## עזרה

| פקודה | תפקיד |
|-------|-------|
| `man cmd` | מדריך מלא |
| `cmd --help` | עזרה קצרה |
| `whatis cmd` | תיאור בשורה אחת |
| `apropos topic` | חפש פקודות לפי נושא |

---

*LINOX LAB — Linux for Beginners | מעבדת לינוקס למתחילים*
