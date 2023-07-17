pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                cleanWs()
                script {
                    def d = new Date()
                    def now = d.format("yyyyMMddHHmmss")
                    withCredentials([usernamePassword(credentialsId: 'GitHub', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                        bat """
                            git clone https://github.com/egartley/records.git
                            cd records/${RECORDTYPE}
                            python generate-html.py
                            cd ../../
                            git clone https://${USERNAME}:${PASSWORD}@github.com/${USERNAME}/net.git
                            cd net
                            git remote set-url origin https://${USERNAME}:${PASSWORD}@github.com/${USERNAME}/net.git
                            git checkout -b jenkins-${now}
                            xcopy \"../records/${RECORDTYPE}/${RECORDTYPE}.html\" \"_pages/records/${RECORDTYPE}.html\" /q /y /F
                            git add .
                            git config --global user.email "evanmgartley@gmail.com"
                            git config --global user.name \"${USERNAME}\"
                            git commit -m \"Update ${RECORDTYPE} records\"
                            git push --set-upstream origin jenkins-${now}
                        """
                    }
                }
            }
        }
    }
}
