import sys
import config

from modelo import PacienteEstandar, PacienteAdultoMayor, GestorDatos
from vista import Vista


class Controlador:
    
    def __init__(self):
        self.vista = Vista()
        self.pacientes = []

        self.cargar_datos_iniciales()


    def cargar_datos_iniciales(self):
        
        self.pacientes = GestorDatos.cargar_pacientes(config.ARCHIVO_DB)
       
        if self.pacientes:
            print(f"[SISTEMA] Se han cargado {len(self.pacientes)} pacientes del historial.")
        else:
            print("[SISTEMA] No hay historial previo. Iniciando base de datos nueva.")


    def registrar_paciente(self):

        datos = self.vista.solicitar_datos_paciente()

        if datos['edad'] <= 75:
            nuevo_paciente = PacienteEstandar(
                datos['nombre'], datos['edad'], datos['sexo'],
                datos['peso'], datos['talla'], datos['presion'],
                datos['frecuencia'], datos['saturacion'], datos['conciencia']
            )
        else:
            nuevo_paciente = PacienteAdultoMayor(
                datos['nombre'], datos['edad'], datos['sexo'],
                datos['peso'], datos['talla'], datos['presion'],
                datos['frecuencia'], datos['saturacion'], datos['conciencia']
            )


        nuevo_paciente.clasificar_atencion()

        self.pacientes.append(nuevo_paciente)

        GestorDatos.guardar_pacientes(config.ARCHIVO_DB, self.pacientes)

        self.vista.mostrar_mensaje(
            f"Paciente registrado.\n   Diagnóstico: {nuevo_paciente.nivel_atencion.upper()}", 
            "exito"
        )
        self.vista.pausar()


    def buscar_paciente(self):
        texto = input("Ingrese el nombre a buscar: ").strip().lower()
        encontrado = None
        
        for p in self.pacientes:
            if texto in p.nombre.lower():
                encontrado = p
                break
        
        self.vista.mostrar_reporte_paciente(encontrado)


    def listar_pacientes(self):

        self.vista.mostrar_tabla_pacientes(self.pacientes, "Listado General")


    def listar_urgentes(self):

        urgentes = [p for p in self.pacientes if p.nivel_atencion == "Urgente"]
        self.vista.mostrar_tabla_pacientes(urgentes, "Listado de URGENCIAS")


    def calcular_estadisticas(self):
    
        if not self.pacientes:
            self.vista.mostrar_mensaje("No hay datos para estadísticas.", "error")
            self.vista.pausar()
            return

        total = len(self.pacientes)
        suma_edad = sum(p.edad for p in self.pacientes)
        promedio = round(suma_edad / total, 1)


        conteo_atencion = {"Urgente": 0, "Normal": 0}
        conteo_imc = {"Bajo peso": 0, "Normal": 0, "Sobrepeso": 0, "Obesidad": 0, "Error (Talla 0)": 0}

        for p in self.pacientes:

            if p.nivel_atencion in conteo_atencion:
                conteo_atencion[p.nivel_atencion] += 1
            
            if p.clasificacion_imc in conteo_imc:
                conteo_imc[p.clasificacion_imc] += 1

        stats = {
            "total": total,
            "promedio_edad": promedio,
            "por_atencion": conteo_atencion,
            "por_imc": conteo_imc
        }
        
        self.vista.mostrar_estadisticas(stats)


    def salir(self):

        if GestorDatos.guardar_pacientes(config.ARCHIVO_DB, self.pacientes):
            print(config.MSG_DESPEDIDA)
        else:
            print("Error al guardar los datos finales.")
        sys.exit()


    def ejecutar(self):

        while True:
            self.vista.limpiar_pantalla()
            self.vista.mostrar_encabezado()
            self.vista.mostrar_menu_principal()
            
            opcion = self.vista.solicitar_opcion()

            if opcion == '1':
                self.registrar_paciente()
            elif opcion == '2':
                self.buscar_paciente()
            elif opcion == '3':
                self.listar_pacientes()
            elif opcion == '4':
                self.listar_urgentes()
            elif opcion == '5':
                self.calcular_estadisticas()
            elif opcion == '6':
                self.salir()
            else:
                self.vista.mostrar_mensaje("Opción no válida. Intente de nuevo.", "error")
                self.vista.pausar()



if __name__ == "__main__":
    app = Controlador()
    app.ejecutar()

