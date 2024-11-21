pipeline {
    agent { label 'blue-steel' }

    environment {
        PYTHON_VENV = '.venv'
        GITHUB_TOKEN = credentials('github-token')  // GitHub token from Jenkins credentials store
    }

    stages {

        stage('Notify GitHub - In Progress') {
            steps {
                script {
                    // Trigger GitHub Status API to set status as "pending" (in-progress)
                    def commitSha = bat(script: 'git rev-parse HEAD', returnStdout: true).trim()
                    githubCommitStatus(
                        context: 'jenkins/build', 
                        status: 'pending', 
                        targetUrl: '${env.JENKINS_URL}/job/${JOB_NAME}/${BUILD_NUMBER}/console', 
                        description: 'Build is in progress', 
                        sha: commitSha
                    )
                }
            }
        }

        


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
                    echo "Running build ${env.BUILD_ID}"
                    def testResult = bat(script: 'py main.py', returnStatus: true)

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
                 def targetUrl = "${env.JENKINS_URL}/job/${JOB_NAME}/${BUILD_NUMBER}/console"

            bat """
                curl -X POST ^
                -H "Content-Type: application/json" ^
                -H "Authorization: token %GITHUB_TOKEN%" ^
                -d "{\\"state\\": \\"success\\", \\"context\\": \\"continuous-integration/jenkins\\", \\"description\\": \\"Jenkins build successful\\", \\"target_url\\": \\"${targetUrl}\\"}" ^
                "https://api.github.com/repos/saboel/bluesteel/statuses/${commitSha}"
            """
            }
        }

        failure {
            // Send failure status to GitHub if the build fails
            script {
                def commitSha = env.GIT_COMMIT
                def targetUrl = "${env.JENKINS_URL}/job/${JOB_NAME}/${BUILD_NUMBER}/console"

            bat """
                curl -X POST ^
                -H "Content-Type: application/json" ^
                -H "Authorization: token %GITHUB_TOKEN%" ^
                -d "{\\"state\\": \\"failure\\", \\"context\\": \\"continuous-integration/jenkins\\", \\"description\\": \\"Jenkins build failed\\", \\"target_url\\": \\"${targetUrl}\\"}" ^
                "https://api.github.com/repos/saboel/bluesteel/statuses/${commitSha}"
            """
            }
        }
    }
}



// Make the code more meaningful: Use repo names of things you enjoy: movies, funny clips, etc. 
//This gives the name more depth and meaning but also ensure it sticks to what you are trying to do 
//A new love for Dream baby dream 
//

