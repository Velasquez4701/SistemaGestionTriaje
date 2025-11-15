# 🏥 Sistema de Gestión de Triaje (SGT)

**Proyecto Final del curso 1FIS275 - Fundamentos de Programación 2**

Este proyecto es una aplicación de consola desarrollada en Python que simula un sistema de triaje de pacientes para el área de emergencias de una clínica ficticia, la "Clínica Santa María".

## 🎯 Problema Solucionado

El sistema aborda la problemática de un proceso de triaje **manual (AS-IS)**, que es lento, propenso a errores humanos de cálculo (IMC) y subjetivo en la priorización de pacientes.

La solución **(TO-BE)** es un sistema digital que **automatiza y estandariza** el registro, cálculo y clasificación de pacientes, asignando un nivel de atención (**"Urgente"** o **"Normal"**) basado en reglas de negocio claras, asegurando la trazabilidad y eficiencia del proceso.

## ✨ Características Principales

El sistema está construido siguiendo el paradigma de **Programación Orientada a Objetos (OOP)** y las buenas prácticas de desarrollo:

* **Arquitectura OOP:** El núcleo del sistema utiliza **clases** (`Persona`, `Paciente`) y **herencia** para modelar el dominio.
* **Polimorfismo:** Se aplica el polimorfismo para el método `clasificar_atencion()`, permitiendo que la lógica de triaje sea diferente para un `PacienteEstandar` y un `PacienteAdultoMayor`.
* **Persistencia de Datos:** El sistema utiliza archivos **JSON** (`datos.json`) para cargar y guardar el historial de pacientes, asegurando que la información no se pierda al cerrar la aplicación.
* **Menú Interactivo:** La aplicación se controla a través de un menú de consola claro y funcional que incluye:
    1.  Registrar Paciente
    2.  Buscar Paciente
    3.  Listar Pacientes (Todos)
    4.  Listar Pacientes (Urgentes)
    5.  Ver Estadísticas
    6.  Salir (con guardado automático)
* **Módulo de Estadísticas:** Ofrece cálculos en tiempo real sobre los datos registrados (ej. % de pacientes urgentes, promedio de edad, etc.).
* **Manejo de Excepciones:** El sistema valida robustamente todas las entradas del usuario (ej. `try-except`) para prevenir errores en tiempo de ejecución.
* **Pruebas Unitarias:** Incluye un módulo de pruebas (`test_modelo.py`) para verificar la correcta funcionalidad de los cálculos críticos (IMC y triaje).

## 🏛️ Arquitectura del Proyecto

El proyecto sigue una arquitectura desacoplada (similar a MVC) para separar responsabilidades:

```
proyecto_triaje/
│
├── main.py             # 1. Controlador (Lógica del menú, orquestador)
├── modelo.py           # 2. Modelo (Clases OOP, lógica de negocio, Gestor JSON)
├── vista.py            # 3. Vista (Manejo de prints/inputs, tablas Tabulate)
├── config.py           # 4. Configuración (Constantes y reglas de negocio)
├── test_modelo.py      # 5. Pruebas Unitarias (unittest)
│
├── datos.json          # Archivo de persistencia (Base de datos)
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Esta documentación
```

## 🚀 Instalación y Ejecución

Siga estos pasos para ejecutar el proyecto en su máquina local:

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/Velasquez4701/SistemaGestionTriaje.git](https://github.com/Velasquez4701/SistemaGestionTriaje.git)
    ```

2.  **Navegar a la carpeta del proyecto:**
    ```bash
    cd SistemaGestionTriaje
    ```

3.  **(Opcional pero recomendado) Crear un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

4.  **Instalar las dependencias:**
    El proyecto solo tiene una dependencia externa (`tabulate`), listada en `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

5.  **Ejecutar la aplicación:**
    ```bash
    python main.py
    ```

6.  **(Opcional) Ejecutar las pruebas:**
    Para verificar que los módulos de cálculo funcionen correctamente:
    ```bash
    python -m unittest test_modelo.py
    ```

## 🛠️ Herramientas de Gestión

* **Trello:** Planificación de actividades (Sprints, Hitos 1 y 2) y asignación de tareas.
* **Git / GitHub:** Control de versiones, trabajo colaborativo y gestión de código.
* **Figma:** Diseño y prototipado del organigrama.
