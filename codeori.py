import tkinter as tk
from tkinter import ttk
import time
import random
import threading
from tkinter import filedialog, messagebox, simpledialog

admin_dnis = {"71139018": "Jhordan Arostegui Ruiz", "71299475": "Danny Kelvin Espinoza Mariano"}

datos = []

historial = []

def cargar_datos():
    dni_ingresado = simpledialog.askstring("Ingresar DNI", "Ingrese su DNI:")
    if dni_ingresado is None:
        return
    if dni_ingresado in admin_dnis:
        nombre_admin = admin_dnis[dni_ingresado]
        messagebox.showinfo("Acceso de Admin, Correcto", f"ACCESO DE ADMIN, CORRECTO\nADMIN = {nombre_admin}")
        archivo_path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if archivo_path:
            datos.clear()
            with open(archivo_path, "r") as archivo:
                for linea in archivo:
                    partes = linea.strip().split(", ")
                    if len(partes) == 3:
                        id_producto, nombre, stock = partes
                        datos.append({"id": int(id_producto), "nombre": nombre, "stock": int(stock)})
            mostrar_datos()
            agregar_historial(f"Cargar Datos desde Archivo: {archivo_path}")
    else:
        messagebox.showerror("Error de Acceso", "ACCESO DENEGADO: DNI incorrecto.")

def mostrar_datos():
    ventana_datos = tk.Toplevel(ventana)
    ventana_datos.title("Datos Cargados")

    tabla = ttk.Treeview(ventana_datos, columns=("ID", "Nombre", "Stock"), show="headings")
    tabla.heading("ID", text="ID")
    tabla.heading("Nombre", text="Nombre")
    tabla.heading("Stock", text="Stock")
    tabla.pack()

    for producto in datos:
        tabla.insert("", "end", values=(producto["id"], producto["nombre"], producto["stock"]))

    botones_frame = tk.Frame(ventana_datos)
    botones_frame.pack(pady=10)

    botones = [
        {"text": "Ingresar Producto", "command": ingresar_producto},
        {"text": "Eliminar Producto", "command": eliminar_producto},
        {"text": "Actualizar Producto", "command": actualizar_producto},
        {"text": "Buscar Producto", "command": buscar_producto},
        {"text": "Generar Datos Aleatorios", "command": generar_datos_aleatorios},
        {"text": "Ordenar por ID", "command": ordenar_por_id},
        {"text": "Ordenar por Nombre", "command": ordenar_por_nombre},
        {"text": "Ordenar por Stock", "command": ordenar_por_stock},
        {"text": "Mostrar Historial", "command": mostrar_historial}
    ]

    for boton_info in botones:
        boton = tk.Button(botones_frame, text=boton_info["text"], command=boton_info["command"])
        boton.pack(side=tk.LEFT, padx=10)

    boton_guardar["state"] = tk.NORMAL

def agregar_historial(accion):
    fecha_actual = time.strftime("%Y-%m-%d %H:%M:%S")
    historial.append(f"{fecha_actual}: {accion}")

def mostrar_historial():
    ventana_historial = tk.Toplevel(ventana)
    ventana_historial.title("Historial de Acciones")

    historial_text = "\n".join(historial)
    historial_label = tk.Label(ventana_historial, text=historial_text)
    historial_label.pack(padx=20, pady=20)

def ingresar_producto():
    id_producto = simpledialog.askinteger("Ingresar ID", "Ingrese el ID del producto:")
    if id_producto is None:
        return
    if id_producto < 0:
        messagebox.showerror("Error", "El ID del producto no puede ser negativo.")
        return

    for producto in datos:
        if producto["id"] == id_producto:
            messagebox.showerror("Error", "Ya existe un producto con el mismo ID.")
            return

    nombre = simpledialog.askstring("Ingresar Nombre", "Ingrese el nombre del producto:")
    if nombre is None:
        return
    if not nombre.strip():
        messagebox.showerror("Error", "El nombre del producto no puede estar en blanco.")
        return

    stock = simpledialog.askinteger("Ingresar Stock", "Ingrese el stock del producto:")
    if stock is None:
        return
    if stock < 0:
        messagebox.showerror("Error", "El stock del producto no puede ser negativo.")
        return

    datos.append({"id": id_producto, "nombre": nombre, "stock": stock})
    mostrar_datos()
    agregar_historial(f"Ingresar Producto: ID={id_producto}")

def eliminar_producto():
    id_producto = simpledialog.askinteger("Eliminar Producto", "Ingrese el ID del producto que desea eliminar:")
    if id_producto is None:
        return

    producto_encontrado = False

    for producto in datos[:]:
        if producto["id"] == id_producto:
            datos.remove(producto)
            producto_encontrado = True

    if not producto_encontrado:
        messagebox.showerror("Error", f"No se encontró ningún producto con ID {id_producto}")
    else:
        mostrar_datos()
        agregar_historial(f"Eliminar Producto: ID={id_producto}")

def actualizar_producto():
    id_producto = simpledialog.askinteger("Actualizar Producto", "Ingrese el ID del producto que desea actualizar:")
    if id_producto is None:
        return

    for producto in datos:
        if producto["id"] == id_producto:
            nuevo_nombre = simpledialog.askstring("Actualizar Nombre", "Ingrese el nuevo nombre del producto:",
                                                 initialvalue=producto["nombre"])
            if nuevo_nombre is None:
                return
            nuevo_stock = simpledialog.askinteger("Actualizar Stock", "Ingrese el nuevo stock del producto:",
                                                  initialvalue=producto["stock"])
            if nuevo_stock is None:
                return
            producto["nombre"] = nuevo_nombre
            producto["stock"] = nuevo_stock

    mostrar_datos()
    agregar_historial(f"Actualizar Producto: ID={id_producto}")

def buscar_producto():
    id_producto = simpledialog.askinteger("Buscar Producto", "Ingrese el ID del producto que desea buscar:")
    if id_producto is None:
        return

    for producto in datos:
        if producto["id"] == id_producto:
            mostrar_producto_en_ventana(producto)
            return

    messagebox.showinfo("Producto no encontrado", f"No se encontró ningún producto con ID {id_producto}")

def mostrar_producto_en_ventana(producto):
    ventana_producto = tk.Toplevel(ventana)
    ventana_producto.title(f"Producto ID: {producto['id']}")

    etiqueta_nombre = tk.Label(ventana_producto, text=f"Nombre: {producto['nombre']}")
    etiqueta_stock = tk.Label(ventana_producto, text=f"Stock: {producto['stock']}")

    etiqueta_nombre.pack(pady=10)
    etiqueta_stock.pack(pady=10)

def generar_datos_aleatorios():
    cantidad_productos = simpledialog.askinteger("Generar Datos Aleatorios", "Ingrese la cantidad de productos a generar:")
    if cantidad_productos is None:
        return

    for _ in range(cantidad_productos):
        id_producto = random.randint(1, 1000)
        nombre = f"Producto {id_producto}"
        stock = random.randint(1, 100)
        datos.append({"id": id_producto, "nombre": nombre, "stock": stock})

    mostrar_datos()
    agregar_historial(f"Generar Datos Aleatorios: {cantidad_productos} productos")

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i]["id"] < R[j]["id"]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)

def partition(arr, low, high):
    i = low - 1
    pivot = arr[high]

    for j in range(low, high):
        if arr[j]["nombre"] < pivot["nombre"]:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def ordenar_por_id():
    copia_datos = datos.copy()
    start_time = time.time()
    merge_sort(copia_datos)
    elapsed_time_merge = time.time() - start_time

    copia_datos = datos.copy()
    start_time = time.time()
    quick_sort(copia_datos, 0, len(copia_datos) - 1)
    elapsed_time_quick = time.time() - start_time

    mostrar_datos()
    agregar_historial("Ordenar por ID")

    mostrar_tiempo_ordenamiento(elapsed_time_merge, elapsed_time_quick)

def ordenar_por_nombre():
    copia_datos = datos.copy()
    start_time = time.time()
    merge_sort(copia_datos)
    elapsed_time_merge = time.time() - start_time

    copia_datos = datos.copy()
    start_time = time.time()
    quick_sort(copia_datos, 0, len(copia_datos) - 1)
    elapsed_time_quick = time.time() - start_time

    mostrar_datos()
    agregar_historial("Ordenar por Nombre")

    mostrar_tiempo_ordenamiento(elapsed_time_merge, elapsed_time_quick)

def ordenar_por_stock():
    copia_datos = datos.copy()
    start_time = time.time()
    merge_sort(copia_datos)
    elapsed_time_merge = time.time() - start_time

    copia_datos = datos.copy()
    start_time = time.time()
    quick_sort(copia_datos, 0, len(copia_datos) - 1)
    elapsed_time_quick = time.time() - start_time

    mostrar_datos()
    agregar_historial("Ordenar por Stock")

    mostrar_tiempo_ordenamiento(elapsed_time_merge, elapsed_time_quick)

def mostrar_tiempo_ordenamiento(merge_time, quick_time):
    ventana_tiempo = tk.Toplevel(ventana)
    ventana_tiempo.title("Tiempos de Ordenamiento")

    resultado_texto = f"Tiempo de ordenamiento con Merge Sort: {merge_time:.6f} segundos\n"
    resultado_texto += f"Tiempo de ordenamiento con Quick Sort: {quick_time:.6f} segundos"

    resultado_label = tk.Label(ventana_tiempo, text=resultado_texto)
    resultado_label.pack(padx=20, pady=20)

def guardar_datos():
    archivo_path = filedialog.asksaveasfilename(filetypes=[("Archivos de texto", "*.txt")])
    if archivo_path:
        with open(archivo_path, "w") as archivo:
            for producto in datos:
                archivo.write(f"{producto['id']}, {producto['nombre']}, {producto['stock']}\n")
def acerca_de():
    creadores = "Juan David, Alex, Danny, Jhordan"
    facultad = "Facultad FIIS"
    messagebox.showinfo("Acerca de", f"Creadores: {creadores}\nFacultad: {facultad}")
               

ventana = tk.Tk()
ventana.title("Cargar y Ordenar Datos desde Archivo TXT")

boton_cargar = tk.Button(ventana, text="Cargar Datos", command=cargar_datos)
boton_cargar.pack(pady=10)

boton_guardar = tk.Button(ventana, text="Guardar Datos", command=guardar_datos, state=tk.DISABLED)
boton_guardar.pack(pady=10)

boton_quick_sort = tk.Button(ventana, text="Ordenar por ID", command=ordenar_por_id)
boton_quick_sort.pack(pady=10)

boton_merge_sort = tk.Button(ventana, text="Ordenar por Nombre", command=ordenar_por_nombre)
boton_merge_sort.pack(pady=10)

boton_stock_sort = tk.Button(ventana, text="Ordenar por Stock", command=ordenar_por_stock)
boton_stock_sort.pack(pady=10)

# Botón Acerca de
boton_acerca_de = tk.Button(ventana, text="Acerca de", command=acerca_de)
boton_acerca_de.pack(pady=10)

ventana.mainloop()

