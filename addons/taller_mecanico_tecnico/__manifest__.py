{
    'name': 'Taller Mecanico - Tecnico',
    'version': '1.0',
    'category': 'Operations',
    'summary': 'Interfaz y automatizaciones para mecánicos',
    'description': """
        Vista restringida de Órdenes de Trabajo, Checklist de recepción y automatización de usuarios para empleados.
    """,
    'author': 'Tu Nombre',
    'depends': ['taller_mecanico', 'hr'],
    'data': [
        'views/tecnico_menus.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
