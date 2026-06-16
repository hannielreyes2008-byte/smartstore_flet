import flet as ft

def splash_view(page: ft.Page, on_complete):
    page.clean()
    page.update()
    page.bgcolor = "white"

    fondo = ft.Image(
        src="bienvenida.png",
        fit="cover",
        expand=True
    )

    btn_avanzar = ft.ElevatedButton(
        content=ft.Text("→", size=20),
        bgcolor="#EFA520",
        color="white",
        on_click=lambda _: avanzar(),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )

    def avanzar():
        page.update()
        on_complete()

    capa_contenido = ft.Container(
        content=ft.Column(
            [btn_avanzar],
            alignment=ft.MainAxisAlignment.END,
            horizontal_alignment=ft.CrossAxisAlignment.END
        ),
        padding=30,
        expand=True
    )

    page.add(
        ft.Stack(
            [
                fondo,
                capa_contenido
            ],
            expand=True
        )
    )
    page.update()