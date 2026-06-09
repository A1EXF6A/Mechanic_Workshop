from odoo.http import request
from odoo import fields
import logging

try:
    # Set up a mock request environment
    env = env
    orden = env['taller.orden.trabajo'].search([('estado', 'in', ['cotizacion_enviada', 'cotizacion_devuelta'])], limit=1)
    if not orden:
        print("No orden found")
    else:
        # Mock what the controller does
        prop = env['taller.propuesta'].sudo().create({
            'orden_id': orden.id,
            'fecha': fields.Datetime.now(),
            'creador_tipo': 'cliente',
            'creador_nombre': "Test Name",
            'notas': "test",
            'linea_servicio_ids': [],
            'linea_repuesto_ids': [],
        })
        print("Created propuesta:", prop.id)
        
        # Test line creation
        env['taller.orden.linea.servicio'].sudo().create({
            'orden_id': orden.id,
            'producto_id': 1,
            'cantidad': 1,
            'precio_unitario': 10.0,
            'is_extra': True,
            'state_extra': 'pendiente',
        })
        print("Created extra service")
        
        orden.write({'estado': 'cotizacion_devuelta'})
        orden.message_post(body="Test")
        print("Finished successfully")
except Exception as e:
    import traceback
    traceback.print_exc()
