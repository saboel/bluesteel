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

          stage('Test') {
            steps {
                script {
                    // Use credentials from Jenkins' credentials store
                    withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
                        // Start the GitHub Check (Tests)
                        def check = githubChecks(
                            credentialsId: 'github-token',  // Reference the stored GitHub credentials
                            repoOwner: 'saboel',
                            repository: 'bluesteel',
                            commitSha: env.GIT_COMMIT,
                            status: 'in_progress', // 'in_progress' status when tests are running
                            context: 'Jenkins Tests',
                            description: 'Running tests'
                        )
                    }
                }
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
        //also add benchmark tests 
        //what tests?

    }

      post {
        always {
            // Clean up after tests
            bat 'rmdir /s /q %PYTHON_VENV%'
        }
    }
}
