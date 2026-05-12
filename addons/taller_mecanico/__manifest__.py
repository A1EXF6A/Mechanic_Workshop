{
    'name': 'Taller Mecanico',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Sitio web para el taller mecanico',
    'description': """
        Modulo para el sitio web del taller mecanico.
        Incluye paginas estaticas: Inicio, Servicios, Contacto y Formulario de Cita.
    """,
    'author': 'Tu Nombre',
    'depends': ['website', 'stock', 'sale', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'data/product.product.csv',
        'views/pages/home.xml',
        'views/pages/servicios.xml',
        'views/pages/contacto.xml',
        'views/pages/cita.xml',
        'views/pages/productos.xml',
        'views/pages/carrito.xml',
        'views/pages/confirmacion.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'assets': {
        'web.assets_frontend': [
            'taller_mecanico/static/src/css/taller_style.css',
            'taller_mecanico/static/src/js/taller_shop.js',
        ],
    },
}
