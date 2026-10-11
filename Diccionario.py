from operaciones import cargar_inventario, guardar_inventario, buscar_producto, registrar_bitacora
from datetime import datetime
RUTA_INVENTARIO = r"C:\Users\Usuario\OneDrive\Documents\Mi_Proyecto\Inventario.txt"
MINIMO_STOCK_ALERTA = 3
mi_inventario, catergorias_set = cargar_inventario(RUTA_INVENTARIO)
print("su inventario se ha cargado exitosamente")
ventas_del_dia = []
while True:
    print("\n=====================================")
    print("            TECNOLOGIA ALEX           ")
    print("======================================")
    print("Bienvenidos al sistema de gestion de la empresa Tecnologia Alex, seleccion  la opcion a realiar")
    print("1- Agregar un nuevo producto al inventario")
    print("2- Buscar un producto, por NOMBRE o ID")
    print("3- Realizar un venta con validacion de stock")
    print("4- Mostrar el inventario completo y ordenado")
    print("5- Generar reporte de ventas del día")
    print("6- Salir del programa guardando cambios")
    try:
        opcion = input("\nSeleccione una opcion (1-6): ").strip()
        if opcion == "1":
            print("\n---AGREGAR UN NUEVO PRODUCTO AL INVENTARIO---")
            nuevo_id = input("Ingrese el codigo del producto (ej. P01): ").strip()
            if buscar_producto(mi_inventario, nuevo_id):
                print("Error: ya existe un producto con ese codigo.")
            else:
                nombre = input("Ingrese el nombre del producto tecnologico: ").strip()
                categoria = input("Ingrese la carterogia entre: (Computadora, Accesorio, Impresora, Gamer)").strip()
                try:
                    precio = float(input("Ingrese el precio (Q.): "))
                    cantidad = int(input("Ingrese la cantidad de producto que ingresara"))
                    nuevo_prod = {
                        "ID": nuevo_id,
                        "PRODUCTO": nombre,
                        "PRECIO": precio,
                        "CANTIDAD": cantidad,
                        "CATEGORIA": categoria if categoria else "General"
                    }
                    mi_inventario.append(nuevo_prod)
                    catergorias_set.add(nuevo_prod["CATEGORIA"])
                    guardar_inventario(RUTA_INVENTARIO, mi_inventario)
                    registrar_bitacora(f"Producto agregado, {nuevo_id} - {nombre}")
                    print("PRODUCTO NUEVO AGRAGADO AL INVETARIO EXITOSAMENTE")
                except ValueError:
                    print("Error: el precio y la cantidada deben de ser valores numericos")
        elif opcion == "2":
            print("\n ==BUSQUEDA DE PRODUCTO== ")
            termino = input("Ingrese el codigo o nombre del producto a buscar")
            encontrado = buscar_producto(mi_inventario, termino)
            if encontrado is None:
                print("X el producto a consultar no existe en el inventario")
            else:
                print("\n==DETALLE DEL PRODUCTO==")
                print(f"CODIGO     : {encontrado['ID']}")
                print(f"PRODUCTO   : {encontrado['PRODUCTO']}")
                print(f"PRECIO     : Q.{encontrado['PRECIO']:2f}")
                print(f"CANTIDAD   : {encontrado['CANTIDAD']} unidades")
                print(f"CATEGORIA  : {encontrado['CATEGORIA']}")
            if encontrado['CANTIDAD'] == 0:
                print("ALERTA: el producto esta Agotado (Stock en 0).")
            elif encontrado['CANTIDAD'] <= MINIMO_STOCK_ALERTA:
                print(f"AVISO: quedan pocas cantidad (<= {MINIMO_STOCK_ALERTA}). Realiza compra del producto pronto")
        elif opcion == "3":
            print("\n ==REGISTRAR VENTA== ")
            termino = input("Ingrese el código o nombre del producto a vender: ")
            encontrado = buscar_producto(mi_inventario, termino)
            if encontrado is None:
                print("Error: Producto no encontrado.")
            else:
                print(f"Producto: {encontrado['PRODUCTO']} | Stock disponible: {encontrado['CANTIDAD']}")
                try:
                    cant_venta = int(input("Ingrese la cantidad a vender: "))
                    if cant_venta <= 0:
                        print("La cantidad debe ser mayor a cero.")
                    elif cant_venta > encontrado["CANTIDAD"]:
                        print("Error: Stock insuficiente para completar la venta.")
                    else:
                        encontrado["CANTIDAD"] -= cant_venta
                        total_venta = cant_venta * encontrado["PRECIO"]
                        fecha_hora_venta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        registro_venta = (fecha_hora_venta, encontrado["ID"], encontrado["PRODUCTO"], cant_venta, total_venta)
                        ventas_del_dia.append(registro_venta)
                        guardar_inventario(RUTA_INVENTARIO, mi_inventario)
                        registrar_bitacora(f"Venta registrada: {cant_venta} unidades de {encontrado['PRODUCTO']} por Q{total_venta:.2f}")
                        print(f"¡Venta exitosa! Total a pagar: Q{total_venta:.2f}")
                        print(f"Stock restante: {encontrado['CANTIDAD']} unidades.")
                        if encontrado['CANTIDAD'] <= MINIMO_STOCK_ALERTA:
                            print(f"AVISO: El producto ha quedado en nivel de stock mínimo ({encontrado['CANTIDAD']} unidades).")
                except ValueError:
                    print(" Error: Ingrese un número entero válido.")
        elif opcion == "4":
            print("\n ==INVENTARIO COMPLETO ORDENADO== ")
            print("¿Cómo desea ordenar el reporte?")
            print("1. Por Nombre del producto")
            print("2. Por Precio (de menor a mayor)")
            sub_op = input("Seleccione criterio (1 o 2): ").strip()
            if sub_op == "1":
                inventario_ordenado = sorted(mi_inventario, key=lambda x: x["PRODUCTO"])
            elif sub_op == "2":
                inventario_ordenado = sorted(mi_inventario, key=lambda x: x["PRECIO"])
            else:
                print("Opción no válida, se mostrará sin ordenar.")
                inventario_ordenado = mi_inventario
            print("\n" + "="*70)
            print(f"{'CÓDIGO':<8} | {'PRODUCTO':<20} | {'CATEGORÍA':<12} | {'PRECIO':<10} | {'STOCK':<6}")
            print("="*70)
            for p in inventario_ordenado:
                alerta = "[MÍNIMO]" if p['CANTIDAD'] <= MINIMO_STOCK_ALERTA else ""
                print(f"{p['ID']:<8} | {p['PRODUCTO']:<20} | {p['CATEGORIA']:<12} | Q{p['PRECIO']:<9.2f} | {p['CANTIDAD']:<6}{alerta}")
            print("="*70)
        elif opcion == "5":
            print("\n==========================================================")
            print("               REPORTE DE VENTAS DEL DÍA                  ")
            print("==========================================================")
            if not ventas_del_dia:
                print("No se han registrado ventas en esta sesión.")
            else:
                print(f"{'FECHA/HORA':<20} | {'CÓDIGO':<8} | {'PRODUCTO':<18} | {'CANT':<5} | {'TOTAL':<8}")
                print("-" * 70)
                total_recaudado = 0
                for v in ventas_del_dia:
                    print(f"{v[0]:<20} | {v[1]:<8} | {v[2]:<18} | {v[3]:<5} | Q{v[4]:<7.2f}")
                    total_recaudado += v[4]
                print("-" * 70)
                print(f"Total general recaudado hoy: Q{total_recaudado:.2f}")
            print("==========================================================")
        elif opcion == "6":
            guardar_inventario(RUTA_INVENTARIO, mi_inventario)
            registrar_bitacora("Cierre de sesión del sistema.")
            break
        else:
            print("\nOpción no válida. Por favor elija un número del 1 al 6.")
    except Exception as e:
        print(f"Ocurrió un error inesperado en el sistema: {e}")
