pipeline {
    agent any

    environment {
        VENV = ".venv"
        PYTHON_WIN = "C:\\TestLeaf\\python.exe"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/RajaRathinaGanesan/API_Cassini.git'
            }
        }

        stage('Setup Python & Dependencies') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                        python3 -m venv $VENV
                        . $VENV/bin/activate
                        python -m pip install --upgrade pip
                        pip install -r requirements.txt
                        '''
                    } else {
                        bat """
                        %PYTHON_WIN% -m venv %VENV%
                        call %VENV%\\Scripts\\activate
                        python -m pip install --upgrade pip
                        pip install -r requirements.txt
                        """
                    }
                }
            }
        }

        stage('Run Pytest') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                        . $VENV/bin/activate
                        pytest -v --disable-warnings --alluredir=allure-results
                        '''
                    } else {
                        bat """
                        call %VENV%\\Scripts\\activate
                        pytest -v --disable-warnings --alluredir=allure-results
                        """
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
