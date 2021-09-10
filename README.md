# Ecowater2MQTT Docker image

This is the dockerized ecowater-Script from https://gnulnx.net/2020/02/18/ecowater-api-scraping/

It is build for my needs (secure broker and so on). Some perameter are configurable, some aren't yet.

## Build
```bash
docker build -t engelb/ecowater2mqtt:<version> .
```

## Run
```bash
docker run -d \
-e MQTT_ID=<mqtt username> \
-e MQTT_PASS=<mqtt password> \
-e MQTT_HOST=<mqtt host> \
-e MQTT_PORT=<mqtt port> \
-e MQTT_TOPIC=<topic where to publish> \
-e ECOWATER_SERIAL=<AC000W.....> \
-e ECOWATER_EMAIL=<ecowater username> \
-e ECOWATER_PASS=<ecowater password> \ 
engelb/ecowater2mqtt:latest
```
 or by env-file:
 ```
docker run -d --env-file envfile.env engelb/ecowater2mqtt:latest
```