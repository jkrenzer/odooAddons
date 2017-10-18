# -*- coding: utf-8 -*-
from openerp import http

# class MrpOperationExtensionHours(http.Controller):
#     @http.route('/mrp_operation_extension_hours/mrp_operation_extension_hours/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mrp_operation_extension_hours/mrp_operation_extension_hours/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mrp_operation_extension_hours.listing', {
#             'root': '/mrp_operation_extension_hours/mrp_operation_extension_hours',
#             'objects': http.request.env['mrp_operation_extension_hours.mrp_operation_extension_hours'].search([]),
#         })

#     @http.route('/mrp_operation_extension_hours/mrp_operation_extension_hours/objects/<model("mrp_operation_extension_hours.mrp_operation_extension_hours"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mrp_operation_extension_hours.object', {
#             'object': obj
#         })