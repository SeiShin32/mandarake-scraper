1. Качаешь питон

        sudo apt install python3.9

2. Качаешь либу для отделенных сред разработки 

        pip install virtualenv


3. Создаешь отдельную среду разработки

        virtualenv venv

4. Запускаешь отдельную среду разработки      

        source venv/bin/activate

5. Устанавливаешь в эту среду все нужные либы      

        pip install flask passlib beautifulsoup4 lxml requests

6. Запускаешь проект      

        FLASK_APP=app.py FLASK_ENV=development flask run