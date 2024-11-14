pipeline {
    agent{label 'blue steel'}

    
    environment {
        PYTHON_VENV = '.venv'
    }


    stages{

          stage('Checkout') {
            steps {
                checkout scm  // Checkout your code from the repository
            }
        }

        
        stage('Set up Python') {
            steps {
                script {
                    // Set up a virtual environment to isolate dependencies
                    sh 'python -m venv ${PYTHON_VENV}'
                    sh '${PYTHON_VENV}/bin/pip install -r requirements.txt'  // Install dependencies
                }
            }
        }




    }


      post {
        always {
            // Clean up after tests
            sh 'rm -rf ${PYTHON_VENV}'
        }
    }
}
