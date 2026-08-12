# IDPS Simulation — Terraform Deployment

> פריסה מקצועית של אפליקציית IDPS על AWS EC2 בפקודות בודדות.

---

## דרישות מוקדמות

| כלי | גרסה מינימלית | הורדה |
|-----|--------------|--------|
| **Terraform** | >= 1.5 | [terraform.io](https://www.terraform.io/downloads) |
| **AWS CLI** | >= 2.0 | [aws.amazon.com/cli](https://aws.amazon.com/cli/) |
| **AWS Account** | — | עם הרשאות EC2, VPC, IAM |
| **SSH Key Pair** | — | `ssh-keygen -t rsa -b 4096` |

---

## מבנה הקבצים

```
terraform/
├── main.tf                  ← משאבים ראשיים (VPC, EC2, SG, EIP)
├── variables.tf             ← הגדרת משתנים + ברירות מחדל
├── outputs.tf               ← פלטים לאחר apply (URL, IP, SSH)
├── user_data.sh             ← סקריפט Bootstrap לEC2
├── terraform.tfvars.example ← תבנית להגדרות אישיות
├── .gitignore               ← מונע חשיפת state ו-tfvars
└── README.md                ← המסמך הזה
```

---

## הרצה מהירה — 4 פקודות

### 1. הכנת תצורה
```bash
# העתק את קובץ הדוגמה
cp terraform.tfvars.example terraform.tfvars

# ערוך את הפרמטרים (אזור, key path וכו')
nano terraform.tfvars
```

### 2. אתחול Terraform
```bash
terraform init
```

### 3. תצוגה מקדימה של מה ייבנה
```bash
terraform plan
```

**פלט צפוי:**
```
Plan: 8 to add, 0 to change, 0 to destroy.

  + aws_vpc.main
  + aws_subnet.public
  + aws_internet_gateway.main
  + aws_route_table.public
  + aws_route_table_association.public
  + aws_security_group.idps
  + aws_key_pair.deployer
  + aws_instance.idps
  + aws_eip.idps
```

### 4. פריסה
```bash
terraform apply -auto-approve
```

**פלט צפוי לאחר ~3 דקות:**
```
Apply complete! Resources: 9 added.

Outputs:
  student_url      = "http://3.90.45.123:8080"
  elastic_ip       = "3.90.45.123"
  ssh_command      = "ssh -i ~/.ssh/id_rsa ubuntu@3.90.45.123"
  health_check_url = "http://3.90.45.123:8080/health"
```

> שתף את `student_url` עם התלמידים — זה הכל!

---

## ארכיטקטורה שנוצרת

```
Internet
    │
    ▼
┌──────────────────────────────────────────┐
│  VPC  10.10.0.0/16                       │
│  ┌──────────────────────────────────┐    │
│  │  Public Subnet  10.10.1.0/24     │    │
│  │                                  │    │
│  │  ┌─────────────────────────┐     │    │
│  │  │  EC2 t2.micro           │     │    │
│  │  │  Ubuntu 24.04           │     │    │
│  │  │  Docker → Flask:8080    │     │    │
│  │  └─────────────────────────┘     │    │
│  │          ↕ Elastic IP            │    │
│  └──────────────────────────────────┘    │
│              ↕ Internet Gateway          │
└──────────────────────────────────────────┘
```

---

## Security Group — פורטים

| פורט | פרוטוקול | מקור | מטרה |
|------|---------|------|------|
| `22` | TCP | `ssh_allowed_cidrs` | SSH לניהול |
| `8080` | TCP | `0.0.0.0/0` | גישת תלמידים |

---

## משתנים מרכזיים

| משתנה | ברירת מחדל | תיאור |
|-------|-----------|-------|
| `aws_region` | `us-east-1` | אזור AWS |
| `instance_type` | `t2.micro` | סוג המכונה |
| `app_port` | `8080` | פורט האפליקציה |
| `ssh_allowed_cidrs` | `["0.0.0.0/0"]` | IP מורשה ל-SSH |
| `public_key_path` | `~/.ssh/id_rsa.pub` | מפתח ציבורי |

---

## פקודות שימושיות

```bash
# הצג את כל ה-outputs שוב
terraform output

# הצג רק את ה-URL
terraform output student_url

# SSH לשרת
$(terraform output -raw ssh_command)

# בדוק שהאפליקציה עובדת
curl $(terraform output -raw health_check_url)

# צפה בלוגי Bootstrap
ssh ubuntu@$(terraform output -raw elastic_ip) \
  "sudo cat /var/log/user-data.log"

# צפה בלוגי הקונטיינר
ssh ubuntu@$(terraform output -raw elastic_ip) \
  "docker logs idps-sim"

# עדכון גרסה
terraform apply -replace="aws_instance.idps"
```

---

## הסרת כל המשאבים (בסוף הקורס)

```bash
terraform destroy -auto-approve
```

> **חשוב:** `destroy` מוחק הכל ומפסיק חיובים לחלוטין.

---

## עלויות AWS

| משאב | סוג | עלות (Free Tier) |
|------|-----|-----------------|
| EC2 | t2.micro | 750 שעות/חודש — **$0** |
| EIP | — | $0 כשמחוברת למכונה |
| Storage | 8 GB gp3 | 30 GB/חודש — **$0** |
| Data Transfer | outbound | 100 GB/חודש — **$0** |

> לאחר שנת Free Tier: ~$9/חודש.  
> השתמש ב-`terraform destroy` לאחר הקורס.

---

## פתרון בעיות

```bash
# שגיאת AWS credentials
aws configure                      # הכנס Access Key + Secret

# שגיאת Public Key
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa   # צור מפתח חדש

# שגיאת VPC limit
# מחק VPCs ישנות ב-AWS Console או בקש העלאת מכסה

# הקונטיינר לא עולה — בדוק logs
ssh ubuntu@<IP> "sudo cat /var/log/user-data.log"
ssh ubuntu@<IP> "docker ps -a"
```
