pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO = '654654369899.dkr.ecr.us-east-1.amazonaws.com/vika-ripardo-dev-ecr-repo'
        DOCKER_IMAGE = "${ECR_REPO}:latest"
        GIT_REPO = 'https://github.com/tmaior/The-Cloud-DevOps-Engineers-Guide.git'
        GIT_BRANCH = 'main'
        PROJECT_PATH = 'tasks-webapp/'
        SSH_KEY = 'ec2-ssh'  // ID of the SSH key credentials in Jenkins
        EC2_USER = 'ubuntu'
        EC2_IP = 'ec2-54-196-219-126.compute-1.amazonaws.com'
        AWS_CREDENTIALS_ID = 'aws-credentials'  // ID of the AWS credentials in Jenkins
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: "${env.GIT_BRANCH}", url: "${env.GIT_REPO}"
            }
        }

        stage('Build Docker Image') {
            steps {
                dir("${env.PROJECT_PATH}") {
                    script {
                        docker.withRegistry("https://${env.ECR_REPO}", "${env.AWS_CREDENTIALS_ID}") {
                            sh '$(aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO)'
                            sh 'docker build -t $DOCKER_IMAGE .'
                        }
                    }
                }
            }
        }

        stage('Push Docker Image to ECR') {
            steps {
                script {
                    sh 'docker push $DOCKER_IMAGE'
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent(credentials: ["${env.SSH_KEY}"]) {
                    script {
                        sh """
                        ssh -o StrictHostKeyChecking=no ${env.EC2_USER}@${env.EC2_IP} << EOF
                        sudo docker pull ${env.DOCKER_IMAGE}
                        sudo docker stop webapp || true
                        sudo docker rm webapp || true
                        sudo docker run -d --name webapp -p 80:80 ${env.DOCKER_IMAGE}
                        EOF
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
