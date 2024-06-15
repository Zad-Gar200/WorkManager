import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from PIL import Image, ImageTk

# Función para cargar el nombre del usuario
def cargar_nombre_usuario():
    try:
        with open("usuario.txt", "r") as file:
            nombre = file.readline().strip()
            return nombre
    except FileNotFoundError:
        return "Usuario"

# Función para cargar el rol del usuario
def cargar_rol():
    try:
        with open("rol.txt", "r") as file:
            rol = file.readline().strip()
            return rol
    except FileNotFoundError:
        return "usuario"  # Asume usuario por defecto si no se encuentra el archivo

# Función para regresar a la página principal
def regresar_a_pag1():
    root.destroy()
    import Pag1

# Función para eliminar un usuario de un equipo
def eliminar_usuario(equipo, usuario):
    equipos[equipo].remove(usuario)
    guardar_datos()
    actualizar_usuarios()

# Función para añadir un usuario a un equipo
def añadir_usuario():
    usuario = simpledialog.askstring("Añadir Usuario", "Ingrese el nombre del nuevo usuario:")
    if usuario:
        equipo = simpledialog.askstring("Añadir Usuario", "Seleccione el equipo para agregar al usuario (Equipo 1 o Equipo 2):")
        if equipo in equipos:
            equipos[equipo].append(usuario)
            guardar_datos()
            actualizar_usuarios()
        else:
            messagebox.showerror("Error", "El equipo seleccionado no existe.")

# Función para guardar los datos en un archivo
def guardar_datos():
    with open("datos.txt", "w") as file:
        for equipo, usuarios in equipos.items():
            file.write(f"{equipo}: {'|'.join(usuarios)}\n")

# Función para cargar los datos desde un archivo
def cargar_datos():
    try:
        with open("datos.txt", "r") as file:
            for line in file:
                line = line.strip()
                if line:  # Solo procesar líneas no vacías
                    try:
                        equipo, usuarios_str = line.split(": ")
                        usuarios = usuarios_str.split("|")
                        equipos[equipo] = usuarios
                    except ValueError:
                        print(f"Formato incorrecto en la línea: {line}")
    except FileNotFoundError:
        pass

# Función para actualizar la lista de usuarios en la interfaz
def actualizar_usuarios():
    # Eliminar los widgets anteriores de los usuarios
    for widget in frame_contenido.winfo_children():
        if widget not in (btn_regresar, btn_añadir_usuario):
            widget.destroy()

    # Actualizar la lista de usuarios en la interfaz
    for equipo, usuarios in equipos.items():
        label_equipo = ttk.Label(frame_contenido, text=equipo, font=("Helvetica", 14, "bold"))
        label_equipo.pack(anchor="w", pady=(10, 0))

        for usuario in usuarios:
            frame_usuario = ttk.Frame(frame_contenido)
            frame_usuario.pack(anchor="w", pady=2)

            label_usuario = ttk.Label(frame_usuario, text=f"• {usuario}", font=("Helvetica", 12))
            label_usuario.pack(side="left", padx=(20, 5))

            btn_mensaje = ttk.Button(frame_usuario, text="MANDAR MENSAJE")
            btn_mensaje.pack(side="left", padx=5)

            if es_administrador:
                btn_sacar = ttk.Button(frame_usuario, text="SACAR", style="Red.TButton", command=lambda e=equipo, u=usuario: eliminar_usuario(e, u))
                btn_sacar.pack(side="left", padx=5)

# Crear la ventana principal
root = tk.Tk()
root.title("Work Manager")
root.geometry("360x640")

# Cargar la imagen y redimensionarla a 20x20 píxeles
image_path = "FON.jpg"
image = Image.open(image_path)
icono = ImageTk.PhotoImage(image)

# Establecer el icono de la ventana
root.iconphoto(False, icono)

# Crear un marco para el encabezado
frame_encabezado = ttk.Frame(root, padding="10 10 10 10")
frame_encabezado.pack(fill="x")

# Cargar la imagen y redimensionarla a 20x20 píxeles
image_path = "FON.jpg"
image = Image.open(image_path)
image = image.resize((20, 20), Image.LANCZOS)
photo = ImageTk.PhotoImage(image)

# Crear un label para la imagen
label_imagen = ttk.Label(frame_encabezado, image=photo)
label_imagen.grid(row=0, column=0, padx=(0, 10))

# Obtener el nombre del usuario
nombre_usuario = cargar_nombre_usuario()

# Crear un label para el mensaje de bienvenida
label_bienvenida = ttk.Label(frame_encabezado, text=f"Bienvenido, {nombre_usuario}")
label_bienvenida.grid(row=0, column=1, sticky="w")

# Crear un marco para el contenido principal
frame_contenido = ttk.Frame(root, padding="10 10 10 10")
frame_contenido.pack(fill="both", expand=True)

# Equipos
equipos = {
    "Equipo 1": ["USUARIO 01", "USUARIO 02", "USUARIO 03", "USUARIO 04"],
    "Equipo 2": ["USUARIO 05", "USUARIO 06", "USUARIO 07", "USUARIO 08"]
}

# Cargar datos desde el archivo
cargar_datos()

# Determinar el rol del usuario
rol_usuario = cargar_rol()
es_administrador = (rol_usuario == "administrador")

# Actualizar la lista de usuarios en la interfaz
actualizar_usuarios()

# Botón para regresar al menú principal
btn_regresar = ttk.Button(frame_contenido, text="REGRESAR AL MENU", command=regresar_a_pag1)
btn_regresar.place(relx=0.5, rely=1.0, anchor="s")

# Crear un estilo para el botón "SACAR"
style = ttk.Style()
style.configure("Red.TButton", foreground="red")

# Botón para añadir un usuario
if es_administrador:
    btn_añadir_usuario = ttk.Button(frame_contenido, text="AÑADIR USUARIO", command=añadir_usuario)
    btn_añadir_usuario.place(relx=0.5, rely=0.95, anchor="s")
    


# Ejecutar la aplicación
root.mainloop()
