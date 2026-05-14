# -*- coding: utf-8 -*-
# from odoo import http


# class TallerVehiculo(http.Controller):
#     @http.route('/taller_vehiculo/taller_vehiculo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/taller_vehiculo/taller_vehiculo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('taller_vehiculo.listing', {
#             'root': '/taller_vehiculo/taller_vehiculo',
#             'objects': http.request.env['taller_vehiculo.taller_vehiculo'].search([]),
#         })

#     @http.route('/taller_vehiculo/taller_vehiculo/objects/<model("taller_vehiculo.taller_vehiculo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('taller_vehiculo.object', {
#             'object': obj
#         })

