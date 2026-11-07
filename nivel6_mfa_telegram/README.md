# Nivel 6 - Autenticación MFA con Pyro4, Telegram y SQLite

## Descripción

Sistema distribuido de autenticación multifactor (MFA) desarrollado en Python utilizando Pyro4 para la comunicación RPC, SQLite para almacenar usuarios y Telegram para enviar códigos de verificación.

El sistema permite que clientes de diferentes computadoras se autentiquen mediante usuario, contraseña y un código temporal de seis dígitos.

## Tecnologías utilizadas

- Python 3
- Pyro4
- SQLite3
- Telegram Bot API
- Requests
- Python-dotenv
- Threading
- Hashlib, HMAC y Secrets

## Archivos principales

- servidor.py: servidor RPC y autenticación MFA.
- cliente.py: cliente que solicita la autenticación.
- base_datos.py: gestión de usuarios mediante SQLite.
- crear_usuario.py: registro de nuevos usuarios.
- requirements.txt: dependencias del proyecto.
- .env.example: ejemplo de configuración.
- .gitignore: exclusión de archivos privados.

## Funcionalidades

1. Registro de usuarios en SQLite.
2. Almacenamiento de contraseñas mediante hashes.
3. Validación de usuarios activos e inactivos.
4. Comunicación cliente-servidor mediante Pyro4.
5. Generación de códigos MFA de seis dígitos.
6. Envío de códigos mediante Telegram.
7. Expiración de códigos después de tres minutos.
8. Bloqueo temporal de cinco minutos después de tres códigos incorrectos.
9. Protección de datos compartidos mediante RLock.
10. Soporte para múltiples clientes en una red LAN.

## Instalación

Crear y activar el entorno virtual:

python3 -m venv venv
source venv/bin/activate

Instalar dependencias:

pip install -r requirements.txt

## Configuración

Crear un archivo .env dentro de nivel6_mfa_telegram:

TELEGRAM_BOT_TOKEN=TOKEN_DE_TU_BOT
IP_SERVIDOR=IP_DE_TU_SERVIDOR

El token se obtiene mediante BotFather en Telegram.

No subir el archivo .env a GitHub.

## Registro de usuarios

Ejecutar:

python3 crear_usuario.py

Ingresar:
- Nombre de usuario.
- Contraseña.
- Chat ID de Telegram.

Los usuarios se almacenan en usuarios.db.

## Ejecución

### Terminal 1 - Name Server

python3 -m Pyro4.naming -n IP_DEL_SERVIDOR -p 9090

### Terminal 2 - Servidor MFA

python3 servidor.py

### Terminal 3 - Cliente

python3 cliente.py

El cliente debe estar configurado para conectarse a la IP del Name Server.

## Funcionamiento

1. El cliente envía usuario y contraseña al servidor.
2. El servidor consulta SQLite.
3. Verifica que el usuario exista, esté activo y tenga la contraseña correcta.
4. Genera un código MFA de seis dígitos.
5. Envía el código al Telegram registrado.
6. El cliente introduce el código recibido.
7. El servidor verifica el código y su tiempo de validez.
8. Si el código es correcto, la autenticación es exitosa.

## Seguridad

- Contraseñas almacenadas mediante PBKDF2-HMAC-SHA256.
- Códigos MFA generados con secrets.
- Comparación de hashes mediante hmac.compare_digest.
- Códigos válidos durante 180 segundos.
- Bloqueo de cinco minutos después de tres intentos MFA incorrectos.
- Token de Telegram almacenado en .env.
- Exclusión de la base de datos real mediante .gitignore.

## Pruebas realizadas

- Autenticación con usuario y contraseña.
- Recepción del código MFA por Telegram.
- Verificación de códigos correctos e incorrectos.
- Registro de múltiples usuarios en SQLite.
- Desactivación de usuarios mediante el campo activo.
- Comunicación entre computadoras de la red LAN.

## Nota

Este proyecto fue desarrollado con fines académicos para demostrar programación distribuida, llamadas a procedimientos remotos (RPC), persistencia de datos y autenticación multifactor.

Para un entorno de producción se requerirían medidas adicionales, como cifrado TLS, controles de acceso más estrictos y gestión persistente de bloqueos.
