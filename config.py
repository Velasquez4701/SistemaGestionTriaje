import os

CARPETA_BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_DB = os.path.join(CARPETA_BASE, "datos.json")

ENCABEZADOS_TABLA = [
    "DNI", "Nombre", "Edad", "Sexo", "Peso (Kg)", "Talla (cm)", "IMC", "Clasificacion", "Presion", "Saturacion", "Atencion"
]

MSG_BIENVENIDA = "🏥 SISTEMA DE GESTION DE TRIAJE  - CLINICA SANTA MARIA"
MSG_DESPEDIDA = "✅ Datos guardados correctamente, ¡Gracias por utilizar el sistema! "
