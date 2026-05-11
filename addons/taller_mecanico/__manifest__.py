{
    'name': 'Taller Mecánico',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Sitio web para el taller mecánico',
    'description': """
        Módulo para el sitio web del taller mecánico.
        Incluye páginas estáticas: Inicio, Servicios, Contacto y Formulario de Cita.
    """,
    'author': 'Tu Nombre',
    'depends': ['website'],
    'data': [
        'views/pages/home.xml',
        'views/pages/servicios.xml',
        'views/pages/contacto.xml',
        'views/pages/cita.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
