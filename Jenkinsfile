pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/FirdousHani/devops-security-dashboard.git',
                    branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t security-dashboard .'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker stop security-dashboard-container || true'
                sh 'docker rm security-dashboard-container || true'
            }
        }

        stage('Run Docker Container') {
            steps {
                sh 'docker run -d -p 5000:5000 --name security-dashboard-container security-dashboard'
            }
        }

        stage('Health Check') {
            steps {
                sh 'sleep 3 && curl -f http://localhost:5000/health || exit 1'
            }
        }
    }

    post {
        success {
            echo 'Deployment Successful!'
        }
        failure {
            echo 'Pipeline Failed. Check logs.'
        }
    }
}
