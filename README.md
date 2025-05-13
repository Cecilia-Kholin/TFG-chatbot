//////////////////////////////////////////////////////
///////////// INSALACIONES NECESARIAS ////////////////
//////////////////////////////////////////////////////
Node.js
Python 3.8 o superior, el que se usó para ese proyeco fue 3.9.12
RASA, el proyecto se realizó con la version 3.6.20


/////////////////////// DEPENDENCIAS //////////////////////

npm install bootstrap intro.js
SpacyNLP: 
    pip install spacy==3.5.4
    python -m spacy download es_core_news_md



/////////////////////// entrenamiento //////////////////////
Hace falta entrenar el bot antes de usarlo, no esta subido al repositorio por el tamaño 


Microsoft Visual C++ Build Tools, que es necesario para compilar partes de esa librería en Windows.


python3.9 -m venv rasa-env
source rasa-env/bin/activate

pip3 install -U pip

pip3 install rasa

//////////////////////////////////////////////////////
//////////////// ENTRENAR CHATBOT ///////////////////
//////////////////////////////////////////////////////

///////////// INFO /////////////

 domain.yml : este es el archivo más importante para RASA. Lo llaman como un dominio asistente. Tu bot tiene 2 componentes: NLU y ra. La NLU es lo que el usuario le preguntará al robot. El CORE es lo que el bot responderá 

 data / stories.md: esto define el flujo de la conversación o puede decir posibles escenarios a los que la conversación puede conducir.

 credentials.yml: En este archivo, podemos configurar las credenciales del bot para conectarse a diferentes canales externos, como Facebook o Slack.

 endpoints.yml: Este archivo se utiliza para especificar los puntos finales a los que se conecta el bot. Por ejemplo, si estás utilizando acciones personalizadas, puedes especificar la URL de tu servidor de acciones aquí.

data/nlu.yml: Este archivo contiene los datos de entrenamiento para el procesamiento del lenguaje natural (NLU) de Rasa. Aquí es donde definimos las intenciones y entidades que el bot debe reconocer.

data/rules.yml: Este archivo contiene reglas que el bot debe seguir. Las reglas son instrucciones específicas que el bot debe cumplir sin ninguna variación.

data/stories.yml: En este archivo, definimos los caminos de conversación y las respuestas del bot en función de las acciones que hemos creado.

///////////// COMANDOS /////////////
rasa train

rasa run actions

Una vez que el modelo ha sido entrenado, podemos probar nuestro bot de Rasa en la línea de comandos. Para iniciar el bot, simplemente ejecuta el siguiente comando:
rasa shell
Esto abrirá una interfaz en la línea de comandos donde podrás enviar mensajes al bot y recibir sus respuestas. Puedes probar diferentes mensajes y ver cómo responde el bot.



//////////////////////////////////////////////////////
///////////// UNIR CHATBOT CON LA PAGINA /////////////
//////////////////////////////////////////////////////

REACT
npx create-react-app frontend
cd frontend
npm start


rasa run --enable-api --cors "*"
Poner "*" permite acceso desde cualquier dominio, lo cual no es seguro en producción.
rasa run --enable-api --cors "https://midominio.com"


rasa run actions
rasa run actions --port 5055
rasa shell --debug


MI IP 
192.168.1.176
