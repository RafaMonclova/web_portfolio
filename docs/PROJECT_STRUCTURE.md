# Django Base API — Estructura del proyecto

## Stack principal

| Tecnología | Versión |
|---|---|
| Python | 3.x |
| Django | 5.1.x |
| Django REST Framework | 3.16.x |
| Simple JWT | 5.5.x |
| drf-spectacular | 0.27.x (Swagger/ReDoc) |
| Celery + django-celery-beat | 5.x |
| Django Channels (WebSocket) | 4.x |
| django-filter | 23.x |

---

## Estructura de carpetas

```
portfolio/
│
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
│
├── config/                        # Configuración global del proyecto
│   ├── settings.py                # Variables de entorno, INSTALLED_APPS, etc.
│   ├── urls.py                    # URL raíz del proyecto
│   ├── celery.py                  # Configuración de Celery
│   ├── consumer.py                # Consumer base de Django Channels
│   ├── routing.py                 # Routing de WebSockets
│   ├── pagination.py              # Clases de paginación globales
│   ├── TokenAuthMiddleware.py     # Middleware de autenticación por token
│   ├── asgi.py
│   └── wsgi.py
│
├── apps/                          # Todas las aplicaciones del proyecto
│   ├── __init__.py
│   ├── users/                     # App de usuarios (incluye el comando custom)
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── filters.py
│   │   ├── permission.py
│   │   ├── admin.py
│   │   ├── apps.py                # name = 'apps.users'
│   │   ├── api/
│   │   │   ├── views.py
│   │   │   └── urls.py
│   │   ├── services/              # Lógica de negocio compleja
│   │   │   └── __init__.py
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── startapp_custom.py   ← comando para crear nuevas apps
│   │   └── migrations/
│   │
│   └── <tu_app>/                  # Estructura que genera startapp_custom
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py                # name = 'apps.<tu_app>'
│       ├── models.py
│       ├── serializers.py
│       ├── filters.py
│       ├── permission.py
│       ├── tests.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── views.py
│       │   └── urls.py
│       ├── services/
│       │   └── __init__.py
│       └── migrations/
│           └── __init__.py
│
├── shared/                        # Código reutilizable entre apps
│   ├── exceptions/
│   └── utils/
│       └── helpers.py
│
├── docs/                          # Documentación del proyecto
├── media/                         # Archivos subidos por usuarios
└── static/                        # Archivos estáticos
```

---

## Convenciones del proyecto

- Todas las apps viven dentro de `apps/` y se registran como `apps.<nombre>` en `INSTALLED_APPS`.
- La lógica de negocio compleja va en la carpeta `services/` de cada app, no en las vistas.
- Las rutas de cada app se incluyen desde `config/urls.py` con el prefijo `apiweb/`.
- Las vistas usan ViewSets de DRF con routers siempre que sea posible.

---

## Crear una nueva app

### Comando

```bash
python manage.py startapp_custom <nombre_app>
```

**Ejemplo:**

```bash
python manage.py startapp_custom facturas
```

Esto crea automáticamente `apps/facturas/` con toda la estructura necesaria.

---

### Pasos posteriores a crear una app

#### 1. Registrar en `INSTALLED_APPS`

Abre `config/settings.py` y añade la app:

```python
INSTALLED_APPS = [
    # ...apps de terceros...
    'apps.users',
    'apps.facturas',   # ← añadir aquí
]
```

#### 2. Registrar las URLs

Abre `config/urls.py` y añade el include:

```python
urlpatterns = [
    # ...rutas existentes...
    path('apiweb/', include('apps.facturas.api.urls')),
]
```

#### 3. Crear los modelos

Edita `apps/facturas/models.py`:

```python
from django.db import models

class Factura(models.Model):
    numero = models.CharField(max_length=20)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado_en']
```

#### 4. Crear el serializer

Edita `apps/facturas/serializers.py`:

```python
from rest_framework import serializers
from apps.facturas.models import Factura

class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = '__all__'
```

#### 5. Crear la vista

Edita `apps/facturas/api/views.py`:

```python
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from apps.facturas.models import Factura
from apps.facturas.serializers import FacturaSerializer

class FacturaViewSet(ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer
    permission_classes = [IsAuthenticated]
```

#### 6. Registrar la ruta en el router

Edita `apps/facturas/api/urls.py`:

```python
from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.facturas.api.views import FacturaViewSet

router = DefaultRouter()
router.register(r'facturas', FacturaViewSet)

urlpatterns = []
urlpatterns += router.urls
```

#### 7. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Documentación de la API (Swagger / ReDoc)

Una vez levantado el servidor, la documentación automática está disponible en:

| Interfaz | URL |
|---|---|
| Swagger UI | `http://localhost:8000/apiweb/swagger/` |
| ReDoc | `http://localhost:8000/apiweb/redoc/` |
| Schema (JSON) | `http://localhost:8000/apiweb/schema/` |

---

## Levantar el servidor

```bash
# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Crear superusuario (opcional)
python manage.py createsuperuser

# Levantar servidor de desarrollo
python manage.py runserver
```

### Con Docker

```bash
docker-compose up --build
```
