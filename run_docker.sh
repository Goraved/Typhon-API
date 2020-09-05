#!/usr/bin/env bash
docker build -t api_test_image .
docker run --name test_container -i api_test_image
docker cp test_container:/Typhon/allure-results  ./
docker stop test_container
docker rm test_container


## Install allure
## Linux
#sudo apt-add-repository ppa:qameta/allure
#sudo apt-get update
#sudo apt-get install allure
## Mac
#brew install allure

## Open generated report
LATEST=$(ls -td allure-results/archive/*/ | head -1)
allure open $LATEST/generated-report