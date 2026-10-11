from datetime import datetime
import os
def registrar_bitacora(mensaje):
    try:
        with open("log.txt", "a", encoding="utf-8") as bitacora:
            tiempo_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            bitacora.write(f"[{tiempo_actual}]{mensaje}\n")
    except Exception as e:
        print(f"error al escribir en la bitacora: {e}")
def cargar_inventario(ruta):
    inventario = []
    categorias = set()
    try:
        if not os.path.exists(ruta):
            with open(ruta, "w", encoding="utf-8-sig") as archivo:
                archivo.write("P01,Laptop HP,4500.00,5,Computadoras\n")
                archivo.write("P02,Mouse,50.00,10,Complementos\n")
            registrar_bitacora("se creo u nuevo archivo de inventario por defetco")
        with open(ruta, "r", encoding="utf-8-sig") as archivo:
            for linea in archivo:
                datos = linea.strip().split(",")
                if len(datos) >= 4:
                    prod = {
                        "ID": datos[0].strip(),
                        "PRODUCTO": datos[1].strip(),
                        "PRECIO": float(datos[2]),
                        "CANTIDAD": int(datos[3]),
                        "CATEGORIA": datos[4].strip() if len(datos) > 4 else "General"
                    }
                    inventario.append(prod)
                    categorias.add(prod["CATEGORIA"])
        registrar_bitacora("Invetario cargado al sistema exitosamente.")
    except Exception as e:
        print(f"Error critico al abrir el inventario: {e}")
        registrar_bitacora(f"Error al cargar inventario: {e}")
    return inventario, categorias
def guardar_inventario(ruta, inventario):
    try:
        with open(ruta, "w", encoding="utf-8-sig") as archivo:
            for prod in inventario:
                linea = f"{prod['ID']},{prod['PRODUCTO']},{prod['PRECIO']},{prod['CANTIDAD']},{prod['CATEGORIA']}\n"
                archivo.write(linea)
        registrar_bitacora("Inventario actualizado y almacenado")
    except Exception as e:
        print("Error al guadar el archivo: {e}")
def buscar_producto(inventario, busqueda):
    busqueda_limpia = busqueda.strip().upper()
    for prod in inventario:
        if prod["ID"].upper() == busqueda_limpia or busqueda_limpia in prod["PRODUCTO"].upper():
             return prod
    return None