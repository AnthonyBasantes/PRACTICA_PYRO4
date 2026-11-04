# Práctica de Sistemas Distribuidos con Pyro4

## Integrantes

- **Anthony Basantes:** Servidor
- **Alex:** Cliente

## Descripción

Proyecto académico desarrollado en Python utilizando Pyro4 para implementar y probar diferentes mecanismos de comunicación distribuida mediante llamadas a procedimientos remotos (RPC).

La práctica comprende cinco niveles progresivos que permiten estudiar la comunicación entre procesos, el descubrimiento de servicios, la administración de sesiones, el procesamiento asíncrono y la concurrencia.

Las pruebas se realizaron utilizando Ubuntu, con comunicación local mediante `127.0.0.1`. La arquitectura también permite realizar pruebas entre computadoras conectadas a una red LAN, configurando las direcciones IP correspondientes.

## Objetivos

- Comprender el funcionamiento de las llamadas a métodos remotos mediante Pyro4.
- Implementar servicios distribuidos utilizando Python.
- Utilizar el Name Server para registrar y localizar servicios.
- Analizar las diferencias entre servicios con estado y sin estado.
- Implementar operaciones asíncronas.
- Gestionar solicitudes concurrentes mediante mecanismos de sincronización.
- Comprobar el funcionamiento de los servicios mediante clientes independientes.

## Tecnologías utilizadas

- Python 3
- Pyro4 4.82
- Comunicación TCP/IP
- Ubuntu
- VSCodium / Visual Studio Code
- Git y GitHub
- Módulo `threading` de Python

## Estructura del proyecto

```text
PRACTICA_PYRO4/
│
├── nivel1_calculadora/
│   ├── servidor.py
│   └── cliente.py
│
├── nivel2_mensajeria/
│   ├── servidor.py
│   └── cliente.py
│
├── nivel3_banco/
│   ├── servidor.py
│   └── cliente.py
│
├── nivel4_asincrono/
│   ├── servidor.py
│   └── cliente.py
│
├── nivel5_subastas/
│   ├── servidor.py
│   └── cliente.py
│
├── .gitignore
└── README.md
```

## Niveles implementados

### Nivel 1: Calculadora distribuida

Implementación de una calculadora que permite ejecutar operaciones matemáticas mediante llamadas a métodos remotos.

**Funcionalidades:**

- Suma.
- Resta.
- Multiplicación.
- División.
- Comunicación mediante URI de Pyro4.

**Concepto aplicado:** llamadas a procedimientos remotos (RPC).

### Nivel 2: Mensajería distribuida

Sistema de mensajería que permite intercambiar mensajes entre diferentes clientes conectados a un servicio compartido.

**Funcionalidades:**

- Registro del servicio en el Name Server.
- Envío de mensajes.
- Consulta del historial.
- Identificación de usuarios.
- Comunicación entre clientes.

**Servicio registrado:** `practica.mensajeria`

**Concepto aplicado:** descubrimiento de servicios y estado compartido.

### Nivel 3: Banco distribuido

Simulación de un sistema bancario que permite administrar operaciones financieras mediante sesiones independientes.

**Funcionalidades:**

- Consulta de saldo.
- Depósitos.
- Retiros.
- Validación de fondos disponibles.
- Administración de saldos independientes por sesión.

Cada sesión comienza con un saldo inicial de $100.

**Servicio registrado:** `practica.banco`

**Concepto aplicado:** administración de estado mediante `instance_mode="session"`.

### Nivel 4: Procesamiento asíncrono

Implementación de un servicio que ejecuta tareas remotas de larga duración.

**Funcionalidades:**

- Envío de tareas al servidor.
- Procesamiento remoto.
- Ejecución de otras actividades mientras se espera el resultado.
- Consulta del resultado final.

**Servicio registrado:** `practica.procesador`

**Concepto aplicado:** comunicación asíncrona mediante Pyro4.

### Nivel 5: Sistema distribuido de subastas

Implementación de una plataforma de subastas que permite a varios clientes competir mediante ofertas.

**Funcionalidades:**

- Producto con precio inicial.
- Duración limitada de la subasta.
- Registro de ofertas.
- Validación de montos.
- Rechazo de ofertas inferiores o iguales al precio actual.
- Actualización automática del mejor postor.
- Consulta del historial.
- Determinación del ganador.
- Control de concurrencia mediante `threading.Lock`.

**Servicio registrado:** `subastas.central`

**Conceptos aplicados:** concurrencia, sincronización, estado compartido y comunicación distribuida.

## Arquitectura del sistema

La práctica utiliza una arquitectura cliente-servidor.

**Servidor:** ejecuta los servicios remotos y procesa las solicitudes.

**Cliente:** invoca los métodos publicados por el servidor mediante Pyro4.

**Name Server:** permite localizar servicios registrados mediante nombres.

En las pruebas locales se utilizó:

- Dirección IP: `127.0.0.1`
- Puerto del Name Server: `9090`

Para ejecutar la práctica en una red LAN, deben configurarse las direcciones IP del servidor y de los clientes.

## Instalación

### 1. Crear el entorno virtual

```bash
python3 -m venv venv
```

### 2. Activar el entorno virtual

```bash
source venv/bin/activate
```

### 3. Instalar Pyro4

```bash
python -m pip install Pyro4==4.82
```

## Ejecución

Todos los comandos deben ejecutarse desde la carpeta principal del proyecto, con el entorno virtual activado.

### Nivel 1: Calculadora

**Terminal 1 — Servidor:**

```bash
python nivel1_calculadora/servidor.py
```

**Terminal 2 — Cliente:**

```bash
python nivel1_calculadora/cliente.py
```

El cliente debe utilizar la URI proporcionada por el servidor.

### Niveles 2, 3, 4 y 5

Primero, iniciar el Name Server:

```bash
python -m Pyro4.naming -n 127.0.0.1 -p 9090
```

El Name Server debe permanecer ejecutándose.

**Nivel 2 — Mensajería:**

```bash
python nivel2_mensajeria/servidor.py
```

En otra terminal:

```bash
python nivel2_mensajeria/cliente.py
```

**Nivel 3 — Banco:**

```bash
python nivel3_banco/servidor.py
```

En otra terminal:

```bash
python nivel3_banco/cliente.py
```

**Nivel 4 — Procesamiento asíncrono:**

```bash
python nivel4_asincrono/servidor.py
```

En otra terminal:

```bash
python nivel4_asincrono/cliente.py
```

**Nivel 5 — Subastas:**

```bash
python nivel5_subastas/servidor.py
```

En otras terminales, ejecutar dos clientes:

```bash
python nivel5_subastas/cliente.py
```

Cada cliente debe ingresar su nombre para participar en la subasta.

## Pruebas realizadas

Durante el desarrollo se efectuaron pruebas funcionales de los cinco niveles.

| Nivel | Prueba | Resultado |
|---|---|---|
| 1 | Operaciones matemáticas remotas | Correcto |
| 2 | Envío y consulta de mensajes | Correcto |
| 3 | Consulta, depósito y retiro | Correcto |
| 4 | Ejecución de tareas asíncronas | Correcto |
| 5 | Ofertas entre clientes y determinación del ganador | Correcto |

## Resultados

La práctica permitió implementar cinco aplicaciones que utilizan mecanismos de comunicación distribuida.

Se comprobó el funcionamiento de las llamadas remotas, el descubrimiento de servicios mediante Name Server, la administración de sesiones independientes, el procesamiento asíncrono y la sincronización de operaciones concurrentes.

## Conclusiones

1. Pyro4 permite implementar comunicación entre procesos mediante llamadas a métodos remotos, simplificando el desarrollo de aplicaciones distribuidas en Python.

2. El Name Server facilita la localización de servicios sin necesidad de introducir manualmente una URI completa en cada cliente.

3. La administración de sesiones permite mantener información independiente para diferentes clientes, como se comprobó en el sistema bancario.

4. El procesamiento asíncrono permite que un cliente continúe realizando actividades mientras espera el resultado de una operación remota.

5. La sincronización mediante mecanismos como `threading.Lock` resulta importante para evitar conflictos cuando varios clientes modifican información compartida.

## Estado del proyecto

- Nivel 1: Completado.
- Nivel 2: Completado.
- Nivel 3: Completado.
- Nivel 4: Completado.
- Nivel 5: Completado.

**Estado general: práctica finalizada.**