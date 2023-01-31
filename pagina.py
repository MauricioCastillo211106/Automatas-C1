import urllib.request
from bs4 import BeautifulSoup
import re
import sys
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog
from tkinter.ttk import Treeview
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from AFD import *

telefonosRecuperados = []
telefonosValidados = []


def borardatosdeltxt():
    with open('TelefonosValidos.txt', 'w') as f:
        pass


def datosfinales():
    mostrardatos()


def mostrardatos():
    ventana = Tk()
    ventana.title('Telefonos validos')
    ventana.geometry('400x300')
    ventana['bg'] = '#fb0'

    tabla = ttk.Treeview(ventana, columns=1, height=50)
    tabla.pack(pady=15, padx=10)
    tabla.column("#0", width=500, minwidth=100)
    tabla.heading("#0", text="Telefonos", anchor=CENTER)

    with open('TelefonosValidos.txt') as archivo:
        print(type(archivo))
        for linea in archivo:
            if linea == " ":
                print("no hay valores")
            else:
                tabla.insert('', 0, text=linea)

    tabla.pack()

    ventana.mainloop()


def lecturaPaginaWeb(urlvalo):

    urlvalor = urlvalo

    with urllib.request.urlopen(urlvalor) as url:
        s = url.read()
        try:
            soup = BeautifulSoup(s)
        except:
            print("Url no valida")


# eliminar todos los elementos de script y estilo
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

# extrae el puro texto
    text = soup.get_text()

# divide en líneas y elimina el espacio inicial y final en cada texto
    lines = (line.strip() for line in text.splitlines())

# ayuda a divir varios titulos en cada linea de cada uno
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

# ayuda a hacer saltos de lineas en cada texto
    text = '\n'.join(chunk for chunk in chunks if chunk)
# print(text)

# escritura en el txt
    try:
        with open('texto.txt', 'w') as f:
            f.write(text)
            f.close()

    except:
        valordeverdad = False

      # recuperacion de posibles Telefonos
    with open('texto.txt') as archivo:
        for linea in archivo:
            #remplazamos los saltos de lineas que se tienen en linea
            lin = linea.replace("\n", "")
            #pasamos el  valor lin sin salto de linea para que el automata lo valide
            afd.automata(lin)
            print(afd.automata(lin))
            #si el automata retorna un true entonces entra
            if afd.automata(lin):
                #imprimimos el valor del automata, posteriormente se guardan los valores verdaderos
                print(afd.automata(lin))
                telefonosValidados.append(lin)
                print(telefonosValidados)
    contenedor = str(telefonosValidados)
    cal = contenedor.replace("[", "")
    lista = cal.replace("]", "")
    limp = lista.replace("'", "")
    limpio = limp.replace("'", "")
    with open('TelefonosValidos.txt', 'w') as f:
        f.write(limpio)
        f.close()
        #limpiamos telefonosvalidados
    telefonosValidados.clear()
    #chequea el txt para poder mostrarlos o dar un aviso de que esta vacio
    with open('TelefonosValidos.txt') as f:
        vacio = f.readlines()
        print(vacio)
        if vacio == []:
            mb.showerror(
                "Mensaje", "No se encontraron Telefonos que sean validos")
        else:
            datosfinales()
    if valordeverdad == False:
        mb.showerror("Mensaje", "pagina protegida")
    else:
        datosfinales()


def datosfinales():
    mostrardatos()


def mostrardatos():
    ventana = Tk()
    ventana.title('Telefonos validos')
    ventana.geometry('400x300')
    ventana['bg'] = '#fb0'

    tabla = ttk.Treeview(ventana, columns=1, height=50)
    tabla.pack(pady=15, padx=10)
    tabla.column("#0", width=500, minwidth=100)
    tabla.heading("#0", text="Telefonos", anchor=CENTER)

    with open('TelefonosValidos.txt') as archivo:
        print(type(archivo))
        for linea in archivo:
            if linea == " ":
                print("no hay valores")
            else:
                saltos = linea.replace(",", "\n")
                tabla.insert('', 0, text=saltos)

    tabla.pack()

    ventana.mainloop()


def inicio():

    # iniciamos ventana

    ventana = tk.Tk()
    ventana.title("Automata")
    ventana.geometry("700x400")
    ventana.iconbitmap("recursos/icon.ico")

   # ventana.config(bg="assets/imgs/Polygon Luminary.png")
    ventana.resizable(width=False, height=False)

    usuario = tk.StringVar()
    # colores
    fondoBtn = "#00c2cb"
    textColor = "#FFFFFF"
    # Fondo
    fondoEntrar = PhotoImage(file="recursos/Polygon_Luminary.png")
    background = Label(image=fondoEntrar)
    background.place(x=0, y=0, relwidth=1, relheight=1)
    # Label
    entrada = tk.Entry(ventana, textvar=usuario, width=50,
                       relief="flat", bg=textColor, fg="black")

    # Texto
    texto = tk.Label(ventana, text="Ingresa el url a analizar", bg="white",
                     fg="black", font=("Futura", 32, ))

    texto.place(x=130, y=100)
    entrada.place(x=200, y=230)

    def sacarvalor():
        print(f"esto trae usuario {usuario.get()}")
        urlvalo = usuario.get()
        usuario.set('')
        lecturaPaginaWeb(urlvalo)
        # Botones

    boton = tk.Button(ventana, text="Ingresar", cursor="hand2", command=sacarvalor,
                      bg=fondoBtn, width=12, relief="flat", font=("Futura", 12))
    boton.place(x=300, y=300)

    ventana.mainloop()


if __name__ == '__main__':
    inicio()
