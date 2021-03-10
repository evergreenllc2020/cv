import paho.mqtt.client as mqtt
import json
import cv2
import time

camera1 = 'rtsp://admin:Sakra%40123@10.70.3.188:554/cam/realmonitor?channel=28&subtype=0'
intrucamera = 'rtsp://admin:Sakra%40123@10.70.3.188:554/cam/realmonitor?channel=22&subtype=0'

# MQTT_IP = mqtt_broker_ip 
MQTT_IP = "127.0.0.1" 
MqttTopic = "test"
# maskTopic = "test2"

INTRUSIONMSG= "LINE_OF_FIRE"
MASKMSG = "MASK"
SOCIALMSG = "SOCIAL_DISTANCING"
OVERCROWDINGMSG = "OVERCROWDING"

global flag ,startTime

flag = False

window_name = 'Image'

timeIntv = 9
  
# font 
font = cv2.FONT_HERSHEY_SIMPLEX 
  
# org 
org = (100, 150) 
  
# fontScale 
fontScale = 1
   
# Blue color in BGR 
color = (0, 0, 255) 
  
# Line thickness of 2 px 
thickness = 3
# topics = [(intrusionTopic),(maskTopic)]
# cap1 = cv2.VideoCapture('rtsp://admin:Sakra%40123@10.70.3.188:554/cam/realmonitor?channel=22&subtype=0') 

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(MQTT_IP))
    client.subscribe(MqttTopic)


def on_message(client, userdata, msg):
    ''' Received Data '''
    recMsg = msg.payload.decode()
    recTOPIC = msg.topic
    # print(recMsg)
    global flag
    global startTime
    ''' Drone Id '''
    if msg.topic == MqttTopic:

        if msg.payload.decode() == INTRUSIONMSG and flag == False:
            print("Cam1")
            flag = True 
                
                # Read until video is completed 
            startTime = time.time()
            cap = cv2.VideoCapture('rtsp://admin:Sakra%40123@10.70.3.188:554/cam/realmonitor?channel=22&subtype=0') 
            while(time.time()-startTime < timeIntv): 
                
                # Capture frame-by-frame 
                ret, frame = cap.read() 
                
                if ret == True: 
                    #print(frame.shape)
                    # if (time.time()-startTime < 10):
                    # Display the resulting frame 
                    cv2.putText(frame, INTRUSIONMSG, org, font,fontScale, color, thickness, cv2.LINE_AA)
                    # cv2.resize()
                    cv2.imshow('Frame', frame) 
                    
                    # Press Q on keyboard to  exit 
                    if cv2.waitKey(1) & 0xFF == ord('q'): 
                        break
            
                # Break the loop 
                else:  
                    break
                
                # When everything done, release  
                # the video capture object 
            cap.release() 
            
            # Closes all the frames 
            cv2.destroyAllWindows() 

            startTime = time.time()
            flag = False

   

        elif msg.payload.decode() == MASKMSG and flag == False:
            print("Cam2") 

            flag = True 
                
            # Read until video is completed 
            startTime = time.time()
            cap = cv2.VideoCapture('rtsp://admin:Sakra%40123@10.70.3.188:554/cam/realmonitor?channel=28&subtype=0') 
            while(time.time()-startTime < timeIntv): 
                
                # Capture frame-by-frame 
                ret, frame = cap.read() 
                
                if ret == True: 
                    ##print(frame.shape)
                    # if (time.time()-startTime < 10):
                    # Display the resulting frame 
                    cv2.putText(frame, MASKMSG, org, font,fontScale, color, thickness, cv2.LINE_AA)
                    cv2.imshow('Frame', frame) 
                    
                    # Press Q on keyboard to  exit 
                    if cv2.waitKey(1) & 0xFF == ord('q'): 
                        break
            
                # Break the loop 
                else:  
                    break
                
                # When everything done, release  
                # the video capture object 
            cap.release() 
            
            # Closes all the frames 
            cv2.destroyAllWindows() 

            startTime = time.time()
            flag = False
            

        elif msg.payload.decode() == SOCIALMSG and flag == False:
            print("Cam4") 
            flag = True 
                
            # Read until video is completed 
            startTime = time.time()
            cap = cv2.VideoCapture('rtsp://admin:Sakra%40123@10.70.3.188:554/cam/realmonitor?channel=28&subtype=0') 
            while(time.time()-startTime < timeIntv): 
                
                # Capture frame-by-frame 
                ret, frame = cap.read() 
                
                if ret == True: 
                    ##print(frame.shape)
                    # if (time.time()-startTime < 10):
                    # Display the resulting frame 
                    cv2.putText(frame, SOCIALMSG, org, font,fontScale, color, thickness, cv2.LINE_AA)
                    cv2.imshow('Frame', frame) 
                    
                    # Press Q on keyboard to  exit 
                    if cv2.waitKey(1) & 0xFF == ord('q'): 
                        break
            
                # Break the loop 
                else:  
                    break
                
                # When everything done, release  
                # the video capture object 
            cap.release() 
            
            # Closes all the frames 
            cv2.destroyAllWindows() 

            startTime = time.time()
            flag = False
            
            
        elif msg.payload.decode() == OVERCROWDINGMSG and flag == False:
            print("Cam5")
            flag = True 
                
            # Read until video is completed 
            startTime = time.time()
            cap = cv2.VideoCapture('rtsp://admin:Sakra%40123@10.70.3.188:554/cam/realmonitor?channel=28&subtype=0') 
            while(time.time()-startTime < timeIntv): 
                
                # Capture frame-by-frame 
                ret, frame = cap.read() 
                
                if ret == True: 
                    ##print(frame.shape)
                    # if (time.time()-startTime < 10):
                    # Display the resulting frame 
                    cv2.putText(frame, OVERCROWDINGMSG, org, font,fontScale, color, thickness, cv2.LINE_AA)
                    cv2.imshow('Frame', frame) 
                    
                    # Press Q on keyboard to  exit 
                    if cv2.waitKey(1) & 0xFF == ord('q'): 
                        break
            
                # Break the loop 
                else:  
                    break
                
                # When everything done, release  
                # the video capture object 
            cap.release() 
            
            # Closes all the frames 
            cv2.destroyAllWindows() 

            startTime = time.time()
            flag = False
            


    # if msg.topic == maskTopic:
    #     if msg.payload.decode() == INTRUSIONMSG:
    #         print("Cam2") 
    #     if msg.payload.decode() == MASKMSG:
    #         print("Cam3") 
    #     if msg.payload.decode() == SOCIALMSG:
    #         print("Cam4") 
    #     if msg.payload.decode() == OVERCROWDINGMSG:
    #         print("Cam5")            


client = mqtt.Client()


while True:
    client.connect(MQTT_IP, 1883, 60)
    client.on_connect = on_connect
    client.on_message = on_message
    # client.send_msg = send_msg

    client.loop_forever()
