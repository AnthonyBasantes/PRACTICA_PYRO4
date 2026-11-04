import Pyro4


def mostrar_mensajes(servicio):
    mensajes = servicio.obtener_mensajes()

    print("\n========== MENSAJES ==========")

    if not mensajes:
        print("No hay mensajes registrados.")
    else:
        for mensaje in mensajes:
            print(
                f"[{mensaje['hora']}] "
                f"{mensaje['usuario']}: "
                f"{mensaje['mensaje']}"
            )

    print("==============================\n")


def main():
    print("=" * 50)
    print("CLIENTE DE MENSAJERÍA - PYRO4")
    print("=" * 50)

    usuario = input("Ingrese su nombre: ").strip()

    if not usuario:
        print("El nombre es obligatorio.")
        return

    try:
        with Pyro4.locateNS(
            host="127.0.0.1",
            port=9090
        ) as ns:
            uri = ns.lookup("practica.mensajeria")

        print("Servicio de mensajería localizado.")

        with Pyro4.Proxy(uri) as servicio:

            while True:
                print("\n1. Enviar mensaje")
                print("2. Consultar mensajes")
                print("3. Salir")

                opcion = input("\nSeleccione una opción: ").strip()

                if opcion == "1":
                    mensaje = input("Escriba su mensaje: ").strip()

                    if not mensaje:
                        print("El mensaje no puede estar vacío.")
                        continue

                    respuesta = servicio.enviar_mensaje(
                        usuario,
                        mensaje
                    )

                    print(f"\n[SERVIDOR] {respuesta}")

                elif opcion == "2":
                    mostrar_mensajes(servicio)

                elif opcion == "3":
                    print("Cliente desconectado.")
                    break

                else:
                    print("Opción no válida.")

    except Pyro4.errors.PyroError as error:
        print(f"Error de comunicación: {error}")


if __name__ == "__main__":
    main()