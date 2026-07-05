pipeline {
    agent any

    environment {
        // Make sure Jenkins can find Docker on macOS
        PATH = "/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

        DOCKER_IMAGE = "madhu58/networksource"
        DOCKER_TAG = "latest"

        CONTAINER_NAME = "networksource"
        PORT = "8080"
    }

    stages {

        stage('Checkout Source') {
            steps {
                checkout scm
            }
        }

        stage('Git Info') {
            steps {
                sh '''
                echo "===== USER ====="
                whoami

                echo "===== CURRENT DIRECTORY ====="
                pwd

                echo "===== GIT STATUS ====="
                git status

                echo "===== LAST COMMIT ====="
                git log --oneline -1
                '''
            }
        }

        stage('Check Docker') {
            steps {
                sh '''
                echo "===== PATH ====="
                echo $PATH

                echo "===== WHICH DOCKER ====="
                which docker

                echo "===== DOCKER VERSION ====="
                docker --version

                echo "===== DOCKER INFO ====="
                docker info
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
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
                docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                '''
            }
        }

        stage('Docker Pull') {
            steps {
                sh '''
                docker pull ${DOCKER_IMAGE}:${DOCKER_TAG}
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

        stage('Run Container') {
            steps {
                sh '''
                docker run -d \
                --name ${CONTAINER_NAME} \
                -p ${PORT}:80 \
                ${DOCKER_IMAGE}:${DOCKER_TAG}
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
                kubectl apply -f k8s/deployment.yaml
                kubectl apply -f k8s/service.yaml
                '''
            }
        }

        stage('Verify Kubernetes') {
            steps {
                sh '''
                kubectl get pods
                kubectl get deployments
                kubectl get services
                '''
            }
        }
    }

    post {

        success {
            echo 'Pipeline completed successfully.'
        }

        failure {
            echo 'Pipeline failed.'
        }

        always {
            sh '''
            docker image prune -f || true
            '''
        }
    }
}