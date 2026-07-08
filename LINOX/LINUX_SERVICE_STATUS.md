# סטאטוסים של שירותים בלינוקס
### systemctl status — מדריך מהיר

> לבדיקת סטאטוס שירות: `systemctl status <שם-שירות>`  
> לדוגמה: `systemctl status ssh`

---

## סטאטוס ראשי (Active State)

| סטאטוס | צבע | משמעות | דוגמה |
|--------|-----|---------|-------|
| `active (running)` | ירוק | השירות **פועל כרגע** ורץ ברקע | `apache2`, `ssh` |
| `active (exited)` | ירוק | השירות **רץ בהצלחה וסיים** (לא תהליך מתמשך) | `iptables`, `networking` |
| `active (waiting)` | ירוק | השירות **פועל וממתין** לאירוע | `udev` |
| `inactive (dead)` | לבן/אפור | השירות **כבוי** — לא רץ כרגע | שירות שעצר |
| `failed` | אדום | השירות **נכשל** בהפעלה או קרס | שגיאה בקוד/הגדרות |
| `activating` | צהוב | השירות **בתהליך הפעלה** כרגע | רגע אחרי `start` |
| `deactivating` | צהוב | השירות **בתהליך כיבוי** כרגע | רגע אחרי `stop` |
| `reloading` | צהוב | השירות **מרענן הגדרות** ללא הפעלה מחדש | אחרי `reload` |

---

## סטאטוס הפעלה אוטומטית (Unit File State)

| סטאטוס | משמעות | פעולה |
|--------|---------|-------|
| `enabled` | **יופעל אוטומטית** בכל אתחול | `systemctl enable <שירות>` |
| `disabled` | **לא יופעל** אוטומטית באתחול | `systemctl disable <שירות>` |
| `masked` | **חסום לחלוטין** — לא ניתן להפעיל בשום דרך | `systemctl mask <שירות>` |
| `static` | **לא ניתן להפעיל/כבות ישירות** — תלוי בשירות אחר | שירות עזר |
| `alias` | **שם חלופי** לשירות אחר | — |
| `not-found` | **לא קיים** במערכת | שם שגוי / לא מותקן |
| `indirect` | מופעל דרך שירות אחר | — |

---

## פקודות שימושיות

| פקודה | מה היא עושה |
|-------|------------|
| `systemctl status <שירות>` | הצג סטאטוס מלא |
| `systemctl start <שירות>` | הפעל שירות |
| `systemctl stop <שירות>` | עצור שירות |
| `systemctl restart <שירות>` | הפעל מחדש |
| `systemctl reload <שירות>` | רענן הגדרות בלבד |
| `systemctl enable <שירות>` | הפעל אוטומטית באתחול |
| `systemctl disable <שירות>` | בטל הפעלה אוטומטית |
| `systemctl is-active <שירות>` | בדוק אם פעיל (active/inactive) |
| `systemctl is-enabled <שירות>` | בדוק אם מופעל באתחול |
| `systemctl list-units --type=service` | רשימת כל השירותים |
| `systemctl list-units --state=failed` | רק שירותים שנכשלו |

---

## איך נראה הפלט

```
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/lib/systemd/system/ssh.service; enabled; vendor preset: enabled)
     Active: active (running) since Tue 2024-07-08 10:00:00 IDT; 2h ago
   Main PID: 1234 (sshd)
      Tasks: 1 (limit: 4915)
     Memory: 2.3M
        CPU: 45ms
     CGroup: /system.slice/ssh.service
             └─1234 "sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups"
```

| שורה | משמעות |
|------|--------|
| `Loaded` | איפה קובץ ההגדרות ומה הגדרת ה-boot |
| `Active` | הסטאטוס הנוכחי + כמה זמן רץ |
| `Main PID` | ה-PID של התהליך הראשי |
| `Memory` | צריכת זיכרון |
| `CGroup` | תהליכים השייכים לשירות |

---

*LINOX — Service Status Reference*
