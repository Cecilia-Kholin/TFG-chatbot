
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import random

class ActionWhoAreYou(Action):
    def name(self):
        return "action_who_are_you"

    def run(self, dispatcher, tracker, domain):
        response = "Soy un asistente virtual diseñado para responder tus preguntas y ayudarte con información útil. ¿En qué puedo ayudarte?"
        dispatcher.utter_message(text=response)
        return []
    
