import flet as ft
import database as db

def carrito_view(page: ft.Page, usuario, go_back):
    page.clean()
    page.bgcolor = "white"

    fondo = ft.Container(
        expand=True,
        image=ft.DecorationImage(src="fondo.png", fit="cover"),
    )

    lista = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, height=400)
    total_text = ft.Text("Total: C$0.00 / $0.00", weight=ft.FontWeight.BOLD)

    def cargar():
        lista.controls.clear()
        reservas = db.obtener_reservas_usuario(usuario['id'])
        total_c = 0.0
        total_d = 0.0
        for r in reservas:
            rid, nom, cant, pc, pd, estado = r
            subtotal_c = pc * cant
            subtotal_d = pd * cant
            if estado == "Reservado":
                total_c += subtotal_c
                total_d += subtotal_d
            card = ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"{nom} x{cant}", weight=ft.FontWeight.BOLD),
                        ft.Text(f"C${pc:.2f} c/u = C${subtotal_c:.2f} / ${subtotal_d:.2f}"),
                        ft.Text(f"Estado: {estado}"),
                        ft.Row(
                            [
                                ft.ElevatedButton("Confirmar", on_click=lambda e, rid=rid: confirmar(rid)) if estado == "Reservado" else ft.Container(),
                                ft.ElevatedButton("Cancelar", on_click=lambda e, rid=rid: cancelar(rid), bgcolor=ft.Colors.RED_400) if estado == "Reservado" else ft.Container(),
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
            lista.controls.append(card)
        total_text.value = f"Total: C${total_c:.2f} / ${total_d:.2f}"
        page.update()

    def confirmar(rid):
        db.confirmar_reserva(rid)
        cargar()

    def cancelar(rid):
        db.eliminar_reserva(rid)
        cargar()

    def confirmar_todo(e):
        reservas = db.obtener_reservas_usuario(usuario['id'])
        for r in reservas:
            if r[5] == "Reservado":
                db.confirmar_reserva(r[0])
        cargar()

    content = ft.Container(
        content=ft.Column(
            [
                ft.Text("Mis Reservas", size=28, weight=ft.FontWeight.BOLD, color="#040D4A"),
                lista,
                total_text,
                ft.ElevatedButton("Confirmar Reserva", on_click=confirmar_todo),
                ft.ElevatedButton("Volver al Menu", on_click=lambda e: go_back(usuario)),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            expand=True,
        ),
        expand=True,
    )

    cargar()
    page.add(ft.Stack([fondo, content], expand=True))