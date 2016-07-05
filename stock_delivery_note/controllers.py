# -*- coding: utf-8 -*-
from openerp import http

# class StockPickingDeliveryNote(http.Controller):
#     @http.route('/stock_picking_delivery_note/stock_picking_delivery_note/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_picking_delivery_note/stock_picking_delivery_note/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_picking_delivery_note.listing', {
#             'root': '/stock_picking_delivery_note/stock_picking_delivery_note',
#             'objects': http.request.env['stock_picking_delivery_note.stock_picking_delivery_note'].search([]),
#         })

#     @http.route('/stock_picking_delivery_note/stock_picking_delivery_note/objects/<model("stock_picking_delivery_note.stock_picking_delivery_note"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_picking_delivery_note.object', {
#             'object': obj
#         })