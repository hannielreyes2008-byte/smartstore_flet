import flet as ft
import database as db
import sqlite3

def perfil_view(page: ft.Page, usuario, go_back, logout):
    page.clean()
    page.bgcolor = "white"

    fondo = ft.Container(
        expand=True,
        image=ft.DecorationImage(src="fondo.png", fit="cover"),
    )

    nueva_pass = ft.TextField(label="Nueva contrasena", password=True, width=300)
    confirm_pass = ft.TextField(label="Confirmar contrasena", password=True, width=300)

    def cambiar_pass(e):
        if nueva_pass.value and nueva_pass.value == confirm_pass.value:
            conn = sqlite3.connect("smartstore.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET contraseña = ? WHERE id = ?", (nueva_pass.value, usuario['id']))
            conn.commit()
            conn.close()
            page.snack_bar = ft.SnackBar(ft.Text("Contrasena cambiada"))
            page.snack_bar.open = True
            nueva_pass.value = ""
            confirm_pass.value = ""
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Las contrasenas no coinciden"))
            page.snack_bar.open = True
            page.update()

    content = ft.Container(
        content=ft.Column(
            [
                ft.Text("Mi Perfil", size=32, weight=ft.FontWeight.BOLD, color="#040D4A"),
                ft.Text(f"Nombre: {usuario['nombre']}", size=18),
                ft.Text(f"Correo: {usuario['correo']}", size=18),
                ft.Text("Cambiar contrasena", size=20, weight=ft.FontWeight.BOLD),
                nueva_pass, confirm_pass,
                ft.ElevatedButton("Actualizar contrasena", on_click=cambiar_pass),
                ft.ElevatedButton("Volver al Menu", on_click=lambda e: go_back(usuario)),
                ft.ElevatedButton("Cerrar Sesion", on_click=lambda e: logout(), bgcolor=ft.Colors.RED_400),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            expand=True,
        ),
        expand=True,
    )

    page.add(ft.Stack([fondo, content], expand=True))