
import getpass
import Pyro4

Pyro4.config.SERIALIZER = "serpent"

IP_SERVIDOR = "172.17.44.103"


def main():
    print("================================")
    print(" CLIENTE MFA PYRO4 + TELEGRAM")
    print("================================")

    try:
        ns = Pyro4.locateNS(
            host=IP_SERVIDOR,
            port=9090
        )

        uri = ns.lookup("practica.mfa")

        with Pyro4.Proxy(uri) as servidor:
            print("Conectado al servidor MFA")

            usuario = input("Usuario: ").strip()
            password = getpass.getpass("Contrasena: ")

            respuesta = servidor.iniciar_sesion(usuario, password)
            print(respuesta["mensaje"])

            if not respuesta["ok"]:
                return

            print("\nRevisa Telegram para obtener tu codigo.")

            for intento in range(3):
                codigo = input("Codigo MFA de 6 digitos: ").strip()

                resultado = servidor.verificar_codigo_mfa(
                    usuario, codigo
                )

                print(resultado["mensaje"])

                if resultado["ok"]:
                    print("\nACCESO CONCEDIDO")
                    return

                if "incorrecto" not in resultado["mensaje"].lower():
                    return

            print("\nAcceso denegado")

    except Pyro4.errors.PyroError as error:
        print("Error de conexion Pyro4:", error)
    except OSError as error:
        print("Error de red:", error)


if __name__ == "__main__":
    main()
