# -*- coding: utf-8 -*-
from openerp import http

# class SaleOrderExtended(http.Controller):
#     @http.route('/sale_order_extended/sale_order_extended/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_order_extended/sale_order_extended/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_order_extended.listing', {
#             'root': '/sale_order_extended/sale_order_extended',
#             'objects': http.request.env['sale_order_extended.sale_order_extended'].search([]),
#         })

#     @http.route('/sale_order_extended/sale_order_extended/objects/<model("sale_order_extended.sale_order_extended"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_order_extended.object', {
#             'object': obj
#         })