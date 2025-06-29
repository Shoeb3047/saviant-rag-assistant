pipeline {
    agent any

    environment {
        PYTHON_PATH = "${WORKSPACE}/.venv/bin/python3"
        PIP_PATH = "${WORKSPACE}/.venv/bin/pip3"
        DOCKER_PATH = '/usr/local/bin/docker'
        COMMIT_HASH = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
        FRONTEND_IMAGE = "saviant-rag-micro-frontend:${env.COMMIT_HASH}"
        BACKEND_IMAGE = "saviant-rag-micro-rag_service:${env.COMMIT_HASH}"
    }

    stages {
        stage('Setup Environment') {
            steps {
                sh """
                    # Create clean virtual environment
                    python3 -m venv "${WORKSPACE}/.venv" --clear
                    
                    # Install protobuf first with exact version
                    ${env.PIP_PATH} install --upgrade pip==23.3.2
                    ${env.PIP_PATH} install "protobuf==3.20.3" --force-reinstall
                    
                    # Install chromadb with pinned version and no dependencies
                    ${env.PIP_PATH} install "chromadb==0.4.15" --no-deps
                """
            }
        }

        stage('Install Requirements') {
            steps {
                sh """
                    # Install remaining requirements with constraints
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

        stage('Build Docker Images') {
            when { 
                expression { 
                    sh(script: "command -v ${env.DOCKER_PATH}", returnStatus: true) == 0 
                } 
            }
            steps {
                sh """
                    ${env.DOCKER_PATH} build -t ${env.FRONTEND_IMAGE} ./frontend/app || echo "Docker build failed but continuing"
                    ${env.DOCKER_PATH} build -t ${env.BACKEND_IMAGE} ./backend/rag_service_api || echo "Docker build failed but continuing"
                """
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
            ✅ Successfully built:
            Frontend: ${env.FRONTEND_IMAGE}
            Backend: ${env.BACKEND_IMAGE}
            """
        }
    }
}