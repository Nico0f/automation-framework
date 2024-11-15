# Framework de Automatización Python

Framework Python modular para la automatización de tareas con programación, monitoreo e interfaz web.

## 🚀 Características

### Funcionalidad Principal
- **Gestión de Tareas**: Sistema modular de tareas con componentes conectables
- **Programación**: Programación de tareas estilo cron con configuración flexible
- **Ejecución Paralela**: Ejecución de tareas multi-hilo con trabajadores configurables
- **Monitoreo**: Sistema integrado de monitoreo de rendimiento del sistema y tareas
- **API REST**: Interfaz REST basada en FastAPI para gestión de tareas
- **Panel Web**: Interfaz de monitoreo en tiempo real y gestión de tareas

### Tipos de Tareas Incorporadas
- 📁 Operaciones de Archivos (copiar, mover, respaldar)
- 🔌 Operaciones de Red
- 💽 Operaciones de Base de Datos
- 🌐 Operaciones de API
- 📧 Operaciones de Correo Electrónico
- 🖥️ Operaciones del Sistema

### Características Adicionales
- Sistema de registro completo
- Manejo de errores y reintentos
- Recolección y monitoreo de métricas
- Gestión segura de credenciales
- Notificaciones por correo electrónico
- Integración con Prometheus

## 📋 Requisitos

- Python 3.9+
- PostgreSQL (para historial de tareas)
- Redis (opcional, para caché)

## 🛠️ Instalación

1. Clonar el repositorio:
```bash
git clone repo-name
cd automation-framework
```

2. Crear un entorno virtual y activarlo:
```bash
python -m venv venv
source venv/bin/activate  # Linux
# o
venv\Scripts\activate  # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Crear archivos de configuración:
```bash
cp config/config.example.yaml config/config.yaml
cp config/schedule.example.yaml config/schedule.yaml
```

5. Actualizar las configuraciones con tus ajustes

## ⚙️ Configuración

### Configuración Principal (config/config.yaml)
```yaml
logging:
  level: INFO
  format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  file: 'automation.log'

task_defaults:
  timeout: 300
  retry_count: 3
  retry_delay: 5

database:
  url: postgresql://usuario:contraseña@localhost/automation
```

### Configuración de Programación (config/schedule.yaml)
```yaml
schedules:
  - name: respaldo_diario
    task: file_operations
    schedule: "0 0 * * *"
    parameters:
      operation: backup
      source_path: /datos
      destination_path: /respaldo
```

## 🚀 Uso

### Iniciando el Framework
```bash
python main.py
```

Esto iniciará:
- Programador de tareas
- Sistema de monitoreo (puerto 9090)
- Servidor API (puerto 8000)
- Panel web (puerto 8000/dashboard)

### Usando la API

Crear una nueva tarea:
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "file_operations",
    "parameters": {
      "operation": "copy",
      "source": "/ruta/origen",
      "destination": "/ruta/destino"
    }
  }'
```

Listar tareas disponibles:
```bash
curl http://localhost:8000/tasks
```

### Creando Tareas Personalizadas

1. Crear una nueva clase de tarea:
```python
from tasks.base_task import BaseTask

class TareaPersonalizada(BaseTask):
    def validate(self) -> bool:
        # Agregar lógica de validación
        return True

    def execute(self) -> bool:
        try:
            # Agregar lógica de ejecución
            return True
        except Exception as e:
            self.logger.error(f"Tarea fallida: {str(e)}")
            raise
```

2. Registrar la tarea:
```python
task_manager.register_task('tarea_personalizada', TareaPersonalizada)
```

## 📊 Monitoreo

### Métricas de Prometheus
Disponibles en `http://localhost:9090/metrics`:
- Tiempos de ejecución de tareas
- Tasas de éxito/fracaso
- Uso de recursos del sistema
- Métricas personalizadas

### Panel Web
Disponible en `http://localhost:8000/dashboard`:
- Estado de tareas en tiempo real
- Métricas del sistema
- Historial de tareas
- Gestión de configuración

## 🧪 Pruebas

Ejecutar suite de pruebas:
```bash
pytest
```

Ejecutar con cobertura:
```bash
pytest --cov=automation_framework tests/
```

## 📁 Estructura del Proyecto

```
automation_framework/
├── config/           # Archivos de configuración
├── core/             # Componentes principales del framework
├── tasks/            # Implementaciones de tareas
├── utils/            # Funciones de utilidad
├── exceptions/       # Excepciones personalizadas
├── database/         # Modelos de base de datos
├── api/              # API REST
├── web/              # Panel web
└── tests/            # Suite de pruebas
```
