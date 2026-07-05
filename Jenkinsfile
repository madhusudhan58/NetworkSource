pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/madhusudhan58/NetworkSource.git'
            }
        }

        stage('Build') {
            steps {
                sh 'echo Building Project'
            }
        }

        stage('Test') {
            steps {
                sh 'echo Testing Project'
            }
        }

        stage('Deploy') {
            steps {
                sh 'echo Deployment Successful'
            }
        }

    }

    post {
        success {
            echo 'Pipeline Completed Successfully'
        }

        failure {
            echo 'Pipeline Failed'
        }
    }
}