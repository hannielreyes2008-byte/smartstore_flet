import flet as ft
import database as db

def crear_tienda_view(page: ft.Page, usuario, go_back):
    page.clean()
    page.bgcolor = "white"

    fondo = ft.Container(
        expand=True,
        image=ft.DecorationImage(src="fondo.png", fit="cover"),
    )

    nombre_input = ft.TextField(label="Nombre de la tienda", width=300)
    whatsapp_input = ft.TextField(label="WhatsApp (ej: 50588888888)", width=300)
    tasa_input = ft.TextField(label="Tasa de cambio", value="36.5", width=300)
    clave_input = ft.TextField(label="Contrasena para proteger la tienda", password=True, width=300)
    pregunta_input = ft.TextField(label="Pregunta de seguridad", width=300)
    respuesta_input = ft.TextField(label="Respuesta", width=300)

    nombre_prod_input = ft.TextField(label="Nombre del producto", width=300)
    marca_input = ft.TextField(label="Marca (opcional)", width=300)
    talla_input = ft.TextField(label="Talla (opcional)", width=300)
    precio_input = ft.TextField(label="Precio en C$", width=300)
    cantidad_input = ft.TextField(label="Cantidad", width=300)

    productos_layout = ft.Column(spacing=5)
    productos_temp = []

    def agregar_producto(e):
        nombre = nombre_prod_input.value
        if not nombre:
            page.snack_bar = ft.SnackBar(ft.Text("Ingrese nombre del producto"))
            page.snack_bar.open = True
            page.update()
            return
        try:
            precio = float(precio_input.value)
            cantidad = int(cantidad_input.value)
            tasa = float(tasa_input.value) if tasa_input.value else 36.5
        except:
            page.snack_bar = ft.SnackBar(ft.Text("Datos invalidos"))
            page.snack_bar.open = True
            page.update()
            return

        marca = marca_input.value
        talla = talla_input.value
        precio_d = precio / tasa

        productos_temp.append((nombre, marca, talla, precio, precio_d, cantidad))

        productos_layout.controls.append(
            ft.Container(
                content=ft.Text(f"{nombre} | C${precio:.2f} | x{cantidad}"),
                padding=5,
                bgcolor=ft.Colors.GREY_100,
                border_radius=10,
            )
        )
        nombre_prod_input.value = ""
        marca_input.value = ""
        talla_input.value = ""
        precio_input.value = ""
        cantidad_input.value = ""
        page.update()

    def guardar_tienda(e):
        nombre = nombre_input.value.strip()
        if not nombre:
            page.snack_bar = ft.SnackBar(ft.Text("Ingrese nombre de la tienda"))
            page.snack_bar.open = True
            page.update()
            return
        try:
            tasa = float(tasa_input.value) if tasa_input.value else 36.5
        except:
            page.snack_bar = ft.SnackBar(ft.Text("Tasa invalida"))
            page.snack_bar.open = True
            page.update()
            return

        db.guardar_tienda(nombre, whatsapp_input.value, clave_input.value, pregunta_input.value, respuesta_input.value, tasa)

        for prod in productos_temp:
            db.registrar_producto(prod[0], prod[1], prod[2], prod[3], prod[4], prod[5])

        page.snack_bar = ft.SnackBar(ft.Text("Tienda y productos guardados"))
        page.snack_bar.open = True
        page.update()
        go_back(usuario)

    form = ft.Container(
        content=ft.Column(
            [
                ft.Text("Crear Tienda", size=28, weight=ft.FontWeight.BOLD, color="#040D4A"),
                nombre_input, whatsapp_input, tasa_input,
                ft.Text("Seguridad de la tienda", weight=ft.FontWeight.BOLD),
                clave_input, pregunta_input, respuesta_input,
                ft.Text("Registrar productos", weight=ft.FontWeight.BOLD),
                nombre_prod_input, marca_input, talla_input, precio_input, cantidad_input,
                ft.ElevatedButton("Agregar Producto", on_click=agregar_producto),
                productos_layout,
                ft.ElevatedButton("Guardar Tienda", on_click=guardar_tienda, bgcolor=ft.Colors.ORANGE_400),
                ft.ElevatedButton("Volver al Menu", on_click=lambda e: go_back(usuario)),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
            height=550,
            expand=True,
        ),
        expand=True,
    )

    page.add(ft.Stack([fondo, form], expand=True))