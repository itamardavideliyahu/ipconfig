# מעבדת Git — העלאת אתר ווב לGitHub
### בניית אתר בננות ושליחתו לענן

> **זמן:** ~30 דקות  
> **מה תעשה:** תיצור אתר ווב מקומי → תדחוף אותו ל-GitHub

---

## שלב 1 — הכן את סביבת העבודה

פתח טרמינל וצור תקייה לפרויקט:

```bash
mkdir ~/banana_site
cd ~/banana_site
```

הפוך אותה ל-Git repository:

```bash
git init
```
פלט:
```
Initialized empty Git repository in /home/student/banana_site/.git/
```

---

## שלב 2 — צור את קבצי האתר

### קובץ 1 — `index.html` (עמוד הבית)

```bash
cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>עולם הבננות</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <header>
        <h1>🍌 עולם הבננות 🍌</h1>
        <p>כל מה שרצית לדעת על הפרי הצהוב</p>
    </header>

    <main>
        <section class="facts">
            <h2>עובדות מעניינות</h2>
            <ul>
                <li>בננה מכילה אשלגן שעוזר לשרירים</li>
                <li>בננה היא טכנית עשב ולא עץ</li>
                <li>הבננה הנפוצה היום נקראת Cavendish</li>
                <li>בננה ירוקה מכילה יותר עמילן</li>
                <li>בננה בשלה מכילה יותר סוכר</li>
            </ul>
        </section>

        <section class="types">
            <h2>סוגי בננות</h2>
            <div class="cards">
                <div class="card">
                    <h3>Cavendish</h3>
                    <p>הנפוצה ביותר בעולם. צהובה, מתוקה.</p>
                </div>
                <div class="card">
                    <h3>Red Banana</h3>
                    <p>אדומה-סגולה, מתוקה יותר.</p>
                </div>
                <div class="card">
                    <h3>Plantain</h3>
                    <p>לבישול בלבד, פחות מתוקה.</p>
                </div>
            </div>
        </section>
    </main>

    <footer>
        <p>נבנה במעבדת Git | 2024</p>
    </footer>

    <script src="script.js"></script>
</body>
</html>
EOF
```

---

### קובץ 2 — `style.css` (עיצוב)

```bash
cat > style.css << 'EOF'
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    background-color: #fffde7;
    color: #333;
}

header {
    background-color: #f9a825;
    text-align: center;
    padding: 40px 20px;
}

header h1 {
    font-size: 2.5em;
    color: white;
}

header p {
    font-size: 1.1em;
    color: #fff8e1;
    margin-top: 8px;
}

main {
    max-width: 900px;
    margin: 40px auto;
    padding: 0 20px;
}

section {
    margin-bottom: 40px;
}

h2 {
    font-size: 1.6em;
    color: #f57f17;
    margin-bottom: 16px;
    border-bottom: 2px solid #f9a825;
    padding-bottom: 8px;
}

ul {
    list-style: none;
    padding: 0;
}

ul li {
    padding: 8px 0;
    border-bottom: 1px solid #ffe082;
}

ul li::before {
    content: "🍌 ";
}

.cards {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
}

.card {
    background: white;
    border: 2px solid #ffe082;
    border-radius: 10px;
    padding: 20px;
    flex: 1;
    min-width: 200px;
}

.card h3 {
    color: #f57f17;
    margin-bottom: 8px;
}

footer {
    text-align: center;
    padding: 20px;
    background-color: #f9a825;
    color: white;
    margin-top: 40px;
}
EOF
```

---

### קובץ 3 — `script.js` (אינטראקטיביות)

```bash
cat > script.js << 'EOF'
// הודעת ברוכים הבאים
console.log("ברוכים הבאים לעולם הבננות!");

// צבע כרטיסים בריחוף
const cards = document.querySelectorAll('.card');

cards.forEach(card => {
    card.addEventListener('mouseover', function() {
        this.style.backgroundColor = '#fff9c4';
    });

    card.addEventListener('mouseout', function() {
        this.style.backgroundColor = 'white';
    });
});
EOF
```

---

### ודא שכל הקבצים נוצרו:

```bash
ls -la
```
פלט:
```
-rw-r--r-- 1 student student 1247 Jul  5 index.html
-rw-r--r-- 1 student student  892 Jul  5 script.js
-rw-r--r-- 1 student student 1103 Jul  5 style.css
```

---

## שלב 3 — הוסף הכל ל-Git

בדוק את מצב הקבצים:

```bash
git status
```
פלט:
```
On branch main

No commits yet

Untracked files:
        index.html
        script.js
        style.css

nothing added to commit but untracked files present
```
> Git רואה את הקבצים אך עדיין לא עוקב אחריהם (Untracked)

הוסף את **כל** הקבצים בבת אחת:

```bash
git add .
```

בדוק שוב:

```bash
git status
```
פלט:
```
Changes to be committed:
        new file:   index.html
        new file:   script.js
        new file:   style.css
```
> כעת הקבצים בירוק — מוכנים ל-commit

שמור עם commit:

```bash
git commit -m "Add banana website - HTML, CSS, JS"
```
פלט:
```
[main (root-commit) a1b2c3d] Add banana website - HTML, CSS, JS
 3 files changed, 87 insertions(+)
 create mode 100644 index.html
 create mode 100644 script.js
 create mode 100644 style.css
```

---

## שלב 4 — צור Repo ב-GitHub

1. כנס ל-**github.com** והתחבר
2. לחץ **"New"** (כפתור ירוק)
3. מלא:
   - **Repository name:** `banana_site`
   - **Description:** `My first banana website`
   - **Public** ✅
   - **אל תסמן** Add README / .gitignore
4. לחץ **"Create repository"**

---

## שלב 5 — חבר ודחוף ל-GitHub

חבר את הrepo המקומי ל-GitHub:

```bash
git remote add origin https://github.com/USERNAME/banana_site.git
```
> החלף `USERNAME` בשם שלך ב-GitHub

ודא החיבור:

```bash
git remote -v
```
פלט:
```
origin  https://github.com/USERNAME/banana_site.git (fetch)
origin  https://github.com/USERNAME/banana_site.git (push)
```

שמור Token כדי לא להקליד בכל פעם:

```bash
git config --global credential.helper store
```

דחוף ל-GitHub:

```bash
git push -u origin main
```
פלט:
```
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Writing objects: 100% (5/5), 1.23 KiB | 1.23 MiB/s, done.
To https://github.com/USERNAME/banana_site.git
 * [new branch]      main -> main
```

> כשישאל — הכנס Username וה-Token כסיסמה. לאחר מכן יישמר.

---

## שלב 6 — עדכן וbush שוב

ערוך את `index.html` — הוסף שורה בfooter:

```bash
nano index.html
```
> מצא את `<footer>` ושנה את הטקסט בתוכו לכל דבר שתרצה. שמור Ctrl+O → Enter → Ctrl+X

הוסף commit ודחוף:

```bash
git add index.html
git commit -m "Update footer text"
git push
```
פלט:
```
To https://github.com/USERNAME/banana_site.git
   a1b2c3d..b2c3d4e  main -> main
```

---

## בדיקה סופית

```bash
git log --oneline
```
פלט:
```
b2c3d4e Update footer text
a1b2c3d Add banana website - HTML, CSS, JS
```

כנס ל-GitHub ורענן — תראה:
```
banana_site/
├── index.html
├── style.css
└── script.js
```

---

## משימות

- [ ] צור תקייה `~/banana_site` והפוך ל-repo עם `git init`
- [ ] צור את שלושת הקבצים (`index.html`, `style.css`, `script.js`)
- [ ] הרץ `git add .` ו-`git commit -m "Add banana website"`
- [ ] צור repo חדש ב-GitHub בשם `banana_site`
- [ ] חבר עם `git remote add origin` ודחוף עם `git push -u origin main`
- [ ] ודא שהקבצים מופיעים ב-GitHub
- [ ] ערוך משהו ב-`index.html` ועשה commit ו-push נוסף

---

*LINOX LAB — Git Website | מעבדת העלאת אתר ל-GitHub*
