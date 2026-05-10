from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError


class MathOperationAPI(http.Controller):

    def _serialize_record(self, rec):
        return {
            'id': rec.id,
            'name': rec.name,
            'operand_1': rec.operand_1,
            'operand_2': rec.operand_2,
            'operation_type': rec.operation_type,
            'result': rec.result,
            'operation_date': str(rec.operation_date) if rec.operation_date else None,
            'user_id': rec.user_id.id if rec.user_id else None,
            'user_name': rec.user_id.name if rec.user_id else None,
            'notes': rec.notes,
            'active': rec.active,  # Añadido para incluir el estado activo
        }

    # LISTAR
    @http.route('/api/operations', type='json', auth='public', methods=['POST'], csrf=False)
    def get_operations(self, **kwargs):
        records = request.env['math.operation'].sudo().search([])
        data = [self._serialize_record(rec) for rec in records]

        return {
            'success': True,
            'count': len(data),
            'data': data
        }

    # CONSULTAR POR ID
    @http.route('/api/operations/get', type='json', auth='public', methods=['POST'], csrf=False)
    def get_operation_by_id(self, record_id):

        rec = request.env['math.operation'].sudo().browse(record_id)

        if not rec.exists():
            return {
                'success': False,
                'message': 'Registro no encontrado'
            }

        return {
            'success': True,
            'data': self._serialize_record(rec)
        }

    # CREAR
    @http.route('/api/operations/create', type='json', auth='public', methods=['POST'], csrf=False)
    def create_operation(self, operand_1=None, operand_2=None, operation_type=None, notes=None):
        if operand_1 is None or operand_2 is None or operation_type is None:
            return {
                'success': False,
                'message': 'Faltan parámetros obligatorios'
            }
        try:

            vals = {
                'operand_1': operand_1,
                'operand_2': operand_2,
                'operation_type': operation_type,
                'notes': notes,
            }

            rec = request.env['math.operation'].sudo().create(vals)

            return {
                'success': True,
                'message': 'Operación creada correctamente',
                'data': self._serialize_record(rec)
            }

        except ValidationError as e:
            return {
                'success': False,
                'message': str(e)
            }

        except Exception as e:
            return {
                'success': False,
                'message': f'Error interno: {str(e)}'
            }

    # ACTUALIZAR
    @http.route('/api/operations/update', type='json', auth='public', methods=['POST'], csrf=False)
    def update_operation(self, record_id, **kwargs):

        rec = request.env['math.operation'].sudo().browse(record_id)

        if not rec.exists():
            return {
                'success': False,
                'message': 'Registro no encontrado'
            }

        try:

            vals = {}

            if 'operand_1' in kwargs:
                vals['operand_1'] = kwargs.get('operand_1')

            if 'operand_2' in kwargs:
                vals['operand_2'] = kwargs.get('operand_2')

            if 'operation_type' in kwargs:
                vals['operation_type'] = kwargs.get('operation_type')

            if 'notes' in kwargs:
                vals['notes'] = kwargs.get('notes')

            rec.write(vals)

            return {
                'success': True,
                'message': 'Operación actualizada correctamente',
                'data': self._serialize_record(rec)
            }

        except ValidationError as e:
            return {
                'success': False,
                'message': str(e)
            }

        except Exception as e:
            return {
                'success': False,
                'message': f'Error interno: {str(e)}'
            }

    # ELIMINAR
    @http.route('/api/operations/delete', type='json', auth='public', methods=['POST'], csrf=False)
    def delete_operation(self, record_id):
        try:
            rec = request.env['math.operation'].sudo().browse(record_id)

            if not rec.exists():
                return {
                    'success': False,
                    'message': 'Registro no encontrado'
                }

            rec.unlink()

            return {
                'success': True,
                'message': 'Operación eliminada correctamente'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error interno: {str(e)}'
            }

    # ELIMINAR LOGICAMENTE
    @http.route('/api/operations/delete_log', type='json', auth='public', methods=['POST'], csrf=False)
    def delete_operation_logical(self, record_id):
        try:
            rec = request.env['math.operation'].sudo().browse(record_id)

            if not rec.exists():
                return {
                    'success': False,
                    'message': 'Registro no encontrado'
                }

            rec.write({'active': False})

            return {
                'success': True,
                'message': 'Operación desactivada correctamente'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error interno: {str(e)}'
            }