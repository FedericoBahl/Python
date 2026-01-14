from tkinter import Entry
from tkinter import Tk
from tkinter import *
from tkinter import StringVar
from tkinter import Label
from tkinter import Button
from tkinter import ttk
from tkinter import messagebox
from modelo_interm import Crud


class VistaAgenda:

    """
    Esta es una clase destinada a agrupar toda la parte visual
    de la aplicación, como los entry, los botones, los labels
    y el treeview.
    """

    def __init__(self, window):
        self.root = window
        self.root.title("Mi Agenda")
        self.root.geometry("620x450")
        self.root.configure(background="#F5F5F5")

        self.objeto_conexion = Crud()

        self.miid = StringVar()
        self.nombre = StringVar()
        self.apellido = StringVar()
        self.dni = StringVar()
        self.tel = StringVar()
        self.mail = StringVar()

        self.e1 = ttk.Entry(self.root, textvariable=self.miid)

        l_nombre = ttk.Label(self.root, text="Nombre")
        l_apellido = ttk.Label(self.root, text="Apellido")
        l_dni = ttk.Label(self.root, text="DNI")
        l_cel = ttk.Label(self.root, text="Tel")
        l_mail = ttk.Label(self.root, text="Email")

        l_nombre.grid(row=0, column=0, sticky=W + E)
        l_apellido.grid(row=1, column=0, sticky=W + E)
        l_dni.grid(row=2, column=0, sticky=W + E)
        l_cel.grid(row=3, column=0, sticky=W + E)
        l_mail.grid(row=4, column=0, sticky=W + E)

        e_nombre = ttk.Entry(self.root, textvariable=self.nombre)
        e_nombre.focus()
        e_apellido = ttk.Entry(self.root, textvariable=self.apellido)
        e_dni = ttk.Entry(self.root, textvariable=self.dni)
        e_tel = ttk.Entry(self.root, textvariable=self.tel)
        e_mail = ttk.Entry(self.root, textvariable=self.mail)

        e_nombre.grid(row=0, column=1)
        e_apellido.grid(row=1, column=1)
        e_dni.grid(row=2, column=1)
        e_tel.grid(row=3, column=1)
        e_mail.grid(row=4, column=1)

        self.tree = ttk.Treeview(self.root, height=13)
        self.tree.grid(row=7, column=0, columnspan=50)
        self.tree["columns"] = ("col1", "col2", "col3", "col4", "col5")
        self.tree.heading("#0", text="ID")
        self.tree.heading("col1", text="Nombre")
        self.tree.heading("col2", text="Apellido")
        self.tree.heading("col3", text="DNI")
        self.tree.heading("col4", text="Tel.")
        self.tree.heading("col5", text="Email")

        self.tree.column("#0", width=20, minwidth=32)
        self.tree.column("col1", width=90, minwidth=80)
        self.tree.column("col2", width=100, minwidth=100)
        self.tree.column("col3", width=87, minwidth=87)
        self.tree.column("col4", width=100, minwidth=100)
        self.tree.column("col5", width=200, minwidth=200)

        self.tree.bind(
            "<Double-1>",
            self.seldobleclick,
        )

        self.sel = self.tree.item(self.tree.selection())["text"]

        b_agregar = ttk.Button(
            self.root,
            text="Agregar",
            command=lambda: self.agregar(
                self.nombre, self.apellido, self.dni, self.tel, self.mail
            ),
        )

        b_editar = ttk.Button(
            self.root,
            text="Editar",
            command=lambda: self.editar(
                self.miid, self.nombre, self.apellido, self.dni, self.tel, self.mail
            ),
        )
        b_eliminar = ttk.Button(
            self.root,
            text="Eliminar",
            command=lambda: self.eliminar(
                self.miid, self.nombre, self.apellido, self.dni, self.tel, self.mail
            ),
        )

        b_listar = ttk.Button(
            self.root,
            text="Ver lista",
            command=lambda: self.ver_lista(
                self.nombre, self.apellido, self.dni, self.tel, self.mail
            ),
        )
        b_limpiar = ttk.Button(
            self.root, text="Limpiar", command=lambda: self.limpiar_registros()
        )
        b_salir = ttk.Button(self.root, text="Salir", command=self.root.quit)

        self.message = Label(text="", fg="blue", bg="#F5F5F5")
        self.message.grid(row=5, column=0, columnspan=50, sticky=W + E)

        b_agregar.grid(row=0, column=3)
        b_listar.grid(row=1, column=3)
        b_editar.grid(row=2, column=3)
        b_eliminar.grid(row=3, column=3)
        b_limpiar.grid(row=4, column=3)
        b_salir.grid(row=8, column=45)

        self.message = Label(text="", fg="blue", bg="#F5F5F5")
        self.message.grid(row=5, column=0, columnspan=50, sticky=W + E)

    def agregar(self, nombre, apellido, dni, tel, mail):
        nombre = self.nombre.get()
        apellido = self.apellido.get()
        dni = self.dni.get()
        tel = self.tel.get()
        mail = self.mail.get()

        self.objeto_conexion.insertar_registros(nombre, apellido, dni, tel, mail)

        self.nombre.set("")
        self.apellido.set("")
        self.dni.set("")
        self.tel.set("")
        self.mail.set("")

    def editar(self, miid, nombre, apellido, dni, tel, mail):

        miid = self.miid.get()
        nombre = self.nombre.get()
        apellido = self.apellido.get()
        dni = self.dni.get()
        tel = self.tel.get()
        mail = self.mail.get()

        self.objeto_conexion.editar_registros(miid, nombre, apellido, dni, tel, mail)

        self.nombre.set("")
        self.apellido.set("")
        self.dni.set("")
        self.tel.set("")
        self.mail.set("")

    def eliminar(self, miid, nombre, apellido, dni, tel, mail):

        miid = self.miid.get()

        self.objeto_conexion.eliminar_registros(miid, nombre, apellido, dni, tel, mail)

        self.nombre.set("")
        self.apellido.set("")
        self.dni.set("")
        self.tel.set("")
        self.mail.set("")

    def ver_lista(self, nombre, apellido, dni, tel, mail):

        list = self.objeto_conexion.listar_registros(nombre, apellido, dni, tel, mail)

        for fila in list:
            self.tree.insert("", END, text=fila[0], values=fila[1:6])

    def limpiar_registros(
        self,
    ):
        self.tree.delete(*self.tree.get_children())

    def seldobleclick(self, event):
        item = self.tree.identify("item", event.x, event.y)
        self.miid.set(self.tree.item(item, "text"))
        self.nombre.set(self.tree.item(item, "values")[0])
        self.apellido.set(self.tree.item(item, "values")[1])
        self.dni.set(self.tree.item(item, "values")[2])
        self.tel.set(self.tree.item(item, "values")[3])
        self.mail.set(self.tree.item(item, "values")[4])
