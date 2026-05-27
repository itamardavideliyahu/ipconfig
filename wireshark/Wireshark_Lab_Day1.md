# מעבדת Wireshark - יום 1 (ניתוח תעבורת רשת למתחילים)

## רקע קצר

**Wireshark** הוא כלי ניתוח תעבורת רשת (Packet Analyzer / Sniffer) בקוד פתוח, הנפוץ ביותר בעולם.  
הוא מאפשר ל**"לראות"** את כל החבילות (Packets) שעוברות בממשק הרשת שלך — בזמן אמת או מתוך קובץ הקלטה.

| שימוש | דוגמה |
|-------|--------|
| **פתרון תקלות רשת** | למה המחשב לא מקבל IP? |
| **ניתוח אבטחה** | מה התהליך שולח לאינטרנט? |
| **הוראת פרוטוקולים** | לראות DNS, TCP, HTTP בפועל |
| **פורנזיקה** | חקירת אירוע סייבר |

המעבדה מיועדת לתלמידים **ללא ניסיון קודם** ב-Wireshark.

---

## מטרות למידה

- להתקין ולהפעיל את Wireshark ולהכיר את הממשק.
- להבין מה זה Packet ואיך לקרוא אותו (שכבות OSI בפועל).
- לצלם תעבורה חיה ולשמור קובץ `pcap`.
- לזהות פרוטוקולים עיקריים: **ARP, ICMP, DNS, TCP, HTTP, HTTPS**.
- לכתוב פילטרים בסיסיים ומתקדמים (Display Filters).
- לבצע ניתוח עצמאי של תרחיש גלישה רגיל.

---

## דרישות מוקדמות

- מחשב Windows 10/11 (או Linux/Mac).
- Wireshark מותקן — הורדה: [https://www.wireshark.org/download.html](https://www.wireshark.org/download.html)
- הרשאות **מנהל (Admin)** — נדרשות לצילום תעבורה.
- חיבור רשת פעיל (Wi-Fi או Ethernet).

> **הערה:** בהתקנה ב-Windows — יש לאשר את התקנת **Npcap** (נהג הצילום). לסמן את כל ברירות המחדל.

---

## חוקי מעבדה

1. מצלמים תעבורה **על המחשב שלכם בלבד** — לא על רשת זרה.
2. אחרי כל שלב — צילום מסך של הפקודות/פילטר והתוצאה.
3. לא מעתיקים פתרון בלי לכתוב מה כל פילטר עושה.
4. אם Wireshark לא מציג חבילות — לבדוק שנבחר הממשק הנכון.

---

## הכנה ראשונית — היכרות עם הממשק (10 דקות)

פתחו Wireshark. הממשק מחולק לשלושה אזורים עיקריים:

```
┌─────────────────────────────────────────────────────────┐
│  Filter Bar  ← כאן כותבים פילטרים לסינון תצוגה         │
├─────────────────────────────────────────────────────────┤
│  Packet List (למעלה) ← רשימת כל החבילות               │
│  No. │ Time │ Source │ Destination │ Protocol │ Info    │
├─────────────────────────────────────────────────────────┤
│  Packet Details (באמצע) ← פירוט שכבות OSI לחבילה נבחרת│
│  ▼ Frame (Physical)                                     │
│  ▼ Ethernet II (Data Link / Layer 2)                   │
│  ▼ Internet Protocol (Network / Layer 3)                │
│  ▼ TCP / UDP (Transport / Layer 4)                      │
│  ▼ HTTP / DNS / ... (Application / Layer 7)             │
├─────────────────────────────────────────────────────────┤
│  Packet Bytes (למטה) ← תצוגת HEX + ASCII של החבילה    │
└─────────────────────────────────────────────────────────┘
```

**עמודות ב-Packet List:**

| עמודה | משמעות |
|-------|--------|
| **No.** | מספר סידורי של החבילה בהקלטה |
| **Time** | זמן יחסי מתחילת ההקלטה (בשניות) |
| **Source** | כתובת IP / MAC של השולח |
| **Destination** | כתובת IP / MAC של היעד |
| **Protocol** | הפרוטוקול הגבוה ביותר שזוהה |
| **Info** | תיאור תוכן החבילה |

---

## שלב 1 — בחירת ממשק רשת והתחלת הקלטה (5 דקות)

1. פתחו Wireshark.
2. במסך הפתיחה תראו רשימת **ממשקי רשת** (Interfaces).
3. בחרו את הממשק הפעיל שלכם:
   - Wi-Fi (אם אתם על אלחוטי)
   - Ethernet (אם אתם על כבל)
   - ניתן לזהות לפי **גרף הפעילות** שזזים בזמן אמת

4. לחצו עליו פעמיים (או כפתור **Shark Fin** הכחול) כדי להתחיל הקלטה.

> **אם אין גרף פעילות:** ממשק לא פעיל — בחרו אחר.  
> **כדי לעצור הקלטה:** לחצו על כפתור ה-**Stop** האדום (מרובע).

---

## שלב 2 — פרוטוקולים עיקריים — מה לחפש ואיך לקרוא

### 🔷 ARP — Address Resolution Protocol

**מה זה?** פרוטוקול Layer 2 שממפה בין **IP לכתובת MAC**.

**מתי מופיע?** בכל פעם שמחשב רוצה לתקשר עם מכשיר חדש ברשת — הוא שואל:  
*"מי מחזיק את ה-IP 192.168.1.1? תגיד לי את ה-MAC שלך!"*

**דוגמה לחבילת ARP בWireshark:**

```
No.  │ Source          │ Destination     │ Protocol │ Info
-----|-----------------|-----------------|----------|-------------------------------
1    │ aa:bb:cc:dd:ee  │ Broadcast       │ ARP      │ Who has 192.168.1.1? Tell 192.168.1.10
2    │ 00:11:22:33:44  │ aa:bb:cc:dd:ee  │ ARP      │ 192.168.1.1 is at 00:11:22:33:44
```

**לחיצה על החבילה תגלה:**

```
▼ Address Resolution Protocol (request)
    Hardware type: Ethernet (1)
    Protocol type: IPv4 (0x0800)
    Sender MAC address: aa:bb:cc:dd:ee:ff (PC-1)
    Sender IP address:  192.168.1.10
    Target MAC address: 00:00:00:00:00:00  ← עדיין לא ידוע
    Target IP address:  192.168.1.1
```

**פילטר:**
```
arp
```

---

### 🔷 ICMP — Internet Control Message Protocol

**מה זה?** פרוטוקול Layer 3 המשמש לבדיקת קישוריות — הוא הבסיס לפקודת `ping`.

**מתי מופיע?** כאשר מריצים `ping`, מכשיר לא נגיש, TTL פג, וכדומה.

**הרצת ping לבדיקה:**

```bat
ping 8.8.8.8
```

**דוגמה לחבילות ICMP ב-Wireshark:**

```
No.  │ Source        │ Destination   │ Protocol │ Info
-----|---------------|---------------|----------|-----------------------------
10   │ 192.168.1.10  │ 8.8.8.8       │ ICMP     │ Echo (ping) request  id=1, seq=1
11   │ 8.8.8.8       │ 192.168.1.10  │ ICMP     │ Echo (ping) reply    id=1, seq=1
12   │ 192.168.1.10  │ 8.8.8.8       │ ICMP     │ Echo (ping) request  id=1, seq=2
13   │ 8.8.8.8       │ 192.168.1.10  │ ICMP     │ Echo (ping) reply    id=1, seq=2
```

**שימו לב:** זוגות של **request / reply** — כל ping שולח בקשה ומקבל תשובה.

**פילטרים:**
```
icmp
icmp.type == 8      ← רק בקשות (Echo Request)
icmp.type == 0      ← רק תשובות (Echo Reply)
```

---

### 🔷 DNS — Domain Name System

**מה זה?** פרוטוקול Layer 7 שמתרגם שמות דומיין (`google.com`) לכתובות IP.

**מתי מופיע?** בכל גלישה לאתר — **לפני** כל חיבור TCP/HTTP.

**הרצת שאילתת DNS:**

```bat
nslookup google.com
```

**דוגמה לחבילות DNS ב-Wireshark:**

```
No.  │ Source        │ Destination   │ Protocol │ Info
-----|---------------|---------------|----------|---------------------------------------
20   │ 192.168.1.10  │ 8.8.8.8       │ DNS      │ Standard query  A google.com
21   │ 8.8.8.8       │ 192.168.1.10  │ DNS      │ Standard query response A 142.250.185.78
```

**לחיצה על תשובת DNS תגלה:**

```
▼ Domain Name System (response)
    Transaction ID: 0x1234
    Flags: Standard query response
    Questions: 1
    Answer RRs: 1
    ▼ Answers
        google.com: type A, class IN, addr 142.250.185.78
        Time to live: 300 seconds
```

**פילטרים:**
```
dns
dns.qry.name == "google.com"       ← שאילתה ספציפית
dns.flags.response == 1            ← רק תשובות DNS
dns.flags.response == 0            ← רק שאילתות DNS
```

---

### 🔷 TCP — Transmission Control Protocol

**מה זה?** פרוטוקול Layer 4 אמין — מבטיח שהנתונים יגיעו **בסדר ובשלמות**.

**תהליך TCP Handshake (3-Way Handshake):**

```
PC-1 (Client)          Server (google.com)
     │                        │
     │ ── SYN ──────────────► │   שלב 1: "רוצה להתחבר"
     │                        │
     │ ◄─────────── SYN-ACK ─ │   שלב 2: "אשרתי, גם אני רוצה"
     │                        │
     │ ── ACK ──────────────► │   שלב 3: "מצוין, נתחבר"
     │                        │
     │ ═══ חיבור פתוח ════════ │   כעת ניתן לשלוח נתונים
```

**דוגמה ב-Wireshark:**

```
No.  │ Source        │ Destination   │ Protocol │ Info
-----|---------------|---------------|----------|--------------------------------
30   │ 192.168.1.10  │ 142.250.185.78│ TCP      │ 54321 → 443 [SYN] Seq=0
31   │ 142.250.185.78│ 192.168.1.10  │ TCP      │ 443 → 54321 [SYN, ACK] Seq=0
32   │ 192.168.1.10  │ 142.250.185.78│ TCP      │ 54321 → 443 [ACK] Seq=1
```

**פילטרים:**
```
tcp
tcp.port == 443                    ← HTTPS
tcp.port == 80                     ← HTTP
tcp.flags.syn == 1                 ← רק SYN
tcp.flags.syn == 1 and tcp.flags.ack == 0   ← רק SYN ראשון (לא SYN-ACK)
tcp.analysis.retransmission        ← שידורים חוזרים (בעיה ברשת!)
```

---

### 🔷 HTTP — HyperText Transfer Protocol

**מה זה?** פרוטוקול Layer 7 — התקשורת של גלישה לאתרים **ללא הצפנה** (פורט 80).

> **שימו לב:** רוב האתרים כיום משתמשים ב-**HTTPS** (פורט 443) שמוצפן. HTTP ברור נמצא בעיקר בסביבות מעבדה ורשתות ישנות.

**דוגמה לבקשת HTTP GET:**

```
No.  │ Source        │ Destination   │ Protocol │ Info
-----|---------------|---------------|----------|-----------------------------
50   │ 192.168.1.10  │ 93.184.216.34 │ HTTP     │ GET /index.html HTTP/1.1
51   │ 93.184.216.34 │ 192.168.1.10  │ HTTP     │ HTTP/1.1 200 OK (text/html)
```

**לחיצה על בקשת GET תגלה:**

```
▼ Hypertext Transfer Protocol
    GET /index.html HTTP/1.1\r\n
    Host: example.com\r\n
    User-Agent: Mozilla/5.0 ...\r\n
    Accept: text/html,...\r\n
    Cookie: session=abc123\r\n    ← ⚠️ נראה בטקסט ברור!
```

**פילטרים:**
```
http
http.request.method == "GET"
http.request.method == "POST"
http.response.code == 200          ← בקשות מוצלחות
http.response.code == 404          ← דפים לא נמצאו
http contains "password"           ← ⚠️ לדוגמה בלבד!
```

---

### 🔷 HTTPS / TLS — תעבורה מוצפנת

**מה זה?** HTTP עם שכבת הצפנה TLS/SSL — **לא ניתן לקרוא את התוכן** ב-Wireshark.

**מה כן ניתן לראות:**
- ה-IP של השרת
- **SNI** — שם הדומיין (Server Name Indication) בתחילת ה-Handshake
- גרסת TLS
- אורך החבילות (כמות הנתונים)

**דוגמה ב-Wireshark:**

```
No.  │ Source        │ Destination   │ Protocol │ Info
-----|---------------|---------------|----------|-----------------------------------
60   │ 192.168.1.10  │ 142.250.185.78│ TLSv1.3  │ Client Hello
61   │ 142.250.185.78│ 192.168.1.10  │ TLSv1.3  │ Server Hello, Certificate
62   │ 192.168.1.10  │ 142.250.185.78│ TLSv1.3  │ Change Cipher Spec
63   │ 142.250.185.78│ 192.168.1.10  │ TLSv1.3  │ Application Data (מוצפן)
```

**פילטרים:**
```
tls
tls.handshake.type == 1            ← Client Hello
tls.handshake.extensions_server_name   ← SNI (שם הדומיין)
```

---

## שלב 3 — פילטרים: מדריך מלא

### Display Filters — פילטרי תצוגה

פילטרי **תצוגה** אינם משפיעים על ההקלטה — הם רק מסננים מה מוצג על המסך.  
כותבים אותם ב-**Filter Bar** שבראש המסך.

> **טיפ:** Wireshark מציע **השלמה אוטומטית** — לחצו `Tab` לאחר כתיבת חלק מהפילטר.

---

### 🟢 פילטרים בסיסיים — לפי פרוטוקול

```wireshark
arp
icmp
dns
tcp
udp
http
tls
dhcp
```

---

### 🟡 פילטרים לפי כתובת IP

```wireshark
ip.addr == 192.168.1.10            ← כל תעבורה מ/אל כתובת זו
ip.src == 192.168.1.10             ← רק תעבורה שיוצאת מהכתובת
ip.dst == 8.8.8.8                  ← רק תעבורה שהולכת לכתובת
ip.addr == 192.168.1.0/24          ← כל הרשת 192.168.1.x
! ip.addr == 192.168.1.1           ← הכל חוץ מהראוטר
```

---

### 🟡 פילטרים לפי פורט

```wireshark
tcp.port == 80                     ← HTTP
tcp.port == 443                    ← HTTPS
tcp.port == 22                     ← SSH
tcp.port == 3389                   ← RDP (שולחן עבודה מרוחק)
udp.port == 53                     ← DNS
udp.port == 67 or udp.port == 68   ← DHCP
```

---

### 🟠 פילטרים מתקדמים — שילוב תנאים

```wireshark
ip.src == 192.168.1.10 and tcp.port == 443
ip.addr == 8.8.8.8 or ip.addr == 1.1.1.1
tcp and !http
dns and ip.dst == 8.8.8.8
ip.src == 192.168.1.10 and (tcp.port == 80 or tcp.port == 443)
```

---

### 🔴 פילטרים מתקדמים — ניתוח תוכן

```wireshark
frame contains "google"            ← חפש מחרוזת בכל החבילה
http.host contains "google"        ← שם שרת HTTP מכיל "google"
dns.qry.name contains "facebook"   ← שאילתת DNS לפייסבוק
tcp.len > 1000                     ← חבילות TCP גדולות מ-1000 בייט
ip.ttl < 10                        ← חבילות שה-TTL שלהן נמוך (קרובות לפקיעה)
tcp.analysis.retransmission        ← בעיות רשת — שידורים חוזרים
```

---

### טבלת אופרטורים

| אופרטור | משמעות | דוגמה |
|---------|--------|--------|
| `==` | שווה ל | `ip.src == 10.0.0.1` |
| `!=` | לא שווה ל | `tcp.port != 80` |
| `>` / `<` | גדול / קטן | `tcp.len > 500` |
| `and` | גם וגם | `dns and ip.dst == 8.8.8.8` |
| `or` | אחד מהם | `tcp.port == 80 or tcp.port == 443` |
| `!` / `not` | שלילה | `!arp` |
| `contains` | מכיל מחרוזת | `http.host contains "google"` |
| `matches` | תואם Regex | `dns.qry.name matches "\.il$"` |

---

## שלב 4 — תרגיל מודרך: ניתוח גלישה לאתר

### הוראות

1. פתחו Wireshark והתחילו הקלטה על ממשק הרשת הפעיל.
2. פתחו **Command Prompt** ובצעו:

```bat
nslookup example.com
ping example.com -n 2
```

3. פתחו דפדפן וגלשו ל: `http://example.com` (HTTP — לא HTTPS).
4. עצרו את ההקלטה.
5. שמרו: `File → Save As → lab_example.pcap`

---

### ניתוח השלב — שאלות לתשובה

**חלק א — ARP:**

```wireshark
arp
```

- כמה חבילות ARP יש בהקלטה?
- מי שאל ועל מי?
- מהי כתובת ה-MAC שהוחזרה?

---

**חלק ב — DNS:**

```wireshark
dns.qry.name == "example.com"
```

- מה ה-IP שהוחזר עבור `example.com`?
- כמה שניות ה-TTL של הרשומה?
- באיזה פורט עובד DNS? (בדקו בעמודת Info)

---

**חלק ג — TCP Handshake:**

```wireshark
tcp.flags.syn == 1 and ip.dst == 93.184.216.34
```

(החליפו את ה-IP בזה שקיבלתם מה-DNS)

- זיהו את שלושת חבילות ה-Handshake: SYN, SYN-ACK, ACK.
- מה מספר הפורט של הלקוח (Source Port)?
- מה מספר הפורט של השרת (Destination Port)?

---

**חלק ד — HTTP:**

```wireshark
http
```

- מצאו את בקשת ה-GET. מה כתוב בשדה `Host`?
- מה קוד התגובה (Response Code) שהשרת החזיר?
- האם ניתן לראות את תוכן ה-HTML? כיצד?

> **להצגת תוכן HTTP:** לחץ ימני על חבילה → *Follow → TCP Stream*

---

## שלב 5 — תרגיל עצמאי: ניתוח תעבורת DHCP

**רקע:** DHCP הוא הפרוטוקול שמחלק IP אוטומטית. תהליך ה-DORA:

```
Client                              DHCP Server (Router)
  │                                       │
  │ ── DHCP Discover (Broadcast) ───────► │  "מישהו פה? צריך IP"
  │                                       │
  │ ◄─────────────────── DHCP Offer ───── │  "קח IP: 192.168.1.25"
  │                                       │
  │ ── DHCP Request ────────────────────► │  "אני לוקח את .25"
  │                                       │
  │ ◄───────────────── DHCP ACK ───────── │  "מאושר! תוקף: 24 שעות"
```

**ביצוע (CMD כמנהל):**

```bat
ipconfig /release
ipconfig /renew
```

**פילטר:**
```wireshark
dhcp
```

**שאלות:**
1. זיהו את 4 שלבי DORA בהקלטה.
2. מה ה-IP שהוצע (DHCP Offer)?
3. כמה זמן תוקף (Lease Time) ניתן לכתובת?
4. מה כתובת ה-DNS שהראוטר שלח יחד עם ה-IP?

---

## שלב 6 — Follow Stream: קריאת שיחה מלאה

Wireshark מאפשר לעקוב אחרי **חיחוי (Stream) מלאה** בין שני מכשירים.

### TCP Stream

1. לחצו ימני על חבילת HTTP כלשהי.
2. בחרו: `Follow → TCP Stream`
3. יפתח חלון שמציג **את כל השיחה** בין הלקוח לשרת.

**מה תראו:**

```
GET /index.html HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0 ...
Accept: text/html

HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Length: 1256

<!doctype html>
<html>
<head><title>Example Domain</title>
...
```

### UDP Stream — DNS

1. לחצו ימני על חבילת DNS.
2. בחרו: `Follow → UDP Stream`
3. תראו את השאילתה והתשובה בבינארי/טקסט.

---

## שלב 7 — Statistics: סטטיסטיקות ותצוגת Overview

Wireshark מציע כלי סטטיסטיקה עוצמתיים:

### Protocol Hierarchy

`Statistics → Protocol Hierarchy`

מציג **אחוז** מכל פרוטוקול בהקלטה:

```
Protocol          │ Packets │ %Packets │ Bytes   │ %Bytes
──────────────────┼─────────┼──────────┼─────────┼────────
Ethernet          │  1,234  │  100.0%  │ 987,654 │ 100.0%
  IPv4            │  1,200  │   97.2%  │ 965,000 │  97.7%
    TCP           │  1,050  │   85.1%  │ 890,000 │  90.1%
      TLS         │    800  │   64.8%  │ 780,000 │  79.0%
      HTTP        │    100  │    8.1%  │  50,000 │   5.1%
    UDP           │    150  │   12.2%  │  75,000 │   7.6%
      DNS         │    100  │    8.1%  │  25,000 │   2.5%
  ARP             │     34  │    2.8%  │  22,654 │   2.3%
```

---

### Conversations

`Statistics → Conversations → IPv4`

מציג את רשימת ה**שיחות** (מי דיבר עם מי) ממוינת לפי כמות נתונים.

> שימושי לגילוי מחשב שמעביר כמות גדולה חריגה של נתונים.

---

### IO Graphs

`Statistics → IO Graph`

גרף של **קצב התעבורה** לאורך הזמן — שימושי לזיהוי פיקים ונפילות.

---

## שלב 8 — Capture Filters: פילטרים בזמן הקלטה

בניגוד ל-Display Filters, **Capture Filters** מוגדרים **לפני תחילת ההקלטה** וחוסכים מקום.

הם כתובים בתחביר **BPF** (Berkeley Packet Filter) — שונה מעט מ-Display Filters.

```
ממשק הרשת → Edit → Capture Filters → New
```

**דוגמאות:**

```bpf
host 192.168.1.10          ← רק תעבורה מ/אל כתובת זו
port 80                    ← רק פורט 80
port 80 or port 443        ← HTTP ו-HTTPS
not port 53                ← הכל חוץ מ-DNS
net 192.168.1.0/24         ← רק הרשת הפנימית
icmp                       ← רק ping
tcp and host 8.8.8.8       ← TCP בלבד מ/אל 8.8.8.8
```

> **בקצרה:** Capture Filter = מה **לצלם**. Display Filter = מה **להציג** מתוך מה שצולם.

---

## סיכום — טבלת פרוטוקולים

| פרוטוקול | שכבה | פורט | מה הוא עושה | פילטר מהיר |
|----------|------|------|-------------|------------|
| **ARP** | Layer 2 | — | IP → MAC | `arp` |
| **ICMP** | Layer 3 | — | Ping / שגיאות | `icmp` |
| **DNS** | Layer 7 | UDP 53 | שם → IP | `dns` |
| **DHCP** | Layer 7 | UDP 67/68 | חלוקת IP | `dhcp` |
| **TCP** | Layer 4 | — | חיבור אמין | `tcp` |
| **UDP** | Layer 4 | — | חיבור מהיר | `udp` |
| **HTTP** | Layer 7 | TCP 80 | גלישה ללא הצפנה | `http` |
| **HTTPS/TLS** | Layer 7 | TCP 443 | גלישה מוצפנת | `tls` |
| **SSH** | Layer 7 | TCP 22 | שליטה מרחוק מוצפנת | `tcp.port == 22` |
| **RDP** | Layer 7 | TCP 3389 | שולחן עבודה מרוחק | `tcp.port == 3389` |

---

## ✅ בדיקה עצמית — שאלות לתלמידים

1. מה ההבדל בין **Capture Filter** ל-**Display Filter**?
2. איזה פרוטוקול ב-Layer 2 מתרגם IP ל-MAC?
3. פתחתם Wireshark וראיתם הרבה חבילות **TLS** — מה זה אומר?
4. כתבו פילטר שמציג **רק DNS ל-8.8.8.8**.
5. אתם רואים הרבה חבילות `tcp.analysis.retransmission` — מה זה מעיד?
6. מה רואים ב-`Follow → TCP Stream` שלא ניתן לראות ישירות ב-Packet List?
7. מה ההבדל בין `ip.src` ל-`ip.addr`?

<details>
<summary>📋 תשובות (למדריך)</summary>

1. Capture Filter = מגדיר מה **יוקלט** (לפני הקלטה, BPF). Display Filter = מסנן מה **מוצג** (בזמן ריאל, מתוך מה שכבר הוקלט)
2. **ARP**
3. רוב התעבורה מוצפנת (HTTPS) — לא ניתן לקרוא תוכן, אבל ניתן לראות שמות דומיינים ב-SNI
4. `dns and ip.dst == 8.8.8.8`
5. ישנן בעיות ברשת — חבילות הולכות לאיבוד ושולחות שוב (ייתכן עומס, כבל פגום וכו')
6. את **כל השיחה** בין שני הצדדים — בקשה + תשובה מלאה + תוכן HTML/נתונים
7. `ip.src` = רק כתובת **מקור**. `ip.addr` = מקור **או** יעד (כל מי שמעורב)

</details>

---

## 🔧 טיפים ומקשי קיצור שימושיים

| פעולה | מקש / תפריט |
|-------|-------------|
| התחלת הקלטה | `Ctrl + E` |
| עצירת הקלטה | `Ctrl + E` (שוב) |
| שמירת קובץ | `Ctrl + S` |
| פתיחת קובץ pcap | `Ctrl + O` |
| ניקוי הקלטה | `Ctrl + Shift + X` |
| חיפוש חבילה | `Ctrl + F` |
| Go to Packet | `Ctrl + G` |
| Colorize — צביעת כללים | `View → Coloring Rules` |
| Mark Packet (סימון) | `Ctrl + M` |
| Export כ-CSV | `File → Export Packet Dissections → As CSV` |

---

## 📚 קישורים למסמכים נוספים בפרויקט

- [יסודות הרשת — IP, DNS, DHCP, Gateway](../network-basics.md)
- [Router ו-Switch — ניתוב ותעבורה](../network/router-and-switch.md)

---

> **למדריך/ה:** מומלץ לפתוח Wireshark על המסך המרכזי בכיתה ולהריץ `ping google.com` בזמן שהתלמידים צופים בחבילות בזמן אמת. כל פרוטוקול — הרצה, עצירה, הסבר. ה"וואו מומנט" הגדול הוא כשהתלמיד רואה בעצמו את ה-DNS query ואז מיד את ה-TCP Handshake — "זה בדיוק מה שלמדנו בשיעור, וזה קורה עכשיו על המחשב שלי!"
