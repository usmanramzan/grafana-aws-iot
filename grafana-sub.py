import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import json
import time
from influxdb import InfluxDBClient

def customCallback(payload, responseStatus,token):
    
    client = InfluxDBClient(host='127.0.0.1', port=8086, username='influxadmin', password='abc123,.', ssl=False, verify_ssl=False)
    client.switch_database('IOT_Data')

    print("Received a new message: ")
    temp=json.loads(payload)
    print(temp)
    red=temp['state']['reported']['red']
    blue=temp['state']['reported']['blue']
    green=temp['state']['reported']['green']
    color=temp['state']['reported']['color']
    
    data = []
    data.append(
		{
		        "measurement": "rpidata",
		        "tags": {
		                "state": "reported", 
		        },
		        "fields": {
                                "red":red,
	        	                "blue": blue, 
                                "green":green,
                                "color":color
		        }
		      
		}
	)
    
    client.write_points(data)
    print("--------------\n\n")
    

# Create an AWS IoT MQTT Client using TLSv1.2 Mutual Authentication


# Make sure that the Client ID is unique for each device
myAWSIoTMQTTShadowClient = AWSIoTPyMQTT.AWSIoTMQTTShadowClient("GrafanaClient")
myAWSIoTMQTTShadowClient.configureEndpoint("xxxxxxxxxxxxxxxxxx", 8883)  # Enter the endpoint for your thing
myAWSIoTMQTTShadowClient.configureCredentials("xxxxxxxxx-root-ca.pem", "xxxxxxxx-private.pem.key", "xxxxxxx.pem.crt") # Enter the path to relevant Key and Root CA


print(myAWSIoTMQTTShadowClient.connect())

BotShadow = myAWSIoTMQTTShadowClient.createShadowHandlerWithName("YourThingName",True)  #Replace with your thing name


while True:
    try:
        print(BotShadow.shadowGet(customCallback, 2))
        time.sleep(2)
    except:
        print("Error! Cannot connect to AWS IOT")
