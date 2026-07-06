pipeline {

    agent any

    environment {

        IMAGE_NAME = "madhu58/networksource"

        IMAGE_TAG = "${BUILD_NUMBER}"

        RESOURCE_GROUP = "YOUR_RESOURCE_GROUP"

        AKS_CLUSTER = "YOUR_AKS_CLUSTER"

    }

    stages {

        stage('Checkout') {

            steps {

                git branch: 'main',
                    url: 'https://github.com/madhusudhan58/NetworkSource.git'

            }

        }

        stage('Build Docker Image') {

            steps {

                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'

            }

        }

        stage('Docker Login') {

            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub',
                        usernameVariable: 'USER',
                        passwordVariable: 'PASS'
                    )
                ]) {

                    sh '''
                    echo "$PASS" | docker login -u "$USER" --password-stdin
                    '''

                }

            }

        }

        stage('Push Docker Image') {

            steps {

                sh '''

                docker push $IMAGE_NAME:$IMAGE_TAG

                docker tag $IMAGE_NAME:$IMAGE_TAG $IMAGE_NAME:latest

                docker push $IMAGE_NAME:latest

                '''

            }

        }

        stage('Azure Login') {

            steps {

                withCredentials([
                    file(credentialsId: 'azure-sp', variable: 'AZURE_SP')
                ]) {

                    sh '''
                    az login --service-principal \
                    --username $(jq -r .clientId $AZURE_SP) \
                    --password $(jq -r .clientSecret $AZURE_SP) \
                    --tenant $(jq -r .tenantId $AZURE_SP)
                    '''

                }

            }

        }

        stage('AKS Credentials') {

            steps {

                sh '''
                az aks get-credentials \
                --resource-group $RESOURCE_GROUP \
                --name $AKS_CLUSTER \
                --overwrite-existing
                '''

            }

        }

        stage('Deploy Kubernetes') {

            steps {

                sh '''

                kubectl apply -f deployment.yaml

                kubectl apply -f service.yaml

                kubectl rollout status deployment/networksource

                '''

            }

        }

    }

    post {

        always {

            sh 'docker image prune -f'

        }

    }

}