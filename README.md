# Proyecto-Final-Progra
# Sistema de gestión y distribución de agua para comunidades rurales de Guatemala
## Integrantes
- Nahomy Duarte
- Adriana Flores
- Josue Argeda

Curso: Fundamentos de Programación - Sección C
Universidad Francisco Marroquín
2026

---

# Descripción del Proyecto
Este proyecto consiste en un sistema desarrollado en Python para la gestión y distribución de agua en comunidades rurales de Gautemala afectadas por escasez hídrica, especialmente en zonas del correcor seco como Chiquimula, Jocotán, Camotán y Olopa.

En muchas comunidades rurales, la distribución de agua se realiza manualmente, sin controles digitales claros sobre: 
- Cuánta agua se recibe
- Cuánto se distribuye.
- Qué comunidades reciben más agua.
- Quién realiza las entregas.
- Cuántos recurso queda disponible.

Este proyecto consiste en un sistema desarrollado en Python que permite registrar el ingreso y distribución de agua en comunidades rurales, controlar el inventario disponible y generar reportes básicos.

---

# ¿Qué hace el programa?
El sistema permite:
- Registar agua recibida.
- Distribuir agua a comunidades
- Consultar inventario disponible.
- Generar reportes por comunidad.
- Generar reportes por operador.
- Ver historial de distribuciones.
- Corregir registros erróneos.
- Guardar automáticamente la información en archivos JSON.

---

# Instalación
## Requisitos
Tener instalado Python 3.
Verificar instalación:
```bash
python --version
```

---

# Cómo ejecutar el programa
1. Descargar o clonar el repositorio.
2. Abrir la carpeta del proyecto.
3. Ejecutar el siguiente comando:
```bash
python main.py
```
El programa iniciará mostrando la pantalla de login.

---

# Uso del Sistema
## Credenciales
### Administrados
Usuario:
```text
admin
```

Contraseña:
```text
1234
```

### Operador 1
Usuario:
```text
operador1
```

Contraseña:
```text
1111
```

### Operador 2
Usuario:
```text
operador2
```

Contraseña:
```text
2222
```

### Invitado
Usuario:
```text
invitado
```

Contraseña:
```text
0000
```

---

# Ejemplo de Uso
## Registrar ingreso de agua
```text
Total de litros recibidos: 5000
```

Resultado:
```text
=== INGRESO REGISTRADO ===
Fuente: Donación
Litros recibidos: 5000
Agua disponible actual: 5000 litros
```

---

## Resgistrar distribución de agua
```text
Seleccione la comunidad: 1
Litros a distribuir: 1000
```

Resultado:
```text
=== DISTRIBUCIÓN REGISTRADA ===
Comunidad: Jocotán
Litros distribuidos: 1000
Operador: operador1
Litros restantes: 4000
```

---

# Estructura del proyecto
```text
proyecto-final/
│
├── main.py
├── datos_agua.json
└── README.md
```

---

# Ejemplo de Docstring
```python
def consultar_inventario():
    """
    Muestra el inventario actual de agua disponible,
    agua recibida y agua distribuida.
    """
```

# Conclusión
Este proyecto permite mejorar el control y la organización de la distribución de agua en comunidades rurales mediante un sistema desarrollado en Python. Además de resolver un problema real, el proyecto aplica conceptos fundamentales de programación, como funciones, estructuras de control, manejo de archivos JSON y manejo de errores.






























