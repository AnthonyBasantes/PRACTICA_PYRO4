
import os
import time
import hmac
import secrets
import hashlib
import requests
import Pyro4
from dotenv import load_dotenv

load_dotenv(".env")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
CLAVE = os.getenv("MFA_PASSWORD", "123456")

if not TOKEN or not CHAT_ID:
    raise RuntimeError("Configura TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID en .env")

USUARIOS = {
    "alex": {
        "clave": hashlib.sha256(CLAVE.encode()).hexdigest(),
        "chat_id": CHAT_ID
    }
}


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class ServidorMFA:

    def __init__(self):
        self.sesiones = {}
        self.bloqueos = {}

    def iniciar_sesion(self, usuario, password):
        ahora = time.time()

        if ahora < self.bloqueos.get(usuario, 0):
            return {"ok": False, "mensaje": "Usuario bloqueado temporalmente"}

        datos = USUARIOS.get(usuario)

        if not datos or not hmac.compare_digest(
            hashlib.sha256(password.encode()).hexdigest(),
            datos["clave"]
        ):
            return {"ok": False, "mensaje": "Credenciales incorrectas"}

        codigo = f"{secrets.randbelow(1000000):06d}"

        mensaje = (
            "🔐 CODIGO MFA PYRO4\n\n"
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
                raise RuntimeError("Telegram rechazo el mensaje")

        except (requests.RequestException, RuntimeError) as error:
            print("Error enviando codigo:", error)
            return {"ok": False, "mensaje": "No se pudo enviar el codigo MFA"}

        self.sesiones[usuario] = {
            "codigo_hash": hashlib.sha256(codigo.encode()).hexdigest(),
            "expira": time.time() + 180,
            "intentos": 0
        }

        print(f"Codigo MFA enviado a Telegram para {usuario}")

        return {
            "ok": True,
            "mensaje": "Codigo enviado a Telegram"
        }

    def verificar_codigo_mfa(self, usuario, codigo):
        ahora = time.time()

        if ahora < self.bloqueos.get(usuario, 0):
            return {"ok": False, "mensaje": "Usuario bloqueado temporalmente"}

        sesion = self.sesiones.get(usuario)

        if not sesion:
            return {"ok": False, "mensaje": "Primero inicia sesion"}

        if ahora > sesion["expira"]:
            del self.sesiones[usuario]
            return {"ok": False, "mensaje": "Codigo expirado"}

        codigo_hash = hashlib.sha256(str(codigo).encode()).hexdigest()

        if not hmac.compare_digest(codigo_hash, sesion["codigo_hash"]):
            sesion["intentos"] += 1

            if sesion["intentos"] >= 3:
                del self.sesiones[usuario]
                self.bloqueos[usuario] = ahora + 300
                return {"ok": False, "mensaje": "Bloqueado por 5 minutos"}

            return {"ok": False, "mensaje": "Codigo incorrecto"}

        del self.sesiones[usuario]

        return {
            "ok": True,
            "mensaje": "AUTENTICACION MFA EXITOSA"
        }


def main():
    Pyro4.config.SERIALIZER = "serpent"

    daemon = Pyro4.Daemon(
        host="172.17.44.103",
        port=9092
    )

    ns = Pyro4.locateNS(
        host="172.17.44.103",
        port=9090
    )

    uri = daemon.register(ServidorMFA)
    ns.register("practica.mfa", uri)

    print("================================")
    print(" SERVIDOR MFA PYRO4 + TELEGRAM")
    print("================================")
    print("Servicio: practica.mfa")
    print("IP: 172.17.44.103")
    print("Puerto: 9092")
    print("Esperando conexiones de Alex...")

    daemon.requestLoop()


if __name__ == "__main__":
    main()
