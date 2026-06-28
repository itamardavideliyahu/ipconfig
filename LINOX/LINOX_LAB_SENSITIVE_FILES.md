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
username : x  : UID  : GID  : comment      : home_dir       : shell
root     : x  : 0    : 0    : root         : /root          : /bin/bash
student  : x  : 1000 : 1000 : Student User : /home/student  : /bin/bash
www-data : x  : 33   : 33   : www-data     : /var/www        : /usr/sbin/nologin
```

| שדה | משמעות | למה מעניין בסייבר |
|-----|---------|------------------|
| username | שם המשתמש | ידיעת שמות משתמשים = צעד ראשון בפריצה |
| `x` | הסיסמה ב-`/etc/shadow` | אם כתוב סיסמה ישירות — בעיה קריטית |
| UID=0 | הרשאות root | כל משתמש עם UID 0 = מנהל מערכת |
| shell=`/bin/bash` | יש Shell פעיל | חשבונות שירות לא אמורים להחזיק Shell |

---

**הצגת כל המשתמשים:**

```bash
cat /etc/passwd
```
פלט לדוגמה:
```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
student:x:1000:1000:Student User:/home/student:/bin/bash
mysql:x:1001:1001:MySQL Server:/var/lib/mysql:/usr/sbin/nologin
backdoor:x:0:0::/home/backdoor:/bin/bash   ← UID 0 — חשוד!
```

---

**חיפוש משתמשים עם Shell אמיתי (יכולים להתחבר):**

```bash
grep -v "nologin\|false" /etc/passwd
```
פלט לדוגמה:
```
root:x:0:0:root:/root:/bin/bash
student:x:1000:1000:Student User:/home/student:/bin/bash
backdoor:x:0:0::/home/backdoor:/bin/bash
```
> רק אלה הם משתמשים שיכולים לפתוח session אמיתי. השאר חסומים.

---

**חיפוש משתמשים עם UID 0 (כל אחד מהם = מנהל מערכת):**

```bash
awk -F: '($3==0)' /etc/passwd
```
פלט תקין (משתמש אחד בלבד):
```
root:x:0:0:root:/root:/bin/bash
```
פלט חשוד (שני משתמשים עם UID 0!):
```
root:x:0:0:root:/root:/bin/bash
backdoor:x:0:0::/home/backdoor:/bin/bash   ← ALERT! backdoor עם הרשאות root
```
> אם מופיע יותר ממשתמש אחד — **זה סימן לפריצה**

---

**ספירת משתמשים במערכת:**

```bash
wc -l /etc/passwd
```
פלט:
```
32 /etc/passwd
```
> מספר גבוה מהצפוי יכול להצביע על חשבונות לא מוכרים

---

### `/etc/shadow` — קובץ הסיסמאות המוצפנות

כאן נמצאות **ה-hash של הסיסמאות**. בניגוד ל-`/etc/passwd`:
- **קריאה מוגבלת לroot בלבד**
- אם תוקף משיג גישה לקובץ הזה — הוא יכול לנסות לפצח את ה-hash

**ניסיון לקרוא ללא הרשאות (כמשתמש רגיל):**

```bash
cat /etc/shadow
```
פלט:
```
cat: /etc/shadow: Permission denied
```
> זה **תקין** — המערכת מגנה על הקובץ. אם הפקודה הצליחה ללא sudo — יש בעיה!

---

**קריאה עם הרשאות root:**

```bash
sudo cat /etc/shadow
```
פלט לדוגמה:
```
root:$y$j9T$hKz8Abc123xyz:19900:0:99999:7:::
student:$6$rounds=656000$xyz$abc123hash...:19800:0:99999:7:::
mysql:*:19500:0:99999:7:::
www-data:!:19500::::::
```

**קריאת הפלט — מה כל שדה אומר:**
```
student : $6$rounds=656000$xyz$abc123... : 19800 : 0 : 99999 : 7 : : :
│         │                               │       │   │        │
│         └── hash הסיסמה                │       │   │        └── ימי אזהרה לפני פקיעה
│                                         │       │   └────────── מקסימום ימים בין שינויים
│                                         │       └────────────── מינימום ימים בין שינויים
│                                         └────────────────────── ימים מ-1/1/1970 עד שינוי אחרון
└── שם משתמש
```

**מה ה-hash אומר לנו:**
```
$y$    → yescrypt  — מודרני וחזק (קשה לפצח)
$6$    → SHA-512   — נפוץ, מאובטח
$5$    → SHA-256   — סביר
$1$    → MD5       — ישן ופגיע! ניתן לפצח מהר
*      → חשבון מנוטרל (ללא סיסמה, לא ניתן להתחבר)
!      → חשבון נעול ידנית
```

---

### `/etc/sudoers` — מי מורשה להריץ פקודות כ-root

**הצגת הקובץ:**

```bash
sudo cat /etc/sudoers
```
פלט לדוגמה (חלק):
```
# User privilege specification
root    ALL=(ALL:ALL) ALL

# Members of the admin group may gain root privileges
%sudo   ALL=(ALL:ALL) ALL

# Student can run apt only
student ALL=(ALL) /usr/bin/apt

# DANGEROUS LINE:
deploy  ALL=(ALL) NOPASSWD: ALL
```

---

**חיפוש ספציפי לשורות NOPASSWD (מסוכן מאוד):**

```bash
sudo grep -i "NOPASSWD" /etc/sudoers /etc/sudoers.d/* 2>/dev/null
```
פלט תקין — ריק (אין שורות כאלו):
```
(no output)
```
פלט חשוד:
```
/etc/sudoers.d/deploy:deploy ALL=(ALL) NOPASSWD: ALL
```
> שורה כזו = המשתמש `deploy` יכול לעשות הכל כ-root **ללא סיסמה**!

---

**משימות — חלק 1:**

- [ ] הרץ `cat /etc/passwd` — זהה את המשתמשים בעלי `/bin/bash` כ-Shell
- [ ] הרץ `awk -F: '($3==0)' /etc/passwd` — האם יש יותר ממשתמש root אחד?
- [ ] נסה `cat /etc/shadow` ללא `sudo` — קיבלת Permission denied? (אם לא — בעיה!)
- [ ] הרץ `sudo grep "NOPASSWD" /etc/sudoers 2>/dev/null` — נמצא משהו?

---

## חלק 2 — מפתחות SSH

### מה זה SSH Key?

SSH מאפשר חיבור מאובטח למחשב מרחוק. ניתן להתחבר עם **סיסמה** או עם **מפתח פרטי** (private key).  
אם תוקף מוצא **מפתח פרטי** — הוא יכול להתחבר לכל שרת שמכיר את המפתח הציבורי המתאים **ללא סיסמה**.

```
~/.ssh/id_rsa          ← מפתח פרטי   (SECRET — לא לשתף לעולם!)
~/.ssh/id_rsa.pub      ← מפתח ציבורי (בטוח לשתף)
~/.ssh/authorized_keys ← מפתחות שמורשים להתחבר למכונה זו
~/.ssh/known_hosts     ← שרתים שהמכונה הזו מכירה
```

---

**חיפוש מפתחות SSH בכל המערכת:**

```bash
find / -name "id_rsa" -o -name "*.pem" -o -name "*.key" 2>/dev/null
```
פלט לדוגמה:
```
/home/student/.ssh/id_rsa
/root/.ssh/id_rsa
/opt/backup/server.key
/var/www/html/app/.env.key
```
> כל `.pem` או `.key` שנמצא **מחוץ ל-`~/.ssh/`** — חשוד וצריך בדיקה

---

**בדיקת הרשאות על מפתח פרטי:**

```bash
ls -la ~/.ssh/
```
פלט **תקין** (הרשאות 600 על הפרטי):
```
drwx------ 2 student student 4096 Jun 20 .
-rw------- 1 student student 2610 Jun 20 id_rsa        ← 600 = בעלים בלבד
-rw-r--r-- 1 student student  575 Jun 20 id_rsa.pub    ← 644 = ציבורי, בסדר
-rw-r--r-- 1 student student  222 Jun 20 known_hosts
```

פלט **מסוכן** (כולם יכולים לקרוא את המפתח הפרטי!):
```
-rw-r--r-- 1 student student 2610 Jun 20 id_rsa        ← 644 = כולם קוראים! ALERT
```
> תיקון: `chmod 600 ~/.ssh/id_rsa`

---

**חיפוש authorized_keys בכל המערכת:**

```bash
find / -name "authorized_keys" 2>/dev/null
```
פלט לדוגמה:
```
/home/student/.ssh/authorized_keys
/root/.ssh/authorized_keys
/home/deploy/.ssh/authorized_keys
```

**הצגת תוכן authorized_keys:**

```bash
cat ~/.ssh/authorized_keys 2>/dev/null
```
פלט לדוגמה:
```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAB... student@workstation
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABg... admin@unknown-machine
```
> שורה שנייה מ-`unknown-machine` — **מי הוסיף מפתח שאינו מוכר?**

---

**משימות — חלק 2:**

- [ ] הרץ `find / -name "id_rsa" 2>/dev/null` — נמצאו מפתחות?
- [ ] הרץ `ls -la ~/.ssh/` — בדוק שה-`id_rsa` מוגן (הרשאות 600)
- [ ] חפש קבצי `.pem` ו-`.key`: `find / -name "*.pem" -o -name "*.key" 2>/dev/null`
- [ ] הרץ `cat ~/.ssh/authorized_keys 2>/dev/null` — האם כל המפתחות מוכרים?

---

## חלק 3 — קבצי היסטוריה

### `.bash_history` — מה המשתמש עשה בעבר

הפקודות שהמשתמש הריץ **נשמרות אוטומטית** בקובץ זה.  
לתוקף, זה כמו למצוא יומן פעולות — כולל סיסמאות שהוקלדו בטעות!

---

**הצגת היסטוריית הפקודות:**

```bash
cat ~/.bash_history
```
פלט לדוגמה:
```
ls -la
cd /var/www/html
nano config.php
mysql -u root -pMySecret123 mydb
ssh admin@192.168.1.50
cat /etc/passwd
wget http://example.com/script.sh
chmod +x script.sh
./script.sh
```
> שורה 4 — **סיסמת MySQL גלויה לחלוטין!** `MySecret123`

---

**חיפוש ממוקד לסיסמאות בהיסטוריה:**

```bash
grep -i "pass\|passwd\|password\|secret\|token\|key" ~/.bash_history
```
פלט לדוגמה:
```
mysql -u root -pMySecret123 mydb
export API_KEY=sk-abc123xyz
curl -H "Authorization: Bearer mytoken456" https://api.example.com
sshpass -p "P@ssw0rd!" ssh user@server
```
> ארבע חשיפות credentials — שינוי סיסמה נדרש לכולן!

---

**הצגת 20 הפקודות האחרונות:**

```bash
tail -20 ~/.bash_history
```
פלט לדוגמה:
```
sudo su
cd /root
ls -la
cat /etc/shadow
nc -lvnp 4444
```
> `nc -lvnp 4444` = פתיחת listener של Netcat — **מאוד חשוד**

---

**חיפוש קבצי history של כל המשתמשים:**

```bash
find /home -name ".bash_history" 2>/dev/null
sudo find /root -name ".bash_history" 2>/dev/null
```
פלט לדוגמה:
```
/home/student/.bash_history
/home/deploy/.bash_history
/home/admin/.bash_history
/root/.bash_history
```
> יש history לכל אחד — כל אחד מהם שווה בדיקה

---

**משימות — חלק 3:**

- [ ] הרץ `cat ~/.bash_history` — כמה פקודות שמורות? יש משהו חשוד?
- [ ] הרץ `grep -i "pass\|secret\|token" ~/.bash_history` — נמצאו credentials?
- [ ] הרץ `tail -20 ~/.bash_history` — מה הפקודות האחרונות שרצו?
- [ ] הרץ `find /home -name ".bash_history" 2>/dev/null` — כמה קבצים נמצאו?

---

## חלק 4 — קבצי הגדרות עם סיסמאות

### קבצי `.env` ו-config — אחסון credentials של אפליקציות

מפתחים משתמשים בקבצי `.env` לאחסון **פרטי חיבור, סיסמאות ומפתחות API**.  
הם אמורים **לא** להיות נגישים לציבור — אבל לעתים הם נשכחים.

---

**חיפוש קבצי .env בכל המערכת:**

```bash
find / -name ".env" -type f 2>/dev/null
```
פלט לדוגמה:
```
/var/www/html/app/.env
/home/deploy/project/.env
/opt/webapp/.env.production
```

**הצגת תוכן קובץ .env שנמצא:**

```bash
cat /var/www/html/app/.env
```
פלט לדוגמה:
```
APP_ENV=production
APP_DEBUG=false

DB_HOST=localhost
DB_PORT=3306
DB_NAME=myapp_db
DB_USER=dbadmin
DB_PASS=Sup3rS3cret!        ← סיסמת מסד נתונים

MAIL_HOST=smtp.gmail.com
MAIL_USER=app@company.com
MAIL_PASS=gmailAppP@ss      ← סיסמת אימייל

AWS_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE     ← מפתח AWS!
AWS_SECRET_KEY=wJalrXUtnFEMI/K7MDENG   ← מסוכן מאוד
```

---

**חיפוש מילת "password" בתוך קבצי `/etc`:**

```bash
grep -r "password" /etc/ 2>/dev/null | grep -v "Binary"
```
פלט לדוגמה:
```
/etc/mysql/debian.cnf:password = debian-sys-maint
/etc/phpmyadmin/config-db.php:$dbpass='phpMyAdminPass';
/etc/roundcube/config.inc.php:$config['db_dsnw'] = 'mysql://rc_user:rcPass@localhost/roundcube';
```
> שלושה credentials שגלויים בקבצי הגדרות!

---

**חיפוש קבצי config של אפליקציות ווב:**

```bash
find / -name "wp-config.php" -o -name "config.php" -o -name "database.yml" 2>/dev/null
```
פלט לדוגמה:
```
/var/www/wordpress/wp-config.php
/var/www/html/config.php
/home/deploy/rails-app/config/database.yml
```

**הצגת wp-config.php שנמצא:**

```bash
cat /var/www/wordpress/wp-config.php 2>/dev/null | grep -i "DB_\|table_prefix"
```
פלט לדוגמה:
```
define( 'DB_NAME', 'wordpress' );
define( 'DB_USER', 'wp_user' );
define( 'DB_PASSWORD', 'wpDBpass123!' );
define( 'DB_HOST', 'localhost' );
$table_prefix = 'wp_';
```

---

**חיפוש קבצי טקסט בספריות הבית (לעתים שם סיסמאות):**

```bash
find /home -name "*.txt" -o -name "passwords*" -o -name "creds*" 2>/dev/null
```
פלט לדוגמה:
```
/home/student/notes.txt
/home/admin/passwords.txt
/home/deploy/creds.txt
```
> `passwords.txt` ו-`creds.txt` — **בדוק מיד!**

---

**משימות — חלק 4:**

- [ ] הרץ `find / -name ".env" -type f 2>/dev/null` — נמצאו קבצים? הצג תוכן עם `cat`
- [ ] הרץ `grep -r "password" /etc/ 2>/dev/null | grep -v "Binary" | head -10`
- [ ] חפש `wp-config.php` — נמצא? הצג את שדות DB_USER ו-DB_PASSWORD
- [ ] חפש קבצים חשודים: `find /home -name "passwords*" -o -name "creds*" 2>/dev/null`

---

## חלק 5 — קבצים עם הרשאות מסוכנות

### SUID — הרצת קובץ עם הרשאות הבעלים

קובץ עם **SUID bit** ירוץ עם הרשאות הבעלים שלו — לא עם הרשאות המשתמש שמריץ.  
אם קובץ שייך ל-root ויש לו SUID — כל משתמש שמריץ אותו מקבל הרשאות root!

**הסבר ויזואלי על הרשאות:**
```
-rwsr-xr-x  root  /usr/bin/passwd
  ↑
  s = SUID מופעל (במקום x)
  כל מי שמריץ passwd מקבל הרשאות root זמנית
  (כדי לשנות את /etc/shadow שנגיש רק ל-root)
```

---

**חיפוש קבצים עם SUID:**

```bash
find / -perm -4000 -type f 2>/dev/null
```
פלט **תקין** — רק קבצי מערכת רגילים:
```
/usr/bin/passwd
/usr/bin/sudo
/usr/bin/su
/usr/bin/mount
/usr/bin/umount
/usr/bin/newgrp
/usr/lib/openssh/ssh-keysign
```

פלט **חשוד** — SUID בספריות לא רגילות:
```
/usr/bin/passwd
/usr/bin/sudo
/tmp/rootshell          ← ALERT! קובץ עם SUID ב-/tmp
/var/tmp/privesc        ← ALERT! נשמע כמו privilege escalation
/home/student/.local/shell  ← ALERT! מחוץ למערכת
```

---

**חיפוש SUID + SGID יחד:**

```bash
find / -perm /6000 -type f 2>/dev/null
```
פלט לדוגמה:
```
/usr/bin/passwd
/usr/bin/sudo
/usr/bin/write          ← SGID: גישה לקבוצה tty
/usr/bin/wall           ← SGID: גישה לקבוצה tty
/usr/bin/crontab        ← SGID: גישה לקבוצה crontab
```

---

### קבצים שכולם יכולים לכתוב בהם (World-Writable)

קובץ עם `777` — כל אחד יכול לשנות אותו.  
אם זה סקריפט שרץ ב-cron כ-root — תוקף יכול להזריק פקודות.

**חיפוש קבצים שכולם יכולים לכתוב בהם:**

```bash
find / -writable -type f 2>/dev/null | grep -v "^/proc\|^/sys\|^/dev"
```
פלט **תקין** — רק קבצי tmp:
```
/tmp/tmpfile123
/var/tmp/session_abc
```

פלט **חשוד**:
```
/etc/cron.d/backup_script    ← ALERT! סקריפט cron שכולם יכולים לשנות!
/usr/local/bin/cleanup.sh    ← ALERT! סקריפט מערכת שכולם יכולים לשנות!
/tmp/rootshell
```

---

**חיפוש ספריות שכולם יכולים לכתוב בהן:**

```bash
find / -writable -type d 2>/dev/null | grep -v "^/proc\|^/sys\|^/dev\|^/tmp\|^/run"
```
פלט לדוגמה:
```
/var/spool/mail/student
/home/student/.cache
/srv/uploads              ← ספרייה שכולם יכולים לכתוב — תלוי בשימוש
```

---

**משימות — חלק 5:**

- [ ] הרץ `find / -perm -4000 -type f 2>/dev/null` — רשום את הקבצים עם SUID
- [ ] האם יש קבצי SUID ב-`/tmp`, `/var/tmp`, או `/home`? (אם כן — חשוד מאוד!)
- [ ] הרץ `find / -writable -type f 2>/dev/null | grep -v "^/proc\|^/sys\|^/dev" | head -15`
- [ ] האם יש קובץ writable ב-`/etc/` או `/usr/`? (אם כן — בעיה קריטית!)

---

## חלק 6 — קבצי לוג ומשימות מתוזמנות

### קבצי לוג — עדויות לפעילות במערכת

לוגים מתעדים **כל פעולה** במערכת — כניסות, שגיאות, שינויים.

**הצגת לוג כניסות אחרונות:**

```bash
sudo tail -20 /var/log/auth.log
```
פלט לדוגמה:
```
Jun 20 09:00:01 server CRON[1234]: pam_unix: session opened for user root
Jun 20 10:12:44 server sshd[5678]: Accepted publickey for student from 192.168.1.10 port 52341
Jun 20 10:15:33 server sshd[5679]: Failed password for root from 185.234.5.6 port 4455
Jun 20 10:15:34 server sshd[5680]: Failed password for root from 185.234.5.6 port 4456
Jun 20 10:15:35 server sshd[5681]: Failed password for root from 185.234.5.6 port 4457
Jun 20 10:15:36 server sshd[5682]: Failed password for root from 185.234.5.6 port 4458
```
> שורות 3-6 — **IP חיצוני ניסה 4 פעמים בשנייה** — זו מתקפת Brute Force!

---

**חיפוש ממוקד לניסיונות Brute Force:**

```bash
sudo grep "Failed password" /var/log/auth.log | tail -10
```
פלט לדוגמה:
```
Jun 20 10:15:33 server sshd: Failed password for root from 185.234.5.6 port 4455
Jun 20 10:15:34 server sshd: Failed password for root from 185.234.5.6 port 4456
Jun 20 10:15:35 server sshd: Failed password for root from 185.234.5.6 port 4457
```

**ספירת ניסיונות כושלים לפי IP (זיהוי מתקיף):**

```bash
sudo grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn | head -5
```
פלט לדוגמה:
```
847  185.234.5.6       ← IP תקפה 847 פעמים! חסום מיד
 23  192.168.1.99
  4  10.0.0.15
```

---

**חיפוש כניסות מוצלחות:**

```bash
sudo grep "Accepted password\|Accepted publickey" /var/log/auth.log | tail -10
```
פלט לדוגמה:
```
Jun 20 10:12:44 server sshd: Accepted publickey for student from 192.168.1.10 port 52341
Jun 20 11:30:02 server sshd: Accepted password for root from 185.234.5.6 port 4499
```
> שורה שנייה — אותה IP שניסתה Brute Force **הצליחה להיכנס כ-root**! **אירוע אבטחה קריטי!**

---

### Cron Jobs — משימות מתוזמנות

Cron מריץ סקריפטים **באופן אוטומטי** בזמנים קבועים. סקריפטים כאלה לעתים רצים כ-root.

**הצגת cron jobs של המשתמש הנוכחי:**

```bash
crontab -l
```
פלט תקין — ריק:
```
no crontab for student
```
פלט חשוד:
```
* * * * * /tmp/reverse_shell.sh
@reboot /home/student/.hidden/backdoor
```
> שתי שורות חשודות — סקריפטים שרצים מ-`/tmp` ומספריה מוסתרת

---

**הצגת cron jobs ברמת מערכת:**

```bash
cat /etc/crontab
```
פלט לדוגמה:
```
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m  h  dom  mon  dow  user   command
17 *  *  *  *   root   cd / && run-parts --report /etc/cron.hourly
25 6  *  *  *   root   test -x /usr/sbin/anacron || run-parts --report /etc/cron.daily
0  4  *  *  0   root   /usr/local/bin/backup.sh
```

**בדיקת הרשאות על הסקריפטים שה-cron מריץ:**

```bash
ls -la /usr/local/bin/backup.sh
```
פלט **תקין**:
```
-rwxr-xr-x 1 root root 512 Jun 10 backup.sh    ← רק root יכול לשנות
```
פלט **מסוכן**:
```
-rwxrwxrwx 1 root root 512 Jun 10 backup.sh    ← כולם יכולים לשנות! רץ כ-root!
```
> אם הסקריפט רץ כ-root וכולם יכולים לערוך אותו — **privilege escalation קלה**

---

**הצגת כל ספריות cron:**

```bash
ls -la /etc/cron*
```
פלט לדוגמה:
```
-rw-r--r-- 1 root root 1042 Jun 20 /etc/crontab

/etc/cron.d:
-rw-r--r-- 1 root root  102 Jun 20 .placeholder
-rw-r--r-- 1 root root  285 Jun 20 php
-rw-rw-rw- 1 root root  150 Jun 20 custom_job     ← כולם יכולים לשנות! ALERT

/etc/cron.daily:
-rwxr-xr-x 1 root root  376 Jun 20 logrotate
-rwxr-xr-x 1 root root  214 Jun 20 apt-compat
```

---

**משימות — חלק 6:**

- [ ] הרץ `sudo grep "Failed password" /var/log/auth.log 2>/dev/null | tail -10` — נמצאו ניסיונות?
- [ ] הרץ `sudo grep "Accepted" /var/log/auth.log 2>/dev/null | tail -5` — מי נכנס בהצלחה?
- [ ] הרץ `crontab -l` — יש משימות מתוזמנות חשודות?
- [ ] הרץ `cat /etc/crontab` — אילו סקריפטים רצים אוטומטית כ-root?

---

## סיכום — Cheat Sheet לפנטסטינג

```bash
# ── חשבונות ──────────────────────────────────────────────
awk -F: '($3==0)' /etc/passwd              # UID 0 = root נוסף?
grep -v "nologin\|false" /etc/passwd       # משתמשים עם shell
sudo grep "NOPASSWD" /etc/sudoers /etc/sudoers.d/* 2>/dev/null  # sudo ללא סיסמה

# ── מפתחות ───────────────────────────────────────────────
find / -name "id_rsa" -o -name "*.pem" -o -name "*.key" 2>/dev/null
find / -name "authorized_keys" 2>/dev/null
ls -la ~/.ssh/

# ── credentials ──────────────────────────────────────────
grep -i "pass\|secret\|token\|key" ~/.bash_history
find / -name ".env" -type f 2>/dev/null
grep -r "password" /etc/ 2>/dev/null | grep -v "Binary"
find / -name "wp-config.php" -o -name "config.php" 2>/dev/null

# ── הרשאות מסוכנות ───────────────────────────────────────
find / -perm -4000 -type f 2>/dev/null     # SUID
find / -writable -type f 2>/dev/null | grep -v "^/proc\|^/sys\|^/dev"  # World-Writable

# ── לוגים ────────────────────────────────────────────────
sudo grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn | head -5
sudo grep "Accepted" /var/log/auth.log | tail -20

# ── cron ─────────────────────────────────────────────────
crontab -l; cat /etc/crontab; ls -la /etc/cron*
```

---

### מה עושים עם המידע שמצאנו?

| ממצא | משמעות | פעולה נדרשת |
|------|---------|------------|
| UID 0 למשתמש שאינו root | backdoor / פריצה | בדוק מתי נוצר, מחק אם חשוד |
| NOPASSWD ב-sudoers | root ללא סיסמה | הסר הרשאה מיותרת |
| `id_rsa` בהרשאות 644 | מפתח פרטי חשוף | `chmod 600 ~/.ssh/id_rsa` |
| credentials בהיסטוריה | חשיפת סיסמאות | שנה סיסמאות, `history -c` |
| SUID ב-`/tmp` | backdoor מותקן | בדוק מיד + הסר |
| סקריפט cron writable | privilege escalation | `chmod 644 script.sh` |
| Brute Force בלוג | מתקפה פעילה | חסום IP: `ufw deny from IP` |

---

> **זכור:** המעבדה הזו מיועדת לסביבת תרגול בלבד.  
> חיפוש קבצים רגישים על מערכות ללא אישור = עבירה פלילית.

---

*LINOX LAB — Sensitive Files | Cyber Course | מעבדת חיפוש קבצים רגישים*
