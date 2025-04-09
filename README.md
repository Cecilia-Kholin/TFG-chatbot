python3.9 -m venv rasa-env
source rasa-env/bin/activate

pip3 install -U pip

pip3 install rasa


entrenar al chatbot
rasa train


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
Poner "*" permite acceso desde cualquier dominio, lo cual no es seguro en producción. Para mayor seguridad, puedes especificar solo los dominios permitidos:
rasa run --enable-api --cors "https://midominio.com"


rasa run actions
rasa run actions --port 5055
rasa shell --debug


MI IP 
192.168.1.176
