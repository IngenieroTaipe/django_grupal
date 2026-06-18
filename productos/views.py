from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Avg
from .models import Producto

def auto_seed_db():
    """
    Seeds the database with classic products if it is empty.
    """
    if Producto.objects.count() == 0:
        productos_mock = [
            {
                "nombre": "Teclado Mecánico Clásico",
                "descripcion": "Teclado mecánico con switches azules táctiles, retroiluminación azul y diseño ergonómico clásico.",
                "precio": 89.99,
                "imagen_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&q=80&w=600"
            },
            {
                "nombre": "Auriculares de Diadema Azul",
                "descripcion": "Auriculares inalámbricos con sonido estéreo nítido, diadema ajustable en color azul cobalto y batería de larga duración.",
                "precio": 120.00,
                "imagen_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&q=80&w=600"
            },
            {
                "nombre": "Ratón Óptico Rojo Gamer",
                "descripcion": "Ratón de alta precisión con luces LED color rojo, botones laterales configurables y diseño ergonómico.",
                "precio": 35.50,
                "imagen_url": "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?auto=format&fit=crop&q=80&w=600"
            },
            {
                "nombre": "Monitor de Oficina FHD 24\"",
                "descripcion": "Pantalla plana Full HD ideal para productividad diaria. Colores fieles y filtro de luz azul.",
                "precio": 199.99,
                "imagen_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&q=80&w=600"
            },
            {
                "nombre": "Lámpara de Escritorio Negra",
                "descripcion": "Lámpara minimalista en color negro con brazo flexible y control de brillo táctil.",
                "precio": 29.90,
                "imagen_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&q=80&w=600"
            }
        ]
        for p in productos_mock:
            Producto.objects.create(**p)

def home(request):
    """
    FBV for the home page.
    """
    auto_seed_db()
    total_productos = Producto.objects.count()
    promedio_precio = Producto.objects.aggregate(Avg('precio'))['precio__avg'] or 0.0
    ultimos_productos = Producto.objects.order_by('-fecha_creacion')[:3]
    
    # Visit counter using sessions
    num_visitas = request.session.get('num_visitas', 0) + 1
    request.session['num_visitas'] = num_visitas
    
    context = {
        'total_productos': total_productos,
        'promedio_precio': promedio_precio,
        'ultimos_productos': ultimos_productos,
        'num_visitas': num_visitas,
        'titulo_pagina': 'Inicio'
    }
    return render(request, 'home.html', context)

class ProductoListView(ListView):
    """
    CBV for listing products in a catalog.
    """
    model = Producto
    template_name = 'catalogo.html'
    context_object_name = 'productos'

    def get(self, request, *args, **kwargs):
        auto_seed_db()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Catálogo'
        context['total_total'] = Producto.objects.count()
        return context


