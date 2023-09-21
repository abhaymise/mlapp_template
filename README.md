This module contains the common structure that any AI app should have.

```
APP_NAME
    +---app : Contains all  external facing code
    |   |   __init__.py
    |   +---apis : Contains http api codes
    |   |       app.py
    |   +---webapp : Contains any web app code like streamlit
    |           git.init       
    +---docker : Contains container related files
    |       .dockerignore
    |       dockerfile
    +---mlapp : Contains the main source code of the app
    |       __init__.py
    +---scripts : Contains all sheel scripts related to project
    |       setup.sh
    +---tests : Contains unit tests of the project
    |       
    |--tools : Contains any utlity, examples. notebooks
    |   .gitignore
    |   main.py
    |   README.md
    |   Requirements.txt   
```
