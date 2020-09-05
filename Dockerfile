FROM ubuntu:18.04 as tests
# Install Python
RUN echo "Installing latest python"
RUN apt-get update
RUN apt-get install -y python3.7
RUN apt-get install -y curl
RUN curl -O https://bootstrap.pypa.io/get-pip.py
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-distutils
RUN python3.7 get-pip.py
RUN python3.7 -m pip install -U setuptools

# Install Chrome
RUN echo "installing Chrome"
RUN apt-get install wget
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get update && apt-get install -y ./google-chrome-stable_current_amd64.deb

# Install Allure.
RUN echo "Installing allure"
# See https://github.com/allure-framework/allure-debian/issues/9
RUN apt-get update && apt-get install -y wget default-jdk && cd /opt && \
    (wget -c https://dl.bintray.com/qameta/generic/io/qameta/allure/allure/2.7.0/allure-2.7.0.tgz -O - | tar -xz && chmod +x allure-2.7.0/bin/allure)
ENV PATH="${PATH}:/opt/allure-2.7.0/bin"
RUN allure --version

# Hack: link allure installation under a path Jenkins plugin expects it.
ENV __JENKINS_ALURE_PATH="/root/tools/ru.yandex.qatools.allure.jenkins.tools.AllureCommandlineInstallation"
RUN mkdir -p $__JENKINS_ALURE_PATH && ln -s /opt/allure-2.7.0 $__JENKINS_ALURE_PATH/._allure

RUN echo "Copying repo"
RUN mkdir /Typhon
WORKDIR /Typhon

COPY * /Typhon/

RUN echo "Installing python packages"
RUN pip install --upgrade pip && \
    pip install virtualenv && \
    virtualenv --python=/usr/bin/python3 /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install -r requirements.txt --quiet

ADD . /Typhon

RUN echo "All done!"
#CMD . /opt/venv/bin/activate && exec python -m py.test tests
CMD . /opt/venv/bin/activate && sh scripts/execute_docker_tests.sh