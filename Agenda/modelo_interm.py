import sqlite3
from sqlite3 import Error
from tkinter import messagebox
from tkinter import ttk
from tkinter import Tk
from peewee import *
from datetime import datetime
import sys
import re


db = SqliteDatabase("basetfinal.db")


class BaseModel(Model):
    class Meta:
        database = db


class Agenda(BaseModel):

    nombre = TextField()
    apellido = TextField()
    dni = TextField()
    tel = TextField()
    mail = TextField()


db.connect()
db.create_tables([Agenda])


class Log(BaseModel):

    datos = TextField()
    fecha = DateTimeField(default=datetime.now())


db.create_tables([Log])

"""
A continuación se crearán dos decoradores que registrarán en una nueva tabla dentro de
la misma base de datos un registro de log para el alta y modificación de los registros
"""


def log(funcion):
    def log_insert(*args, **kwargs):

        funcion(*args, **kwargs)

        cadena = args[5]
        patron = "\w.+@\w+(?:\.[a-z]+)"

        if re.match(patron, cadena):

            entry = [str(args[1]) + " " + str(args[2]), str(datetime.now())]
            log_insert = Log(
                datos=entry[0],
                fecha=entry[1],
            )
            print(
                "El contacto "
                + str(entry[0]).upper()
                + " fue cargado el siguiente día y horario: "
                + str(entry[1])
            )
            log_insert.save()
        else:
            pass

    return log_insert


def log2(funcion):
    def log_modif(*args, **kwargs):

        funcion(*args, **kwargs)

        entry = [str(args[2]) + " " + str(args[3]), str(datetime.now())]
        log_modif = Log(
            datos=entry[0],
            fecha=entry[1],
        )
        print(
            "El contacto "
            + str(entry[0]).upper()
            + " fue modificado el siguiente día y horario: "
            + str(entry[1])
        )
        log_modif.save()

    return log_modif


class Crud:
    """
    En esta clase se desarrollan los métodos que permitirán
    hacer la conexión con la base de datos, crear la tabla
    y realizar las funciones de alta, baja, modificación y
    consulta de los registros de la agenda.
    """

    def __init__(
        self,
    ):
        pass

    def conectar(self):
        db.connect()
        return db

    def creartabla(self):
        try:
            db.connect()
            db.create_tables([Agenda])

        except sqlite3.OperationalError:
            print("La tabla ya existe!")

    @log
    def insertar_registros(self, nombre, apellido, dni, tel, mail):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.tel = tel
        self.mail = mail

        cadena = mail
        patron = "\w.+@\w+(?:\.[a-z]+)"

        if re.match(patron, cadena):
            agenda = Agenda()
            agenda.nombre = nombre
            agenda.apellido = apellido
            agenda.dni = dni
            agenda.tel = tel
            agenda.mail = mail
            agenda.save()

            messagebox.showinfo(
                "REGISTRO AGREGADO", "El registro ha sido agregado con éxito."
            )

        else:

            messagebox.showwarning(
                "ERROR AL INGRESAR EMAIL",
                "El formato ingresado no es válido. \n Debe ingresar un formato de email: 'ejemplo@mail.com'. \n \n Intentalo nuevamente.",
            )

    def listar_registros(self, nombre, apellido, dni, tel, mail):
        agenda = Agenda()
        agenda.nombre = nombre
        agenda.apellido = apellido
        agenda.dni = dni
        agenda.tel = tel
        agenda.mail = mail
        query = Agenda.select().tuples()

        return query

    @log2
    def editar_registros(self, miid, nombre, apellido, dni, tel, mail):
        self.miid = miid
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.tel = tel
        self.mail = mail

        cadena = mail
        patron = "\w.+@\w+(?:\.[a-z]+)"
        if re.match(patron, cadena):
            modificar = Agenda.update(
                nombre=nombre, apellido=apellido, dni=dni, tel=tel, mail=mail
            ).where(Agenda.id == miid)
            modificar.execute()

            messagebox.showinfo(
                "REGISTRO EDITADO", "El registro ha sido editado con éxito."
            )
        else:
            messagebox.showwarning(
                "ERROR AL INGRESAR EMAIL",
                "El formato ingresado no es válido. \n Debe ingresar un formato de email: 'ejemplo@mail.com'. \n \n Intentalo nuevamente.",
            )

    def eliminar_registros(self, miid, nombre, apellido, dni, tel, mail):

        self.miid = miid
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.tel = tel
        self.mail = mail
        query = Agenda.delete().where(Agenda.id == miid)
        query.execute()

        messagebox.showinfo(
            "REGISTRO ELIMINADO", "El registro ha sido eliminado con éxito."
        )
