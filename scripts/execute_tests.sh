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
RUN_TESTS=API
RUN_TESTS=${RUN_TESTS:=API}
echo "Test run folder - $RUN_TESTS"
echo "Environment - $ENVIRONMENT"
pip install -r requirements.txt --quiet
mkdir -p allure-results
mkdir -p allure-results/archive
mkdir -p allure-results/history

# Run The tests in project folder
echo "Running tests"
# Regular
py.test ${dir}/tests/${RUN_TESTS} --tb=no -m "not useful" --alluredir ${dir}/allure-results/archive/${_now}
# Parallel
#py.test -n auto --dist=loadfile ${dir}/tests/${RUN_TESTS} --tb=no -m "not useful" --alluredir ${dir}/allure-results/archive/${_now}
# Loop
#py.test --count=5 --tb=no ${dir}/tests/${RUN_TESTS} --tb=no -m loop --alluredir ${dir}/allure-results/archive/${_now}
echo "Test run finished"

## Environments settings
cp ${dir}/allure-results/environment.properties ${dir}/allure-results/archive/${_now}

## Copy previous history
mkdir ${dir}/allure-results/archive/${_now}/history
cp ${dir}/allure-results/history/*.json ${dir}/allure-results/archive/${_now}/history

## Generate allure report folder
allure generate ${dir}/allure-results/archive/${_now} -o ${dir}/allure-results/archive/${_now}/generated-report

## Saving current test run to history
rm ${dir}/allure-results/history/*
cp -r ${dir}/allure-results/archive/${_now}/generated-report/history/*.json ${dir}/allure-results/history

find . | grep -E "(__pycache__|\.pyc|\.pyo$|.pytest_cache)" | xargs rm -rf

## Open generated report
allure open ${dir}/allure-results/archive/${_now}/generated-report
