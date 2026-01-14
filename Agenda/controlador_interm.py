from tkinter import Tk
from vista_interm import VistaAgenda
import sqlite3


class MiAgenda:
    def __init__(self, window):
        self.ventana = window
        VistaAgenda(self.ventana)


if __name__ == "__main__":
    root = Tk()
    obj = MiAgenda(root)
    root.mainloop()
