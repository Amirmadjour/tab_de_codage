# tab_de_codage

## installation

- Clone repo into your local machine

```
git clone git@github.com:Amirmadjour/tab_de_codage.git
```

- Create a Python virtual environment to install your packages without affecting the system-wide installation.

```
cd tab_de_codage
python3 -m venv venv # For Linux (use python -m venv venv for windows)
source venv/bin/activate  # For Linux/macOS(use venv\Scripts\activate for windows)
```

- Install required packages for django

```
cd backend
pip install -r requirements.txt # install the required packages
deactivate # deactivate the virtual enviroment
```

- Install required packages for next js

```
cd ../frontend
npm i
```

## Development

You need two terminals

First terminal

```
cd frontend
npm run dev
```

Second terminal

```
cd backend
python manage.py runserver
```
