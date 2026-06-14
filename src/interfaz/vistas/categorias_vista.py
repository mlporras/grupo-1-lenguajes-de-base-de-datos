import customtkinter as ctk
from tkinter import messagebox
from interfaz.tema import COLORES, FUENTES
from interfaz.componentes import TablaEstilizada, DialogoFormulario
from servicios import categorias_servicio

COLUMNAS = [
    ("id", "ID", 60),
    ("nombre", "Nombre", 220),
    ("descripcion", "Descripcion", 300),
    ("estado", "Estado", 70),
]

CAMPOS = [
    {"nombre": "nombre", "etiqueta": "Nombre", "tipo": "texto", "requerido": True},
    {"nombre": "descripcion", "etiqueta": "Descripcion", "tipo": "texto"},
]


class CategoriasVista(ctk.CTkFrame):

    def __init__(self, maestro):
        super().__init__(maestro, fg_color=COLORES["fondo"])

        cab = ctk.CTkFrame(self, fg_color="transparent")
        cab.pack(fill="x", padx=30, pady=(25, 15))

        ctk.CTkLabel(cab, text="Categorias", font=FUENTES["titulo"],
                     text_color=COLORES["texto"]).pack(side="left")

        ctk.CTkButton(cab, text="Refrescar", width=100,
                      command=self.refrescar).pack(side="right", padx=5)
        ctk.CTkButton(cab, text="Inactivar", width=100,
                      fg_color=COLORES["peligro"],
                      hover_color=COLORES["peligro_hover"],
                      command=self.inactivar).pack(side="right", padx=5)
        ctk.CTkButton(cab, text="Editar", width=100,
                      fg_color=COLORES["advertencia"],
                      command=self.editar).pack(side="right", padx=5)
        ctk.CTkButton(cab, text="Crear", width=100,
                      fg_color=COLORES["exito"],
                      hover_color=COLORES["exito_hover"],
                      command=self.crear).pack(side="right", padx=5)

        self.tabla = TablaEstilizada(self, COLUMNAS)
        self.tabla.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        self.tabla.vincular_doble_clic(self.editar)

    def refrescar(self):
        try:
            _, filas = categorias_servicio.listar_categorias()
            self.tabla.cargar_datos(filas)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)

    def crear(self):
        dlg = DialogoFormulario(self, "Crear Categoria", CAMPOS)
        if dlg.resultado:
            try:
                r = dlg.resultado
                categorias_servicio.crear_categoria(
                    r["nombre"], r["descripcion"])
                messagebox.showinfo("Exito", "Categoria creada.", parent=self)
                self.refrescar()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self)

    def editar(self):
        sel = self.tabla.obtener_seleccion()
        if not sel:
            messagebox.showwarning("Aviso", "Seleccione una categoria.",
                                   parent=self)
            return
        valores = {"nombre": sel[1], "descripcion": sel[2]}
        dlg = DialogoFormulario(self, "Editar Categoria", CAMPOS, valores)
        if dlg.resultado:
            try:
                r = dlg.resultado
                categorias_servicio.actualizar_categoria(
                    int(sel[0]), r["nombre"], r["descripcion"])
                messagebox.showinfo("Exito", "Categoria actualizada.",
                                    parent=self)
                self.refrescar()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self)

    def inactivar(self):
        sel = self.tabla.obtener_seleccion()
        if not sel:
            messagebox.showwarning("Aviso", "Seleccione una categoria.",
                                   parent=self)
            return
        if messagebox.askyesno("Confirmar",
                               f"Inactivar categoria '{sel[1]}'?",
                               parent=self):
            try:
                categorias_servicio.inactivar_categoria(int(sel[0]))
                messagebox.showinfo("Exito", "Categoria inactivada.",
                                    parent=self)
                self.refrescar()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self)
