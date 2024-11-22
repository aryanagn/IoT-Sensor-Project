import unittest
from django.test import TestCase,Client
import paho.mqtt.client as mqtt
from unittest import TestCase, mock
from subscribe.views import *
import time
from .models import Sensors, DataEntries, Entry


client = mqtt.Client("test_client2")
mqttBroker = "mqtt.eclipseprojects.io"

# Create your tests here.
class MyTestCase(TestCase):
    
    # test for publish
    def test_publish(self):
        mqttBroker = "mqtt.eclipseprojects.io"
        client = mqtt.Client("test_client")
        client.connect(mqttBroker)
        client.subscribe("topic")
        (result,mid) = client.publish("topic", "test")
        self.assertEqual(result,0)
        
    # test for unsubscribe without altering paho method
    def test_unsubscribe2(self):
        mqttBroker = "mqtt.eclipseprojects.io"
        client = mqtt.Client("test_client")
        client.connect(mqttBroker)
        topic = 'test_topic'
        # unsubscribe() returns a tuple (result, mid) where result determines success of connection. 0 for success, 1-4 for errors
        # mid = message id
        (result, mid) = client.unsubscribe(topic)
        assert(result == 0)
    
    # test for subscribe without altering paho method
    def test_subscribe2(self):
        mqttBroker = "mqtt.eclipseprojects.io"
        client = mqtt.Client("test_client")
        client.connect(mqttBroker)
        topic = 'test_topic'
        # subscribe() returns a tuple (result, mid) where result determines success of connection. 0 for success, 1-4 for errors
        # mid = message id
        (result, mid) = client.subscribe(topic)
        assert(result == 0)
        
    # test to ensure the sensorList page is loaded
    def test_sensor_list(self):
        self.client = Client()
        response = self.client.get('/sensorList')
        self.assertEqual(response.status_code, 200)
    
    # test to check if client successfully disconnects from broker
    def test_disconnect(self):
        mqttBroker = "mqtt.eclipseprojects.io"
        client = mqtt.Client("test_client")
        client.connect(mqttBroker)
        client.disconnect()
        self.assertEqual(client.is_connected(), False)
        
    # test for connecting client to broker
    def test_connect(self):
        mqttBroker = "mqtt.eclipseprojects.io"
        client = mqtt.Client("test_client")
        client.connect(mqttBroker)
        client.loop_start()  # start the network loop
        time.sleep(1)        # wait for the client to establish a connection
        self.assertTrue(client.is_connected())  # assert that the client is connected
        client.loop_stop()   
        
    # test to ensure that data is being generated upon method call
   # def test_generate_data(self):
      #  entries = len(Entry2.objects.all().values()) # get the initial amount of data in the database
       # generate_data()    # generate theadditional data
       # entries2 = len(Entry2.objects.all().values())    # get the new amount of data in the databse
       # self.assertFalse(entries==entries2) #assert that some data has been added to the database
       # self.assertTrue(entries2==(entries+30)) #30 values should be added to database upon data generation
       
    # test to ensure appropriate client is instantiated with _client_id 
    def test_init(self):
        testClient = init_client('test')
        self.assertTrue(testClient._client_id.decode()=='test')