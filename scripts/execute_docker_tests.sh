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

mkdir -p allure_results
mkdir -p allure_results/archive
mkdir -p allure_results/history

# Run The tests in project folder
echo "Running tests"
# Regular run
python3 -m py.test -n auto --dist=loadfile tests/${RUN_TESTS} --alluredir allure_results/archive/${_now}
echo "Test run finished"

## Environments settings
cp allure_results/environment.properties allure_results/archive/${_now}

## Copy previous history
mkdir allure_results/archive/${_now}/history
cp allure_results/history/*.json allure_results/archive/${_now}/history

## Generate allure report folder
allure generate allure_results/archive/${_now} -o allure_results/archive/${_now}/generated-report

## Saving current test run to history
rm allure_results/history/*
cp -r allure_results/archive/${_now}/generated-report/history/*.json allure_results/history

find . | grep -E "(__pycache__|\.pyc|\.pyo$|.pytest_cache)" | xargs rm -rf


find . | grep -E "(__pycache__|\.pyc|\.pyo$|.pytest_cache)" | xargs rm -rf