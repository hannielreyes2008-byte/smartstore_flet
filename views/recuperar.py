import flet as ft
import database as db

def recuperar_view(page: ft.Page, go_to_menu):
    page.clean()
    page.bgcolor = "white"

    fondo = ft.Container(
        expand=True,
        image=ft.DecorationImage(src="fondo.png", fit="cover"),
    )

    correo_field = ft.TextField(label="Correo electrónico", width=300)
    resultado_texto = ft.Text("")
    
    def buscar_contraseña(e):
        correo = correo_field.value.strip()
        if not correo:
            resultado_texto.value = "Ingresa tu correo"
            resultado_texto.color = "red"
            page.update()
            return
        
        contraseña = db.obtener_contraseña_por_correo(correo)
        if contraseña:
            resultado_texto.value = f"Tu contraseña es: {contraseña}"
            resultado_texto.color = "green"
        else:
            resultado_texto.value = "No existe una cuenta con ese correo"
            resultado_texto.color = "red"
        page.update()

    def volver_login(e):
        from views.login import login_view
        login_view(page, None, go_to_menu)

    content = ft.Container(
        content=ft.Column(
            [
                ft.Text("Recuperar Contraseña", size=28, weight=ft.FontWeight.BOLD, color="#040D4A"),
                ft.Text("Ingresa tu correo y te mostraremos tu contraseña", size=14, color="#555555"),
                correo_field,
                ft.ElevatedButton("Buscar mi contraseña", on_click=buscar_contraseña),
                resultado_texto,
                ft.ElevatedButton("Volver al Login", on_click=volver_login),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            expand=True,
        ),
        expand=True,
    )

    page.add(ft.Stack([fondo, content], expand=True))