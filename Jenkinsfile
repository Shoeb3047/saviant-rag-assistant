pipeline {
    agent any

    environment {
        // Core paths
        PYTHON_PATH = "${WORKSPACE}/.venv/bin/python3"
        PIP_PATH = "${WORKSPACE}/.venv/bin/pip3"
        DOCKER_PATH = '/usr/local/bin/docker'
        
        // Image tags
        COMMIT_HASH = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
        FRONTEND_IMAGE = "saviant-rag-micro-frontend:${env.COMMIT_HASH}"
        BACKEND_IMAGE = "saviant-rag-micro-rag_service:${env.COMMIT_HASH}"
    }

    stages {
        stage('Setup Python Environment') {
            steps {
                sh """
                    # Create clean virtual environment
                    python3 -m venv "${WORKSPACE}/.venv" --clear
                    
                    # Install pinned dependencies first
                    ${env.PIP_PATH} install --upgrade "pip<24.0"
                    ${env.PIP_PATH} install "protobuf==3.20.3" --force-reinstall
                    ${env.PIP_PATH} install "chromadb==0.4.15" --no-deps
                """
            }
        }

        stage('Install Requirements') {
            steps {
                sh """
                    ${env.PIP_PATH} install -r requirements.txt "protobuf==3.20.3"
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

        stage('Docker Build') {
            steps {
                script {
                    // Method 1: Try with credentials first
                    try {
                        withCredentials([usernamePassword(
                            credentialsId: 'docker-hub-creds',
                            usernameVariable: 'DOCKER_USER',
                            passwordVariable: 'DOCKER_PASS'
                        )]) {
                            sh """
                                echo "${DOCKER_PASS}" | ${env.DOCKER_PATH} login -u "${DOCKER_USER}" --password-stdin
                                ${env.DOCKER_PATH} build --no-cache -t ${env.FRONTEND_IMAGE} ./frontend/app
                                ${env.DOCKER_PATH} build --no-cache -t ${env.BACKEND_IMAGE} ./backend/rag_service_api
                            """
                        }
                    } catch (Exception e) {
                        // Method 2: Fallback to insecure pull
                        echo "Falling back to insecure Docker pull"
                        sh """
                            ${env.DOCKER_PATH} logout 2>/dev/null || true
                            ${env.DOCKER_PATH} build --no-cache -t ${env.FRONTEND_IMAGE} ./frontend/app || echo "Frontend build failed"
                            ${env.DOCKER_PATH} build --no-cache -t ${env.BACKEND_IMAGE} ./backend/rag_service_api || echo "Backend build failed"
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            sh 'rm -rf "${WORKSPACE}/.venv"'
            echo "Pipeline execution completed"
        }
        success {
            echo """
            ✅ Successful execution
            Docker images attempted:
            - ${env.FRONTEND_IMAGE}
            - ${env.BACKEND_IMAGE}
            """
        }
    }
}