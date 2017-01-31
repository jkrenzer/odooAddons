# -*- coding: utf-8 -*-
from openerp import http

# class StockPickingUniqueSerial(http.Controller):
#     @http.route('/stock_picking_unique_serial/stock_picking_unique_serial/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_picking_unique_serial/stock_picking_unique_serial/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_picking_unique_serial.listing', {
#             'root': '/stock_picking_unique_serial/stock_picking_unique_serial',
#             'objects': http.request.env['stock_picking_unique_serial.stock_picking_unique_serial'].search([]),
#         })

#     @http.route('/stock_picking_unique_serial/stock_picking_unique_serial/objects/<model("stock_picking_unique_serial.stock_picking_unique_serial"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_picking_unique_serial.object', {
#             'object': obj
#         })