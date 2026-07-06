pipeline {
    agent any

    environment {
        PATH = "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
    }

    stages {

        stage('Verify Environment') {
            steps {
                sh 'echo "PATH=$PATH"'
                sh 'which docker'
                sh 'docker --version'
            }
        }

    }
}