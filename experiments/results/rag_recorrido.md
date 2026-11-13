# Eje 2 — recorrido RAG
llm=ollama  modelo=gemma2:2b  k=3

## Ejemplo largo: q1 (p25)
Microsoft 365: confirme su sesión
Su licencia caduca en 1 hora. Inicie sesión en http://micros0ft-office.xyz/365 o se suspenderá Outlook.
gold: ['campana_microsoft', 'regla_dominio', 'regla_urgencia']

### LLM sin RAG

Eres analista de phishing. Responde en español, 4 a 8 oraciones.
Explica si este correo es phishing y por qué.
Si se parece a alguna campaña conocida, nómbrala.

CORREO:
Microsoft 365: confirme su sesión
Su licencia caduca en 1 hora. Inicie sesión en http://micros0ft-office.xyz/365 o se suspenderá Outlook.


Este correo es un **phishing** y es una clara amenaza.  La estructura del correo es sospechosa, con un tono urgente y un enlace sospechoso.  Microsoft nunca enviaría un correo electrónico con un enlace directo para iniciar sesión en una página web.  La frase "Su licencia caduca en 1 hora" es una técnica común en phishing para presionar a los usuarios a actuar sin pensar.  Además, el dominio "micros0ft-office.xyz" es muy probable que sea falso y no sea un sitio legítimo de Microsoft.  Las campañas de phishing de Microsoft suelen ser más detalladas y menos urgentes, con un enfoque en la seguridad y la autenticación. 


**Campañas conocidas:**  Esta técnica de phishing se asemeja a campañas de phishing de Microsoft, donde se intenta engañar a los usuarios para que accedan a sitios web falsos.
============================================================
UN CORREO RECORRE EL SISTEMA
============================================================

CORREO
------
Microsoft 365: confirme su sesión
Su licencia caduca en 1 hora. Inicie sesión en http://micros0ft-office.xyz/365 o se suspenderá Outlook.

EJE 1 — predicción
------------------
(sin clasificador)

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
El correo es phishing. Presenta una falsa urgencia ("su licencia caduca en 1 hora") y una amenaza de bloqueo de cuenta ("Nequi, Outlook, Apple ID, matrícula: 'se bloqueará / se anulará si no entra a este link'").  El dominio del enlace es sospechoso ("micros0ft-office.xyz") y se asemeja a la autenticidad de Microsoft 365.  [regla_urgencia]

============================================================
UN CORREO RECORRE EL SISTEMA
============================================================

CORREO
------
Microsoft 365: confirme su sesión
Su licencia caduca en 1 hora. Inicie sesión en http://micros0ft-office.xyz/365 o se suspenderá Outlook.

EJE 1 — predicción
------------------
(sin clasificador)

EJE 2 — retriever = tfidf
-------------------------------
Fragmentos recuperados:
    1. [campana_microsoft] Falso soporte Microsoft / Office 365  score=0.495  (campana)
       Correos que imitan IT Support o Microsoft 365. Dominios tipo micros0ft-login.xyz. Piden restablecer contraseña o la licencia.
    2. [regla_urgencia] Urgencia artificial  score=0.286  (regla)
       El phishing aprieta el tiempo: 'hoy', 'en 1 hora', 'o se bloqueará'. Busca que actúes sin pensar.
    3. [regla_cuenta] Amenaza de bloqueo de cuenta  score=0.152  (regla)
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
El correo es phishing. Presenta una falsa sensación de urgencia ("Su licencia caduca en 1 hora. Inicie sesión en http://micros0ft-office.xyz/365 o se suspenderá Outlook.") y amenaza de bloqueo de cuenta ("Nequi, Outlook, Apple ID, matrícula: 'se bloqueará / se anulará si no entra a este link'"). Además, el dominio del correo es sospechoso ("micros0ft-office.xyz").  La presencia de estos elementos, junto con la falta de información de la empresa real, sugiere que se trata de una estafa.

============================================================
UN CORREO RECORRE EL SISTEMA
============================================================

CORREO
------
Microsoft 365: confirme su sesión
Su licencia caduca en 1 hora. Inicie sesión en http://micros0ft-office.xyz/365 o se suspenderá Outlook.

EJE 1 — predicción
------------------
(sin clasificador)

EJE 2 — retriever = cbow
-------------------------------
Fragmentos recuperados:
    1. [regla_urgencia] Urgencia artificial  score=0.919  (regla)
       El phishing aprieta el tiempo: 'hoy', 'en 1 hora', 'o se bloqueará'. Busca que actúes sin pensar.
    2. [campana_microsoft] Falso soporte Microsoft / Office 365  score=0.911  (campana)
       Correos que imitan IT Support o Microsoft 365. Dominios tipo micros0ft-login.xyz. Piden restablecer contraseña o la licencia.
    3. [campana_dian] Falsa DIAN o premio  score=0.894  (campana)
       Devolución de impuestos o sorteo. Piden datos o un pago adelantado para entregar un dinero que no existe.

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
[regla_urgencia] Urgencia artificial
El phishing aprieta el tiempo: 'hoy', 'en 1 hora', 'o se bloqueará'. Busca que actúes sin pensar.

[campana_microsoft] Falso soporte Microsoft / Office 365
Correos que imitan IT Support o Microsoft 365. Dominios tipo micros0ft-login.xyz. Piden restablecer contraseña o la licencia.

[campana_dian] Falsa DIAN o premio
Devolución de impuestos o sorteo. Piden datos o un pago adelantado para entregar un dinero que no existe.


RESPUESTA
---------
El correo es phishing. Presenta una falsa urgencia ("su licencia caduca en 1 hora") y un dominio sospechoso ("micros0ft-office.xyz").  Los correos de phishing suelen imitar el soporte de empresas legítimas como Microsoft, y pedir información personal o dinero.  [regla_urgencia]

============================================================
UN CORREO RECORRE EL SISTEMA
============================================================

CORREO
------
Microsoft 365: confirme su sesión
Su licencia caduca en 1 hora. Inicie sesión en http://micros0ft-office.xyz/365 o se suspenderá Outlook.

EJE 1 — predicción
------------------
(sin clasificador)

EJE 2 — retriever = skipgram
-------------------------------
Fragmentos recuperados:
    1. [regla_urgencia] Urgencia artificial  score=0.999  (regla)
       El phishing aprieta el tiempo: 'hoy', 'en 1 hora', 'o se bloqueará'. Busca que actúes sin pensar.
    2. [campana_microsoft] Falso soporte Microsoft / Office 365  score=0.999  (campana)
       Correos que imitan IT Support o Microsoft 365. Dominios tipo micros0ft-login.xyz. Piden restablecer contraseña o la licencia.
    3. [campana_dian] Falsa DIAN o premio  score=0.999  (campana)
       Devolución de impuestos o sorteo. Piden datos o un pago adelantado para entregar un dinero que no existe.

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
[regla_urgencia] Urgencia artificial
El phishing aprieta el tiempo: 'hoy', 'en 1 hora', 'o se bloqueará'. Busca que actúes sin pensar.

[campana_microsoft] Falso soporte Microsoft / Office 365
Correos que imitan IT Support o Microsoft 365. Dominios tipo micros0ft-login.xyz. Piden restablecer contraseña o la licencia.

[campana_dian] Falsa DIAN o premio
Devolución de impuestos o sorteo. Piden datos o un pago adelantado para entregar un dinero que no existe.


RESPUESTA
---------
El correo es phishing.  Presenta una falsa urgencia ("su licencia caduca en 1 hora") y un dominio sospechoso ("micros0ft-office.xyz").  Los correos de phishing suelen imitar correos de empresas legítimas como Microsoft o DIAN, y suelen pedir información personal o dinero.  [regla_urgencia]

============================================================
UN CORREO RECORRE EL SISTEMA
============================================================

CORREO
------
Microsoft 365: confirme su sesión
Su licencia caduca en 1 hora. Inicie sesión en http://micros0ft-office.xyz/365 o se suspenderá Outlook.

EJE 1 — predicción
------------------
(sin clasificador)

EJE 2 — retriever = glove
-------------------------------
Fragmentos recuperados:
    1. [campana_microsoft] Falso soporte Microsoft / Office 365  score=0.905  (campana)
       Correos que imitan IT Support o Microsoft 365. Dominios tipo micros0ft-login.xyz. Piden restablecer contraseña o la licencia.
    2. [regla_credenciales] Pide contraseña, PIN o token  score=0.767  (regla)
       Un banco o Microsoft no te pide clave, OTP o PIN por un enlace llegado de sorpresa al correo.
    3. [regla_urgencia] Urgencia artificial  score=0.757  (regla)
       El phishing aprieta el tiempo: 'hoy', 'en 1 hora', 'o se bloqueará'. Busca que actúes sin pensar.

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

[regla_credenciales] Pide contraseña, PIN o token
Un banco o Microsoft no te pide clave, OTP o PIN por un enlace llegado de sorpresa al correo.

[regla_urgencia] Urgencia artificial
El phishing aprieta el tiempo: 'hoy', 'en 1 hora', 'o se bloqueará'. Busca que actúes sin pensar.


RESPUESTA
---------
El correo es phishing. Presenta una falsa urgencia ("su licencia caduca en 1 hora") para presionar al usuario a iniciar sesión en un enlace sospechoso.  El dominio del enlace es [micros0ft-office.xyz], que es similar a dominios de phishing conocidos. Además, el correo solicita credenciales como contraseña, PIN o token, lo que es un indicador de phishing.  [regla_urgencia]


## Las demás preguntas (solo IDs recuperados)

### q2  gold=['campana_banco', 'regla_enlace', 'regla_credenciales']
Alerta Bancolombia sucursal virtual
Hay una transferencia pendiente de $2.100.000. Autorícela ahora: http://bancolombia-virtual.tk/otp
- **bm25**: regla_dominio(7.67), campana_banco(5.36), regla_enlace(4.07)
- **tfidf**: regla_dominio(0.33), campana_banco(0.24), regla_enlace(0.17)
- **cbow**: regla_premio(0.82), campana_drive(0.82), campana_banco(0.81)
- **skipgram**: regla_dominio(1.00), campana_banco(1.00), regla_premio(1.00)
- **glove**: regla_dominio(0.76), campana_banco(0.74), regla_enlace(0.73)

### q3  gold=['campana_paquete', 'regla_urgencia', 'regla_premio']
Servientrega: pague para entregar
Su paquete no se entregó. Abone $7.500 en http://servientrega-pago.ga/abono en las próximas 2 horas.
- **bm25**: campana_paquete(11.82), campana_dian(5.95), regla_urgencia(5.41)
- **tfidf**: campana_paquete(0.36), campana_dian(0.19), regla_urgencia(0.15)
- **cbow**: campana_paquete(0.88), campana_dian(0.88), regla_urgencia(0.86)
- **skipgram**: campana_dian(1.00), campana_paquete(1.00), regla_premio(1.00)
- **glove**: campana_paquete(0.84), campana_dian(0.77), regla_credenciales(0.72)

### q4  gold=['campana_universidad', 'regla_cuenta', 'regla_enlace']
UR: pago de derechos de grado
Si no paga hoy se aplaza la ceremonia. Portal de pagos: http://ur-grados.online/derechos
- **bm25**: campana_universidad(19.91), regla_cuenta(8.53), regla_dominio(4.52)
- **tfidf**: campana_universidad(0.52), regla_cuenta(0.25), regla_dominio(0.11)
- **cbow**: campana_universidad(0.93), campana_banco(0.89), regla_cuenta(0.88)
- **skipgram**: campana_universidad(1.00), campana_banco(1.00), regla_cuenta(1.00)
- **glove**: campana_universidad(0.91), regla_cuenta(0.82), campana_dian(0.73)

### q5  gold=['campana_drive', 'regla_dominio', 'regla_credenciales']
Google Drive: documento confidencial
Le compartieron Nómina.xlsx. Para verlo verifique la cuenta en http://g00gle-drive.net/nomina
- **bm25**: campana_drive(17.63), regla_dominio(4.05), campana_paquete(1.84)
- **tfidf**: campana_drive(0.55), regla_dominio(0.13), campana_paquete(0.06)
- **cbow**: campana_drive(0.91), regla_dominio(0.83), campana_paquete(0.82)
- **skipgram**: campana_drive(1.00), regla_dominio(1.00), regla_cuenta(1.00)
- **glove**: campana_drive(0.89), regla_dominio(0.52), campana_universidad(0.52)

### q6  gold=['campana_banco', 'regla_cuenta', 'regla_credenciales']
Nequi bloqueará su cuenta
Actualice su PIN de inmediato o perderá el saldo. Formulario: http://nequi-seguridad.xyz/pin
- **bm25**: regla_cuenta(8.17), regla_credenciales(7.29), campana_banco(4.66)
- **tfidf**: regla_credenciales(0.33), regla_cuenta(0.27), campana_banco(0.17)
- **cbow**: regla_credenciales(0.91), regla_cuenta(0.91), regla_enlace(0.91)
- **skipgram**: regla_credenciales(1.00), regla_cuenta(1.00), regla_enlace(1.00)
- **glove**: regla_credenciales(0.89), regla_enlace(0.86), campana_universidad(0.85)

### q7  gold=['campana_dian', 'regla_premio', 'regla_urgencia']
Premio de compensación
Fue seleccionado. Pague el impuesto de $40.000 y reciba $8.000.000: http://premio-dian.win/cobrar
- **bm25**: regla_premio(10.95), campana_dian(6.57), campana_universidad(3.04)
- **tfidf**: regla_premio(0.42), campana_dian(0.27), campana_universidad(0.16)
- **cbow**: campana_dian(0.81), regla_urgencia(0.80), campana_universidad(0.80)
- **skipgram**: regla_premio(1.00), campana_dian(1.00), regla_enlace(1.00)
- **glove**: campana_universidad(0.84), regla_premio(0.77), campana_dian(0.76)

### q8  gold=['regla_adjunto', 'campana_dian']
Factura electrónicá pendiente
Abra el adjunto factura_claro.html y habilite el contenido para descargar el PDF de la DIAN.
- **bm25**: regla_adjunto(13.78), regla_dominio(5.27), campana_dian(4.13)
- **tfidf**: regla_adjunto(0.53), regla_dominio(0.23), regla_enlace(0.19)
- **cbow**: regla_adjunto(0.90), regla_dominio(0.87), regla_enlace(0.87)
- **skipgram**: regla_adjunto(1.00), regla_enlace(1.00), regla_dominio(1.00)
- **glove**: regla_adjunto(0.90), regla_enlace(0.87), campana_universidad(0.86)
