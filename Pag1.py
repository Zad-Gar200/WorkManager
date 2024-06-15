import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector

# Función para cargar el nombre del usuario
def cargar_nombre_usuario():
    try:
        with open("usuario.txt", "r") as file:
            nombre = file.readline().strip()
            return nombre
    except FileNotFoundError:
        return "Usuario"

# Función para abrir la página 2
def abrir_pag2():
    root.destroy()
    import Pag2

# Función para abrir la página 3
def abrir_pag3():
    root.destroy()
    import Pag3

# Función para abrir la página 4
def abrir_pag4():
    root.destroy()
    import Pag4

# Función para conectar con la base de datos
def conectar_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='usuarios'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Función para cargar los trabajos del usuario actual
def cargar_trabajos():
    usuario = cargar_nombre_usuario()
    connection = conectar_db()
    
    if connection:
        cursor = connection.cursor()
        
        # Obtener el ID del usuario
        cursor.execute("SELECT id FROM usuarios WHERE nombre_usuario = %s", (usuario,))
        resultado = cursor.fetchone()
        
        if resultado:
            usuario_id = resultado[0]
            
            # Obtener los trabajos del usuario
            cursor.execute("SELECT descripcion FROM trabajos WHERE usuario_id = %s", (usuario_id,))
            trabajos = cursor.fetchall()
            trabajos = [trabajo[0] for trabajo in trabajos]
        else:
            trabajos = []
        
        cursor.close()
        connection.close()
        return trabajos
    else:
        return []

# Función para actualizar los trabajos en la interfaz
def actualizar_trabajos(nuevos_trabajos):
    for widget in frame_contenido.winfo_children():
        widget.destroy()
        
    # Trabajos Pendientes
    label_trabajos_pendientes = ttk.Label(frame_contenido, text="Trabajos Pendientes", font=("Helvetica", 14, "bold"))
    label_trabajos_pendientes.pack(anchor="w")

    for trabajo in nuevos_trabajos:
        label_trabajo = ttk.Label(frame_contenido, text=f"• {trabajo}")
        label_trabajo.pack(anchor="w", padx=20)

    root.update()

# Crear la ventana principal
root = tk.Tk()
root.title("Work Manager")
root.geometry("360x640")

# Cargar la imagen y redimensionarla a 20x20 píxeles
image_path = "FON.jpeg"
image = Image.open(image_path)
image = image.resize((20, 20), Image.LANCZOS)
photo = ImageTk.PhotoImage(image)

# Establecer el icono de la ventana
root.iconphoto(False, photo)

# Crear un marco para el encabezado
frame_encabezado = ttk.Frame(root, padding="10 10 10 10")
frame_encabezado.pack(fill="x")

# Crear un label para la imagen
label_imagen = ttk.Label(frame_encabezado, image=photo)
label_imagen.grid(row=0, column=0, padx=(0, 10))

# Obtener el nombre del usuario
nombre_usuario = cargar_nombre_usuario()

# Crear un label para el mensaje de bienvenida
label_bienvenida = ttk.Label(frame_encabezado, text=f"Bienvenid@ {nombre_usuario}")
label_bienvenida.grid(row=0, column=1, sticky="w")

# Crear un marco para el contenido principal
frame_principal = ttk.Frame(root)
frame_principal.pack(fill="both", expand=True)

# Crear los elementos de la interfaz según la imagen proporcionada
# Barra lateral
frame_lateral = ttk.Frame(frame_principal, width=80, relief="ridge", padding="10 10 10 10")
frame_lateral.pack(side="left", fill="y")

btn_usuario = ttk.Button(frame_lateral, text="USUARIO", command=abrir_pag4)
btn_usuario.pack(pady=5)

btn_equipos = ttk.Button(frame_lateral, text="EQUIPOS", command=abrir_pag2)
btn_equipos.pack(pady=5)

# Contenido principal
frame_contenido = ttk.Frame(frame_principal, padding="10 10 10 10")
frame_contenido.pack(side="left", fill="both", expand=True)

# Cargar los trabajos al inicio
trabajos = cargar_trabajos()
actualizar_trabajos(trabajos)

# Ejecutar la aplicación
root.mainloop()
