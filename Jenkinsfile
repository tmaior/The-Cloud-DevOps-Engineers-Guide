pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'
        ECR_REPO = '654654369899.dkr.ecr.us-east-1.amazonaws.com/flask-web-app'
        DOCKER_IMAGE = "${ECR_REPO}:latest"
        GIT_REPO = 'https://github.com/tmaior/The-Cloud-DevOps-Engineers-Guide.git'
        GIT_BRANCH = 'main'
        PROJECT_PATH = 'tasks-webapp/'
        AWS_CREDENTIALS_ID = 'aws-credentials'
        ECS_CLUSTER = 'webapp-devops-book-cluster'
        ECS_SERVICE = 'flask-app'
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
                        // Use withAWS for AWS credentials and region
                        withAWS(credentials: "${AWS_CREDENTIALS_ID}", region: "${AWS_REGION}") {
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

        stage('Deploy to ECS') {
            steps {
                script {
                    // Use withAWS for ECS service update with credentials and region
                    withAWS(credentials: "${AWS_CREDENTIALS_ID}", region: "${AWS_REGION}") {
                        // Update ECS service with the new image
                        sh '''
                        aws ecs update-service --cluster $ECS_CLUSTER \
                        --service $ECS_SERVICE \
                        --force-new-deployment \
                        --region $AWS_REGION
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