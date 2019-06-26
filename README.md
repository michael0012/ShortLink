# ShortLink
 Website made with the Django backend framework, that shortens urls.
- Install requirements: 
```
 pip install -r requirements.txt
```
- To run: 
```
 python manage.py runserver
```

- To run async Celery Tasks:
- In a second terminal
```
 sudo apt-get install redis-tools
```
- Then
```
 redis-server
```
- In third terminal:
```
 celery -A urlshort worker -l info 
```
- In a fourth terminal:
```
 celery -A urlshort beat -l info
```
