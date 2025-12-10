import json
from datetime import datetime

class TriageException(Exception):
    pass

class DniDuplicadoException(TriageException):
    pass

class PacienteNoEncontradoException(TriageException):
    pass

class DniInvalidoException(Exception):
    pass

class ValidadorDni:

    @staticmethod
    def validar(dni):
        if not isinstance(dni, str):
            raise DniInvalidoException("El DNI debe ser una cadena de texto.")

        dni = dni.strip()

        if len(dni) != 8 or not dni.isdigit():
            raise DniInvalidoException(
                "El DNI debe tener exactamente 8 dígitos numéricos."
            )

        return dni

class Persona:

    def __init__(self, dni, nombre, edad, sexo):
        self.dni = dni
        self.nombre = nombre
        self.sexo = sexo
        self.edad = edad

    @property
    def dni(self):
        return self._dni
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def sexo(self):
        return self._sexo
    
    @property
    def edad(self):
        return self._edad
    
    @dni.setter
    def dni(self, valor):
        if not valor.isdigit() or len(valor) != 8:
            raise ValueError("El DNI debe ser un número de 8 dígitos.")
        self._dni = valor

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre debe ser una cadena no vacía.")
        self._nombre = valor.strip().title()

    @sexo.setter
    def sexo(self, valor):
        if valor not in ["Masculino", "Femenino"]:
            raise ValueError("El sexo debe ser 'Masculino' o 'Femenino'.")
        self._sexo = valor

    @edad.setter
    def edad(self, valor):
        if valor < 0:
            raise ValueError("La edad no puede ser negativa.")
        self._edad = valor

class Paciente(Persona):

    def __init__(self, dni, nombre, edad, sexo):
        super().__init__(dni, nombre, edad, sexo)
        self.fecha_registro = datetime.now().strftime("%d-%m-%Y %H:%M")
        self._lista_atencion_triaje = []

    @property
    def fecha_registro(self):
        return self._fecha_registro

    @fecha_registro.setter
    def fecha_registro(self, valor):
        self._fecha_registro = valor

    @property
    def lista_atencion_triage(self):
        return self._lista_atencion_triaje

    @lista_atencion_triage.setter
    def lista_atencion_triage(self, valor):
        self._lista_atencion_triaje = valor

    def agregar_atencion(self, atencion):
        self._lista_atencion_triaje.append(atencion)

    def obtener_atenciones(self):
        return self._lista_atencion_triaje

    def obtener_ultima_atencion(self):
        return self._lista_atencion_triaje[-1] if self._lista_atencion_triaje else None

    def clasificar_atencion(self, atencion):
        raise NotImplementedError("Debe implementarse en las subclases.")

    def to_dict(self):
        return {
            "dni": self.dni,
            "nombre": self.nombre,
            "edad": self.edad,
            "sexo": self.sexo,
            "fecha_registro": self._fecha_registro,
            "atenciones": [a.to_dict() for a in self._lista_atencion_triaje]
        }

class PacienteEstandar(Paciente):

    def clasificar_atencion(self, atencion):
        es_urgente = (
            atencion.presion < 90 or atencion.presion > 180 or
            atencion.frecuencia > 100 or
            atencion.saturacion < 92 or
            atencion.conciencia != "Alerta"
        )

        atencion.nivel_atencion = "Urgente" if es_urgente else "Normal"
        return atencion.nivel_atencion
    

class PacienteAdultoMayor(Paciente):

    def clasificar_atencion(self, atencion):
        es_urgente = (
            atencion.presion < 100 or atencion.presion > 160 or
            atencion.frecuencia < 55 or atencion.frecuencia > 110 or
            atencion.saturacion < 94 or
            atencion.conciencia != "Alerta"
        )

        atencion.nivel_atencion = "Urgente" if es_urgente else "Normal"
        return atencion.nivel_atencion
    

class AtencionTriage:
    def __init__(self, peso, talla, presion, frecuencia, conciencia, saturacion):
        self.peso = peso
        self.talla = talla
        self.presion = presion
        self.frecuencia = frecuencia
        self.conciencia = conciencia
        self.saturacion = saturacion

        self._imc = 0.0
        self._clasificacion_imc = ""
        self._nivel_atencion = ""
        self._fecha_registro = datetime.now().strftime("%d-%m-%Y %H:%M") 

        self.calcular_imc()

    @property
    def peso(self):
        return self._peso

    @peso.setter
    def peso(self, valor):
        if not (0 <= valor <= 200):
            raise ValueError("El peso debe estar entre 0 y 200 kg.")
        self._peso = valor

    @property
    def talla(self):
        return self._talla

    @talla.setter
    def talla(self, valor):
        # Detectar si están usando metros en lugar de centímetros
        if 0 < valor < 100:
            raise ValueError(
                "La talla debe estar en centímetros (100-250 cm). "
                "¿Ingresó en metros por error?"
            )
        if not (100 <= valor <= 250):
            raise ValueError("La talla debe estar entre 100 y 250 cm.")
        self._talla = valor

    @property
    def presion(self):
        return self._presion

    @presion.setter
    def presion(self, valor):
        if not (0 <= valor <= 200):
            raise ValueError("La presión debe estar entre 0 y 200 mmHg.")
        self._presion = valor

    @property
    def frecuencia(self):
        return self._frecuencia

    @frecuencia.setter
    def frecuencia(self, valor):
        if not (0 <= valor <= 200):
            raise ValueError("La frecuencia debe estar entre 0 y 200 latidos por minuto.")
        self._frecuencia = valor

    @property
    def conciencia(self):
        return self._conciencia

    @conciencia.setter
    def conciencia(self, valor):
        if valor not in ["Alerta", "Verbal", "Dolor", "Inconsciente"]:
            raise ValueError("La conciencia debe ser 'A: Alerta', 'V: Verbal', 'D: Dolor' o 'I: Inconsciente'.")
        self._conciencia = valor   

    @property
    def saturacion(self):
        return self._saturacion
    
    @saturacion.setter
    def saturacion(self, valor):
        if not (0 <= valor <= 100):
            raise ValueError("La saturación debe estar entre 0 y 100.")
        self._saturacion = valor

    @property
    def imc(self):
        return self._imc
    
    @imc.setter
    def imc(self, valor):
        self._imc = valor
    
    @property
    def clasificacion_imc(self):
        return self._clasificacion_imc
    
    @clasificacion_imc.setter
    def clasificacion_imc(self, valor):
        self._clasificacion_imc = valor
    
    @property
    def nivel_atencion(self):
        return self._nivel_atencion
    
    @nivel_atencion.setter
    def nivel_atencion(self, valor):
        self._nivel_atencion = valor

    @property
    def fecha_registro(self):
        return self._fecha_registro    

    @fecha_registro.setter
    def fecha_registro(self, valor):
        self._fecha_registro = valor   
    
    def calcular_imc(self):
        try:
            talla_m = self.talla / 100
            self._imc = round(self.peso / (talla_m ** 2), 2)

            if self._imc < 18.5:
                self._clasificacion_imc = "Bajo peso"
            elif self._imc < 25:
                self._clasificacion_imc = "Normal"
            elif self._imc < 30:
                self._clasificacion_imc = "Sobrepeso"
            else:
                self._clasificacion_imc = "Obesidad"

        except ZeroDivisionError:
            self._imc = 0.0
            self._clasificacion_imc = "Error (Talla 0)"

    def to_dict(self):
        return {
            "peso": self._peso,
            "talla": self._talla,
            "presion": self._presion,
            "frecuencia": self._frecuencia,
            "conciencia": self._conciencia,
            "saturacion": self._saturacion,
            "imc": self._imc,
            "clasificacion_imc": self._clasificacion_imc,
            "nivel_atencion": self._nivel_atencion,
            "fecha_registro": self._fecha_registro
        }    

class GestorDatos:

    @staticmethod
    def guardar_pacientes(archivo, lista_pacientes):
        lista_dicts = [p.to_dict() for p in lista_pacientes]

        try:
            with open(archivo, "w", encoding="utf-8") as f:
                json.dump(lista_dicts, f, indent=4)
            return True
        
        except Exception as e:
            print(f"Error al guardar: {e}")
            return False

    @staticmethod
    def cargar_pacientes(archivo):
        lista_pacientes = []

        try:
            with open(archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)

            for d in datos:
                # elegir clase por edad
                Clase = PacienteEstandar if d["edad"] < 65 else PacienteAdultoMayor
                p = Clase(d["dni"], d["nombre"], d["edad"], d["sexo"])
                p.fecha_registro = d.get("fecha_registro", "")

                for a in d.get("atenciones", []):
                    at = AtencionTriage(
                        a["peso"], a["talla"], a["presion"],
                        a["frecuencia"], a["conciencia"], a["saturacion"]
                    )
                    # sobrescribimos con lo que había en el JSON
                    at._imc = a.get("imc", at.imc)
                    at._clasificacion_imc = a.get("clasificacion_imc", "")
                    at.nivel_atencion = a.get("nivel_atencion", "")
                    at.fecha_registro = a.get("fecha_registro", at.fecha_registro)

                    p.agregar_atencion(at)

                lista_pacientes.append(p)

        except FileNotFoundError:
            print("[SISTEMA] Archivo de datos no encontrado. Iniciando base de datos nueva.")
        except json.JSONDecodeError as e:
            print(f"[ERROR] El archivo JSON está corrupto: {e}")
        except Exception as e:
            print(f"[ERROR] Error inesperado al cargar datos: {e}")

        return lista_pacientes

    
