import os
import sqlite3
import hashlib
import hmac
from pathlib import Path

RUTA_DB = Path(__file__).with_name("usuarios.db")


def conectar():
    conexion = sqlite3.connect(RUTA_DB, timeout=10)
    conexion.row_factory = sqlite3.Row
    return conexion


def iniciar_bd():
    with conectar() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                chat_id TEXT NOT NULL,
                activo INTEGER NOT NULL DEFAULT 1
            )
        """)


def hash_password(clave):
    sal = os.urandom(16)

    resultado = hashlib.pbkdf2_hmac(
        "sha256", clave.encode(), sal, 310000
    )

    return f"{sal.hex()}${resultado.hex()}"


def verificar_password(clave, guardado):
    try:
        sal_hex, esperado = guardado.split("$", 1)

        calculado = hashlib.pbkdf2_hmac(
            "sha256",
            clave.encode(),
            bytes.fromhex(sal_hex),
            310000
        )

        return hmac.compare_digest(
            calculado, bytes.fromhex(esperado)
        )

    except (ValueError, TypeError):
        return False


def buscar_usuario(usuario):
    with conectar() as db:
        fila = db.execute(
            """SELECT usuario, password_hash, chat_id, activo
               FROM usuarios WHERE usuario = ?""",
            (usuario,)
        ).fetchone()

        return dict(fila) if fila else None


def guardar_usuario(usuario, clave, chat_id):
    with conectar() as db:
        db.execute(
            """INSERT INTO usuarios
               (usuario, password_hash, chat_id)
               VALUES (?, ?, ?)""",
            (usuario, hash_password(clave), str(chat_id))
        )