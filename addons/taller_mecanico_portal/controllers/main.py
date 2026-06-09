# pyrefly: ignore [missing-import]
from odoo import http, fields
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
        citas = request.env['taller.cita'].sudo().search([('cliente_id', '=', user.id)], order='id desc')
        
        # Obtener las órdenes de trabajo a partir de los vehículos del cliente
        ordenes = request.env['taller.orden.trabajo'].sudo().search([('vehiculo_id', 'in', vehiculos.ids)], order='id desc')

        # Obtener facturas del cliente
        facturas = request.env['account.move'].sudo().search([
            ('partner_id', '=', user.partner_id.id),
            ('move_type', '=', 'out_invoice')
        ], order='id desc') if user.partner_id else []

        marcas = request.env['taller.marca'].sudo().search([])
        servicios_disponibles = request.env['product.product'].sudo().search([('type', '=', 'service'), ('active', '=', True)])
        repuestos_disponibles = request.env['product.product'].sudo().search([('type', '!=', 'service'), ('active', '=', True)])

        error_cita = kw.get('error_cita')
        error_msg_cita = None
        if error_cita == 'fecha_requerida':
            error_msg_cita = 'Por favor, selecciona una fecha y hora.'
        elif error_cita == 'formato_invalido':
            error_msg_cita = 'El formato de la fecha es inválido.'
        elif error_cita == 'horario_ocupado':
            error_msg_cita = 'Horario no disponible. Por favor, selecciona otra hora o día.'
        elif error_cita == 'taller_cerrado_domingo':
            error_msg_cita = 'El taller está cerrado los domingos.'
        elif error_cita == 'fuera_horario_semana':
            error_msg_cita = 'Las citas de lunes a viernes deben programarse entre las 08:00 y las 17:00 (el taller cierra a las 18:00).'
        elif error_cita == 'fuera_horario_sabado':
            error_msg_cita = 'Las citas los sábados deben programarse entre las 09:00 y las 13:00 (el taller cierra a las 14:00).'

        ecuador = request.env['res.country'].sudo().search([('code', '=', 'EC')], limit=1)
        states = request.env['res.country.state'].sudo().search([('country_id', '=', ecuador.id)]) if ecuador else []
        countries = request.env['res.country'].sudo().search([])

        # --- User Statistics ---
        vehiculos_count = len(vehiculos)
        citas_count = len(citas)
        ordenes_count = len(ordenes)
        ordenes_activas = sum(1 for o in ordenes if o.estado != 'entregado')
        ordenes_completadas = ordenes_count - ordenes_activas
        ultima_cita = citas[0] if citas else False
        ultima_orden = ordenes[0] if ordenes else False

        user_stats = {
            'vehiculos_count': vehiculos_count,
            'citas_count': citas_count,
            'ordenes_count': ordenes_count,
            'ordenes_activas': ordenes_activas,
            'ordenes_completadas': ordenes_completadas,
            'ultima_cita': ultima_cita,
            'ultima_orden': ultima_orden,
        }

        return request.render('taller_mecanico_portal.mi_cuenta_page', {
            'user': user,
            'user_stats': user_stats,
            'vehiculos': vehiculos,
            'citas': citas,
            'ordenes': ordenes,
            'facturas': facturas,
            'marcas': marcas,
            'states': states,
            'countries': countries,
            'default_country': ecuador,
            'error_msg_cita': error_msg_cita,
            'servicios_disponibles': servicios_disponibles,
            'repuestos_disponibles': repuestos_disponibles,
        })


    @http.route(['/taller/vehiculo/submit'], type='http', auth="public", website=True, methods=['POST'], csrf=False)
    def taller_vehiculo_submit(self, **post):
        user_id = request.session.get('taller_user_id')
        if not user_id:
            return request.redirect('/taller/login')
        
        placa = (post.get('placa') or '').strip().upper()
        marca_id_raw = post.get('marca_id')
        marca_id = int(marca_id_raw) if marca_id_raw and str(marca_id_raw).isdigit() else 0
        modelo_str = (post.get('modelo') or '').strip()
        anio_raw = post.get('anio')
        anio = int(anio_raw) if anio_raw and str(anio_raw).isdigit() else 2020
        color = (post.get('color') or '').strip()
        if not color:
            color = 'Otro'
        vehiculo_id_raw = post.get('vehiculo_id')
        vehiculo_id = int(vehiculo_id_raw) if vehiculo_id_raw and str(vehiculo_id_raw).strip().isdigit() else False

        env = request.env
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

        foto_b64 = False
        foto_file = post.get('foto')
        try:
            if foto_file and hasattr(foto_file, 'read'):
                file_data = foto_file.read()
                if file_data and len(file_data) > 0:
                    import base64
                    foto_b64 = base64.b64encode(file_data).decode('utf-8')
        except Exception:
            foto_b64 = False

        vals = {
            'placa': placa,
            'marca_id': marca_id,
            'modelo_id': modelo_id,
            'anio': anio,
            'color': color,
        }
        if foto_b64:
            vals['foto'] = foto_b64

        if vehiculo_id: # Edit
            vehiculo = env['taller.vehiculo'].sudo().browse(vehiculo_id)
            if vehiculo.exists() and vehiculo.propietario_id.id == user_id:
                vehiculo.sudo().write(vals)
        else: # Create
            vehiculo = env['taller.vehiculo'].sudo().search([('placa', '=', placa)], limit=1)
            if not vehiculo:
                vals['propietario_id'] = user_id
                env['taller.vehiculo'].sudo().create(vals)
            else:
                return request.redirect('/taller/mi_cuenta?error=placa_existente')

        return request.redirect('/taller/mi_cuenta')

    @http.route(['/taller/vehiculo/delete/<int:vehiculo_id>'], type='http', auth="public", website=True)
    def taller_vehiculo_delete(self, vehiculo_id, **kw):
        user_id = request.session.get('taller_user_id')
        if not user_id:
            return request.redirect('/taller/login')
            
        vehiculo = request.env['taller.vehiculo'].sudo().browse(vehiculo_id)
        if vehiculo.exists() and vehiculo.propietario_id.id == user_id and vehiculo.can_edit_delete:
            vehiculo.sudo().unlink()
            
        return request.redirect('/taller/mi_cuenta')

    @http.route(['/taller/cambiar_password'], type='http', auth="public", website=True, methods=['POST'])
    def taller_cambiar_password(self, **post):
        user_id = request.session.get('taller_user_id')
        if not user_id:
            return request.redirect('/taller/login')
            
        old_password = post.get('old_password')
        new_password = post.get('new_password')
        confirm_password = post.get('confirm_password')
        
        if new_password != confirm_password:
            return request.redirect('/taller/mi_cuenta?error_pass=mismatch')
            
        user = request.env['usuarios_taller.user_profile'].sudo().browse(user_id)
        if user.password != old_password:
            return request.redirect('/taller/mi_cuenta?error_pass=wrong_old')
            
        user.sudo().write({'password': new_password})
        if user.user_id:
            user.user_id.sudo().write({'password': new_password})
            
        return request.redirect('/taller/mi_cuenta?success_pass=1')

    @http.route(['/taller/mi_cuenta/update_foto'], type='http', auth="public", website=True, methods=['POST'])
    def taller_update_foto(self, **post):
        user_id = request.session.get('taller_user_id')
        if not user_id:
            return request.redirect('/taller/login')

        env = request.env
        user = env['usuarios_taller.user_profile'].sudo().browse(user_id)
        if not user.exists():
            return request.redirect('/taller/login')

        foto_file = post.get('foto')
        if foto_file:
            import base64
            try:
                foto_data = base64.b64encode(foto_file.read())
                user.write({'foto': foto_data})
                request.env.cr.commit()
            except Exception as e:
                _logger.error("Error al actualizar la foto de perfil: %s", e)
                return request.redirect('/taller/mi_cuenta?error_foto=1')

        return request.redirect('/taller/mi_cuenta?success_foto=1')

    @http.route(['/taller/mi_cuenta/update_profile'], type='http', auth="public", website=True, methods=['POST'])
    def taller_update_profile(self, **post):
        user_id = request.session.get('taller_user_id')
        if not user_id:
            return request.redirect('/taller/login')

        env = request.env
        user = env['usuarios_taller.user_profile'].sudo().browse(user_id)
        if not user.exists():
            return request.redirect('/taller/login')

        nombre = (post.get('nombre') or '').strip()
        apellido = (post.get('apellido') or '').strip()
        cedula = (post.get('cedula') or '').strip()
        celular = (post.get('celular') or '').strip()
        email = (post.get('email') or '').strip().lower()
        direccion = (post.get('direccion') or '').strip()
        fecha_nacimiento = (post.get('fecha_nacimiento') or '').strip()
        street = (post.get('street') or '').strip()
        street2 = (post.get('street2') or '').strip()
        city = (post.get('city') or '').strip()
        
        state_id_raw = post.get('state_id')
        state_id = int(state_id_raw) if state_id_raw and str(state_id_raw).isdigit() else False
        
        country_id_raw = post.get('country_id')
        country_id = int(country_id_raw) if country_id_raw and str(country_id_raw).isdigit() else False

        if not (nombre and apellido and cedula and celular and email and direccion and fecha_nacimiento):
            return request.redirect('/taller/mi_cuenta?error_profile=campos_requeridos')

        if not celular.isdigit():
            return request.redirect('/taller/mi_cuenta?error_profile=celular_invalido')

        from datetime import datetime, date
        try:
            dob = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
            today = date.today()
            edad = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if edad < 18:
                return request.redirect('/taller/mi_cuenta?error_profile=edad_invalida')
        except ValueError:
            return request.redirect('/taller/mi_cuenta?error_profile=fecha_invalida')

        existing_cedula = env['usuarios_taller.user_profile'].sudo().search([
            ('cedula', '=', cedula),
            ('id', '!=', user.id)
        ], limit=1)
        if existing_cedula:
            return request.redirect('/taller/mi_cuenta?error_profile=cedula_existente')

        existing_email = env['usuarios_taller.user_profile'].sudo().search([
            ('email', '=', email),
            ('id', '!=', user.id)
        ], limit=1)
        if existing_email:
            return request.redirect('/taller/mi_cuenta?error_profile=email_existente')

        try:
            user.write({
                'nombre': nombre,
                'apellido': apellido,
                'cedula': cedula,
                'celular': celular,
                'email': email,
                'direccion': direccion,
                'fecha_nacimiento': fecha_nacimiento,
                'street': street,
                'street2': street2,
                'city': city,
                'state_id': state_id,
                'country_id': country_id,
            })
            if user.user_id:
                user.user_id.sudo().write({
                    'name': f"{nombre} {apellido}",
                })
            request.env.cr.commit()
        except Exception as e:
            _logger.error("Error al actualizar perfil de usuario: %s", e)
            return request.redirect('/taller/mi_cuenta?error_profile=1')

        return request.redirect('/taller/mi_cuenta?success_profile=1')

    @http.route(['/taller/consulta'], type='http', auth="public", website=True, methods=['GET', 'POST'])
    def taller_consulta(self, **post):
        placa = (post.get('placa') or '').strip().upper()
        if request.httprequest.method == 'POST' and placa:
            ordenes = request.env['taller.orden.trabajo'].sudo().search([
                ('vehiculo_id.placa', '=', placa)
            ], order='id desc')
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
        return request.redirect('/taller/mi_cuenta')

    @http.route(['/taller/cita/submit'], type='http', auth="public", website=True, methods=['POST'])
    def taller_cita_submit(self, **post):
        user_id = request.session.get('taller_user_id')
        if not user_id:
            return request.redirect('/taller/login')

        env = request.env
        user = env['usuarios_taller.user_profile'].sudo().browse(user_id)
        if not user.exists():
            return request.redirect('/taller/login')

        # 2. Procesar Vehículo
        vehiculo_id_raw = post.get('vehiculo_id')
        if vehiculo_id_raw and vehiculo_id_raw != 'new':
            vehiculo = env['taller.vehiculo'].sudo().browse(int(vehiculo_id_raw))
        else:
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
            return request.redirect('/taller/mi_cuenta?error_cita=fecha_requerida')
            
        # Convertir formato HTML5 (YYYY-MM-DDTHH:MM) a Odoo format (YYYY-MM-DD HH:MM:SS)
        fecha_cita = fecha_cita_raw.replace('T', ' ')
        if len(fecha_cita) == 16:
            fecha_cita += ':00'

        # Validación backend de choques de horario (margen de 1 hora)
        from datetime import datetime, timedelta
        import pytz
        try:
            dt_local = datetime.strptime(fecha_cita, '%Y-%m-%d %H:%M:%S')
            user_tz = pytz.timezone(request.env.user.tz or 'America/Guayaquil')
            dt_utc = user_tz.localize(dt_local).astimezone(pytz.utc).replace(tzinfo=None)
            fecha_cita_utc = dt_utc.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            return request.redirect('/taller/mi_cuenta?error_cita=formato_invalido')

        # 3.1. Validación de Horarios del Taller (Lunes-Viernes 8-18, Sabado 9-14, Domingo Cerrado)
        day = dt_local.weekday()
        hour = dt_local.hour
        minute = dt_local.minute
        time_val = hour + minute / 60.0

        if day == 6: # Domingo
            return request.redirect('/taller/mi_cuenta?error_cita=taller_cerrado_domingo')
        elif 0 <= day <= 4: # Lunes a Viernes
            if not (8.0 <= time_val <= 17.0):
                return request.redirect('/taller/mi_cuenta?error_cita=fuera_horario_semana')
        elif day == 5: # Sábado
            if not (9.0 <= time_val <= 13.0):
                return request.redirect('/taller/mi_cuenta?error_cita=fuera_horario_sabado')

        # Buscar citas que solapen (inicio_existente < fin_nuevo AND fin_existente > inicio_nuevo)
        # Como cada cita dura 1 hora, buscamos citas en el rango (dt_utc - 1h, dt_utc + 1h)
        dt_inicio_margen = dt_utc - timedelta(minutes=59)
        dt_fin_margen = dt_utc + timedelta(minutes=59)
        
        choques = env['taller.cita'].sudo().search([
            ('estado', 'in', ['solicitada', 'confirmada']),
            ('fecha_cita', '>', dt_inicio_margen.strftime('%Y-%m-%d %H:%M:%S')),
            ('fecha_cita', '<', dt_fin_margen.strftime('%Y-%m-%d %H:%M:%S'))
        ])

        if choques:
            # Choque detectado en el servidor!
            return request.redirect('/taller/mi_cuenta?error_cita=horario_ocupado')

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
            'fecha_cita': fecha_cita_utc,
            'motivo': motivo_db,
            'descripcion': observaciones,
            'estado': 'solicitada',
        })

        return request.redirect('/taller/mi_cuenta?success_cita=1')

    @http.route(['/taller/cita/get_week_slots'], type='json', auth="public", website=True)
    def taller_cita_get_week_slots(self, week_start=None, **kw):
        from datetime import datetime, timedelta
        import pytz

        user_tz = pytz.timezone(request.env.user.tz or 'America/Guayaquil')
        now_local = datetime.now(pytz.utc).astimezone(user_tz)

        if not week_start:
            # Default to current week's Monday
            today = now_local.date()
            days_since_monday = today.weekday()
            monday = today - timedelta(days=days_since_monday)
            week_start_date = monday
        else:
            try:
                week_start_date = datetime.strptime(week_start, '%Y-%m-%d').date()
            except ValueError:
                return {'success': False, 'message': 'Formato inválido'}

        # Get all citas for the entire week range in one query
        dt_week_start = user_tz.localize(datetime.combine(week_start_date, datetime.min.time()))
        dt_week_end = user_tz.localize(datetime.combine(week_start_date + timedelta(days=6), datetime.max.time()))

        dt_utc_start = dt_week_start.astimezone(pytz.utc).replace(tzinfo=None)
        dt_utc_end = dt_week_end.astimezone(pytz.utc).replace(tzinfo=None)

        citas_existentes = request.env['taller.cita'].sudo().search([
            ('estado', 'in', ['solicitada', 'confirmada']),
            ('fecha_cita', '>=', dt_utc_start.strftime('%Y-%m-%d %H:%M:%S')),
            ('fecha_cita', '<=', dt_utc_end.strftime('%Y-%m-%d %H:%M:%S'))
        ])

        # Build a dict: date_str -> set of taken hours
        taken_map = {}
        for cita in citas_existentes:
            if cita.fecha_cita:
                cita_local = pytz.utc.localize(cita.fecha_cita).astimezone(user_tz)
                date_key = cita_local.strftime('%Y-%m-%d')
                if date_key not in taken_map:
                    taken_map[date_key] = set()
                taken_map[date_key].add(cita_local.hour)

        days_data = []
        day_names_es = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
        month_names_es = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']

        for i in range(6):  # Mon to Sat only
            current_date = week_start_date + timedelta(days=i)
            weekday = current_date.weekday()

            if weekday == 6:  # Sunday - skip
                continue

            start_hour = 8 if weekday <= 4 else 9
            end_hour = 17 if weekday <= 4 else 13

            date_str = current_date.strftime('%Y-%m-%d')
            taken_hours = taken_map.get(date_str, set())

            slots = []
            for h in range(start_hour, end_hour + 1):
                is_past = False
                if current_date == now_local.date() and h <= now_local.hour:
                    is_past = True
                elif current_date < now_local.date():
                    is_past = True

                slots.append({
                    'time': f"{h:02d}:00",
                    'hour': h,
                    'available': not is_past and (h not in taken_hours)
                })

            day_label = f"{day_names_es[weekday]}, {current_date.day} {month_names_es[current_date.month - 1]}"
            days_data.append({
                'date': date_str,
                'label': day_label,
                'slots': slots
            })

        return {
            'success': True,
            'week_start': week_start_date.strftime('%Y-%m-%d'),
            'week_end': (week_start_date + timedelta(days=5)).strftime('%Y-%m-%d'),
            'days': days_data
        }

    @http.route(['/taller/cita/cancelar'], type='http', auth="public", website=True, methods=['POST'])
    def taller_cita_cancelar(self, **post):
        user_id = request.session.get('taller_user_id')
        if not user_id:
            return request.redirect('/taller/login')

        env = request.env
        user = env['usuarios_taller.user_profile'].sudo().browse(user_id)
        if not user.exists():
            return request.redirect('/taller/login')

        cita_id = int(post.get('cita_id', 0))
        if not cita_id:
            return request.redirect('/taller/mi_cuenta?error_cita=cita_no_encontrada')

        cita = env['taller.cita'].sudo().browse(cita_id)
        if not cita.exists():
            return request.redirect('/taller/mi_cuenta?error_cita=cita_no_encontrada')

        # Asegurar que la cita pertenezca al usuario logueado
        if cita.cliente_id.id != user.id:
            return request.redirect('/taller/mi_cuenta?error_cita=no_autorizado')

        # Permitir cancelar si el estado es solicitada o confirmada
        if cita.estado in ['solicitada', 'confirmada']:
            if cita.orden_trabajo_id and (cita.orden_trabajo_id.estado in ['listo', 'entregado'] or cita.orden_trabajo_id.factura_id):
                return request.redirect('/taller/mi_cuenta?error_cita=orden_en_progreso')
                
            cita.action_cancelar()
            request.env.cr.commit()
            return request.redirect('/taller/mi_cuenta?success_cita=cancelada')
        else:
            return request.redirect('/taller/mi_cuenta?error_cita=estado_invalido')

    @http.route(['/taller/cita/check_availability'], type='json', auth="public", website=True)
    def taller_cita_check_availability(self, date=None, **kw):
        if not date:
            return {'available': False, 'message': 'Fecha requerida'}
            
        fecha_cita = date.replace('T', ' ')
        if len(fecha_cita) == 16:
            fecha_cita += ':00'
            
        from datetime import datetime, timedelta
        import pytz
        try:
            dt_local = datetime.strptime(fecha_cita, '%Y-%m-%d %H:%M:%S')
            user_tz = pytz.timezone(request.env.user.tz or 'America/Guayaquil')
            dt_utc = user_tz.localize(dt_local).astimezone(pytz.utc).replace(tzinfo=None)
        except ValueError:
            return {'available': False, 'message': 'Formato inválido'}

        # Validación de Horarios del Taller (Lunes-Viernes 8-18, Sabado 9-14, Domingo Cerrado)
        day = dt_local.weekday()
        hour = dt_local.hour
        minute = dt_local.minute
        time_val = hour + minute / 60.0

        if day == 6: # Domingo
            return {'available': False, 'message': 'El taller está cerrado los domingos.'}
        elif 0 <= day <= 4: # Lunes a Viernes
            if not (8.0 <= time_val <= 17.0):
                return {'available': False, 'message': 'Las citas de lunes a viernes deben programarse entre las 08:00 y las 17:00 (el taller cierra a las 18:00).'}
        elif day == 5: # Sábado
            if not (9.0 <= time_val <= 13.0):
                return {'available': False, 'message': 'Las citas los sábados deben programarse entre las 09:00 y las 13:00 (el taller cierra a las 14:00).'}
            
        dt_inicio_margen = dt_utc - timedelta(minutes=59)
        dt_fin_margen = dt_utc + timedelta(minutes=59)
        
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
        ecuador = request.env['res.country'].sudo().search([('code', '=', 'EC')], limit=1)
        states = request.env['res.country.state'].sudo().search([('country_id', '=', ecuador.id)]) if ecuador else []
        countries = request.env['res.country'].sudo().search([])
        return request.render('taller_mecanico_portal.registro_page', {
            'states': states,
            'countries': countries,
            'default_country': ecuador,
            'error': kw.get('error'),
            'post_data': kw,
        })

    @http.route(['/taller/login'], type='http', auth="public", website=True)
    def taller_login(self, **kw):
        return request.render('taller_mecanico_portal.login_page', {})

    @http.route(['/taller/registro/confirmacion'], type='http', auth="public", website=True)
    def taller_registro_confirmacion(self, **kw):
        return request.render('taller_mecanico_portal.registro_confirmacion_page', {})

    @http.route(['/taller/verificar'], type='http', auth="public", website=True)
    def taller_verificar_cuenta(self, token=None, **kw):
        if not token:
            return request.render('taller_mecanico_portal.login_page', {
                'unverified_error': True,
                'error_msg': 'Token de verificación no proporcionado o inválido.'
            })
        
        user = request.env['usuarios_taller.user_profile'].sudo().search([('verification_token', '=', token)], limit=1)
        if not user:
            return request.render('taller_mecanico_portal.login_page', {
                'unverified_error': True,
                'error_msg': 'El enlace de verificación es inválido o ya ha sido utilizado.'
            })
            
        user.write({
            'is_verified': True,
        })
        request.env.cr.commit()
        
        return request.render('taller_mecanico_portal.login_page', {
            'verified_success': True
        })

    @http.route(['/taller/login/submit'], type='http', auth="public", website=True, methods=['POST'])
    def taller_login_submit(self, **post):
        login_input = (post.get('email') or '').strip()
        password = post.get('password') or ''
        db_name = request.env.cr.dbname
        
        # 1. Intentar autenticación nativa de Odoo (Superadministrador / Usuarios Backend)
        try:
            odoo_user = request.env['res.users'].sudo().search([('login', '=', login_input)], limit=1)
            if odoo_user and odoo_user.has_group('base.group_user'):
                request.session.authenticate(db_name, {
                    'login': login_input,
                    'password': password,
                    'type': 'password'
                })
                return request.redirect('/web')
        except Exception:
            pass

        # 2. Intentar autenticación con el portal del Taller (Por email o por cedula)
        taller_user = request.env['usuarios_taller.user_profile'].sudo().search([
            '|', ('email', '=', login_input), ('cedula', '=', login_input),
            ('password', '=', password),
        ], limit=1)
        if taller_user:
            if not taller_user.is_verified:
                return request.render('taller_mecanico_portal.login_page', {'unverified_error': True})
            request.session['taller_user_id'] = taller_user.id
            
            # Asegurar que exista un res.users portal dedicado para este perfil
            if not taller_user.user_id and taller_user.partner_id:
                # Usar un login único basado en el partner_id para evitar colisiones
                portal_login = f"taller_{taller_user.partner_id.id}@portal"
                existing_portal = request.env['res.users'].sudo().search([
                    ('login', '=', portal_login)
                ], limit=1)
                if existing_portal:
                    taller_user.sudo().write({'user_id': existing_portal.id})
                else:
                    try:
                        portal_group = request.env.ref('base.group_portal')
                        new_user = request.env['res.users'].sudo().with_context(no_reset_password=True).create({
                            'name': f"{taller_user.nombre} {taller_user.apellido}",
                            'login': portal_login,
                            'password': password,
                            'partner_id': taller_user.partner_id.id,
                            'groups_id': [(6, 0, [portal_group.id])],
                        })
                        taller_user.sudo().write({'user_id': new_user.id})
                        _logger.info('Usuario portal creado: %s para %s', portal_login, login_input)
                    except Exception as e:
                        _logger.warning('No se pudo crear usuario portal para %s: %s', login_input, e)

            # Autenticar nativamente en Odoo como usuario portal
            if taller_user.user_id:
                portal_login = taller_user.user_id.login
                # Sincronizar contraseña y hacer commit antes de authenticate
                taller_user.user_id.sudo().write({'password': password})
                request.env.cr.commit()
                try:
                    request.session.authenticate(db_name, {
                        'login': portal_login,
                        'password': password,
                        'type': 'password'
                    })
                except Exception as e:
                    _logger.warning('Error en autenticación nativa para %s: %s', portal_login, e)

            return request.redirect('/')
            
        return request.render('taller_mecanico_portal.login_page', {'login_error': True})

    @http.route(['/taller/registro/submit'], type='http', auth="public", website=True, methods=['POST'])
    def taller_registro_submit(self, **post):
        # 1. Validar que las contraseñas coincidan
        password = post.get('password') or ''
        confirm_password = post.get('confirm_password') or ''
        
        # Recuperar datos para volver a renderizar si hay error
        ecuador = request.env['res.country'].sudo().search([('code', '=', 'EC')], limit=1)
        states = request.env['res.country.state'].sudo().search([('country_id', '=', ecuador.id)]) if ecuador else []
        countries = request.env['res.country'].sudo().search([])
        
        render_error_args = {
            'states': states,
            'countries': countries,
            'default_country': ecuador,
            'post_data': post,
        }

        if password != confirm_password:
            render_error_args['error'] = 'passwords_mismatch'
            return request.render('taller_mecanico_portal.registro_page', render_error_args)

        # 2. Calcular edad y validar fecha de nacimiento
        fecha_nacimiento_str = post.get('fecha_nacimiento') or ''
        if not fecha_nacimiento_str:
            render_error_args['error'] = 'missing_dob'
            return request.render('taller_mecanico_portal.registro_page', render_error_args)
        
        try:
            from datetime import datetime
            dob = datetime.strptime(fecha_nacimiento_str, '%Y-%m-%d').date()
            today = datetime.today().date()
            edad = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if edad < 18:
                render_error_args['error'] = 'underage'
                return request.render('taller_mecanico_portal.registro_page', render_error_args)
        except Exception:
            render_error_args['error'] = 'invalid_dob'
            return request.render('taller_mecanico_portal.registro_page', render_error_args)

        # 3. Validar cédula única y email único
        cedula = (post.get('cedula') or '').strip()
        email = (post.get('email') or '').strip()
        
        existing_cedula = request.env['usuarios_taller.user_profile'].sudo().search([('cedula', '=', cedula)], limit=1)
        if existing_cedula:
            render_error_args['error'] = 'cedula_exists'
            return request.render('taller_mecanico_portal.registro_page', render_error_args)
            
        existing_email = request.env['usuarios_taller.user_profile'].sudo().search([('email', '=', email)], limit=1)
        if existing_email:
            render_error_args['error'] = 'email_exists'
            return request.render('taller_mecanico_portal.registro_page', render_error_args)

        # 4. Formatear dirección completa
        street = post.get('street') or ''
        street2 = post.get('street2') or ''
        city = post.get('city') or ''
        direccion = f"{street}, {street2}, {city}".strip(', ') or 'Ambato'

        # 5. Crear el perfil de taller
        try:
            user = request.env['usuarios_taller.user_profile'].sudo().create({
                'cedula': cedula,
                'nombre': post.get('nombre'),
                'apellido': post.get('apellido'),
                'email': email,
                'direccion': direccion,
                'street': street,
                'street2': street2,
                'city': city,
                'state_id': int(post.get('state_id') or 0) or False,
                'country_id': int(post.get('country_id') or 0) or False,
                'fecha_nacimiento': fecha_nacimiento_str,
                'password': password,
                'celular': post.get('celular'),
                'edad': edad,
            })
        except Exception as e:
            _logger.error("Error al registrar usuario del taller: %s", e)
            render_error_args['error'] = 'create_failed'
            return request.render('taller_mecanico_portal.registro_page', render_error_args)

        # Enviar correo de confirmación de registro
        mail_values = {
            'subject': 'Verifica tu cuenta - Taller Mecánico',
            'email_from': 'joelpstudy10@gmail.com',
            'body_html': f"""
                <div style="font-family: 'Poppins', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 12px; background-color: #ffffff;">
                    <div style="text-align: center; margin-bottom: 20px; border-bottom: 2px solid #3b82f6; padding-bottom: 15px;">
                        <h2 style="color: #1e3a8a; margin: 0; font-size: 24px; font-weight: 700;">¡Verifica tu cuenta de Taller Mecánico!</h2>
                    </div>
                    <div style="color: #334155; font-size: 16px; line-height: 1.6;">
                        <p>Estimado/a <strong>{user.nombre} {user.apellido}</strong>,</p>
                        <p>Gracias por registrarte en nuestra plataforma. Para poder ingresar a tu cuenta, por favor verifica tu dirección de correo electrónico haciendo clic en el siguiente enlace:</p>
                        
                        <div style="text-align: center; margin-top: 30px; margin-bottom: 20px;">
                            <a href="{request.httprequest.url_root}taller/verificar?token={user.verification_token}" style="background-color: #3b82f6; color: #ffffff; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">Verificar mi Cuenta</a>
                        </div>
                        
                        <div style="background-color: #f8fafc; padding: 15px; border-radius: 8px; margin: 20px 0; border: 1px solid #cbd5e1;">
                            <h4 style="margin-top: 0; margin-bottom: 10px; color: #1e3a8a;">Detalles de tu registro:</h4>
                            <ul style="margin: 0; padding-left: 20px; color: #475569;">
                                <li style="margin-bottom: 5px;"><strong>Nombre Completo:</strong> {user.nombre} {user.apellido}</li>
                                <li style="margin-bottom: 5px;"><strong>Cédula (Usuario):</strong> {user.cedula}</li>
                                <li style="margin-bottom: 5px;"><strong>Correo Electrónico:</strong> {user.email}</li>
                            </ul>
                        </div>
                        
                        <p>Si el botón no funciona, puedes copiar y pegar el siguiente enlace en tu navegador:</p>
                        <p style="word-break: break-all; color: #3b82f6;">{request.httprequest.url_root}taller/verificar?token={user.verification_token}</p>
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
            _logger.info('Correo de verificación enviado exitosamente a %s', user.email)
        except Exception as e:
            _logger.error('Error al enviar correo de verificación a %s: %s', user.email, str(e))

        return request.redirect('/taller/registro/confirmacion')

    @http.route(['/taller/logout'], type='http', auth="public", website=True)
    def taller_logout(self, **kw):
        request.session.pop('taller_user_id', None)
        request.session.logout()
        return request.redirect('/')

    @http.route(['/taller/orden/linea/extra/update'], type='json', auth="public", website=True, methods=['POST'])
    def taller_orden_linea_extra_update(self, line_id, line_type, action, **kw):
        try:
            user_id = request.session.get('taller_user_id')
            if not user_id:
                return {'success': False, 'error': 'Sesión no iniciada'}
            
            user = request.env['usuarios_taller.user_profile'].sudo().browse(user_id)
            if not user.exists():
                return {'success': False, 'error': 'Usuario no válido'}
                
            model_name = 'taller.orden.linea.servicio' if line_type == 'servicio' else 'taller.orden.linea.repuesto'
            line = request.env[model_name].sudo().browse(int(line_id))
            if not line.exists():
                return {'success': False, 'error': 'Línea no encontrada'}
                
            if line.orden_id.vehiculo_id.propietario_id.id != user.id:
                return {'success': False, 'error': 'No autorizado para modificar esta orden'}
                
            if action not in ['aprobado', 'rechazado', 'pendiente']:
                return {'success': False, 'error': 'Acción inválida'}
                
            line.write({'state_extra': action})
            line.orden_id.message_post(
                body=f"El cliente ha marcado la línea {line.producto_id.name} como: {action.upper()}."
            )
            return {'success': True}
        except Exception as e:
            import traceback
            _logger.error("Error en update extra: %s", traceback.format_exc())
            return {'success': False, 'error': f"Error en update extra: {str(e)}"}

    @http.route(['/taller/orden/cotizacion/action'], type='json', auth="public", website=True, methods=['POST'])
    def taller_orden_cotizacion_action(self, orden_id, action, **kw):
        user_id = request.session.get('taller_user_id')
        if not user_id:
            return {'success': False, 'error': 'Sesión no iniciada'}
            
        user = request.env['usuarios_taller.user_profile'].sudo().browse(user_id)
        if not user.exists():
            return {'success': False, 'error': 'Usuario no válido'}
            
        orden = request.env['taller.orden.trabajo'].sudo().browse(int(orden_id))
        if not orden.exists():
            return {'success': False, 'error': 'Orden no encontrada'}
            
        if orden.vehiculo_id.propietario_id.id != user.id:
            return {'success': False, 'error': 'No autorizado para modificar esta orden'}
            
        if orden.estado not in ['cotizacion_enviada', 'cotizacion_devuelta']:
            return {'success': False, 'error': 'La orden no está en fase de cotización'}
            
        if action == 'aprobar':
            # Verificar que no haya pendientes
            pendientes = any(l.state_extra == 'pendiente' for l in orden.servicio_linea_ids) or \
                         any(l.state_extra == 'pendiente' for l in orden.repuesto_linea_ids)
            if pendientes:
                return {'success': False, 'error': 'Por favor, aprueba o rechaza todas las líneas pendientes antes de confirmar la propuesta.'}
                
            orden.write({'estado': 'cotizacion_aprobada'})
            orden.message_post(body="El cliente ha APROBADO la propuesta de trabajo.")
            
        elif action == 'devolver':
            orden.write({'estado': 'cotizacion_devuelta'})
            orden.message_post(body="El cliente ha DEVUELTO la propuesta con modificaciones.")
            
        else:
            return {'success': False, 'error': 'Acción inválida'}
            
        return {'success': True}

    @http.route(['/taller/orden/propuesta/crear'], type='json', auth="public", website=True, methods=['POST'])
    def taller_orden_propuesta_crear(self, orden_id, notas, servicios, repuestos, action='devolver', **kw):
        try:
            user_id = request.session.get('taller_user_id')
            if not user_id:
                return {'success': False, 'error': 'Sesión no iniciada'}
                
            user = request.env['usuarios_taller.user_profile'].sudo().browse(user_id)
            if not user.exists():
                return {'success': False, 'error': 'Usuario no válido'}
                
            orden = request.env['taller.orden.trabajo'].sudo().browse(int(orden_id))
            if not orden.exists():
                return {'success': False, 'error': 'Orden no encontrada'}
                
            if orden.vehiculo_id.propietario_id.id != user.id:
                return {'success': False, 'error': 'No autorizado para modificar esta orden'}
                
            if orden.estado not in ['cotizacion_enviada', 'cotizacion_devuelta', 'cotizacion_aprobada']:
                return {'success': False, 'error': 'La orden no está en fase de cotización o ya está lista/entregada'}
                
            # Parse proposed services
            lineas_servicios = []
            for s in servicios:
                prod_id = int(s.get('producto_id'))
                qty = float(s.get('cantidad', 1.0))
                prod = request.env['product.product'].sudo().browse(prod_id)
                if prod.exists():
                    lineas_servicios.append((0, 0, {
                        'producto_id': prod.id,
                        'cantidad': qty,
                        'precio_unitario': prod.list_price,
                    }))
                    
            # Parse proposed parts
            lineas_repuestos = []
            for r in repuestos:
                prod_id = int(r.get('producto_id'))
                qty = float(r.get('cantidad', 1.0))
                prod = request.env['product.product'].sudo().browse(prod_id)
                if prod.exists():
                    lineas_repuestos.append((0, 0, {
                        'producto_id': prod.id,
                        'cantidad': qty,
                        'precio_unitario': prod.list_price,
                    }))
                    
            # Crear propuesta
            if notas or lineas_servicios or lineas_repuestos:
                prop = request.env['taller.propuesta'].sudo().create({
                    'orden_id': orden.id,
                    'fecha': fields.Datetime.now(),
                    'creador_tipo': 'cliente',
                    'creador_nombre': f"{user.nombre} {user.apellido}",
                    'notas': notas,
                    'linea_servicio_ids': lineas_servicios,
                    'linea_repuesto_ids': lineas_repuestos,
                })
            
            # Opcionalmente, agregar las líneas a la orden de trabajo como extra
            new_serv_ids = []
            new_rep_ids = []
            for s in servicios:
                prod_id = int(s.get('producto_id'))
                qty = float(s.get('cantidad', 1.0))
                prod = request.env['product.product'].sudo().browse(prod_id)
                if prod.exists():
                    nl = request.env['taller.orden.linea.servicio'].sudo().create({
                        'orden_id': orden.id,
                        'producto_id': prod.id,
                        'cantidad': qty,
                        'precio_unitario': prod.list_price,
                        'is_extra': True,
                        'state_extra': 'aprobado' if action == 'aprobar' else 'pendiente',
                        'agregado_por_cliente': True,
                    })
                    new_serv_ids.append(nl.id)
            for r in repuestos:
                prod_id = int(r.get('producto_id'))
                qty = float(r.get('cantidad', 1.0))
                prod = request.env['product.product'].sudo().browse(prod_id)
                if prod.exists():
                    nl = request.env['taller.orden.linea.repuesto'].sudo().create({
                        'orden_id': orden.id,
                        'producto_id': prod.id,
                        'cantidad': qty,
                        'precio_unitario': prod.list_price,
                        'is_extra': True,
                        'state_extra': 'aprobado' if action == 'aprobar' else 'pendiente',
                        'agregado_por_cliente': True,
                    })
                    new_rep_ids.append(nl.id)
            
            # Save the global notes to the work order
            orden.sudo().write({'notas_cliente_propuesta': notas})

            # Update the order status
            if action == 'aprobar':
                orden.sudo().write({'estado': 'cotizacion_aprobada'})
                orden.message_post(body=f"El cliente ha APROBADO la propuesta de trabajo, incluyendo sus modificaciones directas.")
            else:
                orden.sudo().write({'estado': 'cotizacion_devuelta'})
                orden.message_post(body=f"El cliente ha DEVUELTO la propuesta con peticiones/comentarios: {notas or 'Sin comentarios'}")
            
            # Send email to technician and admins
            if notas or new_serv_ids or new_rep_ids:
                admin_users = request.env.ref('taller_mecanico.group_taller_manager').sudo().users
                emails = [u.email for u in admin_users if u.email]
                if orden.tecnico_id and orden.tecnico_id.work_email:
                    emails.append(orden.tecnico_id.work_email)
                
                if emails:
                    unique_emails = list(set(emails))
                    subject = f"Modificaciones del Cliente en Orden {orden.name} - Vehículo {orden.vehiculo_id.placa}"
                    
                    previous_html = ""
                    for s in orden.servicio_linea_ids.filtered(lambda x: x.id not in new_serv_ids):
                        previous_html += f"<tr><td style='padding:8px; border-bottom:1px solid #e2e8f0;'>[Servicio] {s.producto_id.name}</td><td style='padding:8px; border-bottom:1px solid #e2e8f0; text-align:center;'>{s.cantidad}</td><td style='padding:8px; border-bottom:1px solid #e2e8f0; text-align:right;'>${s.subtotal:.2f}</td></tr>"
                    for r in orden.repuesto_linea_ids.filtered(lambda x: x.id not in new_rep_ids):
                        previous_html += f"<tr><td style='padding:8px; border-bottom:1px solid #e2e8f0;'>[Repuesto] {r.producto_id.name}</td><td style='padding:8px; border-bottom:1px solid #e2e8f0; text-align:center;'>{r.cantidad}</td><td style='padding:8px; border-bottom:1px solid #e2e8f0; text-align:right;'>${r.subtotal:.2f}</td></tr>"
                    if not previous_html:
                        previous_html = "<tr><td colspan='3' style='padding:8px; text-align:center; color:#94a3b8;'>La orden estaba vacía.</td></tr>"

                    added_html = ""
                    for s in orden.servicio_linea_ids.filtered(lambda x: x.id in new_serv_ids):
                        added_html += f"<tr><td style='padding:8px; border-bottom:1px solid #e2e8f0; color:#047857; font-weight:500;'>[Servicio] {s.producto_id.name}</td><td style='padding:8px; border-bottom:1px solid #e2e8f0; text-align:center; color:#047857;'>{s.cantidad}</td><td style='padding:8px; border-bottom:1px solid #e2e8f0; text-align:right; color:#047857;'>${s.subtotal:.2f}</td></tr>"
                    for r in orden.repuesto_linea_ids.filtered(lambda x: x.id in new_rep_ids):
                        added_html += f"<tr><td style='padding:8px; border-bottom:1px solid #e2e8f0; color:#047857; font-weight:500;'>[Repuesto] {r.producto_id.name}</td><td style='padding:8px; border-bottom:1px solid #e2e8f0; text-align:center; color:#047857;'>{r.cantidad}</td><td style='padding:8px; border-bottom:1px solid #e2e8f0; text-align:right; color:#047857;'>${r.subtotal:.2f}</td></tr>"
                    if not added_html:
                        added_html = "<tr><td colspan='3' style='padding:8px; text-align:center; color:#94a3b8;'>El cliente no añadió ítems del catálogo.</td></tr>"

                    body_html = f"""
                    <div style="font-family: 'Inter', Helvetica, Arial, sans-serif; max-width: 600px; margin: 0 auto; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                        <div style="background: linear-gradient(135deg, #0ea5e9, #0284c7); padding: 30px; text-align: center; color: white;">
                            <h1 style="margin: 0; font-size: 24px; font-weight: 700;">Modificaciones del Cliente</h1>
                            <p style="margin: 6px 0 0 0; color: #e0f2fe; font-size: 14px;">El cliente ha devuelto o aprobado la propuesta con modificaciones</p>
                        </div>
                        <div style="padding: 30px; background-color: white;">
                            <h3 style="color: #334155; margin-top: 0; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px;">Datos del Cliente y Vehículo</h3>
                            <table style="width: 100%; font-size: 14px; margin-bottom: 24px; border-collapse: collapse;">
                                <tr><td style="padding: 4px 0; color: #64748b; width: 40%;">Cliente:</td><td style="padding: 4px 0; color: #0f172a; font-weight: 600;">{user.nombre} {user.apellido}</td></tr>
                                <tr><td style="padding: 4px 0; color: #64748b;">Vehículo:</td><td style="padding: 4px 0; color: #0f172a; font-weight: 600;">{orden.vehiculo_id.marca_id.name} {orden.vehiculo_id.modelo_id.name} ({orden.vehiculo_id.placa})</td></tr>
                                <tr><td style="padding: 4px 0; color: #64748b;">Orden de Trabajo:</td><td style="padding: 4px 0; color: #0f172a; font-weight: 600;">{orden.name}</td></tr>
                            </table>

                            <h3 style="color: #334155; margin-top: 0; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px;">Ítems Pre-existentes</h3>
                            <table style="width: 100%; font-size: 13px; margin-bottom: 24px; border-collapse: collapse;">
                                <thead>
                                    <tr style="background-color: #f8fafc; color: #64748b; text-align: left;">
                                        <th style="padding: 8px;">Descripción</th>
                                        <th style="padding: 8px; text-align:center;">Cant.</th>
                                        <th style="padding: 8px; text-align:right;">Subtotal</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {previous_html}
                                </tbody>
                            </table>

                            <h3 style="color: #047857; margin-top: 0; border-bottom: 2px solid #ecfdf5; padding-bottom: 8px;">Nuevos Ítems Solicitados</h3>
                            <table style="width: 100%; font-size: 13px; margin-bottom: 24px; border-collapse: collapse;">
                                <thead>
                                    <tr style="background-color: #ecfdf5; color: #047857; text-align: left;">
                                        <th style="padding: 8px;">Descripción</th>
                                        <th style="padding: 8px; text-align:center;">Cant.</th>
                                        <th style="padding: 8px; text-align:right;">Subtotal</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {added_html}
                                </tbody>
                            </table>
                            
                            <h3 style="color: #334155; margin-top: 0; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px;">Notas Adicionales</h3>
                            <div style="background-color: #f8fafc; padding: 16px; border-radius: 8px; font-size: 14px; color: #475569; white-space: pre-wrap; font-family: monospace;">{notas or 'El cliente no dejó notas adicionales.'}</div>
                            
                            <div style="margin-top: 30px; text-align: center;">
                                <a href="/web#id={orden.id}&amp;view_type=form&amp;model=taller.orden.trabajo" style="display: inline-block; background-color: #0ea5e9; color: white; text-decoration: none; padding: 12px 24px; border-radius: 6px; font-weight: 600; font-size: 14px; box-shadow: 0 2px 4px rgba(14,165,233,0.3);">Ver Orden en el Sistema</a>
                            </div>
                        </div>
                    </div>
                    """
                        
                    request.env['mail.mail'].sudo().create({
                        'subject': subject,
                        'body_html': body_html,
                        'email_to': ','.join(unique_emails),
                        'auto_delete': True,
                    }).send()

            return {'success': True}
        except Exception as e:
            import traceback
            _logger.error("Error en propuesta crear: %s", traceback.format_exc())
            return {'success': False, 'error': f"Error interno: {str(e)}"}

    @http.route(['/my/vehicles/<int:id>/history'], type='http', auth="public", website=True)
    def taller_vehicle_history(self, id, **kw):
        user_id = request.session.get('taller_user_id')
        if not user_id:
            return request.redirect('/taller/login')
            
        user = request.env['usuarios_taller.user_profile'].sudo().browse(user_id)
        if not user.exists():
            return request.redirect('/taller/login')
            
        vehicle = request.env['taller.vehiculo'].sudo().browse(id)
        if not vehicle.exists() or vehicle.propietario_id.id != user.id:
            return request.redirect('/taller/mi_cuenta')
            
        # Obtener todas las órdenes de trabajo (activas y finalizadas)
        ordenes = request.env['taller.orden.trabajo'].sudo().search([
            ('vehiculo_id', '=', vehicle.id)
        ], order='fecha_ingreso desc')
        
        # Obtener las citas
        citas = request.env['taller.cita'].sudo().search([
            ('vehiculo_id', '=', vehicle.id)
        ], order='fecha_cita desc')
        
        # Obtener las facturas relacionadas a las órdenes
        facturas_ids = ordenes.mapped('factura_id').ids
        facturas = request.env['account.move'].sudo().search([
            ('id', 'in', facturas_ids),
            ('move_type', '=', 'out_invoice')
        ], order='invoice_date desc')
        
        return request.render('taller_mecanico_portal.vehicle_history_page', {
            'user': user,
            'vehicle': vehicle,
            'ordenes': ordenes,
            'citas': citas,
            'facturas': facturas,
        })

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
def _generate_beautiful_html(factura):
    import base64
    from io import BytesIO
    
    company = factura.company_id
    partner = factura.partner_id
    
    logo_html = ''
    if company.logo:
        logo_b64 = company.logo.decode('utf-8') if isinstance(company.logo, bytes) else company.logo
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="max-height:70px;"/>'
    else:
        logo_html = f'<h2 style="color:#0f172a;font-weight:bold;margin:0;">{company.name}</h2>'
    
    barcode_html = ''
    if factura.sri_clave_acceso:
        try:
            from barcode import Code128
            from barcode.writer import ImageWriter
            buffer = BytesIO()
            barcode_obj = Code128(factura.sri_clave_acceso, writer=ImageWriter())
            barcode_obj.write(buffer, options={'write_text': False, 'module_height': 12, 'module_width': 0.25, 'quiet_zone': 2})
            barcode_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            barcode_html = f'<img src="data:image/png;base64,{barcode_b64}" style="width:100%;max-width:550px;height:55px;margin-top:8px;" alt="Código de Barras"/>'
        except Exception:
            barcode_html = '<p style="font-size:10px;color:#999;">[Código de barras no disponible]</p>'
    
    lines_html = ''
    for line in factura.invoice_line_ids:
        if line.display_type not in ('line_section', 'line_note'):
            taxes = ', '.join([t.name for t in line.tax_ids]) if line.tax_ids else '0%'
            lines_html += f'''
            <tr style="border-bottom:1px solid #e2e8f0;">
                <td style="padding:8px;">{line.name or ''}</td>
                <td style="padding:8px;text-align:right;">{line.quantity}</td>
                <td style="padding:8px;text-align:right;">$ {line.price_unit:.2f}</td>
                <td style="padding:8px;text-align:center;">{taxes}</td>
                <td style="padding:8px;text-align:right;">{line.discount} %</td>
                <td style="padding:8px;text-align:right;">$ {line.price_subtotal:.2f}</td>
            </tr>'''
    
    sri_html = ''
    if factura.sri_clave_acceso:
        auth_date = ''
        if factura.sri_fecha_autorizacion:
            auth_date = f'<p style="font-size:11px;color:#64748b;margin:4px 0 0 0;">Fecha de Autorización: {factura.sri_fecha_autorizacion}</p>'
        sri_estado = (factura.sri_estado_autorizacion or 'LOCAL').upper()
        sri_html = f'''
        <div style="border:1px solid #cbd5e1;border-radius:6px;padding:14px;margin-bottom:18px;text-align:center;background:#fefefe;">
            <p style="font-weight:bold;font-size:13px;margin:0 0 4px 0;">CLAVE DE ACCESO:</p>
            <p style="font-size:11px;letter-spacing:0.8px;margin:0 0 4px 0;word-break:break-all;">{factura.sri_clave_acceso}</p>
            {barcode_html}
            <p style="font-size:11px;margin:6px 0 0 0;">Estado: <strong>{sri_estado}</strong></p>
            {auth_date}
        </div>'''

    html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
    @page {{ margin: 20mm 15mm; }}
    body {{ font-family: Helvetica, Arial, sans-serif; font-size: 12px; color: #1e293b; margin: 0; padding: 0; }}
    .meta-table {{ width: 100%; border-collapse: collapse; margin-bottom: 16px; }}
    .meta-table td {{ padding: 7px 10px; background: #f8fafc; border: 1px solid #e2e8f0; font-size: 11px; }}
    .lines-table {{ width: 100%; border-collapse: collapse; margin-bottom: 16px; }}
    .lines-table thead tr {{ background: #0f172a; color: #fff; }}
    .lines-table th {{ padding: 8px; font-size: 11px; text-align: left; }}
    .lines-table th.r {{ text-align: right; }}
    .lines-table td {{ padding: 7px 8px; font-size: 11px; }}
    .totals {{ float: right; width: 240px; }}
    .totals table {{ width: 100%; }}
    .totals td {{ padding: 4px 6px; font-size: 12px; }}
    .totals .total-row {{ border-top: 2px solid #0f172a; font-size: 14px; font-weight: bold; }}
    .footer {{ clear: both; text-align: center; font-size: 10px; color: #94a3b8; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 8px; }}
</style>
</head>
<body>
<div id="wrapwrap" style="width: 100%; height: 100%;">
<table style="width:100%;margin-bottom:16px;border-bottom:3px solid #0f172a;padding-bottom:10px;">
    <tr>
        <td style="vertical-align:middle;">{logo_html}</td>
        <td style="text-align:right;vertical-align:middle;">
            <h2 style="color:#0f172a;font-size:22px;margin:0;font-weight:bold;">FACTURA</h2>
            <h4 style="color:#64748b;margin:2px 0 0 0;font-size:14px;font-weight:400;">{factura.name}</h4>
        </td>
    </tr>
</table>
<table style="width:100%;margin-bottom:16px;">
    <tr>
        <td style="width:48%;vertical-align:top;">
            <h5 style="color:#0f172a;font-weight:bold;border-bottom:1px solid #e2e8f0;padding-bottom:4px;margin:0 0 6px 0;font-size:12px;">EMISOR</h5>
            <strong>{company.name}</strong><br/>
            RUC: {company.vat or '-'}<br/>
            {(company.street or '') + '<br/>' if company.street else ''}
            {(company.city or '') + ', ' + (company.country_id.name or '') + '<br/>' if company.city else ''}
            {'Tel: ' + company.phone + '<br/>' if company.phone else ''}
            {'Email: ' + company.email if company.email else ''}
        </td>
        <td style="width:4%;"></td>
        <td style="width:48%;vertical-align:top;">
            <h5 style="color:#0f172a;font-weight:bold;border-bottom:1px solid #e2e8f0;padding-bottom:4px;margin:0 0 6px 0;font-size:12px;">CLIENTE</h5>
            <strong>{partner.name}</strong><br/>
            Identificación: {partner.vat or '-'}<br/>
            {(partner.street or '') + '<br/>' if partner.street else ''}
            {(partner.city or '') + ', ' + (partner.country_id.name or '') + '<br/>' if partner.city else ''}
            {'Tel: ' + partner.phone + '<br/>' if partner.phone else ''}
            {'Email: ' + partner.email if partner.email else ''}
        </td>
    </tr>
</table>
<table class="meta-table">
    <tr>
        <td><strong>Fecha de Emisión:</strong> {factura.invoice_date}</td>
        <td><strong>Fecha de Vencimiento:</strong> {factura.invoice_date_due}</td>
        <td><strong>Origen:</strong> {factura.invoice_origin or '-'}</td>
    </tr>
</table>
{sri_html}
<table class="lines-table">
    <thead>
        <tr>
            <th>Descripción</th>
            <th class="r">Cantidad</th>
            <th class="r">Precio Unit.</th>
            <th style="text-align:center;">IVA</th>
            <th class="r">Descuento</th>
            <th class="r">Subtotal</th>
        </tr>
    </thead>
    <tbody>
        {lines_html}
    </tbody>
</table>
<div class="totals">
    <table>
        <tr>
            <td><strong>Subtotal</strong></td>
            <td style="text-align:right;">$ {factura.amount_untaxed:.2f}</td>
        </tr>
        <tr>
            <td>IVA 15%</td>
            <td style="text-align:right;">$ {factura.amount_tax:.2f}</td>
        </tr>
        <tr class="total-row">
            <td><strong>TOTAL</strong></td>
            <td style="text-align:right;"><strong>$ {factura.amount_total:.2f}</strong></td>
        </tr>
    </table>
</div>
<div class="footer">
    Documento generado por el Portal de Clientes — {company.name}
</div>
</div>
</body>
</html>'''
    return html

def _generate_beautiful_pdf(factura):
    import subprocess
    import tempfile
    import os
    from odoo.http import request
    
    html = _generate_beautiful_html(factura)

    try:
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as f_html:
            f_html.write(html)
            html_path = f_html.name
        
        pdf_path = html_path.replace('.html', '.pdf')
        
        wkhtmltopdf_bin = '/usr/local/bin/wkhtmltopdf'
        if not os.path.exists(wkhtmltopdf_bin):
            wkhtmltopdf_bin = 'wkhtmltopdf'
        
        subprocess.run(
            [wkhtmltopdf_bin, '--quiet', '--page-size', 'A4', '--margin-top', '15mm',
             '--margin-bottom', '15mm', '--margin-left', '15mm', '--margin-right', '15mm',
             '--encoding', 'utf-8', '--enable-local-file-access', html_path, pdf_path],
            capture_output=True, timeout=30
        )
        
        with open(pdf_path, 'rb') as f_pdf:
            pdf_content = f_pdf.read()
        
        os.unlink(html_path)
        os.unlink(pdf_path)
        
        filename = f"Factura_{factura.name or factura.id}.pdf".replace('/', '_')
        headers = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf_content)),
            ('Content-Disposition', f'attachment; filename="{filename}"'),
        ]
        return request.make_response(pdf_content, headers=headers)
    except Exception as e:
        import logging
        _logger = logging.getLogger(__name__)
        _logger.error(f"Error generando PDF hermoso de factura {factura.id}: {str(e)}")
        return False

def _generate_beautiful_sale_order_html(order):
    import base64
    from io import BytesIO
    
    company = order.company_id
    partner = order.partner_id
    
    logo_html = ''
    if company.logo:
        logo_b64 = company.logo.decode('utf-8') if isinstance(company.logo, bytes) else company.logo
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="max-height:70px;"/>'
    else:
        logo_html = f'<h2 style="color:#0f172a;font-weight:bold;margin:0;">{company.name}</h2>'
    
    lines_html = ''
    for line in order.order_line:
        if line.display_type not in ('line_section', 'line_note'):
            taxes = ', '.join([t.name for t in line.tax_id]) if line.tax_id else '0%'
            lines_html += f'''
            <tr style="border-bottom:1px solid #e2e8f0;">
                <td style="padding:8px;">{line.name or ''}</td>
                <td style="padding:8px;text-align:right;">{line.product_uom_qty}</td>
                <td style="padding:8px;text-align:right;">$ {line.price_unit:.2f}</td>
                <td style="padding:8px;text-align:center;">{taxes}</td>
                <td style="padding:8px;text-align:right;">{line.discount} %</td>
                <td style="padding:8px;text-align:right;">$ {line.price_subtotal:.2f}</td>
            </tr>'''
            
    date_order_str = order.date_order.strftime('%Y-%m-%d') if order.date_order else '-'

    html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
    @page {{ margin: 20mm 15mm; }}
    body {{ font-family: Helvetica, Arial, sans-serif; font-size: 12px; color: #1e293b; margin: 0; padding: 0; }}
    .meta-table {{ width: 100%; border-collapse: collapse; margin-bottom: 16px; }}
    .meta-table td {{ padding: 7px 10px; background: #f8fafc; border: 1px solid #e2e8f0; font-size: 11px; }}
    .lines-table {{ width: 100%; border-collapse: collapse; margin-bottom: 16px; }}
    .lines-table thead tr {{ background: #0f172a; color: #fff; }}
    .lines-table th {{ padding: 8px; font-size: 11px; text-align: left; }}
    .lines-table th.r {{ text-align: right; }}
    .lines-table td {{ padding: 7px 8px; font-size: 11px; }}
    .totals {{ float: right; width: 240px; }}
    .totals table {{ width: 100%; }}
    .totals td {{ padding: 4px 6px; font-size: 12px; }}
    .totals .total-row {{ border-top: 2px solid #0f172a; font-size: 14px; font-weight: bold; }}
    .footer {{ clear: both; text-align: center; font-size: 10px; color: #94a3b8; margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 8px; }}
</style>
</head>
<body>
<div id="wrapwrap" style="width: 100%; height: 100%;">
<table style="width:100%;margin-bottom:16px;border-bottom:3px solid #0f172a;padding-bottom:10px;">
    <tr>
        <td style="vertical-align:middle;">{logo_html}</td>
        <td style="text-align:right;vertical-align:middle;">
            <h2 style="color:#0f172a;font-size:22px;margin:0;font-weight:bold;">ORDEN</h2>
            <h4 style="color:#64748b;margin:2px 0 0 0;font-size:14px;font-weight:400;">{order.name}</h4>
        </td>
    </tr>
</table>
<table style="width:100%;margin-bottom:16px;">
    <tr>
        <td style="width:48%;vertical-align:top;">
            <h5 style="color:#0f172a;font-weight:bold;border-bottom:1px solid #e2e8f0;padding-bottom:4px;margin:0 0 6px 0;font-size:12px;">EMISOR</h5>
            <strong>{company.name}</strong><br/>
            RUC: {company.vat or '-'}<br/>
            {(company.street or '') + '<br/>' if company.street else ''}
            {(company.city or '') + ', ' + (company.country_id.name or '') + '<br/>' if company.city else ''}
            {'Tel: ' + company.phone + '<br/>' if company.phone else ''}
            {'Email: ' + company.email if company.email else ''}
        </td>
        <td style="width:4%;"></td>
        <td style="width:48%;vertical-align:top;">
            <h5 style="color:#0f172a;font-weight:bold;border-bottom:1px solid #e2e8f0;padding-bottom:4px;margin:0 0 6px 0;font-size:12px;">CLIENTE</h5>
            <strong>{partner.name}</strong><br/>
            Identificación: {partner.vat or '-'}<br/>
            {(partner.street or '') + '<br/>' if partner.street else ''}
            {(partner.city or '') + ', ' + (partner.country_id.name or '') + '<br/>' if partner.city else ''}
            {'Tel: ' + partner.phone + '<br/>' if partner.phone else ''}
            {'Email: ' + partner.email if partner.email else ''}
        </td>
    </tr>
</table>
<table class="meta-table">
    <tr>
        <td><strong>Fecha de Orden:</strong> {date_order_str}</td>
        <td><strong>Referencia:</strong> {order.client_order_ref or '-'}</td>
    </tr>
</table>
<table class="lines-table">
    <thead>
        <tr>
            <th>Descripción</th>
            <th class="r">Cantidad</th>
            <th class="r">Precio Unit.</th>
            <th style="text-align:center;">IVA</th>
            <th class="r">Descuento</th>
            <th class="r">Subtotal</th>
        </tr>
    </thead>
    <tbody>
        {lines_html}
    </tbody>
</table>
<div class="totals">
    <table>
        <tr>
            <td><strong>Subtotal</strong></td>
            <td style="text-align:right;">$ {order.amount_untaxed:.2f}</td>
        </tr>
        <tr>
            <td>IVA 15%</td>
            <td style="text-align:right;">$ {order.amount_tax:.2f}</td>
        </tr>
        <tr class="total-row">
            <td><strong>TOTAL</strong></td>
            <td style="text-align:right;"><strong>$ {order.amount_total:.2f}</strong></td>
        </tr>
    </table>
</div>
<div class="footer">
    Documento generado por el Portal de Clientes — {company.name}
</div>
</div>
</body>
</html>'''
    return html

def _generate_beautiful_sale_order_pdf(order):
    import subprocess
    import tempfile
    import os
    from odoo.http import request
    
    html = _generate_beautiful_sale_order_html(order)

    try:
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as f_html:
            f_html.write(html)
            html_path = f_html.name
        
        pdf_path = html_path.replace('.html', '.pdf')
        
        wkhtmltopdf_bin = '/usr/local/bin/wkhtmltopdf'
        if not os.path.exists(wkhtmltopdf_bin):
            wkhtmltopdf_bin = 'wkhtmltopdf'
        
        subprocess.run(
            [wkhtmltopdf_bin, '--quiet', '--page-size', 'A4', '--margin-top', '15mm',
             '--margin-bottom', '15mm', '--margin-left', '15mm', '--margin-right', '15mm',
             '--encoding', 'utf-8', '--enable-local-file-access', html_path, pdf_path],
            capture_output=True, timeout=30
        )
        
        with open(pdf_path, 'rb') as f_pdf:
            pdf_content = f_pdf.read()
        
        os.unlink(html_path)
        os.unlink(pdf_path)
        
        filename = f"Orden_{order.name or order.id}.pdf".replace('/', '_')
        headers = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf_content)),
            ('Content-Disposition', f'attachment; filename="{filename}"'),
        ]
        return request.make_response(pdf_content, headers=headers)
    except Exception as e:
        import logging
        _logger = logging.getLogger(__name__)
        _logger.error(f"Error generando PDF hermoso de orden {order.id}: {str(e)}")
        return False

try:
    from odoo.addons.website_sale.controllers.main import WebsiteSale
except ImportError:
    WebsiteSale = object

class TallerCustomWebsiteSale(WebsiteSale):
    @http.route(['/shop/print'], type='http', auth="public", website=True, sitemap=False)
    def print_saleorder(self, **kwargs):
        sale_order_id = request.session.get('sale_last_order_id')
        if sale_order_id:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            if order.exists():
                response = _generate_beautiful_sale_order_pdf(order)
                if response:
                    return response
        if WebsiteSale != object:
            return super(TallerCustomWebsiteSale, self).print_saleorder(**kwargs)
        return request.redirect('/shop')

try:
    from odoo.addons.account.controllers.portal import PortalAccount
except ImportError:
    PortalAccount = object

class TallerCustomPortalAccount(PortalAccount):
    @http.route(['/my/invoices/<int:invoice_id>'], type='http', auth="public", website=True)
    def portal_my_invoice_detail(self, invoice_id, access_token=None, report_type=None, download=False, **kw):
        if report_type == 'pdf':
            factura = request.env['account.move'].sudo().browse(invoice_id)
            if factura.exists():
                response = _generate_beautiful_pdf(factura)
                if response:
                    return response
        elif report_type == 'html':
            factura = request.env['account.move'].sudo().browse(invoice_id)
            if factura.exists():
                html = _generate_beautiful_html(factura)
                return request.make_response(html, headers=[('Content-Type', 'text/html; charset=utf-8')])
                
        if PortalAccount != object:
            kwargs = dict(kw, access_token=access_token, report_type=report_type, download=download)
            return super(TallerCustomPortalAccount, self).portal_my_invoice_detail(invoice_id=invoice_id, **kwargs)
        return request.redirect('/my/invoices')

class TallerPortalAPI(http.Controller):
    @http.route(['/taller/factura/<int:factura_id>/pdf'], type='http', auth="public")
    def taller_factura_pdf(self, factura_id, **kw):
        user_id = request.session.get('taller_user_id')
        if not user_id:
            return request.redirect('/taller/login')
        user = request.env['usuarios_taller.user_profile'].sudo().browse(user_id)
        if not user.exists() or not user.partner_id:
            return request.redirect('/taller/login')
            
        factura = request.env['account.move'].sudo().search([
            ('id', '=', factura_id),
            ('partner_id', '=', user.partner_id.id)
        ], limit=1)
        if not factura:
            return request.redirect('/taller/mi_cuenta')
            
        response = _generate_beautiful_pdf(factura)
        if response:
            return response
        return request.redirect('/taller/mi_cuenta')
    @http.route(['/taller/factura/<int:factura_id>/xml'], type='http', auth="public")
    def taller_factura_xml(self, factura_id, **kw):
        user_id = request.session.get('taller_user_id')
        if not user_id:
            return request.redirect('/taller/login')
        user = request.env['usuarios_taller.user_profile'].sudo().browse(user_id)
        if not user.exists() or not user.partner_id:
            return request.redirect('/taller/login')
            
        factura = request.env['account.move'].sudo().search([
            ('id', '=', factura_id),
            ('partner_id', '=', user.partner_id.id)
        ], limit=1)
        if not factura or not factura.sri_xml_file:
            return request.redirect('/taller/mi_cuenta')
            
        import base64
        xml_data = base64.b64decode(factura.sri_xml_file)
        headers = [('Content-Type', 'application/xml'), 
                   ('Content-Length', len(xml_data)), 
                   ('Content-Disposition', f'attachment; filename="Factura_{factura.name or factura.id}.xml"'.replace('/', '_'))]
        return request.make_response(xml_data, headers=headers)
