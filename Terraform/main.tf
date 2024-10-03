provider "aws" {
  region = "us-east-1"
}


## Create VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = var.vpc
  }
}

## Create public subnet
resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone = "us-east-1a"

  tags = {
    Name = var.public_subnet
  }
}

## Create private subnet
resource "aws_subnet" "private" {
    vpc_id = aws_vpc.main.id
    cidr_block = "10.0.2.0/24"
    availability_zone = "us-east-1a"

    tags = {
        Name = var.private_subnet
    }
}


## Create internet gateway for public subnet
resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = var.gw_name
  }
}

## Create route table for public subnet
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    Name = "phils-public-route-table"
  }
}

## Associate public subnet with public route table
resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

## Create security group for bastion host in public subnet
resource "aws_security_group" "bastion_sg" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Limit this for better security
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = var.public_sg_name
  }
}

## Create security group for private instances
resource "aws_security_group" "private_sg" {
    vpc_id = aws_vpc.main.id

    ingress {
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = []  # Not needed if using security group reference
        security_groups = [aws_security_group.bastion_sg.id]  # Allow SSH from Bastion's SG
    }

    tags = {
        Name = var.private_sg_name
    }
}

## Create IAM role for Bastion host
resource "aws_iam_role" "bastion_role" {
    name = "bastion-role"
    
    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
        {
            Effect = "Allow"
            Principal = {
            Service = "ec2.amazonaws.com"
            }
            Action = "sts:AssumeRole"
        }
        ]
  })
}

## Attach IAM Role to Instance Profile
resource "aws_iam_instance_profile" "bastion_profile" {
  name = "bastion-profile"
  role = aws_iam_role.bastion_role.name
}

## Create keypair
resource "aws_key_pair" "bastion_key" {
  key_name   = var.key_name
  public_key = var.public_key
}

## Create Bastion host in public subnet
resource "aws_instance" "bastion" {
    ami = "ami-0a886eeb9597d0e11"
    instance_type = "t4g.micro"
    key_name = aws_key_pair.bastion_key.key_name
    subnet_id = aws_subnet.public.id
    vpc_security_group_ids = [aws_security_group.bastion_sg.id]

    tags = {
        Name = "bastion-host"
    }
}

## Create instance in private subnet
resource "aws_instance" "private_instance" {
    ami = "ami-0ebfd941bbafe70c6"
    instance_type = "t3.nano"
    key_name = aws_key_pair.bastion_key.key_name
    subnet_id = aws_subnet.private.id
    vpc_security_group_ids = [aws_security_group.private_sg.id]

    tags = {
        Name = "private-instance"
    }
}


output "bastion_public_ip" {
  value = aws_instance.bastion.public_ip
}
