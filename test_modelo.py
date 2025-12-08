import unittest
from modelo import PacienteEstandar, PacienteAdultoMayor


class TestTriaje(unittest.TestCase):

    def setUp(self):
  
        self.paciente_joven = PacienteEstandar(
            "Joven Test", 30, "Masculino", 80, 180, 120, 80, 98, "Alerta"
        )

        self.paciente_mayor = PacienteAdultoMayor(
            "Abuelo Test", 80, "Masculino", 70, 165, 120, 80, 98, "Alerta"
        )

    def test_calculo_imc_normal(self):

        self.paciente_joven.calcular_imc()
        self.assertEqual(self.paciente_joven.imc, 24.69)
        self.assertEqual(self.paciente_joven.clasificacion_imc, "Normal")

    def test_validacion_edad_negativa(self):
  
        with self.assertRaises(ValueError):
            p = PacienteEstandar("Error", -5, "M", 80, 180, 120, 80, 98, "A")

    def test_polimorfismo_saturacion(self):

        self.paciente_joven.saturacion = 93
        atencion_joven = self.paciente_joven.clasificar_atencion()
        self.assertEqual(atencion_joven, "Normal")

        self.paciente_mayor.saturacion = 93
        atencion_mayor = self.paciente_mayor.clasificar_atencion()
        self.assertEqual(atencion_mayor, "Urgente")



if __name__ == '__main__':
    unittest.main()
