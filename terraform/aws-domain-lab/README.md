# AWS Domain Lab — Terraform

Infrastructure-only lab: **VPC + 2× Windows Server 2022** on AWS.  
Active Directory and domain join are **manual** (student scripts) — see [scripts/Lab-Domain-Join.md](scripts/Lab-Domain-Join.md).

## Architecture

- VPC `10.0.0.0/16`, public subnet `10.0.1.0/24`
- Internet Gateway for RDP and Windows updates
- One security group for both instances:
  - RDP `3389` from `admin_cidr` only
  - All TCP/UDP between instances in the same SG (AD traffic)
  - ICMP inside the VPC (ping exercises)
- EC2 instances:
  - `domain-lab-lab-dc` — future Domain Controller
  - `domain-lab-lab-member` — future domain member

## Prerequisites

| Tool | Purpose |
|------|---------|
| [Terraform](https://www.terraform.io/downloads) >= 1.5 | Deploy infrastructure |
| [AWS CLI](https://aws.amazon.com/cli/) | Credentials + password retrieval |
| AWS account | EC2, VPC billing applies |
| EC2 Key Pair | Decrypt Windows Administrator password |

### Create a key pair (example)

```powershell
# Generate key locally (if you don't have one)
ssh-keygen -t rsa -b 4096 -f domain-lab-key -N '""'

# Import public key to AWS (same region as terraform.tfvars)
aws ec2 import-key-pair --region eu-west-1 --key-name domain-lab-key --public-key-material fileb://domain-lab-key.pub
```

### Find your public IP for RDP

```powershell
(Invoke-WebRequest -Uri "https://checkip.amazonaws.com" -UseBasicParsing).Content.Trim()
# Use as admin_cidr: x.x.x.x/32
```

## Quick start

```powershell
cd terraform/aws-domain-lab
copy terraform.tfvars.example terraform.tfvars
# Edit: admin_cidr, key_pair_name, aws_region

terraform init
terraform plan
terraform apply
```

### Outputs

```powershell
terraform output
terraform output -raw rdp_dc_command
terraform output -raw dc_private_ip
```

### Windows password

Wait **4–5 minutes** after `apply`, then:

```powershell
aws ec2 get-password-data `
  --region eu-west-1 `
  --instance-id (terraform output -raw dc_instance_id) `
  --priv-file C:\path\to\domain-lab-key.pem
```

Repeat for `member_instance_id`.

### Connectivity test (before AD)

RDP to both servers, then from DC:

```powershell
ping <member_private_ip>
Test-NetConnection <member_private_ip> -Port 3389
```

See `terraform output connectivity_test_steps`.

## Active Directory (students)

1. RDP to DC → run [scripts/01-install-ad-dc.ps1](scripts/01-install-ad-dc.ps1)
2. RDP to Member → run [scripts/02-configure-dns-and-join.ps1](scripts/02-configure-dns-and-join.ps1)
3. Full guide (Hebrew): [scripts/Lab-Domain-Join.md](scripts/Lab-Domain-Join.md)

After the domain works, optional: [windows-server maintenance scripts](../../windows-server/Windows-Server-Maintenance.md).

## Cost warning

Approximate cost while running:

- 2 × `t3.large` Windows instances
- 2 × 80 GB gp3 encrypted volumes
- Data transfer

Roughly **$0.15–0.25/hour** depending on region.  
**Always run `terraform destroy` when finished.**

## Security notes

- Never set `admin_cidr = "0.0.0.0/0"` in a real environment.
- Lab SG allows all traffic between instances (`self`) for simplicity. In production, restrict to [AD ports](https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/config-firewall-for-ad-ds).
- `terraform.tfvars` is gitignored (may contain sensitive values).

## Teardown

```powershell
terraform destroy
```

## Variables reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `admin_cidr` | yes | — | Your IP for RDP (`/32`) |
| `key_pair_name` | yes | — | Existing EC2 key pair name |
| `aws_region` | no | `eu-west-1` | AWS region |
| `instance_type` | no | `t3.large` | Instance size |
| `domain_name` | no | `lab.local` | For scripts/docs only |
| `root_volume_size_gb` | no | `80` | OS disk size |

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `InvalidKeyPair.NotFound` | Create/import key pair in the same region |
| Password decrypt fails | Wait longer; verify `.pem` matches key pair |
| RDP timeout | Check `admin_cidr` is your current public IP |
| AMI not found | Change region or update AMI filter in `ec2.tf` |
| Ping works, AD fails | DNS on member must point to `dc_private_ip` |

## Files

```
terraform/aws-domain-lab/
├── versions.tf / providers.tf / variables.tf
├── vpc.tf / security.tf / ec2.tf / outputs.tf
├── terraform.tfvars.example
├── README.md
└── scripts/
    ├── 01-install-ad-dc.ps1
    ├── 02-configure-dns-and-join.ps1
    └── Lab-Domain-Join.md
```
