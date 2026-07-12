# מעבדת journalctl — צפייה בלוגים בלינוקס
### קאלי לינוקס 2026 | מתחילים

> **זמן:** ~20 דקות  
> **מה תלמד:** קריאת לוגי מערכת, חיפוש שגיאות, מעקב בזמן אמת

---

## מה זה journalctl?

כל דבר שקורה בלינוקס — כניסת משתמש, שירות שעלה, שגיאה, אתחול — **נרשם אוטומטית ביומן המערכת**.  
הפקודה `journalctl` מאפשרת לקרוא את כל היומן הזה.

```
מערכת לינוקס
    ↓
systemd (מנהל המערכת)
    ↓
journald (שומר לוגים)
    ↓
journalctl (אנחנו קוראים כאן)
```

> **למה זה חשוב?** כשמשהו לא עובד — הלוגים הם המקום הראשון לבדוק.

---

## שלב 1 — הצגת הלוגים הבסיסית ⏱ 4 דקות

### צפייה בכל הלוגים

```bash
journalctl
```

פלט לדוגמה:
```
Jul 12 18:00:01 kali systemd[1]: Started Session 1 of User root.
Jul 12 18:00:05 kali sshd[1234]: Server listening on 0.0.0.0 port 22.
Jul 12 18:01:10 kali sudo[1456]: student : TTY=pts/0 ; COMMAND=/usr/bin/apt
Jul 12 18:02:33 kali kernel: usb 1-1: new USB device found
```

> יש **הרבה** שורות — לחץ `q` לצאת, חצים לנווט, `Space` לדף הבא.

---

### הצגת הלוגים החדשים ביותר

בדרך כלל רוצים לראות מה קרה **לאחרונה**, לא מה קרה לפני שנה:

```bash
journalctl -e
```
> `-e` = **end** — קפוץ ישר לסוף היומן

---

### הגבלת מספר השורות

```bash
journalctl -n 20
```
פלט לדוגמה:
```
Jul 12 18:10:01 kali CRON[2001]: (root) CMD (command -v debian-sa1 > /dev/null)
Jul 12 18:10:05 kali systemd[1]: NetworkManager.service: Succeeded.
Jul 12 18:11:00 kali kernel: NET: Registered PF_INET6 protocol family
...
(20 שורות אחרונות)
```
> `-n 20` = הצג **20 שורות אחרונות** בלבד

---

**משימות — שלב 1:**

- [ ] הרץ `journalctl` — לחץ `q` לצאת
- [ ] הרץ `journalctl -e` — לאן זה קפץ?
- [ ] הרץ `journalctl -n 10` — ספור שהופיעו בדיוק 10 שורות

---

## שלב 2 — סינון לפי זמן ⏱ 4 דקות

### מה קרה היום?

```bash
journalctl --since today
```
פלט לדוגמה:
```
Jul 12 00:00:01 kali systemd[1]: Starting Daily apt download activities...
Jul 12 06:25:00 kali systemd[1]: Started logrotate.service.
Jul 12 18:00:05 kali sshd[1234]: Server listening on 0.0.0.0 port 22.
```

---

### מה קרה בשעה האחרונה?

```bash
journalctl --since "1 hour ago"
```

---

### טווח זמן מדויק

```bash
journalctl --since "2026-07-12 18:00" --until "2026-07-12 18:30"
```
פלט לדוגמה:
```
Jul 12 18:00:05 kali sshd[1234]: Server listening on 0.0.0.0 port 22.
Jul 12 18:01:10 kali sudo[1456]: student : COMMAND=/usr/bin/apt
Jul 12 18:02:00 kali kernel: usb 1-1: new USB device found
```

> **פורמט הזמן:** `"YYYY-MM-DD HH:MM"`

---

**משימות — שלב 2:**

- [ ] הרץ `journalctl --since today` — כמה אירועים היום?
- [ ] הרץ `journalctl --since "1 hour ago"` — מה קרה בשעה האחרונה?
- [ ] נסה טווח זמן עם `--since` ו-`--until` לפי הזמן הנוכחי

---

## שלב 3 — סינון לפי רמת חומרה ⏱ 4 דקות

### רמות חומרה בלוגים

כל לוג מקבל **רמת חומרה** — מידע רגיל ועד קריסה קריטית:

| מספר | שם | משמעות |
|------|-----|--------|
| 0 | `emerg` | המערכת לא שמישה — קריסה מוחלטת |
| 1 | `alert` | נדרשת פעולה מיידית |
| 2 | `crit` | שגיאה קריטית |
| 3 | `err` | שגיאה רגילה |
| 4 | `warning` | אזהרה — משהו לא תקין |
| 5 | `notice` | מידע חשוב |
| 6 | `info` | מידע רגיל |
| 7 | `debug` | מידע לפיתוח |

---

### הצגת שגיאות בלבד

```bash
journalctl -p err
```
פלט לדוגמה:
```
Jul 12 17:45:02 kali kernel: EXT4-fs error (device sda1): ext4_find_entry
Jul 12 17:50:11 kali NetworkManager[812]: error: connection failed
Jul 12 18:05:33 kali sshd[1234]: error: Could not load host key
```
> `-p err` = הצג רק **שגיאות** (err ומעלה בחומרה)

---

### הצגת אזהרות ושגיאות

```bash
journalctl -p warning
```
> מציג `warning`, `err`, `crit`, `alert`, `emerg` — הכל מרמה 4 ומעלה

---

### שגיאות היום בלבד

```bash
journalctl -p err --since today
```
> שילוב סינון זמן + רמת חומרה

---

**משימות — שלב 3:**

- [ ] הרץ `journalctl -p err` — יש שגיאות? מה הן?
- [ ] הרץ `journalctl -p warning --since today` — כמה אזהרות היום?
- [ ] הרץ `journalctl -p crit` — יש משהו קריטי?

---

## שלב 4 — סינון לפי שירות ⏱ 4 דקות

### מה זה `-u`?

`-u` = **unit** — הצג לוגים של שירות ספציפי בלבד.

```bash
journalctl -u ssh
```
פלט לדוגמה:
```
Jul 12 18:00:05 kali sshd[1234]: Server listening on 0.0.0.0 port 22.
Jul 12 18:00:05 kali sshd[1234]: Server listening on :: port 22.
Jul 12 18:15:33 kali sshd[1235]: Accepted password for student from 192.168.1.10
Jul 12 18:20:01 kali sshd[1236]: Failed password for root from 185.220.101.1
```

> **שים לב לשורה האחרונה** — ניסיון כניסה כושל של root מ-IP חיצוני!

---

```bash
journalctl -u NetworkManager
```
פלט לדוגמה:
```
Jul 12 17:58:00 kali NetworkManager[812]: <info> device eth0: state change: disconnected -> prepare
Jul 12 17:58:02 kali NetworkManager[812]: <info> device eth0: state change: prepare -> config
Jul 12 17:58:05 kali NetworkManager[812]: <info> device eth0: Activation: successful
```

---

### כמה שירותים ביחד

```bash
journalctl -u ssh -u sudo
```
> מציג לוגים של SSH **ו**-sudo יחד

---

### שירות + זמן + חומרה

```bash
journalctl -u ssh --since today -p err
```
> שגיאות SSH שהיו **היום בלבד**

---

**משימות — שלב 4:**

- [ ] הרץ `journalctl -u ssh` — יש ניסיונות כניסה כושלים?
- [ ] הרץ `journalctl -u NetworkManager` — מה מצב הרשת?
- [ ] הרץ `journalctl -u ssh --since today` — כמה אירועי SSH היום?

---

## שלב 5 — מעקב בזמן אמת ⏱ 4 דקות

### מה זה `-f`?

`-f` = **follow** — הצג לוגים חדשים **ברגע שהם נכתבים**.  
כמו `tail -f` — הטרמינל "מאזין" ומדפיס כל שורה חדשה.

```bash
journalctl -f
```
פלט:
```
Jul 12 18:25:00 kali systemd[1]: Started Session 5.
Jul 12 18:25:01 kali sudo[2100]: student : COMMAND=/usr/bin/ls
                                                            ← ממתין לאירועים חדשים...
```

> עצור עם **Ctrl+C**

---

### מעקב על שירות ספציפי

פתח **שני טרמינלים**:

**טרמינל 1 — הפעל מעקב:**
```bash
journalctl -f -u ssh
```

**טרמינל 2 — הפעל/עצור SSH:**
```bash
sudo systemctl restart ssh
```

**בטרמינל 1 תראה בזמן אמת:**
```
Jul 12 18:26:00 kali systemd[1]: Stopping OpenBSD Secure Shell server...
Jul 12 18:26:00 kali sshd[1234]: Received signal 15; terminating.
Jul 12 18:26:00 kali systemd[1]: ssh.service: Succeeded.
Jul 12 18:26:01 kali systemd[1]: Started OpenBSD Secure Shell server.
Jul 12 18:26:01 kali sshd[1300]: Server listening on 0.0.0.0 port 22.
```
> רואים את ה-restart קורה שורה אחרי שורה!

---

**משימות — שלב 5:**

- [ ] הרץ `journalctl -f` — המתן 30 שניות ובדוק אם מופיעות שורות חדשות
- [ ] פתח טרמינל שני, הרץ `journalctl -f -u ssh` בראשון
- [ ] הרץ `sudo systemctl restart ssh` בשני — רואה את זה קורה בזמן אמת?
- [ ] עצור עם **Ctrl+C**

---

## סיכום — הפקודות החשובות

```bash
# ── בסיסי ─────────────────────────────────────────────────
journalctl              # כל הלוגים (q לצאת)
journalctl -e           # קפוץ לסוף היומן
journalctl -n 20        # 20 שורות אחרונות

# ── לפי זמן ───────────────────────────────────────────────
journalctl --since today              # מהיום
journalctl --since "1 hour ago"       # מהשעה האחרונה
journalctl --since "2026-07-12 18:00" --until "2026-07-12 19:00"

# ── לפי חומרה ─────────────────────────────────────────────
journalctl -p err       # שגיאות בלבד
journalctl -p warning   # אזהרות ושגיאות
journalctl -p crit      # קריטי בלבד

# ── לפי שירות ─────────────────────────────────────────────
journalctl -u ssh                     # לוגי SSH
journalctl -u NetworkManager          # לוגי רשת
journalctl -u ssh -u sudo             # שני שירותים

# ── שילובים שימושיים ──────────────────────────────────────
journalctl -p err --since today       # שגיאות היום
journalctl -u ssh -p err              # שגיאות SSH
journalctl -u ssh --since today -n 20 # 20 שורות SSH מהיום

# ── זמן אמת ───────────────────────────────────────────────
journalctl -f           # מעקב כללי
journalctl -f -u ssh    # מעקב על SSH בלבד
```

---

*LINOX LAB — journalctl | מעבדת לוגים בלינוקס קאלי*
