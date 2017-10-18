# -*- coding: utf-8 -*-
from openerp import http

# class MrpBomExtended(http.Controller):
#     @http.route('/mrp_bom_extended/mrp_bom_extended/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mrp_bom_extended/mrp_bom_extended/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mrp_bom_extended.listing', {
#             'root': '/mrp_bom_extended/mrp_bom_extended',
#             'objects': http.request.env['mrp_bom_extended.mrp_bom_extended'].search([]),
#         })

#     @http.route('/mrp_bom_extended/mrp_bom_extended/objects/<model("mrp_bom_extended.mrp_bom_extended"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mrp_bom_extended.object', {
#             'object': obj
#         })