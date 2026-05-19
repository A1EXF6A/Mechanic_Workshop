from odoo import models, fields, api
from odoo.exceptions import UserError
import requests


class TallerMarcaBuscarWizard(models.TransientModel):
    """Wizard para buscar y agregar una marca individual desde la API NHTSA."""
    _name = 'taller.marca.buscar.wizard'
    _description = 'Asistente para Agregar Marca'

    termino_busqueda = fields.Char(
        string='Nombre de la Marca',
        required=True,
        help='Escribe el nombre de la marca a buscar (ej: Hyundai, Renault, Chery...)'
    )
    resultado_ids = fields.One2many(
        'taller.marca.buscar.linea',
        'wizard_id',
        string='Resultados Encontrados'
    )
    mensaje = fields.Char(string='Estado', readonly=True)

    def action_buscar(self):
        """Busca en la API de NHTSA por nombre y muestra solo los resultados nuevos."""
        self.ensure_one()
        termino = (self.termino_busqueda or '').strip()
        if not termino:
            raise UserError('Escribe el nombre de una marca para buscar.')

        try:
            url = 'https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json'
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json().get('Results', [])
        except Exception as e:
            raise UserError(f'Error al conectar con la API de NHTSA: {e}')

        # Filtrar resultados que coincidan con el término de búsqueda (máx 20)
        termino_lower = termino.lower()
        coincidencias = [
            item for item in data
            if termino_lower in str(item.get('Make_Name', '')).lower()
        ][:20]

        # Borrar líneas anteriores
        self.resultado_ids.unlink()

        if not coincidencias:
            self.mensaje = f'❌ No se encontraron marcas con el término "{termino}". Intenta con otro nombre.'
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'taller.marca.buscar.wizard',
                'res_id': self.id,
                'view_mode': 'form',
                'target': 'new',
            }

        # Separar las que ya existen de las nuevas
        ya_existen = []
        nuevas = []
        for item in coincidencias:
            nhtsa_id = item.get('Make_ID', 0)
            nombre = str(item.get('Make_Name', '')).title()
            existe = bool(
                self.env['taller.marca'].sudo().search(
                    [('nhtsa_id', '=', nhtsa_id)], limit=1
                )
            )
            if existe:
                ya_existen.append(nombre)
            else:
                nuevas.append({
                    'wizard_id': self.id,
                    'nhtsa_id': nhtsa_id,
                    'name': nombre,
                    'ya_existe': False,
                })

        # Construir mensaje según el caso
        if ya_existen and not nuevas:
            # Todas las coincidencias ya están en el sistema
            lista = ', '.join(ya_existen)
            self.mensaje = f'✅ La(s) marca(s) encontrada(s) ya está(n) registrada(s) en el sistema: {lista}'
        elif ya_existen and nuevas:
            # Algunas ya existen, otras son nuevas
            lista_existentes = ', '.join(ya_existen)
            self.env['taller.marca.buscar.linea'].create(nuevas)
            self.mensaje = (
                f'ℹ️ Ya registradas: {lista_existentes}. '
                f'Se muestran {len(nuevas)} marca(s) nueva(s) disponible(s) para agregar.'
            )
        else:
            # Todas son nuevas
            self.env['taller.marca.buscar.linea'].create(nuevas)
            self.mensaje = f'🔍 Se encontraron {len(nuevas)} marca(s) nueva(s). Selecciona las que deseas agregar.'

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'taller.marca.buscar.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def action_agregar_seleccionadas(self):
        """Agrega las marcas seleccionadas a la base de datos."""
        self.ensure_one()
        seleccionadas = self.resultado_ids.filtered(lambda l: l.seleccionar and not l.ya_existe)

        if not seleccionadas:
            raise UserError('Selecciona al menos una marca que no esté ya en el sistema.')

        marcas_creadas = []
        for linea in seleccionadas:
            nueva_marca = self.env['taller.marca'].sudo().create({
                'name': linea.name,
                'nhtsa_id': linea.nhtsa_id,
            })
            marcas_creadas.append(nueva_marca.name)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '¡Marcas Agregadas!',
                'message': f'Se agregaron: {", ".join(marcas_creadas)}',
                'sticky': False,
                'type': 'success',
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }


class TallerMarcaBuscarLinea(models.TransientModel):
    """Línea de resultado del wizard de búsqueda de marcas."""
    _name = 'taller.marca.buscar.linea'
    _description = 'Línea de Resultado de Búsqueda de Marca'

    wizard_id = fields.Many2one('taller.marca.buscar.wizard', ondelete='cascade')
    seleccionar = fields.Boolean(string='✔', default=False)
    nhtsa_id = fields.Integer(string='ID NHTSA', readonly=True)
    name = fields.Char(string='Marca', readonly=True)
    ya_existe = fields.Boolean(string='Ya en Sistema', readonly=True)
