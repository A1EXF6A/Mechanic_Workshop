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
        if request.env.user._is_public():
            return request.redirect('/taller/login?redirect=/taller/cita')
        return request.render('taller_mecanico.cita_page', {})

    @http.route(['/taller/cita/user-data'], type='json', auth="user", website=True)
    def taller_cita_user_data(self):
        partner = request.env.user.partner_id
        vehiculos = request.env['taller.vehiculo'].sudo().search([('usuario_id', '=', partner.id)])
        data = {
            'name': partner.name or '',
            'phone': partner.mobile or partner.phone or '',
        }
        if len(vehiculos) == 1:
            v = vehiculos[0]
            data['brand'] = f"{v.marca} {v.modelo}"
            data['plate'] = v.matricula or ''
        return data

    @http.route(['/taller/registro'], type='http', auth="public", website=True)
    def taller_registro(self, **kw):
        return request.render('taller_mecanico.registro_page', {})

    @http.route(['/taller/login'], type='http', auth="public", website=True)
    def taller_login(self, **kw):
        redirect = kw.get('redirect', '/')
        return request.render('taller_mecanico.login_page', {'redirect': redirect})

    @http.route(['/taller/login/submit'], type='http', auth="public", website=True, methods=['POST'])
    def taller_login_submit(self, **post):
        email = (post.get('email') or '').strip()
        password = post.get('password') or ''
        redirect = (post.get('redirect') or '/')
        try:
            request.session.authenticate(
                request.db,
                {'type': 'password', 'login': email, 'password': password},
            )
            return request.redirect(redirect)
        except Exception:
            return request.render('taller_mecanico.login_page', {'login_error': True, 'redirect': redirect})

    @http.route(['/taller/logout'], type='http', auth="public", website=True)
    def taller_logout(self, **kw):
        request.session.logout()
        return request.redirect('/')

    @http.route(['/taller/mis-vehiculos'], type='http', auth="user", website=True)
    def taller_mis_vehiculos(self, **kw):
        partner = request.env.user.partner_id
        vehiculos = request.env['taller.vehiculo'].sudo().search([('usuario_id', '=', partner.id)])
        return request.render('taller_mecanico.mis_vehiculos_page', {'vehiculos': vehiculos})

    @http.route(['/taller/mis-vehiculos/submit'], type='http', auth="user", website=True, methods=['POST'])
    def taller_mis_vehiculos_submit(self, **post):
        partner = request.env.user.partner_id
        request.env['taller.vehiculo'].sudo().create({
            'matricula': (post.get('matricula') or '').strip(),
            'marca': (post.get('marca') or '').strip(),
            'modelo': (post.get('modelo') or '').strip(),
            'anio': int(post.get('anio') or 0) or False,
            'color': (post.get('color') or '').strip(),
            'usuario_id': partner.id,
        })
        return request.redirect('/taller/mis-vehiculos')

    @http.route(['/taller/registro/submit'], type='http', auth="public", website=True, methods=['POST'])
    def taller_registro_submit(self, **post):
        nombre = (post.get('nombre') or '').strip()
        apellido = (post.get('apellido') or '').strip()
        email = (post.get('email') or '').strip()
        password = post.get('password') or ''
        try:
            Partner = request.env['res.partner'].sudo()
            partner = Partner.create({
                'name': f"{nombre} {apellido}",
                'email': email,
                'street': (post.get('direccion') or '').strip(),
                'mobile': (post.get('celular') or '').strip(),
                'cedula': (post.get('cedula') or '').strip(),
                'edad': int(post.get('edad') or 0),
            })
            request.env['res.users'].sudo().create({
                'login': email,
                'password': password,
                'partner_id': partner.id,
                'groups_id': [(4, request.env.ref('base.group_portal').id)],
            })
            return request.redirect('/taller/registro/confirmacion')
        except Exception as e:
            return request.render('taller_mecanico.registro_page', {'error': str(e)})
