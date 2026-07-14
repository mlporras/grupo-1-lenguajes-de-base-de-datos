import customtkinter as ctk
from tkinter import messagebox
from interfaz.tema import COLORES, FUENTES
from interfaz.componentes import TablaEstilizada
from servicios import multas_servicio

COLUMNAS = [
    ("id", "ID", 60),
    ("cedula", "Cedula", 110),
    ("nombre", "Nombre", 120),
    ("apellidos", "Apellidos", 150),
    ("monto", "Monto", 90),
    ("dias", "Dias atraso", 90),
]


class MultasVista(ctk.CTkFrame):

    def __init__(self, maestro):
        super().__init__(maestro, fg_color=COLORES["fondo"])

        cab = ctk.CTkFrame(self, fg_color="transparent")
        cab.pack(fill="x", padx=30, pady=(25, 15))

        ctk.CTkLabel(cab, text="Multas pendientes", font=FUENTES["titulo"],
                     text_color=COLORES["texto"]).pack(side="left")

        ctk.CTkButton(cab, text="Refrescar", width=100,
                      command=self.refrescar).pack(side="right", padx=5)
        ctk.CTkButton(cab, text="Generar automaticas", width=160,
                      fg_color=COLORES["advertencia"],
                      command=self.generar_automaticas).pack(side="right",
                                                             padx=5)
        ctk.CTkButton(cab, text="Pagar", width=100,
                      fg_color=COLORES["exito"],
                      hover_color=COLORES["exito_hover"],
                      command=self.pagar).pack(side="right", padx=5)

        self.tabla = TablaEstilizada(self, COLUMNAS)
        self.tabla.pack(fill="both", expand=True, padx=30, pady=(0, 20))

    def refrescar(self):
        try:
            _, filas = multas_servicio.listar_multas_pendientes()
            self.tabla.cargar_datos(filas)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)

    def pagar(self):
        sel = self.tabla.obtener_seleccion()
        if not sel:
            messagebox.showwarning("Aviso", "Seleccione una multa.",
                                   parent=self)
            return
        if messagebox.askyesno(
                "Confirmar",
                f"Marcar multa {sel[0]} como pagada?",
                parent=self):
            try:
                multas_servicio.pagar_multa(int(sel[0]))
                messagebox.showinfo("Exito", "Multa pagada.", parent=self)
                self.refrescar()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self)

    def generar_automaticas(self):
        if messagebox.askyesno(
                "Confirmar",
                "Generar multas para prestamos activos vencidos?",
                parent=self):
            try:
                multas_servicio.generar_multas_automaticas()
                messagebox.showinfo("Exito", "Proceso completado.",
                                    parent=self)
                self.refrescar()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self)
