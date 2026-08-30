# הדגמת Reverse Shell על אובונטו — למטרות לימוד/פנטסט מורשה בלבד

> אזהרה חשובה: התוכן כאן מיועד רק להרצה במעבדה מבודדת (VM-ים שבבעלותך,
> ברשת host-only/NAT ללא גישה לאינטרנט/רשת ייצור), לצורך הבנת המתודולוגיה
> וללימוד הגנה (Blue Team). אין להריץ נגד מערכת שאינה בבעלותך או שלא קיבלת
> אישור כתוב מפורש לבחון אותה. שימוש לא מורשה בטכניקות אלו הוא עבירה פלילית
> בישראל (חוק המחשבים) ובמדינות רבות אחרות.

## מה זה מדגים

תרחיש קלאסי בפנטסט: אפליקציית Flask פגיעה (Command Injection מכוון, לצורך
הדגמה) על מכונת ה"קורבן" (Ubuntu), אותה תוקף מנצל כדי לקבל Reverse Shell
חזרה למכונת ה"תוקף" (Ubuntu נוספת/אותה מכונה).

attacker/listener.sh      -> מאזין netcat בצד התוקף (מקבל את החיבור החוזר)
victim/vulnerable_app.py  -> אפליקציית Flask עם חור Command Injection מכוון
exploit/exploit.sh        -> שולח payload שמפעיל reverse shell מהקורבן לתוקף

## מבנה המעבדה המומלץ

1. שתי מכונות Ubuntu (למשל VirtualBox/VMware/Proxmox), על רשת host-only
   בלבד (בלי NAT/גישה החוצה):
   - Attacker VM — לדוגמה 192.168.56.10
   - Victim VM — לדוגמה 192.168.56.20
2. אין להריץ את זה על מכונה עם גישה לאינטרנט או ברשת משותפת עם אנשים אחרים.

## שלב 1 — הכנת ה"קורבן" (Victim VM)

sudo apt update
sudo apt install -y python3-pip
pip3 install -r victim/requirements.txt
python3 victim/vulnerable_app.py

האפליקציה עולה על פורט 5000 ומדמה טופס "ping" שמריץ פקודת ping על הפרמטר
שהמשתמש שולח — בלי סניטציה. זהו באג נפוץ ואמיתי (OWASP: Command Injection).

## שלב 2 — הכנת ה"תוקף" (Attacker VM)

chmod +x attacker/listener.sh
./attacker/listener.sh 4444

הסקריפט מריץ nc -lvnp 4444 — מאזין שמחכה לחיבור נכנס מהקורבן.

## שלב 3 — ביצוע הניצול (Exploit)

מהתוקף (או מכל מקום שרואה את הקורבן):

chmod +x exploit/exploit.sh
./exploit/exploit.sh VICTIM_IP ATTACKER_IP ATTACKER_PORT

לדוגמה:

./exploit/exploit.sh 192.168.56.20 192.168.56.10 4444

הסקריפט שולח לאפליקציה הפגיעה פרמטר שמכיל bash -i reverse shell payload
— כלומר "רוכב" על הפקודה הלגיטימית (ping) ומצרף לה פקודה שפותחת חיבור TCP
חוזר לתוקף ומחברת אותו ל-bash אינטראקטיבי.

בצד התוקף (בחלון עם ה-listener) תראה שורה כמו חיבור נכנס, ולאחריה פרומפט
shell של הקורבן.

זהו זה — יש לך shell מרוחק על הקורבן, בלי שנפתח שום פורט האזנה בצד הקורבן
(ולכן קוראים לזה reverse — הקורבן הוא זה שמתחבר אליך, וזה עוקף הרבה
הגדרות פיירוול/NAT שחוסמות חיבורים נכנסים).

## חלופות ל-payload

קיימות דרכים נוספות מוכרות להשגת reverse shell (למשל דרך python, perl או
socat, אם הם מותקנים בקורבן) — כולן מבוססות על אותו עיקרון: תהליך פותח חיבור
TCP יוצא ומחבר את קלט/פלט/שגיאות ה-shell אליו. שימו לב: קבצי טקסט שמכילים
כמה כאלה one-liners יחד עלולים להיחסם/להיכנס ל-quarantine אוטומטית על ידי
אנטי-וירוס (כמו Windows Defender) גם על מכונת פיתוח רגילה — זו התנהגות
צפויה ותקינה של ה-AV, לא באג.

## איך מתגוננים מזה (Blue Team)

- וידוא קלט: לעולם לא להעביר קלט משתמש ל-shell=True/os.system/subprocess
  בלי allow-list קפדני (למשל regex שמאשר רק כתובות IPv4 תקינות).
- Egress filtering: לחסום בפיירוול תעבורה יוצאת לא צפויה משרתים (outbound
  לפורטים לא סטנדרטיים) — reverse shell תלוי בכך שהחיבור היוצא מותר.
- Monitoring: EDR/auditd שמתריע על bash -i, /dev/tcp/*, nc -e,
  תהליכי shell שנפתחים מתחת לתהליך שרת web.
- Least privilege: להריץ שירותי web עם משתמש לא-פריווילגי, לא root.
- WAF / קוד סקירה: לזהות command injection לפני production (SAST/DAST).

## ניקוי המעבדה

בקורבן: Ctrl+C לעצירת vulnerable_app.py
בתוקף: Ctrl+C לעצירת ה-listener, או exit בתוך ה-shell שהתקבל

מומלץ למחוק את ה-VM-ים או להחזיר Snapshot בסיום התרגול.
