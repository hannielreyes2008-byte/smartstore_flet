#la data base la utilizamos para guardar los "DATOS"  de la app entre los cuales tenemos; usuarios, tienda,productos y reservas. 
#sin ella las funciones no funcionarian correctamente
import sqlite3
from datetime import datetime

DB_NAME = "smartstore.db"

def get_db_connection():
    return sqlite3.connect(DB_NAME)

def inicializar_bd():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabla usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            correo TEXT UNIQUE,
            telefono TEXT,
            fecha_nacimiento TEXT,
            contraseña TEXT
        )
    ''')

    # Tabla tiendas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tiendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            whatsapp TEXT,
            clave TEXT,
            pregunta TEXT,
            respuesta TEXT,
            tasa_cambio REAL
        )
    ''')

    # Tabla productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            marca TEXT,
            talla TEXT,
            precio_cordobas REAL,
            precio_dolares REAL,
            stock INTEGER
        )
    ''')

    # Tabla reservas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            producto_id INTEGER,
            cantidad INTEGER,
            fecha TEXT,
            estado TEXT
        )
    ''')

    # Insertar un usuario de prueba
    cursor.execute("SELECT * FROM usuarios WHERE correo = 'admin@smartstore.com'")
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO usuarios (nombre, correo, telefono, fecha_nacimiento, contraseña)
            VALUES (?,?,?,?,?)
        ''', ("Administrador", "admin@smartstore.com", "88888888", "2000-01-01", "admin123"))

    conn.commit()
    conn.close()
    print("Base de datos local inicializada")

def obtener_usuario(correo, contraseña):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, correo FROM usuarios WHERE correo = ? AND contraseña = ?", (correo, contraseña))
    user = cursor.fetchone()
    conn.close()
    return user

def registrar_usuario(nombre, correo, telefono, fecha_nac, contraseña):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO usuarios (nombre, correo, telefono, fecha_nacimiento, contraseña)
            VALUES (?,?,?,?,?)
        ''', (nombre, correo, telefono, fecha_nac, contraseña))
        conn.commit()
        return True, "Usuario registrado"
    except:
        return False, "Error al registrar"
    finally:
        conn.close()

def obtener_tienda():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, whatsapp, clave, pregunta, respuesta, tasa_cambio FROM tiendas LIMIT 1")
    tienda = cursor.fetchone()
    conn.close()
    return tienda

def guardar_tienda(nombre, whatsapp, clave, pregunta, respuesta, tasa_cambio):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tiendas")
    cursor.execute('''
        INSERT INTO tiendas (nombre, whatsapp, clave, pregunta, respuesta, tasa_cambio)
        VALUES (?,?,?,?,?,?)
    ''', (nombre, whatsapp, clave, pregunta, respuesta, tasa_cambio))
    conn.commit()
    conn.close()

def registrar_producto(nombre, marca, talla, precio_cordobas, precio_dolares, stock):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO productos (nombre, marca, talla, precio_cordobas, precio_dolares, stock)
        VALUES (?,?,?,?,?,?)
    ''', (nombre, marca, talla, precio_cordobas, precio_dolares, stock))
    conn.commit()
    conn.close()

def obtener_productos():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, marca, talla, precio_cordobas, precio_dolares, stock FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

def obtener_productos_por_nombre(nombre_filtro):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, marca, talla, precio_cordobas, precio_dolares, stock FROM productos WHERE nombre LIKE ?", (f"%{nombre_filtro}%",))
    productos = cursor.fetchall()
    conn.close()
    return productos

def obtener_stock_total():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(stock) FROM productos")
    total = cursor.fetchone()[0] or 0
    conn.close()
    return total

def agregar_reserva(usuario_id, producto_id, cantidad):
    conn = get_db_connection()
    cursor = conn.cursor()
    fecha = str(datetime.now())
    cursor.execute('''
        INSERT INTO reservas (usuario_id, producto_id, cantidad, fecha, estado)
        VALUES (?,?,?,?,?)
    ''', (usuario_id, producto_id, cantidad, fecha, "Reservado"))
    conn.commit()
    conn.close()

def obtener_reservas_usuario(usuario_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT r.id, p.nombre, r.cantidad, p.precio_cordobas, p.precio_dolares, r.estado
        FROM reservas r
        JOIN productos p ON r.producto_id = p.id
        WHERE r.usuario_id = ?
    ''', (usuario_id,))
    reservas = cursor.fetchall()
    conn.close()
    return reservas

def eliminar_reserva(reserva_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reservas WHERE id = ?", (reserva_id,))
    conn.commit()
    conn.close()

def confirmar_reserva(reserva_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE reservas SET estado = 'Confirmado' WHERE id = ?", (reserva_id,))
    conn.commit()
    conn.close()

def verificar_correo_existe(correo):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE correo = ?", (correo,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

def actualizar_contraseña_por_correo(correo, nueva_contraseña):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET contraseña = ? WHERE correo = ?", (nueva_contraseña, correo))
    conn.commit()
    actualizado = cursor.rowcount > 0
    conn.close()
    return actualizado

def obtener_contraseña_por_correo(correo):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT contraseña FROM usuarios WHERE correo = ?", (correo,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None