## Setup dev environment

This project is [Python](https://www.python.org/) based, so you will need Python to work with it.
For reports generation [Allure](http://allure.qatools.ru/) is used. Install it as well.

```
brew install python3
brew install Allure
```

In Terminal from the main project folder do the following
1. Setup the local virtual env `python3 -m virtualenv venv`
2. Install all the requirements
```
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

Also you can run next script:
```bash
sh scripts/venv.sh
```
### Launch API tests 

Go to `scripts` dir. Execute the following script
```
execute_tests.sh
``` 
