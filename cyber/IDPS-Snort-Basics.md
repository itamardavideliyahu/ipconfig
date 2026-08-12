# מדריך Snort — חוקי IDPS למתחילים

> כל דוגמה כוללת את החוק, פירוק שלו לחלקים, והסבר פשוט.

---

## מבנה כל חוק — פעם אחת, לתמיד

```
action  proto  src_ip  src_port  direction  dst_ip  dst_port  (options)
```

```
alert   tcp    any     any       ->         any     80        (msg:"test"; sid:1; rev:1;)
  ↑      ↑      ↑       ↑         ↑          ↑       ↑          ↑
פעולה  פרוטוקול IP מקור פורט מקור כיוון   IP יעד  פורט יעד   אפשרויות
```

| מילה | אפשרויות | משמעות |
|------|---------|--------|
| **action** | `alert` / `drop` / `pass` / `log` | מה לעשות כשהחוק מתאים |
| **proto** | `tcp` / `udp` / `icmp` / `ip` | סוג הפרוטוקול |
| **src / dst ip** | `any` / `192.168.1.1` / `192.168.1.0/24` | כתובת IP (any = כולם) |
| **src / dst port** | `any` / `80` / `!80` / `1:1024` | פורט (! = חוץ מ, : = טווח) |
| **direction** | `->` / `<>` | `->` חד-כיווני, `<>` דו-כיווני |

---

## חלק 1 — חוקים בסיסיים (פרוטוקול + פורט)

---

### דוגמה 1 — התרע על כל תעבורת TCP

```snort
alert tcp any any -> any any (
    msg:"TCP traffic detected";
    sid:1001;
    rev:1;
)
```

**פירוק:**

| חלק | ערך | משמעות |
|-----|-----|--------|
| `alert` | — | צור התראה |
| `tcp` | — | רק תעבורת TCP |
| `any any` | מקור | כל IP, כל פורט |
| `->` | — | תעבורה שהולכת לכיוון → |
| `any any` | יעד | לכל IP, לכל פורט |
| `msg:` | `"TCP traffic detected"` | הטקסט שיופיע בהתראה |
| `sid:` | `1001` | מספר זיהוי ייחודי לחוק |
| `rev:` | `1` | גרסה (1 = ראשונה) |

> **הסבר פשוט:** "התרע בכל פעם שעובר TCP כלשהו — לא משנה מאיפה ולאן."  
> זה החוק הכי רחב שיש — ישמש רק ללמידה!

---

### דוגמה 2 — התרע על גלישה לאתרים (HTTP)

```snort
alert tcp any any -> any 80 (
    msg:"HTTP web browsing detected";
    sid:1002;
    rev:1;
)
```

**פירוק:**

| חלק | ערך | משמעות |
|-----|-----|--------|
| `tcp` | — | פרוטוקול TCP |
| `any any` | מקור | כל מחשב, כל פורט |
| `any 80` | יעד | לכל IP, **לפורט 80 בלבד** |

> **הסבר פשוט:** פורט 80 = HTTP (גלישה ללא הצפנה).  
> "כל חיבור שיוצא לפורט 80 — צור התראה."

---

### דוגמה 3 — התרע על HTTPS (גלישה מוצפנת)

```snort
alert tcp any any -> any 443 (
    msg:"HTTPS traffic detected";
    sid:1003;
    rev:1;
)
```

> **הסבר פשוט:** פורט 443 = HTTPS.  
> אותו חוק כמו קודם — רק פורט שונה.

---

### דוגמה 4 — התרע על SSH (גישה מרחוק)

```snort
alert tcp any any -> any 22 (
    msg:"SSH connection attempt";
    sid:1004;
    rev:1;
)
```

> **הסבר פשוט:** פורט 22 = SSH = כניסה מרחוק לשרת.  
> כל ניסיון חיבור לפורט 22 יצור התראה.

---

### דוגמה 5 — חסום (DROP) תעבורת Telnet

```snort
drop tcp any any -> any 23 (
    msg:"Telnet blocked - insecure protocol";
    sid:1005;
    rev:1;
)
```

> **הסבר פשוט:** Telnet (פורט 23) הוא פרוטוקול גישה מרחוק **ללא הצפנה** — מסוכן.  
> `drop` = חסום את הפקטה לגמרי (לא רק התרע).

---

## חלק 2 — חוקים עם תוכן (content)

---

### דוגמה 6 — חפש מילה ספציפית ב-Payload

```snort
alert tcp any any -> any 80 (
    msg:"Suspicious keyword - attack detected";
    content:"attack";
    sid:1006;
    rev:1;
)
```

**פירוק:**

| חלק | ערך | משמעות |
|-----|-----|--------|
| `content:` | `"attack"` | חפש את המחרוזת הזו בתוך הפקטה |

> **הסבר פשוט:** `content:` אומר ל-Snort "חפש את המילה הזו בתוכן הפקטה".  
> אם הפקטה מכילה את המחרוזת "attack" — תצור התראה.

---

### דוגמה 7 — חפש שני תכנים (AND — שניהם חייבים להיות)

```snort
alert tcp any any -> any 80 (
    msg:"SQL Injection attempt";
    content:"SELECT";
    content:"FROM";
    sid:1007;
    rev:1;
)
```

> **הסבר פשוט:** שני `content:` בחוק אחד = **שניהם חייבים להופיע** בפקטה.  
> זוהי הדרך של Snort לכתוב **AND** — פשוט מכניסים תנאי אחרי תנאי.  
> "הפקטה מכילה גם SELECT **וגם** FROM" = חשד ל-SQL Injection.

---

### דוגמה 8 — חפש מחרוזת במיקום ספציפי (offset + depth)

```snort
alert tcp any any -> any 80 (
    msg:"HTTP GET request detected";
    content:"GET";
    offset:0;
    depth:3;
    sid:1008;
    rev:1;
)
```

**פירוק:**

| חלק | ערך | משמעות |
|-----|-----|--------|
| `content:` | `"GET"` | חפש את המילה GET |
| `offset:0` | `0` | התחל לחפש מ-byte **0** (תחילת ה-Payload) |
| `depth:3` | `3` | חפש רק בתוך **3 הbytes הראשונים** |

> **הסבר פשוט:** בלי offset ו-depth — Snort מחפש בכל הפקטה.  
> עם offset+depth — אנחנו אומרים לו **בדיוק איפה** לחפש.  
> "GET" חייבת להופיע ב-3 הbytes הראשונים של ה-Payload.

---

## חלק 3 — חוקים עם Regex (pcre)

---

### דוגמה 9 — חפש דפוס גמיש עם Regex

```snort
alert tcp any any -> any 80 (
    msg:"Possible virus name in traffic";
    pcre:"/[a-z]irus[0-9]/";
    sid:1009;
    rev:1;
)
```

**פירוק:**

| חלק | ערך | משמעות |
|-----|-----|--------|
| `pcre:` | `"/[a-z]irus[0-9]/"` | חפש עם ביטוי רגולרי |
| `[a-z]` | — | כל אות קטנה (a עד z) |
| `irus` | — | המחרוזת הקבועה |
| `[0-9]` | — | כל ספרה (0 עד 9) |

> **הסבר פשוט:** `pcre:` = חיפוש גמיש עם ביטויים רגולריים.  
> `/` בהתחלה ובסוף = גבולות הביטוי (חובה ב-pcre).  
> יתאים ל: `virus3`, `avirus7`, `xirus0` — לא יתאים ל: `Virus3` (V גדולה).

---

### דוגמה 10 — Regex עם כמות תווים מוגדרת

```snort
alert tcp any any -> any any (
    msg:"Password-like pattern detected";
    pcre:"/password=[a-zA-Z0-9]{8,}/";
    sid:1010;
    rev:1;
)
```

**פירוק:**

| חלק | ערך | משמעות |
|-----|-----|--------|
| `password=` | — | חיפוש המחרוזת הקבועה |
| `[a-zA-Z0-9]` | — | כל אות (גדולה/קטנה) או ספרה |
| `{8,}` | — | **לפחות 8 תווים** מהסוג הנ"ל |

> **הסבר פשוט:** `{8,}` = "8 ויותר". `{8}` = "בדיוק 8". `{4,8}` = "בין 4 ל-8".  
> החוק הזה יזהה: `password=abcd1234` ✓, `password=abc` ✗ (פחות מ-8).

---

## חלק 4 — חוקים עם דגלי TCP (flags)

---

### דוגמה 11 — זיהוי תחילת חיבור (SYN)

```snort
alert tcp any any -> any any (
    msg:"New TCP connection - SYN packet";
    flags:S;
    sid:1011;
    rev:1;
)
```

> **הסבר פשוט:** `flags:S` = S הוא SYN — הפקטה הראשונה בכל חיבור TCP.  
> אם מישהו שולח הרבה SYN מהיר = חשד ל-**SYN Flood** (מתקפת DDoS).

---

### דוגמה 12 — זיהוי SYN + ACK (שרת מאשר חיבור)

```snort
alert tcp any any -> any any (
    msg:"TCP SYN-ACK - Server responding to connection";
    flags:SA;
    sid:1012;
    rev:1;
)
```

> **הסבר פשוט:** `flags:SA` = SYN + ACK = השרת עונה "כן, אפשר להתחבר".  
> שלב 2 מתוך 3 ב-TCP Handshake.

---

### דוגמה 13 — זיהוי Port Scan (RST מהיר)

```snort
alert tcp any any -> any any (
    msg:"Possible port scan - RST flag";
    flags:R;
    threshold:type both, track by_src, count 20, seconds 5;
    sid:1013;
    rev:1;
)
```

**פירוק:**

| חלק | ערך | משמעות |
|-----|-----|--------|
| `flags:R` | — | דגל RST = "אין שירות בפורט הזה" |
| `threshold:` | — | כלל סינון לפי כמות |
| `type both` | — | ספור גם התרעות וגם פקטות |
| `track by_src` | — | עקוב לפי **IP מקור** |
| `count 20` | — | 20 פקטות |
| `seconds 5` | — | בתוך 5 שניות |

> **הסבר פשוט:** Port Scanner שולח הרבה RST בזמן קצר כי הוא סורק פורטים.  
> `threshold` = "רק אם קרה 20 פעם ב-5 שניות — אז התרע". מונע False Positives.

---

## חלק 5 — חוקים עם IP ספציפי

---

### דוגמה 14 — התרע על תעבורה מ-IP ספציפי

```snort
alert ip 192.168.1.50 any -> any any (
    msg:"Traffic from suspicious host 192.168.1.50";
    sid:1014;
    rev:1;
)
```

> **הסבר פשוט:** ה-IP שאחרי `alert ip` הוא כתובת המקור.  
> כל פקטה שיוצאת מ-192.168.1.50 — תצור התראה.

---

### דוגמה 15 — חסום סאבנט שלם

```snort
drop ip 10.0.0.0/8 any -> any any (
    msg:"Traffic from internal 10.x.x.x blocked";
    sid:1015;
    rev:1;
)
```

> **הסבר פשוט:** `/8` = כל הכתובות שמתחילות ב-10 (10.0.0.0 עד 10.255.255.255).  
> `/24` = סאבנט של 256 כתובות. `/32` = IP יחיד.

---

### דוגמה 16 — כל כתובת **חוץ מ**-IP ספציפי

```snort
alert tcp !192.168.1.1 any -> any 80 (
    msg:"HTTP from non-gateway host";
    sid:1016;
    rev:1;
)
```

> **הסבר פשוט:** `!` = NOT = "כל כתובת **חוץ מ**".  
> `!192.168.1.1` = כל IP שאינו הראוטר.

---

## חלק 6 — חוקים משולבים (AND אמיתי)

---

### דוגמה 17 — IP ספציפי + פורט + תוכן

```snort
alert tcp 192.168.1.0/24 any -> any 80 (
    msg:"Internal user accessing HTTP with keyword";
    content:"login";
    nocase;
    sid:1017;
    rev:1;
)
```

**פירוק — 3 תנאים ב-AND:**

```
תנאי 1: src IP חייב להיות ברשת 192.168.1.0/24
    AND
תנאי 2: dst Port חייב להיות 80
    AND
תנאי 3: הפקטה מכילה "login" (nocase = ללא הבדל גדול/קטן)
```

> **הסבר פשוט:** `nocase;` = לא רגיש לאותיות גדולות/קטנות.  
> `Login`, `LOGIN`, `login` — כולם יתאימו.

---

### דוגמה 18 — חתימה מלאה: IP + פורט + Regex + flow

```snort
alert tcp any any -> 10.0.0.5 8080 (
    msg:"Malware C2 communication pattern";
    flow:established,to_server;
    content:"POST";
    offset:0;
    depth:4;
    pcre:"/beacon=[0-9a-f]{16}/";
    sid:1018;
    rev:1;
)
```

**פירוק — 5 תנאים ב-AND:**

| # | תנאי | הסבר |
|---|------|------|
| 1 | `-> 10.0.0.5 8080` | לכתובת ולפורט ספציפיים |
| 2 | `flow:established,to_server` | חיבור קיים, מהלקוח לשרת |
| 3 | `content:"POST"` | הפקטה מכילה POST |
| 4 | `offset:0; depth:4` | POST חייב להיות ב-4 הbytes הראשונים |
| 5 | `pcre:"/beacon=[0-9a-f]{16}/"` | חפש beacon= ואחריו 16 תווים hex |

> **הסבר פשוט:** חוק כזה יזהה תוכנת Malware שמדברת עם שרת פיקוד (C2 Server).  
> היא שולחת POST עם beacon (קוד זיהוי של 16 תווים hex).  
> `[0-9a-f]` = תו הקסדצימלי (0-9 + a-f).

---

## טבלת עזר מהירה

### דגלי TCP ב-Snort

| אות | דגל | מתי מופיע |
|-----|-----|----------|
| `S` | SYN | פתיחת חיבור |
| `A` | ACK | אישור קבלה |
| `P` | PSH | שלח מיד |
| `F` | FIN | סגירת חיבור |
| `R` | RST | איפוס/דחייה |
| `U` | URG | דחוף |
| `SA` | SYN+ACK | שרת מאשר חיבור |
| `SP` | SYN+PSH | פתיחה + שלח מיד |

### Regex — תווים נפוצים

| ביטוי | משמעות | דוגמה |
|-------|--------|-------|
| `[a-z]` | אות קטנה | `a`, `g` |
| `[A-Z]` | אות גדולה | `A`, `G` |
| `[0-9]` | ספרה | `0`, `7` |
| `[a-zA-Z0-9]` | אות או ספרה | `a`, `Z`, `5` |
| `[a-f0-9]` | hex תו | `a`, `f`, `3` |
| `.` | כל תו | `@`, `5`, `!` |
| `{8}` | בדיוק 8 | `aaaaaaaa` |
| `{4,}` | 4 ויותר | `aaaa`, `aaaaa` |
| `{4,8}` | בין 4 ל-8 | `aaaa`..`aaaaaaaa` |
| `\d` | ספרה (קיצור) | זהה ל-`[0-9]` |
| `\w` | אות/ספרה/_ | זהה ל-`[a-zA-Z0-9_]` |

### פורטים נפוצים

| פורט | שירות |
|------|-------|
| 20/21 | FTP |
| 22 | SSH |
| 23 | Telnet |
| 25 | SMTP (דואר) |
| 53 | DNS |
| 80 | HTTP |
| 443 | HTTPS |
| 3306 | MySQL |
| 3389 | RDP |
| 8080 | HTTP חלופי |

---

## סדר בניית חוק — 5 שאלות

> לפני שכותבים חוק, ענה על 5 שאלות:

```
1. מה אני רוצה לתפוס?          ← msg:
2. איזה פרוטוקול?               ← tcp / udp / ip / icmp
3. מאיפה ולאן?                  ← src/dst IP + port
4. יש תוכן לחפש?               ← content: / pcre:
5. בדיוק איפה בפקטה?            ← offset: / depth:
```

---

> 📌 **לזכור:** כל תנאי בתוך `( )` מחובר **אוטומטית ב-AND**.  
> ככל שיש **יותר** תנאים — החוק **מדויק** יותר — ופחות False Positives.
