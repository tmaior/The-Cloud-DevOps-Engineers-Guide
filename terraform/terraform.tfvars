aws_region          = "us-east-1"
vpc_cidr_block      = "10.0.0.0/16"
vpc_public_subnets  = ["10.0.10.0/24", "10.0.20.0/24"]
vpc_private_subnets = ["10.0.30.0/24", "10.0.40.0/24"]
vpc_enable_nat_gateway = true
vpc_single_nat_gateway = true

# EC2 Configuration
instance_type = "t3.micro"
key_name      = "vika-ripardo"

# Tags and Metadata
owners      = "vika-ripardo"
environment = "dev"

# IAM and ECR
iam_role_name = "book-ec2-role"
ecr_repo_name = "book-ecr-repo"