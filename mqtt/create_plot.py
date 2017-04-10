import MySQLdb
import pandas as pd
import plotly.plotly as py
import ConfigParser
from plotly.graph_objs import *


config = ConfigParser.ConfigParser()
config.read('mqtt_logger.cfg')

mysql_host = config.get('mysql','hostname')
mysql_user = config.get('mysql','user')
mysql_password = config.get('mysql','password')
mysql_db = config.get('mysql','database')

#  create table sensor_readings(id int primary key not null auto_increment, recorded_at timestamp default current_timestamp, channel varchar(256), data varchar(256));
db = MySQLdb.connect(mysql_host,mysql_user,mysql_password,mysql_db)
curs=db.cursor()

print "Querying"

curs.execute("select recorded_at,channel,data from sensor_readings where channel like '%temperature'")
temp_rows = curs.fetchall()
temp_df = pd.DataFrame( [[ij for ij in i] for i in temp_rows] )
temp_df.rename(columns={0: 'Timestamp', 1: 'Channel', 2: 'Reading'}, inplace=True);
temp_df = temp_df.sort(['Timestamp'], ascending=[1])

print "Building Plot"

trace1 = Scatter(
    x=temp_df['Timestamp'],
    y=temp_df['Reading'],
    name='Temperature',
    mode='lines'
)
layout = Layout(
    title='All Sensors Temperature',
    xaxis=XAxis( title='Time' ),
    yaxis=YAxis( title='Degrees C' ),
)
data = Data([trace1])
fig = Figure(data=data, layout=layout)

py.plot(fig, filename='home_sensors')
