from django.shortcuts import render, redirect
from django.http import HttpResponse
import paho.mqtt.client as mqtt
import time, datetime
from random import randrange, uniform
from .models import Sensors, DataEntries, Entry, Entry2, Subscriptions
from django.template import loader
from django.contrib.auth.models import User
from users.views import *

#variables to transfer data
sensor_list = ["sensorX", "sensorY", "sensorZ"]

def sensorList(request):
    context = {
        'sensor_list': getNotSubscribed(request)
        }
    return render(request, 'subscribe/sensorList.html', context)

def sensorRemove(request):
    context = {
        'userSensors': getUserSensors(request)
    }
    return render(request, 'subscribe/sensorRemove.html', context)

def getUserSensors(request):
    user = request.user
    customerName = user.username
    userSensors = []
    subscribed =  Subscriptions.objects.filter(username=customerName)
    for sub in subscribed:
        if(sub.sensorX): userSensors.append('sensorX')
        if(sub.sensorY): userSensors.append('sensorY')
        if(sub.sensorZ): userSensors.append('sensorZ')
    return userSensors

def getNotSubscribed(request):
    sensor_set = set(sensor_list)
    userSensor_set = set(getUserSensors(request))
    return list(sensor_set.symmetric_difference(userSensor_set))

def unsubscribeForm(request):
    user = request.user
    customername = user.username
    sensors = request.POST['sensors']

    obj = Subscriptions.objects.get(username=customername)
    if(sensors=="sensorX"):
        obj.sensorX=False
    if(sensors=="sensorY"):
        obj.sensorY=False
    if(sensors=="sensorZ"):
        obj.sensorZ=False
    obj.save()
    return render(request, 'homePage/homePageTemplate.html', context=show_data(request))


#on_message is callback function for receiving data as a subscriber
#stores data in data structures and database
def on_message(client, userdata, message):
    # create a new entry in the Entry model with the received messaged and the current time
    entry = Entry2(topic=message.topic, data=message.payload.decode(), pub_date=datetime.datetime.now())
    entry.save()
    #print messages, topic
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

def init_client(client_name):
    client = mqtt.Client(client_name) #create new client instance
    
    #attach callback functions:
    client.on_message=on_message        #attach on message function to callback
    client.on_connect=on_connect        #attach on_connect function to callback
    client.on_log=on_log                #attack on_log function to callback
    client.on_disconnect=on_disconnect  #attach disconnect callback
    client.on_subscribe=on_subscribe    #attach subscribe callback
    client.on_publish=on_publish        #attach publish callback
    return client
  
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("good connection, rc=", rc)
    else:
        print("Bad connection, returned code:", rc)
        
    #subcribe to topics when connected
    client.subscribe("sensorX")       #subscribe to topic *MUST BE SUBSCRIBED BEFORE PUBLISH TO RECEIVE MESSAGE*
    client.subscribe("sensorY") 
    client.subscribe("sensorZ") 
    
def on_log(client, userdata, level, buf):
    print("log: ",buf)

def on_publish(client, userdata, mid):
    print("on_publish callback mid= ", str(mid))

def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed")
    
def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected result code ", str(rc))

# generate_data method is used to set up our client and generate the data
def generate_data():
    #instantiate client and broker and sensor model
    print("creating new instance")
    broker_address = "mqtt.eclipseprojects.io"  #online broker
    client = init_client("admin")
   
    #connect, loop, publish, display results
    #note that callback functions are asynchronous on anoter thread so the order may not always appear logical (in logs)
    print("connecting to broker")
    client.connect(broker_address)              #connect to broker
    client.loop_start()                         #start the loop
    time.sleep(4)                               #give client time to establish connection

    #publish data sensor data (mock) - use loop to randomly generate data in lieu of being connected to real data generating sensors
    print("Publishing messages to topics")
    count=0
    while count<10:
        randNumber3 = uniform(20.0, 21.0)
        randNumber2 = uniform(10.0, 15.0)
        randNumber1 = uniform(0.0, 5.0)
        client.publish("sensorX", randNumber1)
        client.publish("sensorY", randNumber2)
        client.publish("sensorZ", randNumber3)
        time.sleep(1)
        count = count +1

    #stop the loop and disconnect client
    time.sleep(4) #wait
    client.loop_stop()
    client.disconnect()

def subscribeForm(request):
    # get user information from logged in User object
    user = request.user
    customername = user.username
    
    # get subscribed sensor from sensor form
    sensors = request.POST['sensors']
    
    # Try to get an instance of MyModel with a specific name
    obj, created = Subscriptions.objects.get_or_create(username=customername)
    
    # Check if the object was created or not
    if created:
        print('A new instance of MyModel was created.')
    else:
        print('An instance of MyModel already exists with this name.')
    
    # if sensors are selected, update the subscriptions in the database.
    if(sensors=="sensorX"):
        obj.sensorX=True
    if(sensors=="sensorY"):
        obj.sensorY=True
    if(sensors=="sensorZ"):
        obj.sensorZ=True
    
    # save the changes
    obj.save()
    results = Subscriptions.objects.filter(username=customername)
    
    # get data from sensor database and send in context
    dataX = Entry2.objects.filter(topic="sensorX")
    dataY = Entry2.objects.filter(topic="sensorY")
    dataZ = Entry2.objects.filter(topic="sensorZ")
    
    # update the context
    context = {
        'results': results, 'dataX': dataX, 'dataY' : dataY, 'dataZ' : dataZ
    }
    return render(request, 'homePage/homePageTemplate.html', context)

def show_data(request):
    # get user based on current logged in user
    user = request.user
    
    # get data parameters from User object and database
    customername = user.username
    dataX = Entry2.objects.filter(topic="sensorX")
    dataY = Entry2.objects.filter(topic="sensorY")
    dataZ = Entry2.objects.filter(topic="sensorZ")
    results = Subscriptions.objects.filter(username=customername)
    
    # append the data to the conext
    context = {
        'results': results, 'dataX': dataX, 'dataY' : dataY, 'dataZ' : dataZ
        }
    return context
