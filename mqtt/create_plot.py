#!/usr/bin/env python
import MySQLdb
import pandas as pd
import plotly as py
import ConfigParser
from plotly.graph_objs import *


config = ConfigParser.ConfigParser()
config.read('/root/raspberry_pi/mqtt/mqtt_logger.cfg')

mysql_host = config.get('mysql','hostname')
mysql_user = config.get('mysql','user')
mysql_password = config.get('mysql','password')
mysql_db = config.get('mysql','database')

#  create table sensor_readings(id int primary key not null auto_increment, recorded_at timestamp default current_timestamp, channel varchar(256), data varchar(256));
db = MySQLdb.connect(mysql_host,mysql_user,mysql_password,mysql_db)
curs=db.cursor()

print "Querying"

curs.execute("select recorded_at,channel,data from sensor_readings where channel like '%temperature' order by recorded_at desc limit 75000")
temp_rows = curs.fetchall()
temp_df = pd.DataFrame( [[ij for ij in i] for i in temp_rows] )
temp_df.rename(columns={0: 'Timestamp', 1: 'Channel', 2: 'Reading'}, inplace=True);
temp_df = temp_df.sort_values(by=['Timestamp'], ascending=[1])

print "Building Plot"

series = []
sensors = temp_df['Channel'].unique()

for sensor in sensors:
    if "linknode" in sensor:
        continue
    if "wemos" in sensor:
        continue
    if "devboard" in sensor:
        continue
    series.append( Scatter(
        x=temp_df[(temp_df['Channel'] == sensor)]['Timestamp'],
        y=temp_df[(temp_df['Channel'] == sensor)]['Reading'],
        name=sensor,
        mode='lines'
    ) )

layout = Layout(
    title='All Sensors Temperature',
    xaxis=XAxis( title='Time' ),
    yaxis=YAxis( title='Degrees C' ),
)
data = Data(series)
fig = Figure(data=data, layout=layout)


print "Querying"

curs.execute("select recorded_at,channel,data from sensor_readings where channel like '%voltage' order by recorded_at desc limit 75000")
volt_rows = curs.fetchall()
volt_df = pd.DataFrame( [[ij for ij in i] for i in volt_rows] )
volt_df.rename(columns={0: 'Timestamp', 1: 'Channel', 2: 'Reading'}, inplace=True);
volt_df = volt_df.sort_values(by=['Timestamp'], ascending=[1])

print "Building Plot"

series2 = []
sensors = volt_df['Channel'].unique()

for sensor in sensors:
    if "linknode" in sensor:
        continue
    if "wemos" in sensor:
        continue
    if "devboard" in sensor:
        continue
    series2.append( Scatter(
        x=volt_df[(volt_df['Channel'] == sensor)]['Timestamp'],
        y=volt_df[(volt_df['Channel'] == sensor)]['Reading'],
        name=sensor,
        mode='lines'
    ) )

layout2 = Layout(
    title='All Sensors Voltage',
    xaxis=XAxis( title='Time' ),
    yaxis=YAxis( title='mV' ),
)
data2 = Data(series2)
fig2 = Figure(data=data2, layout=layout2)

print "Querying"

curs.execute("select recorded_at,channel,data from sensor_readings where channel like '%rssi'  order by recorded_at desc limit 75000")
rssi_rows = curs.fetchall()
rssi_df = pd.DataFrame( [[ij for ij in i] for i in rssi_rows] )
rssi_df.rename(columns={0: 'Timestamp', 1: 'Channel', 2: 'Reading'}, inplace=True);
rssi_df = rssi_df.sort_values(by=['Timestamp'], ascending=[1])

print "Building Plot"

series3 = []
sensors = rssi_df['Channel'].unique()

for sensor in sensors:
    series3.append( Scatter(
        x=rssi_df[(rssi_df['Channel'] == sensor)]['Timestamp'],
        y=rssi_df[(rssi_df['Channel'] == sensor)]['Reading'],
        name=sensor,
        mode='lines'
    ) )

layout3 = Layout(
    title='All Sensors Signal',
    xaxis=XAxis( title='Time' ),
    yaxis=YAxis( title='RSSI' ),
)
data3 = Data(series3)
fig3 = Figure(data=data3, layout=layout3)



print "Uploading Plots to plot.ly"

py.offline.plot(fig, filename='/var/www/html2/home_sensors.html')
py.offline.plot(fig2, filename='/var/www/html2/home_voltage_sensors.html')
py.offline.plot(fig3, filename='/var/www/html2/home_rssi_sensors.html')

