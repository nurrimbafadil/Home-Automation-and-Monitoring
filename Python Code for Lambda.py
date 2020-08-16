"""
This code is developed @nurrimbafadil
"""
 
from __future__ import print_function
import xml.etree.ElementTree as etree
from datetime import datetime as dt
import paho.mqtt.client as mqtt

import boto3
import io
import time

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('onsemi')

def on_connect(client, userdata, flags, rc):
    print("connected")
    
def on_subscribe(client, obj, mid, granted_qos):
    print("subscribed")
    
client = mqtt.Client()
client.on_connect = on_connect
#client.on_message = on_message
client.on_subscribe = on_subscribe

client.connect("mqtt.eclipse.org", 1883, 60)

#def on_message(client, obj, msg):
#    received_message = str(msg.payload)
#    print(msg.topic + " " + str(msg.qos) + " " + received_message)

#client.username_pw_set("cnpemclt", "ccZRVtdCTqID")
#client.connect("mqtt.eclipse.org", "1883")

#client.connect("m12.cloudmqtt.com", 15708, 60)
# Start subscribe, with QoS level 0
#client.subscribe("test/door", 0)



def read_table_item(table_name, pk_name, pk_value):
    """
    Return item read by primary key.
    """
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={pk_name: pk_value})
    
    if 'Item' in response:
        value = response['Item']['value']
        #print (value)
           
    return value
    

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    #print("event.session.application.applicationId=" +
         # event['session']['application']['applicationId'])
 
    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")
 
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
 
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
 
 
def on_session_started(session_started_request, session):
    """ Called when the session starts """
 
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])
 
 
def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
 
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()
 
 
def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """
 
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])
 
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
 
    # Dispatch to your skill's intent handlers
    if intent_name == "TemperatureSensorIntent":
        return temperature_read(intent, session)
    elif intent_name == "HumiditySensorIntent":
        return humidity_read(intent, session)
    elif intent_name == "LightSensorIntent":
        return light_read(intent, session)
    elif intent_name == "LightRequiredIntent":
        return light_required(intent, session)
    elif intent_name == "PressureSensorIntent":
        return pressure_read(intent, session)
    elif intent_name == "AirqualitySensorIntent":
        return airquality_read(intent, session)
    elif intent_name == "AllSensorIntent":
        return all_sensor_read(intent, session)
    elif intent_name == "ControlLightIntent":
        return turn_on_light(intent, session)
    elif intent_name == "ControlLightOffIntent":
        return turn_off_light(intent, session)
    elif intent_name == "FanOnIntent":
        return turn_on_fan(intent, session)
    elif intent_name == "FanOffIntent":
        return turn_off_fan(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.StopIntent" or intent_name == "AMAZON.CancelIntent":
        return session_end(intent, session)
    else:
        raise ValueError("Invalid intent")

 
def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
 
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here
 
# --------------- Functions that control the skill's behavior ------------------
 
 
def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
 
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the room app. " \
                    "I know your room temperature, humidity, light intensity, air quality, air pressure. " \
                    " You can ask me about any parameter."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please ask me like, " \
                    "What is the temperature?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def temperature_read(intent, session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    result = read_table_item("onsemi", "serial", "temperature")
	#temperature = float("{0:.2f}".format(result))
    session_attributes = {}
    card_title = "Reading Temperature"
    speech_output = "The room temperature is {0:.2f} degree centigrade.".format(result)
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = ""
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
 
def humidity_read(intent, session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    result = read_table_item("onsemi", "serial", "humidity")
	#humidity = float("{0:.2f}".format(result))
    session_attributes = {}
    card_title = "Reading Humidity"
    speech_output = "The humidity is {0:.2f} percent.".format(result)
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def light_read(intent, session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    result = read_table_item("onsemi", "serial", "light")
	#temperature = float("{0:.2f}".format(result))
    session_attributes = {}
    card_title = "Reading Light"
    speech_output = "The light intensity in your room is %d Lumen per square meter." %(result)
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def pressure_read(intent, session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    result = read_table_item("onsemi", "serial", "pressure")
	#temperature = float("{0:.2f}".format(result))
    session_attributes = {}
    card_title = "Reading Pressure"
    speech_output = "The Atmospheric Pressure in your room is %d hectopascals." %(result)
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def light_required(intent, session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    #client.publish("walabot/robot/arm/...", "pick")
    #time.sleep(2)
    
    result = read_table_item("onsemi", "serial", "light")
	#temperature = float("{0:.2f}".format(result))
    session_attributes = {}
    card_title = "Calculating..."
    if result < 240:
        speech_output = "Your room illumination is not enough for reading. The recommended light level for reading is 250 to 300 lux, where you have only %d lux" %(result)
    elif result >250 and result <=400:
        speech_output = "Yes, your room illumination is good for reading and normal office work." 
    elif result >700:
        speech_output = "Your room illumination is more than enough."
    
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = ""
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def turn_on_light(intent, session):
    """ mqtt message sent to turn on the light
    """
    client.publish("onsemi/light", "1ON")
    time.sleep(2)

    session_attributes = {}
    card_title = "Calculating..."
    
    speech_output = "Light is on."
    
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def turn_off_light(intent, session):
    """ mqtt message sent ot turn off the light
    """
    client.publish("onsemi/light", "2OFF")
    time.sleep(2)

    session_attributes = {}
    card_title = "Calculating..."
    
    speech_output = "Light is off."
    
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def turn_on_fan(intent, session):
    """ sent mqtt message for turning on the fan
    """
    client.publish("onsemi/light", "3ON")
    time.sleep(2)

    session_attributes = {}
    card_title = "Calculating..."
    
    speech_output = "Fan is on."
    
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def turn_off_fan(intent, session):
    """ sent mqtt message for turning off the fan
    """
    client.publish("onsemi/light", "4OFF")
    time.sleep(2)

    session_attributes = {}
    card_title = "Calculating..."
    
    speech_output = "Fan is off."
    
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
        
def airquality_read(intent, session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    result = read_table_item("onsemi", "serial", "airquality")
	#temperature = float("{0:.2f}".format(result))
    session_attributes = {}
    card_title = "Reading TVOC"
    if result <= 50:
        speech_output = "Total Volatile Organic Compounds in your room air is %d Parts per billion. It seems good." %(result)
    elif result >50 and result <=150:
        speech_output = "Total Volatile Organic Compounds in your room air is %d Parts per billion. It seems air quality is not so good." %(result)
    elif result >150 and result <=250:
        speech_output = "Total Volatile Organic Compounds in your room air is %d Parts per billion and air is polluted." %(result)
    
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
 
		
def all_sensor_read(intent, session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    result1 = read_table_item("onsemi", "serial", "temperature")
    result2 = read_table_item("onsemi", "serial", "humidity")
    result3 = read_table_item("onsemi", "serial", "light")
    result4 = read_table_item("onsemi", "serial", "pressure")
    result5 = read_table_item("onsemi", "serial", "airquality")
	#temperature = float("{0:.2f}".format(result))
    session_attributes = {}
    card_title = "Varifying room condition"
    speech_output1 = "Your room temperature is %.2f degree centigrade and humidity is %.2f percent." %(result1, result2)
    speech_output2 = " Ambiant light is %d lux. Atmospheric air pressure in your room is %d hectopascals and air quality is good." %(result3, result4)
    speech_output = speech_output1 + speech_output2
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def session_end(intent, session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "End"
    speech_output = "Thank you for calling me. Have a nice day!"
    
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))        
 
# --------------- Helpers that build all of the responses ----------------------
 
 
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }
 
 
def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
