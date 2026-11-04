import Pyro4
from decimal import Decimal, InvalidOperation


class SaldoInsuficienteError(Exception):
    pass


@Pyro4.expose
@Pyro4.behavior(instance_mode="session")
class CuentaBancaria:

    def __init__(self):
        self.saldo = Decimal("100.00")
        print("[SERVIDOR] Nueva sesión bancaria iniciada.", flush=True)

    def consultar_saldo(self):
        print(
            f"[SERVIDOR] Consulta de saldo: ${self.saldo:.2f}",
            flush=True
        )
        return float(self.saldo)

    def depositar(self, monto):
        cantidad = self.validar_monto(monto)
        self.saldo += cantidad

        print(
            f"[SERVIDOR] Depósito: ${cantidad:.2f} | "
            f"Saldo: ${self.saldo:.2f}",
            flush=True
        )

        return float(self.saldo)

    def retirar(self, monto):
        cantidad = self.validar_monto(monto)

        if cantidad > self.saldo:
            print(
                "[SERVIDOR] Retiro rechazado: saldo insuficiente.",
                flush=True
            )
            raise SaldoInsuficienteError(
                "Fondos insuficientes para realizar el retiro."
            )

        self.saldo -= cantidad

        print(
            f"[SERVIDOR] Retiro: ${cantidad:.2f} | "
            f"Saldo: ${self.saldo:.2f}",
            flush=True
        )

        return float(self.saldo)

    @staticmethod
    def validar_monto(monto):
        try:
            cantidad = Decimal(str(monto))
        except (InvalidOperation, ValueError, TypeError):
            raise ValueError("El monto ingresado no es válido.")

        if not cantidad.is_finite() or cantidad <= 0:
            raise ValueError("El monto debe ser mayor que cero.")

        if cantidad.as_tuple().exponent < -2:
            raise ValueError("Utilice máximo dos decimales.")

        return cantidad


def main():
    ip_servidor = "127.0.0.1"

    with Pyro4.Daemon(host=ip_servidor) as daemon:

        uri = daemon.register(CuentaBancaria)

        with Pyro4.locateNS(
            host=ip_servidor,
            port=9090
        ) as ns:
            ns.register("practica.banco", uri)

        print("=" * 50)
        print("BANCO DISTRIBUIDO - SERVIDOR ANTHONY")
        print("=" * 50)
        print(f"IP: {ip_servidor}")
        print(f"URI: {uri}")
        print("Servicio registrado: practica.banco")
        print("Política de instancia: SESSION")
        print("Saldo inicial por sesión: $100.00")
        print("Esperando operaciones bancarias de Alex...")
        print("=" * 50)

        daemon.requestLoop()


if __name__ == "__main__":
    main()