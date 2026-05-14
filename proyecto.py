from datetime import datetime

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
        distribucion = {
            "id": len(historial_distribuciones) + 1,
            "usuario": usuario,
            "comunidad": comunidad,
            "litros": litros,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Agregar registro al historial
        historial_distribuciones.append(distribucion)

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

##Etapa 2

def reporte():
    print("\nREPORTE COMUNIDADES")
    for c in comunidades:
        print(c, comunidades[c])

def ver_historial():
    print("\nHISTORIAL")
    for h in historial:
        print(h["id"], h["comunidad"], h["litros"], h["fecha"])

def borrar():
    global stock, usada

    try:
        idb = int(input("id borrar: "))

        for h in historial:
            if h["id"] == idb:
                stock += h["litros"]
                usada -= h["litros"]
                historial.remove(h)
                print("borrado")
                return

        print("no existe")
    except:
        print("mal dato")

while True:
    rol = login()

    if rol == None:
        continue

    while True:
        print("\nMENU")
        print("1 ingreso")
        print("2 distribucion")
        print("3 inventario")
        print("4 reporte")
        print("5 historial")
        print("6 salir")

        if rol == "admin":
            print("7 borrar")

        op = input("op: ")

        if op == "1":
            if rol == "invitado":
                print("sin permiso")
            else:
                ingresar_agua()

        elif op == "2":
            if rol == "invitado":
                print("sin permiso")
            else:
                distribuir(rol)

        elif op == "3":
            inventario()

        elif op == "4":
            reporte()

        elif op == "5":
            ver_historial()

        elif op == "6":
            print("saliendo")
            break

        elif op == "7" and rol == "admin":
            borrar()

        else:
            print("opcion invalida")

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
