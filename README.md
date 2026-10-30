# Práctica de Sistemas Distribuidos con Pyro4

## Integrantes
- Anthony Basantes — Servidor
- Alex — Cliente

## Descripción
Proyecto académico desarrollado en Python utilizando Pyro4 para implementar y probar comunicación distribuida entre dos computadoras conectadas mediante una red LAN.

## Tecnologías
- Python 3
- Pyro4
- Sockets TCP/IP
- Ubuntu
- VSCodium / Visual Studio Code
- Git y GitHub

## Niveles implementados

### Nivel 1: Calculadora distribuida
Implementación de operaciones matemáticas mediante llamadas a métodos remotos (RPC).

### Nivel 2: Mensajería con Name Server
Servicio de mensajería compartida entre clientes, utilizando el Name Server de Pyro4 para localizar el servicio remoto.

### Nivel 3: Banco distribuido
Simulación bancaria con consultas de saldo, depósitos, retiros, validaciones y administración de sesiones independientes.

### Nivel 4: Procesamiento asíncrono
Ejecución de tareas remotas mediante llamadas asíncronas, permitiendo que el cliente continúe realizando otras actividades mientras espera el resultado.

## Arquitectura
- Servidor: Anthony
- Cliente remoto: Alex
- Comunicación: Red LAN
- Name Server: Puerto 9090

## Instalación

Crear un entorno virtual:

python3 -m venv venv

Activarlo:

source venv/bin/activate

Instalar Pyro4:

pip install Pyro4==4.82

## Ejecución

Para los niveles que utilizan Name Server, iniciarlo primero:

python -m Pyro4.naming -n IP_SERVIDOR -p 9090

Después, ejecutar el servidor correspondiente:

python -u servidor.py

Finalmente, ejecutar el cliente:

python -u cliente.py

Nota: Los programas utilizan direcciones IP de la red LAN del laboratorio. Estas deben actualizarse si cambia la red.

## Estado del proyecto
- Nivel 1: Completado
- Nivel 2: Completado
- Nivel 3: Completado
- Nivel 4: Completado
- Nivel 5: Pendiente de implementación
