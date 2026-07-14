import customtkinter as ctk
from tkinter import messagebox
from interfaz.tema import COLORES, FUENTES
from interfaz.componentes import TablaEstilizada
from servicios import reportes_servicio, categorias_servicio

COLUMNAS_DISP = [
    ("id", "ID", 50),
    ("titulo", "Titulo", 200),
    ("autor", "Autor", 140),
    ("isbn", "ISBN", 140),
    ("tipo", "Tipo", 110),
    ("categoria", "Categoria", 120),
]

COLUMNAS_VENC = [
    ("id", "ID", 50),
    ("cedula", "Cedula", 100),
    ("id_mat", "ID Mat.", 70),
    ("f_prest", "Prestamo", 100),
    ("f_esp", "Esperada", 100),
    ("usuario", "Usuario", 160),
    ("material", "Material", 180),
]

COLUMNAS_HIST = [
    ("id", "ID", 50),
    ("cedula", "Cedula", 100),
    ("usuario", "Usuario", 150),
    ("material", "Material", 160),
    ("f_prest", "Prestamo", 100),
    ("f_esp", "Esperada", 100),
    ("f_real", "Real", 100),
    ("estado", "Estado", 80),
]


class ReportesVista(ctk.CTkFrame):

    def __init__(self, maestro):
        super().__init__(maestro, fg_color=COLORES["fondo"])

        cab = ctk.CTkFrame(self, fg_color="transparent")
        cab.pack(fill="x", padx=30, pady=(25, 10))

        ctk.CTkLabel(cab, text="Reportes", font=FUENTES["titulo"],
                     text_color=COLORES["texto"]).pack(side="left")

        ctk.CTkButton(cab, text="Refrescar", width=100,
                      command=self.refrescar).pack(side="right", padx=5)

        self.lbl_totales = ctk.CTkLabel(
            self, text="", font=FUENTES["pequena"],
            text_color=COLORES["texto_secundario"])
        self.lbl_totales.pack(anchor="w", padx=30, pady=(0, 8))

        filtro = ctk.CTkFrame(self, fg_color="transparent")
        filtro.pack(fill="x", padx=30, pady=(0, 5))

        self.filtro = ctk.CTkSegmentedButton(
            filtro,
            values=["Disponibles", "Vencidos", "Por categoria",
                    "Historial usuario"],
            command=self._cambiar_reporte)
        self.filtro.set("Disponibles")
        self.filtro.pack(side="left")

        self.marco_extra = ctk.CTkFrame(filtro, fg_color="transparent")

        self.combo_cat = ctk.CTkComboBox(self.marco_extra, width=200,
                                          values=[])
        self.entrada_cedula = ctk.CTkEntry(
            self.marco_extra, width=160, placeholder_text="Cedula")
        self.btn_buscar = ctk.CTkButton(self.marco_extra, text="Buscar",
                                         width=80, command=self.refrescar)

        self._columnas_actuales = COLUMNAS_DISP
        self.tabla = TablaEstilizada(self, COLUMNAS_DISP)
        self.tabla.pack(fill="both", expand=True, padx=30, pady=(5, 20))

        self._cargar_categorias()

    def _cargar_categorias(self):
        try:
            _, filas = categorias_servicio.listar_categorias()
            opc = [f"{int(f[0])} - {f[1]}" for f in filas if f[3] == "A"]
            self.combo_cat.configure(values=opc or ["(sin categorias)"])
            if opc:
                self.combo_cat.set(opc[0])
        except Exception:
            self.combo_cat.configure(values=["(error)"])
            self.combo_cat.set("(error)")

    def _cambiar_reporte(self, _valor):
        self.marco_extra.pack_forget()
        self.combo_cat.pack_forget()
        self.entrada_cedula.pack_forget()
        self.btn_buscar.pack_forget()

        modo = self.filtro.get()
        if modo == "Por categoria":
            self.marco_extra.pack(side="left", padx=(15, 0))
            self.combo_cat.pack(side="left")
            self.btn_buscar.pack(side="left", padx=5)
        elif modo == "Historial usuario":
            self.marco_extra.pack(side="left", padx=(15, 0))
            self.entrada_cedula.pack(side="left")
            self.btn_buscar.pack(side="left", padx=5)

        self._recrear_tabla(modo)
        if modo in ("Disponibles", "Vencidos"):
            self.refrescar()

    def _recrear_tabla(self, modo):
        self.tabla.destroy()
        if modo == "Vencidos":
            cols = COLUMNAS_VENC
        elif modo == "Historial usuario":
            cols = COLUMNAS_HIST
        else:
            cols = COLUMNAS_DISP
        self._columnas_actuales = cols
        self.tabla = TablaEstilizada(self, cols)
        self.tabla.pack(fill="both", expand=True, padx=30, pady=(5, 20))

    def _actualizar_totales(self):
        try:
            inactivos = reportes_servicio.total_materiales_inactivos()
            devueltos = reportes_servicio.total_prestamos_devueltos()
            try:
                mas = reportes_servicio.material_mas_prestado()
            except Exception:
                mas = "-"
            self.lbl_totales.configure(
                text=(f"Materiales inactivos: {inactivos}  |  "
                      f"Prestamos devueltos: {devueltos}  |  "
                      f"Material mas prestado (ID): {mas}")
            )
        except Exception:
            self.lbl_totales.configure(text="")

    def refrescar(self):
        self._actualizar_totales()
        modo = self.filtro.get()
        try:
            if modo == "Disponibles":
                _, filas = reportes_servicio.listar_materiales_disponibles()
            elif modo == "Vencidos":
                _, filas = reportes_servicio.listar_prestamos_vencidos()
            elif modo == "Por categoria":
                valor = self.combo_cat.get()
                if not valor or valor.startswith("("):
                    messagebox.showwarning("Aviso", "Elija una categoria.",
                                           parent=self)
                    return
                id_cat = int(valor.split(" - ", 1)[0])
                _, filas = reportes_servicio.consultar_materiales_por_categoria(
                    id_cat)
            else:
                cedula = self.entrada_cedula.get().strip()
                if not cedula:
                    messagebox.showwarning("Aviso", "Ingrese la cedula.",
                                           parent=self)
                    return
                _, filas = reportes_servicio.consultar_historial_por_usuario(
                    cedula)
            self.tabla.cargar_datos(filas)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)
