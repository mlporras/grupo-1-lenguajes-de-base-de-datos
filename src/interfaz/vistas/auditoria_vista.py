import customtkinter as ctk
from tkinter import messagebox, simpledialog
from interfaz.tema import COLORES, FUENTES
from interfaz.componentes import TablaEstilizada
from servicios import auditoria_servicio

COLUMNAS = [
    ("tabla", "Tabla", 110),
    ("operacion", "Operacion", 90),
    ("usuario_db", "Usuario DB", 110),
    ("fecha", "Fecha", 120),
    ("detalle", "Detalle", 320),
]


class AuditoriaVista(ctk.CTkFrame):

    def __init__(self, maestro):
        super().__init__(maestro, fg_color=COLORES["fondo"])

        cab = ctk.CTkFrame(self, fg_color="transparent")
        cab.pack(fill="x", padx=30, pady=(25, 10))

        ctk.CTkLabel(cab, text="Auditoria", font=FUENTES["titulo"],
                     text_color=COLORES["texto"]).pack(side="left")

        ctk.CTkButton(cab, text="Refrescar", width=100,
                      command=self.refrescar).pack(side="right", padx=5)
        ctk.CTkButton(cab, text="Purgar", width=100,
                      fg_color=COLORES["peligro"],
                      hover_color=COLORES["peligro_hover"],
                      command=self.purgar).pack(side="right", padx=5)

        filtro = ctk.CTkFrame(self, fg_color="transparent")
        filtro.pack(fill="x", padx=30, pady=(0, 5))

        ctk.CTkLabel(filtro, text="Tabla:",
                     font=FUENTES["normal"]).pack(side="left", padx=(0, 8))
        self.combo_tabla = ctk.CTkComboBox(
            filtro, values=["USUARIOS", "MATERIALES"], width=160,
            command=lambda _: self.refrescar())
        self.combo_tabla.set("USUARIOS")
        self.combo_tabla.pack(side="left")

        self.lbl_total = ctk.CTkLabel(filtro, text="",
                                       font=FUENTES["pequena"],
                                       text_color=COLORES["texto_secundario"])
        self.lbl_total.pack(side="left", padx=15)

        self.tabla = TablaEstilizada(self, COLUMNAS)
        self.tabla.pack(fill="both", expand=True, padx=30, pady=(5, 20))

    def refrescar(self):
        try:
            total, _, filas = auditoria_servicio.listar_cambios_tabla(
                self.combo_tabla.get())
            self.lbl_total.configure(text=f"{total} evento(s)")
            self.tabla.cargar_datos(filas)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)

    def purgar(self):
        dias = simpledialog.askinteger(
            "Purgar auditoria",
            "Eliminar registros con mas de cuantos dias?",
            parent=self, minvalue=1)
        if dias is None:
            return
        if messagebox.askyesno(
                "Confirmar",
                f"Borrar eventos anteriores a {dias} dia(s)?",
                parent=self):
            try:
                auditoria_servicio.purgar_auditoria(dias)
                messagebox.showinfo("Exito", "Auditoria purgada.",
                                    parent=self)
                self.refrescar()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self)
