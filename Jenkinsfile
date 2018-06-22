pipeline {
  agent any
  stages {
    stage('One') {
      steps {
        ws(dir: 'foo') {
          sh 'pwd'
        }

        sh 'printenv | sort'
      }
    }
    stage('two') {
      steps {
        sh 'pwd'
      }
    }
  }
}