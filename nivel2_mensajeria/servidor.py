import Pyro4
from datetime import datetime
from threading import Lock


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class ServicioMensajes:

    def __init__(self):
        self.mensajes = []
        self.lock = Lock()

    def enviar_mensaje(self, usuario, mensaje):
        if not isinstance(usuario, str) or not usuario.strip():
            raise ValueError("El usuario no puede estar vacío")

        if not isinstance(mensaje, str) or not mensaje.strip():
            raise ValueError("El mensaje no puede estar vacío")

        fecha = datetime.now().strftime("%H:%M:%S")

        registro = {
            "usuario": usuario,
            "mensaje": mensaje,
            "hora": fecha
        }

        with self.lock:
            self.mensajes.append(registro)

        print(f"[{fecha}] {usuario}: {mensaje}", flush=True)

        return "Mensaje recibido correctamente"

    def obtener_mensajes(self):
        with self.lock:
            return list(self.mensajes)


def main():
    ip_servidor = "127.0.0.1"

    with Pyro4.Daemon(host=ip_servidor) as daemon:

        uri = daemon.register(ServicioMensajes)

        with Pyro4.locateNS(
            host=ip_servidor,
            port=9090
        ) as ns:

            ns.register("practica.mensajeria", uri)

        print("=" * 50)
        print("SERVIDOR DE MENSAJERÍA - ANTHONY")
        print("=" * 50)
        print(f"IP: {ip_servidor}")
        print(f"URI: {uri}")
        print("Servicio registrado: practica.mensajeria")
        print("Esperando mensajes de Alex...")
        print("=" * 50)

        daemon.requestLoop()


if __name__ == "__main__":
    main()