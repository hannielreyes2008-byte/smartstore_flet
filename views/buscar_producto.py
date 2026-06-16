import flet as ft
import database as db
import webbrowser
from views.reservar import reservar_view

def buscar_producto_view(page: ft.Page, usuario, go_back):
    page.clean()
    page.bgcolor = "white"

    fondo = ft.Container(
        expand=True,
        image=ft.DecorationImage(src="fondo.png", fit="cover"),
    )

    tienda = db.obtener_tienda()
    nombre_tienda = tienda[1] if tienda else "Sin tienda"
    whatsapp = tienda[2] if tienda else None

    buscar_entry = ft.TextField(label="Buscar por nombre", width=200)
    resultados = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, height=400)

    def buscar(e):
        resultados.controls.clear()
        busqueda = buscar_entry.value.strip()
        
        if not busqueda:
            resultados.controls.append(ft.Text("Escribe un nombre para buscar"))
            page.update()
            return
            
        productos = db.obtener_productos_por_nombre(busqueda)
        
        if not productos or len(productos) == 0:
            resultados.controls.append(ft.Text(f"No se encontraron productos con '{busqueda}'"))
            page.update()
            return
        
        for p in productos:
            try:
                id_producto = p[0]
                nombre = p[1]
                precio_c = float(p[4]) if p[4] else 0
                precio_d = float(p[5]) if p[5] else 0
                cantidad = int(p[6]) if p[6] else 0
                
                card = ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(nombre, weight=ft.FontWeight.BOLD),
                            ft.Text(f"C${precio_c:.2f} / ${precio_d:.2f}"),
                            ft.Text(f"Cantidad disponible: {cantidad}"),
                            ft.Row(
                                [
                                    ft.ElevatedButton("Reservar", on_click=lambda e: reservar_view(page, usuario, id_producto, nombre, cantidad, lambda: buscar_producto_view(page, usuario, go_back))),
                                    ft.ElevatedButton("WhatsApp", on_click=lambda e: abrir_whatsapp()) if whatsapp else ft.Container(),
                                ],
                                spacing=10,
                            ),
                        ],
                        spacing=5,
                    ),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=15,
                    padding=10,
                )
                resultados.controls.append(card)
            except Exception as error:
                resultados.controls.append(ft.Text(f"Error: {error}"))
        
        page.update()

    def abrir_whatsapp():
        if whatsapp:
            numero = whatsapp.strip()
            if not numero.startswith("+"):
                numero = "+" + numero
            webbrowser.open(f"https://wa.me/{numero}")

    content = ft.Container(
        content=ft.Column(
            [
                ft.Text(f"Buscar Productos - {nombre_tienda}", size=24, weight=ft.FontWeight.BOLD, color="#040D4A"),
                ft.Row([buscar_entry, ft.ElevatedButton("Buscar", on_click=buscar)]),
                resultados,
                ft.ElevatedButton("Volver al Menu", on_click=lambda e: go_back(usuario)),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            expand=True,
        ),
        expand=True,
    )

    page.add(ft.Stack([fondo, content], expand=True))