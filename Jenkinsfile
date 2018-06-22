pipeline {
  agent none
  stages {
    stage('One') {
      steps {
        ws(dir: 'foo') {
          ws(dir: 'foo') {
            echo 'hello world'
          }

        }

      }
    }
  }
}