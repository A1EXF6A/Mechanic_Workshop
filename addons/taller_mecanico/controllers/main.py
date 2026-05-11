# pyrefly: ignore [missing-import]
from odoo import http
# pyrefly: ignore [missing-import]
from odoo.http import request

class TallerMecanicoController(http.Controller):

    @http.route(['/taller'], type='http', auth="public", website=True)
    def taller_home(self, **kw):
        return request.redirect('/')

    @http.route(['/taller/servicios'], type='http', auth="public", website=True)
    def taller_servicios(self, **kw):
        return request.render('taller_mecanico.servicios_page', {})

    @http.route(['/taller/contacto'], type='http', auth="public", website=True)
    def taller_contacto(self, **kw):
        return request.render('taller_mecanico.contacto_page', {})

    @http.route(['/taller/cita'], type='http', auth="public", website=True)
    def taller_cita(self, **kw):
        return request.render('taller_mecanico.cita_page', {})
