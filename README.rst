### Create virtual environment

`python3 -m venv env`

### Activate virtual environment

`source env/bin/activate`

### Install dependencies

`pip install -r docs/requirements.txt`

### build the documentation

`cd docs`

`make html`

### Open the documentation

`python -m http.server 8080 -d build/html`
