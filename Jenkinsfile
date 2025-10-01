pipeline {
    agent any

    environment {
        AWS_REGION = "us-west-2"
        ECR_REPO   = "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-app"
        IMAGE_TAG  = "latest"
    }

    stages {
        stage('Checkout from GitHub') {
            steps {
                git branch: 'master',
                    url: 'https://github.com/ravalasaradhi2025/fullStack.git',
                    credentialsId: 'docker_git_id'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh """
                  docker build -t $ECR_REPO:$IMAGE_TAG .
                """
            }
        }

        stage('Login to ECR') {
            steps {
                sh """
                  aws ecr get-login-password --region $AWS_REGION \
                  | docker login --username AWS --password-stdin $ECR_REPO
                """
            }
        }

        stage('Push Image to ECR') {
            steps {
                sh "docker push $ECR_REPO:$IMAGE_TAG"
            }
        }
    }
}
