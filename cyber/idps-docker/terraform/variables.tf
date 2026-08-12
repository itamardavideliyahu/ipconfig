###############################################################
#  Variables — override in terraform.tfvars
###############################################################

variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Prefix for all resource names"
  type        = string
  default     = "idps-sim"
}

variable "instance_type" {
  description = "EC2 instance type (t2.micro = Free Tier)"
  type        = string
  default     = "t2.micro"

  validation {
    condition     = contains(["t2.micro", "t3.micro", "t3.small"], var.instance_type)
    error_message = "Use t2.micro (free tier) or t3.micro/small for production."
  }
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.10.0.0/16"
}

variable "subnet_cidr" {
  description = "CIDR block for the public subnet"
  type        = string
  default     = "10.10.1.0/24"
}

variable "app_port" {
  description = "Port the IDPS web app listens on"
  type        = number
  default     = 8080
}

variable "ssh_allowed_cidrs" {
  description = "CIDR list allowed to SSH (restrict to your IP in production)"
  type        = list(string)
  default     = ["0.0.0.0/0"]   # change to ["YOUR.IP.HERE/32"] for security
}

variable "public_key_path" {
  description = "Path to your SSH public key file"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "github_repo" {
  description = "GitHub repo URL to clone (must be public)"
  type        = string
  default     = "https://github.com/itamardavideliyahu/ipconfig.git"
}

variable "docker_image_name" {
  description = "Name to tag the Docker image"
  type        = string
  default     = "idps-simulation"
}
