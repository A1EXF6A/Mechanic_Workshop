# -*- coding: utf-8 -*-
# pyrefly: ignore [missing-import]
from odoo import http
# pyrefly: ignore [missing-import]
from odoo.http import request

class TallerDebugController(http.Controller):
    @http.route('/taller/debug/types', type='json', auth='user')
    def get_product_types(self):
        fields = request.env['product.template'].fields_get(['type'])
        return fields.get('type', {}).get('selection', [])
