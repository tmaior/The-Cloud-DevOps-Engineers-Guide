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
        stage('Clone Repository') {
            steps {
                // Clone the Git repository using specified branch
                git branch: "${GIT_BRANCH}", url: "${GIT_REPO}"
            }
        }

        stage('Build Docker Image') {
            steps {
                dir("${PROJECT_PATH}") {
                    script {
                        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: "${AWS_CREDENTIALS_ID}"]]) {
                            // Login to AWS ECR
                            sh 'aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO'
                            
                            // Build the Docker image using the Dockerfile in the correct directory
                            sh 'DOCKER_BUILDKIT=1 docker build -t $DOCKER_IMAGE -f Dockerfile .'
                        }
                    }
                }
            }
        }

        stage('Push Docker Image to ECR') {
            steps {
                script {
                    // Push the Docker image to the ECR repository
                    sh 'docker push $DOCKER_IMAGE'
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: "${SSH_KEY}", keyFileVariable: 'SSH_KEYFILE')]) {
                        // Deploy to EC2 by pulling the latest image and restarting the service
                        sh '''
                        ssh -t -o StrictHostKeyChecking=no -i $SSH_KEYFILE $EC2_USER@$EC2_IP << 'EOF'

                        # Authenticate Docker to ECR
                        aws ecr get-login-password --region '''${AWS_REGION}''' | sudo docker login --username AWS --password-stdin $ECR_REPO
                        
                        # Pull the Docker image from ECR
                        sudo docker pull $DOCKER_IMAGE
                        
                        # Check if the existing container is running and stop/remove it
                        if sudo docker ps -q -f name=flask_app; then
                            sudo docker stop flask_app
                            sudo docker rm flask_app
                        fi
                        
                        # Run the new Docker container
                        sudo docker run -d --name flask_app -p 80:80 $DOCKER_IMAGE
                        EOF
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            // Clean up the workspace after the pipeline finishes
            cleanWs()
        }
    }
}
