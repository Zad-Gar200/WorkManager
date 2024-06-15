import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from PIL import Image, ImageTk
import datetime
import Pag1  # Importar Pag1 para actualizar los trabajos

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
    trabajos = relationship('Trabajo', back_populates='usuario')

# Definición de la tabla Trabajos
class Trabajo(Base):
    __tablename__ = 'trabajos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('Usuarios.id'), nullable=False)
    descripcion = Column(String(255), nullable=False)
    fecha = Column(Date, nullable=True)
    entregado = Column(Integer, default=0)
    usuario = relationship('Usuario', back_populates='trabajos')

Base.metadata.create_all(engine)

# Función para cargar el nombre del usuario
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

# Función para agregar un nuevo trabajo con fecha de entrega a la base de datos
def agregar_trabajo():
    descripcion = entry_trabajo.get()
    fecha = entry_fecha_entrega.get()
    usuario_seleccionado = combobox_usuario.get()

    if not usuario_seleccionado:
        messagebox.showerror("Error", "Por favor, seleccione un usuario.")
        return

    if descripcion:
        try:
            fecha_dt = datetime.datetime.strptime(fecha, "%Y-%m-%d") if fecha else None
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha incorrecto. Utilice YYYY-MM-DD")
            return

        usuario = session.query(Usuario).filter_by(nombre_usuario=usuario_seleccionado).first()
        if usuario:
            nuevo_trabajo = Trabajo(
                usuario_id=usuario.id,
                descripcion=descripcion,
                fecha=fecha_dt,
                entregado=0  # Assuming new tasks are not delivered by default
            )
            session.add(nuevo_trabajo)
            session.commit()
            entry_trabajo.delete(0, tk.END)
            entry_fecha_entrega.delete(0, tk.END)
            messagebox.showinfo("Éxito", "Trabajo agregado correctamente")
            
            # Actualizar los trabajos en la página 1 después de agregar uno nuevo
            Pag1.cargar_trabajos()
        else:
            messagebox.showerror("Error", "Usuario no encontrado.")
    else:
        messagebox.showerror("Error", "Por favor, complete el campo de descripción")

# Crear la ventana principal
root = tk.Tk()
root.title("Pag3 - Admin")

# Establecer el tamaño de la ventana (dimensiones de un celular)
root.geometry("360x640")

# Crear un marco para el encabezado
frame_encabezado = ttk.Frame(root, padding="10 10 10 10")
frame_encabezado.pack(fill="x")

# Cargar la imagen y redimensionarla a 20x20 píxeles
try:
    image_path = "FON.jpg"
    image = Image.open(image_path)
    image = image.resize((20, 20), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)

    # Crear un label para la imagen
    label_imagen = ttk.Label(frame_encabezado, image=photo)
    label_imagen.grid(row=0, column=0, padx=(0, 10))
except FileNotFoundError:
    print("Error: No se encontró la imagen")

# Obtener el nombre del usuario
nombre_usuario = cargar_nombre_usuario()

# Crear un label para el mensaje de bienvenida
label_bienvenida = ttk.Label(frame_encabezado, text=f"Bienvenido, {nombre_usuario}")
label_bienvenida.grid(row=0, column=1, sticky="w")

# Crear un marco para el contenido principal
frame_principal = ttk.Frame(root, padding="10 10 10 10")
frame_principal.pack(fill="both", expand=True)

# Crear los elementos de la interfaz para agregar trabajos
label_trabajo = ttk.Label(frame_principal, text="Trabajo")
label_trabajo.grid(row=0, column=0, padx=5, pady=5)

entry_trabajo = ttk.Entry(frame_principal, width=30)
entry_trabajo.grid(row=0, column=1, padx=5, pady=5)

label_fecha_entrega = ttk.Label(frame_principal, text="Fecha de Entrega (YYYY-MM-DD)")
label_fecha_entrega.grid(row=1, column=0, padx=5, pady=5)

entry_fecha_entrega = ttk.Entry(frame_principal, width=30)
entry_fecha_entrega.grid(row=1, column=1, padx=5, pady=5)

label_usuario = ttk.Label(frame_principal, text="Usuario")
label_usuario.grid(row=2, column=0, padx=5, pady=5)

# Obtener la lista de usuarios de la base de datos
usuarios = session.query(Usuario).all()
usuario_nombres = [usuario.nombre_usuario for usuario in usuarios]

combobox_usuario = ttk.Combobox(frame_principal, values=usuario_nombres)
combobox_usuario.grid(row=2, column=1, padx=5, pady=5)

btn_agregar_trabajo = ttk.Button(frame_principal, text="Agregar Trabajo", command=agregar_trabajo)
btn_agregar_trabajo.grid(row=3, column=0, columnspan=2, pady=10)

# Botón para regresar al menú principal
btn_regresar = ttk.Button(frame_principal, text="REGRESAR AL MENU", command=regresar_a_pag1)
btn_regresar.grid(row=4, column=0, columnspan=2, pady=20)

# Ejecutar la aplicación
root.mainloop()
