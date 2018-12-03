"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import json
import boto3
from datetime import datetime as dt


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
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


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Allegion Security Service " \
                    "What would you like to do today?"

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I'm really just a rock that has been tricked into thinking, can you rephrase that command so my " \
                    "pea sized brain can understand it"
    should_end_session = False
    #s3_send()
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using the Allegion Security Protocol. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def s3_send(package, code):

    s3 = boto3.client('s3')
    KEY = 'Access.json'
    # Get json object file
    json_obj = s3.get_object(Bucket='securityconfigs', Key=KEY)
    json_dict = json.loads(json_obj['Body'].read().decode('utf-8'))
    err = False
    # Change dictionary package here:
    user = list(package.keys())[0]
    if code == 'g':
        json_dict[user] = package[user]
    elif code == 'm':
        if user in json_dict:
            for key in package[user]:
                if key == 'Time':
                    for subkey in package[user][key]:
                        json_dict[user][key][subkey] = package[user][key][subkey]
                else:
                    json_dict[user][key] = package[user][key]
        else:
            err = True
    elif code == 'r':
        if user in json_dict:
            for key in package[user]:
                json_dict[user][key] = package[user][key]
        else:
            err = True

    # Write to S3 Bucket
    s3.put_object(Body=bytes(json.dumps(json_dict).encode('UTF-8')), Bucket='securityconfigs', Key=KEY)
    return err


def give_access(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    speech_output = "There was an error processing your request"
    reprompt_text = "please try again"

    if 'Identifier' in intent['slots'] and 'value' in intent['slots']['Identifier']:
        user = intent['slots']['Identifier']['value']

        if 'AccessArea' in intent['slots'] and 'value' in intent['slots']['AccessArea']:
            area = intent['slots']['AccessArea']['value']

            if 'AccessTime' in intent['slots'] and 'value' in intent['slots']['AccessTime']:
                end_time = intent['slots']['AccessTime']['value']
                time = dt.time(dt.now())
                mins = str(time.minute).replace(" ", "0")
                hour = str(time.hour).replace(" ", "0")
                start_time = hour + ":" + mins
                attempts = 3

                if 'AccessAttempts' in intent['slots'] and 'value' in intent['slots']['AccessAttempts']:
                    attempts = intent['slots']['AccessAttempts']['value']

                speech_output = "Thank you, " + str(user) + " has access to " + str(area) + " for " + end_time
                reprompt_text = "Would you like to do anything else?"
                package = {user: {"Access": "general", "Time Stamp": start_time, "Attempts": attempts, "Area": area, "Time":
                    {"start": start_time, "end": end_time}}}
                err = s3_send(package, "g")

            elif 'AccessTimePeriodStart' in intent['slots'] and 'AccessTimePeriodEnd' in intent['slots'] and \
                            'value' in intent['slots']['AccessTimePeriodStart'] and \
                            'value' in intent['slots']['AccessTimePeriodEnd']:
                speech_output = "Thank you, " + str(user) + " has access to " + str(area) + " from " + \
                                intent['slots']['AccessTimePeriodStart']['value'] + " until " + \
                                intent['slots']['AccessTimePeriodEnd']['value']
                reprompt_text = "Would you like to do anything else?"
                attempts = 3
                if 'AccessAttempts' in intent['slots'] and 'value' in intent['slots']['AccessAttempts']:
                    attempts = intent['slots']['AccessAttempts']['value']

                time = dt.time(dt.now())
                mins = str(time.minute).replace(" ", "0")
                hour = str(time.hour).replace(" ", "0")
                time_stamp = hour + ":" + mins
                package = {user: {"Access": "general", "Time Stamp":time_stamp, "Attempts": attempts, "Area": area, "Time":
                    {"start": intent['slots']['AccessTimePeriodStart']['value'],
                     "end": intent['slots']['AccessTimePeriodEnd']['value']}}}
                err = s3_send(package, "g")

            else:
                speech_output = "You need to give me a time or duration that " + user + " can access " + area + " for"
                reprompt_text = "Please re-issue command with a time or duration specified"

        else:
            if 'AccessTime' in intent['slots'] and 'value' in intent['slots']['AccessTime']:
                end_time = intent['slots']['AccessTime']['value']
                time = dt.time(dt.now())
                mins = str(time.minute).replace(" ", "0")
                hour = str(time.hour).replace(" ", "0")
                start_time = hour + ":" + mins
                attempts = 3

                if 'AccessAttempts' in intent['slots'] and 'value' in intent['slots']['AccessAttempts']:
                    attempts = intent['slots']['AccessAttempts']['value']

                speech_output = "Thank you, " + str(user) + " has general access for " + end_time
                reprompt_text = "Would you like to do anything else?"
                package = {user: {"Access": "general", "Time Stamp":start_time, "Attempts": attempts, "Area": "General Area", "Time":
                    {"start": start_time, "end": end_time}}}
                s3_send(package, "g")

            elif 'AccessTimePeriodStart' in intent['slots'] and 'AccessTimePeriodEnd' in intent['slots'] and \
                            'value' in intent['slots']['AccessTimePeriodStart'] and \
                            'value' in intent['slots']['AccessTimePeriodEnd']:
                speech_output = "Thank you, " + str(user) + " has general access from " + \
                                intent['slots']['AccessTimePeriodStart']['value'] + " until " + \
                                intent['slots']['AccessTimePeriodEnd']['value']
                reprompt_text = "Would you like to do anything else?"
                attempts = 3
                if 'AccessAttempts' in intent['slots'] and 'value' in intent['slots']['AccessAttempts']:
                    attempts = intent['slots']['AccessAttempts']['value']

                time = dt.time(dt.now())
                mins = str(time.minute).replace(" ", "0")
                hour = str(time.hour).replace(" ", "0")
                time_stamp = hour + ":" + mins
                package = {user: {"Access": "general", "Time Stamp": time_stamp, "Attempts": attempts, "Area": "General Area", "Time":
                    {"start": intent['slots']['AccessTimePeriodStart']['value'],
                     "end": intent['slots']['AccessTimePeriodEnd']['value']}}}
                s3_send(package, "g")

            else:
                speech_output = "You need to give me a time or duration that " + user + " has access"
                reprompt_text = "Please re-issue command with a time or duration specified"

    else:
        speech_output = "You need to give me an identifier to recognize a specific person"
        reprompt_text = "Please re-issue command with a person specified"
    if err:
        speech_output = "The Person you specified is not in the database"
        reprompt_text = "Please re-issue command with a correct person specified"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def remove_access(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Identifier' in intent['slots'] and 'value' in intent['slots']['Identifier']:
        user = intent['slots']['Identifier']['value']

        speech_output = user + " deleted."
        reprompt_text = "Would you like to do anything else?"
        package = {user: "No Access"}
        time = dt.time(dt.now())
        mins = str(time.minute).replace(" ", "0")
        hour = str(time.hour).replace(" ", "0")
        time_stamp = hour + ":" + mins
        if 'AccessArea' in intent['slots'] and 'value' in intent['slots']['AccessArea']:
            area = intent['slots']['AccessArea']['value']
            speech_output = user + " has had their access to area: " + area + " revoked"
            reprompt_text = "Would you like to do anything else?"
            package = {user: {"Access": "None", "Time Stamp": time_stamp, "Attempts": 0, "Area": area}}

        else:
            package = {user: {"Access": "None", "Time Stamp": time_stamp, "Attempts": 0}}

            err = s3_send(package, "r")

    else:
        speech_output = "You need to give me an identifier to recognize a specific person"
        reprompt_text = "Please re-issue command with a person specified"

    if err:
        speech_output = "The Person you specified is not in the database"
        reprompt_text = "Please re-issue command with a correct person specified"
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def modify_access(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Identifier' in intent['slots'] and 'value' in intent['slots']['Identifier']:
        user = intent['slots']['Identifier']['value']
        time = dt.time(dt.now())
        mins = str(time.minute).replace(" ", "0")
        hour = str(time.hour).replace(" ", "0")
        time_stamp = hour + ":" + mins

        if 'AccessTime' in intent['slots'] and 'value' in intent['slots']['AccessTime']:
            t_period = intent['slots']['AccessTime']['value']
            time = dt.time(dt.now())
            mins = str(time.minute).replace(" ", "0")
            hour = str(time.hour).replace(" ", "0")
            start_time = hour + ":" + mins
            speech_output = "Thank you, " + user + "'s time has been extended by " + str(t_period)
            reprompt_text = "Would you like to do anything else?"
            package = {user: {"Time Stamp": time_stamp, "Time": {"start": start_time, "end": t_period}}}
            err = s3_send(package, "m")

        elif 'AccessTimePeriodStart' in intent['slots'] and 'value' in intent['slots']['AccessTimePeriodStart']:
            start_time = intent['slots']['AccessTimePeriodStart']['value']
            speech_output = "Thank you, " + user + "'s hours have been changed to start at: " + str(start_time)
            reprompt_text = "Would you like to do anything else?"
            package = {user: {"Time Stamp": time_stamp, "Time": {"start": start_time}}}
            err = s3_send(package, "m")

        elif 'AccessTimePeriodEnd' in intent['slots'] and 'value' in intent['slots']['AccessTimePeriodEnd']:
            end_time = intent['slots']['AccessTimePeriodEnd']['value']
            speech_output = "Thank you, " + user + "'s hours have been changed to end at: " + str(end_time)
            reprompt_text = "Would you like to do anything else?"
            package = {user: {"Time Stamp": time_stamp, "Time": {"end": end_time}}}
            err = s3_send(package, "m")

        elif 'AccessAttempts' in intent['slots'] and 'value' in intent['slots']['AccessAttempts']:
            attempts = intent['slots']['AccessAttempts']['value']
            speech_output = "Thank you, " + str(user) + " has been given " + str(attempts) + " additional attempts"
            reprompt_text = "Would you like to do anything else?"
            package = {user: {"Time Stamp": time_stamp, "Attempts": attempts}}
            err = s3_send(package, "m")

        else:
            speech_output = "You need to give me something to change"
            reprompt_text = "Please re-issue command "



    else:
        speech_output = "You need to give me an identifier to recognize a specific person"
        reprompt_text = "Please re-issue command with a person specified"

    if err:
        speech_output = "The Person you specified is not in the database"
        reprompt_text = "Please re-issue command with a correct person specified"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

        
def invalid_command(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    speech_output = "The Command you used is not recognized"
    reprompt_text = "Please re-issue command"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

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
    if intent_name == "GiveAccess":
        return give_access(intent, session)
    elif intent_name == "RemoveAccess":
        return remove_access(intent, session)
    elif intent_name == "ModifyAccess":
        return modify_access(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name == "AMAZON.StopIntent":
        return get_welcome_response()
    else:
        return invalid_command(intent, session)


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

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
