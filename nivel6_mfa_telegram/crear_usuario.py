import getpass
import sqlite3

from base_datos import iniciar_bd, guardar_usuario

iniciar_bd()

usuario = input("Nuevo usuario: ").strip()
clave = getpass.getpass("Contraseña: ")
chat_id = input("Chat ID de Telegram: ").strip()

if not usuario or not clave or not chat_id:
    print("Todos los campos son obligatorios.")

else:
    try:
        guardar_usuario(usuario, clave, chat_id)
        print("Usuario guardado correctamente en usuarios.db")

    except sqlite3.IntegrityError:
        print("Ese nombre de usuario ya existe.")