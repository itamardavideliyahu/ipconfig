# מעבדת חזרה — לינוקס
### תרגול מעשי משולב | ~30 דקות

> **נושאים:** תקיות, שמירת פלטים, ps, find, locate, chmod, kill, mv  
> **רמה:** מתחילים  
> **חשוב:** כל שלב בנוי על הקודם — עבוד לפי הסדר!

---

## הסיפור שלנו

אנחנו מגיעים למחשב לינוקס, יוצרים תקיית עבודה, שומרים בה מידע על המערכת, ובסוף מעבירים את הכל למקום אחר.

---

## שלב 1 — יצירת תקיית עבודה ⏱ 5 דקות

### יצירת תקייה ותת-תקיות

```bash
mkdir ~/mylab
```
> אין פלט = הצלחה

ודא שנוצרה:

```bash
ls ~/
```
פלט לדוגמה:
```
Desktop  Documents  Downloads  mylab
```

כנס לתקייה:

```bash
cd ~/mylab
pwd
```
פלט:
```
/home/student/mylab
```

צור שתי תת-תקיות בתוכה:

```bash
mkdir processes files
ls
```
פלט:
```
files  processes
```

---

### שמירת פלטים לקבצים

עד עכשיו ראינו פלטים בטרמינל — הם נעלמים ברגע שסוגרים אותו.  
כדי לשמור מידע, נשתמש ב-`>` ו-`>>`:

```
פקודה > קובץ.txt    ← כותב לקובץ (אם הקובץ קיים — מחליף!)
פקודה >> קובץ.txt   ← מוסיף לסוף הקובץ (לא מוחק מה שיש)
```

נשמור מידע בסיסי על המערכת:

```bash
echo "=== פרטי מערכת ===" > system_info.txt
uname -a >> system_info.txt
echo "=== שם המשתמש ===" >> system_info.txt
whoami >> system_info.txt
```

הצג את מה שנשמר:

```bash
cat system_info.txt
```
פלט לדוגמה:
```
=== פרטי מערכת ===
Linux kali 6.1.0-kali9-amd64 #1 SMP x86_64 GNU/Linux
=== שם המשתמש ===
student
```

---

**משימות — שלב 1:**

- [ ] צור `~/mylab` עם שתי תת-תקיות: `processes` ו-`files`
- [ ] שמור את פרטי המערכת ל-`system_info.txt` בדיוק כמו בדוגמה
- [ ] הצג את הקובץ עם `cat` — יש בו שתי כותרות ותוכן?

---

## שלב 2 — בדיקת תהליכים עם `ps` ⏱ 8 דקות

### מה זה תהליך?

כל דבר שרץ על המחשב — דפדפן, טרמינל, שרת — הוא **תהליך (Process)**.  
לכל תהליך יש מספר זיהוי ייחודי שנקרא **PID**.

```
PID 1 = systemd  ← התהליך הראשון שהמערכת מפעילה
PID 2, 3, 4...  ← כל שאר התהליכים
```

### פקודת `ps aux`

```bash
ps aux
```
פלט לדוגמה:
```
USER       PID %CPU %MEM  COMMAND
root         1  0.0  0.1  /sbin/init
root       423  0.0  0.2  /usr/sbin/sshd
www-data   891  0.1  0.8  /usr/sbin/apache2
student   1203  0.0  0.1  bash
student   1250  0.0  0.0  ps aux
```

**הסבר העמודות:**

| עמודה | משמעות |
|-------|--------|
| `USER` | מי הפעיל את התהליך |
| `PID` | מספר זיהוי (חשוב ל-kill!) |
| `%CPU` | כמה CPU הוא צורך |
| `%MEM` | כמה זיכרון הוא צורך |
| `COMMAND` | מה רץ בפועל |

---

חיפוש תהליך ספציפי לפי שם:

```bash
ps aux | grep bash
```
פלט לדוגמה:
```
student  1203  0.0  0.1  bash
student  1301  0.0  0.0  grep --color=auto bash
```
> השורה הראשונה היא ה-bash שלנו. השנייה היא ה-grep עצמו — אפשר להתעלם ממנה.

---

הפעל תהליך ברקע (נצטרך אותו בשלב 5):

```bash
sleep 500 &
```
פלט:
```
[1] 1456
```
> `1456` הוא ה-PID — **שמור אותו! נשתמש בו אחר כך.**

ודא שהתהליך רץ:

```bash
ps aux | grep sleep
```
פלט:
```
student  1456  0.0  0.0  sleep 500
```

---

שמור את רשימת התהליכים לתקייה שלנו:

```bash
ps aux > ~/mylab/processes/all_processes.txt
```

ודא שנשמר:

```bash
ls -lh ~/mylab/processes/
```
פלט:
```
-rw-r--r-- 1 student student 4.2K Jun 20 all_processes.txt
```

---

**משימות — שלב 2:**

- [ ] הרץ `ps aux` — מצא את ה-PID של `bash` שלך
- [ ] הרץ `ps aux | grep root` — כמה תהליכים רצים כ-root?
- [ ] הפעל `sleep 500 &` — **רשום את ה-PID שהוצג**
- [ ] שמור את כל התהליכים ל-`processes/all_processes.txt`

---

## שלב 3 — הרשאות קבצים עם `chmod` ⏱ 7 דקות

### איך עובדות הרשאות בלינוקס?

כל קובץ יש לו שלוש קבוצות הרשאות:

```
-  rw-  r--  r--
│   │    │    └── Other  — כולם
│   │    └─────── Group  — חברי הקבוצה
│   └──────────── User   — הבעלים של הקובץ
└──────────────── סוג: - = קובץ,  d = תקייה
```

שלוש הרשאות אפשריות:

| אות | מספר | מה זה אומר |
|-----|------|------------|
| `r` | 4 | קריאה (Read) |
| `w` | 2 | כתיבה (Write) |
| `x` | 1 | הרצה (Execute) |

### איך מחשבים את המספר?

```
rwx = 4+2+1 = 7   (הכל)
rw- = 4+2+0 = 6   (קרא וכתוב)
r-- = 4+0+0 = 4   (קריאה בלבד)
--- = 0+0+0 = 0   (כלום)
```

`chmod 644 file` = User: `rw-` (6) | Group: `r--` (4) | Other: `r--` (4)

---

בדוק את ההרשאות הנוכחיות של הקבצים שלנו:

```bash
ls -la ~/mylab/
```
פלט לדוגמה:
```
drwxr-xr-x 4 student student 4096 Jun 20 .
drwxr-xr-x 8 student student 4096 Jun 20 ..
drwxr-xr-x 2 student student 4096 Jun 20 files
drwxr-xr-x 2 student student 4096 Jun 20 processes
-rw-r--r-- 1 student student   95 Jun 20 system_info.txt
```

---

**שנה הרשאות — דוגמאות:**

הפוך קובץ לקריאה בלבד (גם לבעלים):

```bash
chmod 444 ~/mylab/system_info.txt
ls -la ~/mylab/system_info.txt
```
פלט:
```
-r--r--r-- 1 student student 95 Jun 20 system_info.txt
```

נסה לכתוב לקובץ עם הרשאות 444:

```bash
echo "test" >> ~/mylab/system_info.txt
```
פלט:
```
bash: /home/student/mylab/system_info.txt: Permission denied
```
> הרשאות עובדות! לא ניתן לכתוב לקובץ read-only.

החזר הרשאות כתיבה לבעלים:

```bash
chmod 644 ~/mylab/system_info.txt
ls -la ~/mylab/system_info.txt
```
פלט:
```
-rw-r--r-- 1 student student 95 Jun 20 system_info.txt
```

הפוך קובץ לפרטי לחלוטין (רק הבעלים יכול לקרוא ולכתוב):

```bash
chmod 600 ~/mylab/processes/all_processes.txt
ls -la ~/mylab/processes/all_processes.txt
```
פלט:
```
-rw------- 1 student student 4.2K Jun 20 all_processes.txt
```
> כעת אף אחד אחר לא יכול לקרוא את הקובץ

---

**משימות — שלב 3:**

- [ ] הרץ `ls -la ~/mylab/` — מה ההרשאות של `system_info.txt`?
- [ ] הפוך אותו ל-`444` ונסה לכתוב — מה קורה?
- [ ] החזר ל-`644` ונסה שוב לכתוב `echo "test" >> system_info.txt` — עובד?
- [ ] הגן על `all_processes.txt` עם `chmod 600`

---

## שלב 4 — חיפוש קבצים עם `find` ו-`locate` ⏱ 5 דקות

### `find` — חיפוש בזמן אמת

מציאת כל הקבצים בתקיית `mylab`:

```bash
find ~/mylab -type f
```
פלט:
```
/home/student/mylab/system_info.txt
/home/student/mylab/processes/all_processes.txt
```

חיפוש לפי סיומת:

```bash
find ~/mylab -name "*.txt"
```
פלט:
```
/home/student/mylab/system_info.txt
/home/student/mylab/processes/all_processes.txt
```

מציאת תקיות בלבד:

```bash
find ~/mylab -type d
```
פלט:
```
/home/student/mylab
/home/student/mylab/files
/home/student/mylab/processes
```

שמור את רשימת הקבצים:

```bash
find ~/mylab -type f > ~/mylab/files/file_list.txt
cat ~/mylab/files/file_list.txt
```
פלט:
```
/home/student/mylab/system_info.txt
/home/student/mylab/processes/all_processes.txt
```

---

### `locate` — חיפוש מהיר

`locate` מחפש ב-database מוכנה — הרבה יותר מהיר מ-`find`.  
**חסרון:** לא יודע על קבצים שנוצרו לאחרונה — צריך לעדכן קודם.

עדכן את ה-database:

```bash
sudo updatedb
```

חפש את הקובץ שיצרנו:

```bash
locate system_info.txt
```
פלט:
```
/home/student/mylab/system_info.txt
```

חפש לפי חלק מהשם:

```bash
locate mylab
```
פלט:
```
/home/student/mylab
/home/student/mylab/files
/home/student/mylab/files/file_list.txt
/home/student/mylab/processes
/home/student/mylab/processes/all_processes.txt
/home/student/mylab/system_info.txt
```

---

**משימות — שלב 4:**

- [ ] הרץ `find ~/mylab -type f` — כמה קבצים יש?
- [ ] הרץ `find ~/mylab -name "*.txt"` — נמצאו אותם קבצים?
- [ ] הרץ `sudo updatedb` ואז `locate system_info.txt` — נמצא?
- [ ] שמור רשימת קבצים ל-`files/file_list.txt`

---

## שלב 5 — סיום תהליכים עם `kill` ⏱ 5 דקות

### מה זה `kill`?

`kill` שולח **הודעה לתהליך** שיפסיק לרוץ.  
יש שני סוגים עיקריים:

```
kill PID      ← בקשה נעימה — "בבקשה תסגר" (SIGTERM)
kill -9 PID   ← כיבוי כוחני — "מת עכשיו" (SIGKILL)
```

תמיד מנסים `kill` רגיל קודם. רק אם התהליך לא מגיב — משתמשים ב-`kill -9`.

---

**זכור את ה-`sleep 500` שהפעלנו בשלב 2?**

מצא אותו שוב — וודא שה-PID שרשמת נכון:

```bash
ps aux | grep sleep
```
פלט:
```
student  1456  0.0  0.0  sleep 500
student  1890  0.0  0.0  grep --color=auto sleep
```
> ה-PID שלנו הוא `1456` — לא `1890` שזה ה-grep עצמו

שלח לו הודעת סיום:

```bash
kill 1456
```

ודא שנסגר:

```bash
ps aux | grep sleep
```
פלט לאחר kill:
```
student  1891  0.0  0.0  grep --color=auto sleep
```
> שורת ה-`sleep 500` נעלמה — התהליך נסגר!

בטרמינל תופיע גם הודעה:
```
[1]+  Terminated              sleep 500
```

---

הפעל תהליך חדש ורוג אותו עם `-9`:

```bash
sleep 999 &
```
פלט:
```
[1] 2050
```

```bash
kill -9 2050
```

```bash
ps aux | grep sleep
```
פלט:
```
[1]+  Killed                  sleep 999
```
> `Killed` = נרצח בכוח (SIGKILL). `Terminated` = נסגר בנימוס (SIGTERM).

---

**משימות — שלב 5:**

- [ ] הרץ `ps aux | grep sleep` — מצא את ה-PID של ה-sleep משלב 2
- [ ] הרץ `kill <PID>` — ודא שנסגר עם `ps aux | grep sleep`
- [ ] הפעל `sleep 999 &` — רשום PID ורוג עם `kill -9`
- [ ] מה ההבדל בהודעה בין `Terminated` ל-`Killed`?

---

## שלב 6 — העברת התקייה ⏱ 2 דקות

### מה יש לנו?

```bash
find ~/mylab -type f
```
פלט:
```
/home/student/mylab/system_info.txt
/home/student/mylab/files/file_list.txt
/home/student/mylab/processes/all_processes.txt
```

```bash
du -sh ~/mylab
```
פלט לדוגמה:
```
28K     /home/student/mylab
```

---

### העבר הכל לתקיית ארכיון

```bash
mkdir ~/archive
mv ~/mylab ~/archive/
```

ודא שנעלמה מ-home:

```bash
ls ~/
```
פלט:
```
Desktop  Documents  Downloads  archive
```
> `mylab` נעלמה!

ודא שנמצאת בארכיון:

```bash
ls ~/archive/
```
פלט:
```
mylab
```

ודא שכל הקבצים שרדו:

```bash
find ~/archive/mylab -type f
```
פלט:
```
/home/student/archive/mylab/system_info.txt
/home/student/archive/mylab/files/file_list.txt
/home/student/archive/mylab/processes/all_processes.txt
```

---

**משימות — שלב 6:**

- [ ] הרץ `find ~/mylab -type f` — כמה קבצים יש בסה"כ?
- [ ] צור `~/archive` ו-העבר אליה את `mylab` עם `mv`
- [ ] ודא שה-`mylab` נעלמה מ-`~/` ונמצאת ב-`~/archive/`
- [ ] ודא שכל הקבצים שרדו עם `find ~/archive/mylab -type f`

---

## סיכום הפקודות

| פקודה | מה היא עושה |
|-------|------------|
| `mkdir dir` | יצירת תקייה |
| `mv source dest` | העברת תקייה/קובץ |
| `command > file` | שמור פלט לקובץ |
| `command >> file` | הוסף פלט לקובץ קיים |
| `ps aux` | הצג את כל התהליכים |
| `ps aux \| grep name` | חפש תהליך לפי שם |
| `sleep N &` | הפעל תהליך ברקע |
| `chmod 644 file` | שנה הרשאות |
| `find ~/dir -type f` | חפש קבצים |
| `find ~/dir -name "*.txt"` | חפש לפי שם |
| `sudo updatedb` | עדכן database של locate |
| `locate name` | חפש קובץ במהירות |
| `kill PID` | סגור תהליך בנימוס |
| `kill -9 PID` | סגור תהליך בכוח |

---

*LINOX LAB — Review | מעבדת חזרה משולבת*
