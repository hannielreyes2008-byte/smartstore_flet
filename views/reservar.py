import flet as ft
import database as db

def reservar_view(page: ft.Page, usuario, producto_id, producto_nombre, producto_stock, go_back):
    page.clean()
    page.bgcolor = "white"

    fondo = ft.Container(
        expand=True,
        image=ft.DecorationImage(src="fondo.png", fit="cover"),
    )

    cantidad_field = ft.TextField(label="¿Cuántos deseas reservar?", value="1", width=300)
    resultado_texto = ft.Text("", color="green")

    def confirmar_reserva(e):
        try:
            cant = int(cantidad_field.value)
            if 1 <= cant <= producto_stock:
                db.agregar_reserva(usuario['id'], producto_id, cant)
                resultado_texto.value = f"✅ {cant} x '{producto_nombre}' reservado correctamente"
                resultado_texto.color = "green"
                page.update()
            else:
                resultado_texto.value = f"Cantidad inválida. Debe ser entre 1 y {producto_stock}"
                resultado_texto.color = "red"
                page.update()
        except:
            resultado_texto.value = "Cantidad inválida"
            resultado_texto.color = "red"
            page.update()

    content = ft.Container(
        content=ft.Column(
            [
                ft.Text("Realizar Reserva", size=28, weight=ft.FontWeight.BOLD, color="#040D4A"),
                ft.Text(f"Producto: {producto_nombre}", size=18, weight=ft.FontWeight.BOLD),
                ft.Text(f"Stock disponible: {producto_stock}", size=14),
                cantidad_field,
                ft.ElevatedButton("Confirmar Reserva", on_click=confirmar_reserva, bgcolor="#EFA520"),
                resultado_texto,
                ft.ElevatedButton("Volver a Buscar", on_click=lambda e: go_back()),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            expand=True,
        ),
        expand=True,
    )

    page.add(ft.Stack([fondo, content], expand=True))