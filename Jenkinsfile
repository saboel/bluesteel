pipeline {
    agent { label 'blue-steel' }

    environment {
        PYTHON_VENV = '.venv'
        GITHUB_TOKEN = credentials('github-token')  // GitHub token from Jenkins credentials store
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set up Python') {
            steps {
                script {
                    bat 'py -m venv %PYTHON_VENV%'
                    bat '%PYTHON_VENV%\\Scripts\\pip install -r requirements.txt'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Run tests (adjust based on your testing framework)
                    def testResult = bat(script: 'pytest tests', returnStatus: true)

                    // Check if tests passed (exit status 0)
                    if (testResult == 0) {
                        currentBuild.result = 'SUCCESS'
                    } else {
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
        }
    }

    post {
        success {
            // Send success status to GitHub after a successful build
            script {
                def commitSha = env.GIT_COMMIT
                //def githubToken = credentials('github-token')  // Use the token from Jenkins credentials

                // Curl command in Windows, ensure correct escaping
                bat """
                    curl -X POST ^
                    -H "Content-Type: application/json" ^
                    -H "Authorization: token %GITHUB_TOKEN%" ^
                    -d "{\"state\": \"success\", \"context\": \"continuous-integration/jenkins\", \"description\": \"Jenkins\", \"target_url\": \"${env.JENKINS_URL}/job/${JOB_NAME}/${BUILD_NUMBER}/console\"}" ^
                    "https://api.github.com/repos/saboel/bluesteel/statuses/${commitSha}"
                """
            }
        }

        failure {
            // Send failure status to GitHub if the build fails
            script {
                def commitSha = env.GIT_COMMIT
                //def githubToken = credentials('github-token')

                bat """
                    curl -X POST ^
                    -H "Content-Type: application/json" ^
                    -H "Authorization: token %GITHUB_TOKEN%" ^
                    -d "{\"state\": \"failure\", \"context\": \"continuous-integration/jenkins\", \"description\": \"Jenkins\", \"target_url\": \"${env.JENKINS_URL}/job/${JOB_NAME}/${BUILD_NUMBER}/console\"}" ^
                    "https://api.github.com/repos/saboel/bluesteel/statuses/${commitSha}"
                """
            }
        }
    }
}
