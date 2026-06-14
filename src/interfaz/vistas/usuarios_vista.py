import customtkinter as ctk
from tkinter import messagebox
from interfaz.tema import COLORES, FUENTES
from interfaz.componentes import TablaEstilizada, DialogoFormulario
from servicios import usuarios_servicio

COLUMNAS = [
    ("cedula", "Cedula", 120),
    ("nombre", "Nombre", 130),
    ("apellidos", "Apellidos", 170),
    ("correo", "Correo", 180),
    ("telefono", "Telefono", 110),
    ("fecha", "Registro", 100),
    ("estado", "Estado", 70),
]

CAMPOS_CREAR = [
    {"nombre": "cedula", "etiqueta": "Cedula", "tipo": "texto", "requerido": True},
    {"nombre": "nombre", "etiqueta": "Nombre", "tipo": "texto", "requerido": True},
    {"nombre": "apellidos", "etiqueta": "Apellidos", "tipo": "texto", "requerido": True},
    {"nombre": "correo", "etiqueta": "Correo", "tipo": "texto"},
    {"nombre": "telefono", "etiqueta": "Telefono", "tipo": "texto"},
]

CAMPOS_EDITAR = [c for c in CAMPOS_CREAR if c["nombre"] != "cedula"]


class UsuariosVista(ctk.CTkFrame):

    def __init__(self, maestro):
        super().__init__(maestro, fg_color=COLORES["fondo"])

        cab = ctk.CTkFrame(self, fg_color="transparent")
        cab.pack(fill="x", padx=30, pady=(25, 15))

        ctk.CTkLabel(cab, text="Gestion de Usuarios", font=FUENTES["titulo"],
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
            _, filas = usuarios_servicio.listar_usuarios()
            self.tabla.cargar_datos(filas)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)

    def crear(self):
        dlg = DialogoFormulario(self, "Crear Usuario", CAMPOS_CREAR)
        if dlg.resultado:
            try:
                r = dlg.resultado
                usuarios_servicio.crear_usuario(
                    r["cedula"], r["nombre"], r["apellidos"],
                    r["correo"], r["telefono"])
                messagebox.showinfo("Exito", "Usuario creado.", parent=self)
                self.refrescar()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self)

    def editar(self):
        sel = self.tabla.obtener_seleccion()
        if not sel:
            messagebox.showwarning("Aviso", "Seleccione un usuario.",
                                   parent=self)
            return
        valores = {"nombre": sel[1], "apellidos": sel[2],
                   "correo": sel[3], "telefono": sel[4]}
        dlg = DialogoFormulario(self, "Editar Usuario", CAMPOS_EDITAR, valores)
        if dlg.resultado:
            try:
                r = dlg.resultado
                usuarios_servicio.actualizar_usuario(
                    sel[0], r["nombre"], r["apellidos"],
                    r["correo"], r["telefono"])
                messagebox.showinfo("Exito", "Usuario actualizado.",
                                    parent=self)
                self.refrescar()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self)

    def inactivar(self):
        sel = self.tabla.obtener_seleccion()
        if not sel:
            messagebox.showwarning("Aviso", "Seleccione un usuario.",
                                   parent=self)
            return
        if messagebox.askyesno("Confirmar",
                               f"Inactivar usuario {sel[0]}?",
                               parent=self):
            try:
                usuarios_servicio.inactivar_usuario(sel[0])
                messagebox.showinfo("Exito", "Usuario inactivado.",
                                    parent=self)
                self.refrescar()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self)
