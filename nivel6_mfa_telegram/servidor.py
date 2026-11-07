import os
import time
import hmac
import secrets
import hashlib
import threading
import requests
import Pyro4

from dotenv import load_dotenv
from base_datos import iniciar_bd, buscar_usuario, verificar_password

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
IP_SERVIDOR = os.getenv("IP_SERVIDOR", "172.17.44.103")

if not TOKEN:
    raise RuntimeError("Falta TELEGRAM_BOT_TOKEN en .env")


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class ServidorMFA:

    def __init__(self):
        self.sesiones = {}
        self.bloqueos = {}
        self.candado = threading.RLock()

    def iniciar_sesion(self, usuario, password):
        usuario = str(usuario).strip()

        with self.candado:
            ahora = time.time()

            if ahora < self.bloqueos.get(usuario, 0):
                return {
                    "ok": False,
                    "mensaje": "Usuario bloqueado temporalmente"
                }

            datos = buscar_usuario(usuario)

            if not datos or not datos["activo"] or not verificar_password(
                password, datos["password_hash"]
            ):
                return {
                    "ok": False,
                    "mensaje": "Credenciales incorrectas"
                }

            codigo = f"{secrets.randbelow(1000000):06d}"

            mensaje = (
                "CODIGO MFA PYRO4\n\n"
                f"Usuario: {usuario}\n"
                f"Tu codigo es: {codigo}\n\n"
                "Valido durante 3 minutos.\n"
                "No compartas este codigo."
            )

            try:
                respuesta = requests.post(
                    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                    data={
                        "chat_id": datos["chat_id"],
                        "text": mensaje
                    },
                    timeout=15
                )

                respuesta.raise_for_status()

                if not respuesta.json().get("ok"):
                    raise ValueError("Telegram rechazo el mensaje")

            except (requests.RequestException, ValueError):
                return {
                    "ok": False,
                    "mensaje": "Error al enviar codigo a Telegram"
                }

            self.sesiones[usuario] = {
                "codigo_hash": hashlib.sha256(
                    codigo.encode()
                ).hexdigest(),
                "expira": time.time() + 180,
                "intentos": 0
            }

            print(f"Codigo MFA enviado al usuario: {usuario}")

            return {
                "ok": True,
                "mensaje": "Codigo enviado a Telegram"
            }

    def verificar_codigo_mfa(self, usuario, codigo):
        usuario = str(usuario).strip()

        with self.candado:
            ahora = time.time()

            if ahora < self.bloqueos.get(usuario, 0):
                return {
                    "ok": False,
                    "mensaje": "Usuario bloqueado temporalmente"
                }

            sesion = self.sesiones.get(usuario)

            if not sesion:
                return {
                    "ok": False,
                    "mensaje": "Primero inicia sesion"
                }

            if ahora > sesion["expira"]:
                del self.sesiones[usuario]

                return {
                    "ok": False,
                    "mensaje": "Codigo expirado"
                }

            codigo_hash = hashlib.sha256(
                str(codigo).encode()
            ).hexdigest()

            if not hmac.compare_digest(
                codigo_hash, sesion["codigo_hash"]
            ):
                sesion["intentos"] += 1

                if sesion["intentos"] >= 3:
                    del self.sesiones[usuario]
                    self.bloqueos[usuario] = ahora + 300

                    return {
                        "ok": False,
                        "mensaje": "Bloqueado por 5 minutos"
                    }

                return {
                    "ok": False,
                    "mensaje": "Codigo incorrecto"
                }

            del self.sesiones[usuario]

            print(f"Acceso concedido al usuario: {usuario}")

            return {
                "ok": True,
                "mensaje": "AUTENTICACION MFA EXITOSA"
            }


def main():
    iniciar_bd()

    Pyro4.config.SERIALIZER = "serpent"
    Pyro4.config.SERIALIZERS_ACCEPTED = {"serpent"}

    with Pyro4.Daemon(
        host=IP_SERVIDOR,
        port=9092
    ) as daemon:

        with Pyro4.locateNS(
            host=IP_SERVIDOR,
            port=9090
        ) as ns:

            uri = daemon.register(ServidorMFA)
            ns.register("practica.mfa", uri)

        print("================================")
        print(" SERVIDOR MFA + SQLITE")
        print("================================")
        print(f"IP: {IP_SERVIDOR}")
        print("Puerto: 9092")
        print("Servicio: practica.mfa")
        print("Base de datos: usuarios.db")
        print("Esperando conexiones...")

        daemon.requestLoop()


if __name__ == "__main__":
    main()