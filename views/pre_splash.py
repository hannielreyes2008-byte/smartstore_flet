import flet as ft
import threading
import time

def pre_splash_view(page: ft.Page, on_complete):
    page.clean()
    page.update()
    page.bgcolor = "#EF7620"

    progress = ft.ProgressBar(width=200, color="white", bgcolor="#EFA52088")

    content = ft.Column(
        [
            ft.Text("😉", size=80),
            ft.Text("SmartStore", size=32, weight=ft.FontWeight.BOLD, color="white"),
            ft.Container(height=20),
            progress,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
    )
    page.add(content)
    page.update()

    def desencadenar_cambio():
        for i in range(10):
            time.sleep(0.4)
            progress.value = (i + 1) / 10
            page.update()
        
        # Forzar actualización final antes de cambiar de pantalla
        time.sleep(0.2)
        page.update()
        on_complete()

    threading.Thread(target=desencadenar_cambio, daemon=True).start()