# Bastion with Terraform in AWS
![image](https://github.com/user-attachments/assets/3d3f083f-e244-4e57-85a4-32e0a160cfb0)

## Requirements (Linux)
- terraform ```sudo apt-get install terraform```
- awscli ```sudo apt install awscli```
- keypair ```ssh-keygen -t rsa -b 4096 -C "emailaddress@domain.com"```

## Configuration
#### terraform.tfvars
```
vpc = "phils-vpc"
private_subnet = "phils-private-subnet"
public_subnet = "phils-public-subnet"
key_name = "bastion_key"
public_key = "<PUBLIC_KEY>
private_sg_name = "private_sg"
public_sg_name = "public_sg"
gw_name = "phils_gw"
```
#### AWS CLI
- Generate an access key ID and Secret in AWS
- Configure CLI using the access key ID and Secret
```
$ aws configure
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-east-1
Default output format [None]: json
```

## Deployment
From directory ```Ringier/Terraform/```, deploy the stack using ```terraform apply```
