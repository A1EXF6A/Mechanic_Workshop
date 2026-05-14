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

    @http.route(['/taller/registro'], type='http', auth="public", website=True)
    def taller_registro(self, **kw):
        return request.render('taller_mecanico.registro_page', {})

    @http.route(['/taller/login'], type='http', auth="public", website=True)
    def taller_login(self, **kw):
        return request.render('taller_mecanico.login_page', {})

    @http.route(['/taller/registro/confirmacion'], type='http', auth="public", website=True)
    def taller_registro_confirmacion(self, **kw):
        return request.render('taller_mecanico.registro_confirmacion_page', {})

    @http.route(['/taller/login/submit'], type='http', auth="public", website=True, methods=['POST'])
    def taller_login_submit(self, **post):
        email = (post.get('email') or '').strip()
        password = post.get('password') or ''
        user = request.env['usuarios_taller.user_profile'].sudo().search([
            ('email', '=', email),
            ('password', '=', password),
        ], limit=1)
        if user:
            request.session['taller_user_id'] = user.id
            return request.redirect('/taller/registro/confirmacion')
        return request.render('taller_mecanico.login_page', {'login_error': True})

    @http.route(['/taller/logout'], type='http', auth="public", website=True)
    def taller_logout(self, **kw):
        request.session.pop('taller_user_id', None)
        return request.redirect('/')

    @http.route(['/taller/registro/submit'], type='http', auth="public", website=True, methods=['POST'])
    def taller_registro_submit(self, **post):
        request.env['usuarios_taller.user_profile'].sudo().create({
            'cedula': post.get('cedula'),
            'nombre': post.get('nombre'),
            'apellido': post.get('apellido'),
            'email': post.get('email'),
            'direccion': post.get('direccion'),
            'password': post.get('password'),
            'celular': post.get('celular'),
            'edad': int(post.get('edad') or 0),
        })
        return request.redirect('/taller/registro/confirmacion')
