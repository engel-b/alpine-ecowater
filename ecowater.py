#!/usr/bin/python3

import json
import os
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import re
import requests
import ssl
import urllib
from datetime import datetime

# https://gnulnx.net/2020/02/18/ecowater-api-scraping/
print(datetime.now())

# Regex to match the hidden input on the initial log in page
request_validation_re = re.compile(r'<input name="__RequestVerificationToken" type="hidden" value="(.*?)" />')

mqtt_id=os.getenv('MQTT_ID')
mqtt_passw=os.getenv('MQTT_PASS')
mqtt_host=os.getenv('MQTT_HOST')
mqtt_port=int(os.getenv('MQTT_PORT'))
mqtt_topic=os.getenv('MQTT_TOPIC')

ecowater_serial=os.getenv('ECOWATER_SERIAL')
ecowater_email=os.getenv('ECOWATER_EMAIL')
ecowater_passw=os.getenv('ECOWATER_PASS')

# Ecowater-Data
# The serial number of your ecowater device
dsn = { "dsn": ecowater_serial }

# The initial form data
payload = {
    "Email" : ecowater_email,
    "Password" : ecowater_passw,
    "Remember" : 'false'
}

# Ecowater-API-Header
# The headers needed for the JSON request
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language' : 'en-US,en;q=0.5',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0'
}

# MQTT server details
auth = {
  'username':mqtt_id,
  'password':mqtt_passw
}

tls = {
  'ca_certs':"/ca.crt",
  'tls_version':ssl.PROTOCOL_TLSv1_2
}

with requests.Session() as s:
    # Initial GET request
    g = s.get('https://www.wifi.ecowater.com/Site/Login')

    # Grab the token from the hidden input
    tokens = request_validation_re.findall(g.text)

    # Add the token to the form data payload
    payload['__RequestVerificationToken'] = tokens[0]

    # Log in to the site
    login = s.post('https://www.wifi.ecowater.com/Site/Login', data=payload)

    # Add the correct Referer header
    headers['Referer'] = login.url + '/' + dsn['dsn']

    # Query the JSON endpoint for the data that we actually want
    data = s.post('https://www.wifi.ecowater.com/Dashboard/UpdateFrequentData', data=dsn, headers=headers)

    # Load the data in to json
    jsonMsg = json.loads(data.text)

    s.post("https://wifi.ecowater.com/Support/GenerateEASE/" + urllib.parse.quote_plus(ecowater_email) + "/" + ecowater_serial, headers=headers)
    
    # Publish the message, consisting of all of the json data
    publish.single(mqtt_topic,
        payload=json.dumps(jsonMsg),
        qos=2,
        retain=False,
        hostname=mqtt_host,
        client_id=mqtt_id,
        auth=auth,
        tls=tls,
        port=mqtt_port,
        protocol=mqtt.MQTTv311)
print("done.")

