pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        PATH = "/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

        IMAGE_NAME = "madhu58/networksource"
        IMAGE_TAG = "latest"

        CONTAINER_NAME = "networksource"
        CONTAINER_PORT = "8083"

        K8S_DEPLOYMENT = "network-project"
        K8S_SERVICE = "network-service"

        // Replace these with your AKS details
        AKS_RESOURCE_GROUP = "your-resource-group"
        AKS_CLUSTER_NAME   = "your-aks-cluster"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Git Information') {
            steps {
                sh '''
                echo "========== USER =========="
                whoami

                echo "========== WORKSPACE =========="
                pwd

                echo "========== PATH =========="
                echo $PATH

                echo "========== GIT VERSION =========="
                git --version

                echo "========== GIT STATUS =========="
                git status

                echo "========== LAST COMMIT =========="
                git log --oneline -1
                '''
            }
        }

        stage('Verify Docker') {
            steps {
                sh '''
                echo "========== DOCKER =========="
                which docker
                docker --version
                docker info
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Docker Images') {
            steps {
                sh '''
                docker images
                '''
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login \
                      -u "$DOCKER_USER" \
                      --password-stdin
                    '''
                }
            }
        }

        stage('Docker Push') {
            steps {
                sh '''
                docker push ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Docker Pull') {
            steps {
                sh '''
                docker pull ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Remove Old Container') {
            steps {
                sh '''
                docker rm -f ${CONTAINER_NAME} || true
                '''
            }
        }

        stage('Run Docker Container') {
            steps {
                sh '''
                docker run -d \
                  --name ${CONTAINER_NAME} \
                  -p ${CONTAINER_PORT}:80 \
                  ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Docker Logs') {
            steps {
                sh '''
                docker logs ${CONTAINER_NAME}
                '''
            }
        }

        stage('Docker Copy') {
            steps {
                sh '''
                mkdir -p backup

                docker cp \
                  ${CONTAINER_NAME}:/usr/share/nginx/html/index.html \
                  backup/index.html || true
                '''
            }
        }

        stage('Azure Login') {
            steps {
                withCredentials([
                    string(credentialsId: 'azure-client-id', variable: 'AZURE_CLIENT_ID'),
                    string(credentialsId: 'azure-client-secret', variable: 'AZURE_CLIENT_SECRET'),
                    string(credentialsId: 'azure-tenant-id', variable: 'AZURE_TENANT_ID'),
                    string(credentialsId: 'azure-subscription-id', variable: 'AZURE_SUBSCRIPTION_ID')
                ]) {
                    sh '''
                    echo "========== AZURE CLI =========="
                    az version

                    echo "========== LOGIN =========="
                    az login \
                      --service-principal \
                      --username "$AZURE_CLIENT_ID" \
                      --password "$AZURE_CLIENT_SECRET" \
                      --tenant "$AZURE_TENANT_ID"

                    echo "========== SET SUBSCRIPTION =========="
                    az account set --subscription "$AZURE_SUBSCRIPTION_ID"

                    echo "========== GET AKS CREDENTIALS =========="
                    az aks get-credentials \
                      --resource-group ${AKS_RESOURCE_GROUP} \
                      --name ${AKS_CLUSTER_NAME} \
                      --overwrite-existing

                    echo "========== VERIFY CLUSTER =========="
                    kubectl get nodes
                    '''
                }
            }
        }

        stage('Kubernetes Deploy') {
            steps {
                sh '''
                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml
                '''
            }
        }

        stage('Rollout Status') {
            steps {
                sh '''
                kubectl rollout status deployment/${K8S_DEPLOYMENT} --timeout=180s
                '''
            }
        }

        stage('Verify Kubernetes') {
            steps {
                sh '''
                echo "===== Deployments ====="
                kubectl get deployments

                echo "===== Pods ====="
                kubectl get pods -o wide

                echo "===== Services ====="
                kubectl get svc

                echo "===== Nodes ====="
                kubectl get nodes
                '''
            }
        }

        stage('Application Test') {
            steps {
                sh '''
                kubectl get svc ${K8S_SERVICE}
                '''
            }
        }

        stage('Cleanup') {
            steps {
                sh '''
                docker image prune -f || true
                docker container prune -f || true
                '''
            }
        }
    }

    post {

        success {
            echo '================================='
            echo 'BUILD SUCCESSFUL'
            echo '================================='

            sh '''
            echo "Docker Images:"
            docker images | grep networksource || true

            echo "Running Containers:"
            docker ps
            '''
        }

        failure {
            echo '================================='
            echo 'BUILD FAILED'
            echo '================================='

            sh '''
            echo "Rolling back Kubernetes deployment..."

            kubectl rollout undo deployment/${K8S_DEPLOYMENT} || true

            kubectl get deployments
            kubectl get pods
            '''
        }

        always {
            echo 'Cleaning workspace...'
            cleanWs()
        }
    }
}