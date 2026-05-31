# pyrefly: ignore [missing-import]
from odoo import http
# pyrefly: ignore [missing-import]
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class TallerMecanicoController(http.Controller):

    @http.route(['/taller'], type='http', auth="public", website=True)
    def taller_home(self, **kw):
        return request.redirect('/')

    @http.route(['/taller/mi_cuenta'], type='http', auth="public", website=True)
    def taller_mi_cuenta(self, **kw):
        user_id = request.session.get('taller_user_id')
        if not user_id:
            return request.redirect('/taller/login')
        
        user = request.env['usuarios_taller.user_profile'].sudo().browse(user_id)
        if not user.exists():
            request.session.pop('taller_user_id', None)
            return request.redirect('/taller/login')

        vehiculos = request.env['taller.vehiculo'].sudo().search([('propietario_id', '=', user.id)])
        citas = request.env['taller.cita'].sudo().search([('cliente_id', '=', user.id)], order='fecha_cita desc')
        
        # Obtener las órdenes de trabajo a partir de los vehículos del cliente
        ordenes = request.env['taller.orden.trabajo'].sudo().search([('vehiculo_id', 'in', vehiculos.ids)], order='fecha_ingreso desc')

        # Obtener facturas del cliente
        facturas = request.env['account.move'].sudo().search([
            ('partner_id', '=', user.partner_id.id),
            ('move_type', '=', 'out_invoice')
        ], order='invoice_date desc') if user.partner_id else []

        return request.render('taller_mecanico_portal.mi_cuenta_page', {
            'user': user,
            'vehiculos': vehiculos,
            'citas': citas,
            'ordenes': ordenes,
            'facturas': facturas,
        })


    @http.route(['/taller/consulta'], type='http', auth="public", website=True, methods=['GET', 'POST'])
    def taller_consulta(self, **post):
        placa = (post.get('placa') or '').strip().upper()
        if request.httprequest.method == 'POST' and placa:
            ordenes = request.env['taller.orden.trabajo'].sudo().search([
                ('vehiculo_id.placa', '=', placa)
            ], order='fecha_ingreso desc')
            return request.render('taller_mecanico_portal.consulta_orden_page', {
                'searched': True,
                'ordenes': ordenes,
                'placa': placa
            })
        return request.render('taller_mecanico_portal.consulta_orden_page', {
            'searched': False,
            'ordenes': [],
            'placa': ''
        })

    @http.route(['/taller/cita'], type='http', auth="public", website=True)
    def taller_cita(self, **kw):
        marcas = request.env['taller.marca'].sudo().search([])
        error = kw.get('error')
        error_msg = None
        if error == 'fecha_requerida':
            error_msg = 'Por favor, selecciona una fecha y hora.'
        elif error == 'formato_invalido':
            error_msg = 'El formato de la fecha es inválido.'
        elif error == 'horario_ocupado':
            error_msg = 'Horario no disponible. Por favor, selecciona otra hora o día.'
        elif error == 'taller_cerrado_domingo':
            error_msg = 'El taller está cerrado los domingos.'
        elif error == 'fuera_horario_semana':
            error_msg = 'Las citas de lunes a viernes deben programarse entre las 08:00 y las 17:00 (el taller cierra a las 18:00).'
        elif error == 'fuera_horario_sabado':
            error_msg = 'Las citas los sábados deben programarse entre las 09:00 y las 13:00 (el taller cierra a las 14:00).'
        return request.render('taller_mecanico_portal.cita_page', {'marcas': marcas, 'error_msg': error_msg})

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

        # 3.1. Validación de Horarios del Taller (Lunes-Viernes 8-18, Sabado 9-14, Domingo Cerrado)
        day = dt_cita.weekday()
        hour = dt_cita.hour
        minute = dt_cita.minute
        time_val = hour + minute / 60.0

        if day == 6: # Domingo
            return request.redirect('/taller/cita?error=taller_cerrado_domingo')
        elif 0 <= day <= 4: # Lunes a Viernes
            if not (8.0 <= time_val <= 17.0):
                return request.redirect('/taller/cita?error=fuera_horario_semana')
        elif day == 5: # Sábado
            if not (9.0 <= time_val <= 13.0):
                return request.redirect('/taller/cita?error=fuera_horario_sabado')

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

        # Validación de Horarios del Taller (Lunes-Viernes 8-18, Sabado 9-14, Domingo Cerrado)
        day = dt_cita.weekday()
        hour = dt_cita.hour
        minute = dt_cita.minute
        time_val = hour + minute / 60.0

        if day == 6: # Domingo
            return {'available': False, 'message': 'El taller está cerrado los domingos.'}
        elif 0 <= day <= 4: # Lunes a Viernes
            if not (8.0 <= time_val <= 17.0):
                return {'available': False, 'message': 'Las citas de lunes a viernes deben programarse entre las 08:00 y las 17:00 (el taller cierra a las 18:00).'}
        elif day == 5: # Sábado
            if not (9.0 <= time_val <= 13.0):
                return {'available': False, 'message': 'Las citas los sábados deben programarse entre las 09:00 y las 13:00 (el taller cierra a las 14:00).'}
            
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
        return request.render('taller_mecanico_portal.cita_confirmacion_page', {})

    @http.route(['/taller/registro'], type='http', auth="public", website=True)
    def taller_registro(self, **kw):
        return request.render('taller_mecanico_portal.registro_page', {})

    @http.route(['/taller/login'], type='http', auth="public", website=True)
    def taller_login(self, **kw):
        return request.render('taller_mecanico_portal.login_page', {})

    @http.route(['/taller/registro/confirmacion'], type='http', auth="public", website=True)
    def taller_registro_confirmacion(self, **kw):
        return request.render('taller_mecanico_portal.registro_confirmacion_page', {})

    @http.route(['/taller/login/submit'], type='http', auth="public", website=True, methods=['POST'])
    def taller_login_submit(self, **post):
        email = (post.get('email') or '').strip()
        password = post.get('password') or ''
        
        # 1. Intentar autenticación nativa de Odoo (Superadministrador / Usuarios Backend)
        try:
            db_name = request.env.cr.dbname
            odoo_user = request.env['res.users'].sudo().search([('login', '=', email)], limit=1)
            if odoo_user:
                # En Odoo 18, request.session.authenticate recibe (db, credential_dict)
                request.session.authenticate(db_name, {
                    'login': email,
                    'password': password,
                    'type': 'password'
                })
                return request.redirect('/web')
        except Exception:
            pass

        # 2. Intentar autenticación con el portal del Taller
        user = request.env['usuarios_taller.user_profile'].sudo().search([
            ('email', '=', email),
            ('password', '=', password),
        ], limit=1)
        if user:
            request.session['taller_user_id'] = user.id
            return request.redirect('/')
            
        return request.render('taller_mecanico_portal.login_page', {'login_error': True})

    @http.route(['/taller/logout'], type='http', auth="public", website=True)
    def taller_logout(self, **kw):
        request.session.pop('taller_user_id', None)
        return request.redirect('/')

    @http.route(['/taller/registro/submit'], type='http', auth="public", website=True, methods=['POST'])
    def taller_registro_submit(self, **post):
        user = request.env['usuarios_taller.user_profile'].sudo().create({
            'cedula': post.get('cedula'),
            'nombre': post.get('nombre'),
            'apellido': post.get('apellido'),
            'email': post.get('email'),
            'direccion': post.get('direccion'),
            'password': post.get('password'),
            'celular': post.get('celular'),
            'edad': int(post.get('edad') or 0),
        })

        # Enviar correo de confirmación de registro
        mail_values = {
            'subject': 'Confirmación de Registro - Taller Mecánico',
            'email_from': 'joelpstudy10@gmail.com',
            'body_html': f"""
                <div style="font-family: 'Poppins', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 12px; background-color: #ffffff;">
                    <div style="text-align: center; margin-bottom: 20px; border-bottom: 2px solid #3b82f6; padding-bottom: 15px;">
                        <h2 style="color: #1e3a8a; margin: 0; font-size: 24px; font-weight: 700;">¡Bienvenido al Taller Mecánico!</h2>
                    </div>
                    <div style="color: #334155; font-size: 16px; line-height: 1.6;">
                        <p>Estimado/a <strong>{user.nombre} {user.apellido}</strong>,</p>
                        <p>Nos complace informarte que tu registro en nuestra plataforma se ha completado con éxito.</p>
                        
                        <div style="background-color: #f8fafc; padding: 15px; border-radius: 8px; margin: 20px 0; border: 1px solid #cbd5e1;">
                            <h4 style="margin-top: 0; margin-bottom: 10px; color: #1e3a8a;">Detalles de tu cuenta:</h4>
                            <ul style="margin: 0; padding-left: 20px; color: #475569;">
                                <li style="margin-bottom: 5px;"><strong>Nombre Completo:</strong> {user.nombre} {user.apellido}</li>
                                <li style="margin-bottom: 5px;"><strong>Cédula:</strong> {user.cedula}</li>
                                <li style="margin-bottom: 5px;"><strong>Correo Electrónico:</strong> {user.email}</li>
                                <li style="margin-bottom: 5px;"><strong>Celular:</strong> {user.celular}</li>
                            </ul>
                        </div>
                        
                        <p>Ahora puedes acceder a nuestro portal para agendar tus citas de mantenimiento, hacer seguimiento en tiempo real de tus vehículos y comprar repuestos.</p>
                        
                        <div style="text-align: center; margin-top: 30px; margin-bottom: 20px;">
                            <a href="{request.httprequest.url_root}taller/login" style="background-color: #3b82f6; color: #ffffff; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">Ingresar al Portal</a>
                        </div>
                    </div>
                    <div style="text-align: center; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 15px; font-size: 12px; color: #64748b;">
                        <p>Este es un correo automático. Por favor no respondas a este mensaje.</p>
                        <p>&copy; Taller Mecánico. Todos los derechos reservados.</p>
                    </div>
                </div>
            """,
            'email_to': user.email,
        }
        try:
            mail = request.env['mail.mail'].sudo().create(mail_values)
            mail.send()
            _logger.info('Correo de confirmación enviado exitosamente a %s', user.email)
        except Exception as e:
            _logger.error('Error al enviar correo de confirmación a %s: %s', user.email, str(e))

        return request.redirect('/taller/registro/confirmacion')

    @http.route(['/taller/factura/<int:factura_id>/pdf'], type='http', auth="public")
    def taller_factura_pdf(self, factura_id, **kw):
        user_id = request.session.get('taller_user_id')
        if not user_id:
            return request.redirect('/taller/login')
        user = request.env['usuarios_taller.user_profile'].sudo().browse(user_id)
        if not user.exists() or not user.partner_id:
            return request.redirect('/taller/login')
            
        factura = request.env['account.move'].sudo().browse(factura_id)
        if factura.partner_id.id != user.partner_id.id:
            return request.redirect('/taller/mi_cuenta')
            
        pdf, _ = request.env['ir.actions.report'].sudo()._render_qweb_pdf('account.account_invoices', [factura.id])
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf)), ('Content-Disposition', f'attachment; filename={factura.name.replace("/", "_")}.pdf')]
        return request.make_response(pdf, headers=pdfhttpheaders)

    @http.route(['/taller/factura/<int:factura_id>/xml'], type='http', auth="public")
    def taller_factura_xml(self, factura_id, **kw):
        user_id = request.session.get('taller_user_id')
        if not user_id:
            return request.redirect('/taller/login')
        user = request.env['usuarios_taller.user_profile'].sudo().browse(user_id)
        if not user.exists() or not user.partner_id:
            return request.redirect('/taller/login')
            
        factura = request.env['account.move'].sudo().browse(factura_id)
        if factura.partner_id.id != user.partner_id.id or not factura.sri_xml_file:
            return request.redirect('/taller/mi_cuenta')
            
        import base64
        xml_data = base64.b64decode(factura.sri_xml_file)
        headers = [('Content-Type', 'application/xml'), 
                   ('Content-Disposition', f'attachment; filename={factura.sri_xml_filename or "factura.xml"}')]
        return request.make_response(xml_data, headers=headers)
