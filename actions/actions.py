# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


# Librerías Importadas

from typing import Any, Text, Dict, List

import random
import os
import json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction
# actions.py
from actions.utils import generate_division, explicar_divisiones_incorrectas, generate_enunciado

class ActionSum(Action):

    def name(self) -> Text:
        return "action_sum"

    def run(self, dispatcher: CollectingDispatcher, #dispatcher: Permite enviar mensajes al usuario.
            tracker: Tracker,                       #tracker: Contiene información sobre la conversación actual 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:  #domain: Contiene información sobre la configuración del dominio, como intents y acciones.
        
        # Extraer los números de los mensajes del usuario
        first_number = next(tracker.get_latest_entity_values("number1"), None)
        second_number = next(tracker.get_latest_entity_values("number2"), None)

        
        if first_number and second_number:
            try:
                # Convertir los números a float para manejar decimales
                first_number = float(first_number)
                second_number = float(second_number)

                # Calcular la suma
                result = first_number + second_number
                response = f"La suma de {first_number} y {second_number} es {result:.2f}."
            except ValueError:
                response = "Hubo un error al intentar realizar la suma. ¿Podrías intentarlo de nuevo?"
        else:
            response = "No entendí los números, ¿puedes repetirlos?"

        # Enviar la respuesta al usuario
        dispatcher.utter_message(text=response)
        return []
    
####

class ActionDiv(Action):

    def name(self) -> Text:
        return "action_div"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extraer los números de los mensajes del usuario
        first_number = next(tracker.get_latest_entity_values("number1"), None)
        second_number = next(tracker.get_latest_entity_values("number2"), None)

        if first_number and second_number:
            try:
                first_number = float(first_number)
                second_number = float(second_number)

                # Verificar que el segundo número no sea cero (evitar división por cero)
                if second_number == 0:
                    response = (
                    f"¡Ups! No podemos dividir entre cero."
                    f"🤔 ¿Puedes darme otro número?"
                    )
                else:
                 # Calcular la división
                    result = first_number / second_number
                    
                    # Verificar si el resultado es un número entero o decimal
                    if result.is_integer():  # Si es un número entero
                        result = int(result)  # Convertir el resultado a entero
                        response = (
                            f"Imagina que tienes {first_number} 🍎 manzanas y las repartes entre {second_number} amigos 🧑‍🤝‍🧑. "
                            f"Cada uno recibe {result} manzanas. 🍏 ¡Una división exacta!"
                        )
                    else:  # Si es un número decimal
                        response = (
                            f"El resultado es {result} "
                        )
            except ValueError:
                response = "Hubo un error al intentar realizar la división. ¿Podrías intentarlo de nuevo?"
        else:
            response = "No entendí los números. 😅 ¿Puedes repetirlos, por favor?"

        # Enviar la respuesta al usuario
        dispatcher.utter_message(text=response)
        return []


class ActionGenerateDivisionExercises(Action):
    def name(self):
        return "action_exercises"

    def run(self, dispatcher, tracker, domain):
        ejercicio = generate_division()  # Genera un solo ejercicio

        first_request = tracker.get_slot("first_division_request")  # Obtener el valor del slot

        if first_request:  # Si es la primera vez que se solicita una división
            dispatcher.utter_message(text=f"¡Genial, ve a por papel y boli! Vamos a hacer unas divisiones.\n\n¿Cuánto es {ejercicio['dividendo']} ÷ {ejercicio['divisor']}? 🤔")
            # actualizar el slot a False
            return [
                SlotSet("first_division_request", False),
                SlotSet("correct_answer", ejercicio["respuesta"])
            ]
        
        dispatcher.utter_message(text=f"¿Cuánto es {ejercicio['dividendo']} ÷ {ejercicio['divisor']}? 🤔")
        return [SlotSet("correct_answer", ejercicio["respuesta"])]
    
class ActionCheckDivisionAnswer(Action):
    def name(self):
        return "action_check_division_answer"

    def run(self, dispatcher, tracker, domain):
        print("ACTION CHECK DIVISION ANSWER")

        user_answer_raw = tracker.latest_message.get("text")  # Captura la respuesta del usuario
        correct_answer = tracker.get_slot("correct_answer")  # Obtiene la respuesta correcta del slot
        ejercicios = tracker.get_slot("ejercicios") or []  # Lista de ejercicios
        current_exercise = tracker.get_slot("current_exercise") or 0  # Índice del ejercicio actual
        incorrect_divisions = tracker.get_slot("incorrect_divisions") or []

        tolerancia = 0.01

        if correct_answer is None:
            dispatcher.utter_message(text="Primero genera un ejercicio de división antes de responder.")
            return []

        try:
            # Reemplaza coma por punto y elimina espacios
            # esto lo hacemos porque el user_answer es un text (string)
            user_answer_clean = user_answer_raw.replace(",", ".").strip() #Da error si uso "."
            user_answer = float(user_answer_clean) 
            print("🧪 correct_answer:", correct_answer)
            
            if abs(user_answer - correct_answer) < tolerancia: #si el resultado es 3.3333, y el usuario escribe 3.33, se lo cuentas como válido.
                response = "¡Correcto! 🎉 Buen trabajo."
                dispatcher.utter_message(
                text=response,
                custom={"correcto": True}  # React detectará esto como respuesta correcta
                )
            else:
                response = f"Incorrecto. ❌ La respuesta correcta era {correct_answer}"
                incorrect_entry = {
                    "division": f"{ejercicios[current_exercise]['dividendo']} ÷ {ejercicios[current_exercise]['divisor']}",
                    "user_answer": user_answer,
                    "correct_answer": correct_answer
                }
                incorrect_divisions.append(incorrect_entry)  # Guardar el error sin mostrarlo todavía
                dispatcher.utter_message(
                 text=response,
                 custom={"correcto": False}  # React sabrá que fue incorrecto
                )

        except ValueError:
            dispatcher.utter_message(text="No entendí tu respuesta. ¿Puedes decirme un número? 🤔", custom={"correcto": False})
            return []

        # 📌 Avanzar al siguiente ejercicio si quedan más
        current_exercise += 1

        if current_exercise < len(ejercicios):
            siguiente_ejercicio = ejercicios[current_exercise]
            print("SIGUIENTE EJERCICIO: ", siguiente_ejercicio)

            if "enunciado" in siguiente_ejercicio:
                mensaje = siguiente_ejercicio.get("enunciado", "Error al generar el enunciado.")
            else:
                mensaje = f"Ahora intenta: ¿Cuánto es {siguiente_ejercicio['dividendo']} ÷ {siguiente_ejercicio['divisor']}?"

            dispatcher.utter_message(text=mensaje)

            return [
                SlotSet("current_exercise", current_exercise),
                SlotSet("correct_answer", siguiente_ejercicio["respuesta"]),
                SlotSet("incorrect_divisions", incorrect_divisions)  # Se almacena, pero no se muestra
            ]

        else:
            #Si ya se completaron todos los ejercicios, SE ENVÍA DIRECTAMENTE LA CORRECCIÓN
            print("✅ TODOS LOS EJERCICIOS COMPLETADOS, ENVIANDO CORRECCIÓN")
            
            mensaje, divisiones_faciles = explicar_divisiones_incorrectas(incorrect_divisions)

            # 📌 Convertir mensaje a string si no lo es
            if isinstance(mensaje, list):
                mensaje = "\n\n".join(mensaje)
            if not isinstance(mensaje, str):
                mensaje = str(mensaje)

            print("✅ Enviando mensaje de corrección...")
            dispatcher.utter_message(text=mensaje)

            # 📌 Enviar las imágenes como un mensaje separado si hay divisiones fáciles
            if divisiones_faciles:
                print("✅ Enviando imágenes de corrección...")
                dispatcher.utter_message(custom={"divisiones_faciles": divisiones_faciles})  # mensaje separado

            print("🟡 BORRANDO incorrect_divisions después de enviar la corrección...")

            return [
                SlotSet("current_exercise", 0), 
                SlotSet("correct_answer", None), 
                SlotSet("ejercicios", None),  # Reiniciar la lista de ejercicios
                SlotSet("incorrect_divisions", None)  # AHORA SÍ se vacía después de enviar la corrección
            ]

class ActionGenerarEjercicios(Action):
    def name(self):
        return "action_generar_ejercicios"

    def run(self, dispatcher, tracker, domain):
        print("-------------ACTION GENERAR EJERCICIOS---------------")
        dificultad_ejercicio = tracker.get_slot("dificultad")  
        num_ejercicios = tracker.get_slot("numero")
        tipo_ejercicio = tracker.get_slot("tipo_ejercicio")  
        print("TIPO EJERCICIOS: ", tipo_ejercicio)
        print("DIFICULTAD EJERCICIOS: ", dificultad_ejercicio)

        if not dificultad_ejercicio:
           print("🔴 ERROR: Slot 'dificultad' no está asignado")  # 🔍 DEPURACIÓN
           dificultad_ejercicio = "medio"  # Valor por defecto


        if num_ejercicios is None:
            dispatcher.utter_message(text="No entendí cuántos ejercicios quieres. ¿Puedes decirme un número?")
            return []
        
        try:
            num_ejercicios = int(str(num_ejercicios).strip())  # Convertir a entero
        except ValueError:
            dispatcher.utter_message(text="Parece que hubo un error con el número de ejercicios. ¿Puedes intentarlo de nuevo?")
            return []
        
        
        if tipo_ejercicio == "sueltas":
            ejercicios = [generate_division(dificultad_ejercicio) for _ in range(num_ejercicios)]
        else:
            ejercicios = [generate_enunciado(dificultad_ejercicio) for _ in range(num_ejercicios)]

        if not ejercicios:
            dispatcher.utter_message(text="No se generaron ejercicios. Intenta de nuevo.")
            return []

        primer_ejercicio = ejercicios[0]

        if tipo_ejercicio == "sueltas":
            mensaje = f"¿Cuánto es {primer_ejercicio['dividendo']} ÷ {primer_ejercicio['divisor']}?"
        else:
            mensaje = primer_ejercicio["enunciado"]

        dispatcher.utter_message(text=mensaje)

        return [
            SlotSet("ejercicios", ejercicios), 
            SlotSet("current_exercise", 0),
            SlotSet("correct_answer", primer_ejercicio["respuesta"])
        ]
    
#### SUMA  ####
class ActionResponderEjercicio(Action):

    def name(self):
        return "action_responder_ejercicio"

    def run(self, dispatcher, tracker, domain):
        # Obtenemos la respuesta del usuario
        respuesta_usuario = tracker.latest_message.get("text")

        # Obtenemos el ejercicio actual y los ejercicios restantes
        current_exercise = tracker.get_slot("current_exercise")
        ejercicios = tracker.get_slot("ejercicios")

        # Validamos la respuesta (simple comparación de respuestas)
        num1, num2 = map(int, ejercicios[current_exercise].split(" ÷ ")[0].split())
        correct_answer = num1 // num2

        if float(respuesta_usuario) == correct_answer:
            dispatcher.utter_message(text="¡Respuesta correcta! 😊")
        else:
            dispatcher.utter_message(text=f"La respuesta correcta era {correct_answer}. 😔")

        # Actualizamos el índice del ejercicio
        next_exercise = current_exercise + 1

        if next_exercise < len(ejercicios):
            dispatcher.utter_message(text=f"Tu siguiente ejercicio: {ejercicios[next_exercise]}")
            return [SlotSet("current_exercise", next_exercise)]
        else:
            dispatcher.utter_message(text="¡Has completado todos los ejercicios! 🎉")
            return [SlotSet("current_exercise", None)]

