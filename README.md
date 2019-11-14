# GeoPhoto_Server

GeoDjango server for the GeoPhoto Android app

## Configurar docker per a correr el servidor

Utilitzarem la imatge de docker de [amatmv/postgis](https://github.com/amatmv/docker-postgis)

`docker pull kartoza/postgis`

Crearem la imatge:

```
git clone https://github.com/amatmv/docker-postgis.git
cd docker-postgis
docker build -t postgis . 
```

I aixecarem un container utilitzant la comanda: 

`docker run --name=postgis -d -e POSTGRES_USER=geophoto -e POSTGRES_PASS=geophoto -e POSTGRES_DBNAME=geophoto_db -p 5432:5432 postgis

## Clonar el repositori al docker

`docker exec -it postgis bash`

I ara, estant dins el docker, farem l'entorn virtual i instal·larem les dependències del servidor

```
python3 -m venv geophoto
source geophoto/bin/activate
git clone https://github.com/amatmv/GeoPhoto_Server.git
cd GeoPhoto_Server/
pip install -r requirements.txt
```
