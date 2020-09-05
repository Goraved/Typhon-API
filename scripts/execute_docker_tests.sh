#!/bin/bash
. /opt/venv/bin/activate

_now=$(date +%Y-%m-%d_%H:%M:%S)
dir=$(pwd)


# Path to base folder of tests
PYTHONPATH="${PYTHONPATH}:${dir}"
export PYTHONPATH

## Set environment
ENVIRONMENT=DEV
RUN_TESTS=${RUN_TESTS:=api}
export TOKEN
TOKEN=d8d730eae31ff24e4ed0152a0a3c12529e76e0a2b62ed5a6836ff3c7ac40488e

mkdir -p allure-results
mkdir -p allure-results/archive
mkdir -p allure-results/history

# Run The tests in project folder
echo "Running tests"
# Regular run
python3 -m py.test -n auto --dist=loadfile ${dir}/tests/${RUN_TESTS} --alluredir ${dir}/allure_reports/archive/${_now}
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