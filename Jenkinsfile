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
          def hash = sh(script: 'git rev-parse --short HEAD || echo "no-git"', returnStdout: true).trim()
          env.COMMIT_HASH = hash
          env.FRONTEND_IMAGE = "saviant-rag-micro-frontend:${env.COMMIT_HASH}"
          env.BACKEND_IMAGE = "saviant-rag-micro-rag_service:${env.COMMIT_HASH}"
        }

        echo "🔧 COMMIT_HASH: ${env.COMMIT_HASH}"
        echo "📦 FRONTEND_IMAGE: ${env.FRONTEND_IMAGE}"
        echo "📦 BACKEND_IMAGE: ${env.BACKEND_IMAGE}"
      }
    }

    stage('Run Tests') {
      steps {
        sh '''
          if ! command -v pip &>/dev/null; then
            echo "pip not found"; exit 1;
          fi

          pip install uv || python3 -m pip install uv
          uv pip install -r requirements.txt || pip install -r requirements.txt
          python tests/evaluation/run_rag_eval.py
        '''
      }
    }

    stage('Build Docker Images') {
      steps {
        sh '''
          if ! command -v docker &>/dev/null; then
            echo "Docker not installed. Skipping image build."
            exit 1
          fi

          docker build -t ${FRONTEND_IMAGE} ./frontend/app
          docker build -t ${BACKEND_IMAGE} ./backend/rag_service_api
        '''
      }
    }

    stage('(Optional) Push to GCR') {
      when {
        expression { return false } // enable manually when needed
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
