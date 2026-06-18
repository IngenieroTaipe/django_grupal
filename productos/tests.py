"""
Pruebas de QA y validación del ORM para la app `productos`.

Responsable: Sulluchuco — QA & ORM Validator.

Cubre:
  - Creación y persistencia del modelo Producto.
  - Representación `__str__`.
  - Validación de `precio` con MinValueValidator (no negativos).
  - Ordenamiento por defecto del Meta (`-fecha_creacion`).
  - Los QuerySets reales usados por las vistas (home / catálogo).
"""

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.test import TestCase
from django.urls import reverse

from .models import Producto


class ProductoModelTest(TestCase):
    """Valida la definición y el comportamiento del modelo Producto."""

    def setUp(self):
        self.producto = Producto.objects.create(
            nombre="Teclado Mecánico",
            descripcion="Switches azules táctiles.",
            precio=Decimal("89.99"),
        )

    def test_creacion_persiste_en_bd(self):
        """Un producto creado debe quedar almacenado y recuperable."""
        self.assertEqual(Producto.objects.count(), 1)
        guardado = Producto.objects.get(pk=self.producto.pk)
        self.assertEqual(guardado.nombre, "Teclado Mecánico")
        self.assertEqual(guardado.precio, Decimal("89.99"))

    def test_str_devuelve_nombre(self):
        """`__str__` debe retornar el nombre (útil en admin y shell)."""
        self.assertEqual(str(self.producto), "Teclado Mecánico")

    def test_fecha_creacion_se_asigna_automaticamente(self):
        """`fecha_creacion` usa auto_now_add, no debe ser nula."""
        self.assertIsNotNone(self.producto.fecha_creacion)

    def test_campos_opcionales_pueden_quedar_vacios(self):
        """`descripcion` e `imagen_url` son opcionales."""
        p = Producto.objects.create(nombre="Mouse", precio=Decimal("35.50"))
        p.full_clean()  # no debe lanzar ValidationError
        self.assertEqual(p.descripcion, "")
        self.assertIsNone(p.imagen_url)

    def test_precio_negativo_es_invalido(self):
        """MinValueValidator(0) debe rechazar precios negativos."""
        producto = Producto(nombre="Erróneo", precio=Decimal("-1.00"))
        with self.assertRaises(ValidationError):
            producto.full_clean()

    def test_precio_cero_es_valido(self):
        """Un precio de 0 (producto gratuito/promocional) es válido."""
        producto = Producto(nombre="Promo", precio=Decimal("0.00"))
        producto.full_clean()  # no debe lanzar ValidationError


class ProductoOrderingTest(TestCase):
    """Valida el ordenamiento por defecto definido en Meta."""

    def test_ordering_por_fecha_descendente(self):
        primero = Producto.objects.create(nombre="Primero", precio=Decimal("10.00"))
        segundo = Producto.objects.create(nombre="Segundo", precio=Decimal("20.00"))
        # El más reciente debe aparecer primero (ordering = ['-fecha_creacion']).
        nombres = list(Producto.objects.values_list("nombre", flat=True))
        self.assertEqual(nombres, ["Segundo", "Primero"])
        self.assertGreaterEqual(segundo.fecha_creacion, primero.fecha_creacion)


class QuerySetTest(TestCase):
    """Valida los QuerySets y agregaciones usados por las vistas."""

    @classmethod
    def setUpTestData(cls):
        cls.precios = [Decimal("10.00"), Decimal("20.00"), Decimal("30.00")]
        for i, precio in enumerate(cls.precios):
            Producto.objects.create(nombre=f"Producto {i}", precio=precio)

    def test_promedio_precio_aggregate(self):
        """Avg('precio') replica el cálculo de la FBV home()."""
        promedio = Producto.objects.aggregate(Avg("precio"))["precio__avg"]
        self.assertEqual(promedio, Decimal("20.00"))

    def test_ultimos_tres_productos(self):
        """El slice [:3] de la home devuelve a lo más 3 productos."""
        ultimos = Producto.objects.order_by("-fecha_creacion")[:3]
        self.assertEqual(len(ultimos), 3)

    def test_queryset_es_lazy(self):
        """Definir un QuerySet no ejecuta SQL hasta que se evalúa."""
        qs = Producto.objects.filter(precio__gt=Decimal("15.00"))
        self.assertIsNone(qs._result_cache, "El QuerySet no debe estar evaluado aún")
        evaluado = list(qs)  # fuerza la evaluación
        self.assertEqual(len(evaluado), 2)


class VistasTest(TestCase):
    """Pruebas de integración de las vistas (smoke tests de QA)."""

    def test_home_responde_200_y_siembra_datos(self):
        """La home auto-siembra 5 productos cuando la BD está vacía."""
        self.assertEqual(Producto.objects.count(), 0)
        respuesta = self.client.get(reverse("productos:home"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(Producto.objects.count(), 5)

    def test_catalogo_responde_200(self):
        respuesta = self.client.get(reverse("productos:catalogo"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("productos", respuesta.context)

    def test_contador_de_visitas_incrementa(self):
        """El contador de sesión debe incrementar entre visitas."""
        self.client.get(reverse("productos:home"))
        respuesta = self.client.get(reverse("productos:home"))
        self.assertEqual(respuesta.context["num_visitas"], 2)
