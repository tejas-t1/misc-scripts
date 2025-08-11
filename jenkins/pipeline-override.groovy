#!/usr/bin/env groovy
@Library("jenkins-lib@main") _




def releaseTagPattern = "release-*"
def notifyUsers = ['rails_release_notification@intel.com']
def RELEASE_TAG_PREFIX = "release-"

pipeline {
    agent none
    options {
        skipDefaultCheckout true
    }
    stages {
        stage('release') {
            agent {
                kubernetes(agents.winAgent(labelPrefix: "rails-release"))
            }
            options {
                skipDefaultCheckout false
            }
            environment {
                POETRY_REPOSITORIES_NIFTY_GELATO_URL = "https://af-owr.devtools.intel.com/artifactory/api/pypi/adoaddautomation-or-local"
                POETRY_REPOSITORIES_MYSTERIOUS_ADVENTURE_URL = "https://ubit-artifactory-ba.intel.com/artifactory/api/pypi/platform-automation-pypi-ba-local"
            }
            when {
                tag "${releaseTagPattern}"
                beforeOptions true
            }
            steps {
                script {
                    container(agents.container()) {
                        withCredentials([
                            usernamePassword(credentialsId: '49761374-e38d-4cf9-ae23-244f4ef64b98', passwordVariable: 'JENKINS_ADMIN_PASSWORD', usernameVariable: 'JENKINS_ADMIN_USERNAME'),
                            usernamePassword(credentialsId: 'email-and-password', passwordVariable: '_', usernameVariable: 'JENKINS_ADMIN_EMAIL'),
                            usernamePassword(credentialsId: 'artifactory-auth', passwordVariable: 'ARTIFACTORY_APIKEY', usernameVariable: 'ARTIFACTORY_USER')
                        ]) {
                            bat "set"
                            bat "setx HTTP_PROXY http://proxy-dmz.intel.com:911 /m"
                            bat "setx HTTPS_PROXY http://proxy-dmz.intel.com:912 /m"
                            bat "setx NO_PROXY intel.com,.intel.com,10.0.0.0/8,192.168.0.0/16,localhost,127.0.0.0/8,134.134.0.0/16 /m"
                            bat "setx PYPI_INDEX_URL https://af-owr.devtools.intel.com/artifactory/api/pypi/adoaddautomation-or-local/simple"
                            bat "pip -V"
                            bat "pip install -U requests_toolbelt==1.0.0 -i %PYPI_INDEX_URL%"
                            bat "pip install -U poetry==1.5.1 -i %PYPI_INDEX_URL%"
                            bat "poetry --version"
                            bat "poetry config virtualenvs.create false"
                            bat "poetry install --all-extras"
                            bat "set"

                            if (fileExists('pyproject.toml')) {
                                def version = "${TAG_NAME}".substring("${RELEASE_TAG_PREFIX}".length())
                                bat "poetry version ${version}"
                                bat "poetry build --format wheel"
								
								archiveArtifacts artifacts: 'dist/*.whl', fingerprint: true

                                bat "poetry publish --repository nifty_gelato -u ${ARTIFACTORY_USER} -p ${ARTIFACTORY_APIKEY} -v --no-interaction --skip-existing"
                                bat "poetry publish --repository mysterious_adventure -u ${ARTIFACTORY_USER} -p ${ARTIFACTORY_APIKEY} -v --no-interaction --skip-existing"
                            }

                            if (fileExists("jenkins/release.py")) {
                                bat "python jenkins\\release.py"
                            }

                            if (fileExists('docs/make.bat')) {
                                githubpageslib.generateSphinxDocs('docs\\make.bat')
                                githubpageslib.pushSphinxDocs("gh-pages")
                            }
                        }
                    }
                }
            }
            post {
                always {
                    sendNotifications buildStatus: currentBuild.currentResult, emails: notifyUsers
                }
            }
        }
    }
}
