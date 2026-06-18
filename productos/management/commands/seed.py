from django.core.management.base import BaseCommand
from productos.models import Producto


class Command(BaseCommand):
    help = 'Seed the database with example products (if none exist)'

    def handle(self, *args, **options):
        if Producto.objects.exists():
            self.stdout.write(self.style.WARNING('Productos ya existen. No se sembró nada.'))
            return

        sample = [
            {
                'nombre': 'Lámpara de Escritorio Negra',
                'descripcion': 'Lámpara LED con brazo ajustable y brillo regulable.',
                'precio': '49.90',
                'imagen_url': 'https://example.com/lampara.jpg',
            },
            {
                'nombre': 'Monitor de Oficina FHD 24"',
                'descripcion': 'Monitor 24 pulgadas Full HD, entrada HDMI y VGA.',
                'precio': '199.99',
                'imagen_url': 'https://example.com/monitor.jpg',
            },
            {
                'nombre': 'Ratón Óptico Rojo Gamer',
                'descripcion': 'Ratón ergonómico con iluminación RGB y 6 botones.',
                'precio': '29.50',
                'imagen_url': 'https://example.com/raton.jpg',
            },
            {
                'nombre': 'Auriculares de Diadema Azul',
                'descripcion': 'Auriculares con cancelación pasiva y micrófono integrado.',
                'precio': '59.00',
                'imagen_url': 'https://example.com/auriculares.jpg',
            },
            {
                'nombre': 'Teclado Mecánico Clásico',
                'descripcion': 'Teclado mecánico con switches táctiles y retroiluminación.',
                'precio': '99.99',
                'imagen_url': 'https://example.com/teclado.jpg',
            },
        ]

        objs = [Producto(**p) for p in sample]
        Producto.objects.bulk_create(objs)
        self.stdout.write(self.style.SUCCESS('Sembrado 5 productos de ejemplo.'))
