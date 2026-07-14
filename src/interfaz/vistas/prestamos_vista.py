import customtkinter as ctk
from tkinter import messagebox
from interfaz.tema import COLORES, FUENTES
from interfaz.componentes import TablaEstilizada, DialogoFormulario
from servicios import (
    prestamos_servicio, usuarios_servicio, materiales_servicio,
    validaciones_servicio, reportes_servicio,
)

COLUMNAS = [
    ("id", "ID", 50),
    ("usuario", "Usuario", 180),
    ("material", "Material", 200),
    ("f_prest", "Fecha Prestamo", 110),
    ("f_dev_esp", "Dev. Esperada", 110),
    ("f_dev_real", "Dev. Real", 110),
    ("estado", "Estado", 90),
]

_MSG_VALIDACION = {
    "USUARIO_INACTIVO_O_NO_EXISTE": "El usuario no existe o esta inactivo.",
    "USUARIO_CON_MULTAS_PENDIENTES": "El usuario tiene multas pendientes.",
    "LIMITE_DE_PRESTAMOS_ALCANZADO": "El usuario ya tiene 3 prestamos activos.",
}


class PrestamosVista(ctk.CTkFrame):

    def __init__(self, maestro):
        super().__init__(maestro, fg_color=COLORES["fondo"])

        cab = ctk.CTkFrame(self, fg_color="transparent")
        cab.pack(fill="x", padx=30, pady=(25, 10))

        ctk.CTkLabel(cab, text="Gestion de Prestamos", font=FUENTES["titulo"],
                     text_color=COLORES["texto"]).pack(side="left")

        ctk.CTkButton(cab, text="Refrescar", width=100,
                      command=self.refrescar).pack(side="right", padx=5)
        ctk.CTkButton(cab, text="Anular", width=100,
                      fg_color=COLORES["peligro"],
                      hover_color=COLORES["peligro_hover"],
                      command=self.anular).pack(side="right", padx=5)
        ctk.CTkButton(cab, text="Devolver", width=100,
                      fg_color=COLORES["advertencia"],
                      command=self.devolver).pack(side="right", padx=5)
        ctk.CTkButton(cab, text="Registrar Prestamo", width=150,
                      fg_color=COLORES["exito"],
                      hover_color=COLORES["exito_hover"],
                      command=self.registrar_prestamo).pack(side="right", padx=5)

        filtro_marco = ctk.CTkFrame(self, fg_color="transparent")
        filtro_marco.pack(fill="x", padx=30, pady=(0, 5))

        self.filtro = ctk.CTkSegmentedButton(
            filtro_marco, values=["Todos", "Activos", "Vencidos", "Historial"],
            command=self._cambiar_filtro)
        self.filtro.set("Todos")
        self.filtro.pack(side="left")

        self.marco_historial = ctk.CTkFrame(filtro_marco, fg_color="transparent")

        ctk.CTkLabel(self.marco_historial, text="Cedula:",
                     font=FUENTES["normal"]).pack(side="left", padx=(15, 5))
        self.entrada_cedula = ctk.CTkEntry(self.marco_historial, width=160,
                                            placeholder_text="Ingrese cedula")
        self.entrada_cedula.pack(side="left")
        self.entrada_cedula.bind("<Return>", lambda _: self._buscar_historial())
        ctk.CTkButton(self.marco_historial, text="Buscar", width=80,
                      command=self._buscar_historial).pack(side="left", padx=5)

        self.tabla = TablaEstilizada(self, COLUMNAS)
        self.tabla.pack(fill="both", expand=True, padx=30, pady=(5, 20))

    def _cambiar_filtro(self, _valor):
        if self.filtro.get() == "Historial":
            self.marco_historial.pack(side="left")
        else:
            self.marco_historial.pack_forget()
            self.refrescar()

    def refrescar(self):
        modo = self.filtro.get()
        try:
            if modo == "Activos":
                _, filas = prestamos_servicio.listar_prestamos_activos()
                mapeadas = [self._mapear(f) for f in filas]
            elif modo == "Vencidos":
                _, filas = reportes_servicio.listar_prestamos_vencidos()
                mapeadas = [self._mapear_vencido(f) for f in filas]
            elif modo == "Historial":
                self._buscar_historial()
                return
            else:
                _, filas = prestamos_servicio.listar_prestamos()
                mapeadas = [self._mapear(f) for f in filas]
            self.tabla.cargar_datos(mapeadas)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)

    def _mapear(self, fila):
        return (fila[0], fila[7], fila[8], fila[3], fila[4], fila[5], fila[6])

    def _mapear_vencido(self, fila):
        # VW: id, cedula, id_mat, f_prest, f_esp, usuario, material
        return (fila[0], fila[5], fila[6], fila[3], fila[4], "", "VENCIDO")

    def _mapear_historial(self, fila):
        return (fila[0], "-", fila[6], fila[2], fila[3], fila[4], fila[5])

    def _buscar_historial(self):
        cedula = self.entrada_cedula.get().strip()
        if not cedula:
            messagebox.showwarning("Aviso", "Ingrese la cedula del usuario.",
                                   parent=self)
            return
        try:
            _, filas = prestamos_servicio.listar_historial_usuario(cedula)
            mapeadas = [self._mapear_historial(f) for f in filas]
            self.tabla.cargar_datos(mapeadas)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)

    def registrar_prestamo(self):
        try:
            _, usuarios = usuarios_servicio.listar_usuarios()
            opc_usr = [(u[0], f"{u[0]} - {u[1]} {u[2]}")
                       for u in usuarios if u[6] == "A"]
        except Exception:
            opc_usr = []

        try:
            _, materiales = materiales_servicio.listar_materiales()
            opc_mat = [(int(m[0]), f"{m[0]} - {m[1]}")
                       for m in materiales if m[8] == "DISPONIBLE"]
        except Exception:
            opc_mat = []

        if not opc_usr:
            messagebox.showwarning("Aviso",
                                   "No hay usuarios activos disponibles.",
                                   parent=self)
            return
        if not opc_mat:
            messagebox.showwarning("Aviso",
                                   "No hay materiales disponibles.",
                                   parent=self)
            return

        campos = [
            {"nombre": "cedula", "etiqueta": "Usuario", "tipo": "combo",
             "opciones": opc_usr, "requerido": True},
            {"nombre": "id_material", "etiqueta": "Material", "tipo": "combo",
             "opciones": opc_mat, "requerido": True},
            {"nombre": "fecha_dev", "etiqueta": "Fecha Devolucion Esperada",
             "tipo": "fecha", "requerido": True},
        ]

        dlg = DialogoFormulario(self, "Registrar Prestamo", campos)
        if dlg.resultado:
            try:
                r = dlg.resultado
                # valida antes de registrar
                resultado = validaciones_servicio.validar_prestamo(r["cedula"])
                if resultado != "OK":
                    msg = _MSG_VALIDACION.get(
                        resultado, f"No se puede prestar: {resultado}")
                    messagebox.showwarning("Validacion", msg, parent=self)
                    return

                prestamos_servicio.registrar_prestamo(
                    r["cedula"], r["id_material"], r["fecha_dev"])
                messagebox.showinfo("Exito", "Prestamo registrado.",
                                    parent=self)
                self.refrescar()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self)

    def devolver(self):
        sel = self.tabla.obtener_seleccion()
        if not sel:
            messagebox.showwarning("Aviso", "Seleccione un prestamo.",
                                   parent=self)
            return
        if sel[6] not in ("ACTIVO", "VENCIDO"):
            messagebox.showwarning("Aviso",
                                   "Solo se pueden devolver prestamos activos.",
                                   parent=self)
            return

        id_prestamo = int(sel[0])
        mensaje = f"Registrar devolucion del prestamo {id_prestamo}?"
        try:
            dias = reportes_servicio.dias_retraso(id_prestamo)
            if dias > 0:
                mensaje = (
                    f"El prestamo {id_prestamo} tiene {dias} dia(s) de atraso.\n"
                    "Se generara una multa al devolver.\n\nContinuar?"
                )
        except Exception:
            pass

        if messagebox.askyesno("Confirmar", mensaje, parent=self):
            try:
                prestamos_servicio.registrar_devolucion(id_prestamo)
                messagebox.showinfo("Exito", "Devolucion registrada.",
                                    parent=self)
                self.refrescar()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self)

    def anular(self):
        sel = self.tabla.obtener_seleccion()
        if not sel:
            messagebox.showwarning("Aviso", "Seleccione un prestamo.",
                                   parent=self)
            return
        if sel[6] not in ("ACTIVO", "VENCIDO"):
            messagebox.showwarning("Aviso",
                                   "Solo se pueden anular prestamos activos.",
                                   parent=self)
            return
        if messagebox.askyesno("Confirmar",
                               f"Anular prestamo {sel[0]}?", parent=self):
            try:
                prestamos_servicio.anular_prestamo(int(sel[0]))
                messagebox.showinfo("Exito", "Prestamo anulado.", parent=self)
                self.refrescar()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self)
