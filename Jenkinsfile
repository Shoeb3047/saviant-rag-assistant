pipeline {
  agent any

  environment {
    COMMIT_HASH = ''
    FRONTEND_IMAGE = ''
    BACKEND_IMAGE = ''
  }

  stages {
    stage('Checkout') {
      steps {
        git branch: 'main', url: 'https://github.com/Shoeb3047/saviant-rag-assistant.git'
      }
    }

    stage('Assign and Echo Variables') {
      steps {
        script {
          env.COMMIT_HASH = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
          env.FRONTEND_IMAGE = "saviant-rag-micro-frontend:${env.COMMIT_HASH}"
          env.BACKEND_IMAGE = "saviant-rag-micro-rag_service:${env.COMMIT_HASH}"
        }

        echo "🔧 COMMIT_HASH: ${env.COMMIT_HASH}"
        echo "📦 FRONTEND_IMAGE: ${env.FRONTEND_IMAGE}"
        echo "📦 BACKEND_IMAGE: ${env.BACKEND_IMAGE}"
      }
    }

    stage('Run Tests') {
      agent {
        docker {
          image 'python:3.10-slim'
          args '-u root'
        }
      }
      steps {
        sh '''
          pip install uv
          uv pip install -r requirements.txt
          python tests/evaluation/run_rag_eval.py
        '''
      }
    }

    stage('Build Docker Images') {
      steps {
        sh """
          docker build -t ${env.FRONTEND_IMAGE} ./frontend/app
          docker build -t ${env.BACKEND_IMAGE} ./backend/rag_service_api
        """
      }
    }

    stage('(Optional) Push to GCR') {
      when {
        expression { return false }
      }
      steps {
        echo "🛑 Skipping push to GCR."
      }
    }
  }

  post {
    success {
      echo "✅ Pipeline succeeded. Images built: ${env.FRONTEND_IMAGE} and ${env.BACKEND_IMAGE}"
    }
    failure {
      echo "❌ Pipeline failed."
    }
  }
}
