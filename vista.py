import os
from tabulate import tabulate
import config 
from modelo import ValidadorDni, DniInvalidoException


class Vista:

    def limpiar_pantalla(self):
        os.system("cls" if os.name == "nt" else "clear")

    def mostrar_encabezado(self):
        print("=" * 60)
        print(f"{config.MSG_BIENVENIDA:^60}")
        print("=" * 60)

    def mostrar_menu_principal(self):
        print("\nMenú Principal:")
        print("1. 📝 Registrar Nuevo Paciente")
        print("2. 🔍 Buscar Paciente por DNI")
        print("3. 🔍 Buscar Paciente por Nombre")
        print("4. 📋 Listar Pacientes (Todos)")
        print("5. 🚨 Listar Pacientes (Solo Urgentes)")
        print("6. 📊 Ver Estadísticas")
        print("7. 📋 Ver Historial de Paciente")
        print("8. 💾 Salir y Guardar")
        print("-" * 30)

    def solicitar_opcion(self):
        return input("Seleccione una opción (1-8): ").strip()
    

    def __leer_texto(self, mensaje):

        while True:
            valor = input(mensaje).strip()
            if valor:
                return valor
            print("❌ Error: El campo no puede estar vacío.")


    def __leer_entero(self, mensaje, min_val=None, max_val=None):

        while True:
            try:
                valor = int(input(mensaje))
                if min_val is not None and valor < min_val:
                    print(f"❌ Error: El valor debe ser mayor o igual a {min_val}.")
                    continue
                if max_val is not None and valor > max_val:
                    print(f"❌ Error: El valor debe ser menor o igual a {max_val}.")
                    continue
                return valor
            
            except ValueError:
                print("❌ Error: Debe ingresar un número entero válido.")


    def __leer_flotante(self, mensaje, min_val=0.0):

        while True:
            try:
                valor = float(input(mensaje))
                if valor <= min_val:
                    print(f"❌ Error: El valor debe ser mayor a {min_val}.")
                    continue
                return valor
            
            except ValueError:
                print("❌ Error: Debe ingresar un número válido (ej. 70.5).")


    def __leer_opcion(self, mensaje, opciones_validas):

        while True:
            valor = input(mensaje).strip().upper()
            if valor in opciones_validas:
                return valor
            print(f"❌ Error: Opción inválida. Ingrese una de estas: {opciones_validas}")

    
    def solicitar_datos_personales(self):

        print("\n--- 📝 Registro de Nuevo Paciente ---")
        nombre = self.__leer_texto("Nombre y Apellido: ")

        sexo_input = self.__leer_opcion("Sexo (M/F): ", ["M", "F"])
        sexo = "Masculino" if sexo_input == "M" else "Femenino"
        
        edad = self.__leer_entero("Edad (años): ", min_val=0, max_val=120)
        
        return {
            "nombre": nombre, 
            "edad": edad, 
            "sexo": sexo,
        }

    def solicitar_datos_triaje(self):

        print("\n--- Signos Vitales ---")
        peso = self.__leer_flotante("Peso (kg): ", min_val=0)
        talla = self.__leer_flotante("Talla (cm): ", min_val=0)
        presion = self.__leer_flotante("Presión Sistólica (mmHg): ", min_val=0)
        frecuencia = self.__leer_entero("Frecuencia Cardiaca (lpm): ", min_val=0, max_val=300)
        saturacion = self.__leer_entero("Saturación de Oxígeno (%): ", min_val=0, max_val=100)

        conciencia_op = self.__leer_opcion("Nivel de Conciencia (A/V/D/I): ", ["A", "V", "D", "I"])
        mapa_conciencia = {"A": "Alerta", "V": "Verbal", "D": "Dolor", "I": "Inconsciente"}
        conciencia = mapa_conciencia[conciencia_op]

        return {
            "peso": peso, 
            "talla": talla, 
            "presion": presion,
            "frecuencia": frecuencia, 
            "conciencia": conciencia,
            "saturacion": saturacion,
        }


    def mostrar_tabla_pacientes(self, lista_pacientes, titulo="Listado de Pacientes"):

        print(f"\n=== {titulo} ===")

        if not lista_pacientes:
            print("[INFO] No hay pacientes para mostrar.")
            self.pausar()
            return
        
        datos_tabla = []

        for p in lista_pacientes:
            at = p.obtener_ultima_atencion()
            if at is None:
                datos_tabla.append([
                    p.dni,
                    p.nombre,
                    f"{p.edad} años",
                    p.sexo,
                    "-", "-", "-", "-", "-", "-", "SIN ATENCIÓN"
                ])
            else:
                datos_tabla.append([
                    p.dni,
                    p.nombre,
                    f"{p.edad} años",
                    p.sexo,
                    at.peso,
                    at.talla,
                    at.imc,
                    at.clasificacion_imc,
                    at.presion,
                    f"{at.saturacion}%",
                    at.nivel_atencion.upper()
                ])

        print(tabulate(datos_tabla, headers=config.ENCABEZADOS_TABLA, tablefmt="fancy_grid"))
        self.pausar()


    def mostrar_reporte_paciente(self, paciente):

        if not paciente:
            self.mostrar_mensaje("Paciente no encontrado.")
            self.pausar()
            return

        p_ultima_atencion = paciente.obtener_ultima_atencion()
        
        print("\n" + "="*40)
        print(f"📄 FICHA DEL PACIENTE: {paciente.nombre.upper()}")
        print("="*40)
        print(f"📅 Registrado: {paciente.fecha_registro}")
        print(f"👤 Edad: {paciente.edad} años | Sexo: {paciente.sexo}")
        print(f"⚖️  Peso: {p_ultima_atencion.peso} kg | Talla: {p_ultima_atencion.talla} cm")
        print("-" * 40)
        print(f"💓 Presión: {p_ultima_atencion.presion} | Frecuencia: {p_ultima_atencion.frecuencia}")
        print(f"🫁 Saturación: {p_ultima_atencion.saturacion}% | Conciencia: {p_ultima_atencion.conciencia}")
        print("-" * 40)
        print(f"📊 IMC: {p_ultima_atencion.imc} ({p_ultima_atencion.clasificacion_imc})")

        estado = p_ultima_atencion.nivel_atencion.upper()
        icono = "🚨" if estado == "URGENTE" else "✅"
        print(f"{icono} NIVEL DE ATENCIÓN: {estado}")
        print("="*40)
        self.pausar()


    def mostrar_estadisticas(self, stats):

        print("\n📊 ESTADÍSTICAS DEL SISTEMA")
        print("=" * 40)
        print(f"Total de Pacientes: {stats['total']}")
        print(f"Edad Promedio: {stats['promedio_edad']} años")
        print("-" * 40)
        print("Por Nivel de Atención:")
        for k, v in stats["por_atencion"].items():
            print(f"  - {k}: {v}")
        print("=" * 40)
        self.pausar()

    def solicitar_dni(self, mensaje = "Ingrese número de DNI: "):
        # return self.__leer_texto("Ingrese número de DNI: ")
        while True:
            dni = input(mensaje).strip()
            try:
                dni_validado = ValidadorDni.validar(dni)
                return dni_validado
            except DniInvalidoException as e:
                print(f"❌ {e}")   # muestra el error

    def mostrar_historial_paciente(self, paciente):

        if not paciente:
            self.mostrar_mensaje("Paciente no encontrado.", "error")
            self.pausar()
            return

        if not paciente.lista_atencion_triage:
            self.mostrar_mensaje("Este paciente no tiene atenciones registradas.", "info")
            self.pausar()
            return

        print("\n" + "="*50)
        print(f"📄 HISTORIAL DEL PACIENTE: {paciente.nombre.upper()}")
        print(f"DNI: {paciente.dni} | Edad: {paciente.edad} años | Sexo: {paciente.sexo}")
        print("="*50)

        filas = []
        for i, a in enumerate(paciente.lista_atencion_triage, start=1):
            filas.append([
                i,
                a.fecha_registro,
                a.peso,
                a.talla,
                a.imc,
                a.clasificacion_imc,
                a.presion,
                a.frecuencia,
                a.saturacion,
                a.conciencia,
                a.nivel_atencion
            ])

        encabezados = [
            "N°",
            "Fecha",
            "Peso",
            "Talla",
            "IMC",
            "Clasif. IMC",
            "Presión",
            "Frecuencia",
            "Saturación",
            "Conciencia",
            "Atención"
        ]

        print(tabulate(filas, headers=encabezados, tablefmt="fancy_grid"))
        self.pausar()


    def mostrar_mensaje(self, mensaje, tipo="info"):

        if tipo == "exito":
            print(f"\n✅ [ÉXITO] {mensaje}")
        elif tipo == "error":
            print(f"\n❌ [ERROR] {mensaje}")
        else:
            print(f"\nℹ️  [INFO] {mensaje}")

    def pausar(self):
        input("\nPresione ENTER para continuar...")
