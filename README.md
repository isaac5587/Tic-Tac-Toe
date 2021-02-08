## t3-starter

Starter kit for the tic-tac-toe project in CSCI 390: Cloud Computing.

### Setup

Complete all the setup steps in https://docs.google.com/document/d/1WNvt-ci3ELynBo-6zz-8v3NpujIKSSe2H7XNIUAXrt0

### Getting Started

1. Create the database:
    ```bash
    mysql -u root -ppassword -e 'CREATE DATABASE t3;'
    ```
1. Install Python dependencies:
    ```bash
    pipenv install
    ```
1. Start a pipenv shell. All subsequent instructions should be run from this new shell:
    ```bash
    pipenv shell
    ```
1. Generate a new database migration (the player model is the only provided model in models.py):
    ```bash
    flask db revision --autogenerate -m 'player model'
    ```
1. Run your newly minted database migration:
    ```bash
    flask db upgrade
    ```
1. Run the app!
    ```bash
    flask run
    ```
1. Make a JSON request to the app!
    ```bash
    curl -H "Content-Type: application/json" http://localhost:5000
    ```
