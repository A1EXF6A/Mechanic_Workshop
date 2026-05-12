# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class TallerShopController(http.Controller):

    @http.route(['/taller/productos'], type='http', auth="public", website=True)
    def productos(self, **kw):
        # Buscamos productos que se puedan vender y tengan stock (storable)
        products = request.env['product.product'].sudo().search([
            ('sale_ok', '=', True),
            ('type', 'in', ['product', 'consu']),
        ])
        return request.render('taller_mecanico.productos_page', {
            'products': products,
        })

    @http.route(['/taller/carrito'], type='http', auth="public", website=True)
    def carrito(self, **kw):
        cart = request.session.get('taller_cart', {})
        cart_items = []
        total = 0.0

        for product_id, qty in cart.items():
            product = request.env['product.product'].sudo().browse(int(product_id))
            if product.exists():
                subtotal = product.lst_price * qty
                total += subtotal
                cart_items.append({
                    'product': product,
                    'qty': qty,
                    'subtotal': subtotal,
                })

        return request.render('taller_mecanico.carrito_page', {
            'cart_items': cart_items,
            'total': total,
        })

    @http.route(['/taller/carrito/agregar'], type='json', auth="public", website=True)
    def agregar_al_carrito(self, product_id, qty=1, **kw):
        product = request.env['product.product'].sudo().browse(int(product_id))
        if not product.exists():
             return {'success': False, 'error': 'Producto no encontrado'}
        
        cart = dict(request.session.get('taller_cart', {}))
        pid = str(product_id)
        requested_qty = cart.get(pid, 0) + int(qty)
        
        # Validación de Stock
        if product.type == 'product' and product.qty_available < requested_qty:
             return {
                 'success': False, 
                 'error': f'Solo quedan {int(product.qty_available)} unidades disponibles.'
             }

        cart[pid] = requested_qty
        request.session['taller_cart'] = cart
        request.session.modified = True
        return {'count': sum(cart.values()), 'success': True}

    @http.route(['/taller/carrito/eliminar'], type='json', auth="public", website=True)
    def eliminar_del_carrito(self, product_id, **kw):
        cart = dict(request.session.get('taller_cart', {}))
        pid = str(product_id)
        if pid in cart:
            del cart[pid]
            request.session['taller_cart'] = cart
            request.session.modified = True
        return {'success': True}

    @http.route(['/taller/carrito/actualizar'], type='json', auth="public", website=True)
    def actualizar_cantidad(self, product_id, qty, **kw):
        product = request.env['product.product'].sudo().browse(int(product_id))
        if not product.exists():
             return {'success': False, 'error': 'Producto no encontrado'}

        cart = dict(request.session.get('taller_cart', {}))
        pid = str(product_id)
        new_qty = int(qty)

        # Validación de Stock al actualizar
        if product.type == 'product' and product.qty_available < new_qty:
             return {
                 'success': False, 
                 'error': f'Stock insuficiente. Máximo disponible: {int(product.qty_available)}'
             }

        if new_qty > 0:
            cart[pid] = new_qty
        elif pid in cart:
            del cart[pid]
            
        request.session['taller_cart'] = cart
        request.session.modified = True
        return {'success': True}

    @http.route(['/taller/confirmar-compra'], type='http', auth="user", website=True, methods=['POST'], csrf=True)
    def confirmar_compra(self, **kw):
        partner = request.env.user.partner_id
        cart = request.session.get('taller_cart', {})

        if not cart:
            return request.redirect('/taller/productos')

        # Obtenemos el almacén de forma segura
        warehouse = getattr(request.website, 'warehouse_id', False)
        if not warehouse:
            warehouse = request.env['stock.warehouse'].sudo().search([
                ('company_id', '=', request.website.company_id.id)
            ], limit=1)

        sale_order = request.env['sale.order'].sudo().create({
            'partner_id': partner.id,
            'company_id': request.website.company_id.id,
            'warehouse_id': warehouse.id if warehouse else False,
        })

        for product_id, qty in cart.items():
            product = request.env['product.product'].sudo().browse(int(product_id))
            if product.exists():
                request.env['sale.order.line'].sudo().create({
                    'order_id': sale_order.id,
                    'product_id': product.id,
                    'product_uom_qty': qty,
                    'price_unit': product.lst_price,
                })

        # Confirmar la orden (Esto descuenta INVENTARIO)
        sale_order.action_confirm()

        # Generar Factura
        invoice = sale_order._create_invoices()
        invoice.action_post()

        # Limpiar carrito
        request.session['taller_cart'] = {}

        return request.render('taller_mecanico.confirmacion_page', {
            'order': sale_order,
        })
