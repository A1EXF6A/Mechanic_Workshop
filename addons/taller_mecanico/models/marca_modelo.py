from odoo import models, fields, api
from odoo.exceptions import UserError
import requests

class TallerMarca(models.Model):
    _name = 'taller.marca'
    _description = 'Marca de Vehículo'
    _rec_name = 'name'
    _order = 'name asc'

    name = fields.Char(string='Marca', required=True)
    nhtsa_id = fields.Integer(string='ID NHTSA')
    modelo_ids = fields.One2many('taller.modelo', 'marca_id', string='Modelos')
    modelos_count = fields.Integer(string='Modelos', compute='_compute_modelos_count', store=True)

    @api.depends('modelo_ids')
    def _compute_modelos_count(self):
        for rec in self:
            rec.modelos_count = self.env['taller.modelo'].search_count([('marca_id', '=', rec.id)])

    def action_open_wizard(self):
        """Abre el wizard de búsqueda de marca en lugar del formulario de creación estándar."""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Buscar y Agregar Marca',
            'res_model': 'taller.marca.buscar.wizard',
            'view_mode': 'form',
            'target': 'new',
        }

    def action_sync_all_models(self):
        """Sincroniza los modelos de TODAS las marcas desde la API NHTSA en batch."""
        marcas = self.search([('nhtsa_id', '>', 0)])
        total = len(marcas)
        sincronizadas = 0
        errores = 0

        for marca in marcas:
            try:
                url = f'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformakeid/{marca.nhtsa_id}?format=json'
                response = requests.get(url, timeout=15)
                response.raise_for_status()
                data = response.json().get('Results', [])

                existing_names = set(
                    n.lower() for n in
                    self.env['taller.modelo'].search([('marca_id', '=', marca.id)]).mapped('name')
                    if n
                )
                to_create = []
                for item in data:
                    model_name = str(item.get('Model_Name') or '').title()
                    if model_name and model_name.lower() not in existing_names:
                        to_create.append({'name': model_name, 'marca_id': marca.id})
                        existing_names.add(model_name.lower())

                if to_create:
                    self.env['taller.modelo'].create(to_create)
                sincronizadas += 1
            except Exception:
                errores += 1
                continue

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': '✅ Sincronización Masiva Completada',
                'message': (
                    f'Se procesaron {sincronizadas} de {total} marcas. '
                    + (f'{errores} con errores.' if errores else 'Sin errores.')
                ),
                'sticky': True,
                'type': 'success',
            }
        }

    def action_sync_makes(self):
        url = 'https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json'
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json().get('Results', [])
        except Exception as e:
            raise UserError(f'Error al conectar con la API de NHTSA: {e}')

        makes_to_create = []
        existing_nhtsa_ids = set(self.search([]).mapped('nhtsa_id'))
        
        # Lista de marcas principales para filtrar la basura de la API
        POPULAR_BRANDS = {
            'toyota', 'honda', 'ford', 'chevrolet', 'nissan', 'hyundai', 'kia', 
            'volkswagen', 'bmw', 'mercedes-benz', 'audi', 'jeep', 'subaru', 'lexus', 
            'mazda', 'tesla', 'peugeot', 'renault', 'fiat', 'volvo', 'suzuki', 
            'mitsubishi', 'land rover', 'porsche', 'jaguar', 'mini', 'alfa romeo', 
            'chrysler', 'dodge', 'ram', 'gmc', 'cadillac', 'buick', 'acura', 'infiniti',
            'lincoln', 'genesis', 'seat', 'skoda', 'citroen', 'opel', 'dacia', 'chery', 
            'great wall', 'jac', 'mg', 'byd', 'geely', 'ssangyong', 'tata', 'mahindra', 
            'aston martin', 'ferrari', 'lamborghini', 'maserati', 'bentley', 'rolls-royce',
            'smart', 'isuzu', 'pontiac', 'saturn', 'saab', 'daewoo', 'hummer', 'rover'
        }
        
        count = 0
        for item in data:
            make_id = item.get('Make_ID')
            raw_name = item.get('Make_Name') or ''
            make_name = str(raw_name).title()
            
            # Solo crear si es una marca popular y no existe
            if make_id and make_name.lower() in POPULAR_BRANDS and make_id not in existing_nhtsa_ids:
                makes_to_create.append({
                    'name': make_name,
                    'nhtsa_id': make_id
                })
                existing_nhtsa_ids.add(make_id)
                count += 1
                
                if len(makes_to_create) >= 100:
                    self.create(makes_to_create)
                    makes_to_create = []
                    
        if makes_to_create:
            self.create(makes_to_create)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Sincronización Completada',
                'message': f'Se importaron {count} marcas nuevas desde la NHTSA.',
                'sticky': False,
                'type': 'success',
            }
        }

    def action_sync_models(self):
        self.ensure_one()
        if not self.nhtsa_id:
            raise UserError('Esta marca no tiene un ID de NHTSA válido. Por favor asigne uno o vuelva a sincronizar.')
            
        url = f'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformakeid/{self.nhtsa_id}?format=json'
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json().get('Results', [])
        except Exception as e:
            raise UserError(f'Error al conectar con la API de NHTSA: {e}')

        existing_names = set(
            name.lower() for name in self.env['taller.modelo'].search([('marca_id', '=', self.id)]).mapped('name') if name
        )
        models_to_create = []
        count = 0
        
        for item in data:
            model_name = item.get('Model_Name', '').title()
            if model_name and model_name.lower() not in existing_names:
                models_to_create.append({
                    'name': model_name,
                    'marca_id': self.id,
                })
                existing_names.add(model_name.lower())
                count += 1
                
        if models_to_create:
            self.env['taller.modelo'].create(models_to_create)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'taller.marca',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'current',
        }


class TallerModelo(models.Model):
    _name = 'taller.modelo'
    _description = 'Modelo de Vehículo'
    _rec_name = 'name'
    _order = 'name asc'

    name = fields.Char(string='Modelo', required=True)
    marca_id = fields.Many2one('taller.marca', string='Marca', required=True, ondelete='cascade')
