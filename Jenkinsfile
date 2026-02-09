pipeline {
    agent any

    environment {
        VENV = ".venv"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/RajaRathinaGanesan/API_Test.git'
            }
        }

        stage('Setup Python') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                        python3 -m venv $VENV
                        . $VENV/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        '''
                    } else {
                        bat '''
                        python -m venv %VENV%
                        call %VENV%\\Scripts\\activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                        '''
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                        . $VENV/bin/activate
                        pytest --alluredir=allure-results
                        '''
                    } else {
                        bat '''
                        call %VENV%\\Scripts\\activate
                        pytest --alluredir=allure-results
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            allure(
                includeProperties: false,
                jdk: '',
                results: [[path: 'allure-results']]
            )
        }
    }
}
