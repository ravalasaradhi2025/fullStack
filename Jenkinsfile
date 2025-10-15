pipeline {
    agent any

    environment {
        AWS_REGION = "us-west-2"
        ECR_REPO   = "109398616914.dkr.ecr.us-west-2.amazonaws.com/partha/fullstack"
        IMAGE_TAG  = "latest"
        CLUSTER_NAME = "education-eks-fullstack"
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
                sh '''
                  export AWS_REGION=us-west-2
                  aws ecr get-login-password --region $AWS_REGION \
                  | docker login --username AWS --password-stdin 109398616914.dkr.ecr.us-west-2.amazonaws.com
                '''
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

                stage('map user to k8s') {
                    steps {
                        sh """
                                   eksctl create iamidentitymapping \
                                       --cluster $CLUSTER_NAME \
                                       --region us-east-2 \
                                       --arn arn:aws:iam::109398616914:role/myec2role \
                                       --username myec2role \
                                       --group system:masters
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
