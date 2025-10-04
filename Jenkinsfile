pipeline {
    agent any

    environment {
        AWS_REGION = "us-west-2"
        ECR_REPO   = "109398616914.dkr.ecr.us-west-2.amazonaws.com/partha/fullstack"
        IMAGE_TAG  = "latest"
        CLUSTER_NAME = "education-eks-6neSTHHy"
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
        stage('Configure Kubeconfig') {
            steps {
                sh """
                  aws eks --region $AWS_REGION update-kubeconfig --name $CLUSTER_NAME
                """
            }
        }

        stage('Deploy to EKS') {
            steps {
              sh """
                        kubectl apply -f deployment.yaml
                          kubectl rollout status deployment/nginx-deployment
                        """
                    }
                }
    }
}
//sre_user