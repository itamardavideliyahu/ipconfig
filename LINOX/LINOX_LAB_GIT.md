# מעבדת Git ו-GitHub בקאלי לינוקס
### עבודה עם גרסאות קוד מהטרמינל

> **רמה:** מתחילים ממש  
> **זמן:** ~45 דקות  
> **דרישה:** חשבון GitHub (צור בחינם ב-github.com אם אין לך)

---

## מה זה Git ולמה צריך אותו?

**Git** הוא כלי שעוקב אחרי כל שינוי שעשית בקבצים.  
**GitHub** הוא אתר שמאחסן את הקוד שלך באינטרנט.

```
בלי Git:                    עם Git:
mycode.py                   mycode.py
mycode_v2.py                ← Git זוכר כל גרסה בלי לשמור עותקים
mycode_v2_final.py
mycode_v2_final_REAL.py     ← מוכר?
```

### 3 מקומות שחשוב להכיר

```
Working Directory  →  Staging Area  →  Repository (.git)  →  GitHub
   (הקבצים שלך)       (git add)        (git commit)          (git push)
```

---

## שלב 1 — הכנה ראשונית ⏱ 5 דקות

### בדוק ש-Git מותקן

```bash
git --version
```
פלט לדוגמה:
```
git version 2.43.0
```
> אם Git לא מותקן: `sudo apt install git -y`

---

### הגדר את הפרטים שלך

Git חייב לדעת מי אתה לפני שמתחיל לעבוד:

```bash
git config --global user.name "השם שלך"
git config --global user.email "המייל@שלך.com"
```

> השתמש באותו מייל שרשמת ב-GitHub!

ודא שנשמר:

```bash
git config --list
```
פלט לדוגמה:
```
user.name=Itamar David
user.email=itamar@example.com
```

---

**משימות — שלב 1:**

- [ ] הרץ `git --version` — מה הגרסה?
- [ ] הגדר `user.name` ו-`user.email` עם הפרטים שלך
- [ ] ודא עם `git config --list`

---

## שלב 2 — יצירת Repository מקומי ⏱ 8 דקות

### מה זה Repository?

Repository (בקצרה: **repo**) = תקייה שGit עוקב אחריה.  
כשמריצים `git init` — Git יוצר תקיית `.git` מוסתרת בתוכה שמכילה את כל ההיסטוריה.

---

**צור תקיית פרויקט:**

```bash
mkdir ~/my_first_repo
cd ~/my_first_repo
```

**הפוך אותה ל-Git repository:**

```bash
git init
```
פלט:
```
Initialized empty Git repository in /home/student/my_first_repo/.git/
```

**ראה את תקיית `.git` הנסתרת:**

```bash
ls -la
```
פלט:
```
total 12
drwxr-xr-x 3 student student 4096 Jul  1 18:00 .
drwxr-xr-x 8 student student 4096 Jul  1 18:00 ..
drwxr-xr-x 7 student student 4096 Jul  1 18:00 .git
```
> התקייה `.git` = "המוח" של Git. **לעולם אל תמחק אותה!**

**בדוק את מצב ה-repo:**

```bash
git status
```
פלט:
```
On branch main

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```
> "No commits yet" = הRepo ריק, אין שום שינויים שנשמרו עדיין

---

**משימות — שלב 2:**

- [ ] צור תקייה `~/my_first_repo` וכנס אליה
- [ ] הרץ `git init` — ראה את ההודעה
- [ ] ודא שנוצרה `.git` עם `ls -la`
- [ ] הרץ `git status` — מה הוא אומר?

---

## שלב 3 — הוספה ו-Commit ⏱ 10 דקות

### הזרימה הבסיסית של Git

```
1. שנה קובץ       →  Working Directory
2. git add         →  Staging Area (הכנה לשמירה)
3. git commit      →  Repository (נשמר לצמיתות!)
```

---

**צור קובץ ראשון:**

```bash
echo "# My First Repo" > README.md
echo "This is my first Git project." >> README.md
cat README.md
```
פלט:
```
# My First Repo
This is my first Git project.
```

**ראה מה Git חושב על השינוי:**

```bash
git status
```
פלט:
```
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	README.md

nothing added to commit but untracked files present (use "git add" to track)
```
> **Untracked** = Git רואה את הקובץ אך עדיין לא עוקב אחריו

---

**הוסף לStaging Area:**

```bash
git add README.md
git status
```
פלט:
```
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   README.md
```
> **Changes to be committed** = הקובץ מוכן לcommit (בירוק!)

---

**שמור את השינוי (Commit):**

```bash
git commit -m "Add README file"
```
פלט:
```
[main (root-commit) a1b2c3d] Add README file
 1 file changed, 2 insertions(+)
 create mode 100644 README.md
```

> `-m "הודעה"` = הודעת commit — תיאור קצר של מה שינית  
> `a1b2c3d` = מספר ה-commit הייחודי (hash)

**ודא שנשמר:**

```bash
git status
```
פלט:
```
On branch main
nothing to commit, working tree clean
```
> "working tree clean" = אין שינויים חדשים, הכל נשמר

---

**הוסף עוד קובץ וראה את כל ה-Workflow:**

```bash
echo "print('Hello from Kali!')" > hello.py
git status
```
פלט:
```
Untracked files:
	hello.py
```

```bash
git add hello.py
git commit -m "Add hello python file"
```
פלט:
```
[main b2c3d4e] Add hello python file
 1 file changed, 1 insertion(+)
 create mode 100644 hello.py
```

---

**הצג את היסטוריית הCommits:**

```bash
git log
```
פלט:
```
commit b2c3d4e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4
Author: Itamar David <itamar@example.com>
Date:   Tue Jul 01 18:10:00 2025 +0300

    Add hello python file

commit a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0
Author: Itamar David <itamar@example.com>
Date:   Tue Jul 01 18:05:00 2025 +0300

    Add README file
```
> `q` לצאת מ-log

**הצגה מקוצרת:**

```bash
git log --oneline
```
פלט:
```
b2c3d4e Add hello python file
a1b2c3d Add README file
```

---

**משימות — שלב 3:**

- [ ] צור `README.md` עם כותרת ושורת תיאור
- [ ] הרץ `git status` — האם הוא Untracked?
- [ ] הרץ `git add README.md` ושוב `git status` — מה השתנה?
- [ ] הרץ `git commit -m "Add README file"`
- [ ] צור `hello.py` והוסף commit נוסף
- [ ] הרץ `git log --oneline` — רואה שני commits?

---

## שלב 4 — חיבור ל-GitHub ⏱ 7 דקות

### יצירת Repo חדש ב-GitHub

1. כנס ל-**github.com** והתחבר לחשבון שלך
2. לחץ על **"New"** (כפתור ירוק בצד שמאל)
3. תן שם: `my_first_repo`
4. **אל תסמן** "Add README file" — הRepo שלנו כבר קיים!
5. לחץ **"Create repository"**

GitHub יראה לך מסך עם פקודות — השתמש בחלק של **"…or push an existing repository from the command line"**

---

### חיבור ה-Repo המקומי ל-GitHub

```bash
git remote add origin https://github.com/USERNAME/my_first_repo.git
```
> החלף `USERNAME` בשם המשתמש שלך ב-GitHub

ודא שהחיבור נוצר:

```bash
git remote -v
```
פלט:
```
origin  https://github.com/USERNAME/my_first_repo.git (fetch)
origin  https://github.com/USERNAME/my_first_repo.git (push)
```
> `origin` = השם שנתנו לשרת המרוחק (GitHub)

---

**משימות — שלב 4:**

- [ ] צור repo חדש ב-GitHub בשם `my_first_repo`
- [ ] הרץ `git remote add origin <הURL שלך>`
- [ ] ודא עם `git remote -v`

---

## שלב 5 — העלאה ל-GitHub (Push) ⏱ 5 דקות

### העלה את הCommits ל-GitHub

```bash
git push -u origin main
```
פלט:
```
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Writing objects: 100% (4/4), 345 bytes | 345.00 KiB/s, done.
Total 4 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/USERNAME/my_first_repo.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

> `-u origin main` = "העלה לorigin לענף main, ובפעמים הבאות זכור את זה"  
> בפעמים הבאות מספיק `git push` בלבד

> **אם GitHub מבקש סיסמה** — צריך Personal Access Token.  
> ב-GitHub: Settings → Developer settings → Personal access tokens → Generate new token

---

**לאחר ה-push — כנס לGitHub ורענן את הדף.**  
תראה את `README.md` ו-`hello.py` שם!

---

**ערוך קובץ ועשה push נוסף:**

```bash
echo "# Updated!" >> README.md
git add README.md
git commit -m "Update README with new line"
git push
```
פלט:
```
Enumerating objects: 5, done.
To https://github.com/USERNAME/my_first_repo.git
   b2c3d4e..c3d4e5f  main -> main
```

---

**משימות — שלב 5:**

- [ ] הרץ `git push -u origin main` — עלה בהצלחה?
- [ ] פתח GitHub בדפדפן — האם הקבצים מופיעים?
- [ ] ערוך `README.md`, עשה commit ו-`git push` נוסף
- [ ] ודא שהשינוי מופיע ב-GitHub

---

## שלב 6 — הורדה מ-GitHub (Pull & Clone) ⏱ 5 דקות

### `git pull` — הבא שינויים מ-GitHub

אם מישהו שינה קובץ ב-GitHub (ישירות דרך האתר) — `git pull` מוריד את השינויים:

```bash
git pull
```
פלט כשאין שינויים:
```
Already up to date.
```

פלט כשיש שינויים:
```
Updating b2c3d4e..d4e5f6a
Fast-forward
 README.md | 2 ++
 1 file changed, 2 insertions(+)
```

---

### `git clone` — הורדת Repo שלם

`clone` מוריד repo שלם מ-GitHub למחשב — כולל כל ההיסטוריה.  
לא צריך `git init` — הכל בא ביחד.

```bash
cd ~
git clone https://github.com/USERNAME/my_first_repo.git my_repo_copy
```
פלט:
```
Cloning into 'my_repo_copy'...
remote: Enumerating objects: 6, done.
remote: Counting objects: 100% (6/6), done.
Receiving objects: 100% (6/6), done.
```

```bash
ls ~/my_repo_copy/
```
פלט:
```
README.md  hello.py
```
> כל הקבצים הורדו! כולל ההיסטוריה המלאה של commits.

```bash
cd ~/my_repo_copy
git log --oneline
```
פלט:
```
c3d4e5f Update README with new line
b2c3d4e Add hello python file
a1b2c3d Add README file
```

---

**משימות — שלב 6:**

- [ ] הרץ `git pull` מתוך `~/my_first_repo`
- [ ] הרץ `git clone <URL שלך> my_repo_copy`
- [ ] כנס לתקייה החדשה ובדוק שהקבצים שם עם `ls` ו-`git log --oneline`

---

## סיכום — פקודות Git הבסיסיות

```bash
# ── הגדרה ────────────────────────────────────────────────
git config --global user.name "שם"     # הגדר שם משתמש
git config --global user.email "מייל"  # הגדר מייל
git config --list                       # הצג הגדרות

# ── יצירת Repo ───────────────────────────────────────────
git init                                # הפוך תקייה ל-repo
git clone <URL>                         # הורד repo מGitHub

# ── מעקב שינויים ─────────────────────────────────────────
git status                              # מה המצב הנוכחי?
git add filename                        # הוסף קובץ לStaging
git add .                               # הוסף את כל הקבצים
git commit -m "הודעה"                  # שמור שינויים

# ── היסטוריה ─────────────────────────────────────────────
git log                                 # הצג commits מפורט
git log --oneline                       # הצג commits בשורה אחת

# ── GitHub ───────────────────────────────────────────────
git remote add origin <URL>             # חבר ל-GitHub
git remote -v                           # הצג חיבורים קיימים
git push -u origin main                 # העלה לGitHub (ראשון)
git push                                # העלה לGitHub (הבא)
git pull                                # הורד שינויים מGitHub
```

---

## הזרימה שתחזור כל פעם

```
1.  ערוך קובץ
2.  git status       ← ראה מה השתנה
3.  git add .        ← הכן לשמירה
4.  git commit -m "" ← שמור עם הודעה
5.  git push         ← העלה ל-GitHub
```

---

*LINOX LAB — Git & GitHub | מעבדת גרסאות קוד*
