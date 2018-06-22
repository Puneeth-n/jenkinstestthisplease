pipeline {
  agent any
  stages {
    stage('One') {
      steps {
        ws(dir: 'foo') {
          echo 'hello world'
        }

      }
    }
  }
}