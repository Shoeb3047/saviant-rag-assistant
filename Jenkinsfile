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
        checkout([
          $class: 'GitSCM',
          branches: [[name: '*/main']],
          userRemoteConfigs: [[
            url: 'https://github.com/Shoeb3047/saviant-rag-assistant.git',
            credentialsId: 'github-pat'
          ]]
        ])
      }
    }

    stage('Assign and Echo Variables') {
      steps {
        script {
          COMMIT_HASH = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
          env.FRONTEND_IMAGE = "saviant-rag-micro-frontend:${COMMIT_HASH}"
          env.BACKEND_IMAGE = "saviant-rag-micro-rag_service:${COMMIT_HASH}"
          echo "🔧 COMMIT_HASH: ${COMMIT_HASH}"
          echo "📦 FRONTEND_IMAGE: ${env.FRONTEND_IMAGE}"
          echo "📦 BACKEND_IMAGE: ${env.BACKEND_IMAGE}"
        }
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
          docker build -t $FRONTEND_IMAGE ./frontend/app
          docker build -t $BACKEND_IMAGE ./backend/rag_service_api
        """
      }
    }

    stage('(Optional) Push to GCR') {
      when {
        expression { return false }
      }
      steps {
        echo "Skipping push to GCR for now."
      }
    }
  }

  post {
    success {
      echo "✅ Pipeline succeeded. Images built: $FRONTEND_IMAGE and $BACKEND_IMAGE"
    }
    failure {
      echo "❌ Pipeline failed."
    }
  }
}
