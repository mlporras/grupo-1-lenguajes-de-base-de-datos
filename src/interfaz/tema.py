import customtkinter as ctk
from tkinter import ttk

COLORES = {
    "primario": "#3b82f6",
    "primario_hover": "#2563eb",
    "primario_claro": "#dbeafe",
    "exito": "#22c55e",
    "exito_hover": "#16a34a",
    "advertencia": "#f59e0b",
    "peligro": "#ef4444",
    "peligro_hover": "#dc2626",
    "sidebar": "#1e293b",
    "sidebar_hover": "#334155",
    "sidebar_texto": "#e2e8f0",
    "sidebar_activo": "#3b82f6",
    "fondo": "#f1f5f9",
    "tarjeta": "#ffffff",
    "borde": "#e2e8f0",
    "texto": "#0f172a",
    "texto_secundario": "#64748b",
    "tabla_cabecera": "#f1f5f9",
    "tabla_par": "#f8fafc",
    "tabla_impar": "#ffffff",
    "tabla_seleccion": "#dbeafe",
}

FUENTES = {
    "titulo": ("Segoe UI", 22, "bold"),
    "subtitulo": ("Segoe UI", 16, "bold"),
    "normal": ("Segoe UI", 13),
    "pequena": ("Segoe UI", 11),
    "boton": ("Segoe UI", 13),
    "tabla": ("Segoe UI", 12),
    "tabla_cabecera": ("Segoe UI", 12, "bold"),
    "tarjeta_valor": ("Segoe UI", 28, "bold"),
    "tarjeta_titulo": ("Segoe UI", 12),
}


def configurar_tema():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    estilo = ttk.Style()
    estilo.theme_use("clam")
    estilo.configure("Treeview",
                     background=COLORES["tabla_impar"],
                     foreground=COLORES["texto"],
                     fieldbackground=COLORES["tabla_impar"],
                     rowheight=32,
                     font=FUENTES["tabla"],
                     borderwidth=0)
    estilo.configure("Treeview.Heading",
                     background=COLORES["tabla_cabecera"],
                     foreground=COLORES["texto"],
                     font=FUENTES["tabla_cabecera"],
                     borderwidth=1,
                     relief="flat")
    estilo.map("Treeview",
               background=[("selected", COLORES["tabla_seleccion"])],
               foreground=[("selected", COLORES["texto"])])
    estilo.map("Treeview.Heading",
               background=[("active", COLORES["borde"])])
