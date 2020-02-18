import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
from time import sleep
import json

# Function called when a shadow is updated
def customShadowCallback_Update(payload, responseStatus, token):
    # Display status and data from update request
    if responseStatus == "timeout":
        print("Update request " + token + " time out!")

    if responseStatus == "accepted":
        payloadDict = json.loads(payload)
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Update request with token: " + token + " accepted!")
        print("red: " + str(payloadDict["state"]["reported"]["red"]))
        print("blue: " + str(payloadDict["state"]["reported"]["blue"]))
        print("green: " + str(payloadDict["state"]["reported"]["green"]))
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")

    if responseStatus == "rejected":
        print("Update request " + token + " rejected!")

# Function called when a shadow is deleted
def customShadowCallback_Delete(payload, responseStatus, token):

     # Display status and data from delete request
    if responseStatus == "timeout":
        print("Delete request " + token + " time out!")

    if responseStatus == "accepted":
        print("~~~~~~~~~~~~~~~~~~~~~~~")
        print("Delete request with token: " + token + " accepted!")
        print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")

    if responseStatus == "rejected":
        print("Delete request " + token + " rejected!")


def start():

  # Make sure that Client ID is unique for each device
  myAWSIoTMQTTShadowClient = AWSIoTPyMQTT.AWSIoTMQTTShadowClient("IoTPublishDevice")
  myAWSIoTMQTTShadowClient.configureEndpoint("xxxxxxxxxxxxxxxxxx", 8883)  # Enter the endpoint for your thing
  myAWSIoTMQTTShadowClient.configureCredentials("xxxxxxxxx-root-ca.pem", "xxxxxxxx-private.pem.key", "xxxxxxx.pem.crt") # Enter the path to relevant Key and Root CA

  
  print(myAWSIoTMQTTShadowClient.connect())
  
  BotShadow = myAWSIoTMQTTShadowClient.createShadowHandlerWithName("YourThingName",True)  #Replace with your thing name
  
  
  payload = {"state":{"reported":{"key1":"value1","key2":"value2","key3":"value3","key4":"value4"}}}
    

  try:
     #Updating Device Shadow
     print(BotShadow.shadowUpdate(json.dumps(payload), customShadowCallback_Update, 2))
     time.sleep(2)
  except: 
     print("Error Connecting to AWS IOT")


def endprogram():
    GPIO.cleanup()

if __name__=='__main__':
    try:
        start()
    except KeyboardInterrupt:
        endprogram()
