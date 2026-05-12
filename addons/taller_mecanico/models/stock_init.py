from odoo import models, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def _init_taller_stock(self):
        """Método para inicializar stock de productos del taller si están en cero."""
        warehouse = self.env['stock.warehouse'].search([], limit=1)
        if not warehouse:
            return
            
        location = warehouse.lot_stock_id
        # Buscamos productos que pertenecen al taller (puedes filtrar por categoría o tag si prefieres)
        products = self.search([('qty_available', '=', 0)])
        
        for product in products:
            # Solo aplicamos a productos que parecen ser del taller (basado en el contexto de este módulo)
            self.env['stock.quant'].with_context(inventory_mode=True).create({
                'product_id': product.id,
                'location_id': location.id,
                'inventory_quantity': 50,
            }).action_apply_inventory()
