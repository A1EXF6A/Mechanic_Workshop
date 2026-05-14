{
    'name': "Vehículos Taller",
    'summary': "Registro de vehículos del taller con historial",
    'author': "Taller",
    'category': 'Workshop',
    'version': '1.0',
    'depends': ['base', 'usuarios_taller'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'installable': True,
    'application': True,
}
