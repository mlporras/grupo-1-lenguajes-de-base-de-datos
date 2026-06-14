import customtkinter as ctk
from tkinter import messagebox
from interfaz.tema import COLORES, FUENTES
from interfaz.componentes import TablaEstilizada, DialogoFormulario
from servicios import tipos_material_servicio

COLUMNAS = [
    ("id", "ID", 60),
    ("nombre", "Nombre", 200),
    ("descripcion", "Descripcion", 300),
    ("estado", "Estado", 70),
]

CAMPOS = [
    {"nombre": "nombre", "etiqueta": "Nombre", "tipo": "texto", "requerido": True},
    {"nombre": "descripcion", "etiqueta": "Descripcion", "tipo": "texto"},
]


class TiposMaterialVista(ctk.CTkFrame):

    def __init__(self, maestro):
        super().__init__(maestro, fg_color=COLORES["fondo"])

        cab = ctk.CTkFrame(self, fg_color="transparent")
        cab.pack(fill="x", padx=30, pady=(25, 15))

        ctk.CTkLabel(cab, text="Tipos de Material", font=FUENTES["titulo"],
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
            _, filas = tipos_material_servicio.listar_tipos_material()
            self.tabla.cargar_datos(filas)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)

    def crear(self):
        dlg = DialogoFormulario(self, "Crear Tipo de Material", CAMPOS)
        if dlg.resultado:
            try:
                r = dlg.resultado
                tipos_material_servicio.crear_tipo_material(
                    r["nombre"], r["descripcion"])
                messagebox.showinfo("Exito", "Tipo creado.", parent=self)
                self.refrescar()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self)

    def editar(self):
        sel = self.tabla.obtener_seleccion()
        if not sel:
            messagebox.showwarning("Aviso", "Seleccione un tipo.",
                                   parent=self)
            return
        valores = {"nombre": sel[1], "descripcion": sel[2]}
        dlg = DialogoFormulario(self, "Editar Tipo de Material", CAMPOS,
                                valores)
        if dlg.resultado:
            try:
                r = dlg.resultado
                tipos_material_servicio.actualizar_tipo_material(
                    int(sel[0]), r["nombre"], r["descripcion"])
                messagebox.showinfo("Exito", "Tipo actualizado.", parent=self)
                self.refrescar()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self)

    def inactivar(self):
        sel = self.tabla.obtener_seleccion()
        if not sel:
            messagebox.showwarning("Aviso", "Seleccione un tipo.",
                                   parent=self)
            return
        if messagebox.askyesno("Confirmar",
                               f"Inactivar tipo '{sel[1]}'?", parent=self):
            try:
                tipos_material_servicio.inactivar_tipo_material(int(sel[0]))
                messagebox.showinfo("Exito", "Tipo inactivado.", parent=self)
                self.refrescar()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self)
