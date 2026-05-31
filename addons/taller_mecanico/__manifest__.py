{
    'name': 'Taller Mecanico - Core',
    'version': '1.0',
    'category': 'Operations',
    'summary': 'Módulo Base para el Taller Mecánico',
    'description': """
        Contiene los modelos principales de vehículos, citas y órdenes de trabajo.
    """,
    'author': 'Tu Nombre',
    'depends': ['stock', 'sale', 'account', 'usuarios_taller', 'contacts', 'hr', 'mail', 'payment_stripe', 'payment_paypal'],
    'external_dependencies': {
        'python': ['requests'],
    },
    'data': [
        'security/taller_security.xml',
        'security/ir.model.access.csv',
        'data/product.product.csv',
        'data/stock_init_data.xml',
        'data/demo_data.xml',
        'views/menus.xml',
        'views/vehiculo_views.xml',
        'views/orden_trabajo_views.xml',
        'views/cita_taller_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
