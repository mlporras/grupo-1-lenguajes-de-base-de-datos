import customtkinter as ctk
from interfaz.tema import COLORES, FUENTES
from interfaz.componentes import Tarjeta
from conexion_bd import probar_conexion


class PanelVista(ctk.CTkFrame):

    def __init__(self, maestro):
        super().__init__(maestro, fg_color=COLORES["fondo"])

        ctk.CTkLabel(self, text="Panel Principal", font=FUENTES["titulo"],
                     text_color=COLORES["texto"]).pack(anchor="w", padx=30,
                                                       pady=(25, 5))

        self.lbl_conexion = ctk.CTkLabel(self, text="", font=FUENTES["pequena"])
        self.lbl_conexion.pack(anchor="w", padx=30, pady=(0, 20))

        marco = ctk.CTkFrame(self, fg_color="transparent")
        marco.pack(fill="x", padx=30, pady=10)

        self.t_usuarios = Tarjeta(marco, "Usuarios Activos",
                                   color=COLORES["primario"])
        self.t_usuarios.pack(side="left", padx=(0, 15), fill="x", expand=True)

        self.t_materiales = Tarjeta(marco, "Materiales Disponibles",
                                     color=COLORES["exito"])
        self.t_materiales.pack(side="left", padx=(0, 15), fill="x", expand=True)

        self.t_prestamos = Tarjeta(marco, "Prestamos Activos",
                                    color=COLORES["advertencia"])
        self.t_prestamos.pack(side="left", padx=(0, 15), fill="x", expand=True)

        self.t_vencidos = Tarjeta(marco, "Prestamos Vencidos",
                                   color=COLORES["peligro"])
        self.t_vencidos.pack(side="left", fill="x", expand=True)

        info = ctk.CTkFrame(self, fg_color=COLORES["tarjeta"], corner_radius=12,
                            border_width=1, border_color=COLORES["borde"])
        info.pack(fill="x", padx=30, pady=(25, 10))

        ctk.CTkLabel(info, text="Acerca del Sistema", font=FUENTES["subtitulo"],
                     text_color=COLORES["texto"]).pack(anchor="w", padx=20,
                                                        pady=(15, 5))
        ctk.CTkLabel(
            info, font=FUENTES["normal"], text_color=COLORES["texto_secundario"],
            text="Sistema de gestion de biblioteca desarrollado con Python y Oracle.\n"
                 "Todo el CRUD se ejecuta mediante paquetes PL/SQL.\n\n"
                 "Integrantes:\n"
                 "  Fabio Esteban Dondi Umana\n"
                 "  Jose Paulo Monge Alfaro\n"
                 "  Marco Leon Porras Gonzalez",
            justify="left"
        ).pack(anchor="w", padx=20, pady=(0, 15))

    def refrescar(self):
        ok, msg = probar_conexion()
        if ok:
            self.lbl_conexion.configure(text="Conectado a Oracle",
                                         text_color=COLORES["exito"])
            self._cargar_conteos()
        else:
            self.lbl_conexion.configure(text=f"Sin conexion: {msg}",
                                         text_color=COLORES["peligro"])
            for t in (self.t_usuarios, self.t_materiales,
                      self.t_prestamos, self.t_vencidos):
                t.actualizar("--")

    def _cargar_conteos(self):
        from servicios import reportes_servicio

        try:
            self.t_usuarios.actualizar(
                reportes_servicio.total_usuarios_activos())
        except Exception:
            self.t_usuarios.actualizar("--")

        try:
            self.t_materiales.actualizar(
                reportes_servicio.total_materiales_disponibles())
        except Exception:
            self.t_materiales.actualizar("--")

        try:
            self.t_prestamos.actualizar(
                reportes_servicio.total_prestamos_activos())
        except Exception:
            self.t_prestamos.actualizar("--")

        try:
            self.t_vencidos.actualizar(
                reportes_servicio.total_prestamos_vencidos())
        except Exception:
            self.t_vencidos.actualizar("--")
