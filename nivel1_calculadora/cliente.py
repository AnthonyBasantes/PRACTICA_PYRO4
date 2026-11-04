import Pyro4


def mostrar_menu():
    print("\n========== CALCULADORA DISTRIBUIDA ==========")
    print("1. Sumar")
    print("2. Restar")
    print("3. Multiplicar")
    print("4. Dividir")
    print("5. Salir")


def main():
    print("=" * 50)
    print("CLIENTE - CALCULADORA PYRO4")
    print("=" * 50)

    uri = input("Ingrese la URI del servidor: ").strip()

    try:
        with Pyro4.Proxy(uri) as calculadora:

            while True:
                mostrar_menu()
                opcion = input("Seleccione una opción: ").strip()

                if opcion == "5":
                    print("Cliente desconectado.")
                    break

                if opcion not in ("1", "2", "3", "4"):
                    print("Opción no válida.")
                    continue

                try:
                    a = float(input("Ingrese el primer número: "))
                    b = float(input("Ingrese el segundo número: "))

                    if opcion == "1":
                        resultado = calculadora.sumar(a, b)

                    elif opcion == "2":
                        resultado = calculadora.restar(a, b)

                    elif opcion == "3":
                        resultado = calculadora.multiplicar(a, b)

                    else:
                        resultado = calculadora.dividir(a, b)

                    print(f"\nResultado: {resultado}")

                except ValueError:
                    print("Error: ingrese números válidos.")

                except Exception as error:
                    print(f"Error en la operación: {error}")

    except Pyro4.errors.PyroError as error:
        print(f"No se pudo conectar al servidor: {error}")


if __name__ == "__main__":
    main()