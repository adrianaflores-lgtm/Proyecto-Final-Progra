from datetime import datetime

# sistema agua
agua = 0
usada = 0
stock = 0

comunidades = {}
operador = {}
historial = []

def login():
    print("SISTEMA AGUA")
    user = input("user: ")
    passw = input("pass: ")

    if user == "admin" and passw == "1234":
        return "admin"
    elif user == "op" and passw == "1111":
        return "operador"
    elif user == "invitado":
        return "invitado"
    else:
        print("error login")
        return None

def ingresar_agua():
    global agua, stock

    try:
        litros = int(input("litros: "))
        t1 = int(input("tanque1: "))
        t2 = int(input("tanque2: "))

        if t1 + t2 != litros:
            print("no coincide")
            return

        agua = agua + litros
        stock = stock + litros

        print("guardado")
    except:
        print("fallo")

def distribuir(us):
    global stock, usada

    com = input("comunidad: ")

    try:
        litros = int(input("litros a dar: "))

        if litros > stock:
            print("no hay")
            return

        stock = stock - litros
        usada = usada + litros

        if com in comunidades:
            comunidades[com] += litros
        else:
            comunidades[com] = litros

        if us in operador:
            operador[us] += litros
        else:
            operador[us] = litros

        dato = {
            "id": len(historial) + 1,
            "operador": us,
            "comunidad": com,
            "litros": litros,
            "fecha": datetime.now()
        }

        historial.append(dato)

        print("hecho")
        print("stock:", stock)

    except:
        print("error")

def inventario():
    print("\nINVENTARIO")
    print("agua total:", agua)
    print("agua usada:", usada)
    print("stock:", stock)

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
