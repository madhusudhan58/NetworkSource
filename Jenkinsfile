pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        PATH = "/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

        IMAGE_NAME = "madhu58/networksource"
        IMAGE_TAG  = "latest"

        CONTAINER_NAME = "networksource"
        CONTAINER_PORT = "8083"
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
                echo "==============================="
                echo "Current User"
                echo "==============================="
                whoami

                echo "==============================="
                echo "Current Directory"
                echo "==============================="
                pwd

                echo "==============================="
                echo "PATH"
                echo "==============================="
                echo $PATH

                echo "==============================="
                echo "Git Version"
                echo "==============================="
                git --version

                echo "==============================="
                echo "Git Status"
                echo "==============================="
                git status

                echo "==============================="
                echo "Latest Commit"
                echo "==============================="
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

        stage('Build Image') {
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

        stage('Run Container') {
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
                kubectl rollout status deployment/networksource --timeout=180s
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

        stage('Cleanup') {
            steps {
                sh '''
                docker image prune -f
                '''
            }
        }
    }

    post {

        success {

            echo "Build Successful"

            sh '''
            echo "Pipeline completed successfully."
            '''

        }

        failure {

            echo "Build Failed"

            sh '''
            echo "Pipeline failed."

            kubectl rollout undo deployment/networksource || true
            '''

        }

        always {

            sh '''
            docker ps -a

            docker images
            '''

            cleanWs()

        }
    }
}