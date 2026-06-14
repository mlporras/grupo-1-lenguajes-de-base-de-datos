import customtkinter as ctk
from tkinter import messagebox
from interfaz.tema import COLORES, FUENTES
from interfaz.componentes import TablaEstilizada, DialogoFormulario
from servicios import materiales_servicio, tipos_material_servicio, categorias_servicio

COLUMNAS = [
    ("id", "ID", 50),
    ("titulo", "Titulo", 200),
    ("autor", "Autor", 150),
    ("editorial", "Editorial", 120),
    ("anio", "Anio", 60),
    ("isbn", "ISBN", 140),
    ("tipo_id", "Tipo ID", 0),
    ("cat_id", "Cat ID", 0),
    ("estado", "Estado", 90),
    ("tipo", "Tipo", 110),
    ("categoria", "Categoria", 120),
]


class MaterialesVista(ctk.CTkFrame):

    def __init__(self, maestro):
        super().__init__(maestro, fg_color=COLORES["fondo"])

        cab = ctk.CTkFrame(self, fg_color="transparent")
        cab.pack(fill="x", padx=30, pady=(25, 10))

        ctk.CTkLabel(cab, text="Gestion de Materiales", font=FUENTES["titulo"],
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

        barra = ctk.CTkFrame(self, fg_color="transparent")
        barra.pack(fill="x", padx=30, pady=(0, 10))

        self.entrada_busqueda = ctk.CTkEntry(barra, width=300,
                                              placeholder_text="Buscar por titulo, autor o categoria...")
        self.entrada_busqueda.pack(side="left")
        self.entrada_busqueda.bind("<Return>", lambda _: self.buscar())

        ctk.CTkButton(barra, text="Buscar", width=80,
                      command=self.buscar).pack(side="left", padx=5)
        ctk.CTkButton(barra, text="Limpiar", width=80,
                      fg_color=COLORES["texto_secundario"],
                      command=self._limpiar_busqueda).pack(side="left", padx=5)

        self.tabla = TablaEstilizada(self, COLUMNAS)
        self.tabla.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        self.tabla.vincular_doble_clic(self.editar)

    def refrescar(self):
        try:
            _, filas = materiales_servicio.listar_materiales()
            self.tabla.cargar_datos(filas)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)

    def buscar(self):
        texto = self.entrada_busqueda.get().strip()
        if not texto:
            self.refrescar()
            return
        try:
            _, filas = materiales_servicio.buscar_materiales(texto)
            self.tabla.cargar_datos(filas)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)

    def _limpiar_busqueda(self):
        self.entrada_busqueda.delete(0, "end")
        self.refrescar()

    def _obtener_campos(self, incluir_id=False):
        try:
            _, tipos = tipos_material_servicio.listar_tipos_material()
            opc_tipo = [(int(t[0]), t[1]) for t in tipos if t[3] == "A"]
        except Exception:
            opc_tipo = []
        try:
            _, cats = categorias_servicio.listar_categorias()
            opc_cat = [(int(c[0]), c[1]) for c in cats if c[3] == "A"]
        except Exception:
            opc_cat = []

        campos = [
            {"nombre": "titulo", "etiqueta": "Titulo", "tipo": "texto",
             "requerido": True},
            {"nombre": "autor", "etiqueta": "Autor", "tipo": "texto"},
            {"nombre": "editorial", "etiqueta": "Editorial", "tipo": "texto"},
            {"nombre": "anio", "etiqueta": "Anio Publicacion", "tipo": "texto"},
            {"nombre": "isbn", "etiqueta": "Codigo ISBN", "tipo": "texto"},
            {"nombre": "id_tipo", "etiqueta": "Tipo de Material",
             "tipo": "combo", "opciones": opc_tipo, "requerido": True},
            {"nombre": "id_categoria", "etiqueta": "Categoria",
             "tipo": "combo", "opciones": opc_cat, "requerido": True},
        ]
        return campos

    def crear(self):
        campos = self._obtener_campos()
        dlg = DialogoFormulario(self, "Crear Material", campos)
        if dlg.resultado:
            try:
                r = dlg.resultado
                anio = int(r["anio"]) if r["anio"] else None
                isbn = r["isbn"] if r["isbn"] else None
                materiales_servicio.crear_material(
                    r["titulo"], r["autor"], r["editorial"],
                    anio, isbn, r["id_tipo"], r["id_categoria"])
                messagebox.showinfo("Exito", "Material creado.", parent=self)
                self.refrescar()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self)

    def editar(self):
        sel = self.tabla.obtener_seleccion()
        if not sel:
            messagebox.showwarning("Aviso", "Seleccione un material.",
                                   parent=self)
            return
        campos = self._obtener_campos()
        valores = {
            "titulo": sel[1], "autor": sel[2], "editorial": sel[3],
            "anio": sel[4], "isbn": sel[5],
            "id_tipo": sel[6], "id_categoria": sel[7],
        }
        dlg = DialogoFormulario(self, "Editar Material", campos, valores)
        if dlg.resultado:
            try:
                r = dlg.resultado
                anio = int(r["anio"]) if r["anio"] else None
                isbn = r["isbn"] if r["isbn"] else None
                materiales_servicio.actualizar_material(
                    int(sel[0]), r["titulo"], r["autor"], r["editorial"],
                    anio, isbn, r["id_tipo"], r["id_categoria"])
                messagebox.showinfo("Exito", "Material actualizado.",
                                    parent=self)
                self.refrescar()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self)

    def inactivar(self):
        sel = self.tabla.obtener_seleccion()
        if not sel:
            messagebox.showwarning("Aviso", "Seleccione un material.",
                                   parent=self)
            return
        if messagebox.askyesno("Confirmar",
                               f"Inactivar material '{sel[1]}'?",
                               parent=self):
            try:
                materiales_servicio.inactivar_material(int(sel[0]))
                messagebox.showinfo("Exito", "Material inactivado.",
                                    parent=self)
                self.refrescar()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self)
