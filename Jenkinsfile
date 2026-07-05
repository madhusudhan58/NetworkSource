pipeline {

    agent any

    environment {

        IMAGE_NAME = "madhu58/network-project"

        CONTAINER_NAME = "network-project"

        DOCKER_TAG = "latest"

    }

    stages {

        stage('Checkout') {

            steps {

                git branch: 'main',
                url: 'https://github.com/madhu58/network-project.git'

            }

        }

        stage('Git Info') {

            steps {

                sh 'git status'

                sh 'git log --oneline'

            }

        }

        stage('Build Docker Image') {

            steps {

                sh '''
                docker build \
                -t ${IMAGE_NAME}:${DOCKER_TAG} .
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
                    echo $DOCKER_PASS | docker login \
                    -u $DOCKER_USER \
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

                sh 'docker logs ${CONTAINER_NAME}'

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

                kubectl get svc

                kubectl get deployment

                '''

            }

        }

    }

    post {

        always {

            sh 'docker system prune -f'

        }

        success {

            echo "Pipeline Completed Successfully"

        }

        failure {

            echo "Pipeline Failed"

        }

    }

}