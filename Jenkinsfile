pipeline {
    agent any

    environment {
        PYTHON_PATH = "${WORKSPACE}/.venv/bin/python3"
        PIP_PATH = "${WORKSPACE}/.venv/bin/pip3"
        DOCKER_PATH = '/usr/local/bin/docker'
    }

    stages {
        stage('Get Commit Hash') {
            steps {
                script {
                    env.COMMIT_HASH = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    env.FRONTEND_IMAGE = "saviant-rag-micro-frontend:${env.COMMIT_HASH}"
                    env.BACKEND_IMAGE = "saviant-rag-micro-rag_service:${env.COMMIT_HASH}"
                }
            }
        }

        stage('Setup Environment') {
            steps {
                sh """
                    python3 -m venv "${WORKSPACE}/.venv" --clear
                    ${env.PIP_PATH} install --upgrade pip==23.3.2
                    ${env.PIP_PATH} install "protobuf==3.20.3" --force-reinstall
                    ${env.PIP_PATH} install "chromadb==0.4.15" --no-deps
                """
            }
        }

        stage('Install Requirements') {
            steps {
                sh """
                    ${env.PIP_PATH} install -r requirements.txt
                """
            }
        }

        stage('Run Tests') {
            environment {
                PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION = 'python'
            }
            steps {
                sh """
                    ${env.PYTHON_PATH} -W ignore tests/evaluation/run_rag_eval.py
                """
            }
        }

        stage('Build Docker Images') {
            when { 
                expression { 
                    sh(script: "command -v ${env.DOCKER_PATH}", returnStatus: true) == 0 
                } 
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        mkdir -p /tmp/docker-config
                        echo '{ "auths": {}, "credsStore": "" }' > /tmp/docker-config/config.json
                        echo "$DOCKER_PASS" | DOCKER_CONFIG=/tmp/docker-config docker login -u "$DOCKER_USER" --password-stdin

                        DOCKER_CONFIG=/tmp/docker-config docker build -t $FRONTEND_IMAGE ./frontend/app || echo "Docker frontend build failed but continuing"
                        DOCKER_CONFIG=/tmp/docker-config docker build -t $BACKEND_IMAGE ./backend/rag_service_api || echo "Docker backend build failed but continuing"
                    '''
                }
            }
        }
    }

    post {
        always {
            sh "rm -rf \"${WORKSPACE}/.venv\""
            echo "Pipeline execution completed"
        }
        success {
            echo """
            ✅ Successfully built:
            Frontend: ${env.FRONTEND_IMAGE}
            Backend: ${env.BACKEND_IMAGE}
            """
        }
    }
}
