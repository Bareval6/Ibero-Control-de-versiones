import tkinter as tk
from tkinter import messagebox

# Función para manejar el registro de usuarios
def registrar_usuario():
    nombre = entrada_nombre.get()
    correo = entrada_correo.get()
    contraseña = entrada_contraseña.get()
    
    if nombre and correo and contraseña:
        # Simulando el registro (puedes guardarlo en una base de datos o archivo)
        with open("usuarios_registrados.txt", "a") as archivo:
            archivo.write(f"{nombre},{correo},{contraseña}\n")
        messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
        # Limpiar los campos
        entrada_nombre.delete(0, tk.END)
        entrada_correo.delete(0, tk.END)
        entrada_contraseña.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Formulario de Registro")
ventana.geometry("300x250")

# Etiqueta y campo para el nombre
etiqueta_nombre = tk.Label(ventana, text="Nombre:")
etiqueta_nombre.pack(pady=5)
entrada_nombre = tk.Entry(ventana)
entrada_nombre.pack(pady=5)

# Etiqueta y campo para el correo
etiqueta_correo = tk.Label(ventana, text="Correo:")
etiqueta_correo.pack(pady=5)
entrada_correo = tk.Entry(ventana)
entrada_correo.pack(pady=5)

# Etiqueta y campo para la contraseña
etiqueta_contraseña = tk.Label(ventana, text="Contraseña:")
etiqueta_contraseña.pack(pady=5)
entrada_contraseña = tk.Entry(ventana, show="*")
entrada_contraseña.pack(pady=5)

# Botón para registrar al usuario
boton_registrar = tk.Button(ventana, text="Registrar", command=registrar_usuario)
boton_registrar.pack(pady=20)

# Iniciar el bucle de la interfaz gráfica
ventana.mainloop()
