import threading
import Pyro4


def mostrar_estado(estado):
    print("\n" + "=" * 45)
    print("ESTADO ACTUAL DE LA SUBASTA")
    print("=" * 45)

    print(f"Producto: {estado['producto']}")
    print(f"Precio inicial: ${estado['precio_inicial']:.2f}")
    print(f"Precio actual: ${estado['precio_actual']:.2f}")
    print(f"Mejor postor: {estado['mejor_postor'] or 'Ninguno'}")
    print(f"Tiempo restante: {estado['tiempo_restante']} segundos")

    if estado["activa"]:
        print("Estado: SUBASTA ACTIVA")
    else:
        print("Estado: SUBASTA FINALIZADA")

        if estado["mejor_postor"]:
            print(f"Ganador: {estado['mejor_postor']}")
        else:
            print("No hubo ofertas.")

    print("=" * 45)


def monitorear_subasta(uri, detener):
    try:
        with Pyro4.Proxy(uri) as servidor:
            servidor._pyroTimeout = 5
            ultimo_estado = None

            while not detener.is_set():
                estado = servidor.obtener_estado()

                actual = (
                    estado["precio_actual"],
                    estado["mejor_postor"],
                    estado["activa"]
                )

                if actual != ultimo_estado:
                    print("\n\nACTUALIZACIÓN DE SUBASTA")
                    print(f"Precio: ${estado['precio_actual']:.2f}")
                    print(
                        f"Mejor postor: "
                        f"{estado['mejor_postor'] or 'Ninguno'}"
                    )

                    ultimo_estado = actual

                if not estado["activa"]:
                    print("\nSUBASTA FINALIZADA")

                    if estado["mejor_postor"]:
                        print(f"GANADOR: {estado['mejor_postor']}")

                    break

                detener.wait(2)

    except Pyro4.errors.PyroError as error:
        if not detener.is_set():
            print(f"\nError de monitoreo: {error}")


def main():
    print("=" * 45)
    print("CLIENTE - SISTEMA DE SUBASTAS")
    print("=" * 45)

    usuario = input("Ingrese su nombre: ").strip()

    if not usuario:
        print("Debe ingresar un nombre.")
        return

    detener = threading.Event()
    hilo = None

    try:
        with Pyro4.locateNS(
            host="127.0.0.1",
            port=9090
        ) as ns:
            uri = ns.lookup("subastas.central")

        hilo = threading.Thread(
            target=monitorear_subasta,
            args=(uri, detener),
            daemon=True
        )
        hilo.start()

        with Pyro4.Proxy(uri) as servidor:
            servidor._pyroTimeout = 5

            while True:
                print("\n1. Consultar estado")
                print("2. Realizar oferta")
                print("3. Ver historial")
                print("4. Salir")

                opcion = input("\nSeleccione una opción: ").strip()

                if opcion == "1":
                    estado = servidor.obtener_estado()
                    mostrar_estado(estado)

                elif opcion == "2":
                    monto = input("Ingrese su oferta ($): ")

                    respuesta = servidor.realizar_oferta(
                        usuario, monto
                    )

                    print(f"\n{respuesta['mensaje']}")

                elif opcion == "3":
                    estado = servidor.obtener_estado()

                    print("\nHISTORIAL DE OFERTAS")

                    if not estado["historial"]:
                        print("No existen ofertas.")
                    else:
                        for oferta in estado["historial"]:
                            print(
                                f"{oferta['hora']} | "
                                f"{oferta['usuario']} | "
                                f"${oferta['monto']:.2f}"
                            )

                elif opcion == "4":
                    print("Cliente desconectado.")
                    break

                else:
                    print("Opción no válida.")

    except Pyro4.errors.PyroError as error:
        print(f"\nError de comunicación: {error}")

    finally:
        detener.set()

        if hilo is not None:
            hilo.join(timeout=3)


if __name__ == "__main__":
    main()