import React, { useState } from "react";
import './chatContainer.css';
import DivisionIncorrectaSVG from "./DivisionIncorrectaSVG"; // Importar el componente de animación
import 'intro.js/introjs.css';

//***************SPEAK***********************
//const speak = (text) => {
//  if ("speechSynthesis" in window) {
//    const utterance = new SpeechSynthesisUtterance(text);
//    utterance.lang = "es-ES"; // Cambia el idioma 
//    utterance.pitch = 1.2; 
//    utterance.rate = 1; // Velocidad normal
//    window.speechSynthesis.speak(utterance);
//  }
//};
//
const Chatbot = ({setCorrectAnswers}) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const sendMessage = async (messageText = input) => {
    if (!messageText.trim()) return;

    // Filtrar intents: No agregar mensajes que empiezan con "/"
    if (messageText.startsWith("/")) {
      sendMessageToBot(messageText);
      setInput("");
      return;
    }

    const userMessage = { text: messageText, sender: "user" };
    setMessages([...messages, userMessage]);
    setInput("");

    sendMessageToBot(messageText);
  };

  const sendMessageToBot = async (messageText) => {
    try {
      //http://192.168.1.176:5005/webhooks/rest/webhook
      const response = await fetch("http://localhost:5005/webhooks/rest/webhook", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sender: "user", message: messageText }),
      });

      const data = await response.json();
      console.log("📩 Respuesta de RASA:", data);

      if (data.length > 0) {
        const newMessages = data.map((response) => {
          if (response.text && response.buttons && response.image) {
            // Maneja texto, botones e imagen
            return { 
              text: response.text, 
              options: response.buttons, 
              image: response.image, 
              sender: "bot" 
            };
          }
          if (response.text && response.buttons) {
            // Maneja texto y botones
            return { 
              text: response.text, 
              options: response.buttons, 
              sender: "bot" 
            };
          }
          if (response.text && response.image) {
            // Maneja texto e imagen
            return { 
              text: response.text, 
              image: response.image, 
              sender: "bot" 
            };
          }
          if (response.text) {
            // Maneja solo texto
            return { 
              text: response.text, 
              sender: "bot" 
            };
          }
          if (response.buttons) {
            // Maneja solo botones
            return { 
              options: response.buttons, 
              sender: "bot" 
            };
          }
          if (response.image) {
            // Maneja solo imagen
            return { 
              image: response.image, 
              sender: "bot" 
            };
          }
          return null;
        }).filter(Boolean);
      
        // Extraer las divisiones fáciles incorrectas si están en la respuesta de RASA
        const incorrectas = data.find((msg) => msg.custom && msg.custom.divisiones_faciles);        
        const esCorrecto = data.find((msg) => msg.custom && msg.custom.correcto === true);

        if (incorrectas) {
          console.log("✅ Divisiones fáciles incorrectas recibidas:", incorrectas.custom.divisiones_faciles);       

          // 🔥 Primero agregamos los mensajes normales del bot
          setMessages((prevMessages) => [
            ...prevMessages,
            ...newMessages, // Asegura que los mensajes de texto del bot también se guarden
            { text: "Aquí está tu corrección visual:", sender: "bot" }, // Mensaje explicativo
            { custom: incorrectas.custom.divisiones_faciles, sender: "bot" } // Corrección visual
          ]);
        } else {
          // Si no hay corrección, solo agregamos los mensajes normales
          if (esCorrecto) {
            console.log("✅ Respuesta correcta detectada");
            setCorrectAnswers((prev) => prev + 1); // Incrementar correctAnswers
          } 
          setMessages((prevMessages) => [...prevMessages, ...newMessages]);
          //newMessages.forEach((msg) => {
          //  if (msg.text) {
          //    speak(msg.text);
          //  }
          //});
        }
       

      }
    } catch (error) {
      console.error("❌ Error al conectar con el chatbot:", error);
    }
  };
 
  const sendmessagefrombutton = (payload) => {
    console.log("📩 Payload enviado al bot:", payload);
    sendMessage(payload);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && input.trim()) {
      sendMessage(input);
      setInput("");
    }
  };

  return (
    <>
   

    <div className="chat-container">
      <div className="chatbox" data-intro="Aquí es donde el chatbot responde. 🤖">
        {messages.map((msg, index) => (
          <div key={index} className={msg.sender}>
            {msg.text && (
              <div className="message__bubble">
                {msg.text.split('\n').map((linea, i) => (
                  <p key={i}>{linea}</p>
                ))}
              </div>
            )}
            {msg.options && (
              <div className="message__bubble">
                {msg.options.map((option, i) => (
                  <button
                    key={i}
                    className="bot-option"
                    onClick={() => {
                      sendmessagefrombutton(option.payload);
                      if (option.payload === "/pedir_correccion") {
                        setTimeout(() => sendMessage("/pedir_correccion"), 500);
                      }
                    }}
                    data-intro={i === 0 ? "Puedes usar estos botones para responder rápidamente. 🧠" : null}
                  >
                    {option.title}
                  </button>
                ))}
              </div>
            )}
            {msg.image && (
              <div className="message__bubble">
                <img src={msg.image} alt="Animación" className="gif-message" />
              </div>
            )}
            {msg.custom && (
              <div className="message__bubble">
                <h3>Corrección Visual de Errores</h3>
                {msg.custom.map((division, i) => (
                  <DivisionIncorrectaSVG
                    key={i}
                    dividendo={division.dividendo}
                    divisor={division.divisor}
                    respuestaCorrecta={division.respuesta_correcta}
                    respuestaUsuario={division.respuesta_usuario}
                  />
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
      <div className="input-container">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="input"
          placeholder="Escribe tu mensaje..."
          onKeyDown={handleKeyDown}
          data-intro="Escribe aquí tu respuesta. ✍️"
        />
        <button
          className="send-button"
          onClick={() => sendMessage(input)}
          data-intro="Haz clic para enviar tu respuesta. 📤"
        >
          Enviar
        </button>

      </div>
    </div>
    </>
  );
};

export default Chatbot;
