import tkinter as tk  # Importa la biblioteca tkinter para la interfaz gráfica 
from tkinter import messagebox  # Importa submódulos específicos de tkinter
from PIL import Image, ImageTk  # Importa módulos de PIL para trabajar con imágenes

precio_por_asiento = 4.50  # Precio por asiento
def cargar_asientos(sala_number, funcion_number):
    # Cargar asientos específicos para cada combinación de sala y función
    if (sala_number, funcion_number) not in asientos_dict:
        asientos_dict[(sala_number, funcion_number)] = [["L" for _ in range(8)] for _ in range(8)]
    return asientos_dict[(sala_number, funcion_number)]


# Función para seleccionar un asiento en una fila y columna específicas
def seleccionar_asiento(row, col):
    if (row, col) not in selected_asientos:
        selected_asientos.append((row, col))
        cambiar_estado_asiento(row, col)  # Cambia el estado solo cuando se selecciona un asiento
    else:
        selected_asientos.remove((row, col))
        if asientos[row][col] == "S":  # Verifica si el asiento estaba seleccionado
            asientos[row][col] = "L"  # Cambia a estado "Libre" si estaba seleccionado previamente
        actualizar_interfaz()  # Actualiza la interfaz después de deseleccionar un asiento


# Función para cambiar el estado de un asiento específico
def cambiar_estado_asiento(row, col):
    estado_actual = asientos[row][col]
    if estado_actual == "L":
        asientos[row][col] = "S"
    actualizar_interfaz()  # Actualiza la interfaz después de cambiar el estado del asiento

# Función para reservar los asientos seleccionados
def reservar_asiento():
    global precio_por_asiento
    if selected_asientos:
        costo_total = len(selected_asientos) * precio_por_asiento  # Calcular costo total
        for (row, col) in selected_asientos:
            if asientos[row][col] == "S":
                asientos[row][col] = "O"
        selected_asientos.clear()
        actualizar_interfaz()
        messagebox.showinfo("Reservar Asiento", f"Los asientos seleccionados han sido reservados. Costo Total: ${costo_total:.2f}")
    else:
        messagebox.showwarning("seleccione uno o más asientos.")


def actualizar_interfaz():
    for i in range(8):
        for j in range(8):
            estado = asientos[i][j]
            color = "green" if estado == "L" else "orange" if estado == "S" else "red" if estado == "O" else "yellow" if estado == "M" else "gray"  # Añade un caso para el mejor asiento (estado "M")
            botones[i][j].config(text=estado, bg=color)


def mostrar_mejores_asientos():
    filas = len(asientos)
    columnas = len(asientos[0])
    centro_fila = filas // 2
    centro_columna = columnas // 2
    letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Lista de letras para las filas

    mejores_asientos = sorted(
        [(i, j) for i in range(filas) for j in range(columnas) if asientos[i][j] == "L"],
        key=lambda x: (abs(centro_fila - x[0]), abs(centro_columna - x[1]))
    )

    if mejores_asientos:
        row, col = mejores_asientos[0]
        asientos[row][col] = "M"  # Marcar el asiento como "Mejor"
        actualizar_interfaz()

        fila_letra = letras[row]
        respuesta = messagebox.askyesno("Mejores Asientos", f"El mejor asiento disponible está en el asiento {fila_letra}{col + 1}. ¿Desea reservarlo?")

        if respuesta:
            asientos[row][col] = "O"  # Reservar el asiento si la respuesta es sí
            actualizar_interfaz()
            costo_total = precio_por_asiento  # El mejor asiento tiene un solo costo
            messagebox.showinfo("Reservar Asiento", f"El asiento {fila_letra}{col + 1} ha sido reservado como el mejor asiento. Costo Total: ${costo_total:.2f}")
        else:
            asientos[row][col] = "L"  # Liberar el asiento si la respuesta es no

        actualizar_interfaz()
    else:
        messagebox.showinfo("Mejores Asientos", "No hay asientos disponibles.")


def volver_a_principal():
    # Declara asientos_window como una variable global para poder acceder a ella y modificarla.
    global asientos_window
    # Verifica si la ventana de selección de asientos está actualmente abierta.  
    if asientos_window:  
        # Cierra (destruye) la ventana de selección de asientos.
        asientos_window.destroy()
        # Establece la variable asientos_window a None para indicar que la ventana ya no está abierta.  
        asientos_window = None  


# Función para abrir la ventana de selección de asientos
def abrir_ventana():
    global asientos, selected_asientos, botones, asientos_window, sala_number, funcion_number, fondo_photo

    sala_number = selected_sala.get()
    funcion_number = selected_hora.get()
    if not sala_number.strip():
        messagebox.showerror("Error", "Por favor, seleccione una sala antes de continuar.")
    elif not funcion_number.strip():
        messagebox.showerror("Error", "Por favor, seleccione una hora antes de continuar.")
    else:
        asientos = cargar_asientos(sala_number, funcion_number)
        selected_asientos = []
        asientos_window = tk.Toplevel(root)
        asientos_window.title(f"Simulador de Asientos - Sala {sala_number} - Función {funcion_number}")

        asientos_window.geometry("650x600")
        asientos_window.resizable(False, False)  # Para deshabilitar el redimensionamiento
        
        # Establecer el foco en la ventana de selección de asientos
        asientos_window.grab_set()  # Evitar que la ventana principal recupere el foco

        fondo_path = r"C:\Users\EQUIPO\Pictures\FondoReserva.jpg"
        fondo_image = Image.open(fondo_path)
        fondo_image = fondo_image.resize((650, 600))  # Ajustar el tamaño del fondo
        fondo_photo = ImageTk.PhotoImage(fondo_image)

        fondo_label = tk.Label(asientos_window, image=fondo_photo)
        fondo_label.place(x=0, y=0, relwidth=1, relheight=1)  # Colocar el fondo en toda la ventana

        letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        # Crear etiquetas para los números de las columnas
        for j in range(8):
            columna_label = tk.Label(asientos_window, text=str(j+1), font=("Arial", 10), bg="white")
            columna_label.place(x=100 + j*60, y=40, width=60, height=20)

        # Crear etiquetas para las letras de las filas
        for i, letra in enumerate(letras[:8]):
            fila_label = tk.Label(asientos_window, text=letra, font=("Arial", 10), bg="white")
            fila_label.place(x=40, y=100 + i*50, width=20, height=50)
        libre_label = tk.Label(asientos_window, text="Libre", font=("Arial", 10, "bold"),bg="gray10",fg="white")
        libre_label.place(x=110, y=550, width=60, height=20)

        ocupado_label = tk.Label(asientos_window, text="Ocupado", font=("Arial", 10, "bold"), bg="gray10",fg="white")
        ocupado_label.place(x=200, y=550, width=60, height=20)

        seleccionado_label = tk.Label(asientos_window, text="Seleccionado", font=("Arial", 10, "bold"), bg="gray10",fg="white")
        seleccionado_label.place(x=300, y=550, width=90, height=20)

        libre_color = tk.Label(asientos_window, bg="green")
        libre_color.place(x=100, y=555, width=10, height=10)

        ocupado_color = tk.Label(asientos_window, bg="red")
        ocupado_color.place(x=190, y=555, width=10, height=10)

        seleccionado_color = tk.Label(asientos_window, bg="orange")
        seleccionado_color.place(x=290, y=555, width=10, height=10)
        botones = []

        for i in range(8):
            fila_botones = []
            for j in range(8):
                estado = asientos[i][j]
                color = "green" if estado == "L" else "orange" if estado == "S" else "red"
                boton = tk.Button(asientos_window, text=estado, bg=color, width=4, height=2,
                                  command=lambda row=i, col=j: seleccionar_asiento(row, col))
                boton.place(x=100 + j*60, y=100 + i*50, width=50, height=40)

                fila_botones.append(boton)
            botones.append(fila_botones)
                

        reservar_btn = tk.Button(asientos_window, text="Reservar Asiento", font=("Georgia", 10, "bold"), command=reservar_asiento, bg="orange")
        reservar_btn.place(x=100, y=500, width=150, height=30)

        mejores_asientos_btn = tk.Button(asientos_window, text="Mejores Asientos", font=("Georgia", 10, "bold"),command=mostrar_mejores_asientos, bg="orange")
        mejores_asientos_btn.place(x=280, y=500, width=150, height=30)
        
        volver_btn = tk.Button(asientos_window, text="Volver", font=("Georgia", 10, "bold"), command=asientos_window.destroy, bg="tomato2")
        volver_btn.place(x=470, y=500, width=100, height=30)


# Diccionario que contiene descripciones de las películas
descripciones_peliculas = {
    "1": "Título: Scream\nGénero: Terror\nEdad: +18\nDuración: 1:51 minutos",
    "2": "Título: WhiteChicks\nGénero: Comedia\nEdad: +13\nDuración: 1:49 minutos",
    "3": "Título: The NoteBook\nGénero: Romance/Drama\nEdad: +13\nDuración: 2:03 minutos",
    "4": "Título: El Rey León\nGénero: Animación\nEdad: Todos\nDuración: 1:58 minutos",
    "5": "Título: John Wick 3\nGénero: Acción\nEdad: +18\nDuración: 2:10 minutos"
}

# Función para actualizar la imagen de la película seleccionada
def actualizar_pelicula_imagen():
    # Obtener la hora seleccionada
    hora = selected_hora.get()
    # Obtener la descripción de la película correspondiente a la hora seleccionada
    descripcion = descripciones_peliculas.get(hora, "")
    
    # Verificar la hora seleccionada y asignar la ruta de la imagen correspondiente
    if hora == "1":
        pelicula_image_path = r"C:\Users\EQUIPO\Pictures\peli1.jpeg"
    elif hora == "2":
        pelicula_image_path = r"C:\Users\EQUIPO\Pictures\peli2.jpeg"
    elif hora == "3":
        pelicula_image_path = r"C:\Users\EQUIPO\Pictures\peli3.jpeg"
    elif hora == "4":
        pelicula_image_path = r"C:\Users\EQUIPO\Pictures\peli4.jpeg"
    elif hora == "5":
        pelicula_image_path = r"C:\Users\EQUIPO\Pictures\peli5.jpeg"
    else:
        # Si la hora no es válida, eliminar la imagen de la etiqueta
        pelicula_label.config(image=None)
        pelicula_image_path = None
    
    # Si se ha encontrado la ruta de la imagen de la película
    if pelicula_image_path:
        # Abrir la imagen de la película
        pelicula_image = Image.open(pelicula_image_path)
        # Redimensionar la imagen a 140x150 píxeles
        pelicula_image = pelicula_image.resize((140, 150))
        # Convertir la imagen en un objeto PhotoImage
        pelicula_photo = ImageTk.PhotoImage(pelicula_image)
        # Configurar la imagen de la etiqueta pelicula_label con la nueva imagen
        pelicula_label.config(image=pelicula_photo)
        # Guardar una referencia al objeto PhotoImage en la etiqueta pelicula_label
        pelicula_label.image = pelicula_photo  
        # Colocar la etiqueta pelicula_label en una posición relativa dentro de la ventana
        pelicula_label.place(relx=0.4, rely=0.5)
        # Configurar el texto de la etiqueta descripcion_label con la descripción de la película
        descripcion_label.config(text=descripcion)
        # Colocar la etiqueta descripcion_label en una posición relativa dentro de la ventana
        descripcion_label.place(relx=0.4, rely=0.8)
    else:
        # Si no se encontró la ruta de la imagen de la película, eliminar la imagen de la etiqueta
        pelicula_label.config(image=None)


# Función para salir de la aplicación
def salir():
    root.destroy()


# Función principal que configura la ventana principal de la aplicación
def main():
    # Declarar variables globales para usarlas en toda la aplicación
    global selected_sala, selected_hora, pelicula_label, descripcion_label, root, asientos_dict

    # Crear la ventana principal de la aplicación
    root = tk.Tk()
    root.title("Interfaz de CINE")  # Título de la ventana
    root.geometry("800x550")  # Tamaño de la ventana
    root.resizable(False, False)  # Para deshabilitar el redimensionamiento

    # Inicializar el diccionario para almacenar los asientos de cada combinación de sala y función
    asientos_dict = {}

    # Cargar la imagen de fondo
    bg_image_path = r"C:\Users\EQUIPO\Pictures\FONDO.jpeg"  # Ruta de la imagen de fondo

    # Abrir y ajustar el tamaño de la imagen de fondo
    bg_image = Image.open(bg_image_path)
    bg_image = bg_image.resize((800, 550))
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Crear un canvas para colocar la imagen de fondo
    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Asignar la imagen de fondo al canvas para que no se elimine con la recolección de basura
    canvas.image = bg_photo

    # Etiqueta para el título de "Funciones"
    funciones_label = tk.Label(root, text="Funciones", font=("Georgia", 24, "bold"), bg="gray10", fg="red")
    funciones_label.place(relx=0.1, rely=0.4)

    # Lista de opciones de horarios de funciones y su valor correspondiente
    horas = [("10:00 am", 1), ("13:00 pm", 2), ("16:00 pm", 3), ("8:00 pm", 4), ("11:00 pm", 5)]
    selected_hora = tk.StringVar(value=" ")  # Variable para almacenar la hora seleccionada

    # Crear botones de radio para cada horario de función
    for hora, value in horas:
        rb = tk.Radiobutton(root, text=hora, variable=selected_hora, value=str(value), bg="gray10", activebackground="orange", font=("Georgia", 16), fg="white", selectcolor="black", command=actualizar_pelicula_imagen)
        rb.place(relx=0.1, rely=0.5 + (value - 1) * 0.1)

    # Etiqueta para el título de "Sala"
    sala_label = tk.Label(root, text="Sala", font=("Georgia", 24, "bold"), bg="gray10", fg="red")
    sala_label.place(relx=0.7, rely=0.4)

    # Lista de opciones de salas y su valor correspondiente
    salas = [("Sala 1", 1), ("Sala 2", 2), ("Sala 3", 3)]
    selected_sala = tk.StringVar(value=" ")  # Variable para almacenar la sala seleccionada

    # Crear botones de radio para cada sala
    for sala, value in salas:
        rb = tk.Radiobutton(root, text=sala, variable=selected_sala, value=str(value), bg="gray10", activebackground="orange", font=("Georgia", 16), fg="white", selectcolor="black")
        rb.place(relx=0.7, rely=0.5 + (value - 1) * 0.1)

    # Etiqueta para el título de "Película"
    funciones_label = tk.Label(root, text="Película", font=("Georgia", 24, "bold"), bg="gray10", fg="red")
    funciones_label.place(relx=0.4, rely=0.4)

    # Etiqueta para mostrar la imagen de la película seleccionada
    pelicula_label = tk.Label(root, bg="gray10")
    pelicula_label.place(relx=0.4, rely=0.5)

    # Etiqueta para mostrar la descripción de la película seleccionada
    descripcion_label = tk.Label(root, bg="gray10", fg="white", font=("Georgia", 12))
    descripcion_label.place(relx=0.7, rely=0.7)

    # Botón para seleccionar la combinación de sala y función y abrir la ventana de selección de asientos
    otro_boton = tk.Button(root, text="Seleccionar", command=abrir_ventana, bg="gold3", font=("Georgia", 12))
    otro_boton.place(relx=0.7, rely=0.8)

    # Botón para salir de la aplicación
    salir_btn = tk.Button(root, text="Salir Programa", command=root.destroy, bg="tomato2", font=("Georgia", 12))
    salir_btn.place(relx=0.7, rely=0.9)

    # Iniciar el bucle principal de la aplicación
    root.mainloop()


# Ejecuta la función principal si el script es ejecutado directamente
if __name__ == "__main__":
    main()
