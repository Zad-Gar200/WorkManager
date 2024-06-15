import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from PIL import Image, ImageTk

# Configuración de la base de datos MySQL
Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://root@localhost:3306/usuarios')
Session = sessionmaker(bind=engine)
session = Session()

# Definición de la tabla Usuarios
class Usuario(Base):
    __tablename__ = 'Usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    nombre_usuario = Column(String(255), nullable=False)
    contraseña = Column(String(255), nullable=False)
    tipo = Column(String(50), nullable=False)
    rol = Column(String(50))
    imagen = Column(String(255), nullable=True)

Base.metadata.create_all(engine)

# Funciones de la aplicación
def registrar():
    email = entry_email.get()
    nombre_usuario = entry_nombre_usuario.get()
    contraseña = entry_contraseña.get()
    tipo = tipo_var.get()
    rol = rol_var.get()
    imagen = imagen_var.get()

    if not email or not nombre_usuario or not contraseña or not tipo or not rol:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
        return

    if session.query(Usuario).filter_by(email=email).first():
        messagebox.showwarning("Advertencia", "El correo electrónico ya está registrado.")
        return

    nuevo_usuario = Usuario(
        email=email,
        nombre_usuario=nombre_usuario,
        contraseña=contraseña,
        tipo=tipo,
        rol=rol,
        imagen=imagen
    )
    session.add(nuevo_usuario)
    session.commit()

    messagebox.showinfo("Éxito", "Usuario registrado con éxito.")
    limpiar_campos()

def iniciar_sesion():
    email = entry_email.get()
    contraseña = entry_contraseña.get()

    usuario = session.query(Usuario).filter_by(email=email, contraseña=contraseña).first()
    if usuario:
        with open("usuario.txt", "w") as file:
            file.write(usuario.nombre_usuario)
        with open("rol.txt", "w") as file:
            file.write(usuario.rol)
        messagebox.showinfo("Éxito", f"Bienvenido, {usuario.nombre_usuario}!")
        root.destroy()  # Cerrar la ventana de Pag0
        import Pag1  # Importar Pag1 y ejecutarlo
    else:
        messagebox.showwarning("Error", "Correo electrónico o contraseña incorrectos.")


def limpiar_campos():
    entry_email.delete(0, tk.END)
    entry_nombre_usuario.delete(0, tk.END)
    entry_contraseña.delete(0, tk.END)
    tipo_var.set("")
    rol_var.set("")
    imagen_var.set("")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Registro e Inicio de Sesión")
root.geometry("600x600")
root.configure(bg="#ccffcc")  # Cambia el color de fondo a un verde claro
root.resizable(False, False)  # No permitir cambiar el tamaño

# Cargar y redimensionar la imagen de encabezado
image_path = "FON.jpeg"  # Ajusta esta línea con la ruta completa si es necesario
header_image = Image.open(image_path)
header_image = header_image.resize((120, 120), Image.LANCZOS)  # Ajusta el tamaño según tu preferencia
header_photo = ImageTk.PhotoImage(header_image)

# Establecer el icono de la ventana
root.iconphoto(False, header_photo)

# Crear un frame para el encabezado
header_frame = tk.Frame(root, bg="#99cc99")  # Color verde más oscuro
header_frame.pack(fill=tk.X, pady=10)

# Crear un Label para la imagen de encabezado y colocarlo en el frame
label_header = tk.Label(header_frame, image=header_photo, bg="#99cc99")
label_header.pack(side=tk.LEFT, padx=10)

# Crear un Label para el texto "Work Manager" y colocarlo en el frame
label_title = tk.Label(header_frame, text="Work Manager", font=("Helvetica", 24), bg="#99cc99")
label_title.pack(side=tk.LEFT, padx=10)

# Variables
tipo_var = tk.StringVar()
rol_var = tk.StringVar()
imagen_var = tk.StringVar()

# Estilo para los Labels
label_style = {'font': ("Helvetica", 12), 'background': "#ccffcc"}

# Widgets
label_email = ttk.Label(root, text="Email:", **label_style)
label_email.pack(pady=5)
entry_email = ttk.Entry(root, font=("Helvetica", 12))
entry_email.pack(pady=5)

label_nombre_usuario = ttk.Label(root, text="Nombre de Usuario:", **label_style)
label_nombre_usuario.pack(pady=5)
entry_nombre_usuario = ttk.Entry(root, font=("Helvetica", 12))
entry_nombre_usuario.pack(pady=5)

label_contraseña = ttk.Label(root, text="Contraseña:", **label_style)
label_contraseña.pack(pady=5)
entry_contraseña = ttk.Entry(root, show="*", font=("Helvetica", 12))
entry_contraseña.pack(pady=5)

label_tipo = ttk.Label(root, text="Tipo:", **label_style)
label_tipo.pack(pady=5)
combo_tipo = ttk.Combobox(root, textvariable=tipo_var, font=("Helvetica", 12))
combo_tipo['values'] = ("educación", "oficio")
combo_tipo.pack(pady=5)

label_rol = ttk.Label(root, text="Rol:", **label_style)
label_rol.pack(pady=5)
combo_rol = ttk.Combobox(root, textvariable=rol_var, font=("Helvetica", 12))
combo_rol['values'] = ("profesor", "estudiante", "administrador", "trabajador")
combo_rol.pack(pady=5)

button_registrar = ttk.Button(root, text="Registrar", command=registrar, width=20)
button_registrar.pack(pady=20)

button_iniciar_sesion = ttk.Button(root, text="Iniciar Sesión", command=iniciar_sesion, width=20)
button_iniciar_sesion.pack(pady=10)

# Ejecución de la aplicación
root.mainloop()
