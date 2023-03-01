#!/usr/bin/python3

import json
import os
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import ssl
from datetime import datetime

# https://github.com/barleybobs/ecowater-softener
from ecowater_softener import Ecowater

print(datetime.now())

mqtt_id = os.getenv('MQTT_ID')
mqtt_passw = os.getenv('MQTT_PASS')
mqtt_host = os.getenv('MQTT_HOST')
mqtt_port = int(os.getenv('MQTT_PORT'))
mqtt_topic = os.getenv('MQTT_TOPIC')

ecowater_serial = os.getenv('ECOWATER_SERIAL')
ecowater_email = os.getenv('ECOWATER_EMAIL')
ecowater_passw = os.getenv('ECOWATER_PASS')

# Ecowater-Data
ecowaterDevice = Ecowater(ecowater_email, ecowater_passw, ecowater_serial)
print(ecowaterDevice.getData())

# MQTT server details
auth = {
  'username': mqtt_id,
  'password': mqtt_passw
}

tls = {
  'ca_certs': '/ca.crt',
  'tls_version': ssl.PROTOCOL_TLSv1_2
}

# Publish the message, consisting of all of the json data
publish.single(mqtt_topic,
               payload=json.dumps(ecowaterDevice.getData()),
               qos=2,
               retain=False,
               hostname=mqtt_host,
               client_id=mqtt_id,
               auth=auth,
               tls=tls,
               port=mqtt_port,
               protocol=mqtt.MQTTv311)
print('done.')
