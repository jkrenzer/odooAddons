# -*- coding: utf-8 -*-
from openerp import http

# class ReportGermanLetterLayout(http.Controller):
#     @http.route('/report_german_letter_layout/report_german_letter_layout/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_german_letter_layout/report_german_letter_layout/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_german_letter_layout.listing', {
#             'root': '/report_german_letter_layout/report_german_letter_layout',
#             'objects': http.request.env['report_german_letter_layout.report_german_letter_layout'].search([]),
#         })

#     @http.route('/report_german_letter_layout/report_german_letter_layout/objects/<model("report_german_letter_layout.report_german_letter_layout"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_german_letter_layout.object', {
#             'object': obj
#         })