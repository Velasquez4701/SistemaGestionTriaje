import unittest
from modelo import PacienteEstandar, PacienteAdultoMayor, AtencionTriage


class TestTriaje(unittest.TestCase):

    def setUp(self):
        # Crear pacientes con constructor correcto: dni, nombre, edad, sexo
        self.paciente_joven = PacienteEstandar("12345678", "Joven Test", 30, "Masculino")
        self.paciente_mayor = PacienteAdultoMayor("87654321", "Abuelo Test", 80, "Masculino")
        
        # Crear atención con datos vitales correctos
        atencion_joven = AtencionTriage(
            peso=80, talla=180, presion=120, frecuencia=80, 
            conciencia="Alerta", saturacion=98
        )
        self.paciente_joven.agregar_atencion(atencion_joven)
        
        atencion_mayor = AtencionTriage(
            peso=70, talla=165, presion=120, frecuencia=80,
            conciencia="Alerta", saturacion=98
        )
        self.paciente_mayor.agregar_atencion(atencion_mayor)

    def test_calculo_imc_normal(self):
        # El IMC ya se calcula en el constructor de AtencionTriage
        atencion = self.paciente_joven.obtener_ultima_atencion()
        self.assertEqual(atencion.imc, 24.69)
        self.assertEqual(atencion.clasificacion_imc, "Normal")

    def test_validacion_edad_negativa(self):
        # DNI, Nombre, Edad (negativa), Sexo
        with self.assertRaises(ValueError):
            p = PacienteEstandar("12345678", "Error", -5, "Masculino")

    def test_polimorfismo_saturacion(self):
        # Obtener atención del paciente joven y modificar saturación
        atencion_joven = self.paciente_joven.obtener_ultima_atencion()
        atencion_joven.saturacion = 93
        self.paciente_joven.clasificar_atencion(atencion_joven)
        self.assertEqual(atencion_joven.nivel_atencion, "Normal")

        # Obtener atención del paciente mayor y modificar saturación
        atencion_mayor = self.paciente_mayor.obtener_ultima_atencion()
        atencion_mayor.saturacion = 93
        self.paciente_mayor.clasificar_atencion(atencion_mayor)
        self.assertEqual(atencion_mayor.nivel_atencion, "Urgente")



if __name__ == '__main__':
    unittest.main()
