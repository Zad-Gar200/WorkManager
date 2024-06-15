import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import mysql.connector

# Función para cargar el nombre del usuario desde el archivo de texto
def cargar_nombre_usuario():
    try:
        with open("usuario.txt", "r") as file:
            nombre = file.readline().strip()
            return nombre
    except FileNotFoundError:
        return "Usuario"

# Función para regresar a la página principal
def regresar_a_pag1():
    root.destroy()
    import Pag1

# Función para seleccionar una foto y guardarla en la base de datos
def seleccionar_foto_y_guardar_en_bd():
    filename = filedialog.askopenfilename(
        initialdir="/", 
        title="Seleccionar archivo de imagen", 
        filetypes=(("Archivos de imagen", "*.jpg;*.png;*.jpeg"), ("Todos los archivos", "*.*"))
    )

    if filename:
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="usuarios"
            )
            cursor = connection.cursor()

            with open(filename, "rb") as file:
                imagen_blob = file.read()

            query = "INSERT INTO imagen (imagen) VALUES (%s)"
            cursor.execute(query, (imagen_blob,))
            connection.commit()

            cursor.close()
            connection.close()
            messagebox.showinfo("Éxito", "La imagen se ha guardado correctamente en la base de datos.")
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al guardar la imagen en la base de datos: {str(e)}")

# Función para cambiar el nombre de usuario en la base de datos y archivo
def cambiar_usuario():
    nuevo_nombre = simpledialog.askstring("Cambiar Usuario", "Ingrese el nuevo nombre de usuario:")
    if nuevo_nombre:
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="usuarios"
            )
            cursor = connection.cursor()
            
            nombre_actual = cargar_nombre_usuario()
            cursor.execute("SELECT id FROM usuarios WHERE nombre_usuario = %s", (nombre_actual,))
            usuario = cursor.fetchone()

            if usuario:
                query = "UPDATE usuarios SET nombre_usuario = %s WHERE id = %s"
                cursor.execute(query, (nuevo_nombre, usuario[0]))
                connection.commit()

                cursor.close()
                connection.close()
                
                # Actualizar el nombre en la interfaz y en el archivo
                label_nombre_usuario.config(text=f"Usuario actual: {nuevo_nombre}")
                with open("usuario.txt", "w") as file:
                    file.write(nuevo_nombre)
                messagebox.showinfo("Éxito", "El nombre de usuario se ha actualizado correctamente.")
            else:
                messagebox.showerror("Error", "No se encontró el usuario en la base de datos.")
        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al cambiar el nombre de usuario: {str(e)}")

# Crear la ventana principal
root = tk.Tk()
root.title("Pag4")
root.geometry("360x640")

# Configuración del icono de la ventana
image_path = "FON.jpg"
image = Image.open(image_path)
icono = ImageTk.PhotoImage(image)
root.iconphoto(False, icono)

# Crear el marco del encabezado
frame_encabezado = ttk.Frame(root, padding="10 10 10 10")
frame_encabezado.pack(fill="x")
label_encabezado = ttk.Label(frame_encabezado, text="CONFIGURACIONES", font=("Helvetica", 16, "bold"), background="#00AEEF")
label_encabezado.pack(fill="x")

# Crear el marco del contenido principal
frame_contenido = ttk.Frame(root, padding="10 10 10 10")
frame_contenido.pack(fill="both", expand=True)

# Etiqueta para mostrar el nombre del usuario
nombre_usuario_actual = cargar_nombre_usuario()
label_nombre_usuario = ttk.Label(frame_contenido, text=f"Usuario actual: {nombre_usuario_actual}", font=("Helvetica", 12))
label_nombre_usuario.pack(padx=20, pady=10)

# Botón para seleccionar y guardar una foto en la base de datos
btn_cambiar_foto = ttk.Button(frame_contenido, text="SELECCIONAR Y GUARDAR FOTO", command=seleccionar_foto_y_guardar_en_bd)
btn_cambiar_foto.pack(padx=20, pady=20)

# Botón para cambiar el nombre de usuario
btn_cambiar_usuario = ttk.Button(frame_contenido, text="CAMBIAR USUARIO", command=cambiar_usuario)
btn_cambiar_usuario.pack(padx=20, pady=20)

# Botón para regresar al menú principal
btn_regresar = ttk.Button(frame_contenido, text="REGRESAR AL MENU", command=regresar_a_pag1)
btn_regresar.pack(pady=20)

# Ejecutar la aplicación
root.mainloop()
