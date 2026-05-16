{
    'name': 'Citas Estado Vehículo',
    'version': '1.0',
    'depends': ['base', 'usuarios_taller', 'taller_vehiculo'],
    'data': [
        'security/ir.model.access.csv',
        'views/tipo_citas_views.xml',
        'views/citas_views.xml',
        
    ],
    'installable': True,
    'application': True,
}