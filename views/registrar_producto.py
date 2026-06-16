import flet as ft
import database as db

def registrar_producto_view(page: ft.Page, usuario, go_back):
    page.clean()
    page.bgcolor = "white"

    fondo = ft.Container(
        expand=True,
        image=ft.DecorationImage(src="fondo.png", fit="cover"),
    )

    modo_registrar = True

    # Modo registrar
    nombre_input_reg = ft.TextField(label="Nombre del producto", width=300)
    marca_input = ft.TextField(label="Marca (opcional)", width=300)
    talla_input = ft.TextField(label="Talla (opcional)", width=300)
    precio_input_reg = ft.TextField(label="Precio en C$", width=300)
    cantidad_input = ft.TextField(label="Cantidad disponible", width=300)

    # Modo calcular
    nombre_input_cal = ft.TextField(label="Nombre del producto", width=300, visible=False)
    precio_input_cal = ft.TextField(label="Precio C$", width=300, visible=False)
    cantidad_input_cal = ft.TextField(label="Cantidad", width=300, visible=False)

    resultado_texto = ft.Text("", color="green")
    total_c = 0.0
    total_d = 0.0
    total_acumulado = ft.Text("Total acumulado: C$0.00 / $0.00", weight=ft.FontWeight.BOLD, visible=False)

    tienda = db.obtener_tienda()
    tasa = tienda[6] if tienda else 36.5
    tasa_texto = ft.Text(f"Tasa de cambio actual: C${tasa} = $1", size=12, color="#555555")

    def cambiar_modo(e):
        nonlocal modo_registrar, total_c, total_d
        modo_registrar = not modo_registrar

        if modo_registrar:
            btn_modo.text = "Registrar Producto"
            btn_alternativo.text = "Cambiar a Modo Calcular"

            nombre_input_reg.visible = True
            marca_input.visible = True
            talla_input.visible = True
            precio_input_reg.visible = True
            cantidad_input.visible = True

            nombre_input_cal.visible = False
            precio_input_cal.visible = False
            cantidad_input_cal.visible = False
            total_acumulado.visible = False

            resultado_texto.value = ""
            page.update()
        else:
            btn_modo.text = "Calcular"
            btn_alternativo.text = "Cambiar a Modo Registrar"

            nombre_input_reg.visible = False
            marca_input.visible = False
            talla_input.visible = False
            precio_input_reg.visible = False
            cantidad_input.visible = False

            nombre_input_cal.visible = True
            precio_input_cal.visible = True
            cantidad_input_cal.visible = True
            total_acumulado.visible = True

            total_c = 0.0
            total_d = 0.0
            total_acumulado.value = "Total acumulado: C$0.00 / $0.00"
            resultado_texto.value = ""
            page.update()

    def accion_principal(e):
        nonlocal total_c, total_d

        if modo_registrar:
            nombre = nombre_input_reg.value.strip()
            if not nombre:
                resultado_texto.value = "Ingrese el nombre del producto"
                resultado_texto.color = "red"
                page.update()
                return

            try:
                precio = float(precio_input_reg.value)
                cantidad = int(cantidad_input.value)
            except:
                resultado_texto.value = "Precio y cantidad deben ser números válidos"
                resultado_texto.color = "red"
                page.update()
                return

            tasa_actual = tienda[6] if tienda else 36.5
            precio_dolares = round(precio / tasa_actual, 2)
            
            # Debug: imprime en terminal
            print(f"Registrando: {nombre}, Precio C${precio}, Precio ${precio_dolares}, Cantidad {cantidad}")

            marca = marca_input.value.strip() if marca_input.value else ""
            talla = talla_input.value.strip() if talla_input.value else ""

            db.registrar_producto(nombre, marca, talla, precio, precio_dolares, cantidad)

            resultado_texto.value = f"Producto '{nombre}' registrado correctamente (C${precio:.2f} / ${precio_dolares:.2f})"
            resultado_texto.color = "green"

            nombre_input_reg.value = ""
            marca_input.value = ""
            talla_input.value = ""
            precio_input_reg.value = ""
            cantidad_input.value = ""
            page.update()
        else:
            try:
                nombre = nombre_input_cal.value.strip()
                precio = float(precio_input_cal.value)
                cantidad = int(cantidad_input_cal.value)

                if not nombre:
                    resultado_texto.value = "Ingrese el nombre"
                    resultado_texto.color = "red"
                    page.update()
                    return

                tasa_actual = tienda[6] if tienda else 36.5
                total_c_producto = precio * cantidad
                total_d_producto = total_c_producto / tasa_actual
                total_c += total_c_producto
                total_d += total_d_producto

                resultado_texto.value = f"{nombre}: C${total_c_producto:.2f} / ${total_d_producto:.2f}"
                resultado_texto.color = "green"
                total_acumulado.value = f"Total acumulado: C${total_c:.2f} / ${total_d:.2f}"

                nombre_input_cal.value = ""
                precio_input_cal.value = ""
                cantidad_input_cal.value = ""
                page.update()
            except:
                resultado_texto.value = "Error en los datos"
                resultado_texto.color = "red"
                page.update()

    btn_modo = ft.ElevatedButton("Registrar Producto", on_click=accion_principal, bgcolor="#EFA520")
    btn_alternativo = ft.TextButton("Cambiar a Modo Calcular", on_click=cambiar_modo)

    form = ft.Container(
        content=ft.Column(
            [
                ft.Text("Registrar Producto", size=28, weight=ft.FontWeight.BOLD, color="#040D4A"),
                tasa_texto,
                nombre_input_reg,
                marca_input,
                talla_input,
                precio_input_reg,
                cantidad_input,
                nombre_input_cal,
                precio_input_cal,
                cantidad_input_cal,
                total_acumulado,
                btn_modo,
                resultado_texto,
                btn_alternativo,
                ft.ElevatedButton("Volver al Menu", on_click=lambda e: go_back(usuario)),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            expand=True,
        ),
        expand=True,
    )

    page.add(ft.Stack([fondo, form], expand=True))