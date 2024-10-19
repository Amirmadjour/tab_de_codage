# tab_de_codage

## installation

git clone git@github.com:Amirmadjour/tab_de_codage.git
cd tab_de_codage
python3 -m venv venv # For Linux (use python -m venv venv for windows)
source venv/bin/activate  # For Linux/macOS(use venv\Scripts\activate for windows)

cd backend
pip install -r requirements.txt # install the required packages
deactivate # deactivate the virtual enviroment

cd ../frontend
npm i

## Development
You need two terminals

First terminal

cd frontend
npm run dev

Second terminal

cd backend
python manage.py runserver
