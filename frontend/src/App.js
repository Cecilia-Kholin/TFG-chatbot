import './App.css';
import React, { useState, useEffect } from "react";
import Chatbot from "./components/chatbot"; //añadimos el chatbot
import 'bootstrap/dist/css/bootstrap.min.css';
import introJs from 'intro.js';


function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [correctAnswers, setCorrectAnswers] = useState(0);

  useEffect(() => {
    const savedMode = JSON.parse(localStorage.getItem("dark-mode"));
    if (savedMode !== null) {
      setDarkMode(savedMode);
    } else {
      setDarkMode(window.matchMedia('(prefers-color-scheme: dark)').matches);
    }
  }, []);
  

  useEffect(() => {
    localStorage.setItem("dark-mode", JSON.stringify(darkMode));
    if (darkMode) {
      document.documentElement.classList.add("dark-mode");
    } else {
      document.documentElement.classList.remove("dark-mode");
    }
  }, [darkMode]);

  return (
    <div className={`App-header ${darkMode ? 'dark-mode' : ''}`}>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h3>¡A practicar!</h3>
        <label className="switch">
          <input 
            type="checkbox" 
            checked={darkMode} 
            onChange={() => setDarkMode(!darkMode)} 
          />
          <span className="slider"></span>
        </label>
      </div>

      <div className="row">
        {/* Columna izquierda: insignias */}
        <div className="col-md-3 text-center mb-4"   data-intro="Aquí están tus logros">
          <img 
            src={correctAnswers >= 10 ? "logro_10.png" : "sinlogro10.png"} 
            alt="Logro 10" 
            className="img-fluid mb-2"
          />
          <img 
            src={correctAnswers >= 50 ? "logro50.png" : "sinlogro10.png"} 
            alt="Logro 50" 
            className="img-fluid mb-2"
          />
          <img 
            src={correctAnswers >= 100 ? "logro100.png" : "sinlogro10.png"} 
            alt="Logro 100" 
            className="img-fluid mb-2"
          />
        </div>

        {/* Columna central: chatbot */}
        <div className="col-md-6">
          <Chatbot setCorrectAnswers={setCorrectAnswers} />
        </div>

        {/* Columna derecha: guía */}
        <div className="col-md-3">
        <button
          onClick={() => introJs().start()}
          className="bg-blue-500 hover:bg-blue-600 text-black font-bold py-2 px-4 rounded-xl shadow-md mb-4"
        >
          🧭 Ver guía
        </button>
          <ul>
            <li>Haz clic en el chatbot para comenzar</li>
            <li>Responde las divisiones correctamente</li>
            <li>¡Gana insignias por tus logros!</li>
          </ul>
          <img 
            src={"capibara.png"} 
            alt="Logro 100" 
            className="img-fluid mb-2"
          />
        </div>
      </div>
    </div>
  );
}

export default App;
