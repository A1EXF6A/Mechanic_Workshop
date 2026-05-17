{
    'name': 'Taller Mecánico',
    'version': '18.0.1.0.0',
    'category': 'Services',
    'summary': 'Gestión de citas, vehículos y órdenes de trabajo',
    'description': """
        Módulo para la gestión integral de un taller mecánico automotriz.
        Permite gestionar vehículos de clientes, agendar citas y llevar el control de las órdenes de trabajo.
    """,
    'author': 'Grupo 5',
    'depends': ['base', 'contacts', 'hr', 'stock', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/menus.xml',
        'views/vehiculo_views.xml',
        'views/orden_trabajo_views.xml',
        'views/cita_taller_views.xml',
        'data/demo_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
