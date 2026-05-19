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
        marcas = request.env['taller.marca'].sudo().search([])
        return request.render('taller_mecanico.cita_page', {'marcas': marcas})

    @http.route(['/taller/cita/submit'], type='http', auth="public", website=True, methods=['POST'])
    def taller_cita_submit(self, **post):
        env = request.env

        # 1. Procesar Cliente
        nombre_completo = post.get('name', '').strip()
        nombres = nombre_completo.split(' ', 1)
        nombre = nombres[0]
        apellido = nombres[1] if len(nombres) > 1 else 'Sin Apellido'
        
        cedula = post.get('cedula', '').strip()
        email = post.get('email', '').strip()
        celular = post.get('phone', '').strip()

        user = env['usuarios_taller.user_profile'].sudo().search(['|', ('cedula', '=', cedula), ('email', '=', email)], limit=1)
        if not user:
            user = env['usuarios_taller.user_profile'].sudo().create({
                'cedula': cedula,
                'nombre': nombre,
                'apellido': apellido,
                'email': email,
                'celular': celular,
                'direccion': 'Registrado por Web',
                'password': cedula, # Default pass
                'edad': 18, # Default edad
            })

        # 2. Procesar Vehículo
        marca_id = int(post.get('marca_id', 0))
        modelo_str = post.get('modelo', '').strip()
        placa = post.get('plate', '').strip().upper()

        if marca_id and modelo_str:
            modelo = env['taller.modelo'].sudo().search([('name', '=ilike', modelo_str), ('marca_id', '=', marca_id)], limit=1)
            if not modelo:
                modelo = env['taller.modelo'].sudo().create({
                    'name': modelo_str.upper(),
                    'marca_id': marca_id
                })
            modelo_id = modelo.id
        else:
            modelo_id = False

        vehiculo = env['taller.vehiculo'].sudo().search([('placa', '=', placa)], limit=1)
        if not vehiculo:
            vehiculo = env['taller.vehiculo'].sudo().create({
                'placa': placa,
                'marca_id': marca_id,
                'modelo_id': modelo_id,
                'anio': 2020,  # default
                'color': 'otro',  # default válido para campo Selection
                'propietario_id': user.id,
            })

        # 3. Procesar Cita
        fecha_cita = post.get('date')
        repair_type = post.get('repair_type')
        observaciones = post.get('observations', '')

        # Mapeo de valores frontend a backend
        motivo_map = {
            'mantenimiento': 'mantenimiento',
            'motor': 'falla_mecanica',
            'frenos': 'revision',
            'diagnostico': 'revision',
            'otro': 'otro'
        }
        motivo_db = motivo_map.get(repair_type, 'otro')

        cita = env['taller.cita'].sudo().create({
            'cliente_id': user.id,
            'vehiculo_id': vehiculo.id,
            'fecha_cita': fecha_cita,
            'motivo': motivo_db,
            'descripcion': observaciones,
            'estado': 'solicitada',
        })

        return request.redirect('/taller/cita/confirmacion')

    @http.route(['/taller/cita/confirmacion'], type='http', auth="public", website=True)
    def taller_cita_confirmacion(self, **kw):
        return request.render('taller_mecanico.cita_confirmacion_page', {})

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
