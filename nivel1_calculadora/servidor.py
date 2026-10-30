import Pyro4


@Pyro4.expose
class Calculadora:

    def sumar(self, a, b):
        resultado = a + b
        print(f"[CLIENTE ALEX] SUMA: {a} + {b}")
        print(f"[SERVIDOR] Resultado enviado: {resultado}\n")
        return resultado

    def restar(self, a, b):
        resultado = a - b
        print(f"[CLIENTE ALEX] RESTA: {a} - {b}")
        print(f"[SERVIDOR] Resultado enviado: {resultado}\n")
        return resultado

    def multiplicar(self, a, b):
        resultado = a * b
        print(f"[CLIENTE ALEX] MULTIPLICACIÓN: {a} * {b}")
        print(f"[SERVIDOR] Resultado enviado: {resultado}\n")
        return resultado

    def dividir(self, a, b):
        print(f"[CLIENTE ALEX] DIVISIÓN: {a} / {b}")

        if b == 0:
            print("[SERVIDOR] Error: División entre cero\n")
            raise ValueError("No se puede dividir entre cero")

        resultado = a / b
        print(f"[SERVIDOR] Resultado enviado: {resultado}\n")
        return resultado


def main():
    ip_servidor = "172.17.44.97"

    with Pyro4.Daemon(host=ip_servidor) as daemon:
        uri = daemon.register(Calculadora)

        print("=== SERVIDOR DE ANTHONY ===")
        print(f"IP: {ip_servidor}")
        print(f"URI: {uri}")
        print("Esperando solicitudes de Alex...\n")

        daemon.requestLoop()


if __name__ == "__main__":
    main()