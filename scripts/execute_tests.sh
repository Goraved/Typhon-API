#!/bin/bash
if [[ ! -f requirements.txt ]]; then
    cd ..
fi
source venv/bin/activate

_now=$(date +%Y-%m-%d_%H:%M:%S)
dir=$(pwd)


# Path to base folder of tests
PYTHONPATH="${PYTHONPATH}:${dir}"
export PYTHONPATH

## Set environment
export ENVIRONMENT=${ENVIRONMENT:=dev}
RUN_TESTS=${RUN_TESTS:=api}
echo "Test run folder - $RUN_TESTS"
echo "Environment - $ENVIRONMENT"
pip install -r requirements.txt --quiet
mkdir -p allure-results
mkdir -p allure-results/archive
mkdir -p allure-results/history

# Run The tests in project folder
echo "Running tests"
# Regular
py.test tests/${RUN_TESTS} --tb=no -m "not useful" --alluredir allure-results/archive/${_now}
# Parallel
#py.test -n auto --dist=loadfile tests/${RUN_TESTS} --tb=no -m "not useful" --alluredir allure-results/archive/${_now}
# Loop
#py.test --count=5 --tb=no tests/${RUN_TESTS} --tb=no -m loop --alluredir allure-results/archive/${_now}
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

## Open generated report
allure open allure-results/archive/${_now}/generated-report
