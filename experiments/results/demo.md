============================================================
UN CORREO RECORRE EL SISTEMA
============================================================

CORREO
------
Microsoft 365: confirme su sesión
Su licencia caduca en 1 hora. Inicie sesión en http://micros0ft-office.xyz/365 o se suspenderá Outlook.

EJE 1 — predicción
------------------
SVM + TF-IDF → phishing  (clase positiva: phishing)

EJE 2 — retriever = bm25
-------------------------------
Fragmentos recuperados:
    1. [campana_microsoft] Falso soporte Microsoft / Office 365  score=15.847  (campana)
       Correos que imitan IT Support o Microsoft 365. Dominios tipo micros0ft-login.xyz. Piden restablecer contraseña o la licencia.
    2. [regla_urgencia] Urgencia artificial  score=10.384  (regla)
       El phishing aprieta el tiempo: 'hoy', 'en 1 hora', 'o se bloqueará'. Busca que actúes sin pensar.
    3. [regla_cuenta] Amenaza de bloqueo de cuenta  score=4.788  (regla)
       Nequi, Outlook, Apple ID, matrícula: 'se bloqueará / se anulará si no entra a este link'.

PROMPT QUE SE LE ENVÍA AL LLM
-----------------------------
Eres analista de phishing. Responde en español, 4 a 8 oraciones.
Usando SOLO los fragmentos de abajo, explica si el correo es phishing y por qué.
Cita los IDs entre corchetes, por ejemplo [regla_urgencia].
Si los fragmentos no alcanzan, responde exactamente: evidencia insuficiente.
No inventes campañas, bancos ni URLs que no aparezcan en los fragmentos.

CORREO:
Microsoft 365: confirme su sesión
Su licencia caduca en 1 hora. Inicie sesión en http://micros0ft-office.xyz/365 o se suspenderá Outlook.

FRAGMENTOS:
[campana_microsoft] Falso soporte Microsoft / Office 365
Correos que imitan IT Support o Microsoft 365. Dominios tipo micros0ft-login.xyz. Piden restablecer contraseña o la licencia.

[regla_urgencia] Urgencia artificial
El phishing aprieta el tiempo: 'hoy', 'en 1 hora', 'o se bloqueará'. Busca que actúes sin pensar.

[regla_cuenta] Amenaza de bloqueo de cuenta
Nequi, Outlook, Apple ID, matrícula: 'se bloqueará / se anulará si no entra a este link'.


RESPUESTA
---------
El correo es phishing. Presenta una falsa urgencia ("Su licencia caduca en 1 hora. Inicie sesión en http://micros0ft-office.xyz/365 o se suspenderá Outlook.") para presionar al usuario a realizar una acción sin pensar.  Además, el dominio del enlace es sospechoso ("micros0ft-office.xyz") y se menciona la amenaza de bloquear la cuenta si no se accede al enlace.  [regla_urgencia]

============================================================
MISMO CORREO, LLM SIN RAG  (Gemma se inventa lo que quiera)
============================================================

PROMPT
------
Eres analista de phishing. Responde en español, 4 a 8 oraciones.
Explica si este correo es phishing y por qué.
Si se parece a alguna campaña conocida, nómbrala.

CORREO:
Microsoft 365: confirme su sesión
Su licencia caduca en 1 hora. Inicie sesión en http://micros0ft-office.xyz/365 o se suspenderá Outlook.


RESPUESTA SIN BASE
------------------
Este correo es un claro ejemplo de phishing. Presenta varias características que lo hacen sospechoso:

* **Mensaje urgente:**  "Su licencia caduca en 1 hora" crea presión y urgencia para que el usuario actúe sin pensar. 
* **URL sospechosa:**  La URL en el correo,  "http://micros0ft-office.xyz/365",  no es una URL legítima de Microsoft.  Las URLs de Microsoft suelen ser  "support.microsoft.com" o "outlook.live.com".
* **Falta de autenticación:**  Microsoft nunca enviaría un correo electrónico con un enlace para iniciar sesión en una página web con un nombre tan similar a la de Microsoft. 
* **Aspecto de spam:**  El tono del correo es muy similar a los correos de phishing que se envían a usuarios de Microsoft 365.

Este correo parece ser una variante de campañas de phishing que se han utilizado en el pasado, como las que se han relacionado con el **phishing de Microsoft 365**.  Es importante recordar que **nunca debes hacer clic en enlaces sospechosos** ni ingresar información personal en sitios web que no sean legítimos.

La diferencia: con RAG tiene que citar [campana_microsoft] / [regla_urgencia].
Sin RAG puede nombrar campañas que no están en la base.
