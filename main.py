import flet as ft
import threading
import time
from views.pre_splash import pre_splash_view
from views.splash import splash_view
from views.login import login_view
from views.menu import menu_view
from views.registrar_producto import registrar_producto_view
from views.buscar_producto import buscar_producto_view
from views.carrito import carrito_view
from views.crear_tienda import crear_tienda_view
from views.perfil import perfil_view
import database as db

def main(page: ft.Page):
    page.title = "SmartStore PyMES"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0
    page.expand = True

    db.inicializar_bd()
    usuario_actual = None

    def go_to_splash():
        splash_view(page, go_to_login)

    def go_to_login():
        login_view(page, usuario_actual, go_to_menu)

    def go_to_menu(usuario):
        nonlocal usuario_actual
        usuario_actual = usuario
        menu_view(page, usuario_actual, logout,
                  go_to_registrar_producto,
                  go_to_buscar_producto,
                  go_to_carrito,
                  go_to_crear_tienda,
                  go_to_perfil)

    def go_to_registrar_producto():
        registrar_producto_view(page, usuario_actual, go_to_menu)

    def go_to_buscar_producto():
        buscar_producto_view(page, usuario_actual, go_to_menu)

    def go_to_carrito():
        carrito_view(page, usuario_actual, go_to_menu)

    def go_to_crear_tienda():
        crear_tienda_view(page, usuario_actual, go_to_menu)

    def go_to_perfil():
        perfil_view(page, usuario_actual, go_to_menu, logout)

    def logout():
        nonlocal usuario_actual
        usuario_actual = None
        go_to_login()

    pre_splash_view(page, go_to_splash)
    page.update()
    
    # Forzar refresco después de 0.3 segundos
    def refrescar():
        time.sleep(0.3)
        page.update()
    threading.Thread(target=refrescar, daemon=True).start()

ft.app(target=main, assets_dir="assets")