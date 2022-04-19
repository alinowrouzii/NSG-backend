# NSG-backend
Night Sky Gallery Backend written in Django

To run API:
```
cd nightSky
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Note: rename .env.test to .env and then run the API
