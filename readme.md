1. Качаешь питон 

        sudo apt install python3.9 python3-pip postgresql libpq-dev

3. Качаешь либу для отделенных сред разработки 

        pip install virtualenv

4. Создаешь отдельную среду разработки

        virtualenv venv

5. Запускаешь отдельную среду разработки      

        source venv/bin/activate

6. Устанавливаешь в эту среду все нужные либы      

        pip install flask passlib beautifulsoup4 lxml requests psycopg2

7. Запускаешь проект      

        FLASK_APP=app.py FLASK_ENV=development flask run