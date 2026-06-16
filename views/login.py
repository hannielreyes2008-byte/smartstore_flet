import flet as ft
from datetime import datetime
import database as db
from views.recuperar import recuperar_view

def login_view(page: ft.Page, usuario_actual, go_to_menu):
    page.clean()
    page.update()
    page.bgcolor = "white"

    fondo = ft.Container(
        expand=True,
        image=ft.DecorationImage(
            src="fondo.png",
            fit="cover",
        ),
    )

    es_registro = False

    titulo = ft.Text("Iniciar Sesión", size=28, weight=ft.FontWeight.BOLD, color="#040D4A")
    correo_input = ft.TextField(label="Correo electrónico", width=300)
    password_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    nombre_input = ft.TextField(label="Nombre completo", width=300, visible=False)
    telefono_input = ft.TextField(label="Teléfono", width=300, visible=False)
    
    fecha_input = ft.TextField(
        label="Fecha de nacimiento (2009-05-15)",
        width=300,
        visible=False
    )

    btn_accion = ft.ElevatedButton(content=ft.Text("Ingresar"), width=300)
    btn_alternar = ft.TextButton(content=ft.Text("Crear cuenta nueva"))
    btn_recuperar = ft.TextButton(content=ft.Text("¿Olvidaste contraseña?"), on_click=lambda e: recuperar_view(page, go_to_menu))

    def mostrar_mensaje(texto):
        page.snack_bar = ft.SnackBar(ft.Text(texto), open=True)
        page.update()

    def calcular_edad(fecha_nac_str):
        try:
            fecha_nac = datetime.strptime(fecha_nac_str, "%Y-%m-%d")
            hoy = datetime.now()
            edad = hoy.year - fecha_nac.year
            if (hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day):
                edad -= 1
            return edad
        except:
            return -1

    def toggle(e):
        nonlocal es_registro
        es_registro = not es_registro
        titulo.value = "Crear Cuenta" if es_registro else "Iniciar Sesión"
        btn_accion.content = ft.Text("Registrarse" if es_registro else "Ingresar")
        btn_alternar.content = ft.Text("Volver a Iniciar Sesión" if es_registro else "Crear cuenta nueva")
        nombre_input.visible = es_registro
        telefono_input.visible = es_registro
        fecha_input.visible = es_registro
        page.update()

    def accion(e):
        if es_registro:
            nombre = nombre_input.value.strip()
            correo = correo_input.value.strip()
            telefono = telefono_input.value.strip()
            fecha_str = fecha_input.value.strip()
            password = password_input.value
            
            if not nombre or not correo or not telefono or not fecha_str or not password:
                mostrar_mensaje("Completa todos los campos")
                return
            
            edad = calcular_edad(fecha_str)
            if edad == -1:
                mostrar_mensaje("Formato de fecha inválido. Usa AAAA-MM-DD (ej: 2009-05-15)")
                return
            if edad < 17:
                mostrar_mensaje(f"Debes tener al menos 17 años. Tienes {edad} años.")
                return
            
            exitoso, mensaje = db.registrar_usuario(nombre, correo, telefono, fecha_str, password)
            mostrar_mensaje(mensaje)
            if exitoso:
                toggle(None)
        else:
            correo = correo_input.value.strip()
            password = password_input.value
            if not correo or not password:
                mostrar_mensaje("Ingresa correo y contraseña")
                return
            
            usuario = db.obtener_usuario(correo, password)
            if usuario:
                usuario_dict = {"id": usuario[0], "nombre": usuario[1], "correo": usuario[2]}
                go_to_menu(usuario_dict)
            else:
                mostrar_mensaje("Correo o contraseña incorrectos")

    btn_accion.on_click = accion
    btn_alternar.on_click = toggle

    form = ft.Column(
        [titulo, correo_input, password_input, nombre_input, telefono_input, fecha_input,
         btn_accion, btn_alternar, btn_recuperar],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        expand=True,
    )

    page.add(ft.Stack([fondo, form], expand=True))