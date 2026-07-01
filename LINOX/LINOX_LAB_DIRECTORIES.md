# מעבדת תקיות בלינוקס
### פקודות: mkdir -p | rmdir | mv | dir | rm -r

> **רמה:** מתחילים  
> **זמן:** ~20 דקות  
> **עבוד לפי הסדר — כל שלב בנוי על הקודם!**

---

## פקודת `mkdir -p` — יצירת תקיות מקוננות

### מה ההבדל בין `mkdir` רגיל ל-`mkdir -p`?

```bash
mkdir a/b/c
```
פלט (שגיאה!):
```
mkdir: cannot create directory 'a/b/c': No such file or directory
```
> `mkdir` רגיל לא יכול ליצור תקייה אם תקיית האב לא קיימת.

```bash
mkdir -p a/b/c
```
פלט:
```
(שקט = הצלחה)
```
> `-p` = **parents** — יוצר את כל הדרך, גם אם תקיות ביניים לא קיימות.

---

### הדגמות

**צור עץ תקיות שלם בפקודה אחת:**

```bash
mkdir -p ~/myproject/docs/reports
```

ודא שנוצרו כולן:

```bash
ls ~/myproject/
```
פלט:
```
docs
```

```bash
ls ~/myproject/docs/
```
פלט:
```
reports
```

**יצירת כמה ענפים במקביל:**

```bash
mkdir -p ~/myproject/src ~/myproject/tests ~/myproject/logs
ls ~/myproject/
```
פלט:
```
docs  logs  src  tests
```

**`mkdir -p` לא נכשל אם התקייה כבר קיימת:**

```bash
mkdir ~/myproject/src
```
פלט (שגיאה):
```
mkdir: cannot create directory '/home/student/myproject/src': File exists
```

```bash
mkdir -p ~/myproject/src
```
פלט:
```
(שקט = הצלחה — לא נכשל!)
```

---

**משימות:**

- [ ] נסה `mkdir a/b/c` ללא `-p` — מה הודעת השגיאה?
- [ ] צור `~/myproject/docs/reports` בפקודה אחת עם `mkdir -p`
- [ ] צור גם `~/myproject/src`, `~/myproject/tests`, `~/myproject/logs`
- [ ] הרץ `ls ~/myproject/` — כמה תקיות יש?

---

## פקודת `dir` — הצגת תוכן תקייה

### מה זה `dir`?

`dir` היא אחות של `ls` — שתיהן מציגות תוכן תקייה.  
`ls` נפוצה יותר, אך `dir` קיימת בכל מערכת לינוקס.

```bash
dir ~/myproject/
```
פלט:
```
docs  logs  src  tests
```

**עם פרטים מורחבים:**

```bash
dir -l ~/myproject/
```
פלט:
```
total 16
drwxr-xr-x 3 student student 4096 Jul  1 18:00 docs
drwxr-xr-x 2 student student 4096 Jul  1 18:00 logs
drwxr-xr-x 2 student student 4096 Jul  1 18:00 src
drwxr-xr-x 2 student student 4096 Jul  1 18:00 tests
```

**הצג תקיות בשורה אחת לכל אחת:**

```bash
dir -1 ~/myproject/
```
פלט:
```
docs
logs
src
tests
```

---

**משימות:**

- [ ] הרץ `dir ~/myproject/` — מה מוצג?
- [ ] הרץ `dir -l ~/myproject/` — מה ההבדל מ-`dir` רגיל?
- [ ] הרץ גם `ls ~/myproject/` — מה ההבדל בין `dir` ל-`ls`?

---

## פקודת `mv` — העברת תקייה

### זכירה מהירה

`mv` משמשת גם **להעברה** וגם **לשינוי שם**.

```
mv מקור יעד
```

---

**העברת תקייה למקום אחר:**

צור קובץ בתוך `src` לתרגול:

```bash
echo "main code" > ~/myproject/src/main.txt
```

העבר את `src` לתוך `docs`:

```bash
mv ~/myproject/src ~/myproject/docs/
ls ~/myproject/
```
פלט:
```
docs  logs  tests
```
> `src` נעלמה מ-`myproject` ישירות!

```bash
ls ~/myproject/docs/
```
פלט:
```
reports  src
```
> `src` עכשיו בתוך `docs`

---

**שינוי שם תקייה:**

```bash
mv ~/myproject/logs ~/myproject/archive
ls ~/myproject/
```
פלט:
```
archive  docs  tests
```
> `logs` הפכה ל-`archive`

---

**החזר את `src` חזרה למקומה:**

```bash
mv ~/myproject/docs/src ~/myproject/
ls ~/myproject/
```
פלט:
```
archive  docs  src  tests
```

---

**משימות:**

- [ ] העבר את תקיית `src` לתוך `docs` — ודא עם `ls`
- [ ] שנה שם של `logs` ל-`archive`
- [ ] החזר את `src` חזרה ל-`~/myproject/` עם `mv`

---

## פקודת `rmdir` — מחיקת תקייה **ריקה**

### חשוב מאוד!

`rmdir` מוחקת **רק תקיות ריקות**.  
אם יש בתקייה תוכן — היא תיכשל (ואז נשתמש ב-`rm -r`).

---

**מחיקת תקייה ריקה:**

```bash
ls ~/myproject/tests/
```
פלט:
```
(ריקה — אין תוצאות)
```

```bash
rmdir ~/myproject/tests
ls ~/myproject/
```
פלט:
```
archive  docs  src
```
> `tests` נמחקה בהצלחה!

---

**ניסיון למחוק תקייה שיש בה תוכן:**

```bash
rmdir ~/myproject/src
```
פלט (שגיאה):
```
rmdir: failed to remove '/home/student/myproject/src': Directory not empty
```
> `src` יש בה `main.txt` — `rmdir` מסרבת למחוק!

---

**`rmdir -p` — מחיקת שרשרת תקיות ריקות:**

```bash
mkdir -p ~/myproject/tmp/a/b
rmdir -p ~/myproject/tmp/a/b
ls ~/myproject/
```
פלט:
```
archive  docs  src
```
> מחקה `b`, ואז `a`, ואז `tmp` — כולן ריקות, כולן נמחקו

---

**משימות:**

- [ ] הרץ `rmdir ~/myproject/tests` — הצליח? מה קרה?
- [ ] נסה `rmdir ~/myproject/src` — מה הודעת השגיאה? למה?
- [ ] צור `mkdir -p ~/myproject/tmp/a/b` ומחק עם `rmdir -p`

---

## פקודת `rm -r` — מחיקת תקייה עם כל התוכן

### מתי משתמשים?

כשצריך למחוק תקייה שיש בה קבצים ותת-תקיות.  
`-r` = **recursive** — יורד לכל התת-תקיות ומוחק הכל.

```
rm -r תקייה/    ← מוחק תקייה עם כל תוכנה (ללא אישור)
rm -ri תקייה/   ← מוחק עם שאלת אישור לכל פריט
```

> **אזהרה:** `rm -r` **לא** שולחת לסל מחזור. מחיקה = סופית!

---

**מחיקת תקייה עם תוכן:**

בדוק מה יש ב-`src` לפני המחיקה:

```bash
ls ~/myproject/src/
```
פלט:
```
main.txt
```

מחק:

```bash
rm -r ~/myproject/src
ls ~/myproject/
```
פלט:
```
archive  docs
```
> `src` ותוכנה נמחקו!

---

**מחיקה עם אישור לכל פריט (`-i`):**

```bash
mkdir -p ~/myproject/trash
echo "file1" > ~/myproject/trash/file1.txt
echo "file2" > ~/myproject/trash/file2.txt

rm -ri ~/myproject/trash
```
פלט:
```
rm: descend into directory '/home/student/myproject/trash'? y
rm: remove regular file '/home/student/myproject/trash/file1.txt'? y
rm: remove regular file '/home/student/myproject/trash/file2.txt'? y
rm: remove directory '/home/student/myproject/trash'? y
```
> `y` = אשר | `n` = דלג

---

**ניקוי — מחק את כל `myproject`:**

```bash
rm -r ~/myproject
ls ~/
```
פלט:
```
Desktop  Documents  Downloads
```
> `myproject` ו**כל** מה שהיה בה — נמחקו.

---

**משימות:**

- [ ] הרץ `rm -r ~/myproject/src` — ודא שנמחקה עם `ls`
- [ ] צור `~/myproject/trash` עם 2 קבצים בפנים
- [ ] מחק עם `rm -ri` — ענה `y` לכל שאלה
- [ ] בסוף: `rm -r ~/myproject` — ודא שהכל נמחק עם `ls ~/`

---

## סיכום

| פקודה | מה היא עושה | מתי משתמשים |
|-------|------------|-------------|
| `mkdir -p a/b/c` | יוצר תקיות כולל תקיות ביניים | כשצריך עץ תקיות שלם בבת אחת |
| `dir path/` | הצגת תוכן תקייה | חלופה ל-`ls` |
| `mv src dst` | מעביר או משנה שם | תמיד — גם העברה גם שינוי שם |
| `rmdir dir/` | מוחק תקייה ריקה בלבד | כשבטוחים שהתקייה ריקה |
| `rmdir -p a/b/c` | מוחק שרשרת תקיות ריקות | ניקוי עץ תקיות ריק |
| `rm -r dir/` | מוחק תקייה עם כל תוכנה | מחיקה מלאה |
| `rm -ri dir/` | מוחק עם אישור לכל פריט | כשרוצים לבחור מה למחוק |

---

*LINOX LAB — Directories | מעבדת פקודות תקיות*
