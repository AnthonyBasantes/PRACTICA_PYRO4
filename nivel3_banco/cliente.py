import Pyro4
from decimal import Decimal, InvalidOperation


def mostrar_menu():
    print("\n" + "=" * 45)
    print("BANCO DISTRIBUIDO - PYRO4")
    print("=" * 45)
    print("1. Consultar saldo")
    print("2. Depositar dinero")
    print("3. Retirar dinero")
    print("4. Salir")


def solicitar_monto():
    while True:
        entrada = input("Ingrese el monto ($): ").strip()

        try:
            monto = Decimal(entrada)

            if not monto.is_finite() or monto <= 0:
                print("ERROR: Ingrese un monto positivo.")
                continue

            if monto.as_tuple().exponent < -2:
                print("ERROR: Utilice máximo dos decimales.")
                continue

            return str(monto)

        except InvalidOperation:
            print("ERROR: Ingrese un número válido.")


def mostrar_error(error):
    mensaje = str(error)

    if (
        "SaldoInsuficienteError" in mensaje
        or "Fondos insuficientes" in mensaje
    ):
        print("\n" + "=" * 45)
        print("OPERACIÓN RECHAZADA")
        print("Fondos insuficientes para realizar el retiro.")
        print("El monto solicitado supera el saldo disponible.")
        print("=" * 45)

    else:
        print(f"\nOPERACIÓN RECHAZADA: {error}")


def main():
    print("=" * 50)
    print("CLIENTE BANCARIO - PYRO4")
    print("=" * 50)

    try:
        with Pyro4.locateNS(
            host="127.0.0.1",
            port=9090
        ) as ns:
            uri = ns.lookup("practica.banco")

        with Pyro4.Proxy(uri) as banco:
            banco._pyroTimeout = 10
            banco._pyroBind()

            print("\nConectado al servidor bancario.")
            print("Sesión iniciada correctamente.")

            while True:
                mostrar_menu()
                opcion = input("\nSeleccione una opción: ").strip()

                try:
                    if opcion == "1":
                        saldo = banco.consultar_saldo()
                        print(f"\nSALDO ACTUAL: ${saldo:.2f}")

                    elif opcion == "2":
                        monto = solicitar_monto()
                        saldo = banco.depositar(monto)

                        print("\nDEPÓSITO EXITOSO")
                        print(f"Monto depositado: ${Decimal(monto):.2f}")
                        print(f"Nuevo saldo: ${saldo:.2f}")

                    elif opcion == "3":
                        monto = solicitar_monto()
                        saldo = banco.retirar(monto)

                        print("\nRETIRO EXITOSO")
                        print(f"Monto retirado: ${Decimal(monto):.2f}")
                        print(f"Nuevo saldo: ${saldo:.2f}")

                    elif opcion == "4":
                        print("\nSesión bancaria finalizada.")
                        break

                    else:
                        print("\nERROR: Opción no válida.")

                except Pyro4.errors.CommunicationError as error:
                    print(f"\nError de comunicación: {error}")
                    break

                except Exception as error:
                    mostrar_error(error)

    except Pyro4.errors.PyroError as error:
        print(f"\nNo se pudo conectar al banco: {error}")

    except Exception as error:
        print(f"\nError inesperado: {error}")


if __name__ == "__main__":
    main()