# pyrefly: ignore [missing-import]
from odoo import http
# pyrefly: ignore [missing-import]
from odoo.http import request

class TallerMecanicoController(http.Controller):

    @http.route(['/taller'], type='http', auth="public", website=True)
    def taller_home(self, **kw):
        return request.redirect('/')


    @http.route(['/taller/consulta'], type='http', auth="public", website=True, methods=['GET', 'POST'])
    def taller_consulta(self, **post):
        placa = (post.get('placa') or '').strip().upper()
        if request.httprequest.method == 'POST' and placa:
            ordenes = request.env['taller.orden.trabajo'].sudo().search([
                ('vehiculo_id.placa', '=', placa)
            ], order='fecha_ingreso desc')
            return request.render('taller_mecanico.consulta_orden_page', {
                'searched': True,
                'ordenes': ordenes,
                'placa': placa
            })
        return request.render('taller_mecanico.consulta_orden_page', {
            'searched': False,
            'ordenes': [],
            'placa': ''
        })

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
        fecha_cita_raw = post.get('date')
        if not fecha_cita_raw:
            return request.redirect('/taller/cita?error=fecha_requerida')
            
        # Convertir formato HTML5 (YYYY-MM-DDTHH:MM) a Odoo format (YYYY-MM-DD HH:MM:SS)
        fecha_cita = fecha_cita_raw.replace('T', ' ')
        if len(fecha_cita) == 16:
            fecha_cita += ':00'

        # Validación backend de choques de horario (margen de 1 hora)
        from datetime import datetime, timedelta
        try:
            dt_cita = datetime.strptime(fecha_cita, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return request.redirect('/taller/cita?error=formato_invalido')

        # Buscar citas que solapen (inicio_existente < fin_nuevo AND fin_existente > inicio_nuevo)
        # Como cada cita dura 1 hora, buscamos citas en el rango (dt_cita - 1h, dt_cita + 1h)
        dt_inicio_margen = dt_cita - timedelta(minutes=59)
        dt_fin_margen = dt_cita + timedelta(minutes=59)
        
        choques = env['taller.cita'].sudo().search([
            ('estado', 'in', ['solicitada', 'confirmada']),
            ('fecha_cita', '>', dt_inicio_margen.strftime('%Y-%m-%d %H:%M:%S')),
            ('fecha_cita', '<', dt_fin_margen.strftime('%Y-%m-%d %H:%M:%S'))
        ])

        if choques:
            # Choque detectado en el servidor!
            return request.redirect('/taller/cita?error=horario_ocupado')

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

    @http.route(['/taller/cita/check_availability'], type='json', auth="public", website=True)
    def taller_cita_check_availability(self, date=None, **kw):
        if not date:
            return {'available': False, 'message': 'Fecha requerida'}
            
        fecha_cita = date.replace('T', ' ')
        if len(fecha_cita) == 16:
            fecha_cita += ':00'
            
        from datetime import datetime, timedelta
        try:
            dt_cita = datetime.strptime(fecha_cita, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return {'available': False, 'message': 'Formato inválido'}
            
        dt_inicio_margen = dt_cita - timedelta(minutes=59)
        dt_fin_margen = dt_cita + timedelta(minutes=59)
        
        choques = request.env['taller.cita'].sudo().search([
            ('estado', 'in', ['solicitada', 'confirmada']),
            ('fecha_cita', '>', dt_inicio_margen.strftime('%Y-%m-%d %H:%M:%S')),
            ('fecha_cita', '<', dt_fin_margen.strftime('%Y-%m-%d %H:%M:%S'))
        ])
        
        if choques:
            return {'available': False, 'message': 'Horario no disponible. Por favor, selecciona otra hora o día.'}
            
        return {'available': True, 'message': 'Horario disponible.'}


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
