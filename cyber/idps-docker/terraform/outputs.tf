###############################################################
#  Outputs — printed after terraform apply
###############################################################

output "student_url" {
  description = "Share this URL with your students"
  value       = "http://${aws_eip.idps.public_ip}:${var.app_port}"
}

output "elastic_ip" {
  description = "Elastic IP (stable — does not change on reboot)"
  value       = aws_eip.idps.public_ip
}

output "ssh_command" {
  description = "Command to SSH into the server"
  value       = "ssh -i ~/.ssh/id_rsa ubuntu@${aws_eip.idps.public_ip}"
}

output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.idps.id
}

output "instance_type" {
  description = "EC2 instance type used"
  value       = aws_instance.idps.instance_type
}

output "ami_id" {
  description = "AMI used (Ubuntu 24.04)"
  value       = data.aws_ami.ubuntu.id
}

output "health_check_url" {
  description = "Endpoint to verify the app is running"
  value       = "http://${aws_eip.idps.public_ip}:${var.app_port}/health"
}
