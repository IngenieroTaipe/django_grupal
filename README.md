# Tienda - Django

> **Laboratorio 09A · IS093A · Semana 11 · UNCP — Facultad de Ingeniería de Sistemas**

Aplicación web funcional desarrollada con **Django 5.x** aplicando el patrón **MTV (Model-Template-View)**. Simula un catálogo de productos tecnológicos con estilo limpio en tonos blanco, negro, azul y rojo.

---

## 👥 Equipo de Trabajo

| #   | Integrante     | Rol Técnico                     |
| --- | -------------- | ------------------------------- |
| 1   | **Barja**      | Arquitecto Django               |
| 2   | **Yauri**      | Desarrollador de Vistas         |
| 3   | **Toribio**    | Ingeniero de Plantillas         |
| 4   | **Sulluchuco** | QA & ORM Validator              |
| 5   | **Navarro**    | Documentación & Soporte General |

---

## 📂 Estructura del Proyecto

```
django_mtv_app/
│
├── .venv/
├── db.sqlite3
├── manage.py
├── README.md
│
├── tienda_proyecto/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── productos/
    ├── migrations/
    │   └── 0001_initial.py
    ├── templates/
    │   ├── base.html
    │   ├── home.html
    │   └── catalogo.html
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    └── apps.py
```

---

## 🧑‍💻 Asignación por Integrante

---

### 1. Barja — Arquitecto Django

**Archivos bajo responsabilidad:**

- `tienda_proyecto/settings.py`
- `tienda_proyecto/urls.py`
- `productos/urls.py`
- `productos/apps.py`

**AVANCE:**

- Inicializó el proyecto con `django-admin startproject` y la app con `startapp`.
- Registró `'productos'` en `INSTALLED_APPS`.
- Configuró el enrutamiento principal incluyendo las rutas de la app con `include()`.
- Definió las URLs locales con `app_name = 'productos'`, dos rutas nombradas (`home`, `catalogo`) y reversibilidad mediante `{% url %}`.

**ACCIONES:**

- Agregar `LANGUAGE_CODE = 'es-pe'` y `TIME_ZONE = 'America/Lima'` en `settings.py` para localización correcta.
- Separar variables sensibles (como `SECRET_KEY`) a un archivo `.env` usando `python-decouple`.
- Añadir una ruta para el panel de administración con datos de ejemplo pre-cargados.
- Considerar un prefijo `/api/` si en el futuro se extiende a REST.

---

### 2. Yauri — Desarrollador de Vistas

**Archivos bajo responsabilidad:**

- `productos/views.py`

**AVANCE**

- Implementó la **FBV** `home(request)`: renderiza `home.html` con un contador de visitas usando `request.session`.
- Implementó la **CBV** `ProductoListView(ListView)`: lista productos, ordena el queryset por precio y pasa contexto personalizado mediante `get_context_data()`.
- Añadió lógica de sembrado automático: si la base de datos está vacía al visitar el sitio, inserta 5 productos de prueba.

**ACCIONES**

- Agregar manejo de excepciones (`try/except`) en la FBV para errores de sesión.
- En la CBV, filtrar productos con `stock__gt=0` y ordenar por precio ascendente usando `queryset = Producto.objects.filter(stock__gt=0).order_by('precio')`.
- Agregar una vista de detalle `ProductoDetailView` para `/catalogo/<pk>/` como extensión opcional.
- Usar `get_object_or_404` en caso de implementar vistas de detalle.

---

### 3. Toribio — Ingeniero de Plantillas

**Archivos bajo responsabilidad:**

- `productos/templates/base.html`
- `productos/templates/home.html`
- `productos/templates/catalogo.html`

**AVANCE**

- Diseñó `base.html` con estructura responsiva (header, nav, main, footer), estilos en línea (blanco/negro/azul/rojo) y bloques `{% block title %}` y `{% block content %}`.
- Implementó herencia en `home.html` y `catalogo.html` con `{% extends 'base.html' %}`.
- Usó filtros de plantillas: `|title` (capitalización), `|date:"d M, Y"` (fecha legible), `|floatformat:2` (precios con 2 decimales).
- Implementó loop `{% for producto in object_list %}` con condicional `{% if producto.stock == 0 %}` para mostrar "Agotado".
- Usó `{% url 'productos:home' %}` y `{% url 'productos:catalogo' %}` en la navegación.

**ACCIONES**

- Mover los estilos CSS a un archivo estático (`productos/static/productos/style.css`) y cargarlos con `{% load static %}`.
- Agregar un bloque `{% block extra_css %}` en `base.html` para estilos específicos por página.
- Añadir paginación en `catalogo.html` usando `{% if is_paginated %}`.
- Mejorar el mensaje vacío `{% empty %}` con un ícono o imagen descriptiva.

---

### 4. Sulluchuco — QA & ORM Validator

**Archivos bajo responsabilidad:**

- `productos/models.py`
- `productos/migrations/`
- `productos/admin.py`
- `productos/tests.py`

**AVANCE**

- Definió el modelo `Producto` con los campos: `nombre`, `descripcion`, `precio`, `fecha_creacion` (`auto_now_add`) e `imagen_url`.
- Implementó `__str__` retornando el `nombre` y `Meta` con `ordering = ['-fecha_creacion']`.
- Agregó validación `MinValueValidator(0)` en `precio` y generó la migración `0002_alter_producto_precio`.
- Escribió una **suite de 13 tests** en `tests.py` (`TestCase`): persistencia del modelo, `__str__`, validación de precio (negativo/cero), ordenamiento, agregación `Avg`, _lazy evaluation_ de QuerySets y smoke tests de las vistas `home`/`catalogo`.
- Registró el modelo en `admin.py` con `@admin.register(Producto)` y `ModelAdmin` personalizado (`list_display`, `list_filter`, `search_fields`, `ordering`).
- Verificó el proyecto con `python manage.py check` (sin errores) y `python manage.py test` (**13 tests, OK**).

**ACCIONES**

- Mantener la cobertura de tests al alta cada vez que se agreguen campos o vistas nuevas.
- Considerar `coverage.py` para medir el porcentaje de cobertura del código.
- Evaluar agregar un campo `stock` (con `PositiveIntegerField`) si el catálogo lo requiere a futuro.

**QuerySets utilizados:**

Este proyecto utiliza el ORM de Django para interactuar con la base de datos SQLite. A continuación se documentan los QuerySets reales empleados en la aplicación con su consulta SQL generada y su salida de ejemplo:

#### 1. Consulta del Catálogo Completo
*   **Código Python:**
    ```python
    # En ProductoListView (se obtiene implícitamente por el genérico ListView)
    Producto.objects.all()
    ```
    *Nota: El ordenamiento se realiza automáticamente de forma descendente por `fecha_creacion` gracias a la clase `Meta` del modelo.*
*   **SQL Equivalente:**
    ```sql
    SELECT "productos_producto"."id", "productos_producto"."nombre", "productos_producto"."descripcion", "productos_producto"."precio", "productos_producto"."fecha_creacion", "productos_producto"."imagen_url" FROM "productos_producto" ORDER BY "productos_producto"."fecha_creacion" DESC;
    ```
*   **Salida Esperada (Seed Data):**
    ```python
    <QuerySet [
        <Producto: Lámpara de Escritorio Negra>,
        <Producto: Monitor de Oficina FHD 24">,
        <Producto: Ratón Óptico Rojo Gamer>,
        <Producto: Auriculares de Diadema Azul>,
        <Producto: Teclado Mecánico Clásico>
    ]>
    ```

#### 2. Obtención de los últimos 3 productos recientes
*   **Código Python (usado en la vista `home`):**
    ```python
    Producto.objects.order_by('-fecha_creacion')[:3]
    ```
*   **SQL Equivalente:**
    ```sql
    SELECT "productos_producto"."id", "productos_producto"."nombre", "productos_producto"."descripcion", "productos_producto"."precio", "productos_producto"."fecha_creacion", "productos_producto"."imagen_url" FROM "productos_producto" ORDER BY "productos_producto"."fecha_creacion" DESC LIMIT 3;
    ```
*   **Salida Esperada:**
    ```python
    <QuerySet [
        <Producto: Lámpara de Escritorio Negra>,
        <Producto: Monitor de Oficina FHD 24">,
        <Producto: Ratón Óptico Rojo Gamer>
    ]>
    ```

#### 3. Conteo de Productos
*   **Código Python:**
    ```python
    Producto.objects.count()
    ```
*   **SQL Equivalente:**
    ```sql
    SELECT COUNT(*) AS "__count" FROM "productos_producto";
    ```
*   **Salida Esperada:**
    ```python
    5
    ```

#### 4. Promedio de Precios de los Productos
*   **Código Python (usado en la vista `home`):**
    ```python
    Producto.objects.aggregate(Avg('precio'))['precio__avg']
    ```
*   **SQL Equivalente:**
    ```sql
    SELECT AVG("productos_producto"."precio") AS "precio__avg" FROM "productos_producto";
    ```
*   **Salida Esperada:**
    ```python
    94.876
    ```

> **Lazy evaluation (Evaluación Perezosa):** Los QuerySets en Django **no ejecutan** la consulta SQL al momento de definirse. La consulta real a la base de datos ocurre únicamente cuando el resultado se evalúa: al iterar con `for`, al llamar `list()`, al acceder por índice, o al usar `len()`. Esto permite encadenar filtros y ordenamientos sin costo adicional de consultas intermedias.

---

### 5. Navarro — Documentación & Soporte General

**Archivos bajo responsabilidad:**

- `README.md`
- `.gitignore`
- Revisión transversal de todos los archivos del equipo

**AVANCE**

- Redactó la documentación del proyecto (este archivo).
- Configuró el `.gitignore` para excluir `.venv/`, `db.sqlite3`, `__pycache__/`, `.env` y `*.pyc`.
- Apoyó en la verificación final (`python manage.py check`) y validación de que ambas rutas renderizan sin errores 500/404.
- Tomó capturas del catálogo renderizado y de la estructura de carpetas para el entregable.

**ACCIONES**

- Completar el diagrama MTV en este README (ver sección siguiente).
- Agregar instrucciones de despliegue en producción (Gunicorn + WhiteNoise para estáticos).
- Documentar los QuerySets con ejemplos de salida esperada.
- Agregar una sección de capturas de pantalla embebidas en el README.

---

## 🔄 Diagrama MTV — Flujo de una Petición

```
Cliente (Navegador)
        │
        │  HTTP Request GET /catalogo/
        ▼
┌─────────────────────┐
│   urls.py (Router)  │  tienda_proyecto/urls.py → productos/urls.py
│   path('catalogo/') │  Identifica la vista responsable
└────────┬────────────┘
         │
         ▼
┌─────────────────────────┐
│  View (ProductoListView) │  productos/views.py
│  CBV - ListView          │  Consulta el Model, prepara contexto
└────────┬────────────────┘
         │
         ▼
┌─────────────────────┐
│   Model (Producto)  │  productos/models.py
│   ORM QuerySet      │  Producto.objects.all()
└────────┬────────────┘
         │  datos
         ▼
┌─────────────────────────┐
│  Template (catalogo.html)│  productos/templates/
│  Herencia de base.html   │  Renderiza HTML con datos reales
└────────┬────────────────┘
         │
         ▼
   HTTP Response
 (HTML al navegador)
```

---

## 🚀 Pasos para Ejecutar la Aplicación

### Requisitos previos

- Python 3.10 o superior instalado
- Git (opcional, para clonar el repositorio)

### 1. Clonar o descomprimir el proyecto

```bash
# Opción A: desde GitHub
git clone <url-del-repositorio>
cd django_mtv_app

# Opción B: desde ZIP
# Descomprimir y abrir la carpeta del proyecto
```

### 2. Crear y activar el entorno virtual

```bash
# Crear entorno virtual
python -m venv .venv

# Activar en Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Activar en Windows (CMD)
.venv\Scripts\activate.bat

# Activar en Linux / macOS
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install "django>=5.0,<6.0"
```

### 4. Aplicar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Verificar que el proyecto esté limpio

```bash
python manage.py check
# Salida esperada: System check identified no issues (0 silenced).
```

### 6. (Opcional) Crear superusuario para el Admin

```bash
python manage.py createsuperuser
```

### 7. Ejecutar el servidor de desarrollo

```bash
python manage.py runserver
```

### 8. Abrir en el navegador

| URL                               | Descripción                                    |
| --------------------------------- | ---------------------------------------------- |
| `http://127.0.0.1:8000/`          | Página de inicio (FBV con contador de visitas) |
| `http://127.0.0.1:8000/catalogo/` | Catálogo de productos (CBV ListView)           |
| `http://127.0.0.1:8000/admin/`    | Panel de administración Django                 |

> **Nota:** Al visitar el sitio por primera vez con la base de datos vacía, se insertan automáticamente 5 productos de prueba.

---

## 📋 Rúbrica de Evaluación — Laboratorio 09A

| Criterio                                                  | Peso | Responsable |
| --------------------------------------------------------- | ---- | ----------- |
| Configuración Django correcta (MTV, apps, settings, urls) | 20%  | Barja       |
| Vistas FBV + CBV funcionales con contexto válido          | 20%  | Yauri       |
| Plantillas con herencia, bloques, tags y filtros          | 20%  | Toribio     |
| Modelo definido, migraciones aplicadas, ORM queries       | 25%  | Sulluchuco  |
| Documentación, validación técnica y trabajo colaborativo  | 15%  | Navarro     |

---
