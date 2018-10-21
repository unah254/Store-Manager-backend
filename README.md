# Store-Manager-backend
Store app with api endpoints

[![Build Status](https://travis-ci.org/unah254/Store-Manager-backend.svg?branch=ch-api-v1-161337541)](https://travis-ci.org/unah254/Store-Manager-backend)           [![Maintainability](https://api.codeclimate.com/v1/badges/90d93599d1107b23f1a1/maintainability)](https://codeclimate.com/github/unah254/Store-Manager-backend/maintainability)                                [![Coverage Status](https://coveralls.io/repos/github/unah254/Store-Manager-backend/badge.svg?branch=ch-api-v1-161337541)](https://coveralls.io/github/unah254/Store-Manager-backend?branch=ch-api-v1-161337541)

# Heroku link

https://store-product-management-app.herokuapp.com/

# Documentation


# API Endpoints

| EndPoint                    | Method        | Functionality                 |
| --------------------------  | --------------|------------------------------ |
|  api/v1/products            | GET           | fetch all available products .|
| api/v1/products/<int:Id>    | GET           | fetch  a specific order       |
| api/v1/products             | POST          | add a new product .           |
| api/v1/sales                | POST          | add a new sales record .      |
| api/v1/sales/<int:Id>       | GET           | fetch a specific sale record  |
| api/v1/sales                | GET .         | fetch all sales record .      |
| api/v1/sales/<int:Id> .     | DELETE .      | delete a specific sale record |
| api/v1/products/<int:Id> .  |DELETE .       | delete a specific product .   |
| api/v1/signup               | POST .        | register a new user .         |
| api/v1/login .              | POST .        | login a registered user .     |
 ----------------------------    ---------------  -------------------------------
 

# Prerequisites
1.Python 3: https://www.python.org/downloads/                                        
2.Flask_restful: https://flask-restful.readthedocs.io/en/latest/installation.html

# Running App
- Clone the repo and cd into it.

  ```$ git clone https://github.com/unah254/Store-Manager-backend.git```
  
   ```$ cd Store-Manager-backend```

- Create a virtual environment.

  ```$ virtualenv env```

- Activate the virtual environment.

  ```$ source env/bin/activate``` 

- Set environment to development and export Secret key.

   ```$ export APP_SETTINGS=development```
   
    ```$ export APP_SECRET_KEY="1245th"```

- Run the app.

   ```$ python run.py```

# Testing App

```python -m pytest --cov=app```
