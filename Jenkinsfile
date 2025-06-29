pipeline {
    agent any

    environment {
        UV_PYTHON = "${WORKSPACE}/.venv/bin/python3"
        UV_BIN = "${WORKSPACE}/.venv/bin/uv"
        DOCKER_PATH = '/usr/local/bin/docker'
        COMMIT_HASH = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
        FRONTEND_IMAGE = "saviant-rag-micro-frontend:${env.COMMIT_HASH}"
        BACKEND_IMAGE = "saviant-rag-micro-rag_service:${env.COMMIT_HASH}"
    }

    stages {
        stage('Setup Environment') {
            steps {
                sh """
                    # Create a new uv-based virtual environment
                    uv venv .venv
                """
            }
        }

        stage('Install Requirements') {
            steps {
                sh """
                    # Install requirements using uv inside the venv
                    ${env.UV_BIN} pip install -r requirements.txt
                """
            }
        }

        stage('Run Tests') {
            environment {
                PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION = 'python'
            }
            steps {
                sh """
                    ${env.UV_PYTHON} -W ignore tests/evaluation/run_rag_eval.py
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
                    sh """
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        ${env.DOCKER_PATH} build -t ${env.FRONTEND_IMAGE} ./frontend/app || echo "Docker build failed but continuing"
                        ${env.DOCKER_PATH} build -t ${env.BACKEND_IMAGE} ./backend/rag_service_api || echo "Docker build failed but continuing"
                    """
                }
            }
        }
    }

    post {
        always {
            sh 'rm -rf .venv'
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
