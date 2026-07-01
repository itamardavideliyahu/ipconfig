# מעבדת חזרה — לינוקס
### תרגול מעשי משולב | ~30 דקות

> **נושאים:** ספריות, שמירת פלטים, ps, find, locate, chmod, kill, mv  
> **רמה:** מתחילים (לאחר מעבדת הלינוקס הבסיסית)  
> **סגנון:** כל השלבים בנויים אחד על השני — אל תדלג!

---

## הסיפור שלנו

בשיעור הזה נדמה חוקר מערכת שמגיע למחשב לינוקס, **בונה סביבת עבודה**, **מתעד ממצאים לקבצים**, **בודק תהליכים פעילים**, **מחפש קבצים** ולבסוף **מסדר ומארז את התיעוד** ומעביר אותו למיקום קבוע.

---

## שלב 1 — בניית סביבת עבודה ⏱ 5 דקות

### יצירת תקיית עבודה

כל חוקר מערכת טוב מתחיל ביצירת **תקייה ייעודית לממצאים**. לא כותבים לשולחן העבודה — עובדים בסדר.

```bash
# צור תקיית חקירה עם תאריך כשם
mkdir ~/investigation_$(date +%F)
```
פלט — לא יוצג שום דבר (מחיקה שקטה = הצלחה). ודא:
```bash
ls ~/
```
פלט לדוגמה:
```
Desktop  Documents  Downloads  investigation_2024-06-20
```

```bash
# כנס לתקייה
cd ~/investigation_$(date +%F)
pwd
```
פלט לדוגמה:
```
/home/student/investigation_2024-06-20
```

```bash
# צור תת-תקיות לסדר את הממצאים
mkdir processes network files permissions
ls
```
פלט:
```
files  network  permissions  processes
```

> **למה מסדרים ככה?** בחקירות אמיתיות — עשרות ממצאים. תקיות מסודרות חוסכות בלבול.

---

### שמירת פלטים לקבצים

עד עכשיו ראינו פלטים בטרמינל — הם נעלמים. כדי לשמור ממצאים:

```
פקודה > קובץ.txt    ← שמור פלט לקובץ (מחליף)
פקודה >> קובץ.txt   ← הוסף פלט לקובץ קיים
```

**תעד את פרטי המערכת הראשוניים:**

```bash
echo "=== SYSTEM INFO ===" > system_info.txt
uname -a >> system_info.txt
echo "" >> system_info.txt
echo "=== OS RELEASE ===" >> system_info.txt
cat /etc/os-release >> system_info.txt
echo "" >> system_info.txt
echo "=== CURRENT USER ===" >> system_info.txt
whoami >> system_info.txt
echo "=== DATE ===" >> system_info.txt
date >> system_info.txt
```

```bash
# ודא שהקובץ נוצר ויש בו תוכן
cat system_info.txt
```
פלט לדוגמה:
```
=== SYSTEM INFO ===
Linux kali 6.1.0-kali9-amd64 #1 SMP x86_64 GNU/Linux

=== OS RELEASE ===
PRETTY_NAME="Kali GNU/Linux Rolling"
NAME="Kali GNU/Linux"
ID=kali

=== CURRENT USER ===
student

=== DATE ===
Thu Jun 20 11:00:00 IDT 2024
```

---

**משימות — שלב 1:**

- [ ] צור `~/investigation_<תאריך-היום>` עם התת-תקיות
- [ ] צור `system_info.txt` עם פרטי המערכת (כמו בדוגמה)
- [ ] הרץ `ls -la` — כמה קבצים ותקיות יש בתקיית החקירה?

---

## שלב 2 — חקירת תהליכים עם `ps` ⏱ 8 דקות

### מה זה תהליך (Process)?

כל דבר שרץ במחשב הוא **תהליך** — דפדפן, טרמינל, שרת, סקריפט.  
לכל תהליך יש **PID** (Process ID) — מספר ייחודי לזיהוי.

```
[ תהליך אב (Parent) ]  ←  PID 1 = systemd (ראשון תמיד)
        ↓
[ תהליכי ילד (Child) ]  ←  כל שאר התהליכים
```

### פקודת `ps`

```
ps        ← הצג רק תהליכי המשתמש הנוכחי בטרמינל הזה
ps aux    ← הצג את כל התהליכים של כולם
ps -ef    ← פורמט אחר — מוסיף PPID (תהליך אב)
```

| עמודה | משמעות |
|-------|--------|
| `USER` | המשתמש שהפעיל את התהליך |
| `PID` | מספר זיהוי התהליך |
| `%CPU` | אחוז שימוש ב-CPU |
| `%MEM` | אחוז שימוש בזיכרון |
| `STAT` | מצב התהליך (R=רץ, S=ישן, Z=זומבי) |
| `COMMAND` | הפקודה שהפעילה את התהליך |

---

### הדגמות

**הצגת כל התהליכים:**

```bash
ps aux
```
פלט לדוגמה:
```
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1  22520  1856 ?        Ss   09:00   0:01 /sbin/init
root       423  0.0  0.2  55680  2340 ?        Ss   09:00   0:00 /usr/sbin/sshd
www-data   891  0.1  0.8 456120  8432 ?        S    09:01   0:05 /usr/sbin/apache2
student   1203  0.0  0.1  22680  1024 pts/0    Ss   10:00   0:00 bash
student   1337  0.0  0.0  17648   768 pts/0    R+   11:00   0:00 ps aux
```

**הצגת תהליכים של משתמש ספציפי:**

```bash
ps aux | grep root
```
פלט לדוגמה:
```
root     1  0.0  0.1  22520  1856 ?  Ss  09:00  0:01 /sbin/init
root   423  0.0  0.2  55680  2340 ?  Ss  09:00  0:00 /usr/sbin/sshd
root   512  0.0  0.1  12340   890 ?  Ss  09:00  0:00 /usr/sbin/cron
```

**הצגת תהליך לפי שם:**

```bash
ps aux | grep apache2
```
פלט לדוגמה:
```
www-data   891  0.1  0.8 456120  8432 ?  S  09:01  0:05 /usr/sbin/apache2
www-data   892  0.0  0.6 456120  6240 ?  S  09:01  0:00 /usr/sbin/apache2
www-data   893  0.0  0.6 456120  6240 ?  S  09:01  0:00 /usr/sbin/apache2
```

**הצגת תהליכים בעץ (מי הפעיל את מי):**

```bash
ps -ef --forest | head -20
```
פלט לדוגמה:
```
UID    PID  PPID CMD
root     1     0 /sbin/init
root   423     1  \_ /usr/sbin/sshd
root  1100   423      \_ sshd: student [priv]
student 1101  1100          \_ sshd: student@pts/0
student 1203  1101              \_ bash
student 1250  1203                  \_ ps -ef --forest
```

---

**שמירת ממצאי התהליכים:**

```bash
# שמור את כל התהליכים לתקיית processes
ps aux > ~/investigation_$(date +%F)/processes/all_processes.txt

# שמור רק תהליכי root
ps aux | grep root > ~/investigation_$(date +%F)/processes/root_processes.txt

# ודא שהקבצים נשמרו
ls -lh ~/investigation_$(date +%F)/processes/
```
פלט לדוגמה:
```
-rw-r--r-- 1 student student 4.2K Jun 20 all_processes.txt
-rw-r--r-- 1 student student  892 Jun 20 root_processes.txt
```

---

**הפעלת תהליך ברקע לתרגול kill בהמשך:**

```bash
# הפעל sleep למשך 1000 שניות ברקע (& = ברקע)
sleep 1000 &
```
פלט:
```
[1] 1456
```
> `[1]` = מספר job | `1456` = PID של התהליך — שמור את ה-PID הזה!

```bash
# ודא שהתהליך רץ
ps aux | grep sleep
```
פלט:
```
student   1456  0.0  0.0  13360   724 pts/0  S   11:05   0:00 sleep 1000
```

---

**משימות — שלב 2:**

- [ ] הרץ `ps aux` — זהה את PID של `bash` שלך
- [ ] שמור את כל התהליכים ל-`processes/all_processes.txt`
- [ ] שמור רק תהליכי `root` ל-`processes/root_processes.txt`
- [ ] הפעל `sleep 1000 &` — **שמור את ה-PID שהוצג**
- [ ] ודא עם `ps aux | grep sleep` שהתהליך רץ

---

## שלב 3 — ניהול הרשאות עם `chmod` ⏱ 7 דקות

### איך עובדות הרשאות בלינוקס?

כל קובץ יש לו **שלוש קבוצות הרשאות**:

```
-  rw-  r--  r--
│   │    │    └── Other  (כולם שאר המשתמשים)
│   │    └─────── Group  (חברי הקבוצה)
│   └──────────── User   (הבעלים)
└──────────────── סוג (- = קובץ, d = תקייה)
```

**שלוש הרשאות אפשריות:**

| אות | ספרה | משמעות לקובץ | משמעות לתקייה |
|-----|------|-------------|--------------|
| `r` | 4 | קריאה | הצגת תוכן התקייה |
| `w` | 2 | כתיבה | יצירה/מחיקה בתוך התקייה |
| `x` | 1 | הרצה | כניסה לתקייה |

**חישוב מספרי (Octal):**

```
rwx = 4+2+1 = 7    ← הכל
rw- = 4+2+0 = 6    ← קרא וכתוב
r-x = 4+0+1 = 5    ← קרא והרץ
r-- = 4+0+0 = 4    ← קריאה בלבד
--- = 0+0+0 = 0    ← כלום

דוגמה: chmod 755 file → rwxr-xr-x
             │││
             ││└── Other: r-x = 5
             │└─── Group: r-x = 5
             └──── User:  rwx = 7
```

---

### הדגמות

**בדיקת הרשאות קיימות:**

```bash
ls -la ~/investigation_$(date +%F)/processes/all_processes.txt
```
פלט:
```
-rw-r--r-- 1 student student 4.2K Jun 20 all_processes.txt
  ↑ ↑  ↑  ↑
  │ │  │  └── Other: r-- = קריאה בלבד
  │ │  └───── Group: r-- = קריאה בלבד
  │ └──────── User:  rw- = קריאה וכתיבה
  └────────── סוג: - = קובץ רגיל
```

**הגנה על קובץ הממצאים (רק הבעלים יכול לקרוא):**

```bash
chmod 600 ~/investigation_$(date +%F)/processes/all_processes.txt
ls -la ~/investigation_$(date +%F)/processes/all_processes.txt
```
פלט לאחר שינוי:
```
-rw------- 1 student student 4.2K Jun 20 all_processes.txt
     ↑
     כולם הוסרו — רק הבעלים קורא וכותב
```

**יצירת סקריפט והפיכתו להרצה:**

```bash
# צור סקריפט פשוט
echo '#!/bin/bash' > ~/investigation_$(date +%F)/collect_info.sh
echo 'echo "=== Hostname ===" >> report.txt' >> ~/investigation_$(date +%F)/collect_info.sh
echo 'hostname >> report.txt' >> ~/investigation_$(date +%F)/collect_info.sh
echo 'echo "=== Users ===" >> report.txt' >> ~/investigation_$(date +%F)/collect_info.sh
echo 'who >> report.txt' >> ~/investigation_$(date +%F)/collect_info.sh
```

```bash
# בדוק הרשאות לפני
ls -la ~/investigation_$(date +%F)/collect_info.sh
```
פלט:
```
-rw-r--r-- 1 student student 128 Jun 20 collect_info.sh
```
> הרשאת `x` (הרצה) **לא קיימת** — לא ניתן להריץ את הסקריפט עדיין

```bash
# ניסיון הרצה לפני הוספת הרשאה
./collect_info.sh
```
פלט:
```
bash: ./collect_info.sh: Permission denied
```

```bash
# הוסף הרשאת הרצה לבעלים
chmod u+x ~/investigation_$(date +%F)/collect_info.sh
ls -la ~/investigation_$(date +%F)/collect_info.sh
```
פלט:
```
-rwxr--r-- 1 student student 128 Jun 20 collect_info.sh
    ↑
    x נוסף לבעלים בלבד (u+x)
```

```bash
# הרץ את הסקריפט
cd ~/investigation_$(date +%F)
./collect_info.sh
cat report.txt
```
פלט:
```
=== Hostname ===
kali
=== Users ===
student  pts/0  2024-06-20 10:00 (:0)
```

**chmod עם אותיות (סימבולי):**

```bash
chmod o-r collect_info.sh        # הסר קריאה מ-Other
chmod g+w processes/              # הוסף כתיבה לקבוצה
chmod a-x collect_info.sh         # הסר הרצה מכולם (a = all)
chmod u+x,g+x collect_info.sh    # הוסף הרצה לבעלים ולקבוצה
```

---

**משימות — שלב 3:**

- [ ] הרץ `ls -la` על קבצי ה-`processes/` — מה ההרשאות הנוכחיות?
- [ ] הגן על `all_processes.txt` עם `chmod 600`
- [ ] צור את `collect_info.sh` כמו בדוגמה
- [ ] נסה להריץ **לפני** `chmod` — מה הודעת השגיאה?
- [ ] הוסף הרשאת הרצה עם `chmod u+x` והרץ שוב — הצליח?

---

## שלב 4 — חיפוש קבצים עם `find` ו-`locate` ⏱ 7 דקות

### `find` — חיפוש בזמן אמת

```bash
find [ספרייה] [תנאי] [פעולה]
```

**מציאת הקבצים שיצרנו בחקירה:**

```bash
# מצא את כל הקבצים בתקיית החקירה
find ~/investigation_$(date +%F) -type f
```
פלט לדוגמה:
```
/home/student/investigation_2024-06-20/system_info.txt
/home/student/investigation_2024-06-20/report.txt
/home/student/investigation_2024-06-20/collect_info.sh
/home/student/investigation_2024-06-20/processes/all_processes.txt
/home/student/investigation_2024-06-20/processes/root_processes.txt
```

**חיפוש לפי סיומת:**

```bash
find ~/investigation_$(date +%F) -name "*.txt"
```
פלט:
```
/home/student/investigation_2024-06-20/system_info.txt
/home/student/investigation_2024-06-20/report.txt
/home/student/investigation_2024-06-20/processes/all_processes.txt
/home/student/investigation_2024-06-20/processes/root_processes.txt
```

**חיפוש לפי הרשאות:**

```bash
# מצא קבצים עם הרשאות 600 (שהגנו עליהם)
find ~/investigation_$(date +%F) -perm 600
```
פלט:
```
/home/student/investigation_2024-06-20/processes/all_processes.txt
```

**חיפוש קבצים שניתן להריץ:**

```bash
find ~/investigation_$(date +%F) -perm /111 -type f
```
פלט:
```
/home/student/investigation_2024-06-20/collect_info.sh
```

**חיפוש קבצים שנוצרו בדקות האחרונות:**

```bash
find ~/investigation_$(date +%F) -mmin -30
```
פלט:
```
/home/student/investigation_2024-06-20
/home/student/investigation_2024-06-20/system_info.txt
/home/student/investigation_2024-06-20/processes/all_processes.txt
... (כל הקבצים מה-30 דקות האחרונות)
```

**שמירת ממצאי find לקובץ:**

```bash
find ~/investigation_$(date +%F) -type f > ~/investigation_$(date +%F)/files/file_list.txt
cat ~/investigation_$(date +%F)/files/file_list.txt
```

---

### `locate` — חיפוש מהיר ממסד נתונים

```bash
# עדכן את ה-database (חובה לפני חיפוש קבצים חדשים)
sudo updatedb
```
פלט:
```
(שקט — עדכון שקט = הצלחה)
```

```bash
# חפש את קבצי החקירה שלנו
locate system_info.txt
```
פלט לדוגמה:
```
/home/student/investigation_2024-06-20/system_info.txt
```

```bash
# חפש לפי חלק משם
locate investigation
```
פלט לדוגמה:
```
/home/student/investigation_2024-06-20
/home/student/investigation_2024-06-20/collect_info.sh
/home/student/investigation_2024-06-20/report.txt
/home/student/investigation_2024-06-20/system_info.txt
/home/student/investigation_2024-06-20/files/file_list.txt
/home/student/investigation_2024-06-20/processes/all_processes.txt
/home/student/investigation_2024-06-20/processes/root_processes.txt
```

**השוואה מהירה — מתי להשתמש במה:**

```
find  → כשצריך תנאים (גודל, זמן, הרשאות) | מוצא קבצים חדשים
locate → כשרוצים מהירות | לא מוצא קבצים עד sudo updatedb
```

---

**משימות — שלב 4:**

- [ ] הרץ `find ~/investigation_$(date +%F) -type f` — כמה קבצים יש?
- [ ] מצא קבצים עם הרשאות 600: `find ~/investigation_$(date +%F) -perm 600`
- [ ] הרץ `sudo updatedb` ואז `locate system_info.txt` — נמצא?
- [ ] שמור את רשימת הקבצים ל-`files/file_list.txt`

---

## שלב 5 — סיום תהליכים עם `kill` ⏱ 5 דקות

### מה זה `kill`?

הפקודה `kill` שולחת **signal** לתהליך.  
Signal הוא הודעה קצרה שהמערכת שולחת לתהליך — "עצור", "הפסק", "רענן".

| Signal | מספר | משמעות | מתי משתמשים |
|--------|------|---------|-------------|
| `SIGTERM` | 15 | בקשה נעימה לסיום | ברירת המחדל — נותן לתהליך לסגור בסדר |
| `SIGKILL` | 9 | כיבוי כוחני מיידי | כשהתהליך לא מגיב ל-SIGTERM |
| `SIGHUP` | 1 | רענון הגדרות | שרתים (nginx, apache) — reload |

```
kill PID          ← שולח SIGTERM (15) — ברירת מחדל
kill -9 PID       ← שולח SIGKILL — "מוות מיידי"
kill -15 PID      ← שולח SIGTERM במפורש
killall sleep     ← הרוג את כל התהליכים בשם "sleep"
pkill -f sleep    ← הרוג לפי שם תהליך (גמיש יותר)
```

---

### הדגמות

**זכור את ה-`sleep 1000` שהפעלנו בשלב 2? עכשיו נסיים אותו.**

**שלב א — מצא את ה-PID:**

```bash
ps aux | grep sleep
```
פלט לדוגמה:
```
student  1456  0.0  0.0  13360  724 pts/0  S  11:05  0:00 sleep 1000
student  1890  0.0  0.0  13360  712 pts/0  S+ 11:20  0:00 grep --color=auto sleep
```
> PID של sleep = `1456` (לא של grep!)

**שלב ב — שלח SIGTERM (סיום נעים):**

```bash
kill 1456
```
פלט:
```
(שקט — Signal נשלח)
```

```bash
# ודא שהתהליך נסגר
ps aux | grep sleep
```
פלט אחרי kill:
```
student  1891  0.0  0.0  13360  712 pts/0  S+ 11:20  0:00 grep --color=auto sleep
```
> שורת ה-`sleep 1000` נעלמה — התהליך מת!

בטרמינל גם תראה:
```
[1]+  Terminated              sleep 1000
```

---

**הפעלת תהליך עיקש ושימוש ב-kill -9:**

```bash
# הפעל sleep חדש ברקע
sleep 2000 &
```
פלט:
```
[1] 2001
```

```bash
# מצא PID
ps aux | grep "sleep 2000"
```
פלט:
```
student  2001  0.0  0.0  13360  724 pts/0  S  11:22  0:00 sleep 2000
```

```bash
# כבה בכוח עם -9
kill -9 2001
ps aux | grep "sleep 2000"
```
פלט לאחר kill -9:
```
[1]+  Killed                  sleep 2000
```
> `Killed` (לעומת `Terminated`) = SIGKILL שימש

---

**שמירת תיעוד ה-kill:**

```bash
echo "=== KILLED PROCESSES ===" > ~/investigation_$(date +%F)/processes/killed_log.txt
echo "PID 1456 - sleep 1000 - SIGTERM - $(date)" >> ~/investigation_$(date +%F)/processes/killed_log.txt
echo "PID 2001 - sleep 2000 - SIGKILL - $(date)" >> ~/investigation_$(date +%F)/processes/killed_log.txt
cat ~/investigation_$(date +%F)/processes/killed_log.txt
```
פלט:
```
=== KILLED PROCESSES ===
PID 1456 - sleep 1000 - SIGTERM - Thu Jun 20 11:20:00 IDT 2024
PID 2001 - sleep 2000 - SIGKILL - Thu Jun 20 11:22:00 IDT 2024
```

---

**משימות — שלב 5:**

- [ ] הרץ `ps aux | grep sleep` — מצא את ה-PID של ה-sleep שהפעלת בשלב 2
- [ ] שלח לו `kill <PID>` — ודא שנסגר עם `ps aux | grep sleep`
- [ ] הפעל `sleep 2000 &` חדש, ורוג אותו עם `kill -9`
- [ ] שמור את ה-kills ל-`processes/killed_log.txt`

---

## שלב 6 — העברת תקיית החקירה ⏱ 3 דקות

### סיכום — מה יש לנו?

```bash
# הצג את כל מה שאספנו
find ~/investigation_$(date +%F) -type f
```
פלט לדוגמה:
```
/home/student/investigation_2024-06-20/system_info.txt
/home/student/investigation_2024-06-20/report.txt
/home/student/investigation_2024-06-20/collect_info.sh
/home/student/investigation_2024-06-20/files/file_list.txt
/home/student/investigation_2024-06-20/processes/all_processes.txt
/home/student/investigation_2024-06-20/processes/root_processes.txt
/home/student/investigation_2024-06-20/processes/killed_log.txt
```

```bash
# גודל כל תקיית החקירה
du -sh ~/investigation_$(date +%F)
```
פלט לדוגמה:
```
52K     /home/student/investigation_2024-06-20
```

---

### העברה למיקום קבוע

חוקר מסיים חקירה → **מעביר את כל הממצאים לארכיון**.

```bash
# צור תקיית ארכיון (אם לא קיימת)
mkdir -p ~/archive
```

```bash
# העבר את כל תקיית החקירה לארכיון
mv ~/investigation_$(date +%F) ~/archive/
```

```bash
# ודא שהתקייה הועברה
ls ~/archive/
```
פלט:
```
investigation_2024-06-20
```

```bash
# ודא שנעלמה מ-home
ls ~/
```
פלט:
```
Desktop  Documents  Downloads  archive
```
> `investigation_2024-06-20` נעלמה מ-home ועברה ל-`archive/`

```bash
# ודא שכל הקבצים שרדו את ההעברה
find ~/archive/investigation_$(date +%F) -type f
```
פלט:
```
/home/student/archive/investigation_2024-06-20/system_info.txt
/home/student/archive/investigation_2024-06-20/report.txt
/home/student/archive/investigation_2024-06-20/collect_info.sh
/home/student/archive/investigation_2024-06-20/files/file_list.txt
/home/student/archive/investigation_2024-06-20/processes/all_processes.txt
/home/student/archive/investigation_2024-06-20/processes/root_processes.txt
/home/student/archive/investigation_2024-06-20/processes/killed_log.txt
```

---

**משימות — שלב 6:**

- [ ] הרץ `find ~/investigation_$(date +%F) -type f` — כמה קבצים נאספו בסך הכל?
- [ ] העבר את כל תקיית החקירה ל-`~/archive/` עם `mv`
- [ ] ודא שהתקייה נעלמה מ-`~/` ונמצאת ב-`~/archive/`
- [ ] ודא שכל הקבצים שרדו עם `find ~/archive/ -type f`

---

## סיכום הפקודות

```bash
# ── ניהול תקיות ──────────────────────────────────────────
mkdir -p dir/subdir              # צור תקיות כולל תת-תקיות
mv source/ destination/          # העבר תקייה
du -sh directory/                # גודל תקייה

# ── שמירת פלטים ──────────────────────────────────────────
command > file.txt               # שמור פלט (מחליף)
command >> file.txt              # הוסף פלט לקיים
echo "text" >> file.txt          # הוסף שורת טקסט

# ── תהליכים (ps) ─────────────────────────────────────────
ps aux                           # כל התהליכים
ps aux | grep name               # חפש תהליך לפי שם
ps -ef --forest                  # הצג כעץ הורים
command &                        # הפעל ברקע

# ── הרשאות (chmod) ───────────────────────────────────────
chmod 600 file      # rw------- בעלים בלבד
chmod 644 file      # rw-r--r-- קריאה לכולם
chmod 755 file      # rwxr-xr-x הרצה לכולם
chmod u+x file      # הוסף הרצה לבעלים
chmod o-r file      # הסר קריאה מ-Other

# ── חיפוש (find) ─────────────────────────────────────────
find ~/dir -type f              # קבצים בלבד
find ~/dir -name "*.txt"        # לפי שם
find ~/dir -perm 600            # לפי הרשאות
find ~/dir -mmin -30            # שונה בחצי שעה אחרונה

# ── חיפוש (locate) ───────────────────────────────────────
sudo updatedb                   # עדכן database
locate filename                 # חפש קובץ

# ── סיום תהליכים (kill) ──────────────────────────────────
kill PID                        # SIGTERM — סיום נעים
kill -9 PID                     # SIGKILL — סיום כוחני
killall name                    # הרוג לפי שם
```

---

*LINOX LAB — Review | מעבדת חזרה משולבת*
