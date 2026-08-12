# פריסת IDPS Simulation על AWS EC2

> זמן משוער: 15 דקות | עלות: Free Tier (t2.micro)

---

## שלב 1 — הפעל מכונת EC2

### ב-AWS Console:

1. פתח **EC2 → Launch Instance**
2. הגדרות:

| שדה | ערך |
|-----|-----|
| **Name** | `idps-simulation` |
| **AMI** | Ubuntu Server 24.04 LTS (Free tier eligible) |
| **Instance type** | `t2.micro` |
| **Key pair** | צור חדש או השתמש בקיים → שמור את קובץ ה-`.pem` |
| **Network** | VPC ברירת מחדל |

3. **Security Group** — הוסף את החוקים הבאים:

| Type | Port | Source | מטרה |
|------|------|--------|------|
| SSH | 22 | My IP | גישה לניהול |
| Custom TCP | 8080 | 0.0.0.0/0 | גישת תלמידים לאפליקציה |

4. לחץ **Launch Instance** → המתן דקה

---

## שלב 2 — התחבר למכונה

```bash
# Windows PowerShell / Mac Terminal
ssh -i "your-key.pem" ubuntu@<EC2-PUBLIC-IP>
```

> את ה-Public IP תמצא ב: EC2 → Instances → עמודת Public IPv4 address

---

## שלב 3 — התקן Docker

```bash
# עדכון חבילות
sudo apt update && sudo apt upgrade -y

# התקנת Docker
curl -fsSL https://get.docker.com | sudo sh

# הוסף את המשתמש לקבוצת docker (כדי לא לרשום sudo בכל פעם)
sudo usermod -aG docker ubuntu

# הפעל מחדש את ה-session
exit
```

התחבר שוב:
```bash
ssh -i "your-key.pem" ubuntu@<EC2-PUBLIC-IP>
```

---

## שלב 4 — העלה את הקוד

### אפשרות א — Clone מ-GitHub (מומלץ):
```bash
git clone https://github.com/itamardavideliyahu/ipconfig.git
cd ipconfig/cyber/idps-docker
```

### אפשרות ב — העתק ידני עם SCP:
```bash
# מהמחשב שלך (לא מה-EC2)
scp -i "your-key.pem" -r "cyber/idps-docker/" ubuntu@<EC2-PUBLIC-IP>:~/idps-docker
```
```bash
# חזור ל-EC2
cd ~/idps-docker
```

---

## שלב 5 — בנה והרץ

```bash
# בנה את ה-Docker image
docker build -t idps-simulation .

# הרץ את הקונטיינר
docker run -d \
  --name idps-sim \
  --restart unless-stopped \
  -p 8080:8080 \
  idps-simulation

# בדוק שהקונטיינר רץ
docker ps
```

**פלט צפוי:**
```
CONTAINER ID   IMAGE              STATUS          PORTS
abc123def456   idps-simulation    Up 2 seconds    0.0.0.0:8080->8080/tcp
```

---

## שלב 6 — בדיקה

```bash
# בדיקה מהשרת עצמו
curl http://localhost:8080/health
# צפוי: {"rules": 6, "status": "ok"}
```

**פתח בדפדפן:**
```
http://<EC2-PUBLIC-IP>:8080
```

שתף עם התלמידים רק את הכתובת הזו!

---

## פקודות שימושיות לניהול

```bash
# הצג לוגים בזמן אמת
docker logs -f idps-sim

# עצור
docker stop idps-sim

# הפעל מחדש
docker start idps-sim

# עדכון לגרסה חדשה של הקוד
docker stop idps-sim
docker rm idps-sim
docker build -t idps-simulation .
docker run -d --name idps-sim --restart unless-stopped -p 8080:8080 idps-simulation
```

---

## אפשרות מהירה — Docker Compose

```bash
# במקום docker build + docker run
docker compose up -d

# עצירה
docker compose down
```

---

## עלויות AWS

| רכיב | פרטים | עלות |
|------|--------|------|
| EC2 t2.micro | 750 שעות/חודש Free Tier | **$0** |
| Storage (8 GB) | Free Tier | **$0** |
| Data Transfer | עד 100 GB/חודש | **$0** |

> **הערה:** Free Tier תקף לשנה הראשונה. לאחר מכן ~$8/חודש.  
> **כיבוי בסוף הקורס:** Stop (לא Terminate) שומר את הנתונים.

---

## פתרון בעיות נפוצות

| בעיה | פתרון |
|------|--------|
| לא מגיעים לפורט 8080 | בדוק Security Group — האם פורט 8080 פתוח? |
| `docker: command not found` | הרץ שוב `curl -fsSL https://get.docker.com | sudo sh` |
| `Permission denied` | הוסף `sudo` לפני הפקודה |
| קונטיינר נופל | בדוק `docker logs idps-sim` |
| EC2 לא עולה | בדוק שה-Key Pair נבחר ושה-AMI נכון |
