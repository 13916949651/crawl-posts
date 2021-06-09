pipeline {
  agent any
  // 环境变量，全局可用
  environment {
    // 你的企业唯一标识
    ENTERPRISE = "coding-public"
    // 项目名称
    PROJECT = "python-flask-demo"
    // 制品仓库名称
    ARTIFACT_REPO = "registry"
    // Docker 镜像名称
    IMAGE_NAME = "python-flask-demo"
    // CODING DOMAIN，无需更改
    CODING_DOMAIN = "coding.net"

    // 制品库 Registry 的基础 HOST，无需更改
    ARTIFACT_BASE = "${ENTERPRISE}-docker.pkg.${CODING_DOMAIN}"
    // Docker 镜像全名，无需更改
    ARTIFACT_IMAGE = "${ARTIFACT_BASE}/${PROJECT}/${ARTIFACT_REPO}/${IMAGE_NAME}"
  }
  stages {
    stage('检出') {
      steps {
        // Git checkout，无需更改
        checkout([
          $class: 'GitSCM',
          branches: [[name: env.GIT_BUILD_REF]],
          userRemoteConfigs: [[url: env.GIT_REPO_URL, credentialsId: env.CREDENTIALS_ID]]
        ])
      }
    }
    stage('打包镜像') {
      steps {
        // 根据项目根目录下的 Dockerfile 制作镜像
        sh "docker build -t ${ARTIFACT_IMAGE}:${env.GIT_BUILD_REF} ."
    // 将制作出来的镜像打上标签
        sh "docker tag ${ARTIFACT_IMAGE}:${env.GIT_BUILD_REF} ${ARTIFACT_IMAGE}:latest"
      }
    }
    stage('推送到制品库') {
      steps {
    script {
      // 推送至制品库
          docker.withRegistry("https://${ARTIFACT_BASE}", "${env.DOCKER_REGISTRY_CREDENTIALS_ID}") {
            docker.image("${ARTIFACT_IMAGE}:${env.GIT_BUILD_REF}").push()
               docker.image("${ARTIFACT_IMAGE}:latest").push()
          }
        }
      }
    }
  }
}
