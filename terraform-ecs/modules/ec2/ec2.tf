resource "aws_security_group" "ec2_sg" {
  name        = "ec2_security_group"
  description = "Allow SSH and HTTP traffic"
  vpc_id      = var.network.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allows SSH access from anywhere
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allows HTTP access from anywhere
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"          # Allows all outbound traffic
    cidr_blocks = ["0.0.0.0/0"]  # Allows outbound traffic to anywhere
  }
}


resource "aws_instance" "web_server" {
  ami           = data.aws_ami.latest_ubuntu.id
  instance_type = var.instance_type
  key_name      = var.key_name
  security_groups = [aws_security_group.ec2_sg.id]
  subnet_id     = var.network.subnets[0]

  user_data = <<-EOF
    #!/bin/bash
    # Java
    sudo apt update
    sudo apt install openjdk-17-jdk openjdk-17-jre -y

    # Jenkins
    sudo wget -O /usr/share/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
    echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
    sudo apt-get update
    sudo apt-get install jenkins -y


    # Docker and BuildX
    sudo apt install docker.io -y
    sudo apt install docker-buildx -y

    # Adding Jenkins and ubuntu to Docker usergroup
    sudo usermod -aG docker jenkins
    sudo usermod -aG docker ubuntu
    sudo systemctl restart jenkins

    # AWS CLI
    sudo apt install unzip
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
  EOF
              
  tags = {
    Name = "jenkins-server"
  }
}
