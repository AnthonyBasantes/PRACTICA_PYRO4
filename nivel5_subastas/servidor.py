import time
import threading
from decimal import Decimal, InvalidOperation

import Pyro4


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class SistemaSubastas:

    def __init__(self):
        self.producto = "Laptop Gamer"
        self.precio_inicial = Decimal("500.00")
        self.precio_actual = self.precio_inicial
        self.mejor_postor = None
        self.duracion = 120
        self.fecha_fin = time.time() + self.duracion
        self.historial = []
        self.lock = threading.Lock()

        print("=" * 55)
        print("SISTEMA DISTRIBUIDO DE SUBASTAS")
        print("=" * 55)
        print(f"Producto: {self.producto}")
        print(f"Precio inicial: ${self.precio_inicial}")
        print(f"Duración: {self.duracion} segundos")
        print("=" * 55)

    def obtener_estado(self):
        with self.lock:
            tiempo_restante = max(
                0,
                int(self.fecha_fin - time.time())
            )

            return {
                "producto": self.producto,
                "precio_inicial": float(self.precio_inicial),
                "precio_actual": float(self.precio_actual),
                "mejor_postor": self.mejor_postor,
                "tiempo_restante": tiempo_restante,
                "activa": time.time() < self.fecha_fin,
                "historial": list(self.historial),
            }

    def realizar_oferta(self, usuario, monto):
        if not isinstance(usuario, str) or not usuario.strip():
            return {
                "aceptada": False,
                "mensaje": "Debe ingresar un nombre válido."
            }

        try:
            cantidad = Decimal(str(monto))
        except (InvalidOperation, ValueError, TypeError):
            return {
                "aceptada": False,
                "mensaje": "El monto ingresado no es válido."
            }

        if not cantidad.is_finite() or cantidad <= 0:
            return {
                "aceptada": False,
                "mensaje": "La oferta debe ser un monto positivo."
            }

        if cantidad.as_tuple().exponent < -2:
            return {
                "aceptada": False,
                "mensaje": "Utilice máximo dos decimales."
            }

        with self.lock:
            if time.time() >= self.fecha_fin:
                return {
                    "aceptada": False,
                    "mensaje": "La subasta ya finalizó."
                }

            if cantidad <= self.precio_actual:
                return {
                    "aceptada": False,
                    "mensaje": (
                        "La oferta debe superar el precio actual "
                        f"de ${self.precio_actual:.2f}."
                    )
                }

            self.precio_actual = cantidad
            self.mejor_postor = usuario.strip()

            registro = {
                "usuario": self.mejor_postor,
                "monto": float(cantidad),
                "hora": time.strftime("%H:%M:%S")
            }

            self.historial.append(registro)

            print(
                f"[{registro['hora']}] "
                f"Nueva oferta de {self.mejor_postor}: "
                f"${cantidad:.2f}",
                flush=True
            )

            return {
                "aceptada": True,
                "mensaje": (
                    f"Oferta aceptada: ${cantidad:.2f}. "
                    f"Mejor postor: {self.mejor_postor}"
                )
            }


def main():
    ip_servidor = "127.0.0.1"

    with Pyro4.Daemon(host=ip_servidor) as daemon:
        uri = daemon.register(SistemaSubastas)

        with Pyro4.locateNS(
            host=ip_servidor,
            port=9090
        ) as ns:
            ns.register("subastas.central", uri)

        print("\nServidor de subastas iniciado correctamente.")
        print(f"Servicio registrado: subastas.central")
        print(f"URI: {uri}")
        print("Esperando ofertas de los clientes...\n")

        daemon.requestLoop()


if __name__ == "__main__":
    main()