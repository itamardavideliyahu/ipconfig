# חיפוש קבצים רגישים בלינוקס
### מעבדת סייבר — רמת מתחילים

> **דרישה מוקדמת:** השלמת מעבדת LINOX הבסיסית (ניווט, find, locate)  
> **זמן משוער:** ~60 דקות  
> **מטרה:** להכיר קבצים רגישים במערכת לינוקס, להבין למה הם רגישים, ולדעת איך מוצאים אותם

---

## למה חיפוש קבצים רגישים?

בעולם הסייבר, **המידע הכי חשוב לתוקף נמצא לעתים קרובות בקבצי מערכת רגילים לגמרי**.  
הבנה של אילו קבצים קיימים, מה הם מכילים ומי יכול לגשת אליהם — היא כלי יסודי גם למגן (Blue Team) וגם לתוקף (Red Team / Pentest).

```
מנקודת מבט של תוקף:   מצא קבצים רגישים → הבן את המערכת → הסלם הרשאות
מנקודת מבט של מגן:    מצא קבצים רגישים → בדוק הרשאות → סגור חורים
```

---

## חלק 1 — קבצי משתמשים והרשאות

### `/etc/passwd` — רשימת המשתמשים

קובץ זה מכיל את **כל המשתמשים** במערכת.  
בניגוד למה שנשמע — הוא **קריא לכולם** (זה בכוונה, תוכנות רבות צריכות אותו).

**מבנה שורה:**
```
username:x:UID:GID:comment:home_dir:shell
student  :x:1000:1000:Student User:/home/student:/bin/bash
root     :x:0   :0   :root        :/root        :/bin/bash
```

| שדה | משמעות | למה מעניין בסייבר |
|-----|---------|------------------|
| username | שם המשתמש | ידיעת שמות משתמשים = צעד ראשון בפריצה |
| `x` | הסיסמה ב-`/etc/shadow` | אם כתוב סיסמה ישירות — בעיה קריטית |
| UID=0 | הרשאות root | כל משתמש עם UID 0 = מנהל מערכת |
| shell=`/bin/bash` | יש Shell פעיל | חשבונות שירות לא אמורים להחזיק Shell |

**הדגמות:**

```bash
# הצג את כל המשתמשים
cat /etc/passwd
```

```bash
# חפש רק משתמשים שיש להם shell אמיתי (לא /nologin או /false)
grep -v "nologin\|false" /etc/passwd
```

```bash
# חפש משתמשים עם UID 0 (כולם מנהלי מערכת!)
awk -F: '($3==0)' /etc/passwd
```
> אם יש יותר מ-root עם UID 0 — **זה חשוד מאוד**

```bash
# ספור כמה משתמשים יש במערכת
wc -l /etc/passwd
```

---

### `/etc/shadow` — קובץ הסיסמאות המוצפנות

כאן נמצאות **ה-hash של הסיסמאות**. בניגוד ל-`/etc/passwd`:
- **קריאה מוגבלת לroot בלבד**
- אם תוקף משיג גישה לקובץ הזה — הוא יכול לנסות לפצח את ה-hash

```bash
# ניסיון לקרוא את הקובץ (ייכשל ללא הרשאות)
cat /etc/shadow
```
פלט צפוי:
```
cat: /etc/shadow: Permission denied
```

```bash
# קריאה עם הרשאות root
sudo cat /etc/shadow
```
פלט לדוגמה:
```
root:$y$j9T$abc123...:19900:0:99999:7:::
student:$y$j9T$xyz789...:19800:0:99999:7:::
```

**מה ה-hash אומר לנו:**
```
$y$    → אלגוריתם yescrypt (מודרני, חזק)
$6$    → SHA-512 (נפוץ)
$1$    → MD5 (ישן ופגיע!)
*      → חשבון מנוטרל (ללא סיסמה)
!      → חשבון נעול
```
> חשבון עם `*` או `!` = לא ניתן להתחברות ישירה

---

### `/etc/sudoers` — מי מורשה להריץ פקודות כ-root

קובץ זה קובע **מי יכול להשתמש ב-`sudo`** ואיזה פקודות מותר לו להריץ.

```bash
# צפייה בקובץ (דורש הרשאות)
sudo cat /etc/sudoers
```

```bash
# הדרך המומלצת לצפות
sudo visudo -c
```

```bash
# חיפוש משתמשים שיש להם sudo ללא סיסמה (מסוכן מאוד!)
sudo grep -i "NOPASSWD" /etc/sudoers /etc/sudoers.d/* 2>/dev/null
```
> שורה כמו `student ALL=(ALL) NOPASSWD: ALL` = כל אחד שנכנס כ-student יכול לעשות כל דבר ללא סיסמה!

---

**משימות — חלק 1:**

- [ ] הרץ `cat /etc/passwd` — זהה את המשתמשים בעלי `/bin/bash` כ-Shell
- [ ] הרץ `awk -F: '($3==0)' /etc/passwd` — האם יש יותר ממשתמש root אחד?
- [ ] נסה `cat /etc/shadow` ללא `sudo` — מה הפלט? מה זה אומר?
- [ ] הרץ `sudo grep "NOPASSWD" /etc/sudoers 2>/dev/null` — נמצא משהו?

---

## חלק 2 — מפתחות SSH

### מה זה SSH Key?

SSH מאפשר חיבור מאובטח למחשב מרחוק. ניתן להתחבר עם **סיסמה** או עם **מפתח פרטי** (private key).  
אם תוקף מוצא **מפתח פרטי** — הוא יכול להתחבר לכל שרת שמכיר את המפתח הציבורי המתאים **ללא סיסמה**.

```
~/.ssh/id_rsa          ← מפתח פרטי   (SECRET! לא לשתף לעולם)
~/.ssh/id_rsa.pub      ← מפתח ציבורי (בטוח לשתף)
~/.ssh/authorized_keys ← רשימת מפתחות מורשים להתחבר
~/.ssh/known_hosts     ← שרתים מוכרים
```

---

### הדגמות

**חיפוש מפתחות SSH בכל המערכת:**

```bash
find / -name "id_rsa" -o -name "*.pem" -o -name "*.key" 2>/dev/null
```
פלט לדוגמה:
```
/home/student/.ssh/id_rsa
/root/.ssh/id_rsa
/opt/backup/server.key
```
> כל `.pem` או `.key` שנמצא מחוץ לספריות רגילות — **חשוד**

**בדיקת הרשאות על מפתח פרטי:**

```bash
ls -la ~/.ssh/
```
פלט תקין:
```
-rw------- 1 student student 2610 Jun 20 id_rsa       ← 600 = בעלים בלבד
-rw-r--r-- 1 student student  575 Jun 20 id_rsa.pub   ← 644 = קריא לכולם (בסדר)
```
> אם ה-`id_rsa` קריא לכולם (permissions `644` או `777`) — זה **חור אבטחה**

**חיפוש authorized_keys בכל המערכת:**

```bash
find / -name "authorized_keys" 2>/dev/null
```
> מראה לאילו שרתים יש גישה מהמכונה הזו

**הצגת תוכן authorized_keys:**

```bash
cat ~/.ssh/authorized_keys 2>/dev/null
```

---

**משימות — חלק 2:**

- [ ] הרץ `find / -name "id_rsa" 2>/dev/null` — נמצאו מפתחות?
- [ ] הרץ `ls -la ~/.ssh/` — בדוק שה-`id_rsa` מוגן (הרשאות 600)
- [ ] חפש קבצי `.pem` ו-`.key`: `find / -name "*.pem" -o -name "*.key" 2>/dev/null`
- [ ] הרץ `find / -name "authorized_keys" 2>/dev/null` — נמצא היכן?

---

## חלק 3 — קבצי היסטוריה

### `.bash_history` — מה המשתמש עשה בעבר

הפקודות שהמשתמש הריץ **נשמרות אוטומטית** בקובץ זה.  
לתוקף, זה כמו למצוא יומן פעולות — כולל סיסמאות שהוקלדו בטעות!

```bash
# הצג היסטוריית הפקודות של המשתמש הנוכחי
cat ~/.bash_history
```

```bash
# חפש סיסמאות שנכתבו בטעות בשורת הפקודה
grep -i "pass\|passwd\|password\|secret\|token" ~/.bash_history
```

```bash
# חפש היסטוריה של כל המשתמשים (דורש הרשאות)
find /home -name ".bash_history" 2>/dev/null
sudo find /root -name ".bash_history" 2>/dev/null
```

```bash
# הצג 20 הפקודות האחרונות
tail -20 ~/.bash_history
```

> **טיפ:** מפתחים לפעמים מריצים `mysql -u root -pMySecret123` — הסיסמה נשמרת בהיסטוריה!

---

**משימות — חלק 3:**

- [ ] הרץ `cat ~/.bash_history` — כמה פקודות שמורות?
- [ ] הרץ `grep -i "pass" ~/.bash_history` — נמצא משהו חשוד?
- [ ] הרץ `find /home -name ".bash_history" 2>/dev/null` — כמה קבצים נמצאו?

---

## חלק 4 — קבצי הגדרות עם סיסמאות

### קבצי `.env` — סביבת עבודה של אפליקציות

מפתחים משתמשים בקבצי `.env` לאחסון **פרטי חיבור, סיסמאות ומפתחות API**.  
הם אמורים **לא** להיות נגישים לציבור — אבל לעתים הם נשכחים.

```bash
# חפש קבצי .env בכל המערכת
find / -name ".env" -type f 2>/dev/null
```

```bash
# חפש קבצי config עם מילת "password" בתוכן
grep -r "password" /etc/ 2>/dev/null | grep -v "Binary"
```

```bash
# חפש קבצי הגדרות נפוצים של אפליקציות ווב
find / -name "wp-config.php" -o -name "config.php" -o -name "database.yml" 2>/dev/null
```

```bash
# חפש קבצי סיסמאות בספריות הבית
find /home -name "*.txt" -o -name "*.conf" -o -name "*.cfg" 2>/dev/null | head -20
```

**דוגמה לתוכן קובץ `.env` מסוכן:**
```
DB_HOST=localhost
DB_USER=admin
DB_PASS=SuperSecret123!    ← סיסמת מסד נתונים
API_KEY=sk-abc123xyz789    ← מפתח API
SECRET_TOKEN=mytoken456    ← טוקן אפליקציה
```

---

**משימות — חלק 4:**

- [ ] הרץ `find / -name ".env" -type f 2>/dev/null` — נמצאו קבצים?
- [ ] הרץ `grep -r "password" /etc/ 2>/dev/null | grep -v "Binary" | head -10`
- [ ] חפש `wp-config.php` ו-`config.php` — נמצאו?

---

## חלק 5 — קבצים עם הרשאות מסוכנות

### SUID — הרצת קובץ עם הרשאות הבעלים

קובץ עם **SUID bit** ירוץ עם הרשאות הבעלים שלו — לא עם הרשאות המשתמש שמריץ.  
אם קובץ שייך ל-root ויש לו SUID — כל משתמש שמריץ אותו מקבל הרשאות root!

```
-rwsr-xr-x   ← ה-s במקום x = SUID מופעל
       ↑
    המשתמש שמריץ מקבל הרשאות של הבעלים (root)
```

```bash
# מצא כל הקבצים עם SUID ושייכים ל-root
find / -perm -4000 -type f 2>/dev/null
```
פלט לדוגמה:
```
/usr/bin/passwd     ← תקין (כדי לשנות סיסמה)
/usr/bin/sudo       ← תקין
/usr/bin/mount      ← תקין
/tmp/backdoor       ← חשוד מאוד! למה יש SUID ב-/tmp?
```

```bash
# חיפוש מורחב: SUID + SGID
find / -perm /6000 -type f 2>/dev/null
```

> כל קובץ עם SUID שנמצא ב-`/tmp`, `/var`, `/home` — **חשוד מאוד**

---

### קבצים שכולם יכולים לכתוב בהם (World-Writable)

קובץ עם `777` או `666` — כל אחד יכול לשנות אותו.  
אם מדובר בסקריפט שרץ אוטומטית (cron) — תוקף יכול להזריק פקודות.

```bash
# מצא קבצים שכולם יכולים לכתוב בהם (לא כולל /proc ו-/sys)
find / -writable -type f 2>/dev/null | grep -v "^/proc\|^/sys\|^/dev"
```

```bash
# מצא ספריות שכולם יכולים לכתוב בהן
find / -writable -type d 2>/dev/null | grep -v "^/proc\|^/sys\|^/dev\|^/tmp"
```

---

**משימות — חלק 5:**

- [ ] הרץ `find / -perm -4000 -type f 2>/dev/null` — רשום את הקבצים עם SUID
- [ ] האם יש קבצי SUID ב-`/tmp` או `/var`? (אם כן — חשוד!)
- [ ] הרץ `find / -writable -type f 2>/dev/null | grep -v "^/proc\|^/sys\|^/dev" | head -15`

---

## חלק 6 — קבצי לוג ומשימות מתוזמנות

### קבצי לוג — עדויות לפעילות במערכת

לוגים מתעדים **כל פעולה** במערכת — כניסות, שגיאות, שינויים.  
הם שימושיים גם לתוקף (להבין מה קורה) וגם למגן (לזהות פעילות חשודה).

```bash
# לוג כניסות וניסיונות כניסה כושלים
sudo cat /var/log/auth.log | tail -20
```

```bash
# חיפוש ניסיונות כניסה כושלים (Brute Force)
sudo grep "Failed password" /var/log/auth.log | tail -10
```
פלט לדוגמה:
```
Jun 20 10:15:33 server sshd: Failed password for root from 192.168.1.100 port 4455
Jun 20 10:15:34 server sshd: Failed password for root from 192.168.1.100 port 4456
Jun 20 10:15:35 server sshd: Failed password for root from 192.168.1.100 port 4457
```
> מאות ניסיונות מאותה IP = מתקפת Brute Force

```bash
# חיפוש כניסות מוצלחות
sudo grep "Accepted password\|Accepted publickey" /var/log/auth.log | tail -10
```

---

### Cron Jobs — משימות מתוזמנות

Cron מריץ סקריפטים **באופן אוטומטי** בזמנים קבועים.  
אם סקריפט של cron כתוב ב-`/tmp` או שיש לו הרשאות פתוחות — **זה חור אבטחה**.

```bash
# הצג את ה-cron jobs של המשתמש הנוכחי
crontab -l
```

```bash
# הצג cron jobs של כל המשתמשים (דורש הרשאות)
sudo ls -la /var/spool/cron/crontabs/
```

```bash
# הצג cron jobs ברמת מערכת
ls -la /etc/cron*
cat /etc/crontab
```

```bash
# חפש סקריפטים שה-cron מריץ ויש להם הרשאות פתוחות
find /etc/cron* -type f 2>/dev/null | xargs ls -la 2>/dev/null
```

---

**משימות — חלק 6:**

- [ ] הרץ `sudo grep "Failed password" /var/log/auth.log 2>/dev/null | tail -10` — נמצאו ניסיונות?
- [ ] הרץ `crontab -l` — יש משימות מתוזמנות?
- [ ] הרץ `cat /etc/crontab` — אילו סקריפטים רצים אוטומטית?

---

## סיכום — רשימת חיפוש מהירה (Cheat Sheet)

### חיפוש ממוקד לפנטסטינג

```bash
# 1. משתמשים עם UID 0 (root נוסף?)
awk -F: '($3==0)' /etc/passwd

# 2. משתמשים עם shell אמיתי
grep -v "nologin\|false" /etc/passwd

# 3. sudo ללא סיסמה
sudo grep "NOPASSWD" /etc/sudoers /etc/sudoers.d/* 2>/dev/null

# 4. מפתחות SSH פרטיים
find / -name "id_rsa" -o -name "*.pem" -o -name "*.key" 2>/dev/null

# 5. קבצי .env עם סיסמאות
find / -name ".env" 2>/dev/null

# 6. סיסמאות בהיסטוריה
grep -i "pass\|secret\|key\|token" ~/.bash_history

# 7. קבצים עם SUID (הרצה כ-root)
find / -perm -4000 -type f 2>/dev/null

# 8. קבצים שכולם יכולים לכתוב בהם
find / -writable -type f 2>/dev/null | grep -v "^/proc\|^/sys\|^/dev"

# 9. כניסות כושלות (Brute Force)
sudo grep "Failed password" /var/log/auth.log | tail -20

# 10. cron jobs חשודים
cat /etc/crontab; ls /etc/cron*
```

---

### מה עושים עם המידע שמצאנו?

| ממצא | משמעות | פעולה נדרשת |
|------|---------|------------|
| UID 0 למשתמש שאינו root | חשבון backdoor | בדוק מתי נוצר, מחק אם חשוד |
| NOPASSWD ב-sudoers | הרשאת root ללא סיסמה | הסר הרשאה מיותרת |
| `id_rsa` עם הרשאות 644 | מפתח פרטי חשוף | `chmod 600 ~/.ssh/id_rsa` |
| סיסמה בהיסטוריה | חשיפת credentials | שנה סיסמה, `history -c` |
| קובץ SUID ב-`/tmp` | backdoor מותקן | בדוק מיד, הסר |
| מאות Failed password | Brute Force פעיל | חסום IP ב-firewall |

---

> **זכור:** המעבדה הזו מיועדת לסביבת תרגול בלבד.  
> חיפוש קבצים רגישים על מערכות ללא אישור = עבירה פלילית.

---

*LINOX LAB — Sensitive Files | Cyber Course | מעבדת חיפוש קבצים רגישים*
