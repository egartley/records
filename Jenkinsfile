pipeline {
    agent any
    parameters {
        choice(name: 'RECORDTYPE', choices: ['games', 'movies', 'khmom-scores', 'tfbl-scores'], description: 'Pick a record type')
    }
    stages {
        stage("Prepare") {
            steps {
                cleanWs()
                sh "mkdir records"
                dir("records") {
                    git poll: false,
                        url: 'https://github.com/egartley/records.git'
                }
                sh "mkdir net"
                dir("net") {
                    git poll: false,
                        url: 'https://github.com/egartley/net.git'
                }
            }
        }
        stage("Build") {
            steps {
                dir("records/${params.RECORDTYPE}") {
                    sh "python3 generate-html.py"
                }
            }
        }
        stage("Deploy") {
            steps {
                script {
                    d = new Date()
                    now = d.format("yyyyMMddHHmmss")
                }
                dir("net") {
                    withCredentials([usernamePassword(credentialsId: 'GitHub', usernameVariable: 'USER', passwordVariable: 'PAT')]) {
                        sh '''
                            git remote set-url origin https://$USER:$PAT@github.com/$USER/net.git
                            git config --global user.email evanmgartley@gmail.com
                            git config --global user.name $USER
                        '''
                    }
                    sh """
                        git checkout -b jenkins-${now}
                        cp \"../records/${params.RECORDTYPE}/${params.RECORDTYPE}.html\" \"_pages/records/${params.RECORDTYPE}.html\"
                    """
                    script {
                        if (params.RECORDTYPE == "games") {
                            sh "cp \"../records/games/game-records-icons.css\" \"resources/css/game-records-icons.css\""
                        }
                    }
                    sh """
                        git add .
                        git commit -m \"Update ${params.RECORDTYPE} records\"
                        git push --set-upstream origin jenkins-${now}
                    """
                }
            }
        }
    }
}
