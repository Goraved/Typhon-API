#!/bin/bash
. /opt/venv/bin/activate

_now=$(date +%Y-%m-%d_%H:%M:%S)
if [ ! -f requirements.txt ]; then
  cd ..
fi

## Set environment
ENVIRONMENT=DEV
RUN_TESTS=${RUN_TESTS:=api}
export TOKEN

mkdir -p allure-results
mkdir -p allure-results/archive
mkdir -p allure-results/history

# Run The tests in project folder
echo "Running tests"
# Regular run
python3 -m py.test -n auto --dist=loadfile tests/${RUN_TESTS} --alluredir allure-results/archive/${_now}
echo "Test run finished"

## Environments settings
cp allure-results/environment.properties allure-results/archive/${_now}

## Copy previous history
mkdir allure-results/archive/${_now}/history
cp allure-results/history/*.json allure-results/archive/${_now}/history

## Generate allure report folder
allure generate allure-results/archive/${_now} -o allure-results/archive/${_now}/generated-report

## Saving current test run to history
rm allure-results/history/*
cp -r allure-results/archive/${_now}/generated-report/history/*.json allure-results/history

find . | grep -E "(__pycache__|\.pyc|\.pyo$|.pytest_cache)" | xargs rm -rf
