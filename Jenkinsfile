pipeline {
  agent any
  stages {
    stage('One') {
      steps {
        ws(dir: 'foo') {
          sh 'pwd'
        }

      }
    }
    stage('two') {
      steps {
        sh 'pwd'
      }
    }
  }
}