# LabManager GraphQL API
[![CircleCI](https://circleci.com/gh/gigantum/labmanager-service-labbook.svg?style=svg&circle-token=35da44b7cf8ad0cdf2821db40ed11d61287fbdfe)](https://circleci.com/gh/gigantum/labmanager-service-labbook)
[![Coverage Status](https://coveralls.io/repos/github/gigantum/labmanager-service-labbook/badge.svg?t=beG2z0)](https://coveralls.io/github/gigantum/labmanager-service-labbook)

Th LabManager GraphQL API provides all services to manage and manipulate LabBooks.


## Installation

The LabManager API is Python3 only. 

The `gtm` cli tool can help automate a lot of this, but if you want to manually setup and run the API on your host machine 
follow these steps:

1. Install Python 3
    
    OSX
    ```
    brew install python3
    ```
    
    Windows
    ```
    ```
    
2. Create a virtualenv

	Using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/):
	
	```
	mkvirtualenv --python=python3 labmanager
	```
	
3. Clone the `lmcommon` Python library 
([https://github.com/gigantum/labmanager-common](https://github.com/gigantum/labmanager-common))and install all 
system and python dependencies. Follow the installation steps in the README file.
 
4. Install the API python dependencies into your virtualenv:

    ```
    workon labmanager
    pip install -r requirements.txt
    ```
    
## Running the dev server

To run the dev server you must setup your python path so all dependencies are found and run the `service.py` file:

```
cd <labmanager-service-labbook root dir>
workon labmanager
export PYTHONPATH=$PYTHONPATH:<labmanager-service-labbook root dir>:<labmanager-common root dir>
python service.py
```

Navigate your browser to [http://127.0.0.1:5000/labbook/](http://127.0.0.1:5000/labbook/) and you should see the
GraphiQL interface.


## Dumping the GraphQL Schema

To dump the GraphQL schema to a JSON file, setup your python path so all dependencies are found and run the
 `blueprint.py` file:

```
cd <labmanager-service-labbook root dir>
workon labmanager
export PYTHONPATH=$PYTHONPATH:<labmanager-service-labbook root dir>:<labmanager-common root dir>
python blueprint.py
```

The path to the schema.json file will be printed to your console.