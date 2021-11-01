from os import path
from tkinter import *
from tkinter.filedialog import askdirectory, askopenfilenames
from tkinter import messagebox as MessageBox
from unrar import rarfile
import zipfile
import itertools as its

window = Tk()
folderPath = StringVar()
folderPath2 = StringVar()

filename=""
out=""
words = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.' # parámetros relacionados con la generación de contraseñas

def btn_clicked():
    global filename
    global words
    pwds = get_password(1, 20, words)

    if filename != "":

        if filename.endswith('.rar'):
            file = rarfile.RarFile(filename)
            while True:
                word = next(pwds)
                if get_pwd(file, word, "rar"):
                    break
        elif filename.endswith('.zip'):
            file = zipfile.ZipFile(filename)
            while True:
                word = next(pwds)
                if get_pwd(file, bytes(word,'utf-8'), "zip"):
                    break
        else:
            MessageBox.showerror("Alerta", "El archivo seleccionado no es compatible.\n (seleccione .zip o .rar)")
          
        filename = ""
        folderPath.set(filename)
        folderPath2.set(filename)
    else:
        MessageBox.showwarning("Alerta", "Ruta para descifrar archivo comprimido vacia.")

def callbackFile():
    global filename
    global out
    filename = askopenfilenames()[0]
    folderPath.set(filename)
    MessageBox.showinfo("Ubicacion", "Por favor, seleccione la carpeta donde se descomprimira")
    out = askdirectory()

def get_password(min_digits, max_digits, words):
    while min_digits <= max_digits:
        pwds = its.product(words, repeat=min_digits)
        for pwd in pwds:
            yield ''.join(pwd)
        min_digits += 1

def get_pwd(file, word, var):
    # Pase la ruta del archivo descomprimido para generar el objeto de archivo a descomprimir
    global out
    try:
        file.extractall(path=out, pwd=word)
        # Explique que la contraseña actual es válida e informe
        if var=="rar":
            folderPath2.set(word)
            MessageBox.showinfo("Ok", "Archivo descifrado.\nPwd: {}".format(word))
        else:
            folderPath2.set(str(word, 'utf-8'))
            MessageBox.showinfo("Ok", "Archivo descifrado.\nPwd: {}".format(str(word, 'utf-8')))
        out = ""
        return True
    except Exception as e:
        # Contraseña incorrecta
        if var=="rar":
            print('"{}" is nor correct password!'.format(word))
            folderPath2.set(word)
        else:
            print('"{}" is nor correct password!'.format(str(word, 'utf-8')))
            folderPath2.set(str(word, 'utf-8'))
        # print(e)
        return False

window.geometry("400x400")
window.configure(bg = "#dadada")
canvas = Canvas(
    window,
    bg = "#dadada",
    height = 400,
    width = 400,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    200.0, 200.0,
    image=background_img)

entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(
    171.0, 218.0,
    image = entry0_img)

entry0 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0,
    textvariable=folderPath)

entry0.place(
    x = 32.0, y = 201,
    width = 278.0,
    height = 32)

entry1_img = PhotoImage(file = f"img_textBox1.png")
entry1_bg = canvas.create_image(
    194.5, 354.0,
    image = entry1_img)

entry1 = Entry(
    bd = 0,
    bg = "#000000",
    foreground="green",
    highlightthickness = 0,
    textvariable=folderPath2)

entry1.place(
    x = 111.0, y = 341,
    width = 167.0,
    height = 24)

img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 147, y = 281,
    width = 96,
    height = 29)

img1 = PhotoImage(file = f"img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = callbackFile,
    relief = "flat")

b1.place(
    x = 322, y = 199,
    width = 67,
    height = 36)

window.resizable(False, False)
window.mainloop()