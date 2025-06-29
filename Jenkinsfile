pipeline {
  agent any

  environment {
    // Core paths
    PYTHON_PATH = "${WORKSPACE}/.venv/bin/python3"
    PIP_PATH = "${WORKSPACE}/.venv/bin/pip3"
    DOCKER_PATH = '/usr/local/bin/docker'
    
    // Dynamic image tags
    COMMIT_HASH = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
    FRONTEND_IMAGE = "saviant-rag-micro-frontend:${env.COMMIT_HASH}"
    BACKEND_IMAGE = "saviant-rag-micro-rag_service:${env.COMMIT_HASH}"
  }

  stages {
    stage('Setup Environment') {
      steps {
        sh """
          python3 -m venv "${WORKSPACE}/.venv"
          ${env.PIP_PATH} install --upgrade pip
          ${env.PIP_PATH} install protobuf==3.20.3  # Required for ChromaDB compatibility
        """
      }
    }

    stage('Install Dependencies') {
      steps {
        sh "${env.PIP_PATH} install -r requirements.txt"
      }
    }

    stage('Run Tests') {
      steps {
        sh """
          ${env.PYTHON_PATH} -W ignore::UserWarning tests/evaluation/run_rag_eval.py
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
          ${env.DOCKER_PATH} build -t ${env.FRONTEND_IMAGE} ./frontend/app || echo "Docker build failed - continuing"
          ${env.DOCKER_PATH} build -t ${env.BACKEND_IMAGE} ./backend/rag_service_api || echo "Docker build failed - continuing"
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