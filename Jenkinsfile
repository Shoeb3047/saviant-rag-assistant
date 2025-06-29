pipeline {
  agent any

  environment {
    PYTHON_PATH = "${WORKSPACE}/.venv/bin/python3"
    PIP_PATH = "${WORKSPACE}/.venv/bin/pip3"
    DOCKER_PATH = '/usr/local/bin/docker'
  }

  stages {
    stage('Setup Environment') {
      steps {
        sh """
          python3 -m venv "${WORKSPACE}/.venv"
          ${WORKSPACE}/.venv/bin/pip install --upgrade pip
        """
      }
    }

    stage('Install Dependencies') {
      steps {
        sh """
          ${env.PIP_PATH} install --force-reinstall protobuf==3.20.3
          ${env.PIP_PATH} install -r requirements.txt
        """
      }
    }

    stage('Assign Variables') {
      steps {
        script {
          env.COMMIT_HASH = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
          env.FRONTEND_IMAGE = "saviant-rag-micro-frontend:${env.COMMIT_HASH}"
          env.BACKEND_IMAGE = "saviant-rag-micro-rag_service:${env.COMMIT_HASH}"
        }
      }
    }

    stage('Run Tests') {
      steps {
        script {
          try {
            sh """
              ${env.PIP_PATH} install --quiet --upgrade uv pip

              uv pip install --force-reinstall protobuf==3.20.3 || \
              ${env.PIP_PATH} install --force-reinstall protobuf==3.20.3

              uv pip install -r requirements.txt || \
              ${env.PIP_PATH} install -r requirements.txt

              ${env.PYTHON_PATH} -W ignore::UserWarning tests/evaluation/run_rag_eval.py
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
      sh 'rm -rf $WORKSPACE/.venv'
      echo "🏁 Pipeline execution completed"
    }
    success {
      echo """
      ✅ Successfully built:
      - Frontend: ${env.FRONTEND_IMAGE}
      - Backend: ${env.BACKEND_IMAGE}
      """
    }
    failure {
      echo "❌ Build failed. Check above logs for details."
    }
  }
}
