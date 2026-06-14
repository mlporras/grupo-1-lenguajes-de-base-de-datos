import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import customtkinter as ctk
from interfaz.tema import COLORES, FUENTES


class TablaEstilizada(ctk.CTkFrame):
    """Tabla de datos."""

    def __init__(self, maestro, columnas_def, **kwargs):
        super().__init__(maestro, fg_color="transparent", **kwargs)

        nombres = [c[0] for c in columnas_def]

        contenedor = ctk.CTkFrame(self, fg_color=COLORES["tarjeta"],
                                  corner_radius=8)
        contenedor.pack(fill="both", expand=True)

        self.arbol = ttk.Treeview(contenedor, columns=nombres,
                                  show="headings", selectmode="browse")

        for nombre, etiqueta, ancho in columnas_def:
            self.arbol.heading(nombre, text=etiqueta, anchor="w")
            self.arbol.column(nombre, width=ancho, minwidth=40, anchor="w")

        barra_v = ttk.Scrollbar(contenedor, orient="vertical",
                                command=self.arbol.yview)
        barra_h = ttk.Scrollbar(contenedor, orient="horizontal",
                                command=self.arbol.xview)
        self.arbol.configure(yscrollcommand=barra_v.set,
                             xscrollcommand=barra_h.set)

        self.arbol.grid(row=0, column=0, sticky="nsew")
        barra_v.grid(row=0, column=1, sticky="ns")
        barra_h.grid(row=1, column=0, sticky="ew")
        contenedor.grid_rowconfigure(0, weight=1)
        contenedor.grid_columnconfigure(0, weight=1)

        self.arbol.tag_configure("par", background=COLORES["tabla_par"])
        self.arbol.tag_configure("impar", background=COLORES["tabla_impar"])

    def cargar_datos(self, filas):
        for item in self.arbol.get_children():
            self.arbol.delete(item)
        for i, fila in enumerate(filas):
            valores = [self._formatear(v) for v in fila]
            tag = "par" if i % 2 == 0 else "impar"
            self.arbol.insert("", "end", values=valores, tags=(tag,))

    def _formatear(self, valor):
        if valor is None:
            return ""
        if isinstance(valor, (datetime, date)):
            return valor.strftime("%d/%m/%Y")
        return str(valor)

    def obtener_seleccion(self):
        sel = self.arbol.selection()
        if not sel:
            return None
        return self.arbol.item(sel[0], "values")

    def vincular_doble_clic(self, callback):
        self.arbol.bind("<Double-1>", lambda _: callback())


class DialogoFormulario(ctk.CTkToplevel):
    """Dialogo de formulario."""

    def __init__(self, maestro, titulo, campos, valores=None):
        super().__init__(maestro)
        self.title(titulo)
        self.resizable(False, False)
        self.resultado = None
        self._campos = campos
        self._entradas = {}

        self.transient(maestro.winfo_toplevel())
        self.grab_set()

        marco = ctk.CTkFrame(self, fg_color="transparent")
        marco.pack(padx=20, pady=20, fill="both", expand=True)

        for i, campo in enumerate(campos):
            lbl = ctk.CTkLabel(marco, text=campo["etiqueta"] + ":",
                               font=FUENTES["normal"], anchor="e")
            lbl.grid(row=i, column=0, padx=(0, 10), pady=6, sticky="e")

            ancho = campo.get("ancho", 280)
            tipo = campo.get("tipo", "texto")

            if tipo == "combo":
                textos = [op[1] for op in campo.get("opciones", [])]
                entrada = ctk.CTkComboBox(marco, values=textos, width=ancho,
                                          state="readonly")
                if valores and campo["nombre"] in valores:
                    for vl, tx in campo["opciones"]:
                        if str(vl) == str(valores[campo["nombre"]]):
                            entrada.set(tx)
                            break
                elif textos:
                    entrada.set(textos[0])
            elif tipo == "fecha":
                try:
                    from tkcalendar import DateEntry
                    entrada = DateEntry(marco, width=18,
                                       date_pattern="dd/MM/yyyy",
                                       font=FUENTES["normal"])
                    if valores and campo["nombre"] in valores:
                        try:
                            entrada.set_date(valores[campo["nombre"]])
                        except Exception:
                            pass
                except ImportError:
                    entrada = ctk.CTkEntry(marco, width=ancho,
                                           placeholder_text="DD/MM/AAAA")
                    if valores and campo["nombre"] in valores:
                        entrada.insert(0, str(valores[campo["nombre"]]))
            else:
                entrada = ctk.CTkEntry(marco, width=ancho)
                if valores and campo["nombre"] in valores:
                    entrada.insert(0, str(valores[campo["nombre"]]))

            entrada.grid(row=i, column=1, pady=6, sticky="w")
            self._entradas[campo["nombre"]] = (campo, entrada)

        marco_btns = ctk.CTkFrame(marco, fg_color="transparent")
        marco_btns.grid(row=len(campos), column=0, columnspan=2, pady=(15, 0))

        ctk.CTkButton(marco_btns, text="Aceptar", width=120,
                      command=self._aceptar).pack(side="left", padx=5)
        ctk.CTkButton(marco_btns, text="Cancelar", width=120,
                      fg_color=COLORES["texto_secundario"],
                      command=self.destroy).pack(side="left", padx=5)

        self.after(100, lambda: self.focus_force())
        self.wait_window()

    def _aceptar(self):
        resultado = {}
        for nombre, (campo, entrada) in self._entradas.items():
            tipo = campo.get("tipo", "texto")
            if tipo == "combo":
                texto = entrada.get()
                valor = None
                for vl, tx in campo.get("opciones", []):
                    if tx == texto:
                        valor = vl
                        break
                resultado[nombre] = valor
            elif tipo == "fecha":
                if hasattr(entrada, "get_date"):
                    resultado[nombre] = entrada.get_date()
                else:
                    resultado[nombre] = entrada.get().strip()
            else:
                resultado[nombre] = entrada.get().strip()

            if campo.get("requerido") and not resultado.get(nombre):
                messagebox.showwarning(
                    "Campo requerido",
                    f"El campo '{campo['etiqueta']}' es obligatorio.",
                    parent=self)
                return

        self.resultado = resultado
        self.destroy()


class Tarjeta(ctk.CTkFrame):
    """Tarjeta de resumen."""

    def __init__(self, maestro, titulo, valor="0",
                 color=COLORES["primario"], **kwargs):
        super().__init__(maestro, corner_radius=12,
                         fg_color=COLORES["tarjeta"],
                         border_width=1, border_color=COLORES["borde"],
                         **kwargs)

        barra = ctk.CTkFrame(self, height=4, fg_color=color,
                             corner_radius=2)
        barra.pack(fill="x", padx=15, pady=(15, 5))

        self.lbl_valor = ctk.CTkLabel(self, text=str(valor),
                                       font=FUENTES["tarjeta_valor"],
                                       text_color=color)
        self.lbl_valor.pack(pady=(5, 0))

        self.lbl_titulo = ctk.CTkLabel(self, text=titulo,
                                        font=FUENTES["tarjeta_titulo"],
                                        text_color=COLORES["texto_secundario"])
        self.lbl_titulo.pack(pady=(0, 15))

    def actualizar(self, valor):
        self.lbl_valor.configure(text=str(valor))
