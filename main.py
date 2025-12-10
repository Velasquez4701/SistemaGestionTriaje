import sys
import config

from modelo import PacienteEstandar, PacienteAdultoMayor, AtencionTriage, GestorDatos, ValidadorDni, DniInvalidoException, PacienteNoEncontradoException
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


    def _buscar_paciente_por_dni(self, dni):
        for p in self.pacientes:
            if p.dni == dni:
                return p
        return None

    def registrar_paciente(self):

        dni = self.vista.solicitar_dni("Ingrese DNI del paciente: ")

        paciente = self._buscar_paciente_por_dni(dni)   

        if paciente is None:
            datos_personales = self.vista.solicitar_datos_personales()
            if datos_personales['edad'] < 65:
                paciente = PacienteEstandar(
                    dni,
                    datos_personales['nombre'],
                    datos_personales['edad'],
                    datos_personales['sexo']
                )
            else:
                paciente = PacienteAdultoMayor(
                    dni,
                    datos_personales['nombre'],
                    datos_personales['edad'],
                    datos_personales['sexo']
                )
            self.pacientes.append(paciente)

        # Solicitar datos de triaje
        datos_triaje = self.vista.solicitar_datos_triaje()

        atencion = AtencionTriage(
            datos_triaje['peso'],
            datos_triaje['talla'],
            datos_triaje['presion'],
            datos_triaje['frecuencia'],
            datos_triaje['conciencia'],
            datos_triaje['saturacion']
        )

        paciente.agregar_atencion(atencion)
        paciente.clasificar_atencion(atencion)

        GestorDatos.guardar_pacientes(config.ARCHIVO_DB, self.pacientes)

        self.vista.mostrar_mensaje(
            f"Atención registrada para {paciente.nombre}.\n"
            f"   Nivel de atención: {atencion.nivel_atencion.upper()}",
            "exito"
        )
        self.vista.pausar()

    def buscar_paciente_por_nombre(self):
        texto = input("Ingrese el nombre a buscar: ").strip().lower()
        encontrado = None
        
        for p in self.pacientes:
            if texto in p.nombre.lower():
                encontrado = p
                break
        
        self.vista.mostrar_reporte_paciente(encontrado)
    
    def buscar_paciente_por_dni(self):
        try:
            dni = self.vista.solicitar_dni("Ingrese el DNI a buscar: ") 
            paciente = self._buscar_paciente_por_dni(dni)
            self.vista.mostrar_reporte_paciente(paciente)

        except DniInvalidoException as e:
            self.vista.mostrar_mensaje(str(e), "error")
            self.vista.pausar()


    def listar_pacientes(self):

        self.vista.mostrar_tabla_pacientes(self.pacientes, "Listado General")


    def listar_urgentes(self):
        urgentes = []

        for p in self.pacientes:
            ultima_atencion = p.obtener_ultima_atencion()

            if ultima_atencion is None:
                continue

            if ultima_atencion.nivel_atencion == "Urgente":
                urgentes.append(p)

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
        conteo_imc = {
            "Bajo peso": 0,
            "Normal": 0,
            "Sobrepeso": 0,
            "Obesidad": 0,
            "Error (Talla 0)": 0
        }

        for p in self.pacientes:
            atencion = p.obtener_ultima_atencion()
            if atencion is None:
                continue

            if atencion.nivel_atencion in conteo_atencion:
                conteo_atencion[atencion.nivel_atencion] += 1

            if atencion.clasificacion_imc in conteo_imc:
                conteo_imc[atencion.clasificacion_imc] += 1

        stats = {
            "total": total,
            "promedio_edad": promedio,
            "por_atencion": conteo_atencion,
            "por_imc": conteo_imc
        }

        self.vista.mostrar_estadisticas(stats)
    
    def ver_historial_paciente(self):
        try:
            dni = self.vista.solicitar_dni()

            paciente = self._buscar_paciente_por_dni(dni)

            if paciente is None:
                raise PacienteNoEncontradoException(
                    f"No se encontró paciente con DNI {dni}."
                )

            self.vista.mostrar_historial_paciente(paciente)

        except (PacienteNoEncontradoException, DniInvalidoException) as e:
            self.vista.mostrar_mensaje(str(e), "error")
            self.vista.pausar()

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
                self.buscar_paciente_por_dni()
            elif opcion == '3':
                self.buscar_paciente_por_nombre()
            elif opcion == '4':
                self.listar_pacientes()
            elif opcion == '5':
                self.listar_urgentes()
            elif opcion == '6':
                self.calcular_estadisticas()
            elif opcion == '7':
                self.ver_historial_paciente()
            elif opcion == '8':
                self.salir()
            else:
                self.vista.mostrar_mensaje("Opción no válida. Intente de nuevo.", "error")
                self.vista.pausar()



if __name__ == "__main__":
    app = Controlador()
    app.ejecutar()

