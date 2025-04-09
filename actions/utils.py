import random
import json
import os
######################################################
############     GENERA DIVISIONES     ###############
######################################################
def generate_division(dificultad):
    print("generate_division:", dificultad)

    if dificultad == "fácil":
        num2 = random.randint(1, 9)
        resultado = random.randint(1, 9)
        num1 = num2 * resultado  # Asegurar división exacta

    elif dificultad == "medio":
        num2 = random.randint(10, 99)
        resultado = random.randint(2, 20)
        num1 = num2 * resultado

    elif dificultad == "difícil":
        num2 = random.randint(5, 20)
        num1 = random.randint(num2 + 1, num2 * 10)
        resultado = num1 // num2
        residuo = num1 % num2

    elif dificultad == "experto":
        num2 = random.randint(10, 50)
        num1 = random.randint(num2, num2 * 5)
        resultado = round(num1 / num2, 2)

    return {
        "dividendo": num1,
        "divisor": num2,
        "respuesta": resultado,
        "residuo": residuo if dificultad == "difícil" else None
    }

def generate_enunciado(dificultad):
    """Genera un enunciado de división basado en la dificultad seleccionada."""
    
    # Generar una división basada en la dificultad
    division = generate_division(dificultad)

    # Cargar los enunciados de la dificultad seleccionada
    enunciados = load_enunciados(dificultad)  

    # Si no hay enunciados disponibles, devolver un mensaje de error
    if not enunciados:
        return {
            "enunciado": "No se pudieron cargar los enunciados. Intenta más tarde.",
            "dividendo": division["dividendo"],
            "divisor": division["divisor"],
            "respuesta": division["respuesta"]
        }

    # Seleccionar un enunciado aleatorio y formatearlo con los valores correctos
    enunciado = random.choice(enunciados).format(
        dividendo=division["dividendo"], divisor=division["divisor"]
    )

    return {
        "enunciado": enunciado,
        "dividendo": division["dividendo"],
        "divisor": division["divisor"],
        "respuesta": division["respuesta"]
    }


def load_enunciados(dificultad):
    """Carga la lista de enunciados desde un archivo JSON y devuelve solo los de la dificultad seleccionada."""
    script_dir = os.path.dirname(__file__)  # Ruta del script actual
    file_path = os.path.join(script_dir, "../data/enunciados.json")  # Ruta del JSON
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            enunciados = json.load(file)  # Carga el JSON como un diccionario

            # Verifica que la dificultad exista en el JSON
            if dificultad in enunciados:
                return enunciados[dificultad]  # Retorna solo los enunciados de esa dificultad
            else:
                print(f"Error: La dificultad '{dificultad}' no existe en el JSON.")
                return []
    except FileNotFoundError:
        print("Error: No se encontró el archivo enunciados.json")
        return []  # Retorna una lista vacía si hay un error
    except json.JSONDecodeError:
        print("Error: No se pudo leer el archivo enunciados.json")
        return []
    

def explicar_divisiones_incorrectas(incorrect_divisions):
    """
    Genera una explicación detallada de las divisiones incorrectas.
    """
    if not incorrect_divisions:
        return "¡Felicidades! No tienes errores, hiciste todas las divisiones correctamente. 🎉", []

    mensajes = []  # Lista para almacenar los mensajes individuales
    divisiones_faciles = []  

    for i, entry in enumerate(incorrect_divisions, 1):
        dividendo = int(entry["division"].split(" ÷ ")[0])  
        divisor = int(entry["division"].split(" ÷ ")[1])  
        respuesta_correcta = int(entry["correct_answer"])
        respuesta_usuario = int(entry["user_answer"])

        mensaje = (
            f"🔹Ejercicio {i}:\n"
            f"  - División: {dividendo} ÷ {divisor} = ?\n"
            f"  - ❌ Tu respuesta: {respuesta_usuario}\n"
            f"  - ✅ Respuesta correcta: {respuesta_correcta}\n"
            f"  - 📖 Explicación: Si tomamos {dividendo} y lo dividimos en {divisor} partes iguales, cada parte contiene {respuesta_correcta}.\n"
        )

        mensajes.append(mensaje)  # Guardamos en la lista

        # Si la división es fácil, la agregamos a la lista para React
        if divisor <= 9 and dividendo % divisor == 0:
            divisiones_faciles.append({
                "dividendo": dividendo,
                "divisor": divisor,
                "respuesta_correcta": respuesta_correcta,
                "respuesta_usuario": respuesta_usuario
            })

    # 🔥 Convertimos la lista `mensajes` en un solo string con "\n\n"
    mensaje_final = "\n\n".join(mensajes)

    print("✅ ENVIANDO DIVISIONES INCORRECTAS A REACT:", divisiones_faciles)  # Debug en consola de RASA
    return mensaje_final, divisiones_faciles

