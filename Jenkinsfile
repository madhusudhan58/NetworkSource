pipeline {
    agent any

    environment {
        PATH = "/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

        IMAGE_NAME = "madhu58/networksource"
        IMAGE_TAG = "latest"

        CONTAINER_NAME = "networksource"
        PORT = "8080"
    }

    options {
        timestamps()
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

                echo "========== PATH =========="
                echo $PATH

                echo "========== DIRECTORY =========="
                pwd

                echo "========== GIT VERSION =========="
                git --version

                echo "========== STATUS =========="
                git status

                echo "========== LAST COMMIT =========="
                git log --oneline -1
                '''
            }
        }

        stage('Verify Docker') {
            steps {
                sh '''
                which docker

                docker --version

                docker info
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build \
                -t ${IMAGE_NAME}:${IMAGE_TAG} .
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

        stage('Stop Old Container') {
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
                -p ${PORT}:80 \
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

        stage('Copy File From Container') {
            steps {
                sh '''
                mkdir -p backup

                docker cp \
                ${CONTAINER_NAME}:/usr/share/nginx/html/index.html \
                backup/index.html || true
                '''
            }
        }

        stage('Deploy Kubernetes') {
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
                kubectl get deployment

                kubectl get pods

                kubectl get svc
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
            docker ps -a || true

            docker images || true

            docker image prune -f || true
            '''
        }
    }
}