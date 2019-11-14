# GeoPhoto_Server

GeoDjango server for the GeoPhoto Android app

## Configurar docker per a correr el servidor

Per aixecar el container utilitzant la comanda: 

`docker run --name=postgis -d -e POSTGRES_USER=geophoto -e POSTGRES_PASS=geophoto -e POSTGRES_DBNAME=geophoto -p 5432:5432 kartoza/postgis:9.6-2.4`

## Clonar el repositori

Farem l'entorn virtual i instal·larem les dependències del servidor

```
python3 -m venv geophoto
source geophoto/bin/activate
git clone https://github.com/amatmv/GeoPhoto_Server.git
cd GeoPhoto_Server/
pip install -r requirements.txt
```
