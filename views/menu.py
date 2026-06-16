import flet as ft
import database as db

def menu_view(page: ft.Page, usuario, logout, go_to_registrar, go_to_buscar, go_to_carrito, go_to_tienda, go_to_perfil):
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

    productos = db.obtener_productos()
    total_productos = len(productos)
    stock_total = db.obtener_stock_total()

    contenido = ft.Column(
        [
            ft.Text(f"Bienvenido, {usuario['nombre']}", size=24, weight=ft.FontWeight.BOLD, color="#040D4A"),
            ft.Text("Gestiona tu negocio de forma inteligente", size=14, color="#555555"),
            ft.ElevatedButton("📦 Registrar Producto", on_click=lambda e: go_to_registrar(), expand=True),
            ft.ElevatedButton("🔍 Buscar Productos", on_click=lambda e: go_to_buscar(), expand=True),
            ft.ElevatedButton("🛒 Reservas y Carrito", on_click=lambda e: go_to_carrito(), expand=True),
            ft.ElevatedButton("🏪 Crear Tienda", on_click=lambda e: go_to_tienda(), expand=True),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"Total de productos: {total_productos}", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text("Estado del inventario", size=14, color="#555555"),
                        ft.Text(f"+ {stock_total}", size=40, weight=ft.FontWeight.BOLD, color="#EFA520"),
                    ],
                    spacing=5,
                ),
                bgcolor=ft.Colors.WHITE,
                border_radius=15,
                padding=15,
                expand=True,
            ),
            ft.Row(
                [
                    ft.TextButton("Mi Perfil", on_click=lambda e: go_to_perfil()),
                    ft.TextButton("Cerrar Sesión", on_click=lambda e: logout()),
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                expand=True,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
        expand=True,
    )

    page.add(ft.Stack([fondo, contenido], expand=True))