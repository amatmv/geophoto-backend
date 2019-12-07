# geophoto-backend

GeoDjango server for the GeoPhoto Android app

## Configurar docker per encapsular el PostGIS

Per aixecar el container utilitzant la comanda: 

`docker run --name=postgis -d -e POSTGRES_USER=geophoto -e POSTGRES_PASS=geophoto -e POSTGRES_DBNAME=geophoto -p 5432:5432 kartoza/postgis:9.6-2.4`

## Clonar el repositori

Hem de tenir instal·lat el Python 3.6 i el PyPi versió 3.

Farem l'entorn virtual i instal·larem les dependències del servidor

```
git clone https://github.com/amatmv/geophoto-backend.git
cd GeoPhoto_Server/
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
