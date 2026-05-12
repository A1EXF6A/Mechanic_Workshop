/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.TallerShop = publicWidget.Widget.extend({
    selector: '#wrap',
    events: {
        'click .js_add_to_cart': '_onAddToCart',
        'click .js_remove_item': '_onRemoveItem',
        'change .js_update_qty': '_onUpdateQty',
    },

    /**
     * Agrega un producto al carrito
     */
    _onAddToCart: function (ev) {
        var $btn = $(ev.currentTarget);
        var productId = $btn.data('product-id');
        
        if (!productId) {
            console.error("TallerShop: No se encontró product-id en el botón");
            return;
        }

        $btn.prop('disabled', true);

        this._performRPC('/taller/carrito/agregar', {
            product_id: productId,
            qty: 1,
        }).then((data) => {
            if (data && data.success) {
                const originalHtml = $btn.html();
                $btn.removeClass('btn-primary').addClass('btn-success').html('<i class="fa fa-check me-2"/> Agregado');
                
                setTimeout(() => {
                    $btn.removeClass('btn-success').addClass('btn-primary').html(originalHtml);
                    $btn.prop('disabled', false);
                }, 2000);
            } else {
                alert(data.error || "Error al agregar al carrito");
                $btn.prop('disabled', false);
            }
        }).catch((err) => {
            console.error("TallerShop: Error RPC", err);
            $btn.prop('disabled', false);
        });
    },

    /**
     * Elimina un producto del carrito
     */
    _onRemoveItem: function (ev) {
        var productId = $(ev.currentTarget).data('product-id');
        this._performRPC('/taller/carrito/eliminar', {
            product_id: productId
        }).then((data) => {
            if (data && data.success) {
                window.location.reload();
            }
        });
    },

    /**
     * Actualiza la cantidad de un producto
     */
    _onUpdateQty: function (ev) {
        var $input = $(ev.currentTarget);
        var productId = $input.data('product-id');
        var qty = parseInt($input.val());

        if (isNaN(qty) || qty < 0) qty = 0;

        this._performRPC('/taller/carrito/actualizar', {
            product_id: productId,
            qty: qty
        }).then((data) => {
            if (data && data.success) {
                window.location.reload();
            } else {
                alert(data.error || "No se pudo actualizar la cantidad");
                window.location.reload(); // Recargar para revertir el input
            }
        });
    },

    /**
     * Helper para realizar peticiones JSON-RPC compatibles con Odoo
     */
    _performRPC: function (url, params) {
        params = params || {};
        
        if (typeof odoo !== 'undefined' && odoo.csrf_token) {
            params['csrf_token'] = odoo.csrf_token;
        }

        return new Promise((resolve, reject) => {
            $.ajax({
                url: url,
                type: 'POST',
                dataType: 'json',
                contentType: 'application/json',
                data: JSON.stringify({
                    jsonrpc: "2.0",
                    method: "call",
                    params: params
                }),
                success: function (data) {
                    if (data.error) {
                        reject(data.error);
                    } else {
                        resolve(data.result);
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    reject(errorThrown);
                }
            });
        });
    },
});

export default publicWidget.registry.TallerShop;
