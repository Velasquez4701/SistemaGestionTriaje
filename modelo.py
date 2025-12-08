import json
from datetime import datetime


class Persona:

    def __init__(self, nombre, edad, sexo):
        self.nombre = nombre
        self.sexo = sexo
        self.__edad = 0
        self.edad = edad

    @property
    def edad(self):
        return self.__edad
    
    @edad.setter
    def edad(self, valor):
        if valor < 0:
            raise ValueError("La edad no puede ser negativa.")
        self.__edad = valor


class Paciente(Persona):

    def __init__(self, nombre, edad, sexo, peso, talla, presion, frecuencia, saturacion, conciencia):
        super().__init__(nombre, edad, sexo)
        self.peso = peso
        self.talla = talla
        self.presion = presion
        self.frecuencia = frecuencia
        self.conciencia = conciencia

        self.__saturacion = 0
        self.saturacion = saturacion

        self.__imc = 0.0
        self.__clasificacion_imc = ""
        self.__nivel_atencion = ""

        self.fecha_registro = datetime.now().strftime("%d-%m-%Y %H:%M")

        self.calcular_imc()

    @property
    def saturacion(self):
        return self.__saturacion
    
    @saturacion.setter
    def saturacion(self, valor):
        if not (0 <= valor <= 100):
            raise ValueError("La saturación debe estar entre 0 y 100.")
        self.__saturacion = valor

    @property
    def imc(self):
        return self.__imc
    
    @property
    def clasificacion_imc(self):
        return self.__clasificacion_imc
    
    @property
    def nivel_atencion(self):
        return self.__nivel_atencion
    
    def calcular_imc(self):
        try:
            talla_m = self.talla / 100
            self.__imc = round(self.peso / (talla_m ** 2), 2)

            if self.__imc < 18.5:
                self.__clasificacion_imc = "Bajo peso"
            elif self.__imc < 25:
                self.__clasificacion_imc = "Normal"
            elif self.__imc < 30:
                self.__clasificacion_imc = "Sobrepeso"
            else:
                self.__clasificacion_imc = "Obesidad"

        except ZeroDivisionError:
            self.__imc = 0.0
            self.__clasificacion_imc = "Error (Talla 0)"

    def clasificar_atencion(self):
        raise NotImplementedError("Debe ser implementado por la subclase.")

    def _set_nivel_atencion(self, nivel):
        self.__nivel_atencion = nivel

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "edad": self.edad,
            "sexo": self.sexo,
            "peso": self.peso,
            "talla": self.talla,
            "presion": self.presion,
            "frecuencia": self.frecuencia,
            "saturacion": self.saturacion,
            "conciencia": self.conciencia,
            "imc": self.imc,
            "clasificacion_imc": self.clasificacion_imc,
            "nivel_atencion": self.nivel_atencion,
            "fecha_registro": self.fecha_registro
        }    


class PacienteEstandar(Paciente):

    def clasificar_atencion(self):
        es_urgente = (
            self.presion < 90 or self.presion > 180 or
            self.frecuencia > 100 or
            self.saturacion < 92 or
            self.conciencia != "Alerta"
        )

        resultado = "Urgente" if es_urgente else "Normal"
        self._set_nivel_atencion(resultado)
        return resultado
    

class PacienteAdultoMayor(Paciente):

    def clasificar_atencion(self):
        es_urgente = (
            self.presion < 100 or self.presion > 160 or
            self.frecuencia < 55 or self.frecuencia > 110 or
            self.saturacion < 94 or
            self.conciencia != "Alerta"
        )

        resultado = "Urgente" if es_urgente else "Normal"
        self._set_nivel_atencion(resultado)
        return resultado
    
    
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
                Clase = PacienteEstandar if d["edad"] <= 75 else PacienteAdultoMayor

                p = Clase(
                    d['nombre'], d['edad'], d['sexo'], d['peso'], d['talla'],
                    d['presion'], d['frecuencia'], d['saturacion'], d['conciencia']
                )

                p.fecha_registro = d["fecha_registro"]
                p._set_nivel_atencion(d["nivel_atencion"])
                lista_pacientes.append(p)

        except (FileNotFoundError, ValueError):
            pass
        return lista_pacientes

    
