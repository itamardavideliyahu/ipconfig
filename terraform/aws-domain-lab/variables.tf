variable "aws_region" {
  description = "AWS region for the lab (Windows Server AMI must exist in this region)."
  type        = string
  default     = "eu-west-1"
}

variable "project_name" {
  description = "Project name used in resource naming."
  type        = string
  default     = "domain-lab"
}

variable "environment" {
  description = "Environment label (lab, dev, etc.)."
  type        = string
  default     = "lab"
}

variable "vpc_cidr" {
  description = "CIDR block for the lab VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for the public subnet."
  type        = string
  default     = "10.0.1.0/24"
}

variable "admin_cidr" {
  description = "Your public IP in CIDR notation for RDP access (e.g. 203.0.113.10/32). Never use 0.0.0.0/0 in production."
  type        = string
}

variable "key_pair_name" {
  description = "Name of an existing EC2 key pair in the target region (used to decrypt the Windows Administrator password)."
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type for both Windows servers. t3.large is recommended for AD lab work."
  type        = string
  default     = "t3.large"
}

variable "root_volume_size_gb" {
  description = "Root EBS volume size in GB for each instance."
  type        = number
  default     = 80
}

variable "domain_name" {
  description = "Active Directory domain name for documentation and student scripts (not created by Terraform)."
  type        = string
  default     = "lab.local"
}

variable "safe_mode_password" {
  description = "DSRM (Directory Services Restore Mode) password when promoting the DC via student script."
  type        = string
  sensitive   = true
  default     = null
}

variable "tags" {
  description = "Additional tags applied to all resources."
  type        = map(string)
  default     = {}
}
