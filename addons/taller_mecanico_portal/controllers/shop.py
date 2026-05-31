# -*- coding: utf-8 -*-
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class TallerShopController(http.Controller):

    @http.route(['/taller/productos', '/taller/productos/categoria/<model("product.category"):category>'], type='http', auth="public", website=True)
    def productos(self, category=None, search='', sortby=None, filter_new=None, filter_promo=None, **kw):
        domain = [
            ('sale_ok', '=', True),
            ('type', 'in', ['product', 'consu']),
        ]
        
        # Filtro de Búsqueda
        if search:
            domain += [('name', 'ilike', search)]
            
        # Filtro de Categoría de Inventario
        if category:
            domain += [('categ_id', 'child_of', int(category.id))]
            
        # Filtro de Productos Nuevos (creados en los últimos 30 días)
        if filter_new == '1':
            from datetime import datetime, timedelta
            limit_date = datetime.now() - timedelta(days=30)
            domain += [('create_date', '>=', limit_date.strftime('%Y-%m-%d %H:%M:%S'))]
            
        # Filtro de Promociones (que tienen compare_list_price > 0.0)
        if filter_promo == '1':
            domain += [('compare_list_price', '>', 0.0)]
            
        # Lógica de Ordenamiento
        order = 'sequence, id desc'
        if sortby == 'price_asc':
            order = 'list_price asc'
        elif sortby == 'price_desc':
            order = 'list_price desc'
        elif sortby == 'newest':
            order = 'create_date desc'
            
        # Obtenemos productos filtrados y ordenados
        products = request.env['product.product'].sudo().search(domain, order=order)
        
        # Ordenamos de forma estable: primero productos con stock disponible, luego los agotados
        products = products.sorted(key=lambda p: p.qty_available <= 0)
        
        # Obtenemos todas las categorías internas de Inventario para el sidebar
        # Excluimos las categorías internas del sistema por sus IDs de creación base (1=All, 2=Saleable, 3=Expenses, etc.)
        all_categories = request.env['product.category'].sudo().search([('id', 'not in', [1, 2, 3, 4, 5])])
        
        # Calculamos conteos de productos reales activos por categoría
        categories_data = []
        for cat in all_categories:
            count = request.env['product.product'].sudo().search_count([
                ('sale_ok', '=', True),
                ('type', 'in', ['product', 'consu']),
                ('categ_id', 'child_of', cat.id)
            ])
            if count > 0:
                categories_data.append({
                    'category': cat,
                    'count': count
                })
        
        return request.render('taller_mecanico.productos_page', {
            'products': products,
            'categories': categories_data,
            'current_category': category,
            'search': search,
            'sortby': sortby,
            'filter_new': filter_new,
            'filter_promo': filter_promo,
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

    @http.route(['/taller/confirmar-compra'], type='http', auth="public", website=True, methods=['POST'], csrf=True)
    def confirmar_compra(self, **kw):
        taller_user_id = request.session.get('taller_user_id')
        if not taller_user_id:
            return request.redirect('/taller/login')

        cart = request.session.get('taller_cart', {})

        if not cart:
            return request.redirect('/taller/productos')

        # Usar el generador nativo de Odoo para crear la orden asegurando que las direcciones 
        # de facturación y envío (partner_invoice_id, partner_shipping_id) estén correctas.
        sale_order = request.website.sale_get_order(force_create=True)

        # Limpiamos las líneas anteriores del carrito nativo por si acaso
        sale_order.order_line.sudo().unlink()

        # Insertamos los productos de nuestro carrito personalizado
        for product_id, qty in cart.items():
            product = request.env['product.product'].sudo().browse(int(product_id))
            if product.exists():
                request.env['sale.order.line'].sudo().create({
                    'order_id': sale_order.id,
                    'product_id': product.id,
                    'product_uom_qty': qty,
                    'price_unit': product.lst_price,
                })

        # Limpiar carrito personalizado
        request.session['taller_cart'] = {}

        # Redirigir al flujo de checkout oficial (que maneja direcciones y luego pagos)
        return request.redirect('/shop/checkout?express=1')
