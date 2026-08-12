###############################################################
#  IDPS Simulation — Terraform Deployment
#  Provisions: VPC · Subnet · IGW · SG · EC2 · Elastic IP
#  App runs on port 8080 inside Docker (auto-started)
###############################################################

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# ─────────────────────────────────────────────────────────────
# DATA — latest Ubuntu 24.04 LTS AMI (free tier)
# ─────────────────────────────────────────────────────────────
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# ─────────────────────────────────────────────────────────────
# VPC
# ─────────────────────────────────────────────────────────────
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = merge(local.common_tags, { Name = "${var.project_name}-vpc" })
}

# ─────────────────────────────────────────────────────────────
# PUBLIC SUBNET
# ─────────────────────────────────────────────────────────────
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.subnet_cidr
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true

  tags = merge(local.common_tags, { Name = "${var.project_name}-public-subnet" })
}

# ─────────────────────────────────────────────────────────────
# INTERNET GATEWAY + ROUTE TABLE
# ─────────────────────────────────────────────────────────────
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags   = merge(local.common_tags, { Name = "${var.project_name}-igw" })
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = merge(local.common_tags, { Name = "${var.project_name}-rt-public" })
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# ─────────────────────────────────────────────────────────────
# SECURITY GROUP
# ─────────────────────────────────────────────────────────────
resource "aws_security_group" "idps" {
  name        = "${var.project_name}-sg"
  description = "IDPS Simulation — allow SSH and app traffic"
  vpc_id      = aws_vpc.main.id

  # SSH — restrict to your IP in production
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.ssh_allowed_cidrs
  }

  # App port — open to all students
  ingress {
    description = "IDPS Web App"
    from_port   = var.app_port
    to_port     = var.app_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # All outbound (needed for apt-get, Docker pull, GitHub)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(local.common_tags, { Name = "${var.project_name}-sg" })
}

# ─────────────────────────────────────────────────────────────
# KEY PAIR  (uploads your local public key to AWS)
# ─────────────────────────────────────────────────────────────
resource "aws_key_pair" "deployer" {
  key_name   = "${var.project_name}-key"
  public_key = file(var.public_key_path)

  tags = local.common_tags
}

# ─────────────────────────────────────────────────────────────
# EC2 INSTANCE
# ─────────────────────────────────────────────────────────────
resource "aws_instance" "idps" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.idps.id]
  key_name               = aws_key_pair.deployer.key_name

  # Bootstrap script — installs Docker and starts the app
  user_data = templatefile("${path.module}/user_data.sh", {
    app_port     = var.app_port
    github_repo  = var.github_repo
    docker_image = var.docker_image_name
  })

  # Root volume — 8 GB is enough for Docker + app
  root_block_device {
    volume_type           = "gp3"
    volume_size           = 8
    delete_on_termination = true
    encrypted             = true
  }

  # Prevent accidental destruction in class
  lifecycle {
    ignore_changes = [ami, user_data]
  }

  tags = merge(local.common_tags, { Name = "${var.project_name}-server" })
}

# ─────────────────────────────────────────────────────────────
# ELASTIC IP — stable address you can share with students
# ─────────────────────────────────────────────────────────────
resource "aws_eip" "idps" {
  instance = aws_instance.idps.id
  domain   = "vpc"

  depends_on = [aws_internet_gateway.main]

  tags = merge(local.common_tags, { Name = "${var.project_name}-eip" })
}

# ─────────────────────────────────────────────────────────────
# LOCALS
# ─────────────────────────────────────────────────────────────
locals {
  common_tags = {
    Project     = var.project_name
    Environment = "classroom"
    ManagedBy   = "terraform"
  }
}
