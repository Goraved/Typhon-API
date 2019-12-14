FROM python:3.7-stretch

# Install Allure.
# See https://github.com/allure-framework/allure-debian/issues/9
RUN apt-get update && apt-get install -y wget default-jdk && cd /opt && \
    (wget -c https://dl.bintray.com/qameta/generic/io/qameta/allure/allure/2.7.0/allure-2.7.0.tgz -O - | tar -xz && chmod +x allure-2.7.0/bin/allure)
ENV PATH="${PATH}:/opt/allure-2.7.0/bin"
RUN allure --version

# Hack: link allure installation under a path Jenkins plugin expects it.
ENV __JENKINS_ALURE_PATH="/root/tools/ru.yandex.qatools.allure.jenkins.tools.AllureCommandlineInstallation"
RUN mkdir -p $__JENKINS_ALURE_PATH && ln -s /opt/allure-2.7.0 $__JENKINS_ALURE_PATH/._allure
