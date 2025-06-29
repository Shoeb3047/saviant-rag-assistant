pipeline {
  agent any

  environment {
    // Set default paths based on your local environment
    PYTHON_PATH = '/opt/homebrew/bin/python3'
    PIP_PATH = '/opt/homebrew/bin/pip3'
    DOCKER_PATH = '/usr/local/bin/docker'
    COMMIT_HASH = ''
    FRONTEND_IMAGE = ''
    BACKEND_IMAGE = ''
  }

  stages {
    stage('Verify Dependencies') {
      steps {
        script {
          // Check Python
          def pythonExists = sh(script: "command -v ${env.PYTHON_PATH} || command -v python3 || command -v python", returnStatus: true) == 0
          if (!pythonExists) {
            error("❌ Python not found. Install with: brew install python")
          }

          // Check Pip
          def pipExists = sh(script: "command -v ${env.PIP_PATH} || command -v pip3 || command -v pip", returnStatus: true) == 0
          if (!pipExists) {
            error("❌ Pip not found. Install with: curl https://bootstrap.pypa.io/get-pip.py | python3")
          }

          // Check Docker (only warn if missing)
          def dockerExists = sh(script: "command -v ${env.DOCKER_PATH} || command -v docker", returnStatus: true) == 0
          if (!dockerExists) {
            echo "⚠️  Docker not found. Image building will be skipped."
          }

          echo "✅ All required dependencies are available"
        }
      }
    }

    stage('Checkout') {
      steps {
        git branch: 'main', 
             url: 'https://github.com/Shoeb3047/saviant-rag-assistant.git',
             credentialsId: 'github-pat'  // Use your credential ID
      }
    }

    stage('Assign Variables') {
      steps {
        script {
          // Get commit hash with fallback
          env.COMMIT_HASH = sh(
            script: 'git rev-parse --short HEAD || echo "no-commit"', 
            returnStdout: true
          ).trim()
          
          // Set image names
          env.FRONTEND_IMAGE = "saviant-rag-micro-frontend:${env.COMMIT_HASH}"
          env.BACKEND_IMAGE = "saviant-rag-micro-rag_service:${env.COMMIT_HASH}"
          
          // Print debug info
          echo """
          🏷️  Build Information:
          🔧 COMMIT_HASH: ${env.COMMIT_HASH}
          📦 FRONTEND_IMAGE: ${env.FRONTEND_IMAGE}
          📦 BACKEND_IMAGE: ${env.BACKEND_IMAGE}
          """
        }
      }
    }

    stage('Run Tests') {
      steps {
        script {
          try {
            // Use uv if available, fallback to pip
            sh """
              ${env.PIP_PATH} install --quiet --upgrade uv pip
              uv pip install -r requirements.txt || \
              ${env.PIP_PATH} install -r requirements.txt
              
              ${env.PYTHON_PATH} tests/evaluation/run_rag_eval.py
            """
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
      // Optional: Send failure notification
    }
    cleanup {
      echo "🧹 Cleaning up workspace..."
      // Optional: Add cleanup steps
    }
  }
}