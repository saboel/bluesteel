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

                        checkDetails details = new ChecksDetailsBuilder()
                                .withName("Jenkins CI")
                                .withStatus(ChecksStatus.IN_PROGRESS)
                                .withConclusion(ChecksConclusion.NEUTRAL)  // Mark as neutral until we know the result
                                .withDetailsURL(DisplayURLProvider.get().getRunURL(run))  // Link to the Jenkins build
                                .withCompletedAt(LocalDateTime.now(ZoneOffset.UTC))
                                .build();
                        // Start the GitHub Check (Tests)
                         githubChecks(
                            credentialsId: 'github-token',  // Reference the stored GitHub credentials
                            repoOwner: 'saboel',
                            repository: 'bluesteel',
                            commitSha: env.GIT_COMMIT,
                            checkName: "Jenkins CI",
                            status: ChecksStatus.IN_PROGRESS,  // Mark the check as in-progress                            context: 'Jenkins Tests',
                            conclusion: ChecksConclusion.NEUTRAL,
                            detailsUrl: DisplayURLProvider.get().getRunURL(run),
                            completedAt: LocalDateTime.now(ZoneOffset.UTC)
                        )
                         def testResult = sh(script: "pytest tests", returnStatus: true)
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
