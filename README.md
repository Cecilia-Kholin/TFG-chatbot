# 🤖 Proyecto Chatbot Educativo con RASA y React

Este repositorio contiene un asistente conversacional desarrollado con [RASA](https://rasa.com/) y una interfaz web construida con React. El objetivo es enseñar divisiones a niños de forma interactiva.

---

## 🛠️ Instalaciones necesarias

- **Node.js**
- **Python 3.8 o superior** (este proyecto utilizó Python 3.9.12)
- **RASA 3.6.20**
- **Microsoft Visual C++ Build Tools** (necesario para compilar ciertas librerías en Windows)

---

## 📦 Dependencias

### Node.js:
```bash
npm install bootstrap intro.js
```

### Python:
```bash
pip install spacy==3.5.4
python -m spacy download es_core_news_md
```

---

## 🧪 Entrenamiento del bot

> El modelo debe entrenarse antes de usarse. No está incluido en el repositorio debido a su tamaño.

### Crear y activar entorno virtual

**Linux/macOS:**
```bash
python3.9 -m venv rasa-env
source rasa-env/bin/activate
```

**Windows:**
```bash
python3.9 -m venv rasa-env
venv\Scripts\activate
```

### Instalar RASA
```bash
pip install -U pip
pip install rasa
```

---

## 📁 Archivos importantes del proyecto

- `domain.yml`: Archivo principal de configuración del asistente. Define las intenciones, entidades, acciones y respuestas.
- `data/nlu.yml`: Datos de entrenamiento para el modelo de comprensión del lenguaje natural (NLU).
- `data/stories.yml`: Define los posibles caminos de conversación.
- `data/rules.yml`: Contiene reglas fijas que el bot debe seguir.
- `credentials.yml`: Configuración para conectar el bot a canales externos como Slack o Facebook.
- `endpoints.yml`: Define los puntos finales (como el servidor de acciones personalizadas).
- `actions.py`: Código Python con las acciones personalizadas del bot.

---

## 💻 Comandos útiles

### Entrenar el bot:
```bash
rasa train
```

### Ejecutar acciones personalizadas:
```bash
rasa run actions
rasa run actions --port 5055
```

### Probar el bot:
```bash
rasa shell
rasa shell --debug
```

---

## 🌐 Integración con React

### Crear la aplicación:
```bash
npx create-react-app frontend
cd frontend
npm start
```

### Ejecutar RASA con la API habilitada:
```bash
rasa run --enable-api --cors "*"
```

> ⚠️ Usar `"*"` permite acceso desde cualquier dominio, no recomendable en producción.

---

## 📌 Notas finales

Este proyecto combina procesamiento de lenguaje natural y experiencia interactiva web para facilitar el aprendizaje matemático en edades tempranas.