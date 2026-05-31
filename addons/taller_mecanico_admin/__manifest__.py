{
    'name': 'Taller Mecanico - Administrador',
    'version': '1.0',
    'category': 'Operations',
    'summary': 'Interfaz y permisos para administradores del Taller',
    'description': """
        Añade las vistas, reportes y permisos completos para el rol de administrador.
    """,
    'author': 'Tu Nombre',
    'depends': ['taller_mecanico'],
    'data': [
        'views/res_company_views.xml',
        'views/sri_dashboard_views.xml',
        'views/account_move_views.xml',
        'views/report_invoice_sri.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
