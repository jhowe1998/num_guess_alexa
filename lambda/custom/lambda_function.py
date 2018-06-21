from __future__ import print_function


#---------- Helpers that build all of the responses ----------
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return{'outputSpeech':{'type':'SSML', 'ssml':output},'card':{'type':'Simple','title':"SessionSpeechlet - " + title, 'content':"SessionSpeechlet - " + output},
            'reprompt':{'outputSpeech':{'type':'SSML', 'ssml':reprompt_text}}, 'shouldEndSession':should_end_session}

def build_response(speechlet_response):
    return{'version': '1.0', 'response': speechlet_response}


#---------- Functions that control the skill's behavior ----------
def get_welcome_response():
    #If we wanted to initialize the session to have some attributes we could add those here

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "<speak>Welcome to the number guessing game demo. Are you ready?</speak>"

    #If the user either soes not reply to the welcome message or says something that is not understood, they will be prompted again with this text.
    reprompt_text = "<speak>Ready for some intense number guessing?</speak>"
    should_end_session = False

    return build_response(build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "<speak>Thank you for playing with the number guessing demo. Have a nice day!</speak>"

    #Setting this to true ends the session and exits the skill
    should_end_session = True

    return build_response(build_speechlet_response(card_title, speech_output, None, should_end_session))

def handle_fallback_request():
    card_title = "Unknown Intent"
    speech_output = "<speak> <emphasis level=\"strong\">Not quite sure what the <say-as interpret-as=\"expletive\">fuuuuuuuu</say-as> you mean.</emphasis> </speak>"
    should_end_session = False

    return build_response(build_speechlet_response(card_title, speech_output, speech_output, should_end_session))


def game_start_response():
    card_title = "Number Guess Demo"
    speech_output = "<speak>Let's start the game! <amazon:effect name=\"whispered\">Which is not ready at the moment.</amazon:effect> </speak>"
    reprompt_text = "<speak> <emphasis level=\"strong\">What are you looking at?</emphasis> </speak>"
    should_end_session = False

    return build_response(build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

#Add functions so that all the intents are caught


#---------- Events ----------
def on_session_started(session_started_request, session):
    #Called when the session starts

    print("on_session_started requestId=" + session_started_request['requestId'] + ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
    #Called when the user launches the skill without specifying what they want

    print("on_launch requestId=" + launch_request['requestId'] + ", sessionId=" + session['sessionId'])
    return get_welcome_response()

def on_intent(intent_request, session):
    #Called when the user specifies an intent for this skill

    print("on_intent requestId=" + intent_request['requestId'] + ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    #Dispatch to your skill's intent handlers
    if intent_name == "StartGame":
        return game_start_response()
    
    if intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    
    if intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    
    if intent_name == "AMAZON.FallbackIntent":
        return handle_fallback_request()
    
#    else:
#        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    #Called when the user ends the session. Is not called when the skill returns should_end_session = True

    print("on_session_ended requestId=" + session_ended_request['requestId'] + ", sessionId=" + session['sessionId'])
    #Add cleanup logic here


#---------- Main handler ----------
def lambda_handler(event, context):
    #Route the incoming request based on type (LaunchRequest, IntentRequest, etc.) The JOSN body of the request is provided in the event parameter.

    print("event.session.application.applicationId=" + event['session']['application']['applicationId'])

    #Uncomment the if statement and populate with your skil's application ID to prevent someone else from configuring a skill that sends requests to this function.
    '''
    if(event['session']['application']['applicationId'] != "amzn1.echo-sdk-ams.app.[unique-value-here]"):
        raise ValueError("Invalid Application ID")
    '''

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']}, event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "sesionEndedRequest":
        return on_session_ended(event['request'], event['session'])



def test():
    return 'This is a test.'
