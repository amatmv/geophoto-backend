# GeoPhoto_Server
HTTP Java server for the GeoPhoto Android app

## Configurar docker per a correr el servidor

Utilitzarem la imatge de docker de [amatmv/postgis](https://github.com/amatmv/docker-postgis)

`docker pull kartoza/postgis`

Crearem la imatge:

`git clone git@github.com:amatmv/docker-postgis.git`
`cd docker-postgis`
`docker build -t postgis .`

I aixecarem un container utilitzant la comanda: 

`docker run --name=postgis -d -e POSTGRES_USER=geophoto -e POSTGRES_PASS=geophoto -e POSTGRES_DBNAME=geophoto_db -p 5432:5432 kartoza/postgis:9.6-2.4`
