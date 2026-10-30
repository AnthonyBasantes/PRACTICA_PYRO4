import time
import Pyro4
from datetime import datetime


@Pyro4.expose
class ProcesadorTareas:

    def procesar_tarea(self, nombre, segundos):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre de la tarea es obligatorio.")

        if not isinstance(segundos, int) or not 1 <= segundos <= 30:
            raise ValueError("La duración debe estar entre 1 y 30 segundos.")

        inicio = datetime.now().strftime("%H:%M:%S")

        print(
            f"[{inicio}] Iniciando tarea: {nombre} "
            f"({segundos} segundos)",
            flush=True
        )

        time.sleep(segundos)

        fin = datetime.now().strftime("%H:%M:%S")

        print(
            f"[{fin}] Tarea completada: {nombre}",
            flush=True
        )

        return {
            "tarea": nombre,
            "duracion": segundos,
            "inicio": inicio,
            "fin": fin,
            "estado": "COMPLETADA"
        }


def main():
    ip_servidor = "172.17.44.97"

    with Pyro4.Daemon(host=ip_servidor) as daemon:
        uri = daemon.register(ProcesadorTareas)

        with Pyro4.locateNS(
            host=ip_servidor,
            port=9090
        ) as ns:
            ns.register("practica.procesador", uri)

        print("=" * 55)
        print("SERVIDOR DE PROCESAMIENTO - ANTHONY")
        print("=" * 55)
        print(f"IP: {ip_servidor}")
        print(f"URI: {uri}")
        print("Servicio registrado: practica.procesador")
        print("Esperando tareas remotas de Alex...")
        print("=" * 55)

        daemon.requestLoop()


if __name__ == "__main__":
    main()