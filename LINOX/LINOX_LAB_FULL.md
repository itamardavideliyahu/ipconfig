# מעבדת לינוקס מקיפה
### כל הנושאים | רמת מתחילים | ~3 שעות

> **הוראות:** עבוד לפי הסדר. קרא את ההסבר לפני כל פקודה.  
> **סימן:** `$` = פקודה רגילה | `#` = פקודה שדורשת הרשאות root

---

# חלק א' — יסודות

---

## 1. מבנה מערכת ההפעלה LINUX

**מה זה?**  
לינוקס בנויה בשכבות — החומרה בתחתית, ה-Kernel מנהל אותה, ועליו רצות התוכנות שלנו.

```
תוכנות משתמש (Firefox, Terminal, Python)
        ↓
    Shell (bash)
        ↓
   Kernel (ליב הלינוקס)
        ↓
      חומרה (CPU, RAM, דיסק)
```

**מבנה ספריות ראשי:**
```bash
ls /
```
```
bin  boot  dev  etc  home  lib  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```

| ספרייה | תפקיד |
|--------|-------|
| `/bin` | פקודות בסיסיות (ls, cp, mv) |
| `/etc` | קבצי הגדרות המערכת |
| `/home` | ספריות בית של משתמשים |
| `/var` | לוגים וקבצים משתנים |
| `/tmp` | קבצים זמניים |
| `/proc` | מידע על תהליכים פעילים |

```bash
uname -a
```
```
Linux kali 6.6.9-amd64 #1 SMP x86_64 GNU/Linux
```
```bash
cat /etc/os-release
```

**משימות:**
- [ ] הרץ `ls /` — זהה 5 ספריות ורשום את תפקידן
- [ ] הרץ `uname -a` — מה גרסת ה-Kernel שלך?
- [ ] הרץ `cat /etc/os-release` — מה שם ההפצה?

---

## 2. ה-SHELL

**מה זה?**  
ה-Shell הוא הממשק שמקבל פקודות ממך ומעביר אותן ל-Kernel. הנפוץ ביותר: **bash**.

```bash
echo $SHELL
```
```
/bin/bash
```
```bash
echo $USER
```
```
student
```
```bash
env | head -10
```
```
USER=student
HOME=/home/student
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

**משימות:**
- [ ] הרץ `echo $SHELL` — איזה Shell אתה משתמש?
- [ ] הרץ `echo $HOME` — מה הנתיב לספריית הבית שלך?
- [ ] הרץ `env` — מצא 3 משתני סביבה ורשום מה הם עושים

---

## 3. תפריט העזרה הבסיסי

**מה זה?**  
לכל פקודה בלינוקס יש תיעוד מובנה — ניתן לקרוא אותו ישירות מהטרמינל.

```bash
man ls
```
> ניווט: חצים | `q` לצאת | `/מילה` לחפש

```bash
ls --help
```
```
Usage: ls [OPTION]... [FILE]...
  -a  do not ignore entries starting with .
  -l  use a long listing format
  -h  human-readable sizes
```
```bash
whatis cp
```
```
cp (1) - copy files and directories
```
```bash
apropos copy | head -5
```
```
cp (1)    - copy files and directories
rsync (1) - a fast, versatile file-copying tool
```

**משימות:**
- [ ] הרץ `man ls` — מצא 3 דגלים שלא הכרת, לחץ `q` לצאת
- [ ] הרץ `whatis mv` ו-`whatis rm` — מה כל אחד עושה?
- [ ] הרץ `apropos search | head -5` — מה נמצא?

---

## 4. דפי עזרה מתקדמים — Man

**מה זה?**  
ה-man pages מחולקות לפרקים. הכרת המבנה עוזרת למצוא מידע מהר.

```bash
man 1 ls
```
> חלק 1 = פקודות משתמש

```bash
man -k password | head -8
```
```
chpasswd (8) - update passwords in batch mode
passwd (1)   - change user password
passwd (5)   - password file
```

```bash
man -f passwd
```
```
passwd (1) - change user password
passwd (5) - password file
```

> `man -k` = חיפוש בכל ה-man pages | `man -f` = הצג כל הגרסאות

**משימות:**
- [ ] הרץ `man -k network | head -8` — מה נמצא?
- [ ] הרץ `man -f ls` — כמה גרסאות יש?
- [ ] הרץ `man 5 passwd` — מה ההבדל מ-`man 1 passwd`?

---

## 5. ניווט בסיסי

**מה זה?**  
שלוש פקודות הניווט הבסיסיות: `pwd`, `ls`, `cd`.

```bash
pwd
```
```
/home/student
```
```bash
ls -la
```
```
drwxr-xr-x  2 student student 4096 Jul 26 .
drwxr-xr-x  3 root    root    4096 Jul 26 ..
-rw-r--r--  1 student student  220 Jul 26 .bash_logout
-rw-r--r--  1 student student 3526 Jul 26 .bashrc
```
```bash
cd /var/log
pwd
ls
```
```
/var/log
auth.log  dpkg.log  syslog  kern.log
```
```bash
cd ~        # חזור לבית
cd ..       # עלה ספרייה אחת
cd -        # חזור לספרייה הקודמת
```

**משימות:**
- [ ] הרץ `pwd` — רשום את הנתיב הנוכחי
- [ ] נווט ל-`/var/log`, הרץ `ls`, וחזור ל-home עם `cd ~`
- [ ] השתמש ב-`cd -` — לאן חזרת?
- [ ] הרץ `ls -lh /usr/bin | head -10` — מה הדגל `-h` עושה?

---

# חלק ב' — ניהול קבצים

---

## 6. יצירת קובץ טקסט

**מה זה?**  
שלוש דרכים עיקריות ליצור קבצים: `touch`, `echo >`, `cat >`.

```bash
mkdir ~/lab && cd ~/lab
touch myfile.txt
ls -la myfile.txt
```
```
-rw-r--r-- 1 student student 0 Jul 26 myfile.txt
```
```bash
echo "Hello Linux" > myfile.txt
echo "Second line" >> myfile.txt
cat myfile.txt
```
```
Hello Linux
Second line
```
> `>` = החלפה | `>>` = הוספה לסוף

**משימות:**
- [ ] צור `~/lab` וכנס אליה
- [ ] צור `myfile.txt` עם `touch` — מה גודלו?
- [ ] כתוב 2 שורות עם `>` ו-`>>` — הצג עם `cat`

---

## 7. צפייה ועריכת קובץ טקסט

**מה זה?**  
פקודות לקריאה ועריכה של קבצים מהטרמינל.

```bash
cat myfile.txt
```
```bash
cat -n myfile.txt
```
```
     1  Hello Linux
     2  Second line
```
```bash
head -1 myfile.txt
tail -1 myfile.txt
```
```bash
nano myfile.txt
```
> nano: `Ctrl+O` לשמור | `Ctrl+X` לצאת

**משימות:**
- [ ] הרץ `cat -n myfile.txt` — מה `-n` מוסיף?
- [ ] הרץ `head -1` ו-`tail -1` — מה ההבדל?
- [ ] פתח `nano myfile.txt`, הוסף שורה, שמור וצא

---

## 8. העתקת קובץ

**מה זה?**  
`cp` מעתיקה קבצים — המקור נשאר, יוצר עותק ביעד.

```bash
cp myfile.txt myfile_backup.txt
ls
```
```
myfile.txt  myfile_backup.txt
```
```bash
mkdir backups
cp myfile.txt backups/
ls backups/
```
```
myfile.txt
```
```bash
cp -p myfile.txt preserved.txt    # שמור timestamps
cp -i myfile.txt myfile_backup.txt # שאל לפני החלפה
```

**משימות:**
- [ ] העתק `myfile.txt` → `myfile_backup.txt` — ודא שניהם קיימים
- [ ] צור `backups/` והעתק אליה את הקובץ
- [ ] נסה `cp -i` כשהיעד קיים — מה קורה?

---

## 9. העברת קובץ

**מה זה?**  
`mv` מעבירה קבצים — **המקור נמחק** לאחר ההעברה.

```bash
mv myfile_backup.txt backups/
ls
ls backups/
```
```
myfile.txt  preserved.txt  backups/
backups/: myfile.txt  myfile_backup.txt
```
```bash
mv backups/myfile_backup.txt .
```
> `.` = הספרייה הנוכחית

**משימות:**
- [ ] העבר `myfile_backup.txt` ל-`backups/` — ודא שנעלם ממקומו
- [ ] החזר אותו בחזרה עם `mv backups/myfile_backup.txt .`

---

## 10. שינוי שם קובץ

**מה זה?**  
`mv` משמשת גם לשינוי שם — אותה פקודה, אותה ספרייה, שם אחר.

```bash
mv myfile.txt renamed_file.txt
ls
```
```
renamed_file.txt  myfile_backup.txt  preserved.txt  backups/
```

**משימות:**
- [ ] שנה שם `myfile_backup.txt` → `old_backup.txt`
- [ ] ודא עם `ls`

---

## 11. הסתרת קובץ

**מה זה?**  
בלינוקס, קובץ שמתחיל ב-`.` הוא **מוסתר** — לא מוצג ב-`ls` רגיל.

```bash
mv renamed_file.txt .hidden_file.txt
ls
```
```
old_backup.txt  preserved.txt  backups/
```
```bash
ls -a
```
```
.  ..  .hidden_file.txt  old_backup.txt  preserved.txt  backups/
```

**משימות:**
- [ ] הסתר קובץ עם `mv` — ודא שלא מוצג ב-`ls`
- [ ] הרץ `ls -a` — ראה אותו

---

## 12. מחיקת קובץ

**מה זה?**  
`rm` מוחקת קבצים — **אין סל מחזור**, המחיקה סופית!

```bash
rm .hidden_file.txt
ls -a
```
```bash
rm -i old_backup.txt
```
```
rm: remove regular file 'old_backup.txt'? y
```
> `-i` = שאל לפני מחיקה — **מומלץ למתחילים**

**משימות:**
- [ ] מחק `.hidden_file.txt` — ודא עם `ls -a`
- [ ] מחק `old_backup.txt` עם `-i` — אשר עם `y`

---

## 13. ניתוח קבצים

**מה זה?**  
פקודות לניתוח תוכן וסוג קובץ.

```bash
file preserved.txt
```
```
preserved.txt: ASCII text
```
```bash
file /bin/bash
```
```
/bin/bash: ELF 64-bit LSB pie executable, x86-64
```
```bash
wc preserved.txt
```
```
 2  4 24 preserved.txt
 ↑  ↑  ↑
 שורות מילים בתים
```
```bash
stat preserved.txt
```
```
  File: preserved.txt
  Size: 24          Inode: 123456
Access: (0644/-rw-r--r--)
Modify: 2026-07-26 18:00:00
```
```bash
du -sh ~/lab
```
```
12K  /home/student/lab
```

**משימות:**
- [ ] הרץ `file` על קובץ טקסט ועל `/bin/ls` — מה ההבדל?
- [ ] הרץ `wc preserved.txt` — הסבר כל מספר
- [ ] הרץ `stat preserved.txt` — שים לב ל-inode וזמנים

---

# חלק ג' — ניהול תיקיות

---

## 14. יצירת תיקייה

**מה זה?**  
`mkdir` יוצרת תיקיות. `-p` יוצר תיקיות ביניים אוטומטית.

```bash
mkdir project
mkdir -p project/src/utils
ls project/
```
```
src/
```
```bash
ls project/src/
```
```
utils/
```

**משימות:**
- [ ] צור `~/lab/project` עם תת-תקיות `src` ו-`docs` בפקודה אחת
- [ ] ודא עם `ls -la ~/lab/project/`

---

## 15. צפייה בתוכן תיקייה

**מה זה?**  
`ls` עם דגלים שונים מציגה מידע מפורט על תוכן תיקייה.

```bash
ls -la ~/lab/
```
```
drwxr-xr-x 4 student student 4096 Jul 26 .
drwxr-xr-x 8 student student 4096 Jul 26 ..
drwxr-xr-x 3 student student 4096 Jul 26 backups
-rw-r--r-- 1 student student   24 Jul 26 preserved.txt
drwxr-xr-x 4 student student 4096 Jul 26 project
```
```bash
ls -lh ~/lab/    # גדלים קריאים לאדם
ls -R ~/lab/     # רקורסיבי — הצג גם תת-תיקיות
```

**משימות:**
- [ ] הרץ `ls -la ~/lab/` — הסבר כל עמודה
- [ ] הרץ `ls -R ~/lab/` — מה מוצג?

---

## 16. העתקת תיקייה

**מה זה?**  
להעתיק תיקייה שלמה חייבים להשתמש ב-`cp -r`.

```bash
cp -r backups/ backups_copy/
ls
```
```
backups  backups_copy  preserved.txt  project
```

**משימות:**
- [ ] העתק `backups/` → `backups_copy/` עם `cp -r`
- [ ] נסה ללא `-r` — מה הודעת השגיאה?

---

## 17. העברת תיקייה

**מה זה?**  
`mv` עובדת אותו דבר עם תיקיות — לא צריך `-r`.

```bash
mv backups_copy/ project/
ls project/
```
```
backups_copy  docs  src
```

**משימות:**
- [ ] העבר `backups_copy/` לתוך `project/` — ודא עם `ls`

---

## 18. שינוי שם תיקייה

```bash
mv project/backups_copy project/archive
ls project/
```
```
archive  docs  src
```

**משימות:**
- [ ] שנה שם `project/docs` → `project/documentation`

---

## 19. הסתרת תיקייה

**מה זה?**  
בדיוק כמו קובץ — נקודה בהתחלה של השם.

```bash
mv project/archive project/.hidden_archive
ls project/
ls -a project/
```

**משימות:**
- [ ] הסתר תיקייה — ודא עם `ls` ואז `ls -a`

---

## 20. מחיקת תיקייה

**מה זה?**  
`rmdir` מוחקת תיקייה **ריקה** בלבד. `rm -r` מוחקת תיקייה עם כל תוכנה.

```bash
rmdir project/src/utils
```
```bash
rm -r project/
```
> **אזהרה:** `rm -r` מוחק הכל ללא אפשרות שחזור!

```bash
rm -ri backups/
```
```
rm: descend into directory 'backups/'? y
rm: remove 'backups/myfile.txt'? y
rm: remove directory 'backups/'? y
```

**משימות:**
- [ ] מחק תיקייה ריקה עם `rmdir`
- [ ] מחק תיקייה עם תוכן עם `rm -ri` — אשר כל פריט

---

# חלק ד' — חיפוש קבצים ותוכנות

---

## 21. מבוא לחיפוש

**מה זה?**  
שלוש פקודות עיקריות לחיפוש:

| פקודה | מהירות | מציאת קבצים חדשים |
|-------|--------|-------------------|
| `find` | איטי | כן — סורק בזמן אמת |
| `locate` | מהיר | רק אחרי `updatedb` |
| `whereis` | מיידי | כן — לתוכנות בלבד |

```bash
which ls
```
```
/usr/bin/ls
```
```bash
type cd
```
```
cd is a shell builtin
```

**משימות:**
- [ ] הרץ `which python3` — איפה מותקן Python?
- [ ] הרץ `type ls` — מה סוג הפקודה?

---

## 22. הפקודה find

**מה זה?**  
`find` סורקת ספריות בזמן אמת ומחפשת לפי תנאים שונים.

```bash
find ~/lab -name "*.txt"
```
```
/home/student/lab/preserved.txt
```
```bash
find ~/lab -type d
```
```
/home/student/lab
/home/student/lab/project
```
```bash
find /etc -name "*.conf" -type f 2>/dev/null | head -5
```
```
/etc/resolv.conf
/etc/host.conf
/etc/pam.conf
```
```bash
find / -size +10M -type f 2>/dev/null | head -5
```

**משימות:**
- [ ] הרץ `find ~/lab -name "*.txt"` — כמה קבצים נמצאו?
- [ ] מצא תיקיות בלבד ב-`~/lab` עם `-type d`
- [ ] מצא קבצים גדולים מ-5MB: `find /usr -size +5M 2>/dev/null | head -5`

---

## 23. הפקודה locate

**מה זה?**  
`locate` מחפשת במסד נתונים מוכן — מהירה מאוד.

```bash
sudo updatedb
locate preserved.txt
```
```
/home/student/lab/preserved.txt
```
```bash
locate -i readme | head -5
```
> `-i` = לא רגיש לאותיות גדולות/קטנות

```bash
locate -c bash
```
```
47
```
> `-c` = הצג רק ספירת תוצאות

**משימות:**
- [ ] הרץ `sudo updatedb` ואז `locate preserved.txt`
- [ ] הרץ `locate -c python` — כמה תוצאות?

---

## 24. הפקודה whereis

**מה זה?**  
`whereis` מחפשת **תוכנות** — מציאת הבינארי, קבצי הגדרות ודפי man.

```bash
whereis bash
```
```
bash: /usr/bin/bash /etc/bash.bashrc /usr/share/man/man1/bash.1.gz
       ↑ בינארי      ↑ הגדרות          ↑ דף man
```
```bash
whereis python3
```
```
python3: /usr/bin/python3 /usr/lib/python3 /usr/share/man/man1/python3.1.gz
```
```bash
whereis ls
whereis nginx
```

**משימות:**
- [ ] הרץ `whereis ssh` — מה כל שדה אומר?
- [ ] הרץ `whereis python3` — מה מיקום הבינארי?
- [ ] הרץ `whereis nano` — האם יש דף man?

---

## 25. אפשרויות מתקדמות לסינון מידע

**מה זה?**  
`grep`, `cut`, `sort`, `uniq`, `wc` ו-Pipes (`|`) — כלים לסינון ועיבוד פלט.

**grep — חיפוש טקסט:**
```bash
grep "root" /etc/passwd
```
```
root:x:0:0:root:/root:/bin/bash
```
```bash
grep -i "linux" /etc/os-release
```
> `-i` = לא רגיש לרישיות

```bash
grep -v "nologin" /etc/passwd
```
> `-v` = הצג שורות **שלא** מכילות את הדפוס

```bash
grep -c "bin" /etc/passwd
```
```
4
```
> `-c` = ספור התאמות

**Pipe — חיבור פקודות:**
```bash
cat /etc/passwd | grep "bash"
```
```bash
ps aux | grep "ssh"
```

**sort ו-uniq:**
```bash
cat /etc/passwd | cut -d: -f1 | sort
```
```
daemon
messagebus
nobody
root
student
```
```bash
cat /etc/passwd | cut -d: -f7 | sort | uniq -c | sort -rn
```
```
  30 /usr/sbin/nologin
   2 /bin/bash
   1 /bin/sh
```
> `cut -d: -f7` = חתוך בפסיק `:` וקח שדה 7 | `uniq -c` = ספור כפולות

**head ו-tail:**
```bash
cat /etc/passwd | head -5
cat /etc/passwd | tail -5
```

**wc:**
```bash
cat /etc/passwd | wc -l
```
```
32
```

**משימות:**
- [ ] הרץ `grep "student" /etc/passwd` — מצא את שורת המשתמש שלך
- [ ] הרץ `ps aux | grep bash` — כמה תהליכי bash רצים?
- [ ] הרץ `cat /etc/passwd | cut -d: -f1 | sort` — הצג משתמשים ממוינים
- [ ] הרץ `ls /bin | wc -l` — כמה פקודות יש ב-/bin?

---

# חלק ה' — ניהול הרשאות

---

## 26. מבוא להרשאות

**מה זה?**  
כל קובץ ותיקייה בלינוקס יש לו 3 קבוצות הרשאות:

```
-  rw-  r--  r--
│   │    │    └── Other  (כולם)
│   │    └─────── Group  (קבוצה)
│   └──────────── User   (בעלים)
└──────────────── סוג: d=תיקייה, -=קובץ, l=קישור
```

| אות | מספר | קובץ | תיקייה |
|-----|------|------|--------|
| `r` | 4 | קריאה | הצגת תוכן |
| `w` | 2 | כתיבה | יצירה/מחיקה |
| `x` | 1 | הרצה | כניסה |

**משימות:**
- [ ] הרץ `ls -la ~/lab/` — מה ההרשאות של `preserved.txt`?
- [ ] מה משמעות `drwxr-xr-x`?

---

## 27. צפייה וניתוח הרשאות קיימות

```bash
ls -la ~/lab/
```
```
-rw-r--r-- 1 student student 24 Jul 26 preserved.txt
drwxr-xr-x 2 student student 4096 Jul 26 project/
```

**קריאת הרשאות ספציפיות:**
```bash
stat preserved.txt
```
```
Access: (0644/-rw-r--r--)  Uid: (1000/student)  Gid: (1000/student)
```
```bash
ls -la /etc/passwd /etc/shadow
```
```
-rw-r--r-- 1 root root   1823 Jul 26 /etc/passwd   ← קריא לכולם
-rw-r----- 1 root shadow  952 Jul 26 /etc/shadow    ← קריא רק ל-root וקבוצת shadow
```

**הרשאות מיוחדות — SUID:**
```bash
ls -la /usr/bin/passwd
```
```
-rwsr-xr-x 1 root root 68208 Jul 26 /usr/bin/passwd
     ↑
     s = SUID — רץ עם הרשאות הבעלים (root)
```

**משימות:**
- [ ] הרץ `ls -la /etc/` — מצא קובץ עם הרשאות `644` ואחד עם `600`
- [ ] הרץ `stat ~/lab/preserved.txt` — מה ה-Octal של ההרשאות?
- [ ] הרץ `find /usr/bin -perm -4000 2>/dev/null` — מצא קבצי SUID

---

## 28. שינוי הרשאות קיימות

**chmod — שינוי הרשאות:**

```bash
# שיטה מספרית
chmod 644 preserved.txt    # rw-r--r--
chmod 600 preserved.txt    # rw------- (פרטי)
chmod 755 preserved.txt    # rwxr-xr-x

# שיטה סימבולית
chmod u+x preserved.txt    # הוסף הרצה לבעלים
chmod o-r preserved.txt    # הסר קריאה מ-Other
chmod a+r preserved.txt    # הוסף קריאה לכולם
```

**דוגמה מלאה:**
```bash
ls -la preserved.txt
```
```
-rw-r--r-- 1 student student 24 Jul 26 preserved.txt
```
```bash
chmod 444 preserved.txt
ls -la preserved.txt
```
```
-r--r--r-- 1 student student 24 Jul 26 preserved.txt
```
```bash
echo "test" >> preserved.txt
```
```
bash: preserved.txt: Permission denied
```
```bash
chmod 644 preserved.txt   # החזר
```

**chown — שינוי בעלים (דורש sudo):**
```bash
sudo chown root preserved.txt
ls -la preserved.txt
```
```
-rw-r--r-- 1 root student 24 Jul 26 preserved.txt
```
```bash
sudo chown student preserved.txt   # החזר
```

**משימות:**
- [ ] שנה `preserved.txt` ל-`444` — נסה לכתוב אליו, מה קורה?
- [ ] החזר ל-`644` ונסה שוב לכתוב
- [ ] הוסף הרשאת הרצה לבעלים עם `chmod u+x`
- [ ] הרץ `ls -la` — האם רואים `x`?

---

# חלק ו' — תהליכים

---

## 29. מבוא לתהליכים

**מה זה?**  
כל דבר שרץ על המחשב הוא **תהליך (Process)** עם מספר ייחודי — **PID**.

```
PID 1 = systemd (הראשון תמיד)
כל שאר התהליכים = ילדים של systemd
```

```bash
echo $$
```
```
1203
```
> `$$` = ה-PID של ה-Shell הנוכחי

**משימות:**
- [ ] הרץ `echo $$` — מה ה-PID של ה-Shell שלך?

---

## 30. צפייה בתהליכים קיימים

```bash
ps aux
```
```
USER       PID %CPU %MEM  COMMAND
root         1  0.0  0.1  /sbin/init
root       423  0.0  0.2  /usr/sbin/sshd
student   1203  0.0  0.1  bash
student   1250  0.0  0.0  ps aux
```
```bash
ps aux | grep bash
ps -ef --forest | head -20
```
```
root     1     0  /sbin/init
root   423     1   \_ /usr/sbin/sshd
student 1203  423       \_ bash
student 1250 1203           \_ ps -ef
```

**משימות:**
- [ ] הרץ `ps aux | grep root` — כמה תהליכים רצים כ-root?
- [ ] הרץ `ps -ef --forest | head -25` — מי הפעיל את ה-bash שלך?

---

## 31. צפייה בתהליכים דינאמיים

**מה זה?**  
`top` ו-`htop` מציגים תהליכים **בזמן אמת** עם עדכון שוטף.

```bash
top
```
```
Tasks: 112 total, 1 running, 111 sleeping
%Cpu(s):  2.1 us,  0.5 sy
MiB Mem:   3924.0 total,   2100.0 free

  PID USER    %CPU %MEM  COMMAND
  891 www-data  1.2  0.8  apache2
 1203 student   0.0  0.1  bash
```
> `q` לצאת | `k` להרוג תהליך | `M` מיין לפי זיכרון | `P` מיין לפי CPU

```bash
htop
```
> `htop` = גרסה ידידותית יותר עם צבעים

**משימות:**
- [ ] הרץ `top` — מצא את התהליך שצורך הכי הרבה CPU
- [ ] לחץ `M` ב-top — מה השתנה?
- [ ] לחץ `q` לצאת

---

## 32. הגבלת משאבים

**מה זה?**  
`nice` ו-`renice` משנים **עדיפות** של תהליך (Priority).  
ערך nice: מ-**-20** (עדיפות גבוהה) עד **+19** (עדיפות נמוכה).

```bash
nice -n 10 sleep 1000 &
```
```
[1] 1456
```
```bash
ps aux | grep sleep
```
```
student  1456  0.0  0.0  sleep 1000
```
```bash
renice +15 1456
```
```
1456 (process ID) old priority 10, new priority 15
```
> תהליכים עם nice גבוה = פחות עדיפות = "נחמדים" לאחרים

**משימות:**
- [ ] הפעל `nice -n 5 sleep 2000 &` — רשום ה-PID
- [ ] הרץ `ps aux | grep sleep` — ראה את התהליך
- [ ] הרץ `renice +15 <PID>` — שנה עדיפות

---

## 33. סגירת תהליך

**מה זה?**  
`kill` שולח **signal** לתהליך לסגור. שני signals עיקריים:

```
kill PID      = SIGTERM (15) — בקשה נעימה
kill -9 PID   = SIGKILL     — כיבוי כוחני מיידי
```

```bash
sleep 1000 &
```
```
[1] 1500
```
```bash
kill 1500
ps aux | grep sleep
```
```
[1]+  Terminated  sleep 1000
```
```bash
sleep 2000 &
kill -9 $!    # $! = PID של התהליך האחרון ברקע
```
```
[1]+  Killed  sleep 2000
```

**משימות:**
- [ ] הפעל `sleep 500 &` — שמור PID
- [ ] רוג עם `kill <PID>` — ודא עם `ps aux | grep sleep`
- [ ] הפעל `sleep 999 &` ורוג עם `kill -9`
- [ ] מה ההבדל בין `Terminated` ל-`Killed`?

---

# חלק ז' — שירותי מערכת

---

## 34. מבוא לשירותים

**מה זה?**  
שירות (Service) = תוכנה שרצה ברקע כל הזמן — שרת SSH, שרת HTTP, מסד נתונים.  
**systemd** מנהל את כל השירותים בלינוקס מודרני.

```
שירות:   sshd       ← מאזין לחיבורי SSH
שירות:   apache2    ← מגיש דפי ווב
שירות:   cron       ← מריץ משימות מתוזמנות
```

**משימות:**
- [ ] מה ההבדל בין תהליך לשירות?

---

## 35. צפייה וניתוח שירותים

```bash
systemctl status ssh
```
```
● ssh.service - OpenBSD Secure Shell server
   Loaded: loaded (/lib/systemd/system/ssh.service; enabled)
   Active: active (running) since Jul 26 18:00:00
 Main PID: 1234 (sshd)
```
```bash
systemctl list-units --type=service | head -15
```
```
UNIT                    LOAD   ACTIVE SUB     DESCRIPTION
cron.service            loaded active running Regular background jobs
networking.service      loaded active exited  Raise network interfaces
ssh.service             loaded active running OpenBSD Secure Shell server
```
```bash
systemctl list-units --state=failed
```

**משימות:**
- [ ] הרץ `systemctl status ssh` — מה מצב השירות?
- [ ] הרץ `systemctl list-units --type=service | head -15`
- [ ] הרץ `systemctl list-units --state=failed` — יש שגיאות?

---

## 36. הפעלה וכיבוי שירותים

```bash
sudo systemctl stop ssh
systemctl status ssh
```
```
Active: inactive (dead)
```
```bash
sudo systemctl start ssh
systemctl status ssh
```
```
Active: active (running)
```
```bash
sudo systemctl restart ssh     # עצור והפעל מחדש
sudo systemctl reload ssh      # רענן הגדרות בלבד (ללא הפסקה)
sudo systemctl enable ssh      # הפעל אוטומטית באתחול
sudo systemctl disable ssh     # בטל הפעלה אוטומטית
```
```bash
systemctl is-active ssh
systemctl is-enabled ssh
```

**משימות:**
- [ ] הרץ `sudo systemctl stop ssh` — ודא שכבה
- [ ] הפעל שוב עם `sudo systemctl start ssh`
- [ ] הרץ `systemctl is-enabled ssh` — האם מופעל באתחול?

---

## 37. שירות ה-SSH

**מה זה?**  
SSH = Secure Shell — חיבור מאובטח למחשב מרחוק מהטרמינל.

```bash
systemctl status ssh
```
```bash
sudo cat /etc/ssh/sshd_config | grep -v "^#" | grep -v "^$"
```
```
Include /etc/ssh/sshd_config.d/*.conf
KbdInteractiveAuthentication no
UsePAM yes
PrintMotd no
AcceptEnv LANG LC_*
Subsystem sftp /usr/lib/openssh/sftp-server
```
```bash
ss -tlnp | grep ssh
```
```
LISTEN 0  128  0.0.0.0:22   0.0.0.0:*  users:(("sshd",pid=1234))
```
> SSH מאזין על **פורט 22**

**חיבור SSH:**
```bash
ssh username@ip_address
ssh student@192.168.1.50
```

**משימות:**
- [ ] הרץ `ss -tlnp | grep ssh` — על איזה פורט מאזין SSH?
- [ ] הרץ `sudo cat /etc/ssh/sshd_config | grep Port` — מה הפורט?

---

## 38. שירות ה-HTTP (Apache)

**מה זה?**  
Apache = שרת ווב שמגיש דפי HTML לדפדפן.

```bash
sudo apt install apache2 -y
sudo systemctl start apache2
systemctl status apache2
```
```
Active: active (running)
```
```bash
ss -tlnp | grep apache
```
```
LISTEN 0  511  *:80  *:*  users:(("apache2"))
```
> Apache מאזין על **פורט 80** (HTTP)

```bash
curl http://localhost
```
```html
<!DOCTYPE html><html>...Apache Default Page...</html>
```

**קבצי ה-site:**
```bash
ls /var/www/html/
```
```
index.html
```
```bash
echo "<h1>My Kali Server</h1>" | sudo tee /var/www/html/index.html
curl http://localhost
```
```
<h1>My Kali Server</h1>
```

**משימות:**
- [ ] התקן Apache עם `apt install apache2 -y`
- [ ] הפעל ובדוק סטאטוס
- [ ] הרץ `curl http://localhost` — מה מוצג?
- [ ] שנה את `index.html` ובדוק שוב עם `curl`

---

# חלק ח' — לוגים

---

## 39. מבוא ללוגים

**מה זה?**  
לוגים = יומן אירועים של המערכת. כל פעולה חשובה נרשמת.

**לוגים עיקריים בקאלי:**
```bash
ls /var/log/
```
```
auth.log  dpkg.log  kern.log  messages  syslog
```

| קובץ | תוכן |
|------|------|
| `syslog` | לוג כללי של המערכת |
| `auth.log` | כניסות, sudo, SSH |
| `kern.log` | הודעות ה-Kernel |
| `dpkg.log` | התקנות ועדכונים |

**משימות:**
- [ ] הרץ `ls /var/log/` — אילו לוגים קיימים?

---

## 40. קובץ ה-syslog

```bash
sudo tail -20 /var/log/syslog
```
```
Jul 26 18:00:01 kali CRON[2001]: (root) CMD (command -v debian-sa1)
Jul 26 18:00:05 kali systemd[1]: NetworkManager.service: Succeeded.
Jul 26 18:01:00 kali kernel: NET: Registered PF_INET6 protocol family
```
```bash
sudo grep "error" /var/log/syslog | tail -5
```
```bash
sudo journalctl --since today | tail -20
```

**משימות:**
- [ ] הרץ `sudo tail -20 /var/log/syslog` — מה קרה לאחרונה?
- [ ] הרץ `sudo grep "error" /var/log/syslog | tail -5`

---

## 41. קובץ ה-auth.log

**מה זה?**  
`auth.log` = לוג אבטחה — כל כניסה, כישלון, sudo ו-SSH.

```bash
sudo tail -20 /var/log/auth.log
```
```
Jul 26 18:10:01 kali sshd[1234]: Accepted password for student from 192.168.1.10
Jul 26 18:15:33 kali sshd[1235]: Failed password for root from 185.220.101.1
Jul 26 18:16:00 kali sudo[1456]: student : COMMAND=/usr/bin/apt
```
```bash
sudo grep "Failed password" /var/log/auth.log | tail -5
```
```
Jul 26 18:15:33 kali sshd: Failed password for root from 185.220.101.1 port 4455
```
```bash
# ספור ניסיונות כושלים לפי IP
sudo grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn | head -5
```
```
  47  185.220.101.1    ← IP תקפה 47 פעמים!
   3  192.168.1.99
```

**משימות:**
- [ ] הרץ `sudo tail -20 /var/log/auth.log` — מצא כניסות מוצלחות וכושלות
- [ ] הרץ `sudo grep "Failed password" /var/log/auth.log | tail -5`

---

# חלק ט' — משתמשים וקבוצות

---

## 42. מבוא למשתמשים

**מה זה?**  
לינוקס היא מערכת **רב-משתמשים** — כמה משתמשים יכולים לעבוד בו-זמנית.  
לכל משתמש יש: שם, סיסמה, UID, ספריית בית ו-Shell.

```bash
cat /etc/passwd | head -5
```
```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
student:x:1000:1000:Student:/home/student:/bin/bash
```

**משימות:**
- [ ] הרץ `cat /etc/passwd` — זהה את שורת המשתמש שלך
- [ ] מה ה-UID שלך?

---

## 43. קונספט ה-Multiuser

```bash
# כמה משתמשים מחוברים עכשיו
who
```
```
student  pts/0  2026-07-26 18:00 (:0)
```
```bash
w
```
```
USER     TTY   FROM   LOGIN@  IDLE  WHAT
student  pts/0  :0    18:00   0.00s  w
```
```bash
last | head -10
```
```
student  pts/0  :0  Sat Jul 26 18:00  still logged in
root     pts/0  :0  Fri Jul 25 10:00 - 12:00 (02:00)
```

**משימות:**
- [ ] הרץ `who` — מי מחובר?
- [ ] הרץ `last | head -10` — מי נכנס לאחרונה?

---

## 44. החשבון Superuser

**מה זה?**  
`root` = המשתמש הכי חזק במערכת — הרשאות על הכל.  
`sudo` = הרץ פקודה אחת עם הרשאות root (בלי להיות root).

```bash
whoami
```
```
student
```
```bash
sudo whoami
```
```
root
```
```bash
sudo -i    # כנס למצב root (shell שלם)
whoami
```
```
root
```
```bash
exit       # חזור למשתמש רגיל
```

```bash
# מי מורשה להשתמש ב-sudo?
sudo cat /etc/sudoers | grep -v "^#" | grep -v "^$"
```

**משימות:**
- [ ] הרץ `whoami` ואז `sudo whoami` — מה ההבדל?
- [ ] כנס ל-`sudo -i` ויצא עם `exit`
- [ ] מה הסכנה בעבודה תמידית כ-root?

---

## 45. תקיית הבית

**מה זה?**  
לכל משתמש יש תקיית בית אישית ב-`/home/username`.

```bash
echo $HOME
```
```
/home/student
```
```bash
ls -la ~/
```
```
-rw-r--r--  .bash_history    ← היסטוריית פקודות
-rw-r--r--  .bashrc          ← הגדרות Shell
-rw-r--r--  .profile         ← הגדרות כניסה
drwxr-xr-x  lab/
```

**משימות:**
- [ ] הרץ `ls -la ~/` — אילו קבצים מוסתרים יש בבית?
- [ ] הרץ `cat ~/.bashrc | head -10` — מה יש שם?

---

## 46. צפייה במשתמשים קיימים

```bash
cat /etc/passwd | grep -v "nologin\|false"
```
```
root:x:0:0:root:/root:/bin/bash
student:x:1000:1000:Student:/home/student:/bin/bash
```
```bash
# רשימה נקייה של שמות
cut -d: -f1 /etc/passwd | sort
```
```bash
# מצא משתמשים עם UID גבוה (משתמשים אמיתיים)
awk -F: '$3 >= 1000' /etc/passwd
```

**משימות:**
- [ ] הרץ `cut -d: -f1 /etc/passwd | sort` — כמה משתמשים יש?
- [ ] הרץ `awk -F: '$3 == 0' /etc/passwd` — מי עם UID 0?

---

## 47. יצירת משתמש חדש

```bash
sudo adduser testuser
```
```
Adding user 'testuser'...
New password: ****
Retype password: ****
Full Name []: Test User
```
```bash
# ודא שנוצר
grep "testuser" /etc/passwd
```
```
testuser:x:1001:1001:Test User:/home/testuser:/bin/bash
```
```bash
ls /home/
```
```
student  testuser
```

**משימות:**
- [ ] הרץ `sudo adduser testuser` — צור משתמש חדש
- [ ] ודא שנוצר עם `grep testuser /etc/passwd`
- [ ] הרץ `ls /home/` — יש תקיית בית חדשה?

---

## 48. שינוי סיסמה למשתמש

```bash
# שנה סיסמה למשתמש הנוכחי
passwd
```
```
Current password:
New password:
Retype new password:
passwd: password updated successfully
```
```bash
# שנה סיסמה למשתמש אחר (דורש sudo)
sudo passwd testuser
```
```
New password:
Retype new password:
passwd: password updated successfully
```

**משימות:**
- [ ] הרץ `sudo passwd testuser` — שנה סיסמה ל-testuser

---

## 49. מחיקת משתמש

```bash
sudo deluser testuser
```
```
Removing user 'testuser'...
Done.
```
```bash
# מחק גם את תקיית הבית
sudo deluser --remove-home testuser
```
```bash
grep "testuser" /etc/passwd
```
```
(אין תוצאה — נמחק)
```

**משימות:**
- [ ] מחק `testuser` עם `sudo deluser testuser`
- [ ] ודא שנמחק עם `grep testuser /etc/passwd`

---

## 50. ניטור משתמשים פעילים

```bash
who
w
```
```
USER     TTY   FROM   LOGIN@  IDLE  WHAT
student  pts/0  :0    18:00   0.00s  w
```
```bash
last | head -10
```
```bash
lastlog | grep -v "Never"
```
```
Username    Port  From     Latest
root        pts/0           Sat Jul 26 10:00
student     pts/0  :0       Sat Jul 26 18:00
```

**משימות:**
- [ ] הרץ `w` — מה כל עמודה אומרת?
- [ ] הרץ `lastlog | grep -v "Never"` — מי נכנס לאחרונה?

---

## 51. ניטור היסטוריית משתמשים

```bash
history | tail -20
```
```
  45  ls -la
  46  cat /etc/passwd
  47  sudo adduser testuser
```
```bash
cat ~/.bash_history | tail -20
```
```bash
history | grep sudo | tail -10
```
> **זכור:** סיסמאות שנכתבו בשורת הפקודה נשמרות כאן!

**משימות:**
- [ ] הרץ `history | tail -20` — מה הפקודות האחרונות?
- [ ] הרץ `history | grep sudo` — אילו פקודות sudo הרצת?

---

## 52. וידוא החשבון הנוכחי

```bash
whoami
```
```
student
```
```bash
id
```
```
uid=1000(student) gid=1000(student) groups=1000(student),24(cdrom),25(floppy),27(sudo)
```
> `id` מציג: UID, GID וכל הקבוצות שהמשתמש שייך אליהן

```bash
groups
```
```
student cdrom floppy sudo
```

**משימות:**
- [ ] הרץ `id` — מה ה-UID שלך? לאיזה קבוצות אתה שייך?
- [ ] הרץ `groups` — מה הקבוצות שלך?

---

## 53. קבוצות — מבוא

**מה זה?**  
קבוצה = אוסף משתמשים עם הרשאות משותפות.

```bash
cat /etc/group | head -10
```
```
root:x:0:
daemon:x:1:
sudo:x:27:student
student:x:1000:
```

| שדה | משמעות |
|-----|--------|
| שם קבוצה | `sudo` |
| `x` | סיסמה (בד"כ ריקה) |
| GID | `27` |
| חברים | `student` |

**משימות:**
- [ ] הרץ `cat /etc/group | grep student` — באיזה קבוצות אתה?

---

## 54. יצירת קבוצה חדשה

```bash
sudo groupadd developers
grep "developers" /etc/group
```
```
developers:x:1002:
```

**משימות:**
- [ ] צור קבוצה `developers` עם `sudo groupadd`
- [ ] ודא עם `grep developers /etc/group`

---

## 55. הוספת משתמשים לקבוצות

```bash
sudo usermod -aG developers student
```
> `-a` = הוסף (אל תחליף קבוצות קיימות) | `-G` = קבוצות

```bash
id student
```
```
uid=1000(student) gid=1000(student) groups=1000(student),27(sudo),1002(developers)
```

**משימות:**
- [ ] הוסף את `student` לקבוצת `developers`
- [ ] ודא עם `id student` — רואה `developers`?

---

## 56. מחיקת קבוצה

```bash
sudo groupdel developers
grep "developers" /etc/group
```
```
(אין תוצאה — נמחקה)
```
> **שים לב:** לא ניתן למחוק קבוצה ראשית של משתמש

**משימות:**
- [ ] מחק `developers` עם `sudo groupdel`
- [ ] ודא עם `grep developers /etc/group`

---

# חלק י' — תקשורת

---

## 57. מבוא לתקשורת

**מה זה?**  
לכל מחשב יש כרטיס רשת (**Network Interface**) עם כתובת IP.

```
Internet → Router (192.168.1.1) → כרטיס רשת (eth0/wlan0) → המחשב שלך
```

**פקודות רשת עיקריות:**

| פקודה | תפקיד |
|-------|-------|
| `ip addr` | הצג כתובות IP |
| `ping` | בדוק חיבור |
| `traceroute` | עקוב אחרי נתיב |
| `nslookup` | שאל DNS |
| `ss` | חיבורי רשת פעילים |

**משימות:**
- [ ] מה ההבדל בין IP פרטי לציבורי?

---

## 58. הגדרות רשת בסיסיות

```bash
ip addr
```
```
1: lo: <LOOPBACK> 
    inet 127.0.0.1/8
2: eth0: <BROADCAST,MULTICAST,UP>
    inet 192.168.1.100/24 brd 192.168.1.255
    link/ether 00:11:22:33:44:55
```
```bash
ip route
```
```
default via 192.168.1.1 dev eth0
192.168.1.0/24 dev eth0
```
> `default via` = כתובת ה-Router (gateway)

```bash
ifconfig eth0    # פקודה ישנה, עדיין שימושית
```

**משימות:**
- [ ] הרץ `ip addr` — מה כתובת ה-IP שלך?
- [ ] הרץ `ip route` — מה כתובת ה-Gateway?
- [ ] מה ה-MAC address שלך? (link/ether)

---

## 59. הפקודה ping

**מה זה?**  
`ping` שולח חבילות קטנות ליעד ובודק אם הוא מגיב.

```bash
ping 8.8.8.8
```
```
PING 8.8.8.8: 56 bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=12.3 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=117 time=11.8 ms
```
> `Ctrl+C` לעצור

```bash
ping -c 4 google.com
```
```
4 packets transmitted, 4 received, 0% packet loss
```
> `-c 4` = שלח 4 חבילות בלבד ועצור

```bash
ping -c 1 192.168.1.1    # בדוק Gateway
```

**משימות:**
- [ ] הרץ `ping -c 4 8.8.8.8` — יש חיבור לאינטרנט?
- [ ] הרץ `ping -c 2 127.0.0.1` — מה זה loopback?
- [ ] הרץ `ping -c 2 192.168.1.1` — יש חיבור ל-Router?

---

## 60. הפקודה traceroute

**מה זה?**  
`traceroute` מראה את כל הנתב שחבילה עוברת מהמחשב שלך עד ליעד.

```bash
traceroute google.com
```
```
traceroute to google.com (142.250.185.46), 30 hops max
 1  192.168.1.1 (192.168.1.1)      1.123 ms    ← הRouter שלך
 2  10.0.0.1    (10.0.0.1)         5.456 ms    ← ספק האינטרנט
 3  72.14.215.1 (72.14.215.1)     15.789 ms
 4  142.250.185.46 (google.com)   20.123 ms    ← היעד
```
> כל שורה = נתב (hop) אחד בדרך

```bash
traceroute -n google.com    # הצג IPs בלי DNS lookup (מהיר יותר)
```

**משימות:**
- [ ] הרץ `traceroute -n 8.8.8.8` — כמה hops עד Google?
- [ ] מה ה-hop הראשון? (אמור להיות ה-Router שלך)

---

## 61. פקודות DNS בסיסיות

**מה זה DNS?**  
DNS מתרגם שמות (google.com) לכתובות IP (142.250.185.46).

```bash
nslookup google.com
```
```
Server:     8.8.8.8
Address:    8.8.8.8#53

Non-authoritative answer:
Name:    google.com
Address: 142.250.185.46
```
```bash
dig google.com
```
```
;; ANSWER SECTION:
google.com.  300  IN  A  142.250.185.46
```
```bash
dig google.com MX    # שרתי מייל
dig google.com NS    # שרתי DNS
```
```bash
host google.com
```
```
google.com has address 142.250.185.46
```

**משימות:**
- [ ] הרץ `nslookup google.com` — מה כתובת ה-IP?
- [ ] הרץ `dig google.com MX` — מצא שרת המייל
- [ ] הרץ `nslookup 8.8.8.8` — מה שם השרת?

---

## 62. שינוי הגדרות DNS

**מה זה?**  
קובץ `/etc/resolv.conf` מגדיר לאיזה שרת DNS פונים.

```bash
cat /etc/resolv.conf
```
```
nameserver 192.168.1.1
nameserver 8.8.8.8
```
```bash
# שנה DNS ל-Cloudflare
echo "nameserver 1.1.1.1" | sudo tee /etc/resolv.conf
cat /etc/resolv.conf
```
```
nameserver 1.1.1.1
```
```bash
nslookup google.com    # בדוק שהDNS עובד
```

**משימות:**
- [ ] הרץ `cat /etc/resolv.conf` — מה שרת ה-DNS הנוכחי?
- [ ] בדוק DNS עם `nslookup google.com`

---

## 63. קובץ ה-hosts

**מה זה?**  
`/etc/hosts` = מיפוי ידני של שמות לכתובות IP **לפני** שאלת DNS.

```bash
cat /etc/hosts
```
```
127.0.0.1    localhost
127.0.1.1    kali
::1          localhost ip6-localhost
```
```bash
# הוסף מיפוי בדיקה
echo "1.2.3.4  testsite.local" | sudo tee -a /etc/hosts
ping -c 1 testsite.local
```
```
PING testsite.local (1.2.3.4): 56 bytes of data.
```
> עכשיו `testsite.local` מפנה ל-`1.2.3.4` — **ללא DNS!**

```bash
# הסר את השורה שהוספנו
sudo sed -i '/testsite.local/d' /etc/hosts
```

**משימות:**
- [ ] הרץ `cat /etc/hosts` — מה `127.0.0.1` ו-`127.0.1.1`?
- [ ] הוסף מיפוי `1.1.1.1 cloudflare.local` ובדוק עם `ping -c 1`
- [ ] הסר בסוף עם `sudo sed -i '/cloudflare.local/d' /etc/hosts`

---

## 64. ניטור חיבורי רשת

**מה זה?**  
`ss` ו-`netstat` מציגים **חיבורים פעילים** ופורטים שמאזינים.

```bash
ss -tlnp
```
```
State   Recv-Q  Send-Q  Local Address:Port  Peer Address:Port
LISTEN  0       128     0.0.0.0:22          0.0.0.0:*    users:(("sshd"))
LISTEN  0       511     *:80                *:*          users:(("apache2"))
```
> `-t` = TCP | `-l` = מאזינים | `-n` = מספרים לא שמות | `-p` = תהליך

```bash
ss -tnp    # חיבורים פעילים (לא listening)
```
```bash
ss -s      # סטטיסטיקות כלליות
```
```
Total: 156
TCP: 8 (estab 2, closed 1, orphaned 0, timewait 1)
```

**משימות:**
- [ ] הרץ `ss -tlnp` — אילו שירותים מאזינים?
- [ ] הרץ `ss -tlnp | grep :22` — SSH מאזין?
- [ ] הרץ `ss -s` — כמה חיבורי TCP פתוחים?

---

# סיכום — פקודות מהירות

```bash
# יסודות
uname -a              echo $SHELL           man ls
ls -la                cd /path              pwd

# קבצים
touch file.txt        echo "x" > file       cat file
cp src dst            mv src dst            rm file
chmod 644 file        stat file             wc file

# תיקיות
mkdir -p a/b/c        ls -la dir/           cp -r dir1 dir2
mv dir1 dir2          rmdir dir             rm -r dir

# חיפוש
find ~ -name "*.txt"  locate file           whereis bash
grep "text" file      ps aux | grep name

# תהליכים
ps aux                top                   kill PID
kill -9 PID           nice -n 10 cmd        sleep 100 &

# שירותים
systemctl status ssh  systemctl start ssh   systemctl stop ssh
systemctl enable ssh  systemctl list-units --type=service

# לוגים
sudo tail -20 /var/log/syslog
sudo grep "Failed" /var/log/auth.log
sudo journalctl -n 20 -p err

# משתמשים
whoami                id                    who
sudo adduser user     sudo deluser user     passwd user
sudo usermod -aG grp user

# תקשורת
ip addr               ping -c 4 8.8.8.8    traceroute google.com
nslookup google.com   ss -tlnp             cat /etc/hosts
```

---

*LINOX LAB FULL — מעבדת לינוקס מקיפה | Kali Linux 2026*
