@echo off

echo Update pip...
call python.exe -m pip install --upgrade pip

echo Update virtual environment...
pip install --upgrade pip

echo Installing virtualenv...
pip install virtualenv

echo Creating virtual environment...
python -m venv env

echo Activating virtual environment...
call .\env\Scripts\activate

echo Update pip in environment...
call python.exe -m pip install --upgrade pip

echo Installing requirements...
pip install -r requirements.txt

echo Creating .env file...
echo FLASK_ENV=development > .env

echo Installation completed.
pause
