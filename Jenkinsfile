pipeline {
    agent any

    environment {
        IMAGE_NAME = "madhu58/network-project"
        IMAGE_TAG = "latest"
        CONTAINER_NAME = "network-project"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Git Info') {
            steps {
                sh '''
                    echo "Current Directory:"
                    pwd

                    echo "Git Status:"
                    git status

                    echo "Latest Commit:"
                    git log --oneline -1
                '''
            }
        }

        stage('Check Docker') {
            steps {
                sh '''
                    if ! command -v docker >/dev/null 2>&1; then
                        echo "ERROR: Docker is not installed or not in PATH."
                        exit 1
                    fi

                    docker --version
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
                        credentialsId: 'docker-hub',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
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

        stage('Docker Run') {
            steps {
                sh '''
                    docker rm -f ${CONTAINER_NAME} || true

                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p 8080:80 \
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

        stage('Kubernetes Deploy') {
            steps {
                sh '''
                    if command -v kubectl >/dev/null 2>&1; then
                        kubectl apply -f deployment.yaml
                        kubectl apply -f service.yaml
                    else
                        echo "kubectl not installed. Skipping deployment."
                    fi
                '''
            }
        }

        stage('Verify Kubernetes') {
            steps {
                sh '''
                    if command -v kubectl >/dev/null 2>&1; then
                        kubectl get pods
                        kubectl get services
                    else
                        echo "kubectl not installed."
                    fi
                '''
            }
        }
    }

    post {

        success {
            echo "Pipeline completed successfully."
        }

        failure {
            echo "Pipeline failed."
        }

        always {
            sh '''
                if command -v docker >/dev/null 2>&1; then
                    docker logout || true
                    docker image prune -f || true
                else
                    echo "Docker is not installed. Skipping cleanup."
                fi
            '''
        }
    }
}