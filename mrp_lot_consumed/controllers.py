# -*- coding: utf-8 -*-
from openerp import http

# class MrpLotConsumed(http.Controller):
#     @http.route('/mrp_lot_consumed/mrp_lot_consumed/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mrp_lot_consumed/mrp_lot_consumed/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mrp_lot_consumed.listing', {
#             'root': '/mrp_lot_consumed/mrp_lot_consumed',
#             'objects': http.request.env['mrp_lot_consumed.mrp_lot_consumed'].search([]),
#         })

#     @http.route('/mrp_lot_consumed/mrp_lot_consumed/objects/<model("mrp_lot_consumed.mrp_lot_consumed"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mrp_lot_consumed.object', {
#             'object': obj
#         })