pipeline {
  agent any

  environment {
    // Use virtualenv paths
    PYTHON_PATH = "${WORKSPACE}/.venv/bin/python3"
    PIP_PATH = "${WORKSPACE}/.venv/bin/pip3"
    DOCKER_PATH = '/usr/local/bin/docker'
    COMMIT_HASH = ''
    FRONTEND_IMAGE = ''
    BACKEND_IMAGE = ''
  }

  stages {
    stage('Verify Dependencies') {
      steps {
        script {
          // Check Docker exists (optional)
          def dockerExists = sh(script: "command -v ${env.DOCKER_PATH} || command -v docker", returnStatus: true) == 0
          if (!dockerExists) {
            echo "⚠️  Docker not found. Image building will be skipped."
          }
        }
      }
    }

    stage('Checkout') {
      steps {
        git branch: 'main', 
             url: 'https://github.com/Shoeb3047/saviant-rag-assistant.git',
             credentialsId: 'github-pat'
      }
    }

    stage('Setup Python Environment') {
      steps {
        script {
          // Create virtual environment with specific protobuf version
          sh """
            python3 -m venv "${WORKSPACE}/.venv"
            ${env.PIP_PATH} install --upgrade pip==23.3.2
            ${env.PIP_PATH} install protobuf==3.20.3  # Fix for descriptor error
            ${env.PIP_PATH} install uv
          """
        }
      }
    }

    stage('Assign Variables') {
      steps {
        script {
          // Get commit hash properly
          env.COMMIT_HASH = sh(
            script: 'git rev-parse --short HEAD', 
            returnStdout: true
          ).trim()
          
          if (env.COMMIT_HASH == '') {
            error("Failed to get commit hash")
          }
          
          env.FRONTEND_IMAGE = "saviant-rag-micro-frontend:${env.COMMIT_HASH}"
          env.BACKEND_IMAGE = "saviant-rag-micro-rag_service:${env.COMMIT_HASH}"
          
          echo """
          🏷️  Build Information:
          🔧 COMMIT_HASH: ${env.COMMIT_HASH}
          📦 FRONTEND_IMAGE: ${env.FRONTEND_IMAGE}
          📦 BACKEND_IMAGE: ${env.BACKEND_IMAGE}
          """
        }
      }
    }

    stage('Install Dependencies') {
      steps {
        script {
          // Install requirements with specific protobuf constraint
          sh """
            ${env.PIP_PATH} install -r requirements.txt
            ${env.PIP_PATH} install --upgrade protobuf==3.20.3  # Ensure correct version
          """
        }
      }
    }

    stage('Run Tests') {
      steps {
        script {
          try {
            // Set environment variable for protobuf compatibility
            withEnv(['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python']) {
              sh """
                cd ${WORKSPACE}
                ${env.PYTHON_PATH} tests/evaluation/run_rag_eval.py
              """
            }
          } catch (Exception e) {
            error("❌ Tests failed: ${e.getMessage()}")
          }
        }
      }
    }

    stage('Build Docker Images') {
      when {
        expression { 
          sh(script: "command -v ${env.DOCKER_PATH} || command -v docker", returnStatus: true) == 0 
        }
      }
      steps {
        script {
          try {
            sh """
              ${env.DOCKER_PATH} build -t ${env.FRONTEND_IMAGE} ./frontend/app
              ${env.DOCKER_PATH} build -t ${env.BACKEND_IMAGE} ./backend/rag_service_api
            """
          } catch (Exception e) {
            echo "⚠️  Docker build failed: ${e.getMessage()}"
          }
        }
      }
    }

    stage('(Optional) Push to GCR') {
      when { 
        expression { return false } // Change to true when needed
      }
      steps {
        script {
          echo "🚀 Pushing images to GCR..."
          // Add your GCR push commands here
        }
      }
    }
  }

  post {
    always {
      echo "🏁 Pipeline execution complete"
      // Clean up virtualenv
      sh 'rm -rf "${WORKSPACE}/.venv" || true'
    }
    success {
      echo """
      ✅ Pipeline succeeded!
      Built Images:
      - ${env.FRONTEND_IMAGE}
      - ${env.BACKEND_IMAGE}
      """
    }
    failure {
      echo "❌ Pipeline failed. Check logs for details."
    }
  }
}