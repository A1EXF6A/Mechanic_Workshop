# -*- coding: utf-8 -*-
# pyrefly: ignore [missing-import]
from odoo import http
# pyrefly: ignore [missing-import]
from odoo.http import request

class TallerShopController(http.Controller):

    @http.route(['/taller/productos'], type='http', auth="public", website=True)
    def productos(self, **kw):
        # Buscamos productos que se puedan vender y tengan stock (storable)
        # Odoo 16+ usa product.template para el catálogo general
        products = request.env['product.template'].sudo().search([
            ('sale_ok', '=', True),
            ('type', 'in', ['product', 'consu']),
        ])
        return request.render('taller_mecanico.productos_page', {
            'products': products,
        })

    @http.route(['/taller/carrito'], type='http', auth="public", website=True)
    def carrito(self, **kw):
        # Recuperamos el carrito de la sesión
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
        cart = dict(request.session.get('taller_cart', {}))
        pid = str(product_id)
        cart[pid] = cart.get(pid, 0) + int(qty)
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
        cart = dict(request.session.get('taller_cart', {}))
        pid = str(product_id)
        if int(qty) > 0:
            cart[pid] = int(qty)
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

        # 1. Crear Orden de Venta (Modulo Ventas)
        # Obtenemos el almacén de forma segura (warehouse_id no siempre está en website)
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

        # 2. Agregar líneas (Conexión Productos/Inventario)
        for product_id, qty in cart.items():
            product = request.env['product.product'].sudo().browse(int(product_id))
            if product.exists():
                request.env['sale.order.line'].sudo().create({
                    'order_id': sale_order.id,
                    'product_id': product.id,
                    'product_uom_qty': qty,
                    'price_unit': product.lst_price,
                })

        # 3. Confirmar la orden (Esto descuenta INVENTARIO automáticamente)
        sale_order.action_confirm()

        # 4. Generar Factura (Modulo Facturación)
        # Odoo 16+ usa _create_invoices
        invoice = sale_order._create_invoices()
        invoice.action_post() # Publicar factura

        # 5. Limpiar carrito y redirigir
        request.session['taller_cart'] = {}

        return request.render('taller_mecanico.confirmacion_page', {
            'order': sale_order,
        })
