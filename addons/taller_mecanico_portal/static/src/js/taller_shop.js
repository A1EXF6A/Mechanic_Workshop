/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.TallerShop = publicWidget.Widget.extend({
    selector: '#wrap',
    events: {
        'click .js_add_to_cart': '_onAddToCart',
        'click .js_remove_item': '_onRemoveItem',
        'change .js_update_qty': '_onUpdateQty',
        
        // Approve / Reject actions for extra lines
        'click .js_approve_extra_line': '_onApproveExtraLine',
        'click .js_reject_extra_line': '_onRejectExtraLine',
        'click .js_pending_extra_line': '_onPendingExtraLine',
        
        // Inline new UI
        'click .js_swap_btn': '_onSwapLine',
        'click .js_cancel_swap': '_onCancelSwap',
        'click .js_add_new_line': '_onAddNewLine',
        'click .js_remove_new_line': '_onRemoveNewLine',
        'click .js_submit_client_proposal': '_onSubmitClientProposal',
        
        // Catalog modal events
        'click .js_open_catalog_btn': '_onOpenCatalog',
        'input #catalogSearchInput': '_onCatalogSearch',
        'change #catalogSortSelect': '_onCatalogSort',
        'click .js_select_catalog_item': '_onSelectCatalogItem'
    },

    start: function () {
        var def = this._super.apply(this, arguments);
        var self = this;
        this.$('.modal').each(function() {
            if ($(this).find('.js_submit_client_proposal').length > 0) {
                self._updateProposalButtonState($(this));
            }
        });
        return def;
    },

    _updateProposalButtonState: function ($modal) {
        var $btn = $modal.find('.js_submit_client_proposal');
        var $swappedRows = $modal.find('.js_swapped_row');
        var $newRows = $modal.find('.js_new_propuesta_row');
        
        var hasPending = false;
        var hasRejected = false;
        
        $modal.find('.item-row:not(.js_swapped_row) .item-status').each(function() {
            var status = $(this).text().trim().toUpperCase();
            if (status === 'PENDIENTE') {
                hasPending = true;
            } else if (status === 'RECHAZADO') {
                hasRejected = true;
            }
        });
        
        var hasChanges = hasRejected || $swappedRows.length > 0 || $newRows.length > 0;
        
        if (hasPending) {
            $btn.prop('disabled', true).html('<i class="fa fa-paper-plane me-1"/> Enviar Propuesta');
        } else if (hasChanges) {
            $btn.prop('disabled', false).html('<i class="fa fa-paper-plane me-1"/> Enviar Propuesta');
        } else {
            $btn.prop('disabled', false).html('<i class="fa fa-check me-1"/> Aprobar Propuesta');
        }
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
                $btn.removeClass('btn-primary').addClass('btn-success').html('<i class="fa fa-check"/>');
                
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
     * Maneja la aprobación de una línea extra
     */
    _onApproveExtraLine: function (ev) {
        this._updateExtraLine(ev, 'aprobado');
    },

    /**
     * Maneja el rechazo de una línea extra
     */
    _onRejectExtraLine: function (ev) {
        this._updateExtraLine(ev, 'rechazado');
    },

    /**
     * Revierte una línea extra a estado pendiente
     */
    _onPendingExtraLine: function (ev) {
        this._updateExtraLine(ev, 'pendiente');
    },

    /**
     * Envía la actualización de la línea extra al servidor dinámicamente
     */
    _updateExtraLine: function (ev, action) {
        var $btn = $(ev.currentTarget);
        var lineId = $btn.data('line-id');
        var lineType = $btn.data('line-type');
        
        if (!lineId || !lineType) {
            console.error("TallerShop: Faltan datos de la línea extra (line-id o line-type)");
            return;
        }

        $btn.prop('disabled', true);

        this._performRPC('/taller/orden/linea/extra/update', {
            line_id: lineId,
            line_type: lineType,
            action: action
        }).then((data) => {
            if (data && data.success) {
                // Actualizar UI dinámicamente
                var $row = $btn.closest('tr');
                if (action === 'pendiente') {
                    $row.find('.js_action_buttons').attr('style', '');
                    $row.find('.js_undo_buttons').attr('style', 'display:none !important;');
                } else {
                    $row.find('.js_action_buttons').attr('style', 'display:none !important;');
                    $row.find('.js_undo_buttons').attr('style', '');
                }
                
                var $badge = $row.find('.item-status');
                $badge.removeClass('bg-warning bg-success bg-danger bg-info text-dark text-white');
                if (action === 'pendiente') $badge.addClass('bg-warning text-dark').text('PENDIENTE');
                else if (action === 'aprobado') $badge.addClass('bg-success text-white').text('APROBADO');
                else if (action === 'rechazado') $badge.addClass('bg-danger text-white').text('RECHAZADO');
                
                this._updateProposalButtonState($row.closest('.modal'));
            } else {
                alert(data.error || "Error al actualizar la línea extra");
            }
            $btn.prop('disabled', false);
        }).catch((err) => {
            console.error("TallerShop: Error en la actualización de línea extra", err);
            $btn.prop('disabled', false);
        });
    },

    _onSwapLine: function (ev) {
        var $btn = $(ev.currentTarget);
        var $row = $btn.closest('tr');
        var lineType = $row.data('type'); // 'servicio' or 'repuesto'
        
        // Ocultar botones y tachar la línea original
        $row.find('.js_action_buttons').hide();
        $row.addClass('text-decoration-line-through text-muted js_swapped_row');
        
        var $modal = $row.closest('.modal');
        var ordenId = $modal.find('.js_submit_client_proposal').data('orden-id');
        
        var newRowHtml = `
            <tr class="js_new_propuesta_row bg-light align-middle" data-type="${lineType}" data-swap-target="${$row.attr('id')}">
                <td>
                    <div class="d-flex gap-2 align-items-center">
                        <div style="flex: 3; min-width: 0;">
                            <button type="button" class="btn btn-outline-primary btn-sm w-100 text-start bg-white js_open_catalog_btn shadow-sm" style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                                <i class="fa fa-search me-1 text-muted"></i> <span class="js_selected_product_text text-dark">Seleccionar ${lineType}...</span>
                            </button>
                            <input type="hidden" class="js_propuesta_select" required="required"/>
                        </div>
                        <input type="text" class="form-control form-control-sm js_propuesta_note shadow-sm" placeholder="Nota o especificación extra..." required="required" style="flex: 1; min-width: 0;"/>
                    </div>
                </td>
                <td class="text-center">
                    <input type="number" class="form-control form-control-sm js_propuesta_qty shadow-sm" value="1" min="1" required="required" style="width: 70px; margin: 0 auto;"/>
                </td>
                <td colspan="2">
                    <span class="badge bg-secondary px-2 py-1">Intercambio</span>
                </td>
                <td class="text-end">
                    <button type="button" class="btn btn-sm btn-light text-danger border js_cancel_swap" title="Cancelar Intercambio"><i class="fa fa-undo"></i></button>
                </td>
            </tr>
        `;
        var $newRow = $(newRowHtml);
        // Insertar la fila de reemplazo justo encima de la original
        $row.before($newRow);
        this._updateProposalButtonState($modal);
    },

    _onCancelSwap: function(ev) {
        var $newRow = $(ev.currentTarget).closest('.js_new_propuesta_row');
        var targetId = $newRow.data('swap-target');
        var $targetRow = $('#' + targetId);
        
        $targetRow.removeClass('text-decoration-line-through text-muted js_swapped_row');
        $targetRow.find('.js_action_buttons').show();
        $newRow.remove();
        this._updateProposalButtonState($targetRow.closest('.modal'));
    },

    _onAddNewLine: function(ev) {
        var $btn = $(ev.currentTarget);
        var lineType = $btn.data('type'); // 'servicio' or 'repuesto'
        var $modal = $btn.closest('.modal');
        var ordenId = $modal.find('.js_submit_client_proposal').data('orden-id');
        var $tbody = $modal.find('.js_items_tbody_' + lineType);
        $tbody.find('.js_empty_placeholder_row').remove();
        
        var newRowHtml = `
            <tr class="js_new_propuesta_row bg-light align-middle" data-type="${lineType}">
                <td>
                    <div class="d-flex gap-2 align-items-center">
                        <div style="flex: 3; min-width: 0;">
                            <button type="button" class="btn btn-outline-primary btn-sm w-100 text-start bg-white js_open_catalog_btn shadow-sm" style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                                <i class="fa fa-search me-1 text-muted"></i> <span class="js_selected_product_text text-dark">Seleccionar ${lineType}...</span>
                            </button>
                            <input type="hidden" class="js_propuesta_select" required="required"/>
                        </div>
                        <input type="text" class="form-control form-control-sm js_propuesta_note shadow-sm" placeholder="Nota o especificación extra..." required="required" style="flex: 1; min-width: 0;"/>
                    </div>
                </td>
                <td class="text-center">
                    <input type="number" class="form-control form-control-sm js_propuesta_qty shadow-sm" value="1" min="1" required="required" style="width: 70px; margin: 0 auto;"/>
                </td>
                <td colspan="2">
                    <span class="badge bg-primary px-2 py-1">Nuevo</span>
                </td>
                <td class="text-end">
                    <button type="button" class="btn btn-sm btn-light text-danger border js_remove_new_line" title="Eliminar Línea"><i class="fa fa-trash"></i></button>
                </td>
            </tr>
        `;
        var $newRow = $(newRowHtml);
        $tbody.append($newRow);
        this._updateProposalButtonState($modal);
    },

    _onRemoveNewLine: function(ev) {
        var $modal = $(ev.currentTarget).closest('.modal');
        $(ev.currentTarget).closest('tr').remove();
        this._updateProposalButtonState($modal);
    },

    _onSubmitClientProposal: function(ev) {
        var $btn = $(ev.currentTarget);
        var ordenId = $btn.data('orden-id');
        var $modal = $btn.closest('.modal');
        
        var $swappedRows = $modal.find('.js_swapped_row');
        var $newRows = $modal.find('.js_new_propuesta_row');
        var proposalNotes = ($modal.find('.js_proposal_notes').val() || '').trim();
        
        // Check status of existing items
        var hasPending = false;
        
        $modal.find('.item-row:not(.js_swapped_row) .item-status').each(function() {
            var status = $(this).text().trim().toUpperCase();
            if (status === 'PENDIENTE') {
                hasPending = true;
            }
        });
        
        if (hasPending) {
            alert("Por favor, aprueba o rechaza todos los items propuestos (o cámbialos por otros) antes de enviar la propuesta.");
            return;
        }

        // Validate required fields for NEW ROWS ONLY
        var isValid = true;
        $newRows.each(function() {
            var $row = $(this);
            var $btnSelect = $row.find('.js_open_catalog_btn');
            var $hiddenSelect = $row.find('.js_propuesta_select');
            var $qtyInput = $row.find('.js_propuesta_qty');
            
            // Validate search/select
            if (!$hiddenSelect.val()) {
                $btnSelect.addClass('border-danger text-danger').removeClass('btn-outline-primary');
                isValid = false;
            } else {
                $btnSelect.removeClass('border-danger text-danger').addClass('btn-outline-primary');
            }
            
            // Validate qty
            if ($qtyInput.prop('required') && !$qtyInput.val()) {
                $qtyInput.addClass('is-invalid');
                isValid = false;
            } else {
                $qtyInput.removeClass('is-invalid');
            }
        });
        if (!isValid) {
            alert("Por favor selecciona el producto y cantidad en todos los nuevos items.");
            return;
        }

        var originalBtnLabel = $btn.html();
        var action = proposalNotes === '' ? 'aprobar' : 'devolver';
        var loadingText = action === 'aprobar' ? 'Aprobando' : 'Enviando';
        $btn.prop('disabled', true)
            .addClass('btn-sending')
            .html(loadingText + '<span class="taller-dots"><span></span><span></span><span></span></span>');

        var rejectPromises = [];
        var self = this;
        $swappedRows.each(function() {
            var lineId = parseInt($(this).data('id'));
            var lineType = $(this).data('type');
            rejectPromises.push(
                self._performRPC('/taller/orden/linea/extra/update', {
                    line_id: lineId,
                    line_type: lineType,
                    action: 'rechazado'
                })
            );
        });
        
        Promise.all(rejectPromises).then(() => {
            var servicios = [];
            var repuestos = [];
            $newRows.each(function() {
                var $row = $(this);
                var type = $row.data('type');
                var prodId = $row.find('.js_propuesta_select').val();
                var qty = parseFloat($row.find('.js_propuesta_qty').val());
                var lineNote = $row.find('.js_propuesta_note').val();
                
                var item = {
                    producto_id: prodId,
                    cantidad: qty,
                    nota: lineNote
                };
                if (type === 'servicio') { servicios.push(item); }
                else { repuestos.push(item); }
            });

            this._performRPC('/taller/orden/propuesta/crear', {
                orden_id: parseInt(ordenId),
                notas: proposalNotes,
                servicios: servicios,
                repuestos: repuestos,
                action: action
            }).then((data) => {
                if (data && data.success) {
                    window.location.reload();
                } else {
                    alert(data.error || "Error al enviar la propuesta.");
                    $btn.prop('disabled', false).removeClass('btn-sending').html(originalBtnLabel);
                }
            }).catch((err) => {
                console.error("TallerShop: Error", err);
                alert("Error de red al enviar la propuesta.");
                $btn.prop('disabled', false).removeClass('btn-sending').html(originalBtnLabel);
            });
        }).catch((err) => {
            console.error("Error rechazando originales:", err);
            alert("Hubo un problema al procesar los intercambios.");
            $btn.prop('disabled', false).removeClass('btn-sending').html(originalBtnLabel);
        });
    },

    _onOpenCatalog: function(ev) {
        var $btn = $(ev.currentTarget);
        var $row = $btn.closest('tr');
        var lineType = $row.data('type'); // 'servicio' or 'repuesto'
        
        // Guardamos la fila objetivo a la que vamos a inyectar el item seleccionado
        this._currentCatalogTargetRow = $row;
        
        var $modalDetalle = $row.closest('.modal');
        var ordenId = $modalDetalle.find('.js_submit_client_proposal').data('orden-id');
        
        var listId = `datalist_${lineType}s_${ordenId}`;
        var $datalist = $('#' + listId);
        
        var html = '';
        var colorClass = lineType === 'servicio' ? 'text-primary' : 'text-success';
        var bgClass = lineType === 'servicio' ? 'bg-primary-subtle' : 'bg-success-subtle';
        var iconClass = lineType === 'servicio' ? 'fa-wrench' : 'fa-cogs';
        
        $datalist.find('option').each(function() {
            var id = $(this).attr('data-value');
            var text = $(this).attr('value');
            var parts = text.split(' - $');
            var name = $(this).attr('data-name') || parts[0];
            var priceNum = parseFloat($(this).attr('data-price') || '0');
            var price = parts.length > 1 ? '$' + parts[1] : ('$' + priceNum.toFixed(2));
            
            html += `
                <div class="col-md-6 col-lg-4 catalog-item" data-name="${name.toLowerCase()}" data-price="${priceNum}">
                    <div class="card h-100 border-0 shadow-sm catalog-card js_select_catalog_item overflow-hidden" data-id="${id}" data-name="${name}" style="cursor: pointer; transition: transform 0.2s;">
                        <div class="bg-light text-center position-relative" style="height: 120px; display: flex; align-items: center; justify-content: center;">
                            <img src="/web/image/product.product/${id}/image_128" alt="${name}" style="max-height: 100px; max-width: 100%; object-fit: contain;" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';"/>
                            <div style="display: none; align-items: center; justify-content: center; width: 100%; height: 100%;">
                                <div class="${bgClass} ${colorClass} rounded-circle d-inline-flex align-items-center justify-content-center" style="width: 45px; height: 45px;">
                                    <i class="fa ${iconClass} fs-5"></i>
                                </div>
                            </div>
                        </div>
                        <div class="card-body p-3 text-center d-flex flex-column">
                            <h6 class="fw-bold mb-2 text-dark text-truncate" style="font-size: 0.9rem;" title="${name}">${name}</h6>
                            <div class="mt-auto">
                                <span class="badge bg-dark rounded-pill px-3 py-2" style="font-size: 0.85rem;">${price}</span>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });
        
        $('#catalogProductsContainer').html(html);
        $('#catalogSearchInput').val('');
        $('#catalogSortSelect').val('name_asc');
        $('#catalogEmptyState').addClass('d-none');
        
        var title = lineType === 'servicio' ? '<i class="fa fa-wrench me-2"></i> Seleccionar Servicio' : '<i class="fa fa-cogs me-2"></i> Seleccionar Repuesto';
        $('#modalProductCatalogTitle').html(title);
        
        // Show modal via Bootstrap
        var modalEl = document.getElementById('modalProductCatalog');
        if (typeof bootstrap !== 'undefined' && bootstrap.Modal) {
            var m = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
            m.show();
        } else if (typeof jQuery !== 'undefined') {
            jQuery(modalEl).modal('show');
        }
    },

    _onCatalogSearch: function(ev) {
        var val = $(ev.currentTarget).val().toLowerCase();
        var $items = $('#catalogProductsContainer .catalog-item');
        var visibleCount = 0;
        
        $items.each(function() {
            if ($(this).data('name').indexOf(val) > -1) {
                $(this).removeClass('d-none');
                visibleCount++;
            } else {
                $(this).addClass('d-none');
            }
        });
        
        if (visibleCount === 0) {
            $('#catalogEmptyState').removeClass('d-none');
        } else {
            $('#catalogEmptyState').addClass('d-none');
        }
    },

    _onCatalogSort: function(ev) {
        var sortType = $(ev.currentTarget).val();
        var $container = $('#catalogProductsContainer');
        var $items = $container.children('.catalog-item');
        
        $items.sort(function(a, b) {
            var $a = $(a);
            var $b = $(b);
            if (sortType === 'price_asc') {
                return parseFloat($a.data('price')) - parseFloat($b.data('price'));
            } else if (sortType === 'price_desc') {
                return parseFloat($b.data('price')) - parseFloat($a.data('price'));
            } else { // name_asc
                var nameA = $a.data('name').toLowerCase();
                var nameB = $b.data('name').toLowerCase();
                if (nameA < nameB) return -1;
                if (nameA > nameB) return 1;
                return 0;
            }
        });
        
        $container.append($items);
    },

    _onSelectCatalogItem: function(ev) {
        var $item = $(ev.currentTarget);
        var id = $item.data('id');
        var name = $item.data('name');
        
        if (this._currentCatalogTargetRow) {
            var $row = this._currentCatalogTargetRow;
            $row.find('.js_propuesta_select').val(id);
            $row.find('.js_selected_product_text').text(name);
            $row.find('.js_open_catalog_btn').removeClass('border-danger text-danger').addClass('btn-outline-primary');
        }
        
        var modalEl = document.getElementById('modalProductCatalog');
        if (typeof bootstrap !== 'undefined' && bootstrap.Modal) {
            var m = bootstrap.Modal.getInstance(modalEl);
            if (m) m.hide();
        } else if (typeof jQuery !== 'undefined') {
            jQuery(modalEl).modal('hide');
        }
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
