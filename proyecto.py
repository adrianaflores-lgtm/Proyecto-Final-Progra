from datetime import datetime
import json

# --- CLASE --- #
class Distribucion:
    def __init__(self, id, usuario, comunidad, litros, fecha):
        self.id = id
        self.usuario = usuario
        self.comunidad = comunidad
        self.litros = litros
        self.fecha = fecha

    def mostrar_resumen(self):
        return (
            f"ID:{self.id} | Operador:{self.usuario} | "
            f"Comunidad:{self.comunidad} | Litros:{self.litros} | "
            f"Fecha:{self.fecha}"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "usuario": self.usuario,
            "comunidad": self.comunidad,
            "litros": self.litros,
            "fecha": self.fecha
        }

# --- VARIABLES GENERALES --- #
# Guardan el estados total del sistema.
agua_recibida_total = 0
agua_distribuida_total = 0
stock_agua = 0

# --- COMUNIDADES DEL SISTEMA --- #
# Agregar esta lista al codigo final basandonos en el departamento de chiquimula.
# Lista de comunidades que pueden recibir agua
comunidades = [
    "Jocotán",
    "Camotán",
    "Olopa",
    "San Juan Ermita",
    "Chiquimula"
]

# --- DICCIONARIOS --- #
distribucion_por_comunidad = {}
consumo_por_operador = {}

# --- HISTORIAL --- #
# Guarda cada entrega con ID, operador, comunidad, litros y fecha.
historial_distribuciones = []

# --- ARCHIVO JSON --- #
ARCHIVO_DATOS = "datos_agua.json"

# --- GUARDAR DATOS --- #
def guardar_datos():
    datos = {
        "agua_recibida_total": agua_recibida_total,
        "agua_distribuida_total": agua_distribuida_total,
        "stock_agua": stock_agua,
        "distribucion_por_comunidad": distribucion_por_comunidad,
        "consumo_por_operador": consumo_por_operador,
        "historial_distribuciones": [d.to_dict() for d in historial_distribuciones]
    }

    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

# --- CARGAR DATOS --- #
def cargar_datos():
    global agua_recibida_total
    global agua_distribuida_total
    global stock_agua
    global distribucion_por_comunidad
    global consumo_por_operador
    global historial_distribuciones

    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

            agua_recibida_total = datos.get("agua_recibida_total", 0)
            agua_distribuida_total = datos.get("agua_distribuida_total", 0)
            stock_agua = datos.get("stock_agua", 0)

            distribucion_por_comunidad = datos.get("distribucion_por_comunidad", {})
            consumo_por_operador = datos.get("consumo_por_operador", {})

            historial_distribuciones = []
            for d in datos.get("historial_distribuciones", []):
                historial_distribuciones.append(
                    Distribucion(
                        d["id"],
                        d["usuario"],
                        d["comunidad"],
                        d["litros"],
                        d["fecha"]
                    )
                )

    except FileNotFoundError:
        print("No existe archivo de datos. Se creará uno nuevo.\n")

    except json.JSONDecodeError:
        print("El archivo JSON está dañado. Se iniciará con datos vacíos.\n")
        agua_recibida_total = 0
        agua_distribuida_total = 0
        stock_agua = 0
        distribucion_por_comunidad = {}
        consumo_por_operador = {}
        historial_distribuciones = []

# --- LOGIN --- #
# Verifica ususario y contraseña.
# Dependiendo de las credenciales se asigna un rol.
def login():
    print("=== SISTEMA DE GESTION DE AGUA ===")
    
    usuario = input("Usuario: ")
    contrasena = input("Contraseña: ")
    # Revisar los accesos de los operadores e invitados.
    if usuario == "admin" and contrasena == "1234":
        print("Acceso administrador\n")
        return "admin"
    elif usuario == "operador1" and contrasena == "1111":
        print("Acceso operador 1\n")
        return "operador1"
    elif usuario == "operador2" and contrasena == "2222":
        print("Acceso operador 2\n")
        return "operador2"
    elif usuario == "invitado" and contrasena == "0000":
        print("Acceso invitado\n")
        return "invitado"
    # Si las credenciales son incorrectas
    else:
        print("Acceso denegado\n")
        return None

# --- INGRESO DE AGUA --- #
# registra agua, actualiza inventario, suma el total recibido.
def ingresar_agua():
    global agua_recibida_total, stock_agua
    
    try:
        cantidad = int(input("Total de litros recibidos: "))
        
        # valida cantidad mayor 0
        if cantidad <= 0:
            print("Debe ser mayor que 0\n")
            return
        # Mostrar fuentes disponibles de ingreso.
        print("\nFuentes de ingreso:")
        print("1. Camión cisterna")
        print("2. Pozo comunitario")
        print("3. Donación")
        print("4. Municipalidad")

        fuente = input("Seleccione la fuente de agua: ")

        # convertir la opcion elegida en nombre de fuente
        if fuente == "1":
            nombre_fuente = "Camión cisterna"
        elif fuente == "2":
            nombre_fuente = "Pozo comunitario"
        elif fuente == "3":
            nombre_fuente = "Donación"
        elif fuente == "4":
            nombre_fuente = "Municipalidad"
        else:
            print("Fuente inválida\n")
            return

        # Actualizar cantidades del sistema
        agua_recibida_total += cantidad
        stock_agua += cantidad

        guardar_datos()

        # Mostrar resumen del ingreso registrado
        print("\n=== INGRESO REGISTRADO ===")
        print(f"Fuente: {nombre_fuente}")
        print(f"Litros recibidos: {cantidad}")
        print(f"Agua disponible actual: {stock_agua} litros\n")

    except ValueError:
        print("Ingrese un número válido\n")

# --- DISTRIBUCION DEL AGUA --- #
# Se encarga de la entrega de agua a las comunidades.
# Actualiza inventario, guarda estadisticas, registra historial.
def registrar_distribucion(usuario):
    global agua_distribuida_total, stock_agua

    # Mostrar comunidades disponibles
    print("\nComunidades disponibles:")
    for i, comunidad in enumerate(comunidades, start=1):
        print(f"{i}. {comunidad}")

    try:
        opcion = int(input("Seleccione la comunidad: "))

        # Validar que la comunidad exista
        if opcion < 1 or opcion > len(comunidades):
            print("Comunidad inválida\n")
            return

        comunidad = comunidades[opcion - 1]

        litros = int(input("Litros a distribuir: "))

        # Validar cantidad positiva
        if litros <= 0:
            print("Cantidad inválida\n")
            return

        # Verificar que exista suficiente agua
        if litros > stock_agua:
            print("No hay suficiente agua disponible")
            print(f"Disponible: {stock_agua} litros\n")
            return
        
        # Actualizar inventario
        stock_agua -= litros
        agua_distribuida_total += litros

        # Guardar litros entregados por comunidad
        if comunidad in distribucion_por_comunidad:
            distribucion_por_comunidad[comunidad] += litros
        else:
            distribucion_por_comunidad[comunidad] = litros

        # Guardad litros distribuidos por operados
        if usuario in consumo_por_operador:
            consumo_por_operador[usuario] += litros
        else:
            consumo_por_operador[usuario] = litros

        # Crear registro de distribucion
        distribucion = Distribucion(
            len(historial_distribuciones) + 1,
            usuario,
            comunidad,
            litros,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        # Agregar registro al historial
        historial_distribuciones.append(distribucion)

        guardar_datos()

        # Mostrar resumen de la distribucion
        print("\n=== DISTRIBUCIÓN REGISTRADA ===")
        print(f"Comunidad: {comunidad}")
        print(f"Litros distribuidos: {litros}")
        print(f"Operador: {usuario}")
        print(f"Litros restantes: {stock_agua}\n")

    except ValueError:
        print("Ingrese un número válido\n")

# --- INVENTARIO --- #
# Muestra el estado actual del agua
def consultar_inventario():
    print("\n=== INVENTARIO DE AGUA ===")
    print(f"Agua recibida total: {agua_recibida_total} litros")
    print(f"Agua distribuida total: {agua_distribuida_total} litros")
    print(f"Agua disponible: {stock_agua} litros\n")

    #Mostrar alertas segun nivel de agua disponible.
    if stock_agua == 0:
        print("Estado: SIN AGUA DISPONIBLE")
    elif stock_agua < 500:
        print("Estado: ALERTA, nivel bajo de agua")
    else:
        print("Estado: Nivel suficiente de agua")

    print("")

# --- REPORTES DE COMUNIDADES ---
# ¿Que comunidad ha recibido más agua?
def reporte_comunidades():
    print("\n=== REPORTE DE AGUA POR COMUNIDAD ===")

    if not distribucion_por_comunidad:
        print("No hay distribuciones registradas\n")
        return

    for comunidad, litros in distribucion_por_comunidad.items():
        print(f"{comunidad}: {litros} litros recibidos")
    print("")

# --- REPORTE DE OPERADORES ---
# ¿Quien fue el responsable de distribuir el agua?
def reporte_operadores():
    print("\n=== REPORTE DE AGUA POR OPERADOR ===")

    if not consumo_por_operador:
        print("No hay registros de distribución por operador\n")
        return

    for operador, litros in consumo_por_operador.items():
        print(f"{operador}: {litros} litros distribuidos")
    print("")

# --- TOTAL DE REPORTE ---
def total_acumulado():
    print("\n=== TOTAL ACUMULADO ===")
    print(f"Total de agua recibida: {agua_recibida_total} litros")
    print(f"Total de agua distribuida: {agua_distribuida_total} litros")
    print(f"Agua disponible actualmente: {stock_agua} litros")

    if agua_recibida_total > 0:
        porcentaje_distribuido = (agua_distribuida_total / agua_recibida_total) * 100
        print(f"Porcentaje de agua distribuida: {porcentaje_distribuido:.2f}%")
    else:
        print("Todavía no se ha registrado ingreso de agua")

    print("")

# --- HISTORIAL ---
# que operador distribuyó agua, a qué comunidad, cuántos litros entregó y en qué fecha.
def ver_historial():
    print("\n=== HISTORIAL DE DISTRIBUCIONES ===")

    if not historial_distribuciones:
        print("No hay distribuciones registradas\n")
        return

    for d in historial_distribuciones:
        print(d.mostrar_resumen())
    print("")

# --- BUSQUEDA RECURSIVA ---
#Busca un registro dentro del historial usando el ID
def buscar_registro_recursivo(historial, id_buscar, indice=0):
    if indice >= len(historial):
        return None

    if historial[indice].id == id_buscar:
        return historial[indice]

    return buscar_registro_recursivo(historial, id_buscar, indice + 1)

# --- CORREGIR REGISTRO DE DISTRIBUCION ---
def borrar_registro():
    global agua_distribuida_total, stock_agua

    print("\n=== CORRECCIÓN REGISTRO DE DISTRIBUCIÓN ===")

    if not historial_distribuciones:
        print("No hay registros para corregir\n")
        return

    try:
        # Mostrar historial antes de borrar
        print("\nDistribuciones registradas:\n")

        for d in historial_distribuciones:
            print(d.mostrar_resumen())

        print("")

        #Pedir ID
        id_buscar = int(input("ID a corregir: "))

        #Buscar el registro usando recursividad
        registro = buscar_registro_recursivo(historial_distribuciones, id_buscar)

        #si no se encuentra el registro
        if registro is None:
            print("No se encontró un registro con ese ID\n")
            return

        # Devolver los litros al inventario
        stock_agua += registro.litros

        # Restar los litros del total distribuido
        agua_distribuida_total -= registro.litros
        # Restar los litros del reporte por comunidad
        distribucion_por_comunidad[registro.comunidad] -= registro.litros

        # Si la comunidad queda con 0 litros, se elimina del diccionario
        if distribucion_por_comunidad[registro.comunidad] <= 0:
            del distribucion_por_comunidad[registro.comunidad]

        # Restar los litros del reporte por operador
        consumo_por_operador[registro.usuario] -= registro.litros

        # Si el operador queda con 0 litros, se elimina del diccionario
        if consumo_por_operador[registro.usuario] <= 0:
            del consumo_por_operador[registro.usuario]

        # Eliminar el registro del historial
        historial_distribuciones.remove(registro)

        # Reordenar IDs para que queden consecutivos
        for i, d in enumerate(historial_distribuciones, start=1):
            d.id = i

        # Guardar los cambios en el archivo JSON
        guardar_datos()

        print("\nRegistro corregido correctamente")
        print(f"Se devolvieron {registro.litros} litros al inventario")
        print(f"Agua disponible actual: {stock_agua} litros\n")

    except ValueError:
        print("Debe ingresar un número válido\n")
        
#Cargar los datos guardados
cargar_datos()

# --- LOOP PRINCIPAL ---
while True:
    rol = login()

    if not rol:
        continue

    while True:
        print("=== MENÚ PRINCIPAL ===")
        print("1. Ingreso de agua")
        print("2. Distribución de agua")
        print("3. Inventario")

        if rol in ["admin", "operador1", "operador2"]:
            print("4. Reporte de agua por comunidad")

        if rol == "admin":
            print("5. Reporte de agua por operador")
            print("6. Total acumulado")
            print("7. Historial de distribución")
            print("8. Corregir registro")
            print("9. Salir")
        else:
            print("9. Salir")

        op = input("Opción: ")

        if op == "1":
            if rol == "invitado":
                print("No tiene permiso para ingresar agua\n")
            else:
                ingresar_agua()

        elif op == "2":
            if rol == "invitado":
                print("No tiene permiso para distribuir agua\n")
            else:
                registrar_distribucion(rol)

        elif op == "3":
            consultar_inventario()

        elif op == "4" and rol in ["admin", "operador1", "operador2"]:
            reporte_comunidades()

        elif op == "5" and rol == "admin":
            reporte_operadores()

        elif op == "6" and rol == "admin":
            total_acumulado()

        elif op == "7" and rol == "admin":
            ver_historial()

        elif op == "8" and rol == "admin":
            borrar_registro()

        elif op == "9":
            print("Cerrando sesión...\n")
            break

        else:
            print("Opción inválida\n")
