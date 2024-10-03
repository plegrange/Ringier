variable "vpc" {
    description = "Name of the VPC"
    type = string
}

variable "private_subnet" {
    description = "Name of the private subnet"
    type = string
}

variable "public_subnet" {
    description = "Name of the public subnet"
    type = string
}

variable "key_name" {
    description = "Name of the SSH key pair"
    type = string
}

variable "public_key" {
    description = "Public key for SSH access"
    type = string

}

variable "public_sg_name" {
    description = "Name of the public security group"
    type = string
}

variable "private_sg_name" {
    description = "Name of the private security group"
    type = string
}

variable "gw_name" {
    description = "Name of the internet gateway"
    type = string
}
