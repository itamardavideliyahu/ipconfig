resource "aws_security_group" "lab" {
  name        = "${local.name_prefix}-sg"
  description = "Lab SG: RDP from admin, full traffic between lab instances, ICMP inside VPC"
  vpc_id      = aws_vpc.lab.id

  tags = {
    Name = "${local.name_prefix}-sg"
  }
}

# RDP from teacher/student public IP only
resource "aws_vpc_security_group_ingress_rule" "rdp_admin" {
  security_group_id = aws_security_group.lab.id
  description       = "RDP from admin CIDR"
  ip_protocol       = "tcp"
  from_port         = 3389
  to_port           = 3389
  cidr_ipv4         = var.admin_cidr
}

# All traffic between instances in this security group (AD, Kerberos, LDAP, SMB, etc.)
resource "aws_vpc_security_group_ingress_rule" "self_all_tcp" {
  security_group_id            = aws_security_group.lab.id
  description                  = "All TCP between lab instances"
  ip_protocol                  = "tcp"
  from_port                    = 0
  to_port                      = 65535
  referenced_security_group_id = aws_security_group.lab.id
}

resource "aws_vpc_security_group_ingress_rule" "self_all_udp" {
  security_group_id            = aws_security_group.lab.id
  description                  = "All UDP between lab instances"
  ip_protocol                  = "udp"
  from_port                    = 0
  to_port                      = 65535
  referenced_security_group_id = aws_security_group.lab.id
}

# Ping inside VPC (connectivity lab)
resource "aws_vpc_security_group_ingress_rule" "icmp_vpc" {
  security_group_id = aws_security_group.lab.id
  description       = "ICMP inside VPC"
  ip_protocol       = "icmp"
  from_port         = -1
  to_port           = -1
  cidr_ipv4         = var.vpc_cidr
}

resource "aws_vpc_security_group_egress_rule" "all_out" {
  security_group_id = aws_security_group.lab.id
  description       = "Allow all outbound"
  ip_protocol       = "-1"
  cidr_ipv4         = "0.0.0.0/0"
}
