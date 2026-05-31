from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _get_frontend_session_info(cls):
        session_info = super()._get_frontend_session_info()
        taller_user_id = request.session.get('taller_user_id')
        if taller_user_id:
            user = request.env['usuarios_taller.user_profile'].sudo().browse(taller_user_id).exists()
            if user:
                session_info['taller_user_name'] = f"{user.nombre} {user.apellido}"
                session_info['taller_user_id'] = user.id
        return session_info
