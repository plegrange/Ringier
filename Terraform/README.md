# Terraform in AWS
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
Deploy the stack using ```terraform apply```
