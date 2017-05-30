#!/usr/bin/env python
import paho.mqtt.client as mqtt
import ConfigParser
import MySQLdb
import datetime
import time
import json

config = ConfigParser.ConfigParser()
config.read('mqtt_logger.cfg')

print "waiting 15 seconds so mysql will start"
time.sleep(15)

mysql_host = config.get('mysql','hostname')
mysql_user = config.get('mysql','user')
mysql_password = config.get('mysql','password')
mysql_db = config.get('mysql','database')

#  create table sensor_readings(id int primary key not null auto_increment, recorded_at timestamp default current_timestamp, channel varchar(256), data varchar(256));
db = MySQLdb.connect(mysql_host,mysql_user,mysql_password,mysql_db)
curs=db.cursor()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("sensor/+/+")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #recorded_at
    if str(msg.payload)[0] == '{':
        obj = json.loads(str(msg.payload))
        ts = datetime.datetime.strptime(obj['ts'], "%Y-%m-%dT%H:%M:%S.%fZ")
        curs.execute("INSERT INTO sensor_readings(recorded_at,channel,data) values (%s,%s,%s)",(ts.strftime('%Y-%m-%d %H:%M:%S'),msg.topic,str(obj['reading'])))
    else:
        curs.execute("INSERT INTO sensor_readings(channel,data) values (%s,%s)",(msg.topic,str(msg.payload)))
        
    db.commit()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.48", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
