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
    speech_output = "Welcome to the Allegeon Security Service " \
                    "What would you like to do today?"

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me your favorite color by saying, " \
                    "my favorite color is red."
    should_end_session = False
    #s3_send()
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def set_color_in_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Color' in intent['slots']:
        favorite_color = intent['slots']['Color']['value']
        session_attributes = create_favorite_color_attributes(favorite_color)
        speech_output = "I now know your favorite color is " + \
                        favorite_color + \
                        ". You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
        reprompt_text = "You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
    else:
        speech_output = "I'm not sure what your favorite color is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your favorite color is. " \
                        "You can tell me your favorite color by saying, " \
                        "my favorite color is red."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def s3_send(package, filename):
    string = "hey todd"

    file_name = filename
    lambda_path = "/tmp/" + file_name
    s3_path = file_name

    with open(lambda_path, 'w+') as file:
        file.write(package)
        file.close()

    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(lambda_path, 'securityconfigs', s3_path)


def give_access(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Identifier' in intent['slots'] and 'value' in intent['slots']['Identifier']:
        user = intent['slots']['Identifier']['value']

        if 'AccessArea' in intent['slots'] and 'value' in intent['slots']['AccessArea']:
            area = intent['slots']['AccessArea']['value']

            if 'AccessTime' in intent['slots'] and 'value' in intent['slots']['AccessTime']:
                t_period = intent['slots']['AccessTime']['value']
                speech_output = "Thank you, User, Area and Time Confirmed"
                reprompt_text = "Would you like to do anything else?"
                package = {user: {"Area": area, "Time": t_period}}
                s3_send(str(package), "GiveAccess.txt")


            else:
                speech_output = "You need to give me a time or duration that " + user + " can access " + area + " for"
                reprompt_text = "Please re-issue command with a time or duration specified"

        else:
            speech_output = "You need to give me an area that " + user + "can access"
            reprompt_text = "Please re-issue command with an area specified"

    else:
        speech_output = "You need to give me an identifier to recognize a specific person"
        reprompt_text = "Please re-issue command with a person specified"


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
        if 'AccessArea' in intent['slots'] and 'value' in intent['slots']['AccessArea']:
            area = intent['slots']['AccessArea']['value']
            speech_output = user + " has had their access to area: " + area + " revoked"
            reprompt_text = "Would you like to do anything else?"
            package = {user: {"Area": area}}

        s3_send(str(package), "RemoveAccess.txt")

    else:
        speech_output = "You need to give me an identifier to recognize a specific person"
        reprompt_text = "Please re-issue command with a person specified"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def modify_access(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Identifier' in intent['slots'] and 'value' in intent['slots']['Identifier']:
        user = intent['slots']['Identifier']['value']

        if 'AccessTime' in intent['slots'] and 'value' in intent['slots']['AccessTime']:
            t_period = intent['slots']['AccessTime']['value']
            speech_output = "Thank you, User, and Time Modified"
            reprompt_text = "Would you like to do anything else?"
            package = {user: {"Time": t_period}}
            s3_send(str(package), "GiveAccess.txt")

        else:
            speech_output = "You need to give me a time or duration to extend"
            reprompt_text = "Please re-issue command with a time or duration specified"

    else:
        speech_output = "You need to give me an identifier to recognize a specific person"
        reprompt_text = "Please re-issue command with a person specified"

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
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
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