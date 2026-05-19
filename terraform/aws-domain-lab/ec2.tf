data "aws_ami" "windows_server_2022" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["Windows_Server-2022-English-Full-Base-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
}

resource "aws_instance" "dc" {
  ami                    = data.aws_ami.windows_server_2022.id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.lab.id]
  key_name               = var.key_pair_name
  get_password_data      = true

  root_block_device {
    volume_size = var.root_volume_size_gb
    volume_type = "gp3"
    encrypted   = true
  }

  tags = {
    Name = "${local.name_prefix}-dc"
    Role = "DomainController"
  }

  lifecycle {
    ignore_changes = [ami]
  }
}

resource "aws_instance" "member" {
  ami                    = data.aws_ami.windows_server_2022.id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.lab.id]
  key_name               = var.key_pair_name
  get_password_data      = true

  depends_on = [aws_instance.dc]

  root_block_device {
    volume_size = var.root_volume_size_gb
    volume_type = "gp3"
    encrypted   = true
  }

  tags = {
    Name = "${local.name_prefix}-member"
    Role = "DomainMember"
  }

  lifecycle {
    ignore_changes = [ami]
  }
}
