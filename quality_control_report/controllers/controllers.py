# -*- coding: utf-8 -*-
from openerp import http

# class QualityControlReport(http.Controller):
#     @http.route('/quality_control_report/quality_control_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/quality_control_report/quality_control_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('quality_control_report.listing', {
#             'root': '/quality_control_report/quality_control_report',
#             'objects': http.request.env['quality_control_report.quality_control_report'].search([]),
#         })

#     @http.route('/quality_control_report/quality_control_report/objects/<model("quality_control_report.quality_control_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('quality_control_report.object', {
#             'object': obj
#         })