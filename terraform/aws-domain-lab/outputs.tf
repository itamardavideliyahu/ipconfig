output "vpc_id" {
  description = "Lab VPC ID."
  value       = aws_vpc.lab.id
}

output "security_group_id" {
  description = "Security group shared by both instances."
  value       = aws_security_group.lab.id
}

output "domain_name" {
  description = "Intended AD domain name (configure manually on the DC)."
  value       = var.domain_name
}

output "dc_instance_id" {
  description = "EC2 instance ID of the future Domain Controller."
  value       = aws_instance.dc.id
}

output "member_instance_id" {
  description = "EC2 instance ID of the domain member server."
  value       = aws_instance.member.id
}

output "dc_public_ip" {
  description = "Public IP of the DC instance (RDP)."
  value       = aws_instance.dc.public_ip
}

output "member_public_ip" {
  description = "Public IP of the member instance (RDP)."
  value       = aws_instance.member.public_ip
}

output "dc_private_ip" {
  description = "Private IP of the DC — use as DNS target for domain join."
  value       = aws_instance.dc.private_ip
}

output "member_private_ip" {
  description = "Private IP of the member server."
  value       = aws_instance.member.private_ip
}

output "rdp_dc_command" {
  description = "Windows Remote Desktop connection string for the DC."
  value       = "mstsc /v:${aws_instance.dc.public_ip}"
}

output "rdp_member_command" {
  description = "Windows Remote Desktop connection string for the member server."
  value       = "mstsc /v:${aws_instance.member.public_ip}"
}

output "password_retrieval_hint" {
  description = "How to obtain the Administrator password."
  value       = <<-EOT
    Wait 4-5 minutes after instance launch, then run (replace KEY.pem and INSTANCE_ID):
      aws ec2 get-password-data --region ${var.aws_region} --instance-id <INSTANCE_ID> --priv-file KEY.pem
    Or use EC2 Console -> Instance -> Connect -> Get Windows password.
  EOT
}

output "connectivity_test_steps" {
  description = "Steps to verify connectivity before configuring AD."
  value       = <<-EOT
    1. RDP to DC (${aws_instance.dc.public_ip}) and Member (${aws_instance.member.public_ip}).
    2. On DC, open PowerShell:
         ping ${aws_instance.member.private_ip}
         Test-NetConnection ${aws_instance.member.private_ip} -Port 3389
    3. On Member:
         ping ${aws_instance.dc.private_ip}
         Test-NetConnection ${aws_instance.dc.private_ip} -Port 3389
    4. After AD is installed on DC, also test:
         Test-NetConnection ${aws_instance.dc.private_ip} -Port 389
  EOT
}
