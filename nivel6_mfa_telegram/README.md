
# Nivel 6 - Autenticación MFA con Pyro4 y Telegram

## Descripción

Sistema de autenticación multifactor (MFA) desarrollado en Python mediante Pyro4 y Telegram Bot API.

El cliente se conecta al servidor mediante RPC, introduce sus credenciales y recibe un código de verificación de seis dígitos a través de Telegram.

## Integrantes

- Anthony Basantes: servidor Pyro4 e integración con Telegram.
- Alex: cliente Pyro4 y pruebas de autenticación.

## Tecnologías

- Python 3
- Pyro4
- Telegram Bot API
- Requests
- Python-dotenv

## Funcionamiento

1. El servidor registra el servicio `practica.mfa` en el Name Server.
2. El cliente solicita iniciar sesión con usuario y contraseña.
3. El servidor valida las credenciales.
4. Se genera un código aleatorio de seis dígitos.
5. El código se envía al Telegram configurado.
6. El cliente introduce el código recibido.
7. El servidor verifica el código y concede o rechaza el acceso.

## Seguridad

- Códigos generados mediante `secrets`.
- Validez del código: 3 minutos.
- Máximo de 3 intentos incorrectos.
- Bloqueo temporal de 5 minutos.
- Comparación segura de códigos.
- Token de Telegram almacenado en `.env`, excluido de Git.

## Instalación

Instalar las dependencias:

```bash
pip install Pyro4 requests python-dotenv
```

Crear un archivo `.env` a partir de `.env.example` y completar los valores reales.

## Ejecución

### PC servidor

Iniciar el Name Server:

```bash
python3 -m Pyro4.naming -n 172.17.44.103 -p 9090
```

En otra terminal:

```bash
python3 servidor.py
```

### PC cliente

```bash
python3 cliente.py
```

Las direcciones IP corresponden a la red utilizada durante la práctica y deben modificarse si cambia la red.

## Pruebas realizadas

| Prueba | Resultado |
|---|---|
| Credenciales correctas y código válido | Acceso concedido |
| Contraseña incorrecta | Acceso rechazado |
| Tres códigos incorrectos | Bloqueo de 5 minutos |
| Inicio de sesión durante el bloqueo | Acceso rechazado |
| Código expirado | Código rechazado |

## Resultado

Se implementó y probó exitosamente la comunicación distribuida entre dos computadoras mediante Pyro4, incorporando un segundo factor de autenticación a través de Telegram.
