import customtkinter as ctk
from interfaz.tema import COLORES, FUENTES, configurar_tema


class Aplicacion(ctk.CTk):

    def __init__(self):
        super().__init__()
        configurar_tema()

        self.title("Sistema de Biblioteca")
        self.geometry("1280x720")
        self.minsize(1000, 600)

        self.barra_lateral = ctk.CTkFrame(self, width=220, corner_radius=0,
                                           fg_color=COLORES["sidebar"])
        self.barra_lateral.pack(side="left", fill="y")
        self.barra_lateral.pack_propagate(False)

        lbl_logo = ctk.CTkLabel(self.barra_lateral, text="Biblioteca",
                                 font=("Segoe UI", 20, "bold"),
                                 text_color=COLORES["sidebar_texto"])
        lbl_logo.pack(pady=(25, 5))

        lbl_sub = ctk.CTkLabel(self.barra_lateral, text="Sistema de Gestion",
                                font=FUENTES["pequena"],
                                text_color=COLORES["texto_secundario"])
        lbl_sub.pack(pady=(0, 25))

        secciones = [
            ("panel", "Panel"),
            ("usuarios", "Usuarios"),
            ("materiales", "Materiales"),
            ("tipos", "Tipos de Material"),
            ("categorias", "Categorias"),
            ("prestamos", "Prestamos"),
            ("multas", "Multas"),
            ("auditoria", "Auditoria"),
            ("reportes", "Reportes"),
        ]

        self._botones_nav = {}
        for nombre, texto in secciones:
            btn = ctk.CTkButton(
                self.barra_lateral, text=f"  {texto}", font=FUENTES["boton"],
                fg_color="transparent", text_color=COLORES["sidebar_texto"],
                hover_color=COLORES["sidebar_hover"],
                anchor="w", height=40, corner_radius=8,
                command=lambda n=nombre: self.mostrar_vista(n))
            btn.pack(fill="x", padx=12, pady=2)
            self._botones_nav[nombre] = btn

        self.contenido = ctk.CTkFrame(self, fg_color=COLORES["fondo"],
                                       corner_radius=0)
        self.contenido.pack(side="right", fill="both", expand=True)

        self._vistas = {}
        self._vista_actual = None
        self.mostrar_vista("panel")

    def _crear_vista(self, nombre):
        from interfaz.vistas.panel_vista import PanelVista
        from interfaz.vistas.usuarios_vista import UsuariosVista
        from interfaz.vistas.materiales_vista import MaterialesVista
        from interfaz.vistas.tipos_material_vista import TiposMaterialVista
        from interfaz.vistas.categorias_vista import CategoriasVista
        from interfaz.vistas.prestamos_vista import PrestamosVista
        from interfaz.vistas.multas_vista import MultasVista
        from interfaz.vistas.auditoria_vista import AuditoriaVista
        from interfaz.vistas.reportes_vista import ReportesVista

        constructores = {
            "panel": PanelVista,
            "usuarios": UsuariosVista,
            "materiales": MaterialesVista,
            "tipos": TiposMaterialVista,
            "categorias": CategoriasVista,
            "prestamos": PrestamosVista,
            "multas": MultasVista,
            "auditoria": AuditoriaVista,
            "reportes": ReportesVista,
        }
        return constructores[nombre](self.contenido)

    def mostrar_vista(self, nombre):
        if self._vista_actual:
            self._vista_actual.pack_forget()

        for n, btn in self._botones_nav.items():
            if n == nombre:
                btn.configure(fg_color=COLORES["sidebar_activo"])
            else:
                btn.configure(fg_color="transparent")

        if nombre not in self._vistas:
            self._vistas[nombre] = self._crear_vista(nombre)

        self._vista_actual = self._vistas[nombre]
        self._vista_actual.pack(fill="both", expand=True)

        if hasattr(self._vista_actual, "refrescar"):
            self._vista_actual.refrescar()
