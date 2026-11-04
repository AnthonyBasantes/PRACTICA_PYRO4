import Pyro4
import time


def main():
    print("=" * 55)
    print("CLIENTE ASÍNCRONO - PYRO4")
    print("=" * 55)

    try:
        with Pyro4.locateNS(
            host="127.0.0.1",
            port=9090
        ) as ns:
            uri = ns.lookup("practica.procesador")

        print("Servicio remoto localizado correctamente.")

        with Pyro4.Proxy(uri) as servidor:
            servidor._pyroTimeout = 40

            Pyro4.asyncproxy(servidor)

            print("\nEnviando tarea de 10 segundos...")

            inicio = time.monotonic()

            resultado_futuro = servidor.procesar_tarea(
                "Procesamiento de datos",
                10
            )

            print("Solicitud enviada de forma asíncrona.")
            print("El cliente puede continuar trabajando.\n")

            contador = 0

            while not resultado_futuro.ready:
                contador += 1

                print(
                    f"[CLIENTE] Realizando otra actividad... {contador}"
                )

                time.sleep(1)

            resultado = resultado_futuro.value
            tiempo_total = time.monotonic() - inicio

            print("\n" + "=" * 55)
            print("RESULTADO RECIBIDO")
            print("=" * 55)
            print(f"Tarea: {resultado['tarea']}")
            print(f"Estado: {resultado['estado']}")
            print(f"Duración: {resultado['duracion']} segundos")
            print(f"Inicio: {resultado['inicio']}")
            print(f"Fin: {resultado['fin']}")
            print(f"Tiempo total: {tiempo_total:.2f} segundos")
            print("=" * 55)

    except Pyro4.errors.PyroError as error:
        print(f"Error de comunicación: {error}")

    except Exception as error:
        print(f"Error durante el procesamiento: {error}")


if __name__ == "__main__":
    main()