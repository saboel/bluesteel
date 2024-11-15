pipeline {
    agent{label 'blue-steel'}
    
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
                    bat 'py -m venv %PYTHON_VENV%'
                    bat '%PYTHON_VENV%\\Scripts\\pip install -r requirements.txt'  // Install dependencies
                }
            }
        }

        //add unit tests stage based on certain test cases that need to pass on code checks: like? 

    }

      post {
        always {
            // Clean up after tests
            bat 'rmdir /s /q %PYTHON_VENV%'
        }
    }
}
