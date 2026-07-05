pipeline {
    agent any

    environment {
        IMAGE_NAME = "madhu58/network-project"
        CONTAINER_NAME = "network-project"
        DOCKER_TAG = "latest"
    }

    stages {

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

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:${DOCKER_TAG} .
                '''
            }
        }

        stage('Docker Images') {
            steps {
                sh 'docker images'
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
                    docker push ${IMAGE_NAME}:${DOCKER_TAG}
                '''
            }
        }

        stage('Docker Pull') {
            steps {
                sh '''
                    docker pull ${IMAGE_NAME}:${DOCKER_TAG}
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
                      ${IMAGE_NAME}:${DOCKER_TAG}
                '''
            }
        }

        stage('Docker Logs') {
            steps {
                sh '''
                    docker logs ${CONTAINER_NAME} || true
                '''
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

        stage('Verify Kubernetes') {
            steps {
                sh '''
                    kubectl get deployments
                    kubectl get pods
                    kubectl get services
                '''
            }
        }
    }

    post {
        always {
            sh '''
                if command -v docker >/dev/null 2>&1; then
                    docker system prune -f
                else
                    echo "Docker is not installed. Skipping cleanup."
                fi
            '''
        }

        success {
            echo "Pipeline Completed Successfully"
        }

        failure {
            echo "Pipeline Failed"
        }
    }
}